import pandas as pd

# get single csv file
data = pd.read_csv("../data/flight_data.csv")

# print a preview of the dataset
print("preview of the dataset:")
print(data.head())

# show shape of the dataset
print("\nshape of the dataset:")
print(data.shape)

# show data types
print("\ndata types:")
print(data.dtypes)


### rename spelling mistake ###
data.rename(columns={"delay_late_aircarft_arrival": "delay_late_aircraft_arrival"}, inplace=True)

### drop cancelled flights ###
# drop collumns with cancelled_code != "N"
data = data[data["cancelled_code"] == "N"]

### handle missing values ###
# show missing values
print("\nmissing values:")
print(data.isnull().sum())

# print number of rows before dropping
row_count_before = data.shape[0]
print("\nrow count before dropping:", row_count_before)

# drop missing values
data = data.dropna()

print("\nmissing values after dropping:")
print(data.isnull().sum())

# print number of rows after dropping
print("\nrow count before dropping:", row_count_before)
row_count_after = data.shape[0]
print("row count after dropping:", row_count_after)

# print number of removed rows
removed_rows = row_count_before - row_count_after
print("removed rows:", removed_rows)

### handle unimportant columns ###
# drop flight_number, date, tail_number, cancelled_code, STATION_x, STATION_y, year, scheduled_departure_dt, scheduled_arrival_dt, actual_departure_dt, actual_arrival_dt, scheduled_elapsed_time
columns_to_drop = ['flight_number', 'date', 'tail_number', 'cancelled_code', 'STATION_x', 'STATION_y', 'year', 'scheduled_departure_dt', 'scheduled_arrival_dt', 'actual_departure_dt', 'actual_arrival_dt', 'scheduled_elapsed_time'] 
data.drop(columns=columns_to_drop, inplace=True)

# show data after preparation
print("\nData after preparation:")
print(data.dtypes)

#save to new csv file
data.to_csv("../data/flight_data_prepared1.csv", index=False)