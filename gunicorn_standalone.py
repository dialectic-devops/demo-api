from gunicorn.app.base import BaseApplication
from app import app  # Updated import to match Flask app instance

import multiprocessing

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:8050",
        "workers": number_of_workers(),
    }
    StandaloneApplication(app, options).run()

