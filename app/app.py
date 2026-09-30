import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)

df_principal = pd.read_csv('C:/Users/Usuario26/Desktop/chures_dash/data/ventas.csv')


df_region = df_principal.groupby('Region', as_index=False).agg({'Ventas': 'sum'}).reset_index()
df_categoria = df_principal.groupby('Categoria', as_index=False).agg({'Ventas': 'sum'}).reset_index()




print(df_region)

fig = px.bar(df_region, 
             x='Region', 
             y='Ventas',
             title='Ventas por Región',
             labels={'Ventas': 'Ventas Totales', 'Region': 'Región'},)

fig2 = px.bar(df_categoria,
              x='Categoria',
              y='Ventas',
              title='Ventas por Categoría',
              labels={'Ventas': 'Ventas Totales', 'Categoria': 'Categoría'},)


app.layout = html.Div(children=[
    html.H1("Dashboard de Ventas"),
    html.Div(children=[dcc.Graph(
            id='grafico-ventas',
            figure=fig
        ),
    html.Div(children=[dcc.Graph(
            id='grafico-categoria',
            figure=fig2),])]
            )])

fig.update_layout(template='plotly_dark')
fig2.update_layout(template='plotly_dark')

if __name__ == '__main__':
    app.run(debug=True)