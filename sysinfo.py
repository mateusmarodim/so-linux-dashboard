import subprocess
import platform
import psutil
import os

def get_cpu_usage(percpu: bool):
    cpu_percent = psutil.cpu_percent(interval=None, percpu=percpu)
    if percpu:
        cpu_units = []
        for i in range(psutil.cpu_count(logical=True)):
            cpu_units.insert(i, f"cpu_{i}")
        return {"units": cpu_units, "usage": cpu_percent}
    else:
        return cpu_percent

