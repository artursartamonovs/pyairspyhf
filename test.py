#!/usr/bin/python3
import os
from airspyhf import *
from ctypes import *
import time
import sys
import wave
import struct

print("Check airspyHF version")

p = airspyhf_lib_version_t()
print(libairspyhf.airspyhf_lib_version(byref(p)))
print(p.major_version)
print(p.minor_version)
print(p.revision)

print("Get list of devices if there is any")
ndev = libairspyhf.airspyhf_list_devices(None,0)
print("Found %d devices"%(ndev))

for devi in range(0,ndev):
    serial = c_uint64(0)
    libairspyhf.airspyhf_list_devices(byref(serial),devi+1)
    print("Device %d: Serial number %s"%(int(devi),hex(serial.value) ))

print("try to open device")
dev_p = airspyhf_device_t_p(None)
ret = libairspyhf.airspyhf_open_sn(dev_p,0x3b52ab5dada12535)
print("open_sn: Returned %d"%(ret))
if (ret != 0):
    print("airspyhf_open_sn returned != 0, error")
    sys.exit()

print("List sample rates")
nsrates = c_uint32(0)

ret = libairspyhf.airspyhf_get_samplerates(dev_p,byref(nsrates),c_uint32(0))
print("ret %d"%ret)
print("sample rates %d"% nsrates.value)

supportet_samplerates = (c_uint32*4)(0)
ret = libairspyhf.airspyhf_get_samplerates(dev_p,supportet_samplerates,nsrates)
print("ret %d"%ret)
for i in range(0,nsrates.value):
    print("Sample rates %d"% supportet_samplerates[i])

#try to get some samples
ret = libairspyhf.airspyhf_set_samplerate(dev_p, supportet_samplerates[3])
print(f"airspyhf_set_samplerate ret={ret}")

ret = libairspyhf.airspyhf_set_hf_agc(dev_p, 1)
print(f"airspyhf_set_hf_agc ret={ret}")

ret = libairspyhf.airspyhf_set_hf_agc_threshold(dev_p, 0)
print(f"airspyhf_set_hf_agc_threshold ret={ret}")

sample_count = 0
wave_file = wave.open("record.wav","w")
wave_file.setnchannels(2)
wave_file.setsampwidth(4)
wave_file.setframerate(supportet_samplerates[1])
def read_samples(transfer):
    global sample_count
    global wave_file
    #print("Python call back")
    t = transfer.contents
    bytes_to_write = t.sample_count * 4 * 2
    rx_buffer = t.samples
    #print(f"{bytes_to_write} bytes receieved")
    sample_count += t.sample_count
    for i in range(0,t.sample_count):
        d_re = t.samples[i].re
        d_im = t.samples[i].im
        data = struct.pack("<f",d_re) # FIX ?!
        wave_file.writeframesraw(data)
        data = struct.pack("<f", d_im)  # FIX ?!
        wave_file.writeframesraw(data)
    #print("End call back")
    return 0


read_samples_cb = airspyhf_sample_block_cb_fn(read_samples)


ret = libairspyhf.airspyhf_start(dev_p, airspyhf_sample_block_cb_fn(read_samples), None)
print(f"airspyhf_start ret={ret}")

#ret = airspyhf.libairspyhf.py_cb_wrapper(dev_p)
#print(f"airspyhf_start ret={ret}")


ret = libairspyhf.airspyhf_set_freq(dev_p, 3865000)
print(f"airspyhf_set_freq ret={ret}")

count = 0
try:
    while (libairspyhf.airspyhf_is_streaming(dev_p)) and (count < 3):
        print("Main loop")
        time.sleep(1)
        count += 1
except:
    print("Error in main loop")

ret = libairspyhf.airspyhf_stop(dev_p)
print(f"airspyhf_stop ret={ret}")

#Not close for now
ret = libairspyhf.close(dev_p)
print("closed: Returned %d"%(ret))

print(f"Total samples received {sample_count}")

wave_file.close()

print("All is ok")

