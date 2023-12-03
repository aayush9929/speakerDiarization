from pydub import AudioSegment
import wave,os
import whisper
import time
import shutil
import base64

def diarizeAudio(GlobalVariables,filepath):
    '''
    This function diarize the input audio present at filepath
    input:
        GlobalVariables: GlobalVariabls requried to connect to model Pipeline
        filepath: path where audio file is present.
    output:
        returns output in format {[speaker,start_time,end_time],..}
    '''
    return_data = []
    diarization = GlobalVariables.pipeline(filepath)
    for turn,_,speaker in diarization.itertracks(yield_label=True):
        temp = []
        temp.append(speaker)
        temp.append(round(turn.start))
        temp.append(round(turn.end))
        return_data.append(temp)
    return return_data

def extract_text(GlobalVariables,timedetails,filepath,outputfolder):
    '''
    This function extract audio from text use OpenAI
    input:
        GlobalVariables: GlobalVariabls requried to connect to model Pipeline.
        timedetails: containes list of [[audio_1_start_time, audio_1_end_time],..]
        filepath: path where audio file is present.
        outputfolder: path to store tempraroy file
    output:
        returns output in format 'speaker':spkr,'text':result['text']}
    '''
    idx = 0
    audio = AudioSegment.from_file(filepath)
    return_data = []
    for timedetail in timedetails:
        spkr = timedetail[0] #['speaker'][idx]
        start = timedetail[1] #['start'][idx]
        end = timedetail[2] #['end'][idx]
        if start >= end:
            continue
        segment = audio[start*1000:end*1000]
        output_file_path_i = f"{outputfolder}/tmp_file_{idx}.wav"
        segment.export(output_file_path_i, format='wav')
        result = GlobalVariables.whisper_model.transcribe(output_file_path_i,task="transcribe", language="en")
        return_data.append({'speaker':spkr,'text':result['text'],'time':[timedetail[1],timedetail[2]]})
    return return_data
