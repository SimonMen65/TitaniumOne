import sys
sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import tornado.ioloop
import tornado.web
import json
import logging
from configs.configs import config
from core import API


logging.basicConfig(level=config.tutti_configs["local_logging_web"]["level"],
                    filename=config.tutti_configs["local_logging_web"]["filename"],
                    datefmt=config.tutti_configs["local_logging_web"]["datefmt"],
                    format=config.tutti_configs["local_logging_web"]["format"])
logger = logging.getLogger(__name__)


class FlowHandler(tornado.web.RequestHandler):
    def get(self):
        s = str(self.get_argument("symbol"))
        result = API.flow(s)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))


class LatestHandler(tornado.web.RequestHandler):
    def get(self):
        s = str(self.get_argument("symbol")) or "Tutti"
        result = API.latest(s)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))


class SingleHandler(tornado.web.RequestHandler):
    def get(self):
        s = str(self.get_argument("symbol"))
        t = str(self.get_argument("time"))
        result = API.single(s,t)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))


def make_app():
    return tornado.web.Application([
        (r"/flow", FlowHandler),
        (r"/single", SingleHandler),
        (r"/latest", LatestHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
