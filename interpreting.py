# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import whisper
import argostranslate.package
import argostranslate.translate
import time
import os
import getpass

import torch
from TTS.api import TTS

from pydub import AudioSegment

#adjust if appropriate:
path = "/home/" + getpass.getuser() + "/"

#load whisper for speech recognition and Coqui for voice conversion:
def load_models():

    #chech CUDA availability and number of cuda devices:
    cuda_devices = torch.cuda.device_count()

    #whisper initialize

    if cuda_devices > 1:
        device_whisper = "cuda:1" 
    elif cuda_devices == 1:
        device_whisper = "cuda"
    else:
        device_whisper = "cpu" 

    whisper_model = whisper.load_model("large-v3", device=device_whisper)

    #TTS voice conversion initialize:
    if cuda_devices > 1:
        device_tts = "cuda:0" 
    elif cuda_devices == 1:
        device_tts = "cuda"
    else:
        device_tts = "cpu"
        

    #TTS speech generation initialize:
    tts_sg = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device_tts)
    
    return whisper_model, tts_sg

def translation(whisper_model, tts_sg, audio_path = "/home/ubuntu/audio_test.mp3", from_code = "ru", to_code = "en"):
    #do not download all models for argostranslate at once
    #download and install only the ones that are required, if not yet installed
    #download and install Argos Translate package if not installed:
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages))
    argostranslate.package.install_from_path(package_to_install.download())

    #convert mp3 to wav:
    AudioSegment.from_mp3(audio_path).export(audio_path + ".wav")
    # Translate
    result = whisper_model.transcribe(audio_path + ".wav")["text"]
    translated_text = argostranslate.translate.translate(result, from_code, to_code)

    # Speech generation:
    tts_sg.tts_to_file(text = translated_text, speaker_wav = audio_path + ".wav", language = to_code, file_path = path + "generated.wav")

    # Remove temp file and source file:
    os.remove(audio_path + ".wav")
    # os.remove(audio_path)

    return path + "generated.wav"



whisper_model, tts_sg = load_models()

while True:
    audio_path = input('''Input full path for the file name in mp3 format. Press Enter if you want default (/home/ubuntu/audio_test.mp3)''')
    if audio_path == "":
        audio_path = "/home/ubuntu/audio_test.mp3"
    
    from_code = input('''Input the source language, in ISO 639 format (https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes). Press Enter if you want default (Russian)''')
    if from_code == "":
        from_code = "ru"
    
    to_code = input('''Input the source language, in ISO 639 format (https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes). Press Enter if you want default (English)''')
    if to_code == "":
        to_code = "en"
    
    output = translation(whisper_model, tts_sg, audio_path, from_code, to_code)

    print("Done. Find the output audio file at " + output + "\n\n")

