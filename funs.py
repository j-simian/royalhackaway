from statistics import mean
import pygame

class Timer():
    def __init__(self, bpm, offset):
        self.bpm = bpm
        self.offset = offset

    def getTimer(self):
        # milliseconds since start of song
        ms = pygame.mixer.music.get_pos()
        return ms/1000.0-self.offset


    def findAccuracy(self):
        q = (60/self.bpm)/2  #quarter note length
        waythrough = (self.getTimer() / q) % 1  #0 to 1
        accuracy = (0.5+waythrough)%1-0.5 #-0.5 to 0.5
        whichNote = round(self.getTimer() / (q)) % 2
        return (accuracy,whichNote)

    def onRhythm(self, echo=False):
        (accuracy,whichNote) = self.findAccuracy()
        perfectThreshold = 0.25 #tolerance either side of note
        hitThreshold = 0.5
        if echo:
            print(accuracy)
        if (abs(accuracy) < perfectThreshold):
            return ("perfect",whichNote)
        elif (abs(accuracy) < hitThreshold):
            return ("hit",whichNote)
        else:
            return ("miss",whichNote)

    def getFullFrame(self):
        q = (60/self.bpm)
        return round(self.getTimer() / q)

    def getHalfFrame(self):
        q = (60/self.bpm)/2
        return round(self.getTimer() / q) / 2
