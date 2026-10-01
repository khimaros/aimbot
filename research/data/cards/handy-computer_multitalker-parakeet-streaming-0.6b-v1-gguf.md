---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
base_model: nvidia/multitalker-parakeet-streaming-0.6b-v1
base_model_relation: quantized
library_name: transcribe.cpp
pipeline_tag: automatic-speech-recognition
language:
  - en
tags:
  - gguf
  - transcribe.cpp
  - asr
  - speech-to-text
  - parakeet
  - conformer
  - rnnt
  - streaming
  - cache-aware
  - diarization
  - multitalker
  - sortformer
transcribe_cpp:
  schema_version: 2
  wer_fleurs_en:
    q8_0: 6.52
  wer_librispeech_test_clean:
    f32: 2.19
    f16: 2.19
    q8_0: 2.18
    q6_k: 2.2
    q5_k_m: 2.18
    q4_k_m: 2.18
  cpwer_ami_ihm_test_kernel:
    f32: 19.35
  cpwer_ami_ihm_test_masked:
    f32: 23.73
  rtf_m4_max:
    cpu: 32.72
    metal: 217.47
  rtf_ryzen_4750u:
    cpu: 13.41
    vulkan: 26.34
  streaming: true
  diarize: true
  translate: false
  lang_detect: false
  timestamps: token
---

# multitalker-parakeet-streaming-0.6b-v1: transcribe.cpp GGUF

GGUF conversions of [nvidia/multitalker-parakeet-streaming-0.6b-v1](https://huggingface.co/nvidia/multitalker-parakeet-streaming-0.6b-v1) for use
with [transcribe.cpp](https://github.com/handy-computer/transcribe.cpp).

Ported from upstream commit
[8749fc7](https://huggingface.co/nvidia/multitalker-parakeet-streaming-0.6b-v1/commit/8749fc7),
pinned 2026-07-12.
Validated against the NeMo reference at transcribe.cpp commit
[3083021](https://github.com/handy-computer/transcribe.cpp/tree/3083021)
on 2026-08-03.

Offline and cache-aware streaming English speech-to-text with punctuation and capitalization. A 0.6B-parameter cache-aware streaming FastConformer encoder with an RNN-T transducer decoder, fine-tuned from nvidia/nemotron-speech-streaming-en-0.6b. Plain GGUFs run the single_speaker_mode ASR path, while bundle GGUFs under `bundle/` embed nvidia/diar_streaming_sortformer_4spk-v2.1 and, with `--diarize`, transcribe up to four overlapping speakers into a speaker-tagged transcript. The encoder preserves the upstream att_context_size=[70, 13] (1.12s) cache-aware attention mask; all four latency lookahead settings are selectable.


## Downloads

| Quantization | Download | Size | WER (LibriSpeech test-clean, offline) |
| --- | --- | ---: | ---: |
| F32 | [bundle/multitalker-parakeet-streaming-0.6b-v1-F32.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-F32.gguf) | 2.96 GB | 2.19% |
| F16 | [bundle/multitalker-parakeet-streaming-0.6b-v1-F16.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-F16.gguf) | 1.48 GB | 2.19% |
| Q8_0 | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf) | 873 MB | 2.18% |
| Q6_K | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q6_K.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q6_K.gguf) | 743 MB | 2.20% |
| Q5_K_M | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q5_K_M.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q5_K_M.gguf) | 681 MB | 2.18% |
| Q4_K_M | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q4_K_M.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q4_K_M.gguf) | 617 MB | 2.18% |

WER on the full LibriSpeech test-clean split (2,620 utterances), batch size 1, timestamps none. Figures without a commit were published before provenance was recorded.

Run in single_speaker_mode with greedy RNN-T decoding and whisper-normalizer
(PnC-stripped) scoring. F32 reference baseline: 2.19%. The measured NeMo
single_speaker_mode reference and NVIDIA's self-reported number on the same split
are both 2.19%.

### Multitalker bundles (speaker-attributed ASR)

Bundle GGUFs embed the streaming Sortformer diarizer alongside the ASR model. Run them with `--diarize` to get a speaker-tagged transcript with up to four speakers. The tier names the ASR half's dtype; the embedded diarizer is F32 for the F32 bundle, F16 for F16, and Q8_0 for all k-quant tiers.

| Bundle | Download | Size |
| --- | --- | ---: |
| F32 | [bundle/multitalker-parakeet-streaming-0.6b-v1-F32.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-F32.gguf) | 2.96 GB |
| F16 | [bundle/multitalker-parakeet-streaming-0.6b-v1-F16.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-F16.gguf) | 1.48 GB |
| Q8_0 | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf) | 873 MB |
| Q6_K | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q6_K.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q6_K.gguf) | 743 MB |
| Q5_K_M | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q5_K_M.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q5_K_M.gguf) | 681 MB |
| Q4_K_M | [bundle/multitalker-parakeet-streaming-0.6b-v1-Q4_K_M.gguf](https://huggingface.co/handy-computer/multitalker-parakeet-streaming-0.6b-v1-gguf/resolve/main/bundle/multitalker-parakeet-streaming-0.6b-v1-Q4_K_M.gguf) | 617 MB |

cpWER on AMI-IHM test (16 meetings, F32 bundle) is 19.35% in the default kernel mode and 23.73% in masked mode. The matched NeMo reference scores 21.39% and 24.00%, respectively; see the transcribe.cpp model page for the exactness accounting.

```bash
build/bin/transcribe-cli --diarize \
  -m bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf \
  meeting.wav
```


## Usage

Build transcribe.cpp from source:

```bash
git clone git@github.com:handy-computer/transcribe.cpp.git
cd transcribe.cpp
cmake -B build && cmake --build build
```

Run on a 16 kHz mono WAV:

```bash
build/bin/transcribe-cli \
  -m bundle/multitalker-parakeet-streaming-0.6b-v1-Q8_0.gguf \
  input.wav
```

If your audio isn't already 16 kHz mono WAV, convert it first:

```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
```

See the [transcribe.cpp model page](https://github.com/handy-computer/transcribe.cpp/blob/main/docs/models/multitalker-parakeet-streaming-0.6b-v1.md) for performance
numbers, numerical validation, and reproduction steps.

## License

Inherited from the base model: **NVIDIA Open Model License**. See the
[upstream model card](https://huggingface.co/nvidia/multitalker-parakeet-streaming-0.6b-v1) for full terms.

---

## Original Model Card

> The section below is reproduced from
> [nvidia/multitalker-parakeet-streaming-0.6b-v1](https://huggingface.co/nvidia/multitalker-parakeet-streaming-0.6b-v1) at commit
> `8749fc7` for offline reference. The upstream card is the
> authoritative source.

# Multitalker Parakeet Streaming 0.6B v1

<style>
img {
 display: inline;
}
</style>

[![Model architecture](https://img.shields.io/badge/Model_Arch-FastConformer--Transformer-lightgrey#model-badge)](#model-architecture)
| [![Model size](https://img.shields.io/badge/Params-600M-lightgrey#model-badge)](#model-architecture)
<!-- | [![Language](https://img.shields.io/badge/Language-multilingual-lightgrey#model-badge)](#datasets) -->

This model is a streaming multitalker ASR model based on the [Nemotron-Speech-Streaming](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) model. The model only takes the speaker diarization outputs as external information and eliminates the need for explicit speaker queries or enrollment audio [[Wang et al., 2025]](https://arxiv.org/abs/2506.22646). Unlike conventional target-speaker ASR approaches that require speaker embeddings, this model dynamically adapts to individual speakers through speaker-wise speech activity prediction.

The key innovation involves injecting learnable **speaker kernels** into the pre-encode layer of the Fast-Conformer encoder. These speaker kernels are generated via speaker supervision activations, enabling instantaneous adaptation to target speakers. This approach leverages the inherent tendency of streaming ASR systems to prioritize specific speakers, repurposing this mechanism to achieve robust speaker-focused recognition.

The model architecture requires deploying **one model instance per speaker**, meaning the number of model instances matches the number of speakers in the conversation. While this necessitates additional computational resources, it achieves state-of-the-art performance in handling fully overlapped speech in both offline and streaming scenarios.

## Video Demo

[![Watch the video](https://img.youtube.com/vi/AThOsk2qJbs/maxresdefault.jpg)](https://youtu.be/AThOsk2qJbs)

## Key Advantages

This self-speaker adaptation approach offers several advantages over traditional multitalker ASR methods:

1. **No Speaker Enrollment**: Unlike target-speaker ASR systems that require pre-enrollment audio or speaker embeddings, this model only needs speaker activity information from diarization
2. **Handles Severe Overlap**: Each instance focuses on a single speaker, enabling accurate transcription even during fully overlapped speech
3. **Streaming Capable**: Designed for real-time streaming scenarios with configurable latency-accuracy tradeoffs
4. **Leverages Single-Speaker Models**: Can be fine-tuned from strong pre-trained single-speaker ASR models, and single speaker ASR performance is also preserved

## Discover more from NVIDIA:
For documentation, deployment guides, enterprise-ready APIs, and the latest open models—including Nemotron and other cutting-edge speech, translation, and generative AI—visit the NVIDIA Developer Portal at [developer.nvidia.com](https://developer.nvidia.com/).
Join the community to access tools, support, and resources to accelerate your development with NVIDIA’s NeMo, Riva, NIM, and foundation models.<br>

### Explore more from NVIDIA:  <br>
What is [Nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/)?<br>
NVIDIA Developer [Nemotron](https://developer.nvidia.com/nemotron)<br>
[NVIDIA Riva Speech](https://developer.nvidia.com/riva?sortBy=developer_learning_library%2Fsort%2Ffeatured_in.riva%3Adesc%2Ctitle%3Aasc#demos)<br>
[NeMo Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/models.html)<br>


## Model Architecture

### Speaker Kernel Injection

The streaming multitalker Parakeet model employs a **speaker kernel injection** mechanism at some layers of the Fast-Conformer encoder. As shown in the figure below, learnable speaker kernels are injected into selected encoder layers, enabling the model to dynamically adapt to specific speakers.

<div align="center">
    <img src="figures/speaker_injection.png" width="750" />
</div>

The speaker kernels are generated through speaker supervision activations that detect speech activity for each target speaker. This enables the encoder states to become more responsive to the targeted speaker's speech characteristics, even during periods of fully overlapped speech.

### Multi-Instance Architecture

The model is based on the Parakeet architecture and consists of a [NeMo Encoder for Speech Tasks (NEST)](https://arxiv.org/abs/2408.13106)[4] which is based on [Fast-Conformer](https://arxiv.org/abs/2305.05084)[5] encoder. The key architectural innovation is the **multi-instance approach**, where one model instance is deployed per speaker as illustrated below:

<div align="center">
    <img src="figures/multi_instance.png" width="1400" />
</div>

Each model instance:
- Receives the same mixed audio input
- Injects speaker-specific kernels at the pre-encode layer
- Produces transcription output specific to its target speaker
- Operates independently and can run in parallel with other instances

This architecture enables the model to handle severe speech overlap by having each instance focus exclusively on one speaker, eliminating the permutation problem that affects other multitalker ASR approaches.

## NVIDIA NeMo

To train, fine-tune or perform multitalker ASR with this model, you will need to install [NVIDIA NeMo](https://github.com/NVIDIA/NeMo)[7]. We recommend you install it after you've installed Cython and latest PyTorch version.

```bash
apt-get update && apt-get install -y libsndfile1 ffmpeg
pip install Cython packaging
pip install git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[asr]
```

## How to Use this Model

The model is available for use in the NeMo Framework[7], and can be used as a pre-trained checkpoint for inference or for fine-tuning on another dataset.

**Important**: This model uses a multi-instance architecture where you need to deploy one model instance per speaker. Each instance receives the same audio input along with speaker-specific diarization information to perform self-speaker adaptation.

### Method 1. Code snippet 

 Load one of the NeMo speaker diarization models:  
 [Streaming Sortformer Diarizer v2](https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1),  
 [Streaming Sortformer Diarizer v2.1](https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1)   
```python
from nemo.collections.asr.models import SortformerEncLabelModel, ASRModel
import torch
# A speaker diarization model is needed for tracking the speech activity of each speaker.
diar_model = SortformerEncLabelModel.from_pretrained("nvidia/diar_streaming_sortformer_4spk-v2.1").eval().to(torch.device("cuda"))
asr_model = ASRModel.from_pretrained("nvidia/multitalker-parakeet-streaming-0.6b-v1").eval().to(torch.device("cuda"))

# Use the pre-defined dataclass template `MultitalkerTranscriptionConfig` from `multitalker_transcript_config.py`. 
# Configure the diarization model using streaming parameters:
from multitalker_transcript_config import MultitalkerTranscriptionConfig
from omegaconf import OmegaConf
cfg = OmegaConf.structured(MultitalkerTranscriptionConfig())
cfg.audio_file = "/path/to/your/audio.wav"
cfg.output_path = "/path/to/output_transcription.json"

diar_model = MultitalkerTranscriptionConfig.init_diar_model(cfg, diar_model)

# Load your audio file into a streaming audio buffer to simulate a real-time audio session.
from nemo.collections.asr.parts.utils.streaming_utils import CacheAwareStreamingAudioBuffer

samples = [{'audio_filepath': cfg.audio_file}]
streaming_buffer = CacheAwareStreamingAudioBuffer(
    model=asr_model,
    online_normalization=cfg.online_normalization,
    pad_and_drop_preencoded=cfg.pad_and_drop_preencoded,
)
streaming_buffer.append_audio_file(audio_filepath=cfg.audio_file, stream_id=-1)
streaming_buffer_iter = iter(streaming_buffer)

# Use the helper class `SpeakerTaggedASR`, which handles all ASR and diarization cache data for streaming.
from nemo.collections.asr.parts.utils.multispk_transcribe_utils import SpeakerTaggedASR
multispk_asr_streamer = SpeakerTaggedASR(cfg, asr_model, diar_model)

for step_num, (chunk_audio, chunk_lengths) in enumerate(streaming_buffer_iter):
    drop_extra_pre_encoded = (
        0
        if step_num == 0 and not cfg.pad_and_drop_preencoded
        else asr_model.encoder.streaming_cfg.drop_extra_pre_encoded
    )
    with torch.inference_mode():
        with torch.amp.autocast(diar_model.device.type, enabled=True):
            with torch.no_grad():
                multispk_asr_streamer.perform_parallel_streaming_stt_spk(
                    step_num=step_num,
                    chunk_audio=chunk_audio,
                    chunk_lengths=chunk_lengths,
                    is_buffer_empty=streaming_buffer.is_buffer_empty(),
                    drop_extra_pre_encoded=drop_extra_pre_encoded,
                )
                print(multispk_asr_streamer.instance_manager.batch_asr_states[0].seglsts)
# Generate the speaker-tagged transcript and print it.
multispk_asr_streamer.generate_seglst_dicts_from_parallel_streaming(samples=samples)
print(multispk_asr_streamer.instance_manager.seglst_dict_list)
```

### Method 2. Use NeMo example file in NVIDIA/NeMo

Use [the multitalker streaming ASR example script file](https://github.com/NVIDIA-NeMo/NeMo/blob/main/examples/asr/asr_cache_aware_streaming/speech_to_text_multitalker_streaming_infer.py) in [NVIDIA NeMo Framework](https://github.com/NVIDIA-NeMo/NeMo) to launch. With this method, download the `.nemo` model files and specify that in the script:
```bash
python ${NEMO_ROOT}/examples/asr/asr_cache_aware_streaming/speech_to_text_multitalker_streaming_infer.py \
          asr_model="/path/to/your/multitalker-parakeet-streaming-0.6b-v1.nemo" \
          diar_model="/path/to/your/nvidia/diar_streaming_sortformer_4spk-v2.nemo" \
          att_context_size="[70,13]" \
          generate_realtime_scripts=False \
          audio_file="/path/to/example.wav" \
          output_path="/path/to/example_output.json" 
```

Or the `audio_file` argument can be replaced with the `manifest_file` to handle multiple files in batch mode:
```bash
python ${NEMO_ROOT}/examples/asr/asr_cache_aware_streaming/speech_to_text_multitalker_streaming_infer.py \
          ... \
          manifest_file="example.json" \
          ... \
```

In `example.json` file, each line is a dictionary containing the following fields:
```python
{
    "audio_filepath": "/path/to/multispeaker_audio1.wav",  # path to the input audio file 
    "offset": 0, # offset (start) time of the input audio
    "duration": 600,  # duration of the audio, can be set to `null` if using NeMo main branch
}
{
    "audio_filepath": "/path/to/multispeaker_audio2.wav",  
    "offset": 900,
    "duration": 580,  
}
```

### Setting up Streaming Configuration

Latency is defined by the `att_context_size`, all measured in **80ms frames**:
* [70, 0]: Chunk size = 1 (1 * 80ms = 0.08s)
* [70, 1]: Chunk size = 2 (2 * 80ms = 0.16s)
* [70, 6]: Chunk size = 7 (7 * 80ms = 0.56s)
* [70, 13]: Chunk size = 14 (14 * 80ms = 1.12s)

### Input

This model accepts single-channel (mono) audio sampled at 16,000 Hz.

### Output

The results will be found in `output_path`, which is in the seglst format. For more information please refer to [SegLST](https://github.com/fgnt/meeteval?tab=readme-ov-file#segment-wise-long-form-speech-transcription-annotation-seglst) format.

## Datasets

This multitalker ASR model was trained on a large combination of real conversations and simulated audio mixtures.
The training data includes both single-speaker and multi-speaker recordings with corresponding transcriptions and speaker labels in [SegLST](https://github.com/fgnt/meeteval?tab=readme-ov-file#segment-wise-long-form-speech-transcription-annotation-seglst) format
Data collection methods vary across individual datasets. The training datasets include phone calls, interviews, web videos, meeting recordings, and audiobook recordings. Please refer to the [Linguistic Data Consortium (LDC) website](https://www.ldc.upenn.edu/) or individual dataset webpages for detailed data collection methods.


### Training Datasets (Real conversations)
- Granary (single speaker)
- Fisher English (LDC)
- LibriSpeech
- AMI Corpus
- NOTSOFAR
- ICSI

### Training Datasets (Used to simulate audio mixtures)
- Librispeech

## Evaluation: Multitalker ASR Performance

| **Diarization Model** | **AMI IHM** | **AMI SDM** | **CH109** | **Mixer 6** |
|-----------------------|-------------|-------------|-----------|-------------|
| [Streaming Sortformer v2](https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2) | 21.26       | 37.44       | 15.81     | 23.81       |

### Evaluation data specification

| **Dataset** | **Number of speakers** | **Number of Sessions** |
|-------------|------------------------|------------------------|
| **AMI IHM** | 3-4                    | 219                    |
| **AMI SDM** | 3-4                    | 40                     |
| **CH109**   | 2                      | 259                    |
| **Mixer 6** | 2                      | 148                    |

### Concatenated minimum-permutation Word Error Rate (cpWER)

* All evaluations include overlapping speech.  
* Collar tolerance is 0s for DIHARD III Eval, and 0.25s for CALLHOME-part2 and CH109.
* Post-Processing (PP) can be optimized on different held-out dataset splits to improve diarization performance. 
* Latency is 1.12s with 13+1 lookahead frames.



## Evaluation: Single-speaker Mode ASR Performance

The single-speaker mode performance was evaluated on the [HuggingFace ASR Leaderboard](https://github.com/huggingface/open_asr_leaderboard) datasets:

Single speaker mode should be enabled to get the performance in the following table. 
```python
cfg.single_speaker_mode=True
```

| Model Names | **Avg** | AMI | Earnings | GigaSpeech | LS test-clean | LS test-other | SPGI | Tedlium | Voxpopuli |
| :--- | ---: | ------: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [Nemotron Speech Streaming ASR](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) | 7.16 | 11.58 | 12.48 | 11.45 | 2.31 | 4.75 | 2.62 | 4.5 | 7.57 |
| Single Speaker Mode | 7.44 | 11.62 | 14.68 | 11.49 | 2.19 | 4.76 | 2.68 | 4.65 | 7.45 |



## References

[1] [Speaker Targeting via Self-Speaker Adaptation for Multi-talker ASR](https://arxiv.org/abs/2506.22646)  

[2] [Sortformer: Seamless Integration of Speaker Diarization and ASR by Bridging Timestamps and Tokens](https://arxiv.org/abs/2409.06656)

[3] [Streaming Sortformer: Speaker Cache-Based Online Speaker Diarization with Arrival-Time Ordering](https://arxiv.org/abs/2507.18446)

[4] [NEST: Self-supervised Fast Conformer as All-purpose Seasoning to Speech Processing Tasks](https://arxiv.org/abs/2408.13106)

[5] [Fast Conformer with Linearly Scalable Attention for Efficient Speech Recognition](https://arxiv.org/abs/2305.05084)

[6] [Attention is all you need](https://arxiv.org/abs/1706.03762)

[7] [NVIDIA NeMo Framework](https://github.com/NVIDIA/NeMo)

[8] [NeMo speech data simulator](https://arxiv.org/abs/2310.12371)
