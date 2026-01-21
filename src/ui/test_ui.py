from src.ui.data import get_data
from src.ui.data_weather import get_data2
from dash import Dash, html
import dash_ag_grid as dag

df = get_data()
df2 = get_data2()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H3("First App"),
        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": col} for col in df.columns],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            style={"height": "600px", "width": "100%"},
        ),
                html.Hr(),

        html.H3("Tabela 2 – dane z data_weather.py"),
        dag.AgGrid(
            id="grid-2",
            rowData=df2.to_dict("records"),
            columnDefs=[{"field": col} for col in df2.columns],
            defaultColDef={"sortable": True, "filter": True, "resizable": True},
            style={"height": "400px", "width": "100%"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8050,debug=True)
