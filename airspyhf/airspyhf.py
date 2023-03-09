from .libairspyhf import *
from ctypes import *

class AirSpyHF:
    dev_p = airspyhf_device_t_p(None)
    sample_rates = []
    def __init__(self,):
        self.dev_p = None

    def open(self, device_index:int=None, serialnumber:int=None):
        if serialnumber is not None:
            ret = libairspyhf.airspyhf_open_sn(self.dev_p, serialnumber)
            if ret != 0:
                print("Cant open device by serial number")
                return -1
        elif device_index is not None:
            ndev = libairspyhf.airspyhf_list_devices(None, 0)
            if ndev < device_index+1:
                print("Device index higher then device num")
                return -1
            serial = c_uint64(0)
            libairspyhf.airspyhf_list_devices(byref(serial), device_index + 1)
        return 0

    def get_samplerates(self):
        nsrates = c_uint32(0)
        ret = libairspyhf.airspyhf_get_samplerates(self.dev_p, byref(nsrates), c_uint32(0))
        if ret != 0:
            print("Cant get number of avaliable sample rates")
            return []
        supported_samplerates = (c_uint32 * nsrates)(0)
        ret = libairspyhf.airspyhf_get_samplerates(self.dev_p, supported_samplerates, nsrates)
        if ret != 0:
            print("Cant get avaliable sample rate list")
            return []
        self.sample_rates = list(supported_samplerates)
        return self.sample_rates

    def set_samplerate(self, samplerate:int):
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
        ret = libairspyhf.airspyhf_set_hf_agc(self.dev_p, flag)
        return ret

    def set_hf_agc_threshold(self,flag):
        ret = libairspyhf.airspyhf_set_hf_agc_threshold(self.dev_p, flag)
        return ret

    def set_hf_att(self, value):
        ret = libairspyhf.airspyhf_set_hf_att(dev_p, value)
        return ret
    
    def set_hf_lna(self,flag):
        ret = libairspyhf.airspyhf_set_hf_lna(dev_p, 1)
        return ret

    def close(self):
        ret = libairspyhf.close(self.dev_p)
        if ret != 0:
            print("Cant close device")





