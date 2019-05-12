tornado-image-streamer
======================

An image streamer over the Internet. A tornado backend is used to configure
a JPEG image streamer using either server "push" mode, or client "get" mode.
All communication is streamed using HTML5 websockets for maximum throughput. 

Technolgies used
----------------

Client side:

* jquery
* websockets
* HTML5

Server side:

* Python3 (Python2 is not supported)
* Tornado (WebSocketHandler)
* PIL
* numpy
* opencv


Basic Installation
------------------

Activate a Python virtual environment and execute the following command,
    
```bash
pip install tornado-image-streamer
```

Test the application,

```bash
tornado_image_streamer --simulate
```


Linux Developer Installation
----------------------------

Install a virtual environment,

```bash
mkdir ~/venv
cd ~/venv
python3 -m virtualenv --python=/usr/bin/python3 tis_env
source tis_env/bin/activate
```

Activate the virtual environment,

```bash
source ~/venv/tis_env/bin/activate
```

Install this package,

```bash
pip install -U -e git+https://gitlab.com/hsmit/tornado-image-streamer.git#egg=tornado_image_streamer
```

Test the application,

```bash
python test2/src/tornado-image-streamer/tornado_image_streamer/run.py -s
```

 
 User installation
 -----------------
 
 In your current python3 environment execute the following,

```bash
pip install -U git+https://gitlab.com/hsmit/tornado-image-streamer.git#egg=tornado_image_streamer
```

Test the application,

```bash
tornado_image_streamer --help
```


Usage
-----

```bash
$ tornado_image_streamer --help
Usage: tornado_image_streamer [OPTIONS]

  Tornado web server that streams webcam images over the network.

Options:
  -p, --port INTEGER     IP port used for the web server (default: 8888)
  -s, --simulate         Enable simulated camera.
  -m, --mode [get|push]  The mode of operation (default: push).
  --help                 Show this message and exit.
```