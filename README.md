# Arbitrage-Check
## An Arbitrage checking script written in Python using selenium
### Context
__Arbitrage__ on it's own, means leveraging market differences between two sellers to make money. This concept is legal and even encouraged in most countries as it makes markets efficient. __Arbitrage betting__, consequently, is a strategy for betting on every outcome of a sporting event in order to assure a profit, regardless of the outcome. It operates by taking advantage of differences in odds provided by several bookmakers or betting exchanges. These opportunities are however the rarest of their kind, and often generate very little profit per. They are based on the **arbitrage percentage** being less than 100%. See more on arbitrage betting and how the calculations are done [here](https://thearbacademy.com/arbitrage-calculation/) or [here](https://www.sbo.net/strategy/arbitrage-betting/).
### What the Project Does
This is thus a fun project done solely to practice scripting with selenium. It basically fetches data on events of the day from both [sportpesa](sportpesa.com) and [betika](betika.com). Data here being the teams involved in a match(event), the start time, the ID of the game on sportpesa, 'Both Teams To Score' odds on both sites, then calculates the arbitrage percentage of the valid entries collected, and writes all that to a csv file in the root folder of the project, as well as outputs any arbitrage possibility found in the said calculations. The output shows the number of entries checked,  possibilities found, and a break-down of investments and profits from any arbitrage scenario found. 
#### Output (other than the csv file):
![Command line output](/images/Sample_found_output.jpeg)<br>
As shown above, only one possibility out of 76 entries were found. Even worse, the event went ahead and got cancelled a little later that day. Tough stuff. See image below:<br>


![Event cancellation](/images/event_postponed.jpeg)<br>
### Getting the script to work
- Clone the repo.
- Create the virtual environment.
- Install dependencies from the requirement.txt file.
- Run the script.py file (the main file).
### Limitations of the project
- These possibilities are quite rare, and the ouput will almost always be zero.
- Profits of such events are also very low, probably why you have never heard of this concept.
- On the technical side, these sites are quite dynamic and errors easily come up.
- There are still more bugs and need for better error handling (in progress)