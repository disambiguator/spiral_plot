#!/usr/bin/python
import sys
import pygame
import math
import random
import itertools
import argparse
import numpy
from scipy.io.wavfile import read
import scipy
import Color

class SpiralPlot:

    def __init__(self):
	# Color Iterator
        colors = [Color.red, Color.green, Color.blue] #darkBlue], white, black, pink]
        self.color_iterator = itertools.cycle(colors)

    def drawLine(self, (x1, y1), (x2, y2), delta):
        l = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        x2 = x1 + (l+delta)*(x2-x1)/l

        y2 = y1 + (l+delta)*(y2-y1)/l
    #   pygame.draw.aalines(self.screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), False, [(x1, y1), (x2, y2)], 1)
        pygame.draw.aalines(self.screen, self.color_iterator.next(), False, [(x1, y1), (x2, y2)], 1)
        return (x2, y2)

    def stft(self, x, fs, framesz, hop):
        framesamp = int(framesz*fs)
        hopsamp = int(hop*fs)
        w = scipy.hamming(framesamp)
        X = scipy.array([scipy.fft(w*x[i:i+framesamp])
                         for i in range(0, len(x)-framesamp, hopsamp)])
        return X

    def run(self, l=15, SIDE_COUNT=8):

        filename = 'loungedub.wav'

        (samplerate, audio_data) = read(filename)

        #Ditch one of the audio channels
        audio_data, _ = audio_data.reshape((2, -1))

        frame_size = 0.050 #50 milliseconds
        hop =   0.020 #20 milliseconds
        fft = self.stft(audio_data, samplerate, frame_size, hop)
        bins = numpy.split(fft, SIDE_COUNT, axis=1)
        averages = [numpy.average(b, axis=1) for b in bins]

        v_abs = numpy.vectorize(abs)
        averages = [v_abs(a) for a in averages]

        pygame.init()
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while 1:
            theta = 2*math.pi/SIDE_COUNT
            x_0 = pygame.display.Info().current_w/2
            y_0 = pygame.display.Info().current_h/2
            coords = [ (x_0 + l*math.cos(n*theta), y_0 + l*math.sin(n*theta)) for n in range(SIDE_COUNT) ]

            pygame.draw.aalines(self.screen, Color.white, False, coords, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            for _ in range(100):
                new_coords = []
                for i in range(SIDE_COUNT):
                    delta = averages[i][math.floor(pygame.mixer.music.get_pos()/(hop*1000))]/1000
                    new_coords.append(self.drawLine(coords[(i-1) % SIDE_COUNT], coords[i], delta))

                coords = new_coords

            pygame.display.update()
            self.screen.fill( (0, 0, 0) )

PARSER = argparse.ArgumentParser()
PARSER.add_argument('length', type=int)
PARSER.add_argument('sidecount', type=int)
ARGS = PARSER.parse_args()
SpiralPlot().run(l=ARGS.length, SIDE_COUNT=ARGS.sidecount)
pygame.quit()
sys.exit()
