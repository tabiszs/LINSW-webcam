#!/usr/bin/python3
"""ST."""
import os
from pathlib import Path
import click

import tornado.ioloop
import tornado.web
import tornado.websocket

import camera_utils
import image_stream_handler
import download_handler
import tornado_utils
__version__ = "0.6"

@click.command()
@click.option('-p', '--port', default=0, help='IP port used for the web server (default: 0)')
@click.option('-a', '--address', default='0.0.0.0', help='IP address used for the web server (default: 0.0.0.0)')
@click.option('-v', '--verbosity', count=True, help='The verbosity level.')
@click.option('-s', '--simulate', is_flag=True, help='Enable simulated camera.')
@click.option('-m', '--mode',  default='push', type=click.Choice(['get', 'push']), help='The mode of operation (default: push).')
@click.option('-v', '--verbosity', count=True, help='The verbosity level.')
@click.version_option(version=__version__)
def main(port=8888, address='0.0.0.0', simulate=False, mode='push', verbosity=0):
    """Tornado web server that streams webcam images over the network."""
    tornado_utils.config_logging(verbosity)

    pkg_dir = Path(__file__).absolute().parent

    camera_class = [
        camera_utils.WebCam,
        camera_utils.SimCam
    ][simulate]

    streamer_class = {
        'push': image_stream_handler.ImagePushStreamHandler,
        'get': image_stream_handler.ImageStreamHandler,
    }[mode]
    
    app = tornado.web.Application(
        handlers=[
            (r"/imagestream", streamer_class),
            (r"/photo", download_handler.PhotoHandler),
            (r"/download", download_handler.DownloadHandler),
            (r"/", image_stream_handler.IndexPageHandler, {
                "path": pkg_dir.joinpath('www'),
                "default_filename": "index.html",
            }),
            (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': pkg_dir.joinpath('image')}),
            (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': pkg_dir.joinpath('css')}),
            (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': pkg_dir.joinpath('js')})
        ],
        template_path=pkg_dir.joinpath('www'),
        debug=True,
        camera=camera_class(),
        sockets=[],
        timers=[],
        stream_mode=mode,
    )

    streamer_class.start(application=app)
    server = app.listen(port, address)
    tornado_utils.log_url(server)
    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        streamer_class.stop()
        tornado_utils.stop_application(app.settings['sockets'])


if __name__ == "__main__":
    main()
