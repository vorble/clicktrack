#!/usr/bin/env python3

import pyaudio
import random
import re
import sys
import time
import wave

def bpmDeltaSeconds(bpm):
    return 60.0 / bpm

def readChunks(filename):
    wf = wave.open(filename, 'rb')
    data = chunk = wf.readframes(1024)
    while len(chunk) > 0:
        chunk = wf.readframes(1024)
        data += chunk
    wf.close()
    return data

def playSound(chunk):
    stream.write(chunk)

if len(sys.argv) < 3:
    print('Usage: {} bpm measure [accent_beat ...]'.format(sys.argv[0]))
    print('  120 BPM in 4/4 with accents on 1 and 3: {} 120 4 1 3'.format(sys.argv[0]))
    print('  70 to 80 BPM in 3/8 with accent on 1: {} 70-80 3 1'.format(sys.argv[0]))
    sys.exit(1)

# Determine bpm. Regex here is for "float-float" format.
if re.match('^\d+(\.\d*)?-\d+(\.\d*)?$', sys.argv[1]):
    a, b = sys.argv[1].split('-')
    a, b = float(a), float(b)
    if b < a:
        a, b = b, a
    bpm = float(random.random() * (b - a) + a)
else:
    bpm = float(sys.argv[1])
measure = int(sys.argv[2])
accents = list(map(lambda x: int(x) - 1, sys.argv[3:]))

print('bpm', bpm)
print('measure', measure)
print('accents', accents)

def main():
    delta = bpmDeltaSeconds(bpm)
    tick = readChunks('tick.wav')
    tock = readChunks('tock.wav')
    step = 0
    time_next_tick = time.monotonic()
    while True:
        while time.monotonic() < time_next_tick:
            time.sleep(0.001)
        time_next_tick += delta
        playSound(tock if step in accents else tick)
        step = (step + 1) % measure

p = pyaudio.PyAudio()

# Assume the two files have the same format and just use the properties of one of them
# to set up the audio output stream.
wf = wave.open('tick.wav', 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
wf.close()

main()

stream.stop_stream()
stream.close()

p.terminate()

