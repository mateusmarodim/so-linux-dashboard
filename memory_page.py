import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from MemoryMonitor import *


def render_memory_page(memory_info):
    return html.Div(
        [
            html.Div(render_memory_text(memory_info), className="memory-info-text"),
            html.Div(render_memory_graphs(memory_info), className="memory-info-graphs")
        ],
        className="memory-info"
    )
    
def render_memory_text(memory_info):
    rows = []
    rows.append(dbc.Row([
        dbc.Col(html.P("")),
        dbc.Col(html.P("Total")),
        dbc.Col(html.P("Disponível")),
        dbc.Col(html.P("Usada")),
        dbc.Col(html.P("Usada (%)"))
    ]))
    rows.append(dbc.Row([
        dbc.Col(html.P("Memória:")),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["memory_total"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["memory_available"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["memory_used"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["memory_percent"])))
    ]))
    rows.append(dbc.Row([
        dbc.Col(html.P("Swap:")),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["swap_total"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["swap_free"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["swap_used"]))),
        dbc.Col(html.P(MemoryMonitor.get_size(memory_info["swap_percent"])))
    ]))
    return rows

def render_memory_graphs(memory_info):
    rows = []
    rows.append(
        dbc.Row(
            [
                dbc.Col(html.P("Memória")),
                dbc.Col(html.P("Swap"))
            ]
        )
    )
    
    row = []
    row.append(dbc.Col(render_memory_graph(memory_info)))
    row.append(dbc.Col(render_swap_graph(memory_info)))
    rows.append(dbc.Row(row))
    return rows
    
def render_memory_graph(memory_info):
    fig = px.pie(values=[memory_info["memory_available"], memory_info["memory_used"]], names=["Disponível", "Usada"])
    return dcc.Graph(figure=fig)

def render_swap_graph(memory_info):
    fig = px.pie(values=[memory_info["swap_free"], memory_info["swap_used"]], names=["Disponível", "Usado"])
    return dcc.Graph(figure=fig)