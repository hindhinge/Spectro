from mathfunctions import *
from record import *
from play import *
import matplotlib.pylab as plt
import numpy as np
import scipy.io.wavfile as wavf


def genChirp(fstart,fend,fs,length):
    start_freq = fstart
    end_freq = fend
    fs_rate = fs
    len_of_sig = length
    t = np.linspace(0, 2 * np.pi * len_of_sig, num=fs_rate * len_of_sig)
    f0 = start_freq
    f1 = (end_freq / 2) + (start_freq / 2)
    f = np.arange(start = f0,step = (f1 - f0) / len(t),stop = (f1 - (f1 - f0) / len(t)))

    try:
        out = np.array(0.8 * np.sin(f * t))
    except ValueError:
        out = np.array(0.8 * np.sin(f * t[:-1]))
    out_f = 'chirp.wav'
    wavf.write(out_f, fs_rate, out)
    return out

    # rfreq = genRfreq(44100, fs_rate)
    # fft = genFft(out, fs_rate)
    # plt.plot(rfreq[0:fft[1].size], fft[1])
    # plt.axis('tight')
    # plt.show()
    #
    # xaxis = genPlotTime(out, fs_rate)
    # plt.plot(xaxis,out)
    # plt.show()
    # out_f = 'chirp.wav'
    # wavf.write(out_f, fs_rate, out)
