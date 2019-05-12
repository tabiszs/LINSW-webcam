"""TBW."""
import threading
from tornado.ioloop import PeriodicCallback

import tornado.ioloop
import tornado.web
import tornado.websocket


class ImageStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    def __init__(self, *args, **kwargs):
        """TBW."""
        self.counter = 0
        super().__init__(*args, **kwargs)

    def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                image = self.application.settings['camera'].read_image()
                self.write_message(image, binary=True)
            else:
                self.write_message(message)  # echo
        except Exception as exc:
            print(exc)


class ImagePushStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    images = []
    interval = 1

    def __init__(self, *args, **kwargs):
        """TBW."""
        self.counter = 0
        super().__init__(*args, **kwargs)
        self.application.settings['sockets'].append(self)
        PeriodicCallback(self._write_queue, 1).start()

    @staticmethod
    def start_read_image_loop(application):
        """TBW."""
        th = threading.Thread(target=ImagePushStreamHandler.read_image_loop,
                              args=(application,),
                              name='read-camera')
        th.start()

    @staticmethod
    def read_image_loop(application):
        """TBW."""
        cam = application.settings['camera']
        while True:
            interval = float(ImagePushStreamHandler.interval) / 1000.0
            if len(application.settings['sockets']):
                ok, raw = cam.read()
                ImagePushStreamHandler.images.append(raw)
            time.sleep(interval)

    def _write_queue(self):
        """TBW."""
        while self.images:
            image = self.images.pop()
            try:
                self.write_message(image, binary=True)
            except tornado.websocket.WebSocketClosedError as exc:
                self.close()
                socks = self.application.settings['sockets']
                if self in socks:
                    socks.remove(self)

    def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                self._write_queue()
            elif message.startswith('interval'):
                interval = int(message.split('=')[-1])
                ImagePushStreamHandler.interval = interval
                # self.write_message(message)  # echo
        except Exception as exc:
            print(exc)
