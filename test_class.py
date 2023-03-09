from airspyhf import *
from ctypes import *
import time
import sys
import wave
import struct
import argparse

airspy = AirSpyHF()

airspy.open(device_index=0)

airspy.close()