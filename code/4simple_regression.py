from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


# Load data
data = pd.read_csv("../data/flight_data_prepared2_all.csv")
# data = pd.read_csv("../data/flight_data_prepared2_top.csv")
# data = pd.read_csv("../data/flight_data_prepared2_bottom.csv")
# data = pd.read_csv("../data/flight_data_prepared2_lax.csv")

# choose the features
x = data["departure_delay"].values.reshape(-1, 1)
y = data["arrival_delay"].values.reshape(-1, 1)

# Daten aufteilen und lineare Regression durchführen
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Create a model and fit it
regressor = LinearRegression()
regressor.fit(x_train, y_train) # training on the training data
beta0 = regressor.intercept_[0]
beta1 = regressor.coef_[0][0]
score = regressor.score(x_test, y_test) # score based on the test data
mylabel = f"y = {beta0:.2f} + {beta1:.2f}x, R2 = {score:.2f}"

# Make prediction on test data
y_pred = regressor.predict(x_test)

mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.2f}")

# calculate residuals
residuals = y_test - y_pred

# Homoskedastizitätstest
# Plot der Residuen gegen die Vorhersagen (Residualplot)
plt.scatter(y_pred, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Residual Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()

import scipy.stats as stats
import matplotlib.pyplot as plt

stats.probplot(residuals.flatten(), dist="norm", plot=plt)
plt.title("Q Q plot")
plt.show()

# Create a DataFrame for Plotly
plot_data = pd.DataFrame({
    "Departure Delay": x_test.flatten(),
    "Arrival Delay": y_test.flatten(),
    "Prediction": y_pred.flatten()
})

# Create the plot
fig = px.scatter(plot_data, x="Departure Delay", y="Arrival Delay", title="Arrival Delay vs Departure Delay")
fig.add_scatter(
    x=plot_data["Departure Delay"], 
    y=plot_data["Prediction"], 
    mode="lines", 
    name=f"Prediction ({mylabel})",
    line=dict(color="red", width=3),
)
fig.update_xaxes(
    title=dict(
        text="Departure Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14)
)
fig.update_yaxes(
    title=dict(
        text="Arrival Delay in seconds",
        font=dict(size=20)
    ),
    tickfont=dict(size=14)
)
fig.update_layout(
    # width=800,
    # height=600,
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