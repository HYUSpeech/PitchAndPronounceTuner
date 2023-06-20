import tensorflow as tf
import tensorflow_hub as hub

import numpy as np
import matplotlib.pyplot as plt
import librosa
from librosa import display as librosadisplay

import logging
import math
import statistics
import sys

from IPython.display import Audio, Javascript
from scipy.io import wavfile

from base64 import b64decode

import music21
from pydub import AudioSegment

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

EXPECTED_SAMPLE_RATE = 16000
MAX_ABS_INT16 = 32768.0

class PitchDetection:
    def convert_audio_for_model(user_file, output_file='converted_audio_file.wav'):
        audio = AudioSegment.from_file(user_file)
        audio = audio.set_frame_rate(EXPECTED_SAMPLE_RATE).set_channels(1)
        audio.export(output_file, format="wav")
        return output_file

    def output2hz(pitch_output):
        # Constants taken from https://tfhub.dev/google/spice/2
        PT_OFFSET = 25.58
        PT_SLOPE = 63.07
        FMIN = 10.0
        BINS_PER_OCTAVE = 12.0
        cqt_bin = pitch_output * PT_SLOPE + PT_OFFSET
        return FMIN * 2.0 ** (1.0 * cqt_bin / BINS_PER_OCTAVE)    

    def hz2offset(C0,freq):
        # This measures the quantization error for a single note.
        if freq == 0:  # Rests always have zero error.
            return None
        # Quantized note.
        h = round(12 * math.log2(freq / C0))
        return 12 * math.log2(freq / C0) - h

    def quantize_predictions(group, ideal_offset, note_names, C0):
        # Group values are either 0, or a pitch in Hz.
        non_zero_values = [v for v in group if v != 0]
        zero_values_count = len(group) - len(non_zero_values)

        # Create a rest if 80% is silent, otherwise create a note.
        if zero_values_count > 0.8 * len(group):
            # Interpret as a rest. Count each dropped note as an error, weighted a bit
            # worse than a badly sung note (which would 'cost' 0.5).
            return 0.51 * len(non_zero_values), "Rest"
        else:
            # Interpret as note, estimating as mean of non-rest predictions.
            h = round(
                statistics.mean([
                    12 * math.log2(freq / C0) - ideal_offset for freq in non_zero_values
                ]))
            octave = h // 12
            n = h % 12
            note = note_names[n]
            # Quantization error is the total difference from the quantized note.
            error = sum([
                abs(12 * math.log2(freq / C0) - ideal_offset - h)
                for freq in non_zero_values
            ])
        return error, note


    def get_quantization_and_error(pitch_outputs_and_rests, predictions_per_eighth,
                                prediction_start_offset, ideal_offset, note_names, C0):
        # Apply the start offset - we can just add the offset as rests.
        pitch_outputs_and_rests = [0] * prediction_start_offset + \
                                    pitch_outputs_and_rests
        # Collect the predictions for each note (or rest).
        groups = [
            pitch_outputs_and_rests[i:i + predictions_per_eighth]
            for i in range(0, len(pitch_outputs_and_rests), predictions_per_eighth)
        ]

        quantization_error = 0

        notes_and_rests = []
        for group in groups:
            error, note_or_rest = PitchDetection.quantize_predictions(group, ideal_offset, note_names, C0)
            quantization_error += error
            notes_and_rests.append(note_or_rest)

        return quantization_error, notes_and_rests

    def detect_pitch(best_notes_and_rests):
        # At this point, best_notes_and_rests contains the best quantization.
        # Since we don't need to have rests at the beginning, let's remove these:
        while best_notes_and_rests[0] == 'Rest':
            best_notes_and_rests = best_notes_and_rests[1:]
        # Also remove silence at the end.
        while best_notes_and_rests[-1] == 'Rest':
            best_notes_and_rests = best_notes_and_rests[:-1]
        
        return best_notes_and_rests

# Creating the sheet music score.
# sc = music21.stream.Score()
# Adjust the speed to match the actual singing.
# bpm = 60 * 60 / best_predictions_per_note
# print ('bpm: ', bpm)
# a = music21.tempo.MetronomeMark(number=bpm)
# sc.insert(0,a)

# for snote in best_notes_and_rests:   
#     d = 'half'
#     if snote == 'Rest':      
#       sc.append(music21.note.Rest(type=d))
#     else:
#       sc.append(music21.note.Note(snote, type=d))

# rendering the music score