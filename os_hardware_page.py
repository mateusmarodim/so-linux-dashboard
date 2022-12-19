import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html


def render_os_hw_info_page(cpuinfo, sysinfo):
   return html.Div(
      [
         dbc.Row(render_os_hw_info(sysinfo), style={"margin-bottom": "40px"}),
         dbc.Row(render_cpu_info(cpuinfo)),
         dcc.Interval(
            id='cpu-interval',
            disabled=False,
            interval=1 * 500,
            n_intervals=0 # milliseconds
         )
      ]
   )

def render_os_hw_info(sysinfo):
    return html.Div(
        [
            dbc.Row(dbc.Col(html.H5("Informações do Sistema"))),
            dbc.Row([
               dbc.Col(html.P("System:", style={"font-weight": "bold"})), dbc.Col(html.P(sysinfo["System"])),
               dbc.Col(html.P("Node Name:", style={"font-weight": "bold"})), dbc.Col(html.P(sysinfo["Node Name"])),
               dbc.Col(html.P("Release:", style={"font-weight": "bold"})), dbc.Col(html.P(sysinfo["Release"])),
               dbc.Col(html.P("")), dbc.Col(html.P(""))

            ]),

            dbc.Row([
               dbc.Col(html.P("Version:", style={"font-weight": "bold"})), dbc.Col(html.P(sysinfo["Version"])),
               dbc.Col(html.P("")), 
               dbc.Col(html.P("Architecture:", style={"font-weight": "bold"})), dbc.Col(html.P(sysinfo["Machine"])),
               dbc.Col(html.P("")),dbc.Col(html.P("")), dbc.Col(html.P(""))

            ]),
            dbc.Row([
               
            ]),
            dbc.Row([
            ])
  
        ],
        className="os_hw_info"
    )    

def render_cpu_info(cpuinfo):
   core_counts = cpuinfo["cpu_core_counts"]
   usage = cpuinfo["cpu_core_usage"]
   freq = cpuinfo["cpu_freq_info"]
   gpu = cpuinfo["gpu_info"]
   print(cpuinfo)
   return html.Div(
      [
         dbc.Row(dbc.Col(html.H5("Informações do Processador"))),
         render_core_counts(core_counts),
         dbc.Row(render_freq(freq), id="cpu-freq")
      ]
   ),html.Div(render_usage(usage),style={"margin-bottom": "40px"}, id="cpu-usage"),html.Div(render_gpu(gpu), id="gpu")

def render_core_counts(core_counts):
   return dbc.Row([
      dbc.Col(html.P("Núcleos físicos:", style={"font-weight": "bold"})),
      dbc.Col(html.P(core_counts["cores_fisicos"])),
      dbc.Col(html.P("")), 
      dbc.Col(html.P("Núcleos lógicos:", style={"font-weight": "bold"})),
      dbc.Col(html.P(core_counts["total_cores"])),
      dbc.Col(html.P("")) 
   ])

def render_freq(freq):
   return (
      [
         dbc.Col(html.P("Frequência mínima:",style={"font-weight": "bold"})),
         dbc.Col(html.P(str(freq["freq_min"]) + "MHz")),
         dbc.Col(html.P("")), 
         dbc.Col(html.P("Frequência máxima:",style={"font-weight": "bold"})),
         dbc.Col(html.P(str(freq["freq_max"]) + "MHz")),
         dbc.Col(html.P("")),
         dbc.Col(html.P("Frequência atual:",style={"font-weight": "bold"})),
         dbc.Col(html.P(str(round(freq["current_freq"])) + "MHz")),
         dbc.Col(html.P(""))
      ]
   )

def render_usage(usage):
   rows = []
   labels = usage["labels"]
   pcpu = usage["percentages"]
   rows.append(dbc.Row(dbc.Col(html.P("Uso da CPU",style={"font-weight": "bold"}))))
   for i in range(len(usage["labels"])):
      rows.append(
         dbc.Row(
            [
               dbc.Col(html.P(f"Núcleo {i}:",style={"font-weight": "bold"})),
               dbc.Col(html.P(str(pcpu[i]) + "%")),

            ]
         )
      )
   graph = dbc.Row(render_cpu_graph(labels=labels, pcpu=pcpu))
   return (
      dbc.Row(
         [
            dbc.Col(rows, width=2),
            dbc.Col(graph, width=10)
         ]
      )
   )

def render_cpu_graph(labels, pcpu):
   fig = px.bar(x=labels, y=pcpu, range_y=[0,100])
   return dcc.Graph(figure=fig)

def render_gpu(gpus): 
   columns = []

   for gpu in gpus:
      columns.append(dbc.Col(
         [
            dbc.Row(
               [
                  dbc.Col(html.P("GPU ID:"), width=2), dbc.Col(gpu["GPU ID"], width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU name:"), width=2), dbc.Col(gpu["GPU name"], width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU Load:"), width=2), dbc.Col(str(gpu["GPU Load"]) + "%", width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU Free Memory:"), width=2), dbc.Col(str(gpu["GPU Free Memory"]) + "MB", width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU Used Memory:"), width=2), dbc.Col(str(gpu["GPU Used Memory"]) + "%", width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU Total Memory:"), width=2), dbc.Col(str(gpu["GPU Total Memory"]) + "MB", width=2)
               ]
            ),
            dbc.Row(
               [
                  dbc.Col(html.P("GPU Temperature:"), width=2), dbc.Col(str(gpu["GPU Temperature"]) + "°", width=2)
               ]
            )
         ]
      ))
   return (
      [dbc.Row(html.H5("Informações de GPU")),dbc.Row(columns)]
   )