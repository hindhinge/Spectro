import numpy as np
from mathfunctions import *
import matplotlib.pylab as plt

def getChunks(signal,fs,chunk_length,res):
    signal_length = len(signal)
    signal_length_seconds = signal_length / fs
    #resolution = int(np.ceil(fs * chunk_length)) #in samples per square on xaxis
    resolution = res
    iterations = int(np.ceil(signal_length/resolution))
    output = []
    print("iterations: "+str(iterations))
    print("signal_length: " + str(signal_length))
    print("signal_length_seconds: " + str(signal_length_seconds))
    print("resolution: " + str(resolution))
    for i in range(iterations):
        chunk = signal[i*resolution:((i+1)*resolution)+100]
        #chunk = signal[i*resolution:(i+1)*resolution]
        output.append(chunk)
    return output

def getFFT(signal):
    output = []
    for chunk in signal:
        fft = genFft(chunk,len(chunk))[1]
        output.append(fft)
    return output

def convertToColors(signal):
    max_value = 0
    output = []
    for value in signal:
        if(value > max_value):
            max_value = value
    resolution = max_value/255
    for value in signal:
        val = np.floor(value/resolution)
        color = (int(val),0,255)
        output.append(color)
    return output
#
# def convertToColors(signal):
#     max_value = 0
#     output = []
#     for value in signal:
#         if(value > max_value):
#             max_value = value
#     resolution = max_value/510
#     for value in signal:
#         val = np.floor(value/resolution)
#         if(val <= 255):
#             color = (int(val),0,255)
#             output.append(color)
#         else:
#             color = (255,0,int(255-(val-255)))
#             output.append(color)
#         return output




def genFFTplots(signal,fs):
    counter = 0
    for chunk in signal:
        counter += 1
        #x_axis = np.linspace(1,22050,num=len(chunk))
        n = (chunk.size*2) - 1
        timestep = 1/fs
        freq = np.fft.rfftfreq(n,d=timestep)
        plt.plot(freq[0:int(len(freq)/4)],chunk[0:int(len(chunk)/4)])
        plt.show()






