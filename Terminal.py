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
        self.process_list = {"ps":self.execute_command("ps ax -o user,pid,pcpu,pmem,tty,stat,start,time --sort pcpu"), "comm":self.execute_command("ps ax -o comm --sort user")}
        
    def run(self):
        while(True):
            self.update_process_list()
            sleep(0.5)
            
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
        
    def update_process_list(self):
        self.process_list = {"ps":self.execute_command("ps ax -o user,pid,pcpu,pmem,tty,stat,start,time --sort -pcpu"), "comm":self.execute_command("ps ax -o comm --sort user")}

    def get_process_list(self):
        return self.process_list

    def open_terminal(self):
        self.execute_command("gnome-terminal")
        
