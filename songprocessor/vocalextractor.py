import torch
import torchaudio
import numpy as np
from scipy.io import wavfile
import audio
import os
from openunmix import predict
MODEL_RATE = 44100

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

filename = "./Beat_it.wav"

def fixsamplerate(samplerate, vocals_tensor):
    if samplerate != MODEL_RATE:
        resampler = torchaudio.transforms.Resample(orig_freq=MODEL_RATE, new_freq=samplerate)
        vocals_tensor = resampler(vocals_tensor)

def cleanupaudio(vocals_tensor):
    frame = int(0.02 * MODEL_RATE)  
    v_mono = vocals_tensor.mean(dim=0).numpy()

    pad = (-len(v_mono)) % frame
    v_rms = np.sqrt(np.mean(np.pad(v_mono, (0, pad)).reshape(-1, frame) ** 2, axis=1))
    threshold = v_rms.max() * 0.05 

    frame_mask = (v_rms > threshold).astype(np.float32)
    sample_mask = np.repeat(frame_mask, frame)[:len(v_mono)]
    sample_mask = np.convolve(sample_mask, np.ones(frame) / frame, mode="same")
    vocals_tensor = vocals_tensor * torch.from_numpy(sample_mask).float()
    return vocals_tensor


audio = audio.audio(filename)
samplerate = audio.get_samplerate()
# estimates = predict.separate(
#     audio.tensor(),
#     rate=samplerate,
#     targets=['vocals'],
#     residual=True,
#     device=device,
# )



# vocals_tensor = estimates["vocals"].detach().cpu()[0]  




# fixsamplerate(samplerate, vocals_tensor)
# cleanedaudio = cleanupaudio(vocals_tensor)

# vocalaudio = cleanedaudio.numpy().T
# vocalaudio = np.clip(vocalaudio, -1.0, 1.0)
# vocalaudio = (vocalaudio * 32767).astype(np.int16)


# output = filename + "_vocals.wav"
# wavfile.write(output, samplerate, vocalaudio)





