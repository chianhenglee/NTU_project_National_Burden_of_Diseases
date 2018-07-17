import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import json
import colorlover as cl
import plotly.colors as plc

mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"

######## Loading Essential Data for plotting polygons of counties and cities #######
# Get counties name list
with open('counties/counties_list.txt') as f:
    Clist=f.read().splitlines()

# Get centroid of polygons correspond to Clist order
with open('counties/counties_centroid.txt') as f2:
    temp_coords = f2.read().splitlines()
temp2=[i.split(',') for i in temp_coords]
center_lonlat=[[float(k) for k in j] for j in temp2]

# Construct two dictionaries one for storing the lon,lat of the center of each county/city,
# another for storing geojson files (both as key,value pairs)
Dict_counties={}
Dict_counties_center={}
i=0
for c in Clist:
    with open('counties/'+c+'.json') as f:
        geojsonfile = json.load(f)
    Dict_counties[c]=geojsonfile
    Dict_counties_center[c]=center_lonlat[i]
    i=i+1





################# Get data from user specified conditions/criteria

'''
This should just be a function call to get the information needed for this plot
'''




# Here I use some randomly generated values as the data.
data_values = np.abs(np.random.randn(22)*100+100)


####### This section generate proper color scale for plotting ##########
### get color scale
colors = cl.scales['8']['seq']['OrRd']
#['rgb(255,247,236)', 'rgb(254,232,200)', 'rgb(253,212,158)',
# 'rgb(253,187,132)', 'rgb(252,141,89)', 'rgb(239,101,72)',
# 'rgb(215,48,31)', 'rgb(153,0,0)']
# interpolate to get 100 different colors in the color scale gradient
interp_colors=cl.to_rgb(cl.interp( colors, 100 ))
my_colorscale = plc.make_colorscale(interp_colors) # create colorscale e.g. [0.23,'rgb(103, 29, 45)'']
my_colorscale_nums = [i[0] for i in my_colorscale] # get the 0-1 values in each element from above


data_values_n = data_values/np.max(data_values)
index_data_color = [np.argmin(np.abs(np.array(my_colorscale_nums)-k)) for k in data_values_n]

# put it in a dictionary
Dict_colorscale={}
i=0
for c in Clist:
    Dict_colorscale[c] = my_colorscale[index_data_color[i]][1]
    i=i+1

### Now we generate colorbar manually as annotations in the layout
annotations = [
    dict(
        showarrow = False,
        align = 'right',
        text = '<b>Age-adjusted death rate<br>per county per year</b>',
        x = 0.95,
        y = 0.95,
    ),
    dict(
        showarrow = False,
        align = 'right',
        text = str(round(np.max(data_values),0)),
        x = 0.90,
        y = 0.85,
    ),
    dict(
        showarrow = False,
        align = 'right',
        text = str(round(np.min(data_values),0)),
        x = 0.90,
        y = 0.10,
    )]

for i, bin in enumerate(reversed(my_colorscale)):
	color = bin[1]
	annotations.append(
		dict(
			arrowcolor = color,
			#text = bin[0]*np.max(data_values),
			x = 0.95,
			y = 0.85-((i)*((0.85-0.1)/len(my_colorscale))), #0.90-(i/len(my_colorscale)),
			ax = -30,
			ay = 0,
			arrowwidth = 7,
			arrowhead = 0,
            hovertext = str(bin[0]*np.max(data_values))
		)
	)


######### plotting #########
### Plot data points (center of each polygon) on the map so that we can display hover information


data_polygon_center = go.Data(
    [go.Scattermapbox(
        name=i,
        showlegend=False,
        lat=[Dict_counties_center[i][1]],
        lon=[Dict_counties_center[i][0]],
        mode='markers',
        #marker=dict(size=1,),
        hoverinfo='text',
        text=
            'Country: '+i+'<br>'+
            #'Year:    '+time.map(str)+'<br>'+
            #'DALYs:   '+round(DALYs/1000,2).map(str)+'k'+'<br>'+
            #'L_Bound: '+round(L_bound/1000,2).map(str)+'k'+'<br>'+
            #'U_Bound: '+round(U_bound/1000,2).map(str)+'k',
            'Measure: '+str(data_values[ind])+'<br>'+
            'Here is the text shown when hover on a county/city'
    ) for ind,i in enumerate(Clist)]
)




###### Layout of the map #######

## Specify a list of layers (under mapbox under go.Layout) so that each layer(county/city)
## can have different colors.


counties_layers = [
    dict(
        sourcetype = 'geojson',
        source = Dict_counties[cc],
        type = 'fill',
        #color = 'rgba(130,30,10,0.7)' #layer_colors[cc]
        color = Dict_colorscale[cc],
        #color = data_values,
        opacity = 0.79
        )
for cc in Clist]


## Now put the county layers in layers under mapbox under go.Layout
map_layout = dict(
    height=800,
    width=800,
    autosize=True,
    hovermode='closest',
    annotations = annotations,
    mapbox=dict(
        layers=counties_layers,
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=23.67,
            lon=121.05
        ),

        zoom=6.8
    ),
)


# putting all together in to a plot
fig = dict(data=data_polygon_center, layout=map_layout)
pyo.plot(fig, filename='taiwan_choropleth_map.html')
