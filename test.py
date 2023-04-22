import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, dependencies

df = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
ndf = df.sort_values(by=['Trafic'], ascending=False).head(10)
top_villes = df.groupby('Ville').sum().sort_values(by=['Trafic'], ascending=False).head(5).reset_index()

emp_df = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
emp_sort_x = emp_df.groupby('exploitant').groups.keys()
emp_sort_y = emp_df.groupby('exploitant').size().sort_values(ascending=False)

lgn_sort_x = emp_df.groupby('ligne').groups.keys()
lgn_sort_y = emp_df.groupby('ligne').size().sort_values(ascending=False)

emp_df[['lat', 'lng']] = emp_df['Geo Point'].str.split(',', expand=True)
emp_df['lat'] = emp_df['lat'].str.strip().astype(float)
emp_df['lng'] = emp_df['lng'].str.strip().astype(float)




app = Dash(__name__)
app.layout = (html.Div(children=[
    html.H1("Top 10 RATP trafic", style={'textAlign': 'center', 'textDecoration': 'underline', 'color': 'black',"backgroundColor": "lightblue"}),
    html.Hr(),
    html.H2('Données RATP :',style={'textAlign': 'center', 'textDecoration': 'underline', 'color': 'black',"backgroundColor": "lightblue"}),
    html.Hr(),
    # Pour implémenter le filtre pour sélectionner en fonction des réseaux
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': category, 'value': category} for category in df['Réseau'].unique()],
            value=None,
            placeholder='Select a network'
    ),
    # ==================1e div : RATP========================================================================================

    html.Div(style={'display': 'flex',"backgroundColor": "lightblue"}, children=[
        # bar chart : Top 10 des stations en fonction du trafic
        dcc.Graph(
            id='RATP bar chart trafic',
            figure=px.bar(ndf, x='Station', y='Trafic', title='Graphique qui représente les 10 stations les plus fréquentées')
        ),
        # pie chart : Top 5 des villes en fonction du trafic
        dcc.Graph(
            id='RATP pie chart trafic',
            figure=px.pie(top_villes, names='Ville', values='Trafic', title='Graphique qui représente le trafic des 5 plus grande villes')
        ),
    ]),
    html.Hr(),
    # ==================2e div : Ile de france===============================================================================
    html.H2('Données Ile de France :',style={'textAlign': 'center', 'textDecoration': 'underline','color': 'black',"backgroundColor": "lightblue"}),
    html.Hr(),
        dcc.Dropdown(
            id='category-filter2',
            options=[{'label': exploitant, 'value': exploitant} for exploitant in emp_df['exploitant'].unique()],
            value=None,
            placeholder='Select a network'
    ),
    html.Div(style={'display': 'flex',"backgroundColor": "lightblue"}, children=[
        # bar chart du nombre d exploitant en fonction du nombre de stations
        dcc.Graph(
            id='IDF par exploitant',
            figure=px.bar(emp_df, x=lgn_sort_x, y=lgn_sort_y, title="Nombre de stations par exploitant",labels={'x':'Exploitant','y':'Nombre de ligne'})
        ),
        # bar chart du nombre de lignes par ville
        dcc.Graph(
            id='IDF par ligne',
            figure=px.bar(emp_df, x=lgn_sort_x, y=lgn_sort_y, title="Nombre de lignes", labels={'x':'Lignes','y':'Nombres de lignes'})
        ),

    ]),
    html.Div(children=[
        html.Hr(),
        html.H2("Map", style={'textAlign': 'center', 'textDecoration': 'underline', 'color': 'black',"backgroundColor": "lightblue"}),
        html.Hr(),
        dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
            emp_df,
            lat='lat',
            lon='lng',
            hover_name='Geo Point',
            zoom=9,
            color = 'exploitant'
        ).update_layout(mapbox_style='open-street-map'))
])

], style={'background-color': "lightblue"}))

#Premier graph
@app.callback(
    dependencies.Output('RATP bar chart trafic', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        filtered_ndf = ndf
    else:
        filtered_ndf = ndf[ndf['Réseau'] == category]

    return px.bar(filtered_ndf, x='Station', y='Trafic', title='Graphique qui représente les 10 stations les plus fréquentées')

#Deuxieme graph
@app.callback(
    dependencies.Output('RATP pie chart trafic', 'figure'),
    dependencies.Input('category-filter', 'value')
)
def update_pie_chart(selected_category):
    if selected_category is None:
        filtered_df = top_villes
    else:
        filtered_df = df[df['Réseau'] == selected_category].groupby('Ville').sum().sort_values(by=['Trafic'],ascending=False).head(5).reset_index()

    fig = px.pie(filtered_df, names='Ville', values='Trafic', title='Graphique qui représente le trafic des 5 plus grande villes')
    return fig

#Troisieme graph
@app.callback(
    dependencies.Output('IDF par exploitant', 'figure'),
    [dependencies.Input('category-filter2', 'value')]
)

def update_bar_chart_emp(exploitant,filtered_emp=emp_df):
    if exploitant is None:
        filtered_emp = emp_df
    else:
        filtered_emp = emp_df[emp_df['exploitant'] == exploitant]
    emp_sort_x = filtered_emp.groupby('exploitant').groups.keys()
    emp_sort_y = filtered_emp.groupby('exploitant').size().sort_values(ascending=False)
    return px.bar(filtered_emp, x=emp_sort_x, y=emp_sort_y, title="Nombre de lignes par exploitant",labels={'x': 'exploitant', 'y': 'Nombre de lignes '})
#Quatrieme graph
@app.callback(
    dependencies.Output('IDF par ligne', 'figure'),
    [dependencies.Input('category-filter2', 'value')]
)
def update_bar_chart_lgn(exploitant):


    if exploitant is None:
        filtered_emp = emp_df
    else:
        filtered_emp = emp_df[emp_df['exploitant'] == exploitant]
    lgn_sort_x = filtered_emp.groupby('ligne').groups.keys()
    lgn_sort_y = filtered_emp.groupby('ligne').size().sort_values(ascending=False)
    return px.bar(filtered_emp, x=lgn_sort_x, y=lgn_sort_y, title="Nombre de lignes par lignes",labels={'x': 'lignes', 'y': 'Nombre de lignes '})

if __name__ == '__main__':
    app.run_server(debug=True)

app.run_server(host='0.0.0.0', port=8050, debug=True)
