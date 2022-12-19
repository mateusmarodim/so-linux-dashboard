from threading import Thread
from time import sleep
import psutil 
import GPUtil


class CPUMonitor(Thread):

    def __init__(self):
        super().__init__()
        self.cpu_freq = self.cpu_freq_update()
        self.cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        self.is_running = False
        self.gpus = GPUtil.getGPUs()
    
    def run(self):
        self.is_running = True
        while (True):
            self.cpu_freq = self.cpu_freq_update()
            self.cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
            self.update_gpu_information()
            sleep(0.5)

    
    def cpu_freq_info(self):
        return {
            "freq_min": self.cpu_freq.min,
            "freq_max": self.cpu_freq.max,
            "current_freq": self.cpu_freq.current  
    }

    def cores_info(self):
        return {
            "cores_fisicos": psutil.cpu_count(logical = False),
            "total_cores": psutil.cpu_count(logical= True),
        }

    def percent_cpu(self):
        cpu_units = []
        for i in range(psutil.cpu_count(logical=True)):
            cpu_units.insert(i, f"nucleo_{i}")
            
        return {"labels": cpu_units, "percentages": self.cpu_percent}

    def get_is_running(self):
        return self.is_running
    
    def start_monitor(self):
        self.is_running = True
        self.start()

    def gpu_information(self):
        gpus = []
        for gpu in self.gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = gpu.load 
            gpu_free_memory = gpu.memoryFree
            gpu_used_memory = gpu.memoryUsed
            gpu_total_memory = gpu.memoryTotal
            gpu_temperature = gpu.temperature
            gpus.append({
                "GPU ID": gpu_id,
                "GPU name": gpu_name,
                "GPU Load": gpu_load,
                "GPU Free Memory": gpu_free_memory,
                "GPU Used Memory": gpu_used_memory,
                "GPU Total Memory": gpu_total_memory,
                "GPU Temperature": gpu_temperature
            })
        return gpus

    def update_gpu_information(self):
        self.gpus = GPUtil.getGPUs()

    def cpu_freq_update(self):
        return psutil.cpu_freq()

    def cpu_info(self):
        return {
            "cpu_core_counts": self.cores_info(),
            "cpu_core_usage": self.percent_cpu(),
            "cpu_freq_info": self.cpu_freq_info(),
            "gpu_info": self.gpu_information()
        }