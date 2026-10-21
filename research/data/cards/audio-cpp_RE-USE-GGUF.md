---
license: other
license_name: nvidia-one-way-noncommercial
license_link: LICENSE
base_model: nvidia/RE-USE
library_name: audio.cpp
pipeline_tag: audio-to-audio
tags:
  - audio.cpp
  - gguf
  - speech-enhancement
  - language-agnostic
---

# RE-USE GGUF

GGUF weights for native inference with
[audio.cpp](https://github.com/0xShug0/audio.cpp). RE-USE restores degraded
speech while preserving its input sample rate. It uses a convolutional
encoder/decoder and 30 bidirectional time-frequency Mamba blocks.

## Upstream

The checkpoint and reference implementation are pinned to
[nvidia/RE-USE, revision 022e920d727347a64d6c21fbf0628f2a5f37ad78](https://huggingface.co/nvidia/RE-USE/tree/022e920d727347a64d6c21fbf0628f2a5f37ad78).
Each GGUF includes the model weights, configuration, and audio.cpp model spec.
No separate encoder or tokenizer is required. Packages are converted directly
from the original safetensors, not from another GGUF.

## Packages

| File | Size | Storage | Recommendation |
|---|---:|---|---|
| `reuse-f32.gguf` | 37.80 MiB | F32 | Default; fastest of the tested C++ formats. |

Only F32 is provided. F16 and Q8 were rejected because their small disk savings
did not improve speed or peak VRAM in testing, while introducing waveform drift
and additional packaging complexity.

F32 was checked on CUDA and Vulkan. Metal, and HIP were not validated in
this comparison.

## Controlled Parity With Python

These are **separate accuracy runs**, not the performance runs below. Both
implementations used original F32 weights with TF32 disabled. Comparisons cover
the final waveform, with no time alignment or normalization applied.

| Input | Rate / channels | C++ vs Python cosine | Relative RMSE |
|---|---|---:|---:|
| Official `noisy_audio/mic_test2.wav`, 5.10 s | 44.1 kHz / mono | 0.99999846 | 0.001756 |
| `sample_16k.wav`, 14.07 s | 16 kHz / mono | 0.999999995 | 0.0000972 |
| `c.wav`, 7.53 s | 24 kHz / stereo | 0.99964691 | 0.026572 |

The last two inputs are in audio.cpp's
[audio fixtures](https://github.com/0xShug0/audio.cpp/tree/main/assets/resources).
The outputs are not bit-identical to Python; the stereo example has noticeably
larger numerical drift than the mono examples. These checks do not establish
identical output on every recording or backend.

## Ordinary CUDA Performance

- Remeasured on 2026-09-27 after the scoped SSM-convolution optimization.
- NVIDIA RTX 5090, 8 CPU threads, audio.cpp Debug build, PyTorch 2.11.0+cu128.
- Original F32 checkpoint for Python. Normal inference defaults, **no TF32
  overrides or precision overrides**. Logging enabled for C++.
- Five sequential requests in one loaded session. Time is the median of the
  last three; model loading and WAV file I/O are excluded. C++ includes its host
  STFT/ISTFT, and Python includes its GPU STFT/ISTFT.
- Peak VRAM is process memory sampled with `nvidia-smi` every 50 ms across
  loading and all five requests, not PyTorch allocator-only memory.
- RTF is inference time divided by input duration; lower is faster.

| 5.10-second official microphone clip | Inference time | RTF | Peak VRAM |
|---|---:|---:|---:|
| Python F32 | 273.58 ms | 0.0536 | 5,604 MiB |
| C++ F32 | 277.47 ms | 0.0544 | 3,012 MiB |

C++ F32 has similar latency to Python while using less peak VRAM in this
measurement. These results do not establish the same trade-off for every input
or backend.

## Long Recordings

The 327.6-second `qwen3_tts_longform_asr_input.wav` fixture uses **10-second
chunks with 1-second overlap in both implementations**. Same measurement
method as above. This is chunked processing, not full-recording parity.

| Path | Inference time | RTF | Peak VRAM |
|---|---:|---:|---:|
| Python F32 | 9.839 s | 0.0300 | 5,074 MiB |
| C++ F32 | 10.555 s | 0.0322 | 3,008 MiB |

## Usage

```bash
audiocpp_cli --task s2s --family reuse \
  --model /path/to/RE-USE-GGUF/reuse-f32.gguf --backend cuda \
  --audio input.wav --out restored.wav --log
```

Input audio must be 8-48 kHz and longer than 20 ms. Output retains the input
sample rate, channels, and length. Channels are processed independently.

For long recordings, optional overlapping chunks bound graph workspace:

```bash
--request-option audio_chunk_duration_sec=10 \
--request-option audio_chunk_overlap_sec=1
```

Chunking changes bidirectional and normalization context and can change output
quality. It is not equivalent to full-recording inference. Input and output
audio still occupy host memory proportional to recording length.

See the [model usage guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/community_models/reuse.md)
for options and batching.

## License

The weights retain the [NVIDIA One-Way Noncommercial License (NSCLv1)](LICENSE)
specified by the upstream model card. Conversion does not replace those terms.
