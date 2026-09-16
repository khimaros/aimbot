---
license: mit
base_model:
- hexgrad/Kokoro-82M
pipeline_tag: text-to-speech
---
## Purpose

The purpose of this repository is to store various [TTS.cpp](https://github.com/mmwillet/TTS.cpp) compatible GGUF encoded model files for the [Kokoro TTS model](https://huggingface.co/hexgrad/Kokoro-82M).

### Model Types

Currently there are two types of model each with five levels of quantization. The GGUF model files containing `_espeak` are configured to expect and use espeak for phonemization and those containing `_no_espeak` support tts native phonemization. The GGUF model files with no quantization suffix (i.e. `Kokoro_espeak.gguf` and `Kokoro_no_espeak.gguf`) use only 32bit floating point precision and the GGUF model files with Q4, Q5, Q8, and F16 suffixes support Q4_0 quantization, Q5_0 quantization, Q8_0 quantization, and 16 bit floating point precision respectively. 

## Kokoro

This page only contains the GGUF encoded model files of the original Kokoro model. For the original model please see the repository [here](https://huggingface.co/hexgrad/Kokoro-82M).