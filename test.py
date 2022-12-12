from DiskMonitor import DiskMonitor
from Terminal import Terminal

diskMonitor = DiskMonitor()
terminal = Terminal()

# print(diskMonitor.disk_info())
processo = terminal.get_process_list().split('\n')


for i in range(len(processo)):
    proc_col = str(processo[i]).split(' ')
    cont = proc_col.count(' ')
    try:
        while True:
            proc_col.remove('')
    except ValueError:
        pass
    print(proc_col)
    # for j in range(len(proc_col)):
    #     print(proc_col[j])