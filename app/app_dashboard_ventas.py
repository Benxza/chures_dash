import dash
from dash import html, Output, Input, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

df = pd.read_csv('C:/Users/benja/Desktop/Chures_card/app/data/sales.csv')

print(df.columns)









df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['Anio'] = df['Order Date'].dt.year
df['Mes'] = df['Order Date'].dt.month
df['Nombre Mes'] = df['Order Date'].dt.month_name()



Meses  = ['Todas'] + df['Mes'].sort_values().unique().tolist()
Anios  = ['Todas'] + df['Anio'].sort_values().unique().tolist()
Categorias  = ['Todas'] + df['Category'].sort_values().unique().tolist()
Region  = ['Todas'] + df['Region'].sort_values().unique().tolist()
Segmento = ['Todas'] + df['Segment'].sort_values().unique().tolist()






ventas_totales = df['Sales'].sum()
numero_de_pedidos = df['Order ID'].count()
dias_promedio = (df['Ship Date'] - df['Order Date']).dt.days.mean()
dias_promedio_texto = f"{dias_promedio:.1f} días" if pd.notnull(dias_promedio) else "N/A"







app.layout= dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1('Dash Board de Ventas La Mera punta del Segmento')

        )),
    dbc.Row([
            dbc.Col([
                #Kpis
                dbc.Card([
                    dbc.CardHeader('Ventas totales'),
                    dbc.CardBody(
                        html.P(ventas_totales)
                    )
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Numero de pedidos'),
                    dbc.CardBody(
                        html.P(numero_de_pedidos))
            ]),

        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Dias promedio de entrega'),
                dbc.CardBody(
                    html.P(dias_promedio_texto))
        ]),
    ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Ventas por mes'),
             dcc.Dropdown(
                        id='DropDown-mes',
                        options=[{'label' : str(mes) , 'value' : mes} for mes in Meses],
                        value=Meses[0]),
                dcc.Dropdown(
                            id='DropDown-anio-meses',
                            options=[{'label' : str(anio) , 'value' : anio} for anio in Anios],
                            value=Anios[0]),
            dcc.Graph(id='Graficos Mes')

        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Ventas por categoria'),
            dcc.Dropdown(
                id='DropDown-categoria',
                options=[{'label' : str(cat), 'value' : cat} for cat in Categorias ],
                value=Categorias[0],
            ),
            dcc.Graph(id='Graficos Categoria')

    ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Ventas por region y año'),
            dcc.Dropdown(
                id='DropDown-region',
                options=[{'label' : str(reg) , 'value' : reg} for reg in Region],
                value=Region[0]
            ),
            dcc.Dropdown(
                 id='DropDown-anio-region',
                 options=[{'label' : str(anio) , 'value' : anio} for anio in Anios],
                value=Anios[0]),
            dcc.Graph(id='Graficos Region')

            
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Ventas por Segmento'),
            dcc.Dropdown(
                        id='DropDown-Segmento',
                        options=[{'label' : str(seg) , 'value' : seg} for seg in Segmento],
                        value=Segmento[0]),
            dcc.Graph(id='Graficos segmento')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Top 10 Clientes'),
            dcc.Graph(id='Graficos-Top-10')
        ])
    ])
])



@app.callback(
    Output('Graficos Mes', 'figure'),
    Input('DropDown-mes', 'value'),
    Input('DropDown-anio-meses', 'value')
)

def actualizar_grafica_mes(mes_seleccionado, anio_seleccionado):
    dff = df.copy()
    
    if anio_seleccionado != 'Todas':
        dff = dff[dff['Anio'] == anio_seleccionado]
    if mes_seleccionado != 'Todas':
        dff = dff[dff['Mes'] == mes_seleccionado]
        
    df_agrupado = dff.groupby(['Anio', 'Mes', 'Nombre Mes'])['Sales'].sum().reset_index()
    
    fig = px.line(
        data_frame=df_agrupado,
        x='Nombre Mes',
        y='Sales',
        title=f'Ventas Mensuales Año'
    )
    return fig

@app.callback(
    Output('Graficos Region', 'figure'),
    Input('DropDown-region', 'value'),
    Input('DropDown-anio-region', 'value')
)

def actualizar_grafica_region(region_seleccionada, anio_seleccionado):
    dff = df.copy()
    
    if anio_seleccionado != 'Todas':
        dff = dff[dff['Anio'] == anio_seleccionado]
    if region_seleccionada != 'Todas':
        dff = dff[dff['Region'] == region_seleccionada]
        
    df_agrupado = dff.groupby(['Region', 'Anio'])['Sales'].sum().reset_index()
    
    fig = px.bar(
        data_frame=df_agrupado,
        x='Region',
        y='Sales',
        title=f'Ventas por Región Año '
    )
    return fig

@app.callback(
    Output('Graficos Categoria', 'figure'),
    Output('Graficos segmento', 'figure'),
    Input('DropDown-categoria', 'value'),
    Input('DropDown-Segmento', 'value')
)

def actualizar_graficas_restantes(categoria_seleccionada, segmento_seleccionado):
    dff = df.copy()
    
    if categoria_seleccionada != 'Todas':
        dff = dff[dff['Category'] == categoria_seleccionada]
    if segmento_seleccionado != 'Todas':
        dff = dff[dff['Segment'] == segmento_seleccionado]
        
    df_cat = dff.groupby('Category')['Sales'].sum().reset_index()
    df_seg = dff.groupby('Segment')['Sales'].sum().reset_index()
    
    fig_cat = px.pie(
        data_frame=df_cat,
        names='Category',
        values='Sales',
        title='Ventas por Categoría'
    )
    
    fig_seg = px.bar(
        data_frame=df_seg,
        x='Segment',
        y='Sales',
        title='Ventas por Segmento'
    )
    
    return fig_cat, fig_seg

@app.callback(
    Output('Graficos-Top-10', 'figure'),
    Input('DropDown-categoria', 'value')
)

def actualizar_top_10(categoria_seleccionada):
    dff = df.copy()
    
    if categoria_seleccionada != 'Todas':
        dff = dff[dff['Category'] == categoria_seleccionada]
        
    df_clientes = dff.groupby('Customer Name')['Sales'].sum().reset_index()
    df_top10 = df_clientes.sort_values(by='Sales', ascending=False).head(10)
    df_top10 = df_top10.sort_values(by='Sales', ascending=True)
    
    fig = px.bar(
        data_frame=df_top10,
        x='Sales',
        y='Customer Name',
        orientation='h',
        title='Top 10 Clientes'
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)