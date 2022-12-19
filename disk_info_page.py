import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html



def render_disk_info_page(disk_info):
    disk_percentages = disk_info["percent"]
    devices = disk_info["device"]
    
    return html.Div(
        [
            html.H5("Informações de disco", style={"margin-bottom": "40px"}),
            html.Div(render_disk_info_text(disk_info), id="disk-text"),
            html.Div(render_disk_info_graphs(devices, disk_percentages), id="disk-graphs", style={"margin-top": "50px"}),
            dcc.Interval(
                id='disk-interval',
                disabled=False,
                interval=1 * 500,
                n_intervals=0 # milliseconds
            )
        ],
        className="disk-info"
    )    

def render_disk_info_text(disk_info):
    rows = []
    rows.append(
        dbc.Row([
            dbc.Col(html.P("Dispositivo", style={"font-weight": "bold"})),
            dbc.Col(html.P("Ponto de montagem", style={"font-weight": "bold"})),
            dbc.Col(html.P("Tipo", style={"font-weight": "bold"})),
            dbc.Col(html.P("Total(MB)", style={"font-weight": "bold"})),
            dbc.Col(html.P("Usado (MB)", style={"font-weight": "bold"})),
            dbc.Col(html.P("Usado (%)", style={"font-weight": "bold"})),
            dbc.Col(html.P("Livre (MB)", style={"font-weight": "bold"}))
        ]))
    for i in range(len(disk_info["device"])):
        rows.append(
            dbc.Row([
                dbc.Col(html.P(disk_info["device"][i])),
                dbc.Col(html.P(disk_info["mountpoint"][i])),
                dbc.Col(html.P(disk_info["fstype"][i])),
                dbc.Col(html.P(disk_info["total"][i])),
                dbc.Col(html.P(disk_info["used"][i])),
                dbc.Col(html.P(disk_info["percent"][i])),
                dbc.Col(html.P(disk_info["free"][i]))
            ]))
    return rows

def render_disk_info_graphs(devices, percentages):
    rows = []
    row = []
    for i in range(len(devices)):
        row.append(dbc.Col(html.P(devices[i], style={"text-align": "center", "font-weight": "bold"})))
    rows.append(dbc.Row(row))
    
    row = []
    for i in range(len(devices)):
        row.append(dbc.Col(render_disk_info_graph(percentages[i])))
    rows.append(dbc.Row(row))
    
    return rows
    
def render_disk_info_graph(percentage):
    fig = px.pie(values=[percentage, 100-percentage], names=["Usado", "Livre"])
    return dcc.Graph(figure=fig)