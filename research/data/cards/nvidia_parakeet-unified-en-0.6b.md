---
license: other
license_name: nvidia-open-model-license
license_link: >-
  https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
library_name: nemo
datasets:
  - nvidia/Granary
  - YTC
  - Yodas2
  - LibriLight
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
  - fleurs
  - mozilla-foundation/common_voice_8_0
  - MLCommons/peoples_speech
  - google/speech_commands
thumbnail: null
tags:
  - speech-recognition
  - unified-asr
  - offline-asr
  - streaming-asr
  - automatic-speech-recognition
  - speech
  - audio
  - FastConformer
  - RNNT
  - Parakeet
  - ASR
  - pytorch
  - NeMo
widget:
  - example_title: Librispeech sample 1
    src: https://cdn-media.huggingface.co/speech_samples/sample1.flac
  - example_title: Librispeech sample 2
    src: https://cdn-media.huggingface.co/speech_samples/sample2.flac
model-index:
  - name: parakeet-unified-en-0.6b
    results:
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: AMI
          type: ami
          config: ihm
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 10.14
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: Earnings22
          type: earnings22
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 11.16
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: Gigaspeech
          type: gigaspeech
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 10.05
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech test-clean
          type: librispeech_asr
          config: clean
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 1.63
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech test-other
          type: librispeech_asr
          config: other
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 3.11
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: SPGI Speech
          type: spgispeech
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 2.04
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: TEDLIUM
          type: tedlium
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 3.39
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: VoxPopuli
          type: voxpopuli
          config: en
          split: test
        metrics:
          - name: WER (offline)
            type: wer
            value: 5.77
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: AMI
          type: ami
          config: ihm
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 10.67
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: Earnings22
          type: earnings22
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 11.69
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: Gigaspeech
          type: gigaspeech
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 10.39
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech test-clean
          type: librispeech_asr
          config: clean
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 1.78
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: LibriSpeech test-other
          type: librispeech_asr
          config: other
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 3.54
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: SPGI Speech
          type: spgispeech
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 2.32
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: TEDLIUM
          type: tedlium
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 3.63
      - task:
          name: Automatic Speech Recognition
          type: automatic-speech-recognition
        dataset:
          name: VoxPopuli
          type: voxpopuli
          config: en
          split: test
        metrics:
          - name: WER (1.12s latency)
            type: wer
            value: 6.26
metrics:
  - wer
pipeline_tag: automatic-speech-recognition
---

# 🦜Parakeet-unified-en-0.6b: Unified ASR model for offline and streaming inference

| [Model architecture](#model-architecture) | [Model size](#model-architecture) | [Language](#datasets) |
|---|---|---|

Parakeet-unified-en-0.6b is an English automatic speech recognition (ASR) model based on transducer architecture (RNN-T) combining both offline and streaming inference (with a minimum latency of 160ms) in one model [1]. It is trained mostly on the English part of the Granary dataset [4], which contains approximately 250,000 hours of US English (en-US) speech across diverse acoustic conditions. The model transcribes speech to English alphabet, spaces, and apostrophes with punctuation and captalization support.

<figure align="center">
  <img src="figures/wer_comparison.png" width="1250" />
  <figcaption>
    Average WER comparison on the HF ASR Leaderboard datasets including offline and streaming inference with different latency values.
  </figcaption>
</figure>

Why Choose nvidia/parakeet-unified-en-0.6b?

- **One model for both tasks:** You need to utilize only one unified model for both offline and streaming inference with a minimum latency of 160ms.
- **Better accuracy performance:** The unified model achieves better accuracy performance on the HF ASR Leaderboard datasets compared to the previous transducer-based offline and streaming only models.
- **Streaming chunk size flexibilty:** Enables you to choose the optimal streaming latency (chunk + right context) from 2080ms to 160ms with step of 80ms.
- **Punctuation & Capitalization:** Built-in support for punctuation and capitalization in output text

This model consists of a 🦜 Parakeet (FastConformer) encoder (jointly trained in offline and streaming modes) with an RNN-T decoder. It is designed for offline and streaming speech-to-text applications where latency can be as low as 160ms, such as voice assistants, live captioning, and conversational AI systems. The current inference pipeline supports only buffered streaming (left context is recomputed for each chunk) that can be longer than cache-aware streaming.

This model is ready for commercial/non-commercial use.

## License/Terms of Use:

Governing Terms: Use of the model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

## Deployment Geography:

Global   


## Use Case:   

This model is for transcription of English audio in offline and streaming modes.   


## Release Date:    
 
- Hugging Face [04/07/2026] via [https://huggingface.co/nvidia/parakeet-unified-en-0.6b](https://huggingface.co/nvidia/parakeet-unified-en-0.6b)   


## Model Architecture

**Architecture Type:** Unified-FastConformer-RNNT

The unified model architecture is presented in [1]. The model is based on the FastConformer encoder architecture [2] with 24 encoder layers and an RNNT (Recurrent Neural Network Transducer) decoder. The model was trained jointly in offline and streaming modes. In the offline mode we used standard offline training with full-context self-attention and non-causal convolutions. In the streaming mode we applied chunked self-attention masks (incluing left, middle/chunk and right context) together with Dynamic Chunked Convolutions inside each FastConformer layer [3] to adapt the model to both decoding scenarios. We also introduced a novel mode-consistency regularization loss to further reduce the gap between offline and streaming performance. All the model parameters are shared between offline and streaming modes (encoder, predictor, and joint networks), including initial x8 subsampling with non-causal convolutions.

**Network Architecture:**

- Encoder: Unified FastConformer with 24 layers
- Decoder: RNNT (Recurrent Neural Network Transducer)
- Parameters: 600M

## NVIDIA NeMo

## How to Use this Model

For now, we provide only inference support for the unified model. We will release the unified training pipeline soon. 

### Loading the Model

```python
import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-unified-en-0.6b")
```

### Offline Inference

```python
output = asr_model.transcribe([wav_file_path])
print(output[0].text)
```

### Streaming Inference

For streaming inference you can use statfull chunked RNN-T decoding script from NeMo - [/NeMo/blob/main/examples/asr/asr_chunked_inference/rnnt/speech_to_text_streaming_infer_rnnt.py](https://github.com/NVIDIA-NeMo/NeMo/blob/main/examples/asr/asr_chunked_inference/rnnt/speech_to_text_streaming_infer_rnnt.py)

```bash
cd NeMo
python examples/asr/asr_chunked_inference/rnnt/speech_to_text_streaming_infer_rnnt.py \
    model_path=<model_path> \
    dataset_manifest=<dataset_manifest> \ 
    output_filename=<output_json_file> \
    left_context_secs=<left_context_secs> \   # left context in seconds, 5.6s by default
    chunk_secs=<chunk_secs> \                 # chunk size in seconds, 0.56s by default
    right_context_secs=<right_cintext_secs> \ # right context in seconds, 0.56s by default
    att_context_size_as_chunk=true \          # set to true to use chunked self-attention masks
    batch_size=<batch_size>
```

You can also run streaming inference through the pipeline method, which uses [NeMo/examples/asr/conf/asr_streaming_inference/buffered_rnnt.yaml](https://github.com/NVIDIA-NeMo/NeMo/blob/main/examples/asr/conf/asr_streaming_inference/buffered_rnnt.yaml) configuration file to build end‑to‑end workflows with punctuation and capitalization (PnC), inverse text normalization (ITN), and translation support.

```python
from nemo.collections.asr.inference.factory.pipeline_builder import PipelineBuilder
from omegaconf import OmegaConf

# Path to the buffered rnnt config file downloaded from above link
cfg_path = 'buffered_rnnt.yaml'
cfg = OmegaConf.load(cfg_path)

# Pass the paths of all the audio files for inferencing
audios = ['/path/to/your/audio.wav']

# Create the pipeline object and run inference
pipeline = PipelineBuilder.build_pipeline(cfg)
output = pipeline.run(audios)

# Print the output
for entry in output:
  print(entry['text'])
```

---

### Setting up Streaming Configuration

Latency is defined as the sum of the chunk size (middle part) and the right context.
For the left context we use 5.6s by default (5.6s was used during the model training), but you can try to find the optimal value for better accuracy/speed trade-off. 

We would recommend to use the following context parameters for different latencies:

| Left, s | Chunk, s | Right, s | Latency (C+R), s |
| :---: | :---: | :---: | :---: |
| 5.6 | 1.04 | 1.04 | 2.08 |
| 5.6 | 0.56 | 0.56 | 1.12 |
| 5.6 | 0.16 | 0.40 | 0.56 |
| 5.6 | 0.08 | 0.24 | 0.32 |
| 5.6 | 0.08 | 0.16 | 0.24 |
| 5.6 | 0.08 | 0.08 | 0.16 |

### Input

- Input Type(s): Audio   
- Input Format(s): wav   
- Input Parameters: One-Dimensional (1D)   
- Other Properties Related to Input: Maximum Length in seconds specific to GPU Memory, No Pre-Processing Needed, Mono channel is required. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.   


### Output

- Output Type(s): Text String in English   
- Output Format(s): String   
- Output Parameters: One-Dimensional (1D)   
- Other Properties Related to Output: No Maximum Character Length, transcribe punctuation and capitalization. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.   


## Datasets

### Training Datasets

The majority of the training data comes from the English portion of the Granary dataset [4]:

- YouTube-Commons (YTC) (109.5k hours)
- YODAS2 (102k hours)
- Mosel (14k hours)
- LibriLight (49.5k hours)

In addition, the following datasets were used:

- Librispeech 960 hours
- Fisher Corpus
- Switchboard-1 Dataset
- WSJ-0 and WSJ-1
- National Speech Corpus (Part 1, Part 6)
- VCTK
- VoxPopuli (EN)
- Europarl-ASR (EN)
- Multilingual Librispeech (MLS EN)
- Mozilla Common Voice (v11.0)
- Mozilla Common Voice (v7.0)
- Mozilla Common Voice (v4.0)
- People Speech
- AMI

**Data Modality:** Audio and text

**Audio Training Data Size:** 250k hours

**Data Collection Method:** Human - All audios are human recorded

**Labeling Method:** Hybrid (Human, Synthetic) - Some transcripts are generated by ASR models, while some are manually labeled

### Evaluation Datasets

The model was evaluated on the HuggingFace ASR Leaderboard datasets:

- AMI
- Earnings22
- Gigaspeech
- LibriSpeech test-clean
- LibriSpeech test-other
- SPGI Speech
- TEDLIUM
- VoxPopuli

## Performance

## ASR Performance (w/o PnC)

ASR performance is measured using the Word Error Rate (WER). Both ground-truth and predicted texts are processed using [whisper-normalizer](https://pypi.org/project/whisper-normalizer/) version 0.1.12. The obtained results for other models can be slightly different from the official HF model cards because of the different evaluation machines.

The following table show the WER on the [HuggingFace OpenASR leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) datasets including offline and streaming inference with different latency values:


| Model setup | Offline | 2.08s | 1.12s | 0.56s | 0.40s | 0.32s | 0.24s | 0.16s | 0.08s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| nvidia/parakeet-tdt-0.6b-v2 | 6.04 | 7.99 | 22.83 | 69.55 | 95.12 | — | — | — | — |
| nvidia/nemotron-speech-streaming-en-0.6b | 6.92 | 7.46 | 6.92 | 7.09 | 9.52 | 7.64 | 8.01 | **7.84** | **8.70** |
| nvidia/parakeet-unified-en-0.6b | **5.91** | **6.14** | **6.29** | **6.52** | **6.70** | **6.92** | **7.35** | 8.44 | 15.63 |


Parakeet-unified-en-0.6b model outperforms previous NVIDIA transducer-based models in offline and streaming (up to 240ms latency) inference modes. At 160ms latency, the unified model start to degrade because of the ansence of enough right context, yielding slightly to the strong streaming baseline. For 80ms latency we would recommend to use nemotron-speech-streaming-en-0.6b model instead.

## Software Integration

**Runtime Engine:** NeMo 2.7.3

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Ampere
- NVIDIA Blackwell
- NVIDIA Hopper
- NVIDIA Volta

**Test Hardware:**

- NVIDIA V100
- NVIDIA A100
- NVIDIA A6000
- DGX Spark

**Preferred/Supported Operating System(s):** Linux

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## References

[1] [Reducing the Offline-Streaming Gap for Unified ASR Transducer with Consistency Regularization](https://arxiv.org/abs/2604.19079)

[2] [Fast Conformer with Linearly Scalable Attention for Efficient Speech Recognition](https://arxiv.org/abs/2305.05084)

[3] [Dynamic Chunk Convolution for Unified Streaming and Non-Streaming Conformer ASR](https://arxiv.org/abs/2304.09325)

[4] [NVIDIA Granary](https://huggingface.co/datasets/nvidia/Granary)

[5] [NVIDIA NeMo Framework](https://github.com/NVIDIA/NeMo)