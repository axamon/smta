import time
import smta
import redis
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
rlocal = redis.StrictRedis()

class MyHandler(FileSystemEventHandler):
    
    def process(self, event):
        #print event.src_path  # print now only for degug
	time.sleep(6)
        rlocal.lpush('listapcap',event.src_path)

    def on_created(self, event):
	self.process(event)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
