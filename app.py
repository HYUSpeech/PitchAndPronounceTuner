import os

import torch
import torch.nn as nn
import torchaudio


import librosa
import librosa.display

import numpy as np
import speech_recognition as sr
import matplotlib.pyplot as plt
import IPython.display as ipd

from GetSpeech import get_speech
from flask import Flask, render_template, request, redirect
from torch import Tensor

from sp_recog import *
from pcm2wav import *
from pitch_detection import *
from metric import *

'''
FLASK_ENV=development FLASK_APP=pythonProject1 flask run
'''

def parser(signal, audio_extension: str = 'pcm') -> Tensor:

    feature = torchaudio.compliance.kaldi.fbank(
        waveform=Tensor(signal).unsqueeze(0),
        num_mel_bins=80,
        frame_length=20,
        frame_shift=10,
        window_type='hamming'
    ).transpose(0, 1).numpy()

    feature -= feature.mean()
    feature /= np.std(feature)

    return torch.FloatTensor(feature).transpose(0, 1)

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():  # put application's code here

    ### SETUP ###
    sec = 1
    sr = 16000 #16000
    detect_note = []
    ori_note = []

    data_path = '/Users/seyunahn/Downloads/pythonProject1/recog_data'
    pitch_path = '/Users/seyunahn/Downloads/pythonProject1/pitch_data'

    song = 'stars'
    data_name = 'sample6'

    with open(os.path.join(pitch_path, song+'.txt')) as f:
        lines = f.read()
        first_line = lines.split('\n', 1)[0]
    lines_list = []
    for k in range(len(lines)):
        lines_list.append(lines[k])
    ### PCM2WAV ###
    # convert = Pcm2Wav
    # pcm_bytes = Path(os.path.join(data_path, data_name + '.pcm')).read_bytes()
    # wav_bytes = convert.make_wav_format(pcm_bytes, 1)
    # with open(os.path.join(convert_path, data_name + '.wav'), 'wb') as file:
    #     file.write(wav_bytes)

    uploaded_file_name = os.path.join(data_path, data_name + '.wav')

    ### PITCH DETECTION ###
    pitch_d = PitchDetection

    converted_audio_file = pitch_d.convert_audio_for_model(uploaded_file_name)

    sample_rate, audio_samples = wavfile.read(converted_audio_file, 'rb')

    audio_samples = audio_samples / float(MAX_ABS_INT16)

    model = hub.load("https://tfhub.dev/google/spice/2")

    # We now feed the audio to the SPICE tf.hub model to obtain pitch and uncertainty outputs as tensors.
    model_output = model.signatures["serving_default"](tf.constant(audio_samples, tf.float32))

    pitch_outputs = model_output["pitch"]
    uncertainty_outputs = model_output["uncertainty"]

    # 'Uncertainty' basically means the inverse of confidence.
    confidence_outputs = 1.0 - uncertainty_outputs

    confidence_outputs = list(confidence_outputs)
    pitch_outputs = [ float(x) for x in pitch_outputs]

    indices = range(len (pitch_outputs))
    confident_pitch_outputs = [ (i,p)  
    for i, p, c in zip(indices, pitch_outputs, confidence_outputs) if  c >= 0.9  ]
    confident_pitch_outputs_x, confident_pitch_outputs_y = zip(*confident_pitch_outputs)

    confident_pitch_values_hz = [ pitch_d.output2hz(p) for p in confident_pitch_outputs_y ]

    pitch_outputs_and_rests = [
        pitch_d.output2hz(p) if c >= 0.9 else 0
        for i, p, c in zip(indices, pitch_outputs, confidence_outputs)
    ]

    A4 = 440
    C0 = A4 * pow(2, -4.75)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # The ideal offset is the mean quantization error for all the notes
    # (excluding rests):
    offsets = [pitch_d.hz2offset(C0, p) for p in pitch_outputs_and_rests if p != 0]
    # print("offsets: ", offsets)

    ideal_offset = statistics.mean(offsets)
    # print("ideal offset: ", ideal_offset)
    
    best_error = float("inf")
    best_notes_and_rests = None
    best_predictions_per_note = None

    for predictions_per_note in range(20, 65, 1):
        for prediction_start_offset in range(predictions_per_note):

            error, notes_and_rests = pitch_d.get_quantization_and_error(
                pitch_outputs_and_rests, predictions_per_note,
                prediction_start_offset, ideal_offset, note_names, C0)

            if error < best_error:      
                best_error = error
                best_notes_and_rests = notes_and_rests
                best_predictions_per_note = predictions_per_note

    detect_note = pitch_d.detect_pitch(best_notes_and_rests)
    print(len(detect_note))
    if len(detect_note) > 7:
        detect_note = detect_note[0:7]
    detect_pitch_txt = ' '.join(detect_note)
    origin_pitch = ' '.join(lines_list)
    ### SPEECH RECOGNITION  ###
    speech_recog = SpeechRecognition
    origin_txt = '반짝반짝 작은별'

    ### PRONOUNCIATION ###
    pronoun_text = speech_recog.recognition(uploaded_file_name)
    print(pronoun_text)

    ### EVALUATION METRIC-PITCH ###
    metric_p = PitchMetric
    for i in range(len(lines)):
        ori_note = lines[i]
        pitch_score = metric_p.pitch_metric_eval(ori_note, detect_note)

    ### EVALUATION METRIC-PITCH ###
    metric_t = PronounMetric
    pronoun_score = metric_t.pronoun_metric_eval(origin_txt, pronoun_text)
    
    return render_template('index.html', co_pitch_text=origin_pitch, co_pronoun_text = origin_txt, pronoun_text = pronoun_text, pitch_text = detect_pitch_txt, pitch_score = str(pitch_score), pronoun_score = str(pronoun_score))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)