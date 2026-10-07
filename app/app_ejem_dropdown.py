import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px



app = dash.Dash(__name__)

df_principal = pd.read_csv('C:/Users/usuario26/Desktop/chures_dash/data/ventas.csv')

df_aguacate = pd.read_csv('C:/Users/usuario26/Desktop/chures_dash/data/aguacate.csv')


regiones = ['Todas'] + df_principal['Region'].sort_values().unique().tolist()

regiones_aguacate = ['Todas'] + df_aguacate['region'].sort_values().unique().tolist()

categorias = df_principal['Categoria'].sort_values().unique()








app.layout = html.Div(children=[
    html.H1("Dashboard de Ventas"),
    html.Div(children=[
        html.Label("Selecciona una Categoría:"),
        dcc.Dropdown(
            id="Dropdown-categoria",
            options=[{'label': cat, 'value': cat} for cat in categorias],
            value=categorias[0],
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        html.Label("Selecciona una Region:"),
                dcc.Dropdown(
                    id="Dropdown-Region",
                    options=[{'label': reg, 'value': reg} for reg in regiones],
                    value=regiones[0],
                    style={'width': '50%', 'margin-bottom': '20px'}
                ),
        html.Label("Selecciona una Region:"),
            dcc.Dropdown(
                id="Dropdown-aguacate",
                options=[{'label': r, 'value': r} for r in regiones_aguacate],
                value=regiones_aguacate[0],
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
        dcc.Graph(
            id='grafico-ventas'
        ),
        dcc.Graph(
            id='grafico-aguacate'
        ),
    ])
])

@app.callback(
            Output("grafico-ventas", "figure"),
            Output("grafico-aguacate", "figure"),
            Input("Dropdown-categoria", "value"), 
            Input("Dropdown-Region", "value"),
            Input("Dropdown-aguacate", "value"),
              )

def actualizar_grafica(categoria_seleccionada, region_seleccionada, region_aguacate_seleccionada):
    global df_aguacate, df_principal
    
    df_categoria = df_principal[df_principal['Categoria'] == categoria_seleccionada]
    
    if region_seleccionada != 'Todas':
        df_categoria = df_categoria[df_categoria['Region'] == region_seleccionada]
    if region_aguacate_seleccionada != 'Todas':
        df_aguacate = df_aguacate[df_aguacate['region'] == region_aguacate_seleccionada]
    
    df_agrupado = df_categoria.groupby('Region', as_index=False).agg({'Ventas': 'sum'}).reset_index()
    df_agrupado_aguacate = df_aguacate.groupby('region', as_index=False).agg({'Total_Volume': 'sum'}).reset_index()
    
    fig = px.bar(df_agrupado,
                 x='Region', 
                 y='Ventas',
                 title=f'Ventas por Región - Categoría: {categoria_seleccionada}',
                 labels={'Ventas': 'Ventas Totales', 'Region': 'Región'})

    fig_1 = px.bar(df_agrupado_aguacate,
                 x='region', 
                 y='Total_Volume',
                 title=f'Ventas por Región - Region : {region_aguacate_seleccionada}',
                 labels={'Total_Volume': 'Ventas Totales', 'region': 'Región'})
    
    fig.update_layout(template='plotly_dark')
    fig_1.update_layout(template='plotly_dark')
    return fig, fig_1



if __name__ == '__main__':
    app.run(debug=True)