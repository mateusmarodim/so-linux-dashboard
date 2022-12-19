import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html


def render_network_info_page(networkinfo):
   return html.Div(
      [
         dbc.Row(render_network_info(networkinfo))
      ]
   )

def render_network_info(networkinfo):
    rows = []
    for i in range(len(networkinfo["interface"])):
        rows.append(
            dbc.Row([
                dbc.Col(html.P(networkinfo["interface"][i])),
                dbc.Col(html.P(networkinfo["adress"][i])),
                dbc.Col(html.P(networkinfo["netmask"][i])),
                dbc.Col(html.P(networkinfo["broadcast"][i])),
            ]))
    return rows