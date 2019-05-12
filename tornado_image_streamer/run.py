"""TBW."""
from pathlib import Path

import tornado.ioloop
import tornado.web
import tornado.websocket

import click

from tornado_image_streamer import camera_utils
from tornado_image_streamer import image_stream_handler


@click.command()
@click.option('-p', '--port', default=8888,
              help='IP port used for the web server (default: 8888)')
@click.option('-s', '--simulate', is_flag=True,
              help='Enable simulated camera.')
@click.option('-m', '--mode',  default='push', type=click.Choice(['get', 'push']),
              help='The mode of operation.')
def main(port=8888, simulate=False, mode='push'):
    """TBW."""
    pkg_dir = Path(__file__).absolute().parent
    template_dir = pkg_dir.joinpath('templates')
    static_dir  = pkg_dir.joinpath('static')

    if simulate:
        cam = camera_utils.SimCam(),
    else:
        cam = camera_utils.WebCam()

    if mode == 'push':
        streamer_class = image_stream_handler.ImagePushStreamHandler
    else:
        streamer_class = image_stream_handler.ImageStreamHandler

    app = tornado.web.Application(
        handlers=[
            (r"/imagestream", streamer_class),
            (r"/(.*)", tornado.web.StaticFileHandler, {
                "path": str(template_dir),
                "default_filename": "index.html"
            }),
        ],
        static_path=static_dir,
        debug=True,
        camera=cam,
        sockets=[],
    )

    if mode == 'push':
        image_stream_handler.ImagePushStreamHandler.start_read_image_loop(application=app)

    app.listen(port)
    print('http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

