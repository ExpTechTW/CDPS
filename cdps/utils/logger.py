import logging
import os
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import pytz


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, dir_name, when, interval, backupCount):
        self.dir_name = dir_name
        self.when = when
        self.interval = interval
        self.backupCount = backupCount
        filename = self.get_filename()
        super().__init__(filename, when, interval, backupCount)

    def get_filename(self):
        return os.path.join(self.dir_name, time.strftime("%Y-%m-%d") + ".log")

    def doRollover(self):
        """
        doRollover is called whenever the logging time interval has been reached.
        """
        self.stream.close()
        self.baseFilename = self.get_filename()
        self.mode = 'a'
        self.stream = self._open()


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt, tz):
        super().__init__(fmt, datefmt)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        return dt.strftime(datefmt)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def reset_instance(cls, instance_cls):
        if instance_cls in cls._instances:
            del cls._instances[instance_cls]
        cls._instances[instance_cls] = instance_cls()


class Log(metaclass=SingletonMeta):
    def __init__(self, *, url=None):
        self.log_dir = os.path.join(".", "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.config_dir = os.path.join(".", "config")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.plugins_dir = os.path.join(".", "plugins")
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
        self.setup_logger(url=url)
        self.logger.day = 7

    def setup_logger(self, *, url):
        logger = logging.getLogger("MyLogger")
        logger.handlers.clear()
        logger.setLevel("DEBUG")

        handler = CustomTimedRotatingFileHandler(
            self.log_dir,
            when="midnight",
            interval=1,
            backupCount=5
        )
        tz_utc_8 = pytz.timezone('Asia/Taipei')
        formatter = CustomFormatter(
            '[%(asctime)s][%(levelname)s]: %(message)s', '%H:%M:%S', tz_utc_8
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger

    def clean_old_logs(self):
        now = time.time()
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.stat(file_path).st_mtime < now - self.logger.day * 86400:
                print(f"Deleting old log file: {filename}")
                os.remove(file_path)

    @staticmethod
    def reset_instance():
        SingletonMeta.reset_instance(Log)
