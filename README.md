# README

Python wrapper of airspyhf library

https://github.com/airspy/airspyhf.git

Project webpage main.lv
main project page http://main.lv
cgit source viewer http://git.main.lv/cgit.cgi/pyairspyhf.git


# Source code

```
git clone https://git.main.lv/cgit/pyairspyhf.git
```

# Install airspyhf

Install all dependencies such as:
```
    cmake, libusb
```

Checked supported and tested version list

To build the libairspyhf follow: https://github.com/airspy/airspyhf

Workes localy
```
git clone https://github.com/airspy/airspyhf.git
cd airspyhf
cmake .
make
sudo make install
```

If there is issues with libusb header try to find libusb header locations
```
cmake  -DLIBUSB_INCLUDE_DIR=/usr/include/libusb-1.0/ -DINSTALL_UDEV_RULES=ON
```

```commandline
udevadm control --reload-rules
```

# API
## libairspyhf

## AirSpyHF

# Examples

## airspyhf_rx.py

## Supported and tested

| Python | libairspyhf | OS | Status |
| --- |--- | --- | --- | 
| 3.9, 3.10 | 1.7.1 | ArchLinux, Ubuntu 20.04 | Supported and tested |


## Install

## Links

https://docs.python.org/3/library/ctypes.html