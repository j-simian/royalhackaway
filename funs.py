def onRhythm(timer, offset, bpm):
    q = (60/bpm)/4  #quarter note length
    accuracy = ((timer-offset) % q) / q #0 to 1, 0 or 1 are perfect
    perfectThreshold = 0.2
    hitThreshold = 0.4
    if (accuracy < perfectThreshold or
        accuracy > 1-perfectThreshold):
        return "perfect"
    elif (accuracy < hitThreshold or
        accuracy > 1-hitThreshold):
        return "hit"
    else:
        return "miss"