import plotly.offline as pyo
from plotly.graph_objs import *

trace1 = {
  "x": ["台北市", "新北市", "桃園市", "台中市", "高雄市", "彰化縣", "基隆市"],
  "y": [95, 33, 34, 9, 2, 1, 1],
  "marker": {"color": "rgb(248,118,109)"},
  "name": "檢傷一級",
  "showlegend": True,
  "type": "bar",
  "uid": "817a5d",
  "xaxis": "x",
  "yaxis": "y"
}
trace2 = {
  "x": ["台北市", "新北市", "桃園市", "台中市", "高雄市", "彰化縣", "新竹市", "基隆市", "台南市", "嘉義縣", "嘉義市"],
  "y": [118, 65, 15, 10, 6, 4, 4, 1, 4, 2, 1],
  "marker": {"color": "rgb(163,165,0)"},
  "name": "檢傷二級",
  "showlegend": True,
  "type": "bar",
  "uid": "140c8d",
  "xaxis": "x",
  "yaxis": "y"
}
trace3 = {
  "x": ["台北市", "新北市", "桃園市", "台中市", "彰化縣", "新竹市", "基隆市"],
  "y": [45, 34, 15, 3, 2, 1, 1],
  "marker": {"color": "rgb(0,191,125)"},
  "name": "檢傷三級",
  "showlegend": True,
  "type": "bar",
  "uid": "5375e8",
  "xaxis": "x",
  "yaxis": "y"
}
trace4 = {
  "x": ["台北市", "新北市", "台中市", "新竹市", "基隆市"],
  "y": [5, 8, 1, 6, 1],
  "marker": {"color": "rgb(0,176,246)"},
  "name": "檢傷四級",
  "showlegend": True,
  "type": "bar",
  "uid": "869e37",
  "xaxis": "x",
  "yaxis": "y"
}
trace5 = {
  "x": ["台北市"],
  "y": [1],
  "marker": {"color": "rgb(231,107,243)"},
  "name": "檢傷五級",
  "showlegend": True,
  "type": "bar",
  "uid": "286b75",
  "xaxis": "x",
  "yaxis": "y"
}
data = Data([trace1, trace2, trace3, trace4, trace5])
layout = {
  "annotations": [
    {
      "x": 1.05,
      "y": 0.52,
      "showarrow": False,
      "text": "<b>醫療檢傷</b>",
      "textangle": 0,
      "xanchor": "center",
      "xref": "paper",
      "yref": "paper"
    }
  ],
  "autosize": True,
  "barmode": "stack",
  "height": 583,
  "legend": {
    "x": 1.05,
    "y": 0.5,
    "bgcolor": "rgb(255,255,255)",
    "bordercolor": "transparent",
    "font": {"family": "STHeiti"},
    "xanchor": "center",
    "yanchor": "top"
  },
  "margin": {"r": 10},
  "paper_bgcolor": "rgb(255,255,255)",
  "plot_bgcolor": "rgb(229,229,229)",
  "showlegend": True,
  "titlefont": {"family": "STHeiti"},
  "width": 936,
  "xaxis": {
    "autorange": True,
    "gridcolor": "rgb(255,255,255)",
    "range": [-0.5, 10.5],
    "showgrid": True,
    "showline": False,
    "showticklabels": True,
    "tickangle": 0,
    "tickcolor": "rgb(127,127,127)",
    "tickfont": {
      "color": "rgb(127,127,127)",
      "family": "STHeiti",
      "size": 14.4
    },
    "ticks": "outside",
    "title": "醫院縣市別",
    "titlefont": {
      "color": "rgb(0, 0, 0)",
      "family": "STHeiti",
      "size": 18
    },
    "type": "category",
    "zeroline": False
  },
  "yaxis": {
    "autorange": True,
    "gridcolor": "rgb(255,255,255)",
    "range": [0, 277.894736842],
    "showgrid": True,
    "showline": False,
    "showticklabels": True,
    "tickangle": 0,
    "tickcolor": "rgb(127,127,127)",
    "tickfont": {
      "color": "rgb(127,127,127)",
      "family": "STHeiti",
      "size": 14.4
    },
    "ticks": "outside",
    "title": "人數",
    "titlefont": {
      "color": "rgb(0, 0, 0)",
      "family": "STHeiti",
      "size": 18
    },
    "type": "linear",
    "zeroline": False
  }
}
fig = Figure(data=data, layout=layout)
plot_url = pyo.plot(fig)
