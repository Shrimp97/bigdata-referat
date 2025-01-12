import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# get single csv file
data = pd.read_csv("../data/flight_data_prepared1.csv")
# data = pd.read_csv("../data/flight_data_prepared1.csv")

### Korrelation ###
# check for correlation between features and target variable
# select numerical columns
numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns

# calculate correlation matrix
corr_matrix = data[numerical_cols].corr()

# plot heatmap of correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Korrelationsmatrix')
plt.show()

plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix[['arrival_delay']].sort_values(by='arrival_delay', ascending=False), annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Correlation of Arrival Delay with Other Variables')
plt.show()

### Streudiagramm ###

x = data["departure_delay"].values.reshape(-1, 1)
y = data["arrival_delay"].values.reshape(-1, 1)

# Create a DataFrame for Plotly
plot_data = pd.DataFrame({
    "Departure Delay": x.flatten(),
    "Arrival Delay": y.flatten(),
})

# Create the plot
fig = px.scatter(plot_data, x="Departure Delay", y="Arrival Delay", title="Arrival Delay vs Departure Delay")
fig.update_xaxes(
    title=dict(
        text="Departure Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14),
)
fig.update_yaxes(
    title=dict(
        text="Arrival Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14),
)
fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(size=16)
    ),
    title=dict(
        font=dict(size=24)
    )
)
fig.show()

# Filter rows that have no delay (all delay columns are 0) but still have an arrival_delay.
# This ensures only rows with meaningful delay information or early/ontime arrivals are kept.
data = data[(((data["delay_carrier"] != 0) | (data["delay_weather"] != 0) | 
              (data["delay_national_aviation_system"] != 0) | (data["delay_security"] != 0) | 
              (data["delay_late_aircraft_arrival"] != 0)) | 
             ((data["delay_carrier"] == 0) & (data["delay_weather"] == 0) & 
              (data["delay_national_aviation_system"] == 0) & (data["delay_security"] == 0) & 
              (data["delay_late_aircraft_arrival"] == 0) & (data["arrival_delay"] <= 0)))]


# select numerical columns
numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns

# calculate correlation matrix
corr_matrix = data[numerical_cols].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix[['arrival_delay']].sort_values(by='arrival_delay', ascending=False), annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', annot_kws={'size': 14})
plt.title('Correlation of Arrival Delay with Other Variables', fontsize=20)
plt.xlabel('Variables', fontsize=20)
plt.ylabel('Variables', fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


### nach Airports ###

# Filtere nur positive departure_delay-Werte
positive_data = data[data['departure_delay'] > 0]

# Anzahl der verschiedenen Flughäfen
print("Anzahl der verschiedenen Flughäfen:")
print(positive_data['origin_airport'].nunique())

# Berechne den Median der Abflugverspätung pro Flughafen
median_delay_per_airport = positive_data.groupby('origin_airport')['departure_delay'].median().reset_index()

# Sortiere nach der Spalte 'departure_delay' in absteigender Reihenfolge
median_delay_per_airport = median_delay_per_airport.sort_values(by='departure_delay', ascending=False)

# create bar chart
fig = px.bar(median_delay_per_airport, x='origin_airport', y='departure_delay')
fig.update_layout(
    title=dict(
        text="Median Departure Delay per Airport",
        font=dict(size=30)  # Schriftgröße anpassen
    )
)
# Achsenbeschriftung
fig.update_xaxes(
    title=dict(
        text="Origin Airport (origin_airport)",
        font=dict(size=30)
    ),
    tickfont=dict(size=14),
    tickangle=45
)
fig.update_yaxes(
    title=dict(
        text="Median Departure Delay (departure_delay) in Minutes",
        font=dict(size=30)
    ),
    tickfont=dict(size=18),
)

fig.show()

# select top 5 airports with highest median departure delay
top5_airports = median_delay_per_airport.head(5)

# create bar chart
fig = px.bar(top5_airports, x='origin_airport', y='departure_delay')
fig.update_layout(
    title=dict(
        text="Top 5 Airports by Median Departure Delay",
        font=dict(size=30)
    )
)
# Achsenbeschriftung
fig.update_xaxes(
    title=dict(
        text="Origin Airport (origin_airport)",
        font=dict(size=30)
    ),
    tickfont=dict(size=30),
    tickangle=45
)
fig.update_yaxes(
    title=dict(
        text="Median Departure Delay (departure_delay) in Minutes",
        font=dict(size=30)
    ),
    tickfont=dict(size=30),
)

fig.show()


# select bottom 5 airports with lowest median departure delay
bottom5_airports = median_delay_per_airport.tail(5)

# Erstelle das interaktive Balkendiagramm
fig = px.bar(bottom5_airports, x='origin_airport', y='departure_delay', title="Bottom 5 Airports by Median Departure Delay")
fig.update_layout(
    title=dict(
        text="Bottom 5 Airports by Median Departure Delay",
        font=dict(size=30)
    )
)
# Achsenbeschriftung
fig.update_xaxes(
    title=dict(
        text="Origin Airport (origin_airport)",
        font=dict(size=30)
    ),
    tickfont=dict(size=30),
    tickangle=45
)
fig.update_yaxes(
    title=dict(
        text="Median Departure Delay (departure_delay) in Minutes",
        font=dict(size=30)
    ),
    tickfont=dict(size=30),
)

fig.show()


### Streudiagramm ###

x = data["departure_delay"].values.reshape(-1, 1)
y = data["arrival_delay"].values.reshape(-1, 1)

# Create a DataFrame for Plotly
plot_data = pd.DataFrame({
    "Departure Delay": x.flatten(),
    "Arrival Delay": y.flatten(),
})

# Create the plot
fig = px.scatter(plot_data, x="Departure Delay", y="Arrival Delay", title="Arrival Delay vs Departure Delay")
fig.update_xaxes(
    title=dict(
        text="Departure Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14),
)
fig.update_yaxes(
    title=dict(
        text="Arrival Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14),
)
fig.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(size=16)
    ),
    title=dict(
        font=dict(size=24)
    )
)
fig.show()
