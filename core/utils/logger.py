import os
import time
import logging
import pytz
from datetime import datetime
import requests
from logging.handlers import TimedRotatingFileHandler


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


class DiscordHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        current_time = datetime.now(pytz.timezone(
            'Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')

        embed = {
            "embeds": [
                {
                    "title": "{} | {}".format(current_time, record.levelname),
                    "description": record.message,
                    "color": self.get_color(record.levelname)
                }
            ]
        }

        try:
            requests.post(self.webhook_url, json=embed)
        except requests.RequestException as e:
            print(f"Error during post to discord : {e}")

    def get_color(self, levelname):
        if levelname == 'DEBUG':
            return 0x0000ff
        elif levelname == 'INFO':
            return 0x00ff00
        elif levelname == 'WARNING':
            return 0xffa500
        elif levelname == 'ERROR':
            return 0xff0000
        else:
            return 0x000000


class Log(metaclass=SingletonMeta):
    def __init__(self, *, url=None):
        self.log_dir = os.path.join(".", "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = self.setup_logger(url=url)
        self.logger.day = 7

    def setup_logger(self, *, url):
        logger = logging.getLogger("MyLogger")
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

        return logger

    def setup_discord(self, *, url=None, level="DEBUG"):
        discord_handler = DiscordHandler(url)
        discord_handler.setLevel(level)
        tz_utc_8 = pytz.timezone('Asia/Taipei')
        formatter = CustomFormatter(
            '[%(asctime)s][%(levelname)s]: %(message)s', '%H:%M:%S', tz_utc_8
        )
        discord_handler.setFormatter(formatter)
        self.logger.addHandler(discord_handler)

    def clean_old_logs(self):
        now = time.time()
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.stat(file_path).st_mtime < now - self.logger.day * 86400:
                print(f"Deleting old log file: {filename}")
                os.remove(file_path)
