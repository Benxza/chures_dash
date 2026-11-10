import dash 
from dash import Dash, html, Input, Output,dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template 

load_figure_template("Sketchy")

df = pd.read_csv('C:/Users/benja/Desktop/proyecto_dash/data/ventas_papeleria.csv')

orden_meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

df['mes'] = df['mes'].astype(str).str.strip().str.capitalize()

df['mes'] = pd.Categorical(df['mes'], categories=orden_meses, ordered=True)

df_agrupado_por_ventas_mes = df.groupby('mes', as_index=False)['ingreso'].agg('sum').reset_index().sort_values('mes')
df_agrupado_por_ventas_vendedor = df.groupby('vendedor')['ingreso'].agg('sum').reset_index()
df_agrupado_por_ventas_producto = df.groupby('producto')['ingreso'].agg('sum').reset_index()

kpi_1 = df['ingreso'].sum()
kpi_2 = df['cantidad'].count()
kpi_3 = df['ingreso'].mean()



fig = px.bar(
    df_agrupado_por_ventas_mes,
    x='mes',
    y='ingreso',
    title = 'Ventas por mes',
    labels = {'mes' : 'mes', 'ingreso' : 'ingreso'}
)

fig2 = px.bar(
    df_agrupado_por_ventas_vendedor,
    x='vendedor',
    y='ingreso',
    title='Venta por vendedor',
    labels={'vendedor' : 'vendedor', 'ingreso' : 'ingreso'}
)

fig3 = px.bar(
    df_agrupado_por_ventas_producto,
    x='producto',
    y='ingreso',
    title='Venta por vendedor',
    labels={'producto' : 'producto', 'ingreso' : 'ingreso'}
)



app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = dbc.Container(
    children = [
        dbc.Row(
            dbc.Col(
                html.H1('La mera punta del tren', className='titulo_principal')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H1('Grafico de ventas por mes', className='subtitulo_principal')
            )
        ),
        dbc.Row([
            dbc.Col(
                html.Div(f'Ventas Totales : {kpi_1} $', className='kpi_1')
            ),
            dbc.Col(
                html.Div(f'Cantidad de ventas :  {kpi_2}', className='kpi_2')
            ),
            dbc.Col(
                html.Div(f'Venta Promedio : {kpi_3} $', className='kpi_3')
            )
    ]),
        
        dbc.Row(
            dbc.Col(
                html.Div(dcc.Graph(
                    id='Grafico de ventas por mes',
                    figure=fig
                ))
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.H1('Grafico de ventas por vendedor', className='subtitulo_principal')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(dcc.Graph(
                    id='Grafico de ventas por vendedor',
                    figure=fig2
                ))
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.H1('Grafico de ventas por producto', className='subtitulo_principal')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(dcc.Graph(
                    id='Grafico de ventas por producto',
                    figure=fig3
                ))
            ),
        ),
    
    ]
)


if __name__ == '__main__':
    app.run(debug=True)


