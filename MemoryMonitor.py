from threading import Thread
import psutil 
from time import sleep

class MemoryMonitor(Thread):

    def __init__(self):
        super().__init__()
        self.memory = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
        self.is_running = False

    
    def run(self):
        print('oie')
        while(True):
            self.memory = psutil.virtual_memory()
            self.swap = psutil.swap_memory()
            sleep(0.5)

    def get_size(bytes, suffix="B"):

        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    

    def memory_info(self):
        return{
            "memory_total": self.memory.total,
            "memory_available": self.memory.available,
            "memory_used": self.memory.used,
            "memory_percent": self.memory.percent,
            "swap_total": self.swap.total,
            "swap_free": self.swap.free,
            "swap_used": self.swap.used,
            "swap_percent": self.swap.percent,
        }
        
    def get_is_running(self):
            return self.is_running
        
    def start_monitor(self):
        self.is_running = True
        self.start()