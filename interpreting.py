# -*- coding: utf-8 -*-

import whisper
import argostranslate.package
import argostranslate.translate
import getpass

import torch
from TTS.api import TTS

import gradio as gr

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

def translation(audio_path, from_, to_):
    global whisper_model   
    global tts_sg
    global path
    
    language_codes = {"Russian": "ru",
                       "English": "en",
                       "French": "fr",
                       "German": "de",
                       "Spanish": "es",
                       "Italian": "it",
                       "Chinese": "zh"}
    
    from_code = language_codes[from_]
    to_code = language_codes[to_]
    
    # Translate
    result = whisper_model.transcribe(audio_path)["text"]
    translated_text = argostranslate.translate.translate(result, from_code, to_code)

    # Speech generation:
    tts_sg.tts_to_file(text = translated_text, speaker_wav = audio_path, language = to_code, file_path = path + "generated.wav")

    # Remove temp file and source file:
    # os.remove(audio_path + ".wav")
    # os.remove(audio_path)

    return path + "generated.wav"



whisper_model, tts_sg = load_models()

demo = gr.Interface(fn=translation,
             inputs = [gr.Audio(sources =["microphone"], type = "filepath"),
                        gr.Dropdown(["Russian", 
                                     "English", 
                                     "French", 
                                     "German", 
                                     "Spanish", 
                                     "Italian", 
                                     "Chinese"],
                         label = "Input language", info = "Select input language"),

                         gr.Dropdown(["Russian", 
                                     "English", 
                                     "French", 
                                     "German", 
                                     "Spanish", 
                                     "Italian", 
                                     "Chinese"],
                         label = "Output language", info = "Select output language")],
             outputs = "audio"  
            )
#mobile browsers do not allow microphone access to websites without SSL (even within the local network)
#so, if you want to use the tool from your phone, generate an SSL certificate and put the certificate files to your path
demo.launch(server_name = "0.0.0.0"
            ssl_certfile=path + "cert.pem",
            ssl_keyfile=path+"key.pem",
            ssl_verify=False)
#for sharing via gradio:
#demo.launch(share = True)
