"""TBW."""
# import typing as t
import os
import threading
import time
import asyncio
import logging

import tornado.ioloop
import tornado.web
import tornado.websocket

from camera_utils import WebCam


logger = logging.getLogger(__name__)
html_page_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/www/'


class IndexPageHandler(tornado.web.RequestHandler):
    """The index.html HTML generation handler."""

    def __init__(self, application, request, **kwargs):
        """TBW."""
        self._path = kwargs.pop("path")
        self.default_filename = kwargs.pop("default_filename", "index.html")
        self.index_page = os.path.join(self._path, self.default_filename)
        super(IndexPageHandler, self).__init__(application, request, **kwargs)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        # Check if page exists
        index_page = os.path.join(html_page_path, self.default_filename)
        if os.path.exists(index_page):
            # Render it
            print(self.index_page)
            self.render(self.index_page, app=self.application)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=self.index_page)
            # Send response
            self.finish(err_html)


class ImageStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""
    cam = WebCam()

    def __init__(self, *args, **kwargs):
        """TBW."""
        self.counter = 0
        self.cam.open()
        super().__init__(*args, **kwargs)

    def on_connection_close(self):
        """TBW."""
        self.close()
        self.cam.release()

    @staticmethod
    def start(application):
        """ST."""
        pass  # unused, for API compatibility with ImagePushStreamHandler

    @staticmethod
    def stop():
        """TBW."""
        pass  # unused, for API compatibility with ImagePushStreamHandler

    async def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                image = self.cam.read_image()
                await self.write_message(image, binary=True)
            else:
                await self.write_message(message)  # echo
        except Exception as exc:
            logger.exception(exc)


class ImagePushStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    interval = 40
    stop_event = threading.Event()
    cam = WebCam()

    def __init__(self, *args, **kwargs):
        """TBW."""
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.images = []
        self._periodic = tornado.ioloop.PeriodicCallback(self._write_queue, 40)
        self.cam.open()
        self._periodic.start()
        self.application.settings['sockets'].append(self)

    def on_connection_close(self):
        """TBW."""
        logger.info('Closing web socket...')        
        self._periodic.stop()
        self.close()    
        try:
            self.application.settings['sockets'].remove(self)
        except ValueError:
            pass
        finally:
            self.cam.release()    

    @staticmethod
    def start(application):
        """TBW."""
        th = threading.Thread(target=ImagePushStreamHandler.read_image_loop,
                              args=(application,),
                              name='read-camera')
        th.start()

    @staticmethod
    def stop():
        """TBW."""
        ImagePushStreamHandler.stop_event.set()

    @staticmethod
    def read_image_loop(application):
        """TBW."""
        cam = ImagePushStreamHandler.cam
        while not ImagePushStreamHandler.stop_event.is_set():
            interval = float(ImagePushStreamHandler.interval) / 1000.0
            if len(application.settings['sockets']):
                if cam.isOpened():
                    image = cam.read_image()
                    for ws in application.settings['sockets']:
                        ws.images.append(image)
            time.sleep(interval)    
        logger.info('Exiting ImagePushStreamHandler.read_image_loop')

    async def _write_queue(self):
        """TBW."""
        interval = float(ImagePushStreamHandler.interval) / 1000.0
        for _ in range(50):
            if self.images:
                break
            await asyncio.sleep(interval)

        while self.images:
            image = self.images.pop()
            self.images.clear()
            try:
                await self.write_message(image, binary=True)
            except tornado.websocket.WebSocketClosedError:
                self.close()
                socks = self.application.settings['sockets']
                if self in socks:
                    socks.remove(self)

    async def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                await self._write_queue()
            elif message.startswith('interval'):
                interval = int(message.split('=')[-1])
                self._periodic = interval
                ImagePushStreamHandler.interval = interval
                # self.write_message(message)  # echo
        except Exception as exc:
            logger.exception(exc)
