import sounddevice as sd
import numpy as np

def beep(frequency, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    samples = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(samples, samplerate=sample_rate)
    sd.wait()



if True:
    beep(1000, 0.1)
    print("Done")
else:
    print("Nothing")