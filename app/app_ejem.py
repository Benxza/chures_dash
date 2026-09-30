import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)

df_principal = pd.read_csv('C:/Users/Usuario26/Desktop/chures_dash/data/ventas.csv')

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
        dcc.Graph(
            id='grafico-ventas'
        ),
    ])
])

@app.callback(
            Output("grafico-ventas", "figure"),
            Input("Dropdown-categoria", "value"), 
              )

def actualizar_grafica(categoria_seleccionada):
    df_categoria = df_principal[df_principal['Categoria'] == categoria_seleccionada]
    df_agrupado = df_categoria.groupby('Region', as_index=False).agg({'Ventas': 'sum'}).reset_index()
    
    fig = px.bar(df_agrupado,
                 x='Region',
                 y='Ventas',
                 title=f'Ventas por Región - Categoría: {categoria_seleccionada}',
                 labels={'Ventas': 'Ventas Totales', 'Region': 'Región'})
    
    fig.update_layout(template='plotly_dark')
    
    return fig


#fig.update_layout(template='plotly_dark')

if __name__ == '__main__':
    app.run(debug=True)