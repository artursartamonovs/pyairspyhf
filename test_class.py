from airspyhf import *
from ctypes import *
import time
import sys
import wave
import struct
import argparse

airspy = AirSpyHF()

if -1 == airspy.open(device_index=0):
    print("Couldnt open device")
    sys.exit(1)
print("1")
airspy.set_samplerate(192000)
print("1")
airspy.set_hf_agc(1)
print("1")
airspy.set_hf_agc_threshold(0)
print("1")
airspy.set_hf_lna(1)
print("1")
sample_count = 0
def read_samples(transfer):
    global sample_count
    global wave_file
    print("Python call back")
    t = transfer.contents
    bytes_to_write = t.sample_count * 4 * 2
    rx_buffer = t.samples
    #print(f"{bytes_to_write} bytes receieved")
    sample_count += t.sample_count
    #for i in range(0,t.sample_count):
        #d_re = t.samples[i].re
        #d_im = t.samples[i].im
        #data = struct.pack("<f",d_re) # FIX ?!
        #wave_file.writeframesraw(data)
        #data = struct.pack("<f", d_im)  # FIX ?!
        #wave_file.writeframesraw(data)
    #print("End call back")
    return 0
print("1")
airspy.start(read_samples)
print("1")
count = 0
while airspy.is_streaming() and count < 3:
    print("Loop")
    count += 1
    time.sleep(1)

airspy.stop()
airspy.close()