from record import Recording
import pyaudio
import numpy as np
from mathfunctions import genRfreq
import wave
import matplotlib.pyplot as plt
rec = Recording(1024,pyaudio.paInt16,2,44100,1,"mic_test.wav")

def genFft(sig, N):
    y = np.fft.rfft(sig)
    modul = np.abs(y) / (N/2)
    return (y, modul)

rec.openStream()

chunks = []
dfts = []
rfreq = genRfreq(2048,44100)
for i in range(100):
    chunk = rec.recordChunk()
    dft = genFft(chunk,44100)
    chunks.append(chunk)
    dfts.append(dft[1])
wf = wave.open("mic_test.wav", 'wb')
wf.setnchannels(2)
wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(chunks))
wf.close()

# dft1 = genFft(chunk1,44100)
# dft2 = genFft(chunk2,44100)
# rfreq = genRfreq(len(dft1[1]),44100)
