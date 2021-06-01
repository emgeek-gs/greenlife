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
from branca.element import Template, MacroElement

''''points = gpd.GeoDataFrame.from_file('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/checkins.geojson') # or geojson etc
polys = gpd.GeoDataFrame.from_file('C:/Users/Mannu/Desktop/Polardot Docs/JOBS/Festus LIS/Vectors/ken_admbnda_adm1_iebc_20191031.shp')
pointInPoly = gpd.sjoin(points, polys, op='within')'''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
application = app.server
app.title='Greenlife Analytics!'

token = "pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg"

res1 = requests.get('https://portal.greenlife.co.ke/api/checkin')

response1 = json.loads(res1.text)
response1

data_ch = pd.json_normalize(response1, 'checkins')

with open('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/webapp/assets/checkinorder.geojson') as f2:
    gj_1 = geojson.load(f2)
gj_1
with open('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/webapp/assets/checkintsa2.geojson') as f3:
    gj_2 = geojson.load(f3)
gj_1
features_1 = gj_1['features'][0]
features_1
data_ch.columns.values[[0,1,2,3,4,5,6,7,8,9]] = ['Date','Time','Location','Latitude','Longitude','County','Region','TSA First Name','TSA Last Name','Order']
for col in ['Date']:
    data_ch[col] = pd.to_datetime(data_ch[col], format='%d/%m/%Y')
data_ch.sort_values(by='Date',inplace=True, ascending=True)
data_ch['TSA Name']  = data_ch.iloc[:, 7] + ' ' + data_ch.iloc[:, 8]

data_ch2 = data_ch.iloc[:, [0,1,2,10,3,4,5,6,9]]
data_ch2['Order'] = data_ch2['Order'].astype(float)
data_ch2['Latitude'] = data_ch2['Latitude'].astype(float)
data_ch2['Longitude'] = data_ch2['Longitude'].astype(float)

total_per_tsa=data_ch2.groupby(['TSA Name'], as_index=False).agg({'Order' : 'sum'}).sort_values(by=['Order'], ascending=False)

total_per_region=data_ch2.groupby(['Region'], as_index=False).agg({'Order' : 'sum'}).sort_values(by=['Order'], ascending=False)
total_per_county=data_ch2.groupby(['County'], as_index=False).agg({'Order' : 'sum'}).sort_values(by=['Order'], ascending=False)
total_per_county
total_per_county['Order'] = total_per_county['Order'].astype(float)
total_per_county.to_csv('data_analytics_county.csv',index=False)


tsa_daily=data_ch2.groupby(['Date'], as_index=False).agg({'Order' : 'sum'})
tsa_daily

public_health = data_ch2[data_ch2['TSA Name'].str.contains('Samuel Mbithi')]
public_health.to_csv('data_analytics.csv',index=False)
public_health_daily=public_health.groupby(['Date'], as_index=False).agg({'Order' : 'sum'})
public_health_daily

total_ord = data_ch2.loc[:, 'Order']
total_public_h = public_health.loc[:, 'Order']
total_order = total_ord.sum(axis=0)
total_public_health = total_public_h.sum(axis=0)

trial_data = pd.read_csv('https://raw.githubusercontent.com/emgeek-gs/greenlife/main/assets/locationproducts2.csv')

response = requests.get('https://raw.githubusercontent.com/emgeek-gs/greenlife/main/assets/locationproducts2.geojson')

gj = response.json()



features = gj['features'][0]
features
trial_data = pd.read_csv('C:/Users/Mannu/Desktop/surveyexe/Plans/Data Practise/Greenlife/webapp/assets/locationproducts2.csv')
trial_data

county_total=trial_data.groupby(['ADM1_EN'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})
county_total


m3 = folium.Map((0.04626, 37.65587), tiles=None, zoom_start=6)

folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckoienmus0cx218qjz625pnf0/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg', name='Base Map',attr='Emmanuel Nzyoka').add_to(m3)

def style_zero_function(feature):
    default_style = {
        'fillOpacity': 0.3,
        'color': 'black',
        'weight': 0.4
    }

    default_style['fillPattern'] = plugins.pattern.StripePattern(angle=-45)

    return default_style
highlight_function = lambda x: {'fillColor': '#8033ff',
                                'color':'#8033ff',
                                'fillOpacity': 0.70,
                                'weight': 0.4}
folium.GeoJson(
    gj_2,
    style_function=style_zero_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['COUNTY'],
        aliases=['County'],
        localize=False
    ),
    name='Community').add_to(m3)



colormap_dept = cm.StepColormap(
    colors=['#00ae53', '#86dc76', '#daf8aa',
            '#ffe6a4', '#ff9a61', '#ee0028'],
    vmin=min(total_per_county['Order']),
    vmax=max(total_per_county['Order']),
    index=[0,1000000,2000000,5000000,10000000,20000000,120000000])
style_function = lambda x: {
    'fillColor': colormap_dept(x['properties']['ORDER']),
    'color': 'black',
    'weight': 0.7,
    'fillOpacity': 0.7
}
folium.GeoJson(
    gj_1,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['COUNTY', 'ORDER'],
        aliases=['County', 'Orders'],
        localize=False
    ),
    name='dataviz').add_to(m3)

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>
<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:0px; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:25px; left: 0px; top: 0px;'>

<div class='legend-title'>TSA Orders per County</div>

</div>

<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>

<div class='legend-title'>Legend (Kshs)<br></div>
<div class='legend-scale'>


  <ul class='legend-labels'>

    <li><span style='background:#00ae53;opacity:0.7;'></span>0 - 1,000,000</li>
    <li><span style='background:#86dc76;opacity:0.7;'></span>1,000,000 - 2,000,000</li>
    <li><span style='background:#daf8aa;opacity:0.7;'></span>2,000,000 - 5,000,000</li>
    <li><span style='background:#ffe6a4;opacity:0.7;'></span>5,000,000 - 10,000,000</li>
    <li><span style='background:#ff9a61;opacity:0.7;'></span>10,000,000 - 20,000,000</li>
    <li><span style='background:#ee0028;opacity:0.7;'></span>20,000,000 - 120,000,000</li>
    <li><span style='background:repeating-linear-gradient(
    -55deg,
    #ffffff,
    #ffffff 5px,
    #b2b2b2 5px,
    #b2b2b2 10px);
    opacity:0.7;'></span>No Orders</li>
  </ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
m3.get_root().add_child(macro)

m3.save('county.html')






token = "pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg"


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
#data_1.to_csv('data_analytics.csv',index=False)
for col in ['Date']:
    data_1[col] = pd.to_datetime(data_1[col], format='%d/%m/%Y')
data_1.sort_values(by='Date',inplace=True, ascending=True)
data_1
# Trial Data trial_data =
#trial_data = pd.read_csv('data_analytics_fk.csv')

product_per_day=data_1.groupby(['Date', 'Product Name'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'})

product_total=data_1.groupby(['Product Name'], as_index=False).agg({'Amount' : 'sum', 'Quantity' : 'sum'}).sort_values(by=['Amount'], ascending=False)

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
m2 = folium.Map((0.04626, 37.65587), tiles=None, zoom_start=6)

folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckiyknitw6tcx1al28jnkbqyk/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg', name='Base Map',attr='Emmanuel Nzyoka').add_to(m2)

heat_data2 = [[row['Latitude'],row['Longitude']] for index, row in data_ch2.iterrows()]

HeatMap(heat_data2, name = "Heat Map").add_to(m2)
marker_cluster = MarkerCluster(heat_data2,name = "Cluster Map")
# Add marker cluster to map
marker_cluster.add_to(m2)
folium.LayerControl().add_to(m2)

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>
<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:0px; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:25px; left: 0px; top: 0px;'>

<div class='legend-title'>HeatMap and Clustermap</div>

</div>



</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
m2.get_root().add_child(macro)
m2.save('uzito2.html')

m = folium.Map((0.04626, 37.65587), tiles=None, zoom_start=6)

folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/emmanuelnzyoka/ckiyknitw6tcx1al28jnkbqyk/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZW1tYW51ZWxuenlva2EiLCJhIjoiY2swYzA5MTVqMHgweTNsbWR6cTc1OXp3bSJ9.lzaPgndzbQq014PHdgkIsg', name='Base Map',attr='Emmanuel Nzyoka').add_to(m)

mcg = folium.plugins.MarkerCluster(control=False)
m.add_child(mcg)

g1 = folium.plugins.FeatureGroupSubGroup(mcg, "Heat Map")
m.add_child(g1)

g2 = folium.plugins.FeatureGroupSubGroup(mcg, "Clustermap")
m.add_child(g2)
heat_data = [[row['Latitude'],row['Longitude']] for index, row in data_1.iterrows()]

HeatMap(heat_data, name = "Heat Map").add_to(g1)
marker_cluster = MarkerCluster(heat_data,name = "Cluster Map")
# Add marker cluster to map
marker_cluster.add_to(g2)
folium.LayerControl(collapsed=False).add_to(m)



m.save('uzito.html')




"""fig = px.scatter_mapbox(data_1, lat="Latitude", lon="Longitude", color ="Amount" ,size="Quantity",color_continuous_scale=px.colors.sequential.Viridis,size_max=25,

                               hover_name="Product Name", hover_data=['Date','Time','Amount','Quantity','Location'])
fig.update_layout(mapbox_style='light', mapbox_accesstoken=token,mapbox_zoom=5, mapbox_center = {"lat":0.04626, "lon": 37.65587},title="Delivery Locations", height=600)
fig.update(layout=dict(title=dict(x=0.5)))"""
fig1 = px.bar(total_per_county[:10], y= 'County', x='Order',hover_data=['County','Order'],orientation='h')

fig1.update_layout(
    xaxis_title="Amount",
    yaxis_title="County",
    title="TSA orders per County")
fig1.update(layout=dict(title=dict(x=0.5)))
fig1.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})


fig2 = px.pie(product_total[:10], values='Amount', names='Product Name', title='Best Performing Delivery Products')

fig2.update(layout=dict(title=dict(x=0.5)))
fig2.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig3 = px.area(total_per_day, x='Date', y='Amount', hover_data=['Amount','Quantity','Date'],color_discrete_sequence =['blue']*len(total_per_day))

fig3.update_xaxes(dtick= 86400000*3)

fig4 = px.area(tsa_daily, x='Date', y='Order', hover_data=['Order','Date'],color_discrete_sequence =['blue']*len(total_per_day))
fig3.update_layout(
    title= "Daily Delivery Sales")
fig3.update(layout=dict(title=dict(x=0.5)))

fig4.update_xaxes(dtick= 86400000*12)
fig4.update_layout(
    title= "Daily TSA orders")
fig4.update(layout=dict(title=dict(x=0.5)))
fig3.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig3.update_layout(hovermode="x unified")
fig4.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig4.update_layout(hovermode="x unified")
#fig2 = px.line(trial_data, x=date, y=amount,color=employee_name)

fig6 = px.bar(county_total, y= 'ADM1_EN', x='Amount',hover_data=['ADM1_EN','Amount','Quantity'],orientation='h',height=400,color='ADM1_EN')


fig6.update_layout(
    xaxis_title="Amount",
    yaxis_title="County",
    title="Sales per County")
fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig7 = px.pie(total_per_tsa[:10], values='Order', names='TSA Name', title='Best Performing TSAs')
fig7.update(layout=dict(title=dict(x=0.5)))
fig8 = px.pie(total_per_region, values='Order', names='Region', title='Regional Orders')
fig8.update(layout=dict(title=dict(x=0.5)))

app.layout = html.Div([
    html.H1(children = 'GREENLIFE ANALYTICS DASHBOARD',style={'text-align': 'center'}),
    html.Div(),

    html.Div(children = 'Total Sales TSA: Kshs. ' + str(total_order)),
    html.Div(children = 'Total Sales Deliveries: Kshs. ' + str(total_amount)),
    html.Div(children = 'Total Sales Public Health: Kshs. ' + str(total_public_health)),
    html.Div(children=[

        # first column of first row
        html.Div(children=[


            html.Iframe(id = 'map3', srcDoc = open('county.html','r').read(),height =550,width=1300),

        ], style={ 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

    ], className='row'),
        html.Div(children=[

            # first column of second row
            html.Div(children=[

                 dcc.Graph(figure=fig7)

            ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),

            # second column of second row
            html.Div(children=[

                dcc.Graph(figure=fig1)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),


        ], className='row'),
    # first row
    html.Div([

        # first column of first row
        html.Div(children=[

            html.Iframe(id = 'map2', srcDoc = open('uzito2.html','r').read(),height =450,width=1300),

        ], style={ 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '1vw'}),

    ], className='row'),

        html.Div(children=[

            # first column of second row
            html.Div(children=[

                 dcc.Graph(figure=fig8)

            ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),

            # second column of second row
            html.Div(children=[

                dcc.Graph(figure=fig4)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),


        ], className='row'),
        html.Div(children=[

            # first column of first row
            html.Div(children=[


                html.Iframe(id = 'map', srcDoc = open('uzito.html','r').read(),height =450,width=1300),

            ], style={ 'vertical-align': 'top', 'margin-left': '6vw', 'margin-top': '3vw'}),

        ], className='row'),
        html.Div(children=[

            # first column of second row
            html.Div(children=[

                 dcc.Graph(figure=fig2)

            ], style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),

            # second column of second row
            html.Div(children=[

                dcc.Graph(figure=fig3)
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw','text-align': 'center','margin-top': '3vw'}),


        ], className='row'),



    ],
    )


if __name__ == '__main__':
    application.run(port=8080)
