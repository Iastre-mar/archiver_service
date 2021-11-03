import os
import time
import glob
import shutil
from pathlib import Path
from datetime import datetime, date, timedelta
import du


class Archiver():
    def __init__(self,
                 days=90,
                 storage_folder='./storage/',
                 archive_folder='./archive/',
                 max_size_storage='65,0M',
                 logfile='./logfile.log'):
        self.days = days
        self.storage_folder = storage_folder
        self.archive_folder = archive_folder
        self.logfile = logfile
        self.max_size_storage = max_size_storage
        self.scale = self.max_size_storage[-1]
        self.max_size = self.max_size_storage
        self.max_true_size = int(float(self.max_size[:-1].replace(',', '.')) * 1024 ** self.size_function(self.scale))

    def size_function(self, scale):
        return 1 if scale == 'K' else 2 if scale == 'M' else 3 if scale == 'G' else 4

    def checker_size(self):
        """Проверяет размер директории"""
        size = du.du(self.storage_folder)  # Меньше 4 кб не покажет, меня это устраивает
        scale = size[-1]
        # Вычисляю размер в байтах
        true_size = int(float(size[:-1].replace(',', '.')) * 1024 ** self.size_function(scale))
        if self.max_true_size - true_size <= 0.1 * self.max_true_size:
            self.checker_date()

    def checker_date(self):
        """Проверяет дату созданных файлов в случае переполнения памяти"""
        move_date = date.today() - timedelta(days=90)
        move_date = move_date.strftime('%Y/%m/%d/')
        old_path = './storage/' + move_date
        lst_dirs = glob.glob('./storage/*/*/*/', recursive=True)
        print(lst_dirs[0])
        print(old_path)
        lst_old_dirs = [x for x in lst_dirs if x < old_path]
        if lst_old_dirs:
            self.carrier(lst_old_dirs)

    def carrier(self, path):
        """Архивирует файлы, переносит их, удаляет"""
        for dir in path:
            archive_p = (dir[10:])
            archive_name = archive_p[:-1].replace('/', '-')
            shutil.make_archive(
                './' + archive_name,
                'zip',
                root_dir='./storage',
                base_dir=archive_p)
            archive_dir = os.path.join('./archive/' + archive_p)
            os.makedirs(os.path.dirname(archive_dir), exist_ok=True)
            shutil.move('./' + archive_name + '.zip', archive_dir)
            shutil.unpack_archive(self.archive_folder + archive_p + archive_name + '.zip',
                                  extract_dir=self.archive_folder,
                                  format='zip')
            shutil.rmtree(os.path.abspath(dir))
            os.remove(self.archive_folder + archive_p + archive_name + '.zip')



