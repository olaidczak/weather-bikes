from src.ui.data import get_data
from src.ui.data_weather import get_data2

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

import plotly.express as px
from dash import Dash, html, dcc, Input, Output


# loading data
bikes_df = get_data()
weather_df = get_data2()

# aggregate bikes (sum)
bikes_agg = (
    bikes_df
    .groupby(["batch_id", "timestamp"], as_index=False)
    .agg({"free_bikes": "sum"})
)

# merge by batch_id
df = bikes_agg.merge(
    weather_df,
    on="batch_id",
    how="inner"
)

# temperature to integer
df["temperature_int"] = np.floor(df["temperature"]).astype(int)

# sum free bikes per temp
temp_sum = (
    df
    .groupby("temperature_int", as_index=False)
    .agg({"free_bikes": "sum"})
    .sort_values("temperature_int")
)


# train model
X = temp_sum[["temperature_int"]]
y = temp_sum["free_bikes"]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# plot
temp_range = np.arange(
    temp_sum["temperature_int"].min(),
    temp_sum["temperature_int"].max() + 1
)

pred_df = pd.DataFrame({
    "Temperature (°C)": temp_range,
    "Predicted free bikes": model.predict(
        pd.DataFrame({"temperature_int": temp_range})
    )
})

# dash app

app = Dash(__name__)

fig = px.line(
    temp_sum,
    x="temperature_int",
    y="free_bikes",
    markers=True,
    labels={
        "<b>Real data</b><br>"
        "temperature_int": "Temperature (°C)",
        "free_bikes": "Sum of free bikes"
    },
    title="Sum of Free Bikes vs Temperature"
)

# dodac do legendy !!!

fig.add_scatter(
    x=pred_df["Temperature (°C)"],
    y=pred_df["Predicted free bikes"],
    mode="lines",
    name="Model prediction",
    hovertemplate=(
        "<b>Model prediction</b><br>"
        "Temperature: %{x}°C<br>"
        "Free bikes: %{y:.0f}"
        "<extra></extra>"
    )
)

app.layout = html.Div(
    style={"width": "80%", "margin": "auto"},
    children=[

        html.H2("Free Bikes vs Temperature"),

        dcc.Graph(figure=fig),

        html.H4("Predict sum of free bikes for temperature"),

        dcc.Slider(
            id="temp-slider",
            min=int(temp_sum["temperature_int"].min()),
            max=int(temp_sum["temperature_int"].max()),
            step=1,
            value=int(temp_sum["temperature_int"].mean()),
            marks={
                t: str(t)
                for t in range(
                    int(temp_sum["temperature_int"].min()),
                    int(temp_sum["temperature_int"].max()) + 1,
                    2
                )
            }
        ),

        html.Br(),

        html.H3(id="prediction-output")
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
