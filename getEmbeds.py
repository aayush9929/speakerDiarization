import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb")

from pyannote.audio import Audio
from pyannote.core import Segment
audio = Audio(sample_rate=16000, mono="downmix")
audio_file_path = r'C:\Users\user\Documents\New folder\sample_audio_1.wav'

# extract embedding for a speaker speaking between t=3s and t=6s
speaker1 = Segment(3., 6.)
waveform1, sample_rate = audio.crop(audio_file_path, speaker1)
embedding1 = model(waveform1[None])

# extract embedding for a speaker speaking between t=7s and t=12s
speaker2 = Segment(7., 12.)
waveform2, sample_rate = audio.crop(audio_file_path, speaker2)
embedding2 = model(waveform2[None])

# compare embeddings using "cosine" distance
from scipy.spatial.distance import cdist
distance = cdist(embedding1, embedding2, metric="cosine")
print(embedding1)
#print(distance,embedding1,embedding2)