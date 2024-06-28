
def manchester_decode(pulseStream) -> list:
    i = 1

    bits = []

    # here pulseStream[i] is "guaranteed" to be the beginning of a bit
    while i < len(pulseStream):
        if pulseStream[i] == pulseStream[i-1]:
            # if so, sync has slipped
            # try to resync
            i = i - 1
        bits.append(pulseStream[i] == 1)
        i = i + 2

    return bits

