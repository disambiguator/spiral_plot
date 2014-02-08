#!/usr/bin/python
import sys
import pygame
import math
import time
import random
import itertools
import argparse
import numpy
from scipy.io.wavfile import read
import scipy

class spiralPlot:

    def drawLine(self, (x1, y1), (x2, y2)):
        l = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        x2 = x1 + (l+self.delta)*(x2-x1)/l

        y2 = y1 + (l+self.delta)*(y2-y1)/l
    #   pygame.draw.aalines(self.screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), False, [(x1, y1), (x2, y2)], 1)
        pygame.draw.aalines(self.screen, self.c_iter.next(), False, [(x1, y1), (x2, y2)], 1)    
        return (x2, y2)

    def stft(self, x, fs, framesz, hop):
        framesamp = int(framesz*fs)
        hopsamp = int(hop*fs)
        w = scipy.hamming(framesamp)
        X = scipy.array([scipy.fft(w*x[i:i+framesamp])
                         for i in range(0, len(x)-framesamp, hopsamp)])
        return X

    def run(self, l=15, delta=15, SIDE_COUNT=8):
        self.delta = delta
        
        pygame.init()
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        self.screen=pygame.display.set_mode((screen_width, screen_height))
        
        #colors
        red = (255,0,0)
        green = (0,255,0)
        blue = (0,0,255)
        darkBlue = (0,0,128)
        white = (255,255,255)
        black = (0,0,0)
        pink = (255,200,200)
        colors = [red, green, blue] #darkBlue], white, black, pink]
        self.c_iter=itertools.cycle(colors)

        filename = 'loungedub.wav'

        (samplerate, audio_data) = read(filename)
        audio_data = numpy.average(audio_data, axis=1)

        frame_size = 0.050 #50 milliseconds
        hop =   0.020 #20 milliseconds
        X = self.stft(audio_data, samplerate, frame_size, hop)
        X = numpy.average(X, axis=1)
 
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        start_time = time.time()

        while 1:
            theta = 2*math.pi/SIDE_COUNT
            x0 = pygame.display.Info().current_w/2
            y0 = pygame.display.Info().current_h/2
            coords = [ (x0 + l*math.cos(n*theta),y0 + l*math.sin(n*theta)) for n in range(SIDE_COUNT) ]

            pygame.draw.aalines(self.screen, white, False, coords, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.delta = X[math.floor((time.time() - start_time)/hop)]/100
            print self.delta

            for _ in range(100):
                coords = [self.drawLine(coords[(i-1) % SIDE_COUNT], coords[i]) for i in range(SIDE_COUNT)]

            pygame.display.update()
            self.screen.fill( (0,0,0) )

parser= argparse.ArgumentParser()
parser.add_argument('length', type=int)
parser.add_argument('delta', type=int)
parser.add_argument('sidecount', type=int)
args = parser.parse_args()
spiralPlot().run(l=args.length, delta=args.delta, SIDE_COUNT=args.sidecount)
pygame.quit()
sys.exit()
