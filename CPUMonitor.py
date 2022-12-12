from threading import Thread
import psutil 
import GPUtil


class CPUMonitor(Thread):

    def __init__(self):
        super().__init__()
        self.cpu_freq = psutil.cpu_freq()
        self.cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
        self.is_running = False
        self.gpus = GPUtil.getGPUs()
    
    def run(self):
        while (True):
            self.cpu_freq_update()
    
    def cpu_freq_info(self):
        print("Freq info \n")
        return {
            "freq_min": self.cpu_freq.min,
            "freq_max": self.cpu_freq.max,
            "current_freq": self.cpu_freq.current  
    }

    def cores_info(self):
        return {
            "core fisico":psutil.cpu_count(logical = False),
            "total core": psutil.cpu_count(logical= True),
        }

    def percent_cpu(self):
        cpu_units = []
        for i in range(psutil.cpu_count(logical=True)):
            cpu_units.insert(i, f"cpu_{i}")
            
        
        print(self.cpu_percent)
        print(cpu_units)
        
        return {"labels": cpu_units, "percentages": self.cpu_percent}

    def get_is_running(self):
        return self.is_running
    
    def start_monitor(self):
        self.is_running = True
        self.start()

    def gpu_information(self):
        for gpu in self.gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = gpu.load 
            gpu_free_memory = gpu.memoryFree
            gpu_used_memory = gpu.memoryUsed
            gpu_total_memory = gpu.memoryTotal
            gpu_temperature = gpu.temperature
            return{
                "GPU ID": gpu_id,
                "GPU name": gpu_name,
                "GPU Load": gpu_load,
                "GPU Free Memory": gpu_free_memory,
                "GPU Used Memory": gpu_used_memory,
                "GPU Total Memory": gpu_total_memory,
                "GPU Temperature": gpu_temperature
            }

