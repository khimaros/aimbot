---
license: apache-2.0
library_name: audio.cpp
base_model: Soul-AILab/SoulX-FlashHead-1_3B
base_model_relation: quantized
tags:
- audio.cpp
- gguf
- talking-head
- image-to-video
- audio-to-video
---

# SoulX-FlashHead Lite GGUF

Follow or star [audio.cpp](https://github.com/0xShug0/audio.cpp) for the C++ runtime and model integration updates.

GGUF packaging of [Soul-AILab/SoulX-FlashHead-1_3B](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B/tree/5fbd2e44ba08ab2deb28bd55cff2c15523e51ba5).
The model generates streaming talking-portrait video from a reference image and speech audio.
This repository packages **Lite** only, including its DiT, LTX video VAE and
[Wav2Vec2 speech encoder](https://huggingface.co/facebook/wav2vec2-base-960h).
Upstream checkpoint revision: `5fbd2e44ba08ab2deb28bd55cff2c15523e51ba5`.
Model architecture and weights are by Soul-AILab; the C++ integration is in audio.cpp.

> [!IMPORTANT]
> **cuDNN is strongly recommended for CUDA: about 2× faster warm inference, with lower peak VRAM.**
> **Prebuilt audio.cpp binaries do not include cuDNN support.** Build from source
> with cuDNN and `-DGGML_CUDA_CUDNN_CONV3D=ON`, then select
> `--session-option 'soulx_flashhead.exec_plan={"vae":{"impl":"cudnn"}}'`.
> The default GGML path remains available without cuDNN, including in prebuilts.

## English streaming demo

Generated from a single reference portrait and 42.24 seconds of English narration
using audio.cpp: Lite Q8, 512×512, four denoising steps, 25 FPS, Vulkan backend.
Audio is processed in 0.96-second chunks with continuous motion between chunks.

<video controls src="https://huggingface.co/audio-cpp/SoulX-FlashHead-GGUF/resolve/main/demo/english.mp4"></video>

Inputs: [English audio](demo/english.wav), [transcript](demo/english.txt),
and [portrait](demo/portrait.png). The portrait is from the
[upstream example](https://github.com/Soul-AILab/SoulX-FlashHead/blob/main/examples/girl.png).
The English narration was generated with Qwen3-TTS.

## audio.cpp CUDA performance

Measured on an RTX 5090 with the Q8 package, 512×512 output, four denoising steps,
and the 42.24-second English demo above (44 streaming chunks). Debug build,
eight CPU threads; the two modes were run sequentially.

| VAE implementation | Warm RTF ↓ | Full-run RTF ↓ | Peak VRAM |
|---|---:|---:|---:|
| cuDNN (recommended) | 0.215 | 0.430 | 5,168 MiB |
| GGML (default) | 0.490 | 0.706 | 9,152 MiB |

RTF is generation time divided by video duration; lower is faster. Warm RTF
covers the full audio-encoder, DiT, VAE, color-correction and RGB-output pipeline,
excluding the first two chunks and CLI artifact serialization. Full-run RTF also
includes initialization, cold chunks and CLI artifact serialization. Both exclude
model loading and MP4 encoding. Peak VRAM is sampled per-process GPU memory.
The cuDNN VAE uses F16 activations with F32 accumulation.

## Weights and usage

| File | Components |
|---|---|
| `SoulX-FlashHead-Lite-Q8_0.gguf` | Q8 DiT, BF16 LTX VAE, F32 Wav2Vec2, embedded configuration and model contract |
| `SoulX-FlashHead-Lite-BF16.gguf` | BF16 DiT and LTX VAE, F32 Wav2Vec2, embedded configuration and model contract |

```bash
audiocpp_cli --family soulx_flashhead --task gen \
  --model SoulX-FlashHead-Lite-Q8_0.gguf --backend cuda \
  --audio speech.wav --request-option reference_image_file=portrait.png \
  --mode streaming --out-dir outputs/flashhead \
  --log --log-file outputs/flashhead/run.log
```

For a cuDNN-enabled source build, add the following option to the command above:

```bash
--session-option 'soulx_flashhead.exec_plan={"vae":{"impl":"cudnn"}}'
```

Lite emits 24 RGB24 frames per chunk at 25 FPS. Streaming input is mono 16 kHz;
offline input is mixed down and resampled when needed. Default output is 512×512
with four denoising steps. Chunks retain motion continuity from the preceding output.

See the [usage and conversion documentation](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/soulx_flashhead.md).
