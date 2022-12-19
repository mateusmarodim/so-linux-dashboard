import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from memory_page import *
from disk_info_page import *
from proc_page import *
from os_hardware_page import *
from network_page import *


from Terminal import Terminal
from CPUMonitor import CPUMonitor
from DiskMonitor import DiskMonitor
from MemoryMonitor import MemoryMonitor
from SystemInfoMonitor import SystemInfoMonitor
from NetworkMonitor import NetworkMonitor

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

intervals = html.Div(
    [
        dcc.Interval(
            id="cpu-interval",
            interval= 1 * 1000,
            n_intervals=0
        ),dcc.Interval(
            id="mem-interval",
            interval= 1 * 1000,
            n_intervals=0
        ),dcc.Interval(
            id="ps-interval",
            interval= 1 * 1000,
            n_intervals=0
        ),dcc.Interval(
            id="disk-interval",
            interval= 1 * 1000,
            n_intervals=0
        )
    ]
)



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
    if (not cpu.get_is_running()):
        cpu.start()
    if (not mem.get_is_running()):
        mem.start_monitor()
    if (not disk.get_is_running()):
        disk.start_monitor()
    if (not terminal.get_is_running()):
        terminal.start_terminal()
    if pathname == "/":
        return html.Div(render_os_hw_info_page(cpu.cpu_info(),system.system_information()))
    elif pathname == "/proc":
        return html.Div(render_proc_page(terminal.get_process_list()))
    elif pathname == "/memory":
        return render_memory_page(mem.memory_info())
    elif pathname == "/disk":
        return html.Div(render_disk_info_page(disk.disk_info()))
    elif pathname == "/network":
        return html.P(render_network_info(network.network_info()))
    elif pathname == "/terminal":
        terminal.open_terminal()
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

@app.callback(
    Output('cpu-freq', 'children'),Input('cpu-interval', 'n_intervals')
)
def update_cpu_freq(n):
    if (not cpu.get_is_running()):
        cpu.run()

    cpuinfo = cpu.cpu_info()
    freq = cpuinfo["cpu_freq_info"]
    return render_freq(freq=freq)

@app.callback(
    Output('cpu-usage', 'children'),Input('cpu-interval', 'n_intervals')
)
def update_cpu_usage(n):
    if (not cpu.get_is_running()):
        cpu.run()
    
    cpuinfo = cpu.cpu_info()
    pcpu = cpuinfo["cpu_core_usage"]

    return render_usage(pcpu)

@app.callback(
    Output('gpu', 'children'),Input('cpu-interval', 'n_intervals')
)
def update_gpu(n):
    if (not cpu.get_is_running()):
        cpu.run()

    cpuinfo = cpu.cpu_info()
    gpu = cpuinfo["gpu_info"]

    return render_gpu(gpu)

@app.callback(
    Output('memory-text', 'children'),Input('mem-interval', 'n_intervals')
)
def update_mem_text(n):
    if (not mem.get_is_running()):
        mem.run()
    meminfo = mem.memory_info()
    print('oie')
    return render_memory_text(meminfo)

@app.callback(
    Output('memory-graphs', 'children'),Input('mem-interval', 'n_intervals')
)
def update_mem_graphs(n):
    if (not mem.get_is_running()):
        mem.start_monitor()
    meminfo = mem.memory_info()
    return render_memory_graphs(meminfo)

@app.callback(
    Output('proc-text', 'children'), Input('ps-interval', 'n_intervals')
)
def update_proc_text(n):
    if (not terminal.get_is_running()):
        terminal.start_terminal()
    return render_proc(terminal.get_process_list())

@app.callback(
    Output('disk-text', 'children'), Input('disk-interval', 'n_intervals')
)
def update_disk_text(n):
    if (not disk.get_is_running()):
        disk.start_monitor()
    return render_disk_info_text(disk.disk_info())

@app.callback(
    Output('disk-graphs', 'children'), Input('disk-interval', 'n_intervals')
)
def update_disk_text(n):
    if (not disk.get_is_running()):
        disk.start_monitor()

    info = disk.disk_info()
    devs = info["device"]
    perc = info["percent"]

    return render_disk_info_graphs(devs,perc)

if __name__ == "__main__":
    mem = MemoryMonitor()
    disk = DiskMonitor()
    terminal = Terminal()
    system = SystemInfoMonitor()
    network = NetworkMonitor()
    cpu = CPUMonitor()
    app.run_server(port=8889)
