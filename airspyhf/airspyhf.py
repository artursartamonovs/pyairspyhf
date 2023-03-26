from .libairspyhf import *
from ctypes import *

class AirSpyHF:
    dev_p = airspyhf_device_t_p(None)
    sample_rates = []
    initalized = False
    cur_freq = 0
    def __init__(self,):
        #self.dev_p =  airspyhf_device_t_p(None)
        pass

    def open(self, device_index=None, serialnumber=None):
        if serialnumber is not None:
            print("open by serial number")
            ret = libairspyhf.airspyhf_open_sn(self.dev_p, 0x3b52ab5dada12535)
            if ret != 0:
                print("Cant open device by serial number")
                return -1
            self.initalized = True
        elif device_index is not None:
            print("open by index")
            ndev = libairspyhf.airspyhf_list_devices(None, 0)
            if ndev < device_index+1:
                print("Device index higher then device num")
                return -1
            print(ndev)
            serial = c_uint64(0)
            libairspyhf.airspyhf_list_devices(byref(serial), device_index + 1)
            print("try to open by serial ",hex(serial.value))
            ret = libairspyhf.airspyhf_open_sn(self.dev_p, serial.value)
            if ret != 0:
                print("Cant open device by index")
                return -1
            self.initalized = True
        return 0

    def get_samplerates(self):
        if not self.initalized:
            return []
        nsrates = c_uint32(0)
        print("get sample rate number")
        ret = libairspyhf.airspyhf_get_samplerates(self.dev_p, byref(nsrates), c_uint32(0))
        if ret != 0:
            print("Cant get number of avaliable sample rates")
            return []
        print("supported sample rates values")
        supported_samplerates = (c_uint32 * nsrates.value)(0)
        ret = libairspyhf.airspyhf_get_samplerates(self.dev_p, supported_samplerates, nsrates)
        if ret != 0:
            print("Cant get avaliable sample rate list")
            return []
        self.sample_rates = list(supported_samplerates)
        return self.sample_rates

    def set_samplerate(self, samplerate:int):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        if self.sample_rates == []:
            self.get_samplerates()
        if samplerate not in self.sample_rates:
            print(f"Unknown sample rate. Avaliable samplerate {self.sample_rates}")
            return -1

        ret = libairspyhf.airspyhf_set_samplerate(self.dev_p, samplerate)
        if ret != 0:
            print("Cannot set samplerate")
            return -1

        return 0

    def set_hf_agc(self,flag):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_set_hf_agc(self.dev_p, flag)
        return ret

    def set_hf_agc_threshold(self,flag):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_set_hf_agc_threshold(self.dev_p, flag)
        return ret

    def set_hf_att(self, value):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_set_hf_att(self.dev_p, value)
        return ret

    def set_hf_lna(self,flag):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_set_hf_lna(self.dev_p, flag)
        return ret

    def set_frequency(self, freq:int):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_set_freq(self.dev_p, int(freq))
        if ret != 0:
            return -1
        self.cur_freq = int(freq)
        return 0

    #def get_frequency(self,freq:int):
    #    return self.cur_freq

    def start(self, read_samples_cb):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        #read_samples()
        #ret = libairspyhf.airspyhf_start(self.dev_p, airspyhf_sample_block_cb_fn(read_samples), None)
        ret = libairspyhf.airspyhf_start(self.dev_p, read_samples_cb, None)
        if ret != 0:
            print(f"airspyhf_start ret={ret}")
            return -1
        return 0

    def is_streaming(self):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        return libairspyhf.airspyhf_is_streaming(self.dev_p)

    def stop(self):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.airspyhf_stop(self.dev_p)
        if ret != 0:
            print(f"airspyhf_stop ret={ret}")
            return -1
        return 0

    def close(self):
        if not self.initalized:
            print("airspy not initalized")
            return -1
        ret = libairspyhf.close(self.dev_p)
        if ret != 0:
            print("Cant close device")
            return -1
        return 0





