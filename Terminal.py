import subprocess
from threading import Thread
from time import sleep

class Terminal(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.bash_command = ""
        self.terminal_lines = []
        self.result = ""
        self.is_running = False
        
    def run(self):
        while(True):
            sleep(5)
    def execute_command(self, command):
        self.command = command
        command_process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        exit = (command_process.communicate()[0])
        self.terminal_lines.append(exit)
        return exit.decode('ASCII')
        
    def get_is_running(self):
        return self.is_running

    def start_terminal(self):
        self.is_running = True
        self.start()
        
    def get_process_list(self):
        return self.execute_command("ps -eo pid,user,args,pcpu,%mem,s,comm,cputime,ni,nlwp --sort user")
        
