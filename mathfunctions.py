import numpy as np


def genTime(N, fs):
    time = np.zeros(N)
    for i in range(N):
        time[i] = i / fs
    return time

def genPlotTime(wave,fs):
    N = 0
    for w in wave:
        N += w.size
    time = np.zeros(N)
    for i in range(N):
        time[i] = i / fs
    return time


def genSin(time, A, fsin, fi):
    sine = A * np.sin((2 * np.pi * time * fsin) + fi)
    return sine


def genNoise(N, scale):
    noise = np.zeros(N)
    for i in range(N):
        noise[i] = np.random.rand() * scale
    return noise


def genRfreq(N, fs):
    freq = np.zeros(N)
    for k in range(0, int(N / 2)):
        freq[k] = k * fs / N
    return freq


def genFft(sig,N):
    y = np.fft.rfft(sig)
    modul = np.abs(y) / (N/2)
    return (y, modul)
