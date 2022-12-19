import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html



def render_proc_page(proc):

    return html.Div(
        [
            html.Div(render_proc(proc), id="proc-text"),
            dcc.Interval(
                id='ps-interval',
                disabled=False,
                interval=1 * 500,
                n_intervals=0 # milliseconds
            )
        ],
        className="proc"
    )    

def render_proc(proc: dict):
    processo: list = proc["ps"].split('\n')
    comando: list = proc["comm"].split('\n')
    rows = []
    row = []
    header = str(processo[0]).split(' ')
    try:
        while True:
            header.remove('')
    except ValueError:
        pass
    header.append(comando[0])
    for k in range(len(header)):
        row.append(dbc.Col(html.H5(header[k].replace(' ', ''), style={"font-weight": "bold"})))
    rows.append(dbc.Row(row))
    row = []
    for i in range(len(processo)-2):
        proc_col = str(processo[i+1]).split(' ')
        try:
            while True:
                proc_col.remove('')
        except ValueError:
            pass
        for j in range(len(proc_col)):
            row.append(dbc.Col(html.P(proc_col[j].replace(' ', ''))))
        row.append(dbc.Col(html.P(comando[i+1])))
        rows.append(dbc.Row(row))
        row = []
    return rows