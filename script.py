# Use data from sportpesa to search through betika.com and combine all that to a csv file.
"""
Links to articles on arbitrage betting: 
    --> https://www.sbo.net/strategy/arbitrage-betting/
    --> https://thearbacademy.com/arbitrage-calculation/
"""
import sportpesa_data
import betika_data
import csv


# For further research
sample_data_arb = [
    {'teams': 'NOMME KALJU vs FLORA TALLINN', 'start_time': '20:00', 'event_id': 5038,
        'SP': {'GG': 1.72, 'NO_GG': 1.93}, 'BK': {'GG': 1.4, 'NO_GG': 2.6}},
]

INV = 50000


def calculate_arbitrage(arr) -> list:
    """
    INFO: This function analyzes the data given and checks for arbitrage betting opportunities.
    - To calculate the arbitrage percentage, the following formula is used:
        Arbitrage % = ((1 / decimal odds for outcome A) x 100) + ((1 / decimal odds for outcome B) x 100)
    - If the result here is below 100% you have got yourself an arbitrage bet (Extremely rare stuff).

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
        if not "SP" in entry or not "BK" in entry or not entry["BK"]:
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

        arbitrage_percentage = round(((1/gg) * 100) + ((1/no_gg) * 100), 2)
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
def calculate_profit(A, B) -> float:
    profit = round(INV - ((INV / A) + (INV / B)), 2)
    return profit


# Calculating stakes
def calculate_stakes(A, B) -> list:
    A_stake = round(INV / A, 2)
    B_stake = round(INV / B, 2)
    return [A_stake, B_stake]


# Compiled csv report
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


initial_data = sportpesa_data.get_sportpesa_data()

if initial_data:
    updated_array = betika_data.add_betika_data(initial_data)
    for idx, item in enumerate(updated_array):
        print(f"{idx} : {item}")
    new_arr = calculate_arbitrage(updated_array)
    compiled_data(new_arr)
else:
    print("No data from the two sites")
