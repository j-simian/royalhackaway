from statistics import mean

accuracies=[]
def onRhythm(timer, offset, bpm,echo=False):
    q = (60/bpm)/2  #quarter note length
    accuracy = ((timer-offset) / q) % 1 #0 to 1, 0 or 1 are perfect
    whichNote = round((timer-offset)/(q)) % 2
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