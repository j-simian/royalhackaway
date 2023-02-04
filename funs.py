from statistics import mean
accuracies=[]
def onRhythm(timer, offset, bpm):
    q = (60/bpm)/2  #half note length
    accuracy = ((timer / q) - offset) % 1 #0 to 1, 0 or 1 are perfect
    perfectThreshold = 0.1
    hitThreshold = 0.25
    #print(accuracy)
    if (accuracy < perfectThreshold or
        accuracy > 1-perfectThreshold):
        return "perfect"
    elif (accuracy < hitThreshold or
        accuracy > 1-hitThreshold):
        return "hit"
    else:
        return "miss"