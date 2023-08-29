import torch
from pyannote.audio import Audio
from pyannote.core import Segment
from scipy.spatial.distance import cdist
import numpy as np
def getEmbeddings(GlobalVariables,filepath,audioparms):
    '''
    This function diarize the input audio present at filepath
    input:
        GlobalVariables: GlobalVariabls requried to connect to model Pipeline
        filepath: path where audio file is present.
        audioparms: list of audio file parameters recieved after speaker diarization
    output:
        returns embedding as output
    '''
    return_data = []
    for audioparm in audioparms:
        speaker = Segment(audioparm['time'][0], audioparm['time'][1])
        waveform, sample_rate = GlobalVariables.audio_config.crop(filepath, speaker)
        embedding = GlobalVariables.embedding_model(waveform[None])
        print(embedding,type(embedding))
        audioparm['embedding'] = str(embedding)
        return_data.append(audioparm)
    return return_data

def getSimilarEmbedding(src_embeding,embedding_list,threshold=0.1):
    distance_list = []
    for embedding in embedding_list:
        distance = cdist(src_embedding, embedding, metric="cosine")
        distance_list.append(distance)
    return distance_list.index(min(distance_list))
