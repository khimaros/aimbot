---
license: other
license_name: openmdw-1.1
license_link: https://openmdw.ai/license/1-1/
base_model: nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B
base_model_relation: quantized
pipeline_tag: automatic-speech-recognition
language:
- en
- ja
tags:
- gguf
- audio
- audio.cpp
- community-model
---

# Nemotron 3.5 Transcribe 30B-A4B GGUF for audio.cpp

Experimental community packages derived directly from NVIDIA's full BF16
[checkpoint](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B),
revision `a99e33f698257b8b69ca7834f19c73582eb1fa7e`. These are quantized derivatives;
they do not use the separately packed NVFP4 release as input.

Support is merged into upstream [audio.cpp](https://github.com/0xShug0/audio.cpp)
through [PR #1137](https://github.com/0xShug0/audio.cpp/pull/1137), merged on October 31, 2026.
Use merge commit [`ad14f0c4`](https://github.com/0xShug0/audio.cpp/commit/ad14f0c4dbd5b12b7711bb7b46abb8d94f78f067)
or a later upstream revision containing this model. A separate PR branch is no longer required.
The merged runtime includes K-profile loading, the auxiliary encoder filename support,
and the Vulkan encoder normalization fix. Existing model files work unchanged.

The runtime exposes offline transcription, translation, audio questions, language
identification, source-word timestamps and speaker labels. This remains an experimental
community model, separate from the smaller Nemotron RNNT ASR model.

**Update**: [PR #1154](https://github.com/0xShug0/audio.cpp/pull/1154) adds CPU offloading. 
Q4_K_S expert decoder + F16 encoder + RTX 5090: Peak VRAM drops to **~6.7 GB** (CUDA) and **~6.0 GB** (Vulkan), while maintaining **17.5×** and **12.9×** real-time performance, respectively.


## Files

Each model needs **one decoder plus the required shared speech encoder**.
The required auxiliary file uses FP16 speech-encoder weights by default and an FP32 CTC head.
Its `mmproj-` prefix marks an audio encoder/projection sidecar, not a standalone 16-bit model.
The updated loader accepts both this name and the original native encoder filename.
Do not omit it when downloading a decoder.

| Decoder | Bytes | Routed experts | Input padding |
| --- | ---: | --- | --- |
| [IQ4_NL](nemotron-transcribe-30b-a4b-experts-IQ4_NL.gguf) | 20,370,389,728 | IQ4_NL | None |
| [Q4_K_S filename](nemotron-transcribe-30b-a4b-experts-Q4_K_S.gguf) | 21,672,721,184 | Q4_K | 256-element rows |
| [Q3_K_S filename](nemotron-transcribe-30b-a4b-experts-Q3_K_S.gguf) | 17,294,261,024 | Q3_K | 256-element rows |
| [Q2_K](nemotron-transcribe-30b-a4b-experts-Q2_K.gguf) | 13,946,026,784 | Q2_K | 256-element rows |

Download the selected decoder and
[the required shared speech encoder](mmproj-NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-Encoder-F16.gguf) into the same directory.
The shared encoder is 1,670,410,080 bytes. It includes F16 speech weights and
the F32 CTC timestamp head. Decoder specs, configs, tokenizer, trained frontend
window and license notices are embedded. These file sizes are not peak runtime
memory estimates.

The `_S` filename suffixes let the Hub selector recognize the Q3_K and Q4_K expert files.
These are custom mixed profiles, not the stock whole-model llama.cpp `_S` recipes.
Their routed tensors remain Q3_K or Q4_K, with Q8_0 dense linears and preserved floating-point tensors.
The rename changes no tensor data.

IQ4_NL is an unpadded four-bit option. Q4_K, Q3_K and Q2_K use padded routed
expert banks. The profile names describe those banks. Dense decoder linears use
Q8_0; embeddings, output projection, routers, norms and recurrent parameters
retain their floating-point source types. The runtime loads parameters as F32
where its operations require it. The exact per-tensor formats and physical
dimensions are listed in `quantization.json`.

K blocks require 256 input elements. The converter adds zero input columns to
the routed up/down banks, from 2,688 to 2,816 and from 1,856 to 2,048. The model
adds corresponding zero input activations before those two matrix products.
Logical output dimensions, routing, normalization and the other projections are
unchanged. Floating-point padding parity and real K tensor formats are checked
by the supplied code. Padding adds storage, so Q4_K may be larger than unpadded
IQ4_NL.

The three padded K layouts require the audio.cpp community-model adapter. Stock
NeMo-Speech.cpp and llama.cpp inference do not load those layouts. No GGML modification
is required by the audio.cpp port.

## Run

Build upstream audio.cpp at the merged revision or later. For example, with CUDA:

```sh
git clone https://github.com/0xShug0/audio.cpp.git
cd audio.cpp
git checkout ad14f0c4dbd5b12b7711bb7b46abb8d94f78f067
cmake -S . -B build/nemotron -DAUDIOCPP_MODEL_SET=custom \
  -DAUDIOCPP_MODELS=nemotron_transcribe -DAUDIOCPP_DEPLOYMENT_BUILD=ON \
  -DENGINE_ENABLE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=native
cmake --build build/nemotron --target audiocpp_cli --parallel 4
```

Omit the CUDA options for a CPU build and use `--backend cpu` below. On Windows,
build from an x64 Visual Studio developer shell and use the `.exe` suffix.
Run the built CLI from its output directory or put it on `PATH`.

Then download one decoder and the required encoder, for example:

```sh
hf download Jmica/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-GGUF \
  nemotron-transcribe-30b-a4b-experts-Q4_K_S.gguf \
  mmproj-NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-Encoder-F16.gguf \
  --local-dir models/nemotron-transcribe

audiocpp_cli --task asr --family nemotron_transcribe --backend cuda \
  --model models/nemotron-transcribe/nemotron-transcribe-30b-a4b-experts-Q4_K_S.gguf \
  --audio recording.wav --request-option language=ja --text-out transcript.txt
```

For longer recordings, caller-managed clips matching the source processor's
30-second setting are a useful starting point. Shift timestamps by each clip's
source offset. Cuts can split words, and separate requests do not preserve
speaker identities. The runtime's accepted input size is a capacity limit,
not a guarantee of recognition quality at that length.

Use `return_timestamps=true` for CTC words, `diarization=true` for speaker tags,
or `template_name=translation`, `audio_qa` and `language_id` for the other tasks.
See the [model guide](https://github.com/0xShug0/audio.cpp/blob/ad14f0c4dbd5b12b7711bb7b46abb8d94f78f067/docs/models/nemotron_transcribe.md)
for supported options, input formats, API routes and limitations.

## English checks and runtime compatibility

Recorded checks for the initial IQ4_NL package, with word timestamps. Processing
time excludes model loading. Real-time factor is processing time divided by audio duration.

| Input and backend | Audio | Processing | Real-time factor | Matched reference words |
| --- | ---: | ---: | ---: | ---: |
| Short English, CUDA | 7.330 s | 0.556 s | 0.076 | 15/15 |
| Short English, CPU, four threads | 7.330 s | 6.250 s | 0.853 | 15/15 |
| Distinct two-speaker English, CUDA | 49.055 s | 1.232 s | 0.025 | 129/129 |

All four released expert profiles also matched the same 15-word and 129-word
fixtures. Matching ignores case, punctuation and speaker markers. These are
small synthetic checks with other workloads active, not held-out English accuracy
or general throughput estimates. See the upstream [validation record](https://github.com/0xShug0/audio.cpp/blob/ad14f0c4dbd5b12b7711bb7b46abb8d94f78f067/docs/models/nemotron_transcribe_validation.md)
for source versions, fixture texts, commands and known timestamp/repetition limitations.

An older runtime can reject the encoder on Vulkan with
`encoder contains unsupported backend op 'NORM'`. The merged code materializes
strided Q/K inputs before normalization. Update audio.cpp and rebuild; the
weights do not need to be downloaded again. The original rejection was reproduced
and the corrected small encoder completed on the actual Vulkan backend with the
llvmpipe software driver. Released-encoder CPU fixture outputs remained byte-identical.
This does not establish full-model hardware Vulkan support or performance.

## Reproduce conversion

The [conversion guide](https://github.com/0xShug0/audio.cpp/blob/ad14f0c4dbd5b12b7711bb7b46abb8d94f78f067/docs/models/nemotron_transcribe.md#q4_k-q3_k-and-q2_k-expert-profiles)
includes the full-source export, pristine pinned quantizer build and three
profile commands. The scripts use uv/Python, one reusable BF16 export and one
streamed padded cache. They never requantize the existing IQ4 model or patch
GGML. They reject silent quantization fallback, altered preserved payloads,
incorrect pairing and incompatible caches.

Reference converter revision: `66d50d91b75a406becd95fbaf39d2c9c13e95d7c`.
Quantizer revision: `bd4f514db14d87fded667787a7a963bfbaa98e89`.

The packages were executed through the supported audio.cpp task routes before
upload. Functional checks do not establish broad multilingual accuracy or full
Metal/Vulkan coverage. Lower precision changes predictions, and fewer bits do
not imply a predictable ranking on every recording. CTC word times can drift
at pauses and overlap other speakers. MTP, DFlash,
streaming and native batching are outside this port.

Weights retain OpenMDW-1.1 and the included component notices. NVIDIA is the
upstream model author; this repository is a community conversion.
