---
license: other
license_name: mixed-upstream-licenses
license_link: https://github.com/deepinsight/insightface#license
tags:
  - audio.cpp
  - gguf
  - lip-sync
base_model: ByteDance/LatentSync-1.6
---

# LatentSync 1.6 for audio.cpp

Star or watch [audio.cpp on GitHub](https://github.com/0xShug0/audio.cpp)
for model integration and inference updates.

Use this package with [audio.cpp](https://github.com/0xShug0/audio.cpp).
It synchronizes lip motion in an existing video with supplied speech.

Upstream code is pinned to
[`a229c3948406bc2cf6eaf4873e662e70c6a04746`](https://github.com/bytedance/LatentSync/tree/a229c3948406bc2cf6eaf4873e662e70c6a04746).

> [!WARNING]
> This package contains InsightFace face detection and landmark
> weights restricted to non-commercial research. LatentSync's Apache-2.0 license
> does not override those terms. Review upstream licenses before redistribution
> or deployment.

Each GGUF includes the temporal diffusion U-Net, Whisper Tiny
audio encoder, SD VAE, SCRFD face detector, 106-point landmark model, face mask,
configuration sidecars, and embedded audio.cpp model spec. Inference requires
no Python or ONNX Runtime.

| File | Precision |
| --- | --- |
| `latentsync-1.6-q8_0-f16.gguf` (recommended) | Q8 U-Net linear weights; remaining weights F16. |
| `latentsync-1.6-f16.gguf` | F16. |
| `latentsync-1.6-f32-f16.gguf` | Original mixed F32/F16. |

## Full-Duration CUDA Example

This example uses the official LatentSync
[`demo1_video.mp4`](https://github.com/bytedance/LatentSync/blob/a229c3948406bc2cf6eaf4873e662e70c6a04746/assets/demo1_video.mp4)
and [`demo1_audio.wav`](https://github.com/bytedance/LatentSync/blob/a229c3948406bc2cf6eaf4873e662e70c6a04746/assets/demo1_audio.wav).
The complete 9.6-second speech recording is retained, not a shortened smoke clip.
The source video's original soundtrack is replaced by the supplied speech.
Regenerated on 2026-10-21 with audio.cpp
[`545b212f`](https://github.com/0xShug0/audio.cpp/commit/545b212f0e83d92c19e4433ebffdfa50f9e459b1).

<table>
<tr>
<td width="50%"><strong>audio.cpp Q8/F16 (recommended)</strong><br><video controls playsinline preload="metadata" width="100%" src="https://huggingface.co/audio-cpp/LatentSync-1.6-GGUF/resolve/main/examples/demo1/output-cuda-q8-f16-deepcache3.mp4"></video></td>
<td width="50%"><strong>audio.cpp F16</strong><br><video controls playsinline preload="metadata" width="100%" src="https://huggingface.co/audio-cpp/LatentSync-1.6-GGUF/resolve/main/examples/demo1/output-cuda-f16-deepcache3.mp4"></video></td>
</tr>
<tr>
<td width="50%"><strong>audio.cpp Original F32/F16</strong><br><video controls playsinline preload="metadata" width="100%" src="https://huggingface.co/audio-cpp/LatentSync-1.6-GGUF/resolve/main/examples/demo1/output-cuda-deepcache3.mp4"></video></td>
<td width="50%"><strong>Official Python output</strong><br><video controls playsinline preload="metadata" width="100%" src="https://huggingface.co/audio-cpp/LatentSync-1.6-GGUF/resolve/main/examples/demo1/output-python.mp4"></video></td>
</tr>
</table>

The Python reference was generated with the official LatentSync implementation
using the same demo video and speech. It is a generated result, not the source video.
All three audio.cpp outputs use DeepCache (`cache_interval=3`) and the supplied
reference speech below, replacing the source video's original soundtrack.

<audio controls preload="metadata" src="https://huggingface.co/audio-cpp/LatentSync-1.6-GGUF/resolve/main/examples/demo1/reference.wav"></audio>

[Download generated video](examples/demo1/output-cuda-q8-f16-deepcache3.mp4) |
[Official Python output](examples/demo1/output-python.mp4) |
[Source input video](examples/demo1/reference.mp4) |
[Reference speech](examples/demo1/reference.wav)

| Setting | Value |
| --- | --- |
| Backend / GPU | CUDA / NVIDIA GeForce RTX 5090 |
| Package | `latentsync-1.6-q8_0-f16.gguf`, native weight storage |
| Reference speech | 9.60 seconds, 16 kHz mono |
| Output | 1080x1920, 25 FPS, 242 frames (9.68 seconds) |
| Denoising | 20 steps, guidance 1.5, seed 1247 |
| Temporal chunk | 16 frames |
| DeepCache | Enabled (`cache_interval=3`) |
| Session time | 132.95 seconds |
| Video RTF | 13.73 |
| Full CLI wall time | 134.77 seconds |
| Peak VRAM | 9,144 MiB |
| Peak CPU RSS | 5,151.48 MiB |

The slightly longer video follows the model's audio-feature windowing. This
example was generated with the CUDA Debug build and DeepCache enabled,
without the optional cuDNN FP16 execution modes.
The run used eight CPU threads. Peak process memory was sampled every 20 ms
across loading and generation; session time excludes model loading, while
full CLI wall time includes loading and writing the raw-frame artifacts.
MP4 encoding is a separate step and is not included in either timing.

### Precision Comparison

Same full example and settings, with DeepCache enabled (`cache_interval=3`).
Each measurement is the first request in a fresh process, not a warmed average.
RTF uses the 9.68-second generated video duration.

| Package | Session time | Video RTF | Peak VRAM |
| --- | ---: | ---: | ---: |
| Q8/F16 (recommended) | 132.95 s | 13.73 | 9,144 MiB |
| F16 | 137.11 s | 14.16 | 9,974 MiB |
| Original F32/F16 | 155.77 s | 16.09 | 15,700 MiB |

[Download F16 video](examples/demo1/output-cuda-f16-deepcache3.mp4)

### DeepCache Comparison

Same full example, binary, inputs, seed and native precision; only
`cache_interval` changes. Each run is the first request in a fresh process.
RTF is session time divided by the 9.68-second generated video duration.

| DeepCache | Session time | Video RTF | Peak VRAM | Peak CPU RSS |
| --- | ---: | ---: | ---: | ---: |
| On (`cache_interval=3`) | 155.77 s | 16.09 | 15,700 MiB | 5,137.10 MiB |
| Off (`cache_interval=1`) | 294.19 s | 30.39 | 15,540 MiB | 5,162.53 MiB |

DeepCache is **1.89x faster** here, using **160 MiB more peak VRAM**.
No obvious visual degradation was observed in the inspected frames of this
example; this is not a quantitative quality evaluation or pixel-parity claim.

[Download DeepCache video](examples/demo1/output-cuda-deepcache3.mp4) |
[Download no-cache video](examples/demo1/output-cuda.mp4)

The command below reproduces the recommended Q8/F16 cached example.
The DeepCache comparison above uses the original F32/F16 package.

## Run

Install FFmpeg on PATH, then run:

```bash
audiocpp_cli --task gen --family latentsync \
  --model latentsync-1.6-q8_0-f16.gguf --backend cuda \
  --audio examples/demo1/reference.wav \
  --request-option reference_video_file=examples/demo1/reference.mp4 \
  --request-option num_inference_steps=20 \
  --request-option guidance_scale=1.5 \
  --request-option seed=1247 \
  --request-option cache_interval=3 \
  --out-dir outputs/latentsync --log
```

The CLI writes RGB24 frames and a small JSON metadata sidecar. MP4 encoding and audio muxing
are separate FFmpeg steps; see the [model guide](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/latentsync.md).

For these example inputs, encode the generated frames and add the speech with:

```bash
ffmpeg -f rawvideo -pixel_format rgb24 -video_size 1080x1920 -framerate 25 \
  -i outputs/latentsync/latentsync_video_rgb24.rgb \
  -i examples/demo1/reference.wav \
  -c:v libx264 -threads 4 -pix_fmt yuv420p -crf 18 \
  -c:a aac -movflags +faststart output.mp4
```

## Upstream Sources

- [LatentSync weights](https://huggingface.co/ByteDance/LatentSync-1.6)
- [LatentSync code](https://github.com/bytedance/LatentSync/tree/a229c3948406bc2cf6eaf4873e662e70c6a04746)
- [SD VAE](https://huggingface.co/stabilityai/sd-vae-ft-mse)
- [InsightFace license](https://github.com/deepinsight/insightface#license)

