
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import colorlover as cl
import plotly.colors as plc

data_values = (np.random.randn(22)*100+100)


#### create colorscale
colors = cl.scales['8']['seq']['OrRd']

# interpolate to get 100 different colors in the color scale gradient
interp_colors=cl.to_rgb(cl.interp( colors, 100 ))
my_colorscale = plc.make_colorscale(interp_colors) # create colorscale e.g. [0.23,'rgb(103, 29, 45)'']


### assemble into format for data and layout

dummy_trace=(
    go.Scatter(x=[0, 150],
                y=[0, 80],
                mode='markers',
                marker=dict(size=1,
                            color=[np.min(data_values), np.max(data_values)],
                            colorscale=my_colorscale,
                            showscale=True),
                hoverinfo='None'
                )
            )
my_data = go.Data([dummy_trace])




map_layout = go.Layout(
    height=500,
    width=500,
    autosize=True,
    hovermode='closest',


)





# putting all together in to a plot
fig = dict(data=my_data, layout=map_layout)
pyo.plot(fig, filename='dummy_trace.html')
