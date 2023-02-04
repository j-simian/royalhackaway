from statistics import mean

class Timer():
    def __init__(bpm, offset):
        self.bpm = bpm
        self.offset = offset

    def getTimer():
        # milliseconds since start of song
        ms = pygame.mixer.music.get_pos()
        return ms/1000.0-self.offset

    def findAccuracy():
        q = (60/self.bpm)/2  #quarter note length
        accuracy = (getTimer() / q) % 1 #0 to 1, 0 or 1 are perfect
        whichNote = round(getTimer() / (q)) % 2
        return (accuracy,whichNote)

    def onRhythm(echo=False):
        (accuracy,whichNote) = self.findAccuracy(getTimer(),self.bpm)
        perfectThreshold = 0.25 #tolerance either side of note
        hitThreshold = 0.5
        if echo:
            print((0.5+accuracy)%1-0.5)
        if (accuracy < perfectThreshold or
            accuracy > 1-perfectThreshold):
            return ("perfect",whichNote)
        elif (accuracy < hitThreshold or
            accuracy > 1-hitThreshold):
            return ("hit",whichNote)
        else:
            return ("miss",whichNote)

