---
license: cc-by-4.0
language:
  - en
library_name: moshi
tags:
  - audio
  - automatic-speech-recognition
---
# Model Card for Kyutai STT

**Transformers support 🤗:** Starting with `transformers >= 4.53.0` and above, you can now run Kyutai STT natively!
👉 Check it out here: [kyutai/stt-2.6b-en-trfs](https://huggingface.co/kyutai/stt-2.6b-en-trfs).

See also the [project page](https://kyutai.org/next/stt)
and the [GitHub repository](https://github.com/kyutai-labs/delayed-streams-modeling/).

This is a model for streaming speech-to-text (STT, also known as automatic speech recognition, ASR).
Unlike offline speech-to-text, where the model needs the entire audio to produce the transcript,
our model starts to output the transcript as soon as a few seconds of audio become available.

## Model Details

The model architecture is a Transformer that consumes audio tokenized by Mimi (see [the Moshi paper](https://arxiv.org/abs/2410.00037)) and outputs text tokens.
The frame rate is 12.5 Hz and each audio frame is represented by 32 audio tokens.

We release two models:
- `kyutai/stt-1b-en_fr`, an English and French model with ~1B parameters, a 0.5 second delay, and a [semantic VAD](https://kyutai.org/next/stt#semantic-vad).
- `kyutai/stt-2.6b-en`, an English-only model with ~2.6B parameters and a 2.5 second delay.

## Model Description

Kyutai STT is a decoder-only model for streaming speech-to-text.
It leverages the multistream architecture of [Moshi](https://moshi.chat/) to model text stream based on the speech stream.
The text stream is shifted w.r.t. the audio stream to allow the model to predict text tokens based on the input audio.

* Developed by: Kyutai
* Model type: Streaming Speech-to-Text transcription.
* Language(s) (NLP): English and French for `kyutai/stt-1b-en_fr`, English for `kyutai/stt-2.6b-en`
* License: Model weights are licensed under CC-BY 4.0
* Repository: [GitHub](https://github.com/kyutai-labs/delayed-streams-modeling/)

## Uses

### Direct Use

The model can be used for streaming speech-to-text.
It is robust to noisy conditions and was found to perform well with audio as long as 2 hours with no additonal changes.
The model produces transcripts with capitalization and punctuation.
The predicted text token timestamps can be recovered by subtracting the model's text stream offset (0.5 or 2.5 seconds) from the frame's offset.

## How to Get Started with the Model

See the [GitHub repository](https://github.com/kyutai-labs/delayed-streams-modeling/).

## Training Details

### Training Data

Pretraining stage: For both `kyutai/stt-2.6b-en` and `kyutai/stt-1b-en_fr`, we use an audio collection of 2.5 million hours of publicly available audio content.
For this dataset, we obtained synthetic transcripts by running [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped).

For `kyutai/stt-2.6b-en`:

- Finetuning stage: We then finetune the model on a collection of public datasets with
ground-truth transcripts. This dataset contains 24000 hours of audio.

- Long-form finetuning stage: Finally, we finetune the model on a combination of data from the previous stage and long-form audio.
The long-form audio is obtained from two sources: (a) concatenating LibriSpeech examples (1000 hours), (b) synthesizing dialogs (22000 hours).

For `kyutai/stt-1b-en_fr`:

- Finetuning stage: We finetune on the Fisher dataset of 2000 hours of English audio, plus proprietary data (1000 hours in English, 600 hours in French).

### Compute Infrastructure

Pretraining and finetuning was done with 48 and 16 H100 Nvidia GPUs, respectively.

## Model Card Authors

Neil Zeghidour, Eugene Kharitonov, Manu Orsini, Václav Volhejn, Gabriel de Marmiesse, Edouard Grave, Patrick Perez, Laurent Mazaré, Alexandre Défossez