# Use data from sportpesa to search through betika.com and combine all that to a csv file.
import sportpesa_data
import betika_data


initial_data = sportpesa_data.get_sportpesa_data()
updated_array = betika_data.add_betika_data(initial_data)


for idx, item in enumerate(updated_array):
    print(f"{idx} : {item}")
