from threading import Thread
import os

class FileMonitor:

    def __init__(self):
        self.root_path = "/"

    def list_root_files(self):
        startpath = self.root_path
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
