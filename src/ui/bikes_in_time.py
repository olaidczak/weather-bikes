from src.ui.data import get_data
from src.ui.data_weather import get_data2
import plotly.io as pio
import plotly.express as px
pio.templates.default = "plotly_white"


bikes_df = get_data()
weather_df = get_data2()

bikes_agg = (
    bikes_df
    .groupby(["batch_id", "timestamp"], as_index=False)
    .agg({"free_bikes": "sum"})
)

bikes_agg["hour"] = bikes_agg["timestamp"].dt.hour
bikes_hourly = (
    bikes_agg
    .groupby("hour", as_index=False)
    .agg({"free_bikes": "mean"})
)
fig_hour = px.line(
    bikes_hourly,
    x="Hour",
    y="Free bikes",
    markers=True,
    title="Mean of free bikes depending on the hour"
)

fig_hour.write_html("time1.html")


