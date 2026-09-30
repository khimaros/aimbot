---
language:
  - en
library_name: nemo
datasets:
  - librispeech_asr
  - fisher_corpus
  - Switchboard-1
  - WSJ-0
  - WSJ-1
  - National-Singapore-Corpus-Part-1
  - National-Singapore-Corpus-Part-6
  - vctk
  - voxpopuli
  - europarl
  - multilingual_librispeech
  - mozilla-foundation/common_voice_8_0
  - MLCommons/peoples_speech
thumbnail: null
tags:
  - automatic-speech-recognition
  - speech
  - audio
  - CTC
  - FastConformer
  - Transformer
  - pytorch
  - NeMo
  - hf-asr-leaderboard
license: cc-by-4.0
widget:
  - example_title: Librispeech sample 1
    src: https://cdn-media.huggingface.co/speech_samples/sample1.flac
  - example_title: Librispeech sample 2
    src: https://cdn-media.huggingface.co/speech_samples/sample2.flac
model-index:
  - name: stt_en_fastconformer_transducer_large
    results:
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech (clean)
          type: librispeech_asr
          config: clean
          split: test
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 2.1
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech (other)
          type: librispeech_asr
          config: other
          split: test
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 4.2
      - task:
          type: Automatic Speech Recognition
          name: automatic-speech-recognition
        dataset:
          name: Multilingual LibriSpeech
          type: facebook/multilingual_librispeech
          config: english
          split: test
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 6.4
      - task:
          type: Automatic Speech Recognition
          name: automatic-speech-recognition
        dataset:
          name: Mozilla Common Voice 7.0
          type: mozilla-foundation/common_voice_7_0
          config: en
          split: test
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 8.3
      - task:
          type: Automatic Speech Recognition
          name: automatic-speech-recognition
        dataset:
          name: Wall Street Journal 92
          type: wsj_0
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 1.6
      - task:
          type: Automatic Speech Recognition
          name: automatic-speech-recognition
        dataset:
          name: Wall Street Journal 93
          type: wsj_1
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 2.5
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: National Singapore Corpus
          type: nsc_part_1
          split: test
          args:
            language: en
        metrics:
          - name: Test WER
            type: wer
            value: 6.3


---

# NVIDIA FastConformer-CTC Large (en)

<style>
img {
 display: inline;
}
</style>

| [![Model architecture](https://img.shields.io/badge/Model_Arch-FastConformer--CTC-lightgrey#model-badgee)](#model-architecture)
| [![Model size](https://img.shields.io/badge/Params-115M-lightgrey#model-badge)](#model-architecture)
| [![Language](https://img.shields.io/badge/Language-en-lightgrey#model-badge)](#datasets)


This model transcribes speech in lower case English alphabet.
It is a "large" version of FastConformer CTC (around 115M parameters) model.
See the [model architecture](#model-architecture) section and [NeMo documentation](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/models.html#fast-conformer) for complete architecture details.

## NVIDIA NeMo: Training

To train, fine-tune or play with the model you will need to install [NVIDIA NeMo](https://github.com/NVIDIA/NeMo). We recommend you install it after you've installed latest Pytorch version.
```
pip install nemo_toolkit['all']
``` 

## How to Use this Model

The model is available for use in the NeMo toolkit [3], and can be used as a pre-trained checkpoint for inference or for fine-tuning on another dataset.

### Automatically instantiate the model

```python
import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="nvidia/stt_en_fastconformer_ctc_large")
```

### Transcribing using Python
First, let's get a sample
```
wget https://dldata-public.s3.us-east-2.amazonaws.com/2086-149220-0033.wav
```
Then simply do:
```
output = asr_model.transcribe(['2086-149220-0033.wav'])
print(output[0].text)
```

### Transcribing many audio files

```shell
python [NEMO_GIT_FOLDER]/examples/asr/transcribe_speech.py 
 pretrained_name="nvidia/stt_en_fastconformer_ctc_large" 
 audio_dir="<DIRECTORY CONTAINING AUDIO FILES>"
```

### Input

This model accepts 16000 Hz Mono-channel Audio (wav files) as input.

### Output

This model provides transcribed speech as a string for a given audio sample.

## Model Architecture

FastConformer [1] is an optimized version of the Conformer model with 8x depthwise-separable convolutional downsampling. The model is trained in a multitask setup with a Transducer decoder loss. You may find more information on the details of FastConformer here: [Fast-Conformer Model](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/models.html#fast-conformer).

## Training

The NeMo toolkit [3] was used for training the models for over several hundred epochs. These model are trained with this [example script](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/asr_ctc/speech_to_text_ctc_bpe.py) and this [base config](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/conf/fastconformer/fast-conformer_ctc_bpe.yaml).

The tokenizers for these models were built using the text transcripts of the train set with this [script](https://github.com/NVIDIA/NeMo/blob/main/scripts/tokenizers/process_asr_text_tokenizer.py).

### Datasets

The model in this collection is trained on a composite dataset (NeMo ASRSet En) comprising several thousand hours of English speech:

- Librispeech 960 hours of English speech
- Fisher Corpus
- Switchboard-1 Dataset
- WSJ-0 and WSJ-1
- National Speech Corpus (Part 1, Part 6)
- VCTK
- VoxPopuli (EN)
- Europarl-ASR (EN)
- Multilingual Librispeech (MLS EN) - 2,000 hrs subset
- Mozilla Common Voice (v7.0)
- People's Speech  - 12,000 hrs subset

## Performance

The performance of Automatic Speech Recognition models is measuring using Word Error Rate. Since this dataset is trained on multiple domains and a much larger corpus, it will generally perform better at transcribing audio in general.

The following tables summarizes the performance of the available models in this collection with the Transducer decoder. Performances of the ASR models are reported in terms of Word Error Rate (WER%) with greedy decoding. 

|**Version**|**Tokenizer**|**Vocabulary Size**|**LS test-other**|**LS test-clean**|**WSJ Eval92**|**WSJ Dev93**|**NSC Part 1**|**MLS Test**|**MCV Test 7.0**| Train Dataset |
|---------|-----------------------|-----------------|---------------|---------------|------------|-----------|-----|-------|------|------|
| 1.18.0 | SentencePiece Unigram | 1024 | 4.2 | 2.1 | 1.6 | 2.5 | 6.3 | 6.4 | 8.3 | NeMo ASRSET 3.0 |


## Limitations
Since this model was trained on publically available speech datasets, the performance of this model might degrade for speech which includes technical terms, or vernacular that the model has not been trained on. The model might also perform worse for accented speech.

## NVIDIA Riva: Deployment

[NVIDIA Riva](https://developer.nvidia.com/riva), is an accelerated speech AI SDK deployable on-prem, in all clouds, multi-cloud, hybrid, on edge, and embedded. 
Additionally, Riva provides: 

* World-class out-of-the-box accuracy for the most common languages with model checkpoints trained on proprietary data with hundreds of thousands of GPU-compute hours 
* Best in class accuracy with run-time word boosting (e.g., brand and product names) and customization of acoustic model, language model, and inverse text normalization 
* Streaming speech recognition, Kubernetes compatible scaling, and enterprise-grade support 

Although this model isn’t supported yet by Riva, the [list of supported models is here](https://huggingface.co/models?other=Riva).  
Check out [Riva live demo](https://developer.nvidia.com/riva#demos). 

## References
[1] [Fast Conformer with Linearly Scalable Attention for Efficient Speech Recognition](https://arxiv.org/abs/2305.05084)

[2] [Google Sentencepiece Tokenizer](https://github.com/google/sentencepiece)

[3] [NVIDIA NeMo Toolkit](https://github.com/NVIDIA/NeMo)

## Licence

License to use this model is covered by the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). By downloading the public and release version of the model, you accept the terms and conditions of the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) license.
