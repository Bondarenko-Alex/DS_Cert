# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

site_list = ['All Sites'] + list(spacex_df['Launch Site'].unique())
print(site_list)
print(spacex_df[['Launch Site', 'class']].groupby('Launch Site').mean())

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label':i, 'value':i} for i in site_list], value='All Sites', placeholder='Select Launch Site', searchable=True),
                                #dcc.Dropdown( 
                                #    options=sites_list, 
                                #    value='All Sites',
                                #    id='site-dropdown',
                                #),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max=10000, step=1000, value=[min_payload, max_payload], 
                                    id='payload-slider',),
                                #dcc.RangeSlider(id='payload-slider',
                                #    min=min_payload, max=max_payload, step=500, value=[min_payload, max_payload],
                                #),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def draw_pie(site):
    if site in set(spacex_df['Launch Site'].unique()):
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', names='class', title=f"Total Success Launches for site {site}",
            color='class', color_discrete_map={0:'red', 1:'blue'})
    else:
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success launches by all sites')
    return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def draw_scatter(site, payload):
    print(site, payload)
    if site in set(spacex_df['Launch Site'].unique()):
        df = spacex_df[spacex_df['Launch Site'] == site]
    else:
        df = spacex_df
    df = df[(df['Payload Mass (kg)'] >= payload[0]) & (df['Payload Mass (kg)'] <= payload[1])]
    fig = px.scatter(df, x='Payload Mass (kg)', y="Launch Site", color='class')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
