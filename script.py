# Use data from sportpesa to search through betika.com and combine all that to a csv file.
"""
Links to articles on arbitrage betting: 
    --> https://www.sbo.net/strategy/arbitrage-betting/
    --> https://thearbacademy.com/arbitrage-calculation/
"""
from utilities.helpers import adjust_csv, round_float
import csv
import utilities.sportpesa_data as sp


INV = 50000


def calculate_arbitrage(arr) -> list:
    """
    INFO: This function analyzes the data given and checks for arbitrage betting opportunities.
    - To calculate the arbitrage percentage, the following formula is used:
        Arbitrage % = ((1 / decimal odds for outcome A) x 100) + ((1 / decimal odds for outcome B) x 100)
    - If the result here is below 100% you have got yourself an arbitrage bet (Extremely rare stuff).

    (Additional Info): Given the above analogy, you would think that we'd have to calculate the Arbitrage percentage
    using sportpesa gg as outcome A and betika no_gg as outcome B, and also calculate the same using sportpesa no_gg
    as outcome A and betika gg as outcome B, so that we can use the percentage that is the lower of the two. However,
    all we have to do, is pick the larger gg value from the two sites, and use the no_gg value from the other site.

    - In case you are lucky enough:
        - Profit calculation is done as follows (Here, we use ksh 50,000):
            # Profit = Investment - ((Investment / A_odds) + (Investment / B_odds))           
        - Calculation of stake on individual outcome using the same investment amount:
            # Outcome_A_stake = Investment / A_odds, 
            # Outcome_B_stake = Investment / B_odds
    """

    count = 0
    arbs = []
    _profit = 0
    for entry in arr:
        # Get rid of entries with 'None' values
        if "SP" not in entry or "BK" not in entry or not entry["BK"]:
            arr.remove(entry)
            continue

        # Get the bigger gg values
        gg = 0
        gg_site = None
        no_gg = 0
        no_gg_site = None

        if entry["SP"]["GG"] > entry["BK"]["GG"]:
            gg = entry["SP"]["GG"]
            gg_site = "Sportpesa"
            no_gg = entry["BK"]["NO_GG"]
            no_gg_site = "Betika"
        else:
            gg = entry["BK"]["GG"]
            gg_site = "Betika"
            no_gg = entry["SP"]["NO_GG"]
            no_gg_site = "Sportpesa"

        arb_p = ((1/gg) * 100) + ((1/no_gg) * 100)
        arbitrage_percentage = round_float(arb_p)
        entry["Arb_Percentage"] = arbitrage_percentage

        if arbitrage_percentage < 100.00:
            stakes = calculate_stakes(gg, no_gg)
            entry["Stakes"] = {
                "GG": [stakes[0], gg_site],
                "NO_GG": [stakes[1], no_gg_site]
            }

            _profit = calculate_profit(gg, no_gg)
            entry["Profit"] = _profit

            arbs.append(entry)
            count += 1

    # Show output...
    print(
        f"\n Number of Arbitrage opportunities in {len(arr)} entries ---> {count} : \n")
    if arbs:
        for i in arbs:
            print(i)
            print(f"\n-----------ANALYSIS----------(Total Stake --> {INV})\n")
            print(
                f"Stake on GG ({i['Stakes']['GG'][1]}): {i['Stakes']['GG'][0]} \nStake on NO_GG ({i['Stakes']['NO_GG'][1]}): {i['Stakes']['NO_GG'][0]}")
            print(f"Profit from Ksh {INV} = Ksh {i['Profit']}")
    print("\n" * 3)

    return arr


# Profit calculation
def calculate_profit(outcome_a_odds, outcome_b_odds) -> float:
    profit = round_float(INV - ((INV / outcome_a_odds) + (INV / outcome_b_odds)))
    return profit


# Calculating stakes
def calculate_stakes(outcome_a_odds, outcome_b_odds) -> list:
    return [round_float(INV / outcome_a_odds, 2), round_float(INV / outcome_b_odds, 2)]


# Compiled report in excel format
def compiled_data(lst) -> None:
    """
    INFO: Returns a csv file with all the entries with their arbitrage percentage.
    """

    header_values = ["Teams", "Start_time", "SP_event_id", "SP_GG_odds",
                     "SP_NOGG_odds", "BK_GG_odds", "BK_NOGG_odds", "Arb_Percentage", "Profit",
                     "SP_GG_stake", "SP_NOGG_stake", "BK_GG_stake", "BK_NOGG_stake",
                     ]
    with open("all_entries.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header_values)
        writer.writeheader()

        for obj in lst:
            row = {
                "Teams": obj["teams"],
                "Start_time": obj["start_time"],
                "SP_event_id": obj["event_id"],
                "SP_GG_odds": obj["SP"]["GG"],
                "SP_NOGG_odds": obj["SP"]["NO_GG"],
                "BK_GG_odds": obj["BK"]["GG"],
                "BK_NOGG_odds": obj["BK"]["NO_GG"],
                "Arb_Percentage": obj["Arb_Percentage"],
                "Profit": obj.get("Profit", "N/A"),
                "SP_GG_stake": obj["Stakes"]["GG"][0] if "Stakes" in obj and obj["Stakes"]["GG"][1] == "Sportpesa" else "N/A",
                "SP_NOGG_stake": obj["Stakes"]["NO_GG"][0] if "Stakes" in obj and obj["Stakes"]["NO_GG"][1] == "Sportpesa" else "N/A",
                "BK_GG_stake": obj["Stakes"]["GG"][0] if "Stakes" in obj and obj["Stakes"]["GG"][1] == "Betika" else "N/A",
                "BK_NOGG_stake": obj["Stakes"]["NO_GG"][0] if "Stakes" in obj and obj["Stakes"]["NO_GG"][1] == "Betika" else "N/A"
            }

            writer.writerow(row)

    adjust_csv("all_entries.csv")


if __name__ == "__main__":
    initial_data = sp.get_sportpesa_data()

    if initial_data:
        import utilities.betika_data as bd
        updated_array = bd.add_betika_data(initial_data)
        new_arr = calculate_arbitrage(updated_array)
        compiled_data(new_arr)
    else:
        print("No data from the two sites")
