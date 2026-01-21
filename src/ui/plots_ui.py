from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
from src.ui.data import get_data
from src.ui.data_weather import get_data2

# ===== DANE =====
bikes_df = get_data()
weather_df = get_data2()

# 1. Temp in time
fig_temp = go.Figure()

# Temperature – line (LEFT Y AXIS)
fig_temp.add_trace(
    go.Scatter(
        x=weather_df["timestamp"],
        y=weather_df["temperature"],
        name="Temperature [°C]",
        mode="lines",
        line=dict(color="blue"),
        yaxis="y1",
        hovertemplate=(
            "<b>Temperature</b><br>"
            "Time: %{x}<br>"
            "Temp: %{y:.1f} °C"
            "<extra></extra>"
        )
    )
)

# Rain – bars
fig_temp.add_trace(
    go.Bar(
        x=weather_df["timestamp"],
        y=weather_df["rain"],
        name="Rain [mm]",
        yaxis="y2",
        opacity=0.5,
        hovertemplate=(
            "<b>Rain</b><br>"
            "Time: %{x}<br>"
            "Rain: %{y:.2f} mm"
            "<extra></extra>"
        )
    )
)

# Layout with 2 Y axes
fig_temp.update_layout(
    title={"text":"Temperature and Rainfall over Time", "x":0.5, "xanchor":"center"},
    xaxis=dict(title="Time",
                       showgrid=True,
        gridcolor="rgba(0,0,0,0.08)"),
    yaxis=dict(
        title="Temperature [°C]",
        side="left",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    yaxis2=dict(
        title="Rain [mm]",
        side="right",
        overlaying="y",
        showgrid =False
    ),
    plot_bgcolor="white",
    legend=dict(x=0.01, y=0.99),
    bargap=0,
)

# 2. Temp vs free bikes
merged = bikes_df.merge(
    weather_df,
    on="batch_id",
    how = "inner"
)

merged_grouped = merged.groupby('batch_id').agg({
    'temperature': 'mean',
    'free_bikes': 'sum',
    'rain' : 'sum' 
}).reset_index()

merged_grouped["rain_binary"] = merged_grouped["rain"].apply(
    lambda x: "Rain" if x > 0.1 else "No rain"
)

fig_bikes_temp = px.scatter(
    merged_grouped,
    x="temperature",
    y="free_bikes",
    color="rain_binary",
    color_discrete_map={
        "Rain": "#d62728",
        "No rain": "#1f3b73"
    },
    hover_data=["batch_id"],
    labels={
        "temperature": "Temperature [°C]",
        "free_bikes": "Free bikes",
        "rain_binary": "Rain condition"
    }
)
fig_bikes_temp.update_layout(
    yaxis=dict(
        showgrid =True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    xaxis=dict(
        showgrid =True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    plot_bgcolor="white",
    title={"text":"Number of free bikes depending on Temperature and Rainfall", "x":0.5, "xanchor":"center"},

)

# 3. heatmap ?
weather_hm = weather_df.copy()
weather_hm["date"] = weather_hm["timestamp"].dt.date
weather_hm["hour"] = weather_hm["timestamp"].dt.hour

weather_2h = weather_df.copy()
weather_2h["date"] = weather_2h["timestamp"].dt.date
weather_2h["hour_2h"] = (weather_2h["timestamp"].dt.hour // 2) * 2

heatmap_data = (
    weather_2h
    .groupby(["date", "hour_2h"], as_index=False)
    .agg({"temperature": "mean"})
)
fig_weather_heatmap = px.density_heatmap(
    heatmap_data,
    x="date",
    y="hour_2h",
    z="temperature",
    color_continuous_scale="RdYlBu_r",
    labels={
        "date": "Date",
        "hour_2h": "Hour of day",
        "temperature": "Temperature [°C]"
    }
)
fig_weather_heatmap.update_coloraxes(
    colorbar_title="Mean temperature [°C]"
)
fig_weather_heatmap.update_traces(
    hovertemplate=(
        "Date: %{x}<br>"
        "Hour: %{y}<br>"
        "Temperature: %{z:.1f} °C"
        "<extra></extra>"
    )
)
fig_weather_heatmap.update_layout(
    title = {"text":"Daily temperature pattern", "x":0.5, "xanchor":"center"}
)


# 4. Free bikes vs hour
merged_hour = merged.copy()
merged_hour["hour"] = merged_hour["timestamp_x"].dt.hour
hour_grouped = (
    merged_hour
    .groupby("hour", as_index=False)
    .agg({
        "free_bikes": "sum"
    })
)
fig_bikes_hour = px.line(
    hour_grouped,
    x="hour",
    y="free_bikes",
    markers=True,
    labels={
        "hour": "Hour of day",
        "free_bikes": "Average free bikes"
    }
)
fig_bikes_hour.update_traces(
    hovertemplate=(
        "<b>Hour</b>: %{x}:00<br>"
        "<b>Free bikes</b>: %{y:.0f}"
        "<extra></extra>"
    )
)
fig_bikes_hour.update_layout(
    plot_bgcolor="white",
        yaxis=dict(
        showgrid =True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    xaxis=dict(
        showgrid =True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    title={"text":"Average Number of Free Bikes by Hour", "x":0.5, "xanchor":"center"},
)

# NOT REALLY
# numeric_cols = [
#     'temperature', 'relative_humidity', 'apparent_temperature', 
#     'surface_pressure', 'pressure_msl', 'precipitation', 
#     'rain', 'cloud_cover', 'wind_speed'
# ]
# corr_matrix = weather_df[numeric_cols].corr()

# fig_heatmap = px.imshow(
#     corr_matrix,
#     text_auto=True,
#     color_continuous_scale='Viridis',
#     title="Heatmapa korelacji parametrów pogodowych"
# )

# ===== APP =====
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Weather & Bikes Dashboard"),
    html.Div(
        style={"display": "flex", "gap": "20px"},
        children=[
            html.Div(children=dcc.Graph(figure=fig_temp)),
            html.Div(children=dcc.Graph(figure=fig_weather_heatmap)),
        ]
    ),

    # ROW 2
    html.Div(
        style={"display": "flex", "gap": "20px"},
        children=[
            html.Div(children=dcc.Graph(figure=fig_bikes_temp)),
            html.Div(children=dcc.Graph(figure=fig_bikes_hour)),
        ]
    )
])

if __name__ == "__main__":
    app.run(debug=True)
