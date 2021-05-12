import requests
import json
import pandas as pd
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px
import branca.colormap as cm
import geojson
import dash
import dash_bootstrap_components as dbc           #(version 1.9.1) pip install dash==1.9.1
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import folium
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
with open('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/webapp/assets/locationproducts2.geojson') as f:
    gj = geojson.load(f)
gj
features = gj['features'][0]
features
trial_data = pd.read_csv('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/webapp/assets/locationproducts2.csv')
trial_data

county_total=trial_data.groupby(['ADM1_EN'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})
county_total

loc = 'County Sales Map'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)
m3 = folium.Map([0.04626, 37.65587], tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckoienmus0cx218qjz625pnf0/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg',attr='Emmanuel Nzyoka', zoom_start=6)
colormap_dept = cm.StepColormap(
    colors=['#00ae53', '#86dc76', '#daf8aa',
            '#ffe6a4', '#ff9a61', '#ee0028'],
    vmin=min(county_total['Amount']),
    vmax=max(county_total['Amount']),
    index=[0,5000,10000,50000,100000,200000,1250000])

style_function = lambda x: {
    'fillColor': colormap_dept(x['properties']['Amount']),
    'color': 'black',
    'weight': 1.2,
    'fillOpacity': 0.7
}
folium.GeoJson(
    gj,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['ADM1_EN','Quantity','Amount'],
        aliases=['County','Quantity','Amount'],
        localize=False
    ),
    name='dataviz').add_to(m3)
m3.save('county.html')





token = "pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg"

app = dash.Dash(__name__)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
res = requests.get('https://portal.greenlife.co.ke/api/delivery')

response = json.loads(res.text)
response


data = pd.json_normalize(response, 'delivery')
data
data.iloc[:,57]
data.columns = data.columns.map(lambda x: x.split(".")[-1])


data.columns.values[[14,24,15,2,3,61,8,4,5,6,57]] = ['Employee First Name','Employee Middle Name','Employee Last Name','Date','Time','Product Name','Quantity','Location','Latitude','Longitude','Price']
data['Price']
data['Quantity'] = data['Quantity'].astype(float)
data['Price'] = data['Price'].astype(float)
data['Price']
data['Latitude'] = data['Latitude'].astype(float)
data['Longitude'] = data['Longitude'].astype(float)
data['Amount']  = data.iloc[:, 8] * data.iloc[:,57]

data['Employee Name']  = data.iloc[:, 14] + ' ' + data.iloc[:, 24] + ' ' + data.iloc[:,15]
col_mapping = [f"{c[0]}:{c[1]}" for c in enumerate(data.columns)]
col_mapping
data_2 = data.iloc[:, [107,2,3,61,8,4,5,6,57,106,]]
data_2
data_1 = data_2.dropna(subset = ['Price','Product Name'])
data_1
data_1.to_csv('data_analytics.csv',index=False)
for col in ['Date']:
    data_1[col] = pd.to_datetime(data_1[col], format='%d/%m/%Y')
data_1.sort_values(by='Date',inplace=True, ascending=True)
data_1
# Trial Data trial_data =
#trial_data = pd.read_csv('data_analytics_fk.csv')

product_per_day=data_1.groupby(['Date', 'Product Name'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})

product_total=data_1.groupby(['Product Name'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})

product_total
employee_per_day=data_1.groupby(['Date', 'Employee Name'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})




total_per_day=data_1.groupby(['Date'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})
total_per_day





product_name= data_1.loc[:, 'Product Name']
employee_name = data_1.loc[:, 'Employee Name']
amount = data_1.loc[:, 'Amount']
date = data_1.loc[:, 'Date']
quantity = data_1.loc[:, 'Quantity']

product_name_uq = product_name.sort_values().unique()


unique_product = data_1['Product Name'].drop_duplicates()
unique_product

employee_name_uq = employee_name.sort_values().unique()

total_amount = amount.sum(axis=0)
units_sold = quantity.sum(axis=0)
units_sold


fig = px.scatter_mapbox(data_1, lat="Latitude", lon="Longitude", color ="Amount" ,size="Quantity",color_continuous_scale=px.colors.sequential.Viridis,size_max=25,

                               hover_name="Product Name", hover_data=['Date','Time','Amount','Quantity','Location'])
loc = ' Density Heat Map'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)
m = folium.Map([0.04626, 37.65587], tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckoienmus0cx218qjz625pnf0/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg',attr='Emmanuel Nzyoka', zoom_start=6)
heat_data = [[row['Latitude'],row['Longitude']] for index, row in data_1.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('uzito.html')

m2 = folium.Map([-0.44626, 37.65587], tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckoienmus0cx218qjz625pnf0/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg',attr='Emmanuel Nzyoka', zoom_start=7)
# Create a folium marker cluster
marker_cluster = MarkerCluster(heat_data)

# Add marker cluster to map
marker_cluster.add_to(m2)
m2.save('uzito2.html')

fig.update_layout(mapbox_style='light', mapbox_accesstoken=token,mapbox_zoom=5, mapbox_center = {"lat":0.04626, "lon": 37.65587},title="Delivery Locations", height=600)
fig.update(layout=dict(title=dict(x=0.5)))

fig1 = px.bar(product_total, y= 'Product Name', x='Quantity',hover_data=['Product Name','Quantity','Amount'],orientation='h',height=800,color_discrete_sequence =['green']*len(product_total))
fig2 = px.bar(product_total, y= 'Product Name', x='Amount',hover_data=['Product Name','Amount','Quantity'],orientation='h',height=800,color_discrete_sequence =['green']*len(product_total))
fig1.update_layout(
    xaxis_title="Units Sold",
    yaxis_title="Product Name",
    title= "Units Sold per Product")
fig1.update(layout=dict(title=dict(x=0.5)))
fig2.update_layout(
    xaxis_title="Amount",
    yaxis_title="Product Name",
    title="Sales per Product")
fig2.update(layout=dict(title=dict(x=0.5)))
fig3 = px.area(total_per_day, x='Date', y='Amount', hover_data=['Amount','Quantity','Date'],color_discrete_sequence =['green']*len(total_per_day))
fig3.update_xaxes(dtick= 86400000*3)

fig4 = px.area(total_per_day, x='Date', y='Quantity', hover_data=['Amount','Quantity','Date'],color_discrete_sequence =['green']*len(total_per_day))
fig3.update_layout(
    title= "Daily Sales")
fig3.update(layout=dict(title=dict(x=0.5)))
fig4.update_xaxes(dtick= 86400000*3)
fig4.update_layout(
    title= "Units Sold per day")
fig4.update(layout=dict(title=dict(x=0.5)))
#fig2 = px.line(trial_data, x=date, y=amount,color=employee_name)
fig5 = px.bar(county_total, y= 'ADM1_EN', x='Quantity',hover_data=['ADM1_EN','Quantity','Amount'],orientation='h',height=400,color_discrete_sequence =['green']*len(product_total))
fig6 = px.bar(county_total, y= 'ADM1_EN', x='Amount',hover_data=['ADM1_EN','Amount','Quantity'],orientation='h',height=400,color_discrete_sequence =['green']*len(product_total))
fig5.update_layout(
    xaxis_title="Units Sold",
    yaxis_title="ADM1_EN",
    title= "Units Sold per County")
fig5.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(
    xaxis_title="Amount",
    yaxis_title="ADM1_EN",
    title="Sales per County")
fig6.update(layout=dict(title=dict(x=0.5)))

app.layout = html.Div([
    html.H2('GREENLIFE ANALYTICS DASHBOARD',style={'text-align': 'center'}),
    html.Div([], className = 'one column'),

        dcc.Textarea(
        id='textarea-example',
        value='Total Units Sold: ' + str(units_sold),
        style={'width':'30%'},

    ),
    dcc.Textarea(
       id='textarea-example2',
       value='Total Sales: Kshs. ' + str(total_amount),
       style={'width':'30%'},
    ),
    # first row
    html.Div([

        # first column of first row
        html.Div(children=[

            dcc.Graph(figure=fig)

        ], style={ 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '1vw'}),

    ], className='row'),

        html.Div(children=[

            # first column of second row
            html.Div(children=[

                 dcc.Graph(figure=fig3)

            ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),

            # second column of second row
            html.Div(children=[

                dcc.Graph(figure=fig4)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),


        ], className='row'),
    html.Div(children=[

        # first column of first row
        html.Div(children=[

            dcc.Graph(figure=fig1)

        ], style={'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw','text-align': 'center'}),

        # second column of first row
        html.Div(children=[

            dcc.Graph(figure=fig2)
        ], style={'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw','text-align': 'center'}),


    ], className='row'),
        html.Div(children=[

            # first column of first row
            html.Div(children=[

                html.H2('Sales Per County',style={'text-align': 'center'}),
                html.Iframe(id = 'map3', srcDoc = open('county.html','r').read(),height =550,width=1300),

            ], style={ 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

        ], className='row'),
        html.Div(children=[

            # first column of second row
            html.Div(children=[

                 dcc.Graph(figure=fig5)

            ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '3vw','text-align': 'center'}),

            # second column of second row
            html.Div(children=[

                dcc.Graph(figure=fig6)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','text-align': 'center'}),


        ], className='row'),
    html.Div(children=[

        # first column of first row
        html.Div(children=[

            html.H2('Density Heatmap',style={'text-align': 'center'}),
            html.Iframe(id = 'map', srcDoc = open('uzito.html','r').read(),height =450,width=1300),

        ], style={ 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

    ], className='row'),
    html.Div(children=[

        # first column of first row
        html.Div(children=[

            html.H2('Clustermap',style={'text-align': 'center'}),
            html.Iframe(id = 'map2', srcDoc = open('uzito2.html','r').read(),height =550,width=1300),

        ], style={ 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

    ], className='row'),
    ],
    )



if __name__ == '__main__':
    app.run_server()
