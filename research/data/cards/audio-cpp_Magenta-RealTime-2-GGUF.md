---
license: cc-by-4.0
pipeline_tag: text-to-audio
tags:
  - audio.cpp
  - gguf
  - music-generation
base_model: google/magenta-realtime-2
---

# Magenta RealTime 2 — GGUF

Follow or star [audio.cpp](https://github.com/0xShug0/audio.cpp) for runtime
updates and new model support.

GGUF conversions of Google DeepMind's Magenta RealTime 2 Small (230M) and Base
(2.4B). Generate 48 kHz stereo instrumental music from text or audio style
conditioning, with optional note and drum control. Both variants support offline
and streaming generation through audio.cpp.

Upstream weights are pinned to
[`google/magenta-realtime-2@010aa0d`](https://huggingface.co/google/magenta-realtime-2/tree/010aa0dcb0dfd27b24f0ad07b4dad63e8f9521cc).
The port follows
[`magenta/magenta-realtime@694a545`](https://github.com/magenta/magenta-realtime/tree/694a545e4ba0b88bf1150137b129582166d3e07f).

| File | Generator matrices | Size |
|---|---|---:|
| `magenta-rt2-small-f16.gguf` | F16 | 1.42 GiB |
| `magenta-rt2-small-q8_0.gguf` | Q8_0 | 1.24 GiB |
| `magenta-rt2-base-f16.gguf` | F16 | 5.48 GiB |
| `magenta-rt2-base-q8_0.gguf` | Q8_0 | 3.41 GiB |

Download one GGUF. Each package includes the generator, SpectroStream codec,
MusicCoCa text/audio style encoder, mapper, quantizer, vocabulary, configuration,
and model spec. No external resources or Python runtime are needed for inference.
Q8_0 quantizes supported generator matrices; other matrices use F16 where needed.
Codec, MusicCoCa, normalization, bias, scale, and sink tensors remain F32.

## Quick start

```bash
hf download audio-cpp/Magenta-RealTime-2-GGUF \
  magenta-rt2-small-f16.gguf \
  --local-dir Magenta-RealTime-2-GGUF

audiocpp_cli --model Magenta-RealTime-2-GGUF/magenta-rt2-small-f16.gguf \
  --family magenta_realtime_2 --task gen --backend cuda \
  --text "disco funk" --request-option duration_sec=10 \
  --out music.wav --log
```

For Base, download and select `magenta-rt2-base-f16.gguf` instead, or choose either
`-q8_0.gguf` package. Use `--backend vulkan` or `--backend cpu` for another backend. Add `--mode streaming`
to emit audio in blocks of up to 160 ms while generation continues. Offline and
streaming use the same generation path and produce the same final waveform.

Replace the text prompt with `--audio style.wav` to condition on an audio example.
This transfers musical style; it does not continue the input recording.

| Request option | Default | Meaning |
|---|---:|---|
| `duration_sec` | `10` | Output duration, rounded up to 40 ms frames. |
| `seed` | `0` | Generation seed. |
| `temperature` | `1.3` | Sampling temperature; `0` is greedy. |
| `top_k` | `40` | Candidate limit; `0` keeps all 1024 valid codes. |
| `guidance_scale` | `3` | Style guidance, -1–7. |
| `note_guidance_scale` | `1` | Note guidance, -1–7. |
| `drum_guidance_scale` | `1` | Drum guidance, -1–7. |
| `use_mapper` | `true` | Map text style into audio embedding space. |
| `drums` | `-1` | Unspecified (`-1`), no drums (`0`), or drums (`1`). |
| `pianoroll_file` | unset | JSON array of 128 pitch states per 25 Hz frame. |

Set controls through `--request-option name=value`. See the
[model guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/magenta_realtime_2.md)
for pitch-state values and session options. Each request starts fresh music.

## Performance

RTX 5090, CUDA, eight host threads, one persistent session per model. After a
two-second warmup, generate three different 30-second styles and repeat the
first style. Both implementations use temperature 1.3, top-k 40, style guidance
3, note/drum guidance 1, the text mapper enabled, and seed 0.

Warm RTF averages the four measured requests, including style conditioning and
waveform generation. RTF is wall time divided by audio duration. Peak VRAM
includes model preparation and generation. Python uses its official `generate()`
path; every row measures complete waveform generation.

| Model | Runtime | Mode | RTF | Peak VRAM (MiB) |
|---|---|---|---:|---:|
| Small | Official Python | Official generation | 0.1359 | 24,626 |
| Small | audio.cpp F16 | Offline | 0.0861 | 2,146 |
| Small | audio.cpp F16 | Streaming | 0.0874 | 2,146 |
| Small | audio.cpp Q8_0 | Offline | 0.0833 | 1,954 |
| Small | audio.cpp Q8_0 | Streaming | 0.0831 | 1,954 |
| Base | Official Python | Official generation | 0.3714 | 16,946 |
| Base | audio.cpp F16 | Offline | 0.2376 | 6,336 |
| Base | audio.cpp F16 | Streaming | 0.2335 | 6,336 |
| Base | audio.cpp Q8_0 | Offline | 0.1789 | 4,218 |
| Base | audio.cpp Q8_0 | Streaming | 0.1789 | 4,218 |

### Streaming time to first audio

Under the same CUDA settings, TTFA includes text conditioning through the first
160 ms audio block and excludes model loading and preparation. Warm averages
cover the four requests after warmup.

| Model | First request TTFA | Warm average TTFA |
|---|---:|---:|
| Small F16 | 218 ms | 22.1 ms |
| Small Q8_0 | 242 ms | 21.4 ms |
| Base F16 | 262 ms | 46.9 ms |
| Base Q8_0 | 267 ms | 38.4 ms |

## Examples

Small F16 — “A gentle acoustic guitar with warm piano”:

<audio controls src="https://huggingface.co/audio-cpp/Magenta-RealTime-2-GGUF/resolve/main/examples/small-acoustic-piano.wav"></audio>

Base F16 — “A gentle acoustic guitar with warm piano”:

<audio controls src="https://huggingface.co/audio-cpp/Magenta-RealTime-2-GGUF/resolve/main/examples/base-acoustic-piano.wav"></audio>

## License

Original model and resources: Copyright 2026 Google LLC, CC-BY-4.0. These are
converted weights; the upstream attribution, license, and
[usage terms](https://huggingface.co/google/magenta-realtime-2/blob/010aa0dcb0dfd27b24f0ad07b4dad63e8f9521cc/README.md#terms-of-use)
continue to apply. audio.cpp inference code is Apache-2.0.
