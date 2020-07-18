from scipy.io.wavfile import read
import numpy as np
import simpleaudio as sa

def wavToArray(name):
    a = read(name)
    array = np.array(a[1], dtype=float)
    return array

def sliceAudio(sig, fs):
    slices = []
    seconds = np.ceil(sig.size / fs)
    for i in range(int(seconds)):
        slices.append(sig[i*fs:(i+1)*fs])
    return slices

def playAudio(sig,fs):
    audio = sig * (2**15 - 1) / np.max(np.abs(sig))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

def stereoToMono(audiodata):
    newaudiodata = []

    for i in range(len(audiodata)):
        d = (audiodata[:,0] + audiodata[:,1]) / 2
        newaudiodata.append(d)

    return np.array(newaudiodata, dtype='int16')