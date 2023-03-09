import sys
import os
from ctypes import *
from ctypes.util import find_library


def load_libairspyhf():
    if sys.platform == "linux" and 'LD_LIBRARY_PATH' in os.environ.keys():
        ld_library_paths = [local_path for local_path in os.environ['LD_LIBRARY_PATH'].split(':') if local_path.strip()]
        if "AIRSPYHF_TEST_PATH" in os.environ:
            ld_library_paths = [os.environ["AIRSPYHF_TEST_PATH"]]
        driver_files = [local_path + '/libairspyhf.so' for local_path in ld_library_paths]
    else:
        driver_files = []
    driver_files += ['libairspyhf.so']
    driver_files += ['airspyhf.dll', 'libairspyhf.so', 'libairspyhf.dylib']
    driver_files += ['..//airspyhf.dll', '..//libairspyhf.so']
    driver_files += [lambda : find_library('airspyhf'), lambda : find_library('libairspyhf')]
    dll = None

    for driver in driver_files:
        if callable(driver):
            driver = driver()
        if driver is None:
            continue
        #print("Search for driver named %s"%(driver))
        try:
            dll = CDLL(driver)
            break
        except:
            pass
    else:
        raise ImportError('Error loading libairspyhf. Make sure libairspyhf '\
                          '(and all of its dependencies) are in your path')

    return dll

libairspyhf = load_libairspyhf()


#typedef struct {
#	uint32_t major_version;
#	uint32_t minor_version;
#	uint32_t revision;
#} airspyhf_lib_version_t;

airspyhf_device_t_p = c_void_p
class airspyhf_lib_version_t(Structure):
    _fields_ = [("major_version", c_uint32),
                ("minor_version", c_uint32),
                ("revision",      c_uint32)]

class airspyhf_complex_float_t(Structure):
    _fields_ = [("re",c_float),
                ("im",c_float)]
airspyhf_complex_float_t_p = POINTER(airspyhf_complex_float_t)

class airspyhf_transfer_t(Structure):
    _fields_ = [("device",airspyhf_device_t_p),
                ("ctx",c_void_p),
                ("samples",airspyhf_complex_float_t_p),
                ("sample_count",c_int),
                ("dropped_samples",c_uint64)]
airspyhf_transfer_t_p = POINTER(airspyhf_transfer_t)
#airspyhf_transfer_t_p = c_void_p

#typedef int (*airspyhf_sample_block_cb_fn) (airspyhf_transfer_t* transfer_fn);
#airspyhf_sample_block_cb_fn = CFUNCTYPE(c_int, POINTER(airspyhf_transfer_t))
airspyhf_sample_block_cb_fn = PYFUNCTYPE(c_int, POINTER(airspyhf_transfer_t))

#void ADDCALL airspyhf_lib_version(airspyhf_lib_version_t* lib_version);
f = libairspyhf.airspyhf_lib_version
f.restype, f.argtypes = None, [POINTER(airspyhf_lib_version_t)]

#int ADDCALL airspyhf_list_devices(uint64_t *serials, int count);
f = libairspyhf.airspyhf_list_devices
f.restype, f.argtypes = c_int, [POINTER(c_uint64), c_int]

#int ADDCALL airspyhf_open(airspyhf_device_t** device);
f = libairspyhf.airspyhf_open
f.restype, f.argtypes = c_int, [POINTER(airspyhf_device_t_p)]

#int ADDCALL airspyhf_open_sn(airspyhf_device_t** device, uint64_t serial_number);
f = libairspyhf.airspyhf_open_sn
f.restype, f.argtypes = c_int, [POINTER(airspyhf_device_t_p), c_uint64]


#int ADDCALL airspyhf_open_fd(airspyhf_device_t** device, int fd);
f = libairspyhf.airspyhf_open_fd
f.restype, f.argtypes = c_int, [POINTER(airspyhf_device_t_p), c_int]

#int ADDCALL airspyhf_close(airspyhf_device_t* device);
f = libairspyhf.airspyhf_close
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#nt ADDCALL airspyhf_get_output_size(airspyhf_device_t* device); /* Returns the number of IQ samples to expect in the callback */
f = libairspyhf.airspyhf_get_output_size
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]


#int ADDCALL airspyhf_start(airspyhf_device_t* device, airspyhf_sample_block_cb_fn callback, void* ctx);
f = libairspyhf.airspyhf_start
f.restype, f.argtypes = c_int, [airspyhf_device_t_p,airspyhf_sample_block_cb_fn,py_object]

#int ADDCALL airspyhf_stop(airspyhf_device_t* device);
f = libairspyhf.airspyhf_stop
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#int ADDCALL airspyhf_is_streaming(airspyhf_device_t* device);
f = libairspyhf.airspyhf_is_streaming
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#int ADDCALL airspyhf_is_low_if(airspyhf_device_t* device); /* Tells if the current sample rate is Zero-IF (0) or Low-IF (1) */
f = libairspyhf.airspyhf_is_low_if
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#int ADDCALL airspyhf_set_freq(airspyhf_device_t* device, const uint32_t freq_hz);
f = libairspyhf.airspyhf_set_freq
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint32]

#int ADDCALL airspyhf_set_freq_double(airspyhf_device_t* device, const double freq_hz);
f = libairspyhf.airspyhf_set_freq_double
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_double]

#int ADDCALL airspyhf_set_lib_dsp(airspyhf_device_t* device, const uint8_t flag); /* Enables/Disables the IQ Correction, IF shift and Fine Tuning. */
f = libairspyhf.airspyhf_set_lib_dsp
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint8]

#int ADDCALL airspyhf_get_samplerates(airspyhf_device_t* device, uint32_t* buffer, const uint32_t len);
f = libairspyhf.airspyhf_get_samplerates
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, POINTER(c_uint32), c_uint32]

#int ADDCALL airspyhf_set_samplerate(airspyhf_device_t* device, uint32_t samplerate);
f = libairspyhf.airspyhf_set_samplerate
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint32]

#int ADDCALL airspyhf_get_calibration(airspyhf_device_t* device, int32_t* ppb);
f = libairspyhf.airspyhf_get_calibration
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, POINTER(c_int32)]

#int ADDCALL airspyhf_set_calibration(airspyhf_device_t* device, int32_t ppb);
f = libairspyhf.airspyhf_set_calibration
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_int32]

#int ADDCALL airspyhf_get_vctcxo_calibration(airspyhf_device_t* device, uint16_t* vc);
f = libairspyhf.airspyhf_get_vctcxo_calibration
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, POINTER(c_uint16)]

#int ADDCALL airspyhf_set_vctcxo_calibration(airspyhf_device_t* device, uint16_t vc);
f = libairspyhf.airspyhf_set_vctcxo_calibration
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint16]

#int ADDCALL airspyhf_set_optimal_iq_correction_point(airspyhf_device_t* device, float w);
f = libairspyhf.airspyhf_set_optimal_iq_correction_point
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_float]

#int ADDCALL airspyhf_iq_balancer_configure(airspyhf_device_t* device, int buffers_to_skip, int fft_integration, int fft_overlap, int correlation_integration);
f = libairspyhf.airspyhf_iq_balancer_configure
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_int, c_int, c_int, c_int]

#int ADDCALL airspyhf_flash_calibration(airspyhf_device_t* device);	/* streaming needs to be stopped */
f = libairspyhf.airspyhf_flash_calibration
f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#int ADDCALL airspyhf_board_partid_serialno_read(airspyhf_device_t* device, airspyhf_read_partid_serialno_t* read_partid_serialno);
#f = libairspyhf.airspyhf_board_partid_serialno_read(
#f.restype, f.argtypes = c_int, [airspyhf_device_t_p]

#int ADDCALL airspyhf_version_string_read(airspyhf_device_t* device, char* version, uint8_t length);
f = libairspyhf.airspyhf_version_string_read
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_char_p, c_uint8]

#int ADDCALL airspyhf_set_user_output(airspyhf_device_t* device, airspyhf_user_output_t pin, airspyhf_user_output_state_t value);


#int ADDCALL airspyhf_set_hf_agc(airspyhf_device_t* device, uint8_t flag);				/* 0 = off, 1 = on */
f = libairspyhf.airspyhf_set_hf_agc
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint8]

#int ADDCALL airspyhf_set_hf_agc_threshold(airspyhf_device_t* device, uint8_t flag);	/* when agc on: 0 = low, 1 = high */
f = libairspyhf.airspyhf_set_hf_agc_threshold
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint8]

#int ADDCALL airspyhf_set_hf_att(airspyhf_device_t* device, uint8_t value); /* Possible values: 0..8 Range: 0..48 dB Attenuation with 6 dB steps */
f = libairspyhf.airspyhf_set_hf_att
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint8]

#int ADDCALL airspyhf_set_hf_lna(airspyhf_device_t* device, uint8_t flag);	/* 0 or 1: 1 to activate LNA (alias PreAmp): 1 = +6 dB gain - compensated in digital */
f = libairspyhf.airspyhf_set_hf_lna
f.restype, f.argtypes = c_int, [airspyhf_device_t_p, c_uint8]


__all__ = ["libairspyhf", "airspyhf_lib_version_t", "airspyhf_device_t_p", "airspyhf_sample_block_cb_fn", "airspyhf_complex_float_t_p", "airspyhf_transfer_t_p"]