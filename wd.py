import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import archiver


class Handler(FileSystemEventHandler):
    def __init__(self, arch, flag_logging=False):
        self.flag_logging = flag_logging
        self.arch = arch

    def on_any_event(self, event):
        if self.flag_logging:
            f = open("./logger.log", "a")
            f.write(str(event) + '\n')
            f.close()
        else:
            return self.arch.checker_size()



