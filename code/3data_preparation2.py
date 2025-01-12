import pandas as pd
import pandas as pd

# get single csv file
data = pd.read_csv("../data/flight_data_prepared1.csv")

# Filter rows that have no delay (all delay columns are 0) but still have an arrival_delay.
# This ensures only rows with meaningful delay information or early/ontime arrivals are kept.
data = data[(((data["delay_carrier"] != 0) | (data["delay_weather"] != 0) | 
              (data["delay_national_aviation_system"] != 0) | (data["delay_security"] != 0) | 
              (data["delay_late_aircraft_arrival"] != 0)) | 
             ((data["delay_carrier"] == 0) & (data["delay_weather"] == 0) & 
              (data["delay_national_aviation_system"] == 0) & (data["delay_security"] == 0) & 
              (data["delay_late_aircraft_arrival"] == 0) & (data["arrival_delay"] <= 0)))]

### handle unimportant columns ###
# drop flight_number, date, tail_number, cancelled_code, STATION_x, STATION_y, year, scheduled_departure_dt, scheduled_arrival_dt, actual_departure_dt, actual_arrival_dt, scheduled_elapsed_time
columns_to_drop = ['carrier_code', 'destination_airport', 'delay_carrier', 'delay_weather', 'delay_national_aviation_system', 'delay_security', 'delay_late_aircraft_arrival', 'month', 'day', 'weekday', 'HourlyDryBulbTemperature_x', 'HourlyPrecipitation_x', 'HourlyStationPressure_x', 'HourlyVisibility_x', 'HourlyWindSpeed_x', 'HourlyDryBulbTemperature_y', 'HourlyPrecipitation_y', 'HourlyStationPressure_y', 'HourlyVisibility_y', 'HourlyWindSpeed_y'] 
data.drop(columns=columns_to_drop, inplace=True)

#filter data by origin_airport
dataTopAirport = data[data["origin_airport"] == "SHD"]
dataBottomAirport = data[data["origin_airport"] == "AKN"]
dataLaxAirport = data[data["origin_airport"] == "LAX"]

data.drop(columns='origin_airport', inplace=True)

# show data after preparation
print("\nData after preparation:")
print(data.dtypes)


#save 3 new csv files
data.to_csv("../data/flight_data_prepared2_all.csv", index=False)
dataTopAirport.to_csv("../data/flight_data_prepared2_top.csv", index=False)
dataBottomAirport.to_csv("../data/flight_data_prepared2_bottom.csv", index=False)
dataLaxAirport.to_csv("../data/flight_data_prepared2_lax.csv", index=False)
