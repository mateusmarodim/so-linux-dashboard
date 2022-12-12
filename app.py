import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from memory_page import *
from disk_info_page import *
from proc_page import *
from os_hardware_page import *


from Terminal import *
from DiskMonitor import *
from MemoryMonitor import *
from SystemInfoMonitor import *

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("Dash SO", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Sistema/Hardware", href="/", active="exact"),
                dbc.NavLink("Processos/Threads", href="/proc", active="exact"),
                # dbc.NavLink("Sistema de Arquivo", href="/filesystem", active="exact"),
                dbc.NavLink("Memória", href="/memory", active="exact"),
                dbc.NavLink("Disco", href="/disk", active="exact"),
                dbc.NavLink("Network", href="/network", active="exact"),
                dbc.NavLink("Terminal", href="/terminal", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)




def render_disk_info_text(disk_info):
    rows = []
    rows.append(
        dbc.Row([
            dbc.Col(html.P("Dispositivo")),
            dbc.Col(html.P("Ponto de montagem")),
            dbc.Col(html.P("Tipo")),
            dbc.Col(html.P("Total(MB)")),
            dbc.Col(html.P("Usado (MB)")),
            dbc.Col(html.P("Usado (%)")),
            dbc.Col(html.P("Livre (MB)"))
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


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(render_os_hw_info_page(system.system_information()))
    elif pathname == "/proc":
        return html.Div(render_proc_page(terminal.get_process_list()))
    # elif pathname == "/filesystem":
    #     return html.P("SISTEMAS DE ARQUIVOS")
    elif pathname == "/memory":
        return render_memory_page(memoryMonitor.memory_info())
    elif pathname == "/disk":
        return html.Div(render_disk_info_page(diskMonitor.disk_info()))
    elif pathname == "/network":
        return html.P("NETWORK")
    elif pathname == "/terminal":
        return html.P("TERMINAL")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    memoryMonitor = MemoryMonitor()
    diskMonitor = DiskMonitor()
    terminal = Terminal()
    system = SystemInfoMonitor()
    app.run_server(port=8889)
