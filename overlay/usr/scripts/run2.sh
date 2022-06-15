opkg update
opkg install libgpiod
opkg install usbutils
opkg install fswebcam
opkg install python3
opkg install python3-tornado
opkg install python3-click
opkg install python3-numpy
opkg install python3-pillow
opkg install python3-openssl
opkg install python3-asyncio
opkg install python3-gpiod
opkg install python3-readline
opkg install python3-urllib
opkg install kmod-usb-core
opkg install kmod-usb2 kmod-video-core
# Sterownik potrzebny przez wykorzystywaną kamerę. 
# W przypadku innej kamery sprawdź jaki sterownik jest potrzebny
opkg install kmod-video-gspca-ov519

# pobierz nakładkę za pomocą polecenia wget
