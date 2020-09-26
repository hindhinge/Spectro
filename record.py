import sounddevice as sd
import simpleaudio as sa
import pyaudio
import wave
import numpy


class Recording:
    def __init__(self, chunk, sample_format, channels, fs, seconds, filename):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.seconds = seconds
        self.filename = filename
        self.frames = []  # Initialize array to store frames
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream = None

    def record(self):
        print('Recording')
        stream = self.p.open(format=self.sample_format,
                             channels=self.channels,
                             rate=self.fs,
                             frames_per_buffer=self.chunk,
                             input=True)
        # Store data in chunks for 3 seconds
        counter = 0
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            self.frames.append(data)
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        print('Finished recording')

    def openStream(self):
        self.stream = self.p.open(format=self.sample_format,
                             channels=self.channels,
                             rate=self.fs,
                             frames_per_buffer=self.chunk,
                             input=True)

    def closeStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print('Finished recording')

    def recordChunk(self):
        print('Recording chunk')
        data = self.stream.read(self.chunk, exception_on_overflow = False) #  exception_on_overflow = False used to get rid of exception when we are recording at FS > 44100
        return numpy.fromstring(data, 'Int16')

    def save(self):
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()





##########################################################
# chunk = 1024  # Record in chunks of 1024 samples         #
# sample_format = pyaudio.paInt16  # 16 bits per sample    #
# channels = 2                                             #
# fs = 44100  # Record at 44100 samples per second         #
# seconds = 3                                              #
# filename = "output.wav"                                  #
##########################################################

