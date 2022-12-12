import platform

class SystemInfoMonitor():

    def __init__(self) -> None:
        super().__init__()
        self.uname = platform.uname()
        self.is_running = False

    def system_information(self):
        return{
            "System": self.uname.system,
            "Node Name": self.uname.node,
            "Release": self.uname.release,
            "Version": self.uname.version,
            "Machine": self.uname.machine,
            "Processor": self.uname.processor,
        }

