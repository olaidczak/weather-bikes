from dash import Dash, html
import dash_ag_grid as dag

from .data import get_data


df = get_data()

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
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8050,debug=True)
