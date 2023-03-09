import os
import sys
import math

import airspyhf

import matplotlib
import numpy
import pylab

import pygame
from pygame import gfxdraw

CENTER_FREQ = 4e6
SAMPLE_RATE = 196e3
SAMPLE_NUM = 2048
GAIN = 'auto'

SCREEN_X = 1025
SCREEN_Y = 320

MOVE_STEP = 0.1e6

# init RTLSDR and if no then go out
try:
    pass
except IOError:
    print
    "Probably RTLSDR device not attached"
    sys.exit(0)

# config rtlsdr device
#rtl.sample_rate = SAMPLE_RATE
#rtl.center_freq = CENTER_FREQ
#rtl.gain = GAIN


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
    r = int((x + 50) * 255 // 50)
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
samples = []

run = True
line = 0
while run:

    # print "update"

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
                print
                "Left"
                rtl.center_freq -= MOVE_STEP
                print
                "Center freq: ", rtl.center_freq, " Hz"
            elif event.key == pygame.K_RIGHT:
                print
                "Right"
                rtl.center_freq += MOVE_STEP
                print
                "Center freq: ", rtl.center_freq, " Hz"

    width = SCREEN_X
    height = SCREEN_Y

    samples = rtl.read_samples(SAMPLE_NUM)
    spect = numpy.fft.fft(samples)
    spect = spect[0:len(spect) / 2]

    # (1/(Fs*N)) * abs(xdft).^2;
    spect_n = [(1.0 / (SAMPLE_NUM * len(spect))) * iq_abs(x) ** 2 for x in spect]
    spect_n = (10 * numpy.log10(spect_n)).tolist()

    # total data size
    spect_len = len(spect_n)

    # calculate amount spect points per pixel without rounding
    pixel_width = spect_len / SCREEN_X + 1
    pixel_steps = spect_len / pixel_width

    for step in range(0, pixel_steps):
        avg = 0.0
        for i in range(0, pixel_width):
            avg += spect_n[step * pixel_width + i]
        avg /= pixel_width

        # print avg
        # gfxdraw.pixel( screen, step, line, color_normalise((100-abs(avg))/10))
        gfxdraw.pixel(screen, step, line, color_mapping(avg))

    # draw central freq
    font = pygame.font.Font(None, 20)
    text = font.render(str(rtl.center_freq / 1e6), 1, (200, 30, 30), (0, 0, 0))
    screen.blit(text, (SCREEN_X / 2, SCREEN_Y - 20))
    text = font.render(str((rtl.center_freq + SAMPLE_RATE / 2) / 1e6), 1, (200, 30, 30), (0, 0, 0))
    screen.blit(text, (SCREEN_X - 40, SCREEN_Y - 20))
    text = font.render(str((rtl.center_freq - SAMPLE_RATE / 2) / 1e6), 1, (200, 30, 30), (0, 0, 0))
    screen.blit(text, (20, SCREEN_Y - 20))

    pygame.display.flip()
    line += 1
    if (line > SCREEN_Y):
        line = 0

pygame.quit

