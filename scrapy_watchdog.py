# -*- coding:utf-8 -*-
# @Author: Wei Yi

import time
from watchdog.observers import Observer
from threading import Thread
from watchdog.events import FileSystemEventHandler
import os
import win32api

class Moniter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.st = time.time()
        self.is_finish = False

    def run(self):
        while not self.is_finish:
            #time.sleep(5)
            self.cur = time.time()
            if self.cur - self.st >= 120:
                #print("Long time no change!")
                os.system("taskkill /F /IM scrapy.exe")
                self.st = time.time()
                win32api.ShellExecute(0, 'open', 'start_scrapy.bat', '', '', 1)



moniter = Moniter()


def update_time():
    global moniter
    moniter.st = time.time()


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            #print("Created")
            update_time()


        elif event.event_type == 'modified':
            pass
            # Taken any action here when a file is modified.
            #print("Change")


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    path = "sbook1"
    observer.schedule(event_handler, path=path, recursive=True)
    moniter.start()
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        moniter.stop()
    observer.join()
    moniter.join()
