# tornado-image-streamer

## Linux Developer Installation

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

 
 ## User Installation
 
 In your current python3 environment execute the following,

```bash
pip install -U git+https://gitlab.com/hsmit/tornado-image-streamer.git#egg=tornado_image_streamer
```

Test the application,

```bash
tornado_image_streamer --help
```
