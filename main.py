import os
import time
import archiver
import wd


storage_dir = os.path.join('./storage/')
os.makedirs(storage_dir, exist_ok=True)
archive_dir = os.path.join('./archive/')
os.makedirs(archive_dir, exist_ok=True)
arch = archiver.Archiver()
observer_storage = wd.Observer()
observer_storage.schedule(wd.Handler(arch), path='./storage', recursive=True)
observer_archiver = wd.Observer()
observer_archiver.schedule(wd.Handler(arch, flag_logging=True), path='./storage', recursive=True)
observer_storage.start()
observer_archiver.start()
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer_storage.stop()
    observer_archiver.stop()

observer_storage.join()
observer_archiver.join()
