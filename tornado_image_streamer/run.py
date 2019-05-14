"""TBW."""
from pathlib import Path
import threading
import click

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado_image_streamer import camera_utils
from tornado_image_streamer import image_stream_handler


def stop_application(app):
    """TBW."""
    print('Stopping...')
    app.settings['streamer_class'].stop = True
    tornado.ioloop.IOLoop.instance().stop()
    while len(app.settings['sockets']):
        print('Closing socket...')
        app.settings['sockets'].pop().close()

    for th in threading.enumerate():
        if th is not threading.main_thread() \
                and not th.name.startswith('pydevd'):
            print('Waiting for thread: %s' % th.name)
            th.join(timeout=5.0)
            if th.is_alive():
                print('Failed to join thread: %s' % th.name)
    print('Exiting main')


@click.command()
@click.option('-p', '--port', default=0,
              help='IP port used for the web server (default: 0)')
@click.option('-s', '--simulate', is_flag=True,
              help='Enable simulated camera.')
@click.option('-m', '--mode',  default='push',
              type=click.Choice(['get', 'push']),
              help='The mode of operation (default: push).')
def main(port=8888, simulate=False, mode='push'):
    """Tornado web server that streams webcam images over the network."""
    pkg_dir = Path(__file__).absolute().parent

    if simulate:
        cam = camera_utils.SimCam()
    else:
        cam = camera_utils.WebCam()

    if mode == 'push':
        streamer_class = image_stream_handler.ImagePushStreamHandler
    else:
        streamer_class = image_stream_handler.ImageStreamHandler

    app = tornado.web.Application(
        handlers=[
            (r"/imagestream", streamer_class),
            (r"/(.*)", image_stream_handler.IndexPageHandler, {
                "path": pkg_dir.joinpath('templates'),
                "default_filename": "index.html",
            }),
        ],
        template_path=pkg_dir.joinpath('templates'),
        static_path=pkg_dir.joinpath('static'),
        debug=True,
        camera=cam,
        sockets=[],
        stream_mode=mode,
        streamer_class=streamer_class,
    )

    app.settings['streamer_class'].start(application=app)
    server = app.listen(port)
    if port == 0:
        port = list(server._sockets.values())[0].getsockname()[1]

    print('http://localhost:%s' % port)
    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        stop_application(app)


if __name__ == "__main__":
    main()
