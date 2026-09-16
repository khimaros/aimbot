---
license: mit
library_name: magpie.cpp
datasets:
- Hi-FiTTS
- HiFiTTS-2
- LibriTTS
- CML-TTS
- LSVSC
- InfoRe
thumbnail: null
tags:
- ggml
- text-to-speech
- tts
- speech-synthesis
- speech
- audio
- transformer
- NeMo
- multilingual
language:
- en
- es
- de
- fr
- vi
- it
- zh
model-index:
- name: magpie-tts-multilingual-357m
  results:
  - task:
      name: Text-to-Speech
      type: text-to-speech
    dataset:
      name: LibriTTS test-clean
      type: librispeech_asr
      config: clean
      split: test
    metrics:
    - name: CER
      type: cer
      value: 0.38
    - name: Speaker Similarity
      type: speaker-similarity
      value: 0.823
  - task:
      name: Text-to-Speech
      type: text-to-speech
    dataset:
      name: CML-TTS Spanish
      type: cml-tts
      config: es
      split: test
    metrics:
    - name: CER
      type: cer
      value: 1.0
    - name: Speaker Similarity
      type: speaker-similarity
      value: 0.719
  - task:
      name: Text-to-Speech
      type: text-to-speech
    dataset:
      name: CML-TTS French
      type: cml-tts
      config: fr
      split: test
    metrics:
    - name: CER
      type: cer
      value: 2.8
    - name: Speaker Similarity
      type: speaker-similarity
      value: 0.708
  - task:
      name: Text-to-Speech
      type: text-to-speech
    dataset:
      name: CML-TTS German
      type: cml-tts
      config: de
      split: test
    metrics:
    - name: CER
      type: cer
      value: 1.1
    - name: Speaker Similarity
      type: speaker-similarity
      value: 0.646
metrics:
- cer
pipeline_tag: text-to-speech
---

## Magpie TTS GGUF quantization

Derivative of: https://huggingface.co/nvidia/magpie_tts_multilingual_357m

## magpie.cpp

To use these quantizations, you will need the ggml port of Magpie TTS, found here: https://github.com/m1el/magpie.cpp

## Model Architecture

- **Text Encoder**: 6 causal transformer layers, d=768, 12 heads
- **Decoder**: 12 transformer layers with cross-attention, d=768, 12 SA heads + 1 XA head
- **Local Transformer**: 1 layer, d=256, autoregressive over 8 codebooks
- **Audio Codec**: HiFiGAN decoder with FSQ (Finite Scalar Quantization)
- **Output**: 22050 Hz mono audio

## Speakers

| ID | Name |
|----|------|
| 0 | John |
| 1 | Sofia |
| 2 | Aria |
| 3 | Jason |
| 4 | Leo |

## Languages

English (en), Spanish (es), German (de), French (fr), Vietnamese (vi), Italian (it), Mandarin Chinese (zh)

## Quantization

For conversion script, see https://github.com/m1el/magpie.cpp/blob/master/scripts/convert_magpie_to_gguf.py

| Format | Size | Notes |
|--------|------|-------|
| F32 | 858 MB | Full precision |
| Q8_0 | 679 MB | 8-bit quantized |

## Benchmark

|                       | CER (%) | Speaker Similarity |
| --------------------- | ------- | ------------------ |
| LibriTTS test-clean   | 0.38    | 0.823              |
| Spanish CML           | 1.0     | 0.719              |
| French CML            | 2.8     | 0.708              |
| German CML            | 1.1     | 0.646              |

## License

The MIT License

Copyright 2025

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Licensed by NVIDIA Corporation under the NVIDIA Open Model License

https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
