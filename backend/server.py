#!/usr/bin/env python3
import os
import sys
import platform

import falcon
import mss
from mss.tools import to_png

import pyautogui

try:
    import waitress
    class Application:
        def __init__(self, app):
            self.app = app
        def load(self):
            return self.app
except ImportError:
    from gunicorn.app.wsgiapp import WSGIApplication

from pynput.mouse import Button, Controller

mouse = Controller()



def click(x, y):
    saved_position = mouse.position
    mouse.position = (x, y)
    print(f"clicking {x},{y}")
    mouse.click(Button.left)
    mouse.position = saved_position


class ScreenshotApi:
    def on_get(self, req, resp):
        with mss.mss() as sct:
            # monitor = {"top": 0, "left": 0, "width": sct.width, "height": sct.height}
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

            sct_img = sct.grab(monitor)
            image_bytes = to_png(sct_img.rgb, sct_img.size)

        resp.content_type = "image/png"
        resp.body = image_bytes

class ImageClickerApi:
    def on_get(self, req, resp, x, y):
        x = int(x)
        y = int(y)
        click(x, y)

api = falcon.App()
api.add_route("/screenshot", ScreenshotApi())
api.add_route("/click/{x}/{y}", ImageClickerApi())
api.add_static_route('/', os.path.abspath('../frontend/build'))

# if platform.system() == "Windows":
#     waitress.serve(api, host="0.0.0.0", port=8000)
# else:
#     print(sys.argv)
#     sys.argv += [
#         '-b', '127.0.0.1:8080',
#         'server:api',
#     ]
#     WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
