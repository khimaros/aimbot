---
license: other
license_name: mixed-openmdw-and-nvidia-noncommercial
license_link: https://huggingface.co/audio-cpp/RE-USE-GGUF/blob/main/README.md#license
base_model:
  - nvidia/NVIDIA-NemotronLabs-RE-USE
  - nvidia/Real-time_RE-USE
base_model_relation: quantized
library_name: audio.cpp
pipeline_tag: audio-to-audio
tags:
  - audio.cpp
  - gguf
  - speech-enhancement
  - streaming
  - language-agnostic
---

# RE-USE GGUF

Follow or star [audio.cpp](https://github.com/0xShug0/audio.cpp) for the native
C++ runtime, model support, and updates.

This repository contains the original **RE-USE** checkpoint, the two newer,
commercial-friendly **NVIDIA NemotronLabs RE-USE** checkpoints, and causal
**Real-time RE-USE** for streaming enhancement. The NemotronLabs
variants use OpenMDW-1.1; the original checkpoint retains its noncommercial license.

Offline RE-USE restores degraded speech using a convolutional encoder/decoder and 30
bidirectional time-frequency Mamba blocks. All three offline variants use audio.cpp's existing
`reuse` family. Each GGUF embeds its configuration and model spec; no separate
encoder, tokenizer, or configuration file is required.

## Packages and pinned upstream checkpoints

| GGUF | Upstream checkpoint | Revision |
|---|---|---|
| `reuse-f32.gguf` | [Original RE-USE](https://huggingface.co/nvidia/RE-USE) | [`022e920`](https://huggingface.co/nvidia/RE-USE/tree/022e920d727347a64d6c21fbf0628f2a5f37ad78) |
| `reuse-nemotronlabs-f32.gguf` | [NVIDIA-NemotronLabs-RE-USE](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-RE-USE) | [`31f82f2`](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-RE-USE/tree/31f82f2efad1095034492f236e8dac9239ba713b) |
| `reuse-laughter-f32.gguf` | [NVIDIA-NemotronLabs-RE-USE-laughter](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-RE-USE-laughter) | [`1b1521d`](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-RE-USE-laughter/tree/1b1521dd659608e1e063ada83e0acfe1da473a8b) |
| `realtime-reuse-f32.gguf` | [Real-time RE-USE](https://huggingface.co/nvidia/Real-time_RE-USE) | [`4c0c186`](https://huggingface.co/nvidia/Real-time_RE-USE/tree/4c0c186272ca853cd18d832fc5c28777b62f32d1) |

Use the laughter variant when better preservation of laughter is desired.
Each offline GGUF is approximately 38 MiB and retains all 1,416 F32 tensors byte-for-byte
from its upstream checkpoint. The laughter configuration is unwrapped during
conversion to match the existing runtime's configuration layout.

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
  --model models/RE-USE-GGUF/reuse-nemotronlabs-f32.gguf --backend cuda \
  --audio input.wav --out restored.wav --log
```

For the laughter variant, select `reuse-laughter-f32.gguf` instead.

Input audio must be 8–48 kHz and longer than 20 ms. Output retains the input
sample rate, channels, and length. Channels are processed independently.
This is offline speech restoration, not streaming inference.

For long recordings, optional overlapping chunks bound graph workspace:

```bash
--request-option audio_chunk_duration_sec=10 \
--request-option audio_chunk_overlap_sec=1
```

Chunking changes bidirectional and normalization context and can change the
output. It is not equivalent to full-recording inference. Input and output audio
still occupy host memory proportional to recording length.

See the [model usage guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/reuse.md)
for options and batching, and the [converter](https://github.com/0xShug0/audio.cpp/blob/main/tests/reuse/convert_reuse_gguf.py)
for reproducible conversion.

## Real-time RE-USE

`realtime-reuse-f32.gguf` uses the separate `realtime_reuse` family. It is a
causal checkpoint with offline enhancement and incremental waveform streaming,
not another weight variant of the bidirectional offline model. All 1,318
checkpoint tensors are preserved exactly in F32. The upstream NVIDIA One-Way
Noncommercial License applies.

### Usage

Mono input at 8–48 kHz is supported; output preserves its sample rate and length.

```bash
audiocpp_cli --task s2s --family realtime_reuse \
  --model realtime-reuse-f32.gguf --backend cuda --threads 8 \
  --audio noisy.wav --out restored.wav --log
```

Add `--mode streaming` for incremental processing. Session options
`realtime_reuse.exit_layer=3..12` and `realtime_reuse.lookahead_frames=0..2`
select the 30 trained quality/latency configurations. Defaults are exit layer 8
and zero lookahead.

### CUDA performance

RTX 5090, eight host threads, a 14.07-second mono 24 kHz input, exit layer 8,
zero lookahead, one warmup followed by two warm requests. Both implementations
use the original F32 checkpoint. VRAM is the sampled process peak, including
runtime allocations.

| Mode | audio.cpp warm RTF | Official Python warm RTF | audio.cpp peak VRAM | Python peak VRAM |
|---|---:|---:|---:|---:|
| Streaming | 0.0272 | 0.340 | 1,033 MiB | 854 MiB |
| Offline | 0.0119 | 0.00622 | 967 MiB | 3,748 MiB |

Streaming is approximately 12.5× faster; warm first-audio latency through the
local streaming HTTP API is approximately 7–8 ms. audio.cpp starts with single
frames, then grows to 2, 4, and 8 frames, caching each graph size. At steady state,
eight frames correspond to approximately 160 ms of live input. RTF excludes real-time pacing
of the input. Python's online script processes network frames individually but
precomputes the complete recording's STFT and reconstructs the waveform at the
end. audio.cpp performs incremental STFT and overlap-add synthesis.

Offline audio.cpp uses bounded causal blocks to reduce GPU memory; Python is
faster for this offline input. Streaming processing state is bounded, while the
standard final-result interface also collects emitted audio in host memory.

### Streaming across GPU backends

F32 weights on RTX 5090, eight host threads, 14.07-second mono 24 kHz input,
exit layer 8, zero lookahead. Results average two requests after one warmup.
TTFA is measured at the HTTP client with prerecorded input; live capture adds
input-buffering latency. Peak VRAM is sampled per process.

| Backend | Warm TTFA | Warm RTF | Peak VRAM |
|---|---:|---:|---:|
| CUDA | 7.46 ms | 0.02703 | 1,033 MiB |
| Vulkan | 14.94 ms | 0.04918 | 511 MiB |

## License

- `reuse-nemotronlabs-f32.gguf` and `reuse-laughter-f32.gguf`: [OpenMDW-1.1](LICENSE).
- Original `reuse-f32.gguf`: [NVIDIA One-Way Noncommercial License](LICENSE-original).
- `realtime-reuse-f32.gguf`: [upstream NVIDIA One-Way Noncommercial License](https://huggingface.co/nvidia/Real-time_RE-USE/tree/4c0c186272ca853cd18d832fc5c28777b62f32d1).
