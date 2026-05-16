import torch
import numpy as np
from scipy.io import wavfile


class audio():
    def __init__(self, filename: str):
        self.filename   = filename
        self.samplerate, self.audio_data = wavfile.read(filename)
        self.audio_data = self.audio_data.astype(np.float32)
        self.chunked_audio = self.__chunk__(self.audio_data)

    def __split__(self , s, n):
         return [s[i:i+n] for i in range(0, len(s), n)]


    def __chunk__(self, audio_data):

        # 10 seconds of audio
        chunk_size = self.samplerate * 10
        chunked = self.__split__(audio_data, chunk_size)
        return chunked

    def tensor(self):
        if self.audio_data.max() > 1.0:
            audio_data /= 32768.0

        if self.audio_data.ndim == 1:
            self.audio_data = audio_data[np.newaxis, np.newaxis, :]
        else:
            self.audio_data = self.audio_data.T[np.newaxis, :]

        audio_tensor = torch.from_numpy(audio_data).float()
        return audio_tensor
    
    def get_samplerate(self):
        print(self.samplerate)
        return self.samplerate
    
