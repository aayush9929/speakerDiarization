import wave
import os
import time
import shutil
from pydub import AudioSegment
import base64

def save_m4a_audio_file_base64(binary_audio_string,audio_output_folder):
    '''
        This functions takes audio as base64 audio of "m4a" format and saves it in "wav" format
        input:
            binary_audio_string Audio in binary format
            audio_output_folder Output folder where the audio would be stored as out_temp.m4a
        return:
            It returns path where the audio file is saved.
    '''
    output_wav_path = audio_output_folder + '/out_temp.m4a'
    with open(output_wav_path,'wb') as wave_file:
        decode_string = base64.b64decode(binary_audio_string)
        wave_file.write(decode_string)
    audio = AudioSegment.from_file(output_wav_path, format="m4a")
	# Convert M4A to WAV
    output_wav_path = audio_output_folder + '/out_temp.wav'
    audio.export(output_wav_path, format="wav")
    return output_wav_path

def save_m4a_audio_file(binary_audio,audio_output_folder):
    '''
        This functions takes audio as binary audio of "m4a" format and saves it in "wav" format
        input:
            binary_audio_string Audio in binary format
            audio_output_folder Output folder where the audio would be stored as out_temp.m4a
        return:
            It returns path where the audio file is saved.
    '''
    output_wav_path = audio_output_folder + '/out_temp.m4a'
    with open(output_wav_path,'wb') as wave_file:
        wave_file.write(binary_audio)
    audio = AudioSegment.from_file(output_wav_path, format="m4a")
	# Convert M4A to WAV
    output_wav_path = audio_output_folder + '/out_temp.wav'
    audio.export(output_wav_path, format="wav")
    return output_wav_path

def save_audio_file(binary_audio,audio_output_folder):
    '''
        This functions takes audio as binary audio of "wav" format and saves it in "wav" format
        input:
            binary_audio_string Audio in binary format
            audio_output_folder Output folder where the audio would be stored as out_temp.m4a
        return:
            It returns path where the audio file is saved.
    '''
    output_wav_path = audio_output_folder + '/out_temp.wav'
    with open(output_wav_path,'wb') as wave_file:
        wave_file.write(binary_audio)
        #num_channels = int(params.get('num_channels'))
        #sample_width = int(params.get('sample_width'))
        #frame_rate = int(params.get('frame_rate'))
        #print(num_channels,sample_width,frame_rate)
        #wave_file.setnchannels(num_channels)
        #wave_file.setsampwidth(sample_width)
        #wave_file.setframerate(frame_rate)
        #wave_file.writeframes(audio_file)
    return output_wav_path

def save_mp3_audio_file_base64(binary_audio_string,audio_output_folder):
    '''
        This functions takes audio as base64 audio of "mp3" format and saves it in "wav" format
        input:
            binary_audio_string Audio in binary format
            audio_output_folder Output folder where the audio would be stored as out_temp.m4a
        return:
            It returns path where the audio file is saved.
    '''
    output_wav_path = audio_output_folder + '/out_temp.mp3'
    with open(output_wav_path,'wb') as wave_file:
        decode_string = base64.b64decode(binary_audio_string)
        wave_file.write(decode_string)
    # audio = AudioSegment.from_file(output_wav_path, format="m4a")
    audio = AudioSegment.from_mp3(output_wav_path) 
    # sound.export(output_file, format="wav")
	# Convert M4A to WAV
    output_wav_path = audio_output_folder + '/out_temp.wav'
    audio.export(output_wav_path, format="wav")
    return output_wav_path
