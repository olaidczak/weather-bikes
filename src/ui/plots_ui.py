from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
from src.ui.data import get_data
from src.ui.data_weather import get_data2
from src.ui.data import get_data3
from src.model.data import get_data as get_data_model
import pandas as pd

GLOBAL_FIG_STYLE = dict(
    font=dict(
        family="Arial",
        size=18,
        color="#2c3e50"
    ),
    legend=dict(
        font=dict(size=18),
        title_font=dict(size=20)
    ),
    xaxis=dict(
        title_font=dict(size=22),
        tickfont=dict(size=18)
    ),
    yaxis=dict(
        title_font=dict(size=22),
        tickfont=dict(size=18)
    ),
    title=dict(
        font=dict(size=28, family="Arial", color="#2c3e50"),
        x=0.5,
        xanchor='center'
    )

)

# ===== DANE =====
bikes_df = get_data()
weather_df = get_data2()
stations_df = get_data3()

weather_df["timestamp_ny"] = (
    weather_df["timestamp"]
    .dt.tz_localize("UTC")         
    .dt.tz_convert("America/New_York")
)


# 1. TEMP IN TIME
fig_temp = go.Figure()

# Temperature – line
fig_temp.add_trace(
    go.Scatter(
        x=weather_df["timestamp_ny"],
        y=weather_df["temperature"],
        name="Temperature [°C]",
        mode="lines",
        line=dict(color="blue"),
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
        x=weather_df["timestamp_ny"],
        y=weather_df["precipitation"],
        yaxis="y2",
        name="Precipitation [mm]", 
        opacity=0.5,
        hovertemplate=(
            "<b>Precipitation</b><br>"
            "Time: %{x}<br>"
            "Precipitation: %{y:.2f} mm"
            "<extra></extra>"
        )
    )
)

# layout with 2 y axes
fig_temp.update_layout(
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
        title="Precipitation [mm]",
        side="right",
        overlaying="y",
        showgrid=False,
        title_font=dict(size=22),
        tickfont=dict(size=18)
    ),
    title=dict(
        text= "Temperature and precipitation over time",
        font=dict(size=40, family="Arial", color="#2c3e50"),
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor="white",
    legend=dict(x=0.01, y=0.99),
    bargap=0,
)

# 2. TEMP VS BIKES - SCATTER
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

# 3. HEATMAP ?
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
    colorbar_title="Temperature [°C]"
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


# 4. FREE BIKES VS HOUR
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

# OLA
# change time to ny time
df = get_data_model()
df["timestamp_ny"] = (
    df["timestamp"]
    .dt.tz_localize("UTC")         
    .dt.tz_convert("America/New_York")
)
df["hour"] = df["timestamp_ny"].dt.hour
fig_ola = go.Figure()

# Used Bikes (left y-axis)
fig_ola.add_trace(
    go.Scatter(
        x=df['timestamp_ny'],
        y=df["used_bikes"],
        name="Percentage of Used Bikes",
        mode="lines"
    )
)

# Apparent Temperature (right y-axis)
fig_ola.add_trace(
    go.Scatter(
        x=df['timestamp_ny'],
        y=df["apparent_temperature"],
        name="Apparent Temperature",
        mode="lines",
        yaxis="y2",
        line=dict(color="red")
    )
)

fig_ola.update_layout(
    plot_bgcolor="white",
    xaxis_title="Time",
    yaxis=dict(
        title="Used Bikes",
        showgrid =True,
        gridcolor="rgba(0,0,0,0.08)"
    ),
    yaxis2=dict(
        title="Temperature [°C]",
        overlaying="y",
        side="right",
        title_font=dict(size=22),
        tickfont=dict(size=18)
    ),
    legend=dict(
        x=0.01,
        y=0.99
    ),
    title=dict(
        text="Percentage of bikes used and apparent temperature",
        x= 0.5,
        font=dict(size=40, family="Arial", color="#2c3e50"),
    )
)


# TRY --------------------------------------------------------------------------

merged_grouped["temp_bin"] = pd.cut(
    merged_grouped["temperature"], bins=5
).astype(str)


fig_fig = px.box(
    merged_grouped,
    x="temp_bin",
    y="free_bikes",
    labels={
        "temp_bin": "Temperature [°C]",
        "free_bikes": "Total free bikes"
    },
)

fig_fig.update_traces(
    boxmean=True,
    hovertemplate=
        "Temp bin: %{x}<br>" +
        "Min: %{lowerfence}<br>" +
        "Mean: %{mean}<br>" +
        "Max: %{upperfence}<extra></extra>"
)

fig_fig.update_layout(
    title=dict(
        text="Free Bikes distribution depending on temperature",
        font=dict(size=40, family="Arial", color="#2c3e50"),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(showgrid=True,
               gridcolor="rgba(0,0,0,0.08)"),
    yaxis=dict(showgrid=True,
               gridcolor="rgba(0,0,0,0.08)"),
)

# MAPA
stations_df = stations_df.reset_index(drop=True)

fig_map = px.scatter_mapbox(
    stations_df,
    lat="lat",
    lon="lon",
    zoom=11,
    height=450
)

fig_map.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Slots: %{customdata[1]}"
        "<extra></extra>"
    ),
    customdata=stations_df[["name", "slots"]].values
)


fig_map.update_layout(
    mapbox_style="carto-positron",
    title=dict(
        text= "Bike stations and possible bikes spots",
        font=dict(size=40, family="Arial", color="#2c3e50"),
        x=0.5,
        xanchor='center'
),
    margin={"r":0, "t":40, "l":0, "b":0}
)



# mapa = go.Figure()
# mapa = px.scatter_mapbox(
#     df,
#     lat="lat",
#     lon="lon",
#     hover_name="name",
#     zoom=11,
#     center={"lat": 40.7128, "lon": -74.0060},
#     height=600
# )

# mapa.update_layout(
#     mapbox_style="carto-positron",  # clean, no API key needed
#     title="Selected Points in New York City",
#     margin={"r":0,"t":40,"l":0,"b":0}
# )


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

# TABELKA
from src.model.data import get_forecast_data
from src.model.model_predict import predict
forecast_df = get_forecast_data()
forecast_df["predicted_used_bikes"] = predict(forecast_df)

# ===== APP =====
PAGE_STYLE = {
    "maxWidth": "4000px",
    "margin": "0 auto",
    "padding": "20px 30px",
    "backgroundColor": "#f7f9fb"
}


ROW_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "1fr 1fr",
    "gap": "20px",
    "marginBottom": "20px"
}

CARD_STYLE = {
    "backgroundColor": "white",
    "borderRadius": "10px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
    "padding": "12px"
}

STANDARD_HEIGHT = 500
MAP_HEIGHT = 600

fig_temp.update_layout(height=STANDARD_HEIGHT)
fig_fig.update_layout(height=STANDARD_HEIGHT)
fig_ola.update_layout(height=STANDARD_HEIGHT)
fig_map.update_layout(height=MAP_HEIGHT)

for fig in [fig_temp, fig_fig, fig_ola, fig_map ]:
    fig.update_layout(
        margin=dict(l=40, r=30, t=120, b=40),
        plot_bgcolor="white"
    )

for fig in [fig_temp, fig_fig, fig_ola, fig_map, fig_bikes_temp, fig_weather_heatmap, fig_bikes_hour]:
    fig.update_layout(**GLOBAL_FIG_STYLE)


app = Dash(__name__)
##
app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        html.H2(
            "Weather & Bikes Dashboard",
        style={
            "fontFamily": "Arial, sans-serif",
            "fontSize": "40px",  # większy
            "fontWeight": "700", # grubszy
            "color": "#2c3e50",
            "marginBottom": "30px",
            "textAlign": "center"  # wyśrodkowanie
        }
        ),

        # ===== ROW 1 =====
        html.Div(
            style=ROW_STYLE,
            children=[
                html.Div(dcc.Graph(figure=fig_temp), style=CARD_STYLE),
                html.Div(dcc.Graph(figure=fig_fig), style=CARD_STYLE),
            ]
        ),

        # ===== ROW 2 =====
        html.Div(
            style=ROW_STYLE,
            children=[
                html.Div(dcc.Graph(figure=fig_map), style=CARD_STYLE),
                html.Div(dcc.Graph(figure=fig_ola), style=CARD_STYLE),
            ]
        ),

        # ===== TABLE SECTION =====
        html.Div(
            style={
                **CARD_STYLE,
            },
            children=[
                html.H4(
                    "Bike Usage Forecast",
                    style={
                        "marginBottom": "20px",
                        "color": "#2c3e50",
                        "fontSize": "28px",
                        "textAlign": "center",
                        "fontFamily": "Arial"
                        }
                    ),
                dash_table.DataTable(
                    id="forecast-table",
                    columns=[
                        {"name": col.replace("_", " ").title(), "id": col}
                        for col in forecast_df.columns
                    ],
                    data=forecast_df.round(2).to_dict("records"),
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "center",
                        "padding": "8px",
                        "fontFamily": "Arial"
                    },
                    style_header={
                        "backgroundColor": "#ecf0f1",
                        "fontWeight": "600"
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "#fafafa"
                        }
                    ]
                )
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True,port=8050,host="0.0.0.0")
