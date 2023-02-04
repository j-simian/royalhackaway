from statistics import mean

def findAccuracy(timer, offset, bpm):
    q = (60/bpm)/2  #quarter note length
    accuracy = ((timer-offset) / q) % 1 #0 to 1, 0 or 1 are perfect
    whichNote = round((timer-offset)/(q)) % 2
    return (accuracy,whichNote)

def onRhythm(timer, offset, bpm,echo=False):
    (accuracy,whichNote) = findAccuracy(timer,offset,bpm)
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