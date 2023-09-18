from flask import request
from flask import Flask
from pyannote.audio import Pipeline
from flask import jsonify
import wave,os
import whisper
import time
import shutil
import base64
from .utils.SaveFile import *
from .utils.AudioOps import *
from .utils.EmbeddingOps import *
import logging
import json
import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)

class GlobalVariables:
    init_done = False
    pipeline = None
    whisper_model = None
    embedding_model = None
    audio_config = None

def initializeGlobalVars():
    if not GlobalVariables.init_done:
        fptr = open('config/config.json')
        configs = json.load(fptr)
        app.logger.info('accesing pipeline from hugging face....')
        pipeline = Pipeline.from_pretrained(configs['diarization_model_name'],use_auth_token=configs['access_token'])
        model = whisper.load_model(configs['diarization_model_type'])
        GlobalVariables.pipeline = pipeline
        GlobalVariables.whisper_model = model
        GlobalVariables.init_done = True
        GlobalVariables.embedding_model = PretrainedSpeakerEmbedding(configs['embedding_model_name'])
        GlobalVariables.audio_config = Audio(sample_rate=16000, mono="downmix")

@app.route('/test_api',methods=['GET','POST'])
def test_api():
    initializeGlobalVars()
    return "I am live!"

@app.route('/speech-to-text/pyannote-service',methods = ['POST'])
def extract_speaker_time():
    try:
        initializeGlobalVars()
        audio_file = request.files['audio'].read()
        app.logger.info(f'Type of audio file recieved {type(audio_file)}')
        audio_output_folder = str(round(time.time()))
        os.mkdir(audio_output_folder)
        output_wav_path = save_audio_file(audio_file,audio_output_folder)
        diarizeaudio_result = diarizeAudio(GlobalVariables,output_wav_path)
        shutil.rmtree(audio_output_folder)
        return jsonify(diarizeaudio_result)
    except:
        if os.path.exists(audio_output_folder):
            shutil.rmtree(audio_output_folder)


@app.route('/speech-to-text/whisper-service',methods=['POST'])
def text_to_speech():
    try:
        initializeGlobalVars()
        audio_file = request.files['audio'].read()
        app.logger.info(f'Type of audio file recieved {type(audio_file)}')
        audio_output_folder = str(round(time.time()))
        os.mkdir(audio_output_folder)
        output_file_path_i = save_audio_file(audio_file,audio_output_folder)
        result = GlobalVariables.whisper_model.transcribe(output_file_path_i,task="transcribe", language="en")
        return_data = {'text' : result['text']}
        shutil.rmtree(audio_output_folder)
        return jsonify(return_data)
    except:
        if os.path.exists(audio_output_folder):
            shutil.rmtree(audio_output_folder)

@app.route('/speech-to-text/whisper-pyannote-service-m4a',methods = ['POST'])
def extract_speakers_speech_m4a(internal=False,req=None,return_embedding=False):
    try:
        initializeGlobalVars()
        audio_file = request.files['audio'].read()
        app.logger.info(f'Type of audio file recieved {type(audio_file)}')
        audio_output_folder = str(round(time.time()))
        os.mkdir(audio_output_folder)
        output_file_path_i = save_m4a_audio_file(audio_file,audio_output_folder)
        diarized_data = diarizeAudio(GlobalVariables,output_file_path_i)
        return_data = extract_text(GlobalVariables,diarized_data,output_file_path_i,audio_output_folder)
        if return_embedding == True:
            return_data = getEmbeddings(GlobalVariables,output_file_path_i,return_data)
        shutil.rmtree(audio_output_folder)
        return jsonify(return_data)
    except:
        if os.path.exists(audio_output_folder):
            shutil.rmtree(audio_output_folder)

@app.route('/speech-to-text/whisper-pyannote-service-m4a-body',methods = ['POST'])
def extract_speakers_speech_m4a_body(internal=False,req=None,return_embedding=False):
    try:
        initializeGlobalVars()
        print(request.json['audio'])
        audio_file = request.json['audio']
        # print(audio_file)
        app.logger.info(f'Type of audio file recieved {type(audio_file)}')
        audio_output_folder = str(round(time.time()))
        os.mkdir(audio_output_folder)
        output_file_path_i = save_m4a_audio_file_base64(audio_file,audio_output_folder)
        diarized_data = diarizeAudio(GlobalVariables,output_file_path_i)
        return_data = extract_text(GlobalVariables,diarized_data,output_file_path_i,audio_output_folder)
        if return_embedding == True:
            return_data = getEmbeddings(GlobalVariables,output_file_path_i,return_data)
        # shutil.rmtree(audio_output_folder)
        return jsonify(return_data)
    except Exception as e:
        print(e)
        if os.path.exists(audio_output_folder):
            shutil.rmtree(audio_output_folder)

# @app.route('/speech-to-text/whisper-pyannote-service',methods = ['POST'])
# def extract_speakers_speech(internal=False,req=None,return_embedding=False):
#     try:
#         initializeGlobalVars()
#         audio_file = request.files['audio'].read()
#         app.logger.info(f'Type of audio file recieved {type(audio_file)}')
#         audio_output_folder = str(round(time.time()))
#         os.mkdir(audio_output_folder)
#         output_file_path_i = save_audio_file(audio_file,audio_output_folder)
#         diarized_data = diarizeAudio(GlobalVariables,output_file_path_i)
#         return_data = extract_text(GlobalVariables,diarized_data,output_file_path_i,audio_output_folder)
#         # app.logger.info(return_data)
#         if return_embedding == True:
#             return_data = getEmbeddings(GlobalVariables,output_file_path_i,return_data)
#         shutil.rmtree(audio_output_folder)
#         return jsonify(return_data)
#     except:
#         if os.path.exists(audio_output_folder):
#             shutil.rmtree(audio_output_folder)

# @app.route('/speech-to-text/embedding-whisper-pyannote-service',methods = ['POST'])
# def extract_speakers_speech_embedding():
#     return extract_speakers_speech(return_embedding=True)

# @app.route('/speech-to-text/embedding-whisper-pyannote-service-m4a-body',methods = ['POST'])
# def extract_speakers_speech_m4a_body_embedding():
#     return extract_speakers_speech_m4a_body(return_embedding=True)

@app.route('/diarization-transcription-embedding-binary',methods = ['POST'])
def extract_speakers_speech_m4a_embedding_binary():
    return extract_speakers_speech_m4a_body(return_embedding=True)

@app.route('/diarization-transcription-embedding',methods = ['POST'])
def extract_speakers_speech_m4a_embedding():
    return extract_speakers_speech_m4a(return_embedding=True)

@app.route('/speech-to-text/speaker-comparison',methods = ['POST'])
def get_matching_embedding():
    embd_list = request.json['list_of_embeddings']
    embd = request.json['user_embedding']
    return jsonify(getSimilarEmbedding(embd,embd_list))

def main():
    # global pipeline
    initializeGlobalVars()
    return app
    # app.run(port=int(os.environ.get("PORT", 8080)),host="0.0.0.0")
