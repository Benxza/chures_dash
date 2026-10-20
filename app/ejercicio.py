import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px



app = dash.Dash(__name__)

df_aguacate = pd.read_csv('C:/Users/usuario26/Desktop/chures_dash/data/aguacate.csv')


Region = ["Todas"] + df_aguacate['region'].sort_values().unique().tolist()
tipos= ["Todas"] + df_aguacate['type'].sort_values().unique().tolist()

app.layout = html.Div(children=[
    html.H1('Dashboard de Aguacate'),
    html.Div(children=[
        html.Label('Seleccione la región:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in Region],
            value='Todas'
        ),
    ]),
    html.Div(children=[
        html.Label('Seleccione el tipo:'),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': tipo, 'value': tipo} for tipo in tipos],
            value='Todas'
        ),
    ]),
    dcc.Graph(id='price-graph')
])


@app.callback(
    Output('price-graph', 'figure'),
    Input('region-dropdown', 'value'),
    Input('type-dropdown', 'value')
)

def actualizar(region,tipos):
    df_total=df_aguacate.copy()
    if region != 'Todas':
        df_total=df_total[df_total["region"]==region]
    if tipos != "Todas":
        df_total=df_total[df_total["type"]==tipos]
    fig=px.bar(df_total,x="region",y="Total_Volume",
               title=f"penes largos para ariel {region}")
        
    return fig


if __name__ == '__main__':
    app.run(debug=True)