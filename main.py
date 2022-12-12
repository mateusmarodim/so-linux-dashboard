# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import platform
import psutil
import os
import subprocess
from sysinfo import *

app = Dash(__name__)


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def system_information():
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")


def cpu_information():
    print("=" * 40, "CPU Info", "=" * 40,'\n')
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False),'\n')
    print("Total cores:", psutil.cpu_count(logical=True), '\n')
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    print(f"Cpu usage: {psutil.cpu_percent(interval=None)}\n")
    percent_per_cpu = psutil.cpu_percent(interval=None, percpu=True)
    for i in range(psutil.cpu_count(logical = True)):
        print(f"Cpu_{i}: {percent_per_cpu[i]}\n")


def memory_information():
    # Memory Information
    print("=" * 40, "Memory Information", "=" * 40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("=" * 20, "SWAP", "=" * 20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")


def disk_information():
    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def network_information():
    print("=" * 40, "Network Information", "=" * 40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")



@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        bash_command = value
        teste = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        saida = (teste.communicate()[0])
        return html.Div(children=('You have entered: \n{}'.format(saida)))

@app.callback(
    Output('example-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    os.system('clear')

    cpu_units_update = []
    cpu_percents_update = psutil.cpu_percent(interval=None, percpu=True)
    for i in range(psutil.cpu_count(logical=True)):
        cpu_units_update.insert(i, f"cpu_{i}")
    print(cpu_percents_update)
    print(cpu_units_update)
    fig_update = go.Figure(data=[go.Bar(x=cpu_units_update, y=cpu_percents_update)],
                           layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
    )
    return fig_update

# ==============================================================================
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

cpu_units = []
cpu_percents = psutil.cpu_percent(interval=None, percpu=True)
for i in range(psutil.cpu_count(logical = True)):
    cpu_units.insert(i, f"cpu_{i}")

cpu_df = pd.DataFrame({
    "CPU": cpu_units,
    "Usage(%)": cpu_percents
})

fig = px.bar(cpu_df, x="CPU", y="Usage(%)", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(
        id='teste',
        children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Textarea(
        id='textarea-state-example',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 200},
    ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
    dcc.Graph(
        id='example-graph'
    ),
    dcc.Interval(
        id='interval-component',
        disabled=False,
        interval=1 * 3000,  # in milliseconds
        max_intervals=4,
        n_intervals=0
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
    #system_information()
    #cpu_information()
    #memory_information()
    #disk_information()
    #list_files('/home/mateus/Downloads')
    #network_information()
