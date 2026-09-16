---
license: apache-2.0
language:
- ja
library_name: nemo
tags:
  - automatic-speech-recognition
  - NeMo
---

# reazonspeech-nemo-v2

`reazonspeech-nemo-v2` is an automatic speech recognition model trained
on [ReazonSpeech v2.0 corpus](https://huggingface.co/datasets/reazon-research/reazonspeech).

This model supports inference of long-form Japanese audio clips up to
several hours.

## Model Architecture

The model features an improved Conformer architecture from
[Fast Conformer with Linearly Scalable Attention for Efficient
Speech Recognition](https://arxiv.org/abs/2305.05084).

* Subword-based RNN-T model. The total parameter count is 619M.

* Encoder uses [Longformer](https://arxiv.org/abs/2004.05150) attention
  with local context size of 256, and has a single global token.

* Decoder has a vocabulary space of 3000 tokens constructed by
  [SentencePiece](https://github.com/google/sentencepiece)
  unigram tokenizer.

We trained this model for 1 million steps using AdamW optimizer
following Noam annealing schedule.

## Usage

We recommend to use this model through our
[reazonspeech](https://github.com/reazon-research/reazonspeech)
library.

```
from reazonspeech.nemo.asr import load_model, transcribe, audio_from_path

audio = audio_from_path("speech.wav")
model = load_model()
ret = transcribe(model, audio)
print(ret.text)
```

## License

[Apaceh Licence 2.0](https://choosealicense.com/licenses/apache-2.0/)
