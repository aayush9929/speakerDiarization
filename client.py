# from email.mime import audio
from urllib import response
import wave,requests

url = 'http://34.173.218.51:65534/speech-to-text/whisper-pyannote-service'

audio_file_path = r'C:\Users\user\Documents\New folder\sample_audio_1.wav'

with wave.open(audio_file_path,'rb') as wav_file:
    num_channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    frame_rate = wav_file.getframerate()
    params = {'num_channels':num_channels,'sample_width':sample_width,'frame_rate':frame_rate}
    # files = {'audio':wav_file}
with open(audio_file_path,'rb') as f:
    files = {'audio':f.read()}
    print(type(files['audio']))
response = requests.post(url,files=files,data=params,timeout=10**6)
print(response)
print(response.text)