# virtual-interpreter
AI solution to translate your voice messages into other languages - in your own voice! Try a web demo here - https://ffts.short.gy/ai-interpreter 

Only locally-runnable models, no calls to external APIs. After the models are downloaded, can be run completely offline.

This solution runs in a web-based interface created with the help of gradio package.

## Requirements:
This script is tested with the following configuration:
 - OS: Ubuntu 22.04 LTS / Linux Mint 21.3
 - Kernel: 5.15
 - NVIDIA driver version: 535
 - CUDA version: 12.2
 - GPUs: 2 x RTX 3080 / 1 x RTX 3060

## Used models:
 - multilingual speech recognition: [whisper](https://github.com/openai/whisper). From OpenAI but open source and runnable locally
 - translation: [argostranslate](https://github.com/argosopentech/argos-translate)
 - text-to-speech conversion and voice cloning: [coqui-TTS](https://github.com/coqui-ai/TTS). Keep in mind that the license only allows to use this model for free for non-commercial use, otherwise, a commercial license is required.

## Installation:
First, you need to install Anaconda (miniconda, to reduce the download size ):
```
sudo apt update && sudo apt upgrade -y
sudo apt install curl git ffmpeg  
curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" > "Miniconda3.sh"
chmod +x Miniconda3.sh
bash ./Miniconda3.sh
```
Log out and log back in. Then clone the repository via git run the following:
```
conda env create  --yes --file requirements.yml
```

## Running:
Activate the conda environment, then run the following script:
```
conda activate whisper
python load_language_packages.py
```

Keep in mind that downloading and installing all the required language models for Argos Translate will require about 10 minutes and several GB of disc space.

After that, within whisper environment, run:
```
python interpreting.py
```

Then open the browser at 127.0.0.1:7860 and it's ready to run locally. It can be also ran from within the local network, you just need to access the server by its local IP address (e.g. 192.168.0.100:7860).

## License
The code is released under MIT license. The models used are licensed under their respective licenses.
