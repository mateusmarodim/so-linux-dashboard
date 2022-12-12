import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html



def render_os_hw_info_page(sysinfo):
    
    return html.Div(
        [
            dbc.Row([
               dbc.Col(html.P("System:")), dbc.Col(html.P(sysinfo["System"])) 
            ]),
            dbc.Row([
               dbc.Col(html.P("Node Name:")), dbc.Col(html.P(sysinfo["Node Name"])) 
            ]),
            dbc.Row([
               dbc.Col(html.P("Release:")), dbc.Col(html.P(sysinfo["Release"])) 
            ]),
            dbc.Row([
               dbc.Col(html.P("Version:")), dbc.Col(html.P(sysinfo["Version"])) 
            ]),
            dbc.Row([
               dbc.Col(html.P("Machine:")), dbc.Col(html.P(sysinfo["Machine"])) 
            ]),
            dbc.Row([
               dbc.Col(html.P("Processor:")), dbc.Col(html.P(sysinfo["Processor"])) 
            ])
        ],
        className="os_hw-info"
    )    

