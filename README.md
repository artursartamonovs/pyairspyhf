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

Works with airspyhf master branch install. Master airspyhf version is 1.7.1,
most distribution have tagged version of 1.6.8 beware when building master branch.
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

Imported functions from libairspyhf library

| Function declaration | Version |
| --- | --- | 
| airspyhf_lib_version | |
| airspyhf_list_devices | |
| airspyhf_open | |
| airspyhf_open_sn | |
| airspyhf_open_fd | >= 1.7.1 |
| airspyhf_close | |
| airspyhf_get_output_size | |
| airspyhf_start | |
| airspyhf_stop | |
| airspyhf_is_streaming | |
| airspyhf_is_low_if | |
| airspyhf_set_freq | | 
| airspyhf_set_freq_double | >= 1.7.1 |
| airspyhf_set_lib_dsp | |
| airspyhf_get_samplerates | |
| airspyhf_set_samplerate | |
| airspyhf_get_calibration | |
| airspyhf_set_calibration | |
| airspyhf_get_vctcxo_calibration | >= 1.7.1 |
| airspyhf_set_vctcxo_calibration | >= 1.7.1 |
| airspyhf_set_optimal_iq_correction_point | |
| airspyhf_iq_balancer_configure | |
| airspyhf_flash_calibration | |
| airspyhf_version_string_read | |
| airspyhf_set_hf_agc | |
| airspyhf_set_hf_agc_threshold | |
| airspyhf_set_hf_att | |
| airspyhf_set_hf_lna | |

## AirSpyHF

# Examples

## airspyhf_rx.py

## Supported and tested

| Python | libairspyhf | OS | Status |
| --- |--- | --- | --- | 
| 3.9, 3.10 | 1.7.1 | ArchLinux, Ubuntu 20.04 | Supported and tested |
| 3.9, 3.10 | 1.6.8 | MacOS | Supported and tested |

## Install



## Links

https://docs.python.org/3/library/ctypes.html