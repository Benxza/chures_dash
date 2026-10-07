import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df_aguacate = pd.read_csv('C:/Users/Usuario26/Desktop/chures_dash/data/aguacate.csv')


app.layout = html.Div(children=[
        html.Label("Selecciona una Region:"),
                dcc.Dropdown(
                    id="Dropdown-aguacate",
                    options=[{'label': reg, 'value': reg} for reg in df_aguacate['region'].sort_values().unique()],
                    value=df_aguacate['region'].sort_values().unique()[0],
                    style={'width': '50%', 'margin-bottom': '20px'}
    
                ),
])


@app.callback()