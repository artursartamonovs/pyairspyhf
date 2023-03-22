import os
import sys
import math

import airspyhf

import matplotlib
import numpy
import pylab
import time
import threading

import pygame
from pygame import gfxdraw

CENTER_FREQ = 101000000
SAMPLE_RATE = 196e3
SAMPLE_NUM = 2048

SCREEN_X = 1025
SCREEN_Y = 320

MOVE_STEP = int(SAMPLE_RATE/2)

sample_buf_lock = threading.Lock()

# init AIRSPY and if no then go out
airspy = airspyhf.AirSpyHF()
if airspy.open(device_index=0) == -1:
    print("Cant open airspyhf device")
    sys.exit(1)

# config rtlsdr device
airspy.set_samplerate(SAMPLE_RATE)
airspy.set_frequency(CENTER_FREQ)
airspy.set_hf_agc(1)
airspy.set_hf_agc_threshold(0)
airspy.set_hf_lna(1)


def iq_abs(c):
    return (math.sqrt((c.real ** 2 + c.imag ** 2)))


# point should be normalised to 0.0 ... 1.0
def color_normalise(point):
    ret = (255, 0, 0)
    # blue
    if (point < 0.3):
        ret = (0, 0, int(point * 255 * 3.3))
    # yello
    elif (point < 0.7):
        ret = (0, int((point - 0.3) * 255 * 2.5), 0)
    # red
    elif (point <= 1.0):
        ret = (int((point - 0.7) * 255 * 3.3), 0, 0)
    else:
        # print "Color Error ", point
        pass
    return ret


def color_mapping(x):
    "assumes -50 to 0 range, returns color"
    r = int((x + 70) * 255 // 70)
    r = max(0, r)
    r = min(255, r)
    return (r, r, 100)


# def draw_Hz( surface, x, y, hz ):


arr = [[0 for i in range(0, SCREEN_X)] for j in range(0, SCREEN_Y)]

# init all pygame modules audio,video and more
pygame.init()

# [NEW] creates screen surface using constants
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

#samples = rtl.read_samples(SAMPLE_NUM)
sample_buffer = []
def read_samples(transfer):
    global sample_buffer
    #print("callback")
    #if sample_buf_lock.locked():
    #    print("Buffer locked")
    #    return 0
    #sample_buf_lock.acquire()
    #print("Python call back")
    t = transfer.contents
    bytes_to_write = t.sample_count * 4 * 2
    #print("Received %d samples"%(t.sample_count))
    rx_buffer = t.samples
    #print(f"{bytes_to_write} bytes receieved")
    #sample_buffer.append(rx_buffer)
    for i in range(0,t.sample_count):
        d_re = t.samples[i].re
        d_im = t.samples[i].im
        sample_buffer.append(math.sqrt(d_re*d_re+d_im*d_im))
        #data = struct.pack("<f",d_re) # FIX ?!
        #wave_file.writeframesraw(data)
        #data = struct.pack("<f", d_im)  # FIX ?!
        #wave_file.writeframesraw(data)
    #print("End call back")
    #sample_buf_lock.release()
    return 0

def get_samples(num=1024):
    global sample_buffer
    buf_size = len(sample_buffer)

    if buf_size < num:
        print("sample buffer small")
        return [1]*num
    print("getting stuff ", buf_size)
    #while sample_buf_lock.locked():
    #    time.sleep(0.1)
    samples = sample_buffer[:int(buf_size/2)]
    del sample_buffer[:int(buf_size/2)]
    return samples
    #if len(samples) == num:
    #    sample_buffer = []
    #    return samples
    #if len(samples) > num:
    #    arr = []
    #    times = len(samples)/num
    #    for i in range(0, num):
    #        avg = numpy.average(samples[times*num:times*num+times-1])
    #        arr.append(avg)
    #    return arr
    #else:
    #    print("Error in get_samples")
    #    return []
    return []

read_samples_cb = airspyhf.airspyhf_sample_block_cb_fn(read_samples)
airspy.start(read_samples_cb)

run = True
line = 0
while run and airspy.is_streaming():

    print("Loop tick")

    # check for all events that where ocure
    for event in pygame.event.get():
        # if some one clicked on close button
        if event.type == pygame.QUIT:
            # terminate programm
            run = False
            # don't waste your time by waiting while event loop will end
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left")
                #rtl.center_freq -= MOVE_STEP
                airspy.set_frequency(airspy.cur_freq - MOVE_STEP)
                #print("Center freq: ", rtl.center_freq, " Hz")
            elif event.key == pygame.K_RIGHT:
                print("Right")
                #rtl.center_freq += MOVE_STEP
                #print("Center freq: ", rtl.center_freq, " Hz")
                airspy.set_frequency(airspy.cur_freq + MOVE_STEP)

    width = SCREEN_X
    height = SCREEN_Y

    samples = get_samples(SAMPLE_NUM)
    if samples == []:
        print("sample buffer is empty")
        time.sleep(1)
        continue
    #print(samples)
    spect = numpy.fft.fft(samples,n=SAMPLE_NUM)

    spect = spect[0:int((len(spect) / 2))]

    # (1/(Fs*N)) * abs(xdft).^2;
    spect_n = [(1.0 / (SAMPLE_NUM * len(spect))) * iq_abs(x) ** 2 for x in spect]
    spect_n = (10 * numpy.log10(spect_n)).tolist()

    #print(spect_n)

    # total data size
    spect_len = len(spect_n)
    #print(spect_len)
    # calculate amount spect points per pixel without rounding
    pixel_width = int(spect_len / SCREEN_X + 1)
    #print(pixel_width)
    pixel_steps = int(spect_len / pixel_width)
    #print(pixel_steps)
    #print(spect_n)
    for step in range(0, pixel_steps):
        avg = 0.0
        for i in range(0, pixel_width):
            avg += spect_n[step * pixel_width + i]
        avg /= pixel_width
        if math.isinf(avg):
            avg = -1000

        # print avg
        # gfxdraw.pixel( screen, step, line, color_normalise((100-abs(avg))/10))
        gfxdraw.pixel(screen, step, line, color_mapping(int(avg)))

    # draw central freq
    #font = pygame.font.Font(None, 20)
    #text = font.render(str(rtl.center_freq / 1e6), 1, (200, 30, 30), (0, 0, 0))
    #screen.blit(text, (SCREEN_X / 2, SCREEN_Y - 20))
    #text = font.render(str((rtl.center_freq + SAMPLE_RATE / 2) / 1e6), 1, (200, 30, 30), (0, 0, 0))
    #screen.blit(text, (SCREEN_X - 40, SCREEN_Y - 20))
    #text = font.render(str((rtl.center_freq - SAMPLE_RATE / 2) / 1e6), 1, (200, 30, 30), (0, 0, 0))
    #screen.blit(text, (20, SCREEN_Y - 20))

    pygame.display.flip()
    line += 1
    if (line > SCREEN_Y):
        line = 0
    time.sleep(0.1)

pygame.quit()

airspy.stop()
airspy.close()

