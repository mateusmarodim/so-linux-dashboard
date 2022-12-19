from threading import Thread
import psutil 
from time import sleep


class DiskMonitor(Thread):

    def __init__(self):
        super().__init__()
        self.partitions = psutil.disk_partitions()
        self.is_running = False
    
    def run(self):
        while(True):
            self.partitions = psutil.disk_partitions()
            sleep(0.5)

    
    def get_size(self,bytes, suffix="B"):

        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    
    def disk_info(self):
        partitions_device = []
        partitions_mountpoint = []
        partitions_fstype = []
        partitions_total = []
        partitions_used = []
        partitions_free =[]
        partitions_percent =[]
        for i in range (len(self.partitions)):
            partitions_device.insert(i, self.partitions[i].device)
            partitions_mountpoint.insert(i, self.partitions[i].mountpoint)
            partitions_fstype.insert(i, self.partitions[i].fstype)
            try: 
                partition_usage = psutil.disk_usage(self.partitions[i].mountpoint)
            except PermissionError:
                continue
            partitions_total.insert(i, self.get_size(partition_usage.total))
            partitions_used.insert(i, self.get_size(partition_usage.used))
            partitions_free.insert(i, self.get_size(partition_usage.free))
            partitions_percent.insert(i, partition_usage.percent)
        
        return{ "device":partitions_device,
                "mountpoint": partitions_mountpoint,
                "fstype": partitions_fstype,
                "total": partitions_total,
                "used": partitions_used,
                "free": partitions_free,
                "percent": partitions_percent
        }

    def get_is_running(self):
            return self.is_running
        
    def start_monitor(self):
        self.is_running = True
        self.start()

    
