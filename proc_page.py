import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html



def render_proc_page(proc):

    return html.Div(
        [
            html.Div(render_proc(proc), className="proc-text"),
        ],
        className="proc"
    )    

def render_proc(proc):
    processo = proc.split('\n')
    rows = []
    row = []
    for i in range(len(processo)):
        proc_col = str(processo[i]).split(' ')
        try:
            while True:
                proc_col.remove('')
        except ValueError:
            pass
        for j in range(len(proc_col)):
            row.append(dbc.Col(html.P(proc_col[j].replace(' ', ''))))
        rows.append(dbc.Row(row))
        row = []
    return rows