import logging
import os
import sys

from flask import Flask


class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class HealthMonitor:
    def __init__(self, flask_app):
        self.flask_app = flask_app
        self.register_routes()

    def register_routes(self):
        @self.flask_app.route('/')
        def home():
            return "Hello, Flask!"


def start_monitor():
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    HealthMonitor(app)
    with SuppressOutput():
        app.run(host='0.0.0.0', port=1015)
