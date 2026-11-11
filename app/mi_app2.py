import dash 
from dash import Dash, html, Input, Output, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template 

load_figure_template("Sketchy")

# Cargar datos
df = pd.read_csv('C:/Users/usuario26/Desktop/chures_dash/data/ventas_papeleria.csv')

orden_meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

df['mes'] = df['mes'].astype(str).str.strip().str.capitalize()
df['mes'] = pd.Categorical(df['mes'], categories=orden_meses, ordered=True)


kpi_1 = df['ingreso'].sum()
kpi_2 = df['cantidad'].count()
kpi_3 = df['ingreso'].mean()

meses_opciones = ['Todas'] + orden_meses
vendedores = ['Todos'] + df['vendedor'].dropna().sort_values().unique().tolist()
productos = ['Todos'] + df['producto'].dropna().sort_values().unique().tolist()

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = html.Div(
    children=[
        html.H1('La mera punta del tren', className='titulo_principal'),
        
        html.Div(children=[
            html.Div([
                html.H3("Ingreso Total", className='kpi-title'),
                html.P(f"${kpi_1:,.2f}", className='kpi-value')
            ], className='kpi-card'),
            
            html.Div([
                html.H3("Total de Ventas", className='kpi-title'),
                html.P(f"{kpi_2:,}", className='kpi-value')
            ], className='kpi-card'),
            
            html.Div([
                html.H3("Ingreso Promedio", className='kpi-title'),
                html.P(f"${kpi_3:,.2f}", className='kpi-value')
            ], className='kpi-card'),
        ], className='kpi-container'),

        html.Div(children=[
            html.H1('Grafico de ventas por mes', className='subtitulo_principal'),
            html.Label("Selecciona un Mes:"),
            dcc.Dropdown(
                id="dropdown-mes",
                options=[{'label': m, 'value': m} for m in meses_opciones],
                value='Todas',
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='grafico-mes')
        ]),

        html.Div(children=[
            html.H1('Grafico de ventas por vendedor', className='subtitulo_principal'),
            html.Label("Selecciona un Vendedor:"),
            dcc.Dropdown(
                id="dropdown-vendedor",
                options=[{'label': v, 'value': v} for v in vendedores],
                value='Todos',
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='grafico-vendedor')
        ]),

        html.Div(children=[
            html.H1('Grafico de ventas por producto', className='subtitulo_principal'),
            html.Label("Selecciona un Producto:"),
            dcc.Dropdown(
                id="dropdown-producto",
                options=[{'label': p, 'value': p} for p in productos],
                value='Todos',
                style={'width': '50%', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='grafico-producto')
        ]),
    ]
)

@app.callback(
    Output("grafico-mes", "figure"),
    Output("grafico-vendedor", "figure"),
    Output("grafico-producto", "figure"),
    Input("dropdown-mes", "value"),
    Input("dropdown-vendedor", "value"),
    Input("dropdown-producto", "value")
)
def actualizar_graficas(mes_seleccionado, vendedor_seleccionado, producto_seleccionado):
    
    df_mes = df.copy()
    if mes_seleccionado != 'Todas':
        df_mes = df_mes[df_mes['mes'] == mes_seleccionado]
    df_agrupado_mes = df_mes.groupby('mes', as_index=False, observed=False)['ingreso'].sum().sort_values('mes')
    
    fig1 = px.bar(
        df_agrupado_mes,
        x='mes',
        y='ingreso',
        title=f'Ventas por mes  {mes_seleccionado})',
        labels={'mes': 'Mes', 'ingreso': 'Ingreso'}
    )

    df_vendedor = df.copy()
    if vendedor_seleccionado != 'Todos':
        df_vendedor = df_vendedor[df_vendedor['vendedor'] == vendedor_seleccionado]
    df_agrupado_vendedor = df_vendedor.groupby('vendedor', as_index=False)['ingreso'].sum()
    
    fig2 = px.bar(
        df_agrupado_vendedor,
        x='vendedor',
        y='ingreso',
        title=f'Venta por vendedor  {vendedor_seleccionado})',
        labels={'vendedor': 'Vendedor', 'ingreso': 'Ingreso'}
    )

    df_producto = df.copy()
    if producto_seleccionado != 'Todos':
        df_producto = df_producto[df_producto['producto'] == producto_seleccionado]
    df_agrupado_producto = df_producto.groupby('producto', as_index=False)['ingreso'].sum()
    
    fig3 = px.bar(
        df_agrupado_producto,
        x='producto',
        y='ingreso',
        title=f'Venta por producto  {producto_seleccionado})',
        labels={'producto': 'Producto', 'ingreso': 'Ingreso'}
    )

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run(debug=True)