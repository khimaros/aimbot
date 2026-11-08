---
language:
- en
- zh
license: apache-2.0
library_name: diffusers
pipeline_tag: text-to-audio
base_model:
- Qwen/Qwen3-1.7B
tags:
- text-to-audio
- diffusion
- flow-matching
- sound-effects
- audio-generation
---

# MOSS-SoundEffect-V2.0

<p align="center">
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/openmoss_x_mosi" height="50" align="middle" />
</p>

<div align="center">
  <a href="https://github.com/OpenMOSS/MOSS-TTS/tree/main/moss_soundeffect_v2"><img src="https://img.shields.io/badge/Project%20Page-GitHub-blue"></a>
</div>

**MOSS-SoundEffect v2.0** is a text-to-audio model with a Diffusion Transformer (DiT) backbone trained with the Flow Matching objective, paired with a DAC VAE and a Qwen3 text encoder. It generates high-fidelity environmental, urban, creature, and human-action sound effects from natural-language prompts, with controllable duration up to 30 seconds at 48 kHz.

## 1. Overview

### 1.1 TTS Family Positioning

Within the MOSS-TTS Family, MOSS-SoundEffect is the dedicated **text-to-sound** model — the family member that turns natural-language captions into non-speech audio (ambience, urban scenes, creatures, human actions, short music-like clips). v2.0 supersedes the v1 discrete-token autoregressive backbone (`MossTTSDelay`) with a continuous-latent **Diffusion Transformer + Flow Matching** design.

### 1.2 Key Capabilities

- **Broad SFX coverage**: natural environments, urban environments, animals & creatures, human actions, and short musical/percussive clips.
- **Long-form generation**: stable audio up to **30 seconds** per call with the duration tag prepended to the prompt at training time.
- **Bilingual prompts**: trained with both **English and Chinese** captions.

### 1.3 Released Models

| Model | Architecture | DiT Variant | Parameters |
|---|---|---|---:|
| **MOSS-SoundEffect-V2.0** | DiT + Flow Matching | `1.3B` | 1.3B |

**Recommended inference hyperparameters**

| Parameter | Default | Description |
|---|---:|---|
| `num_inference_steps` | 100 | Number of flow-match solver steps. |
| `cfg_scale` | 4.0 | Classifier-free guidance weight. |
| `sigma_shift` | 5.0 | Flow-match scheduler shift applied per call. |
| `seconds` | 10.0 | Output duration. Up to 30. |

## 2. Quick Start

### Environment Setup

We recommend a clean, isolated Python 3.12 environment to avoid dependency conflicts with the top-level MOSS-TTS environment.

```bash
conda create -n moss-soundeffect-v2 python=3.12 -y
conda activate moss-soundeffect-v2

git clone https://github.com/OpenMOSS/MOSS-TTS.git
cd MOSS-TTS/moss_soundeffect_v2
pip install --extra-index-url https://download.pytorch.org/whl/cu128 \
    -e ".[torch-cu128,finetune]"
```

For a minimal **inference-only** install (still ships the Gradio demo; skips the fine-tuning extras):

```bash
pip install --extra-index-url https://download.pytorch.org/whl/cu128 \
    -e ".[torch-cu128]"
```

### Basic Usage

```python
import torch
from moss_soundeffect_v2 import MossSoundEffectPipeline

pipe = MossSoundEffectPipeline.from_pretrained(
    "OpenMOSS-Team/MOSS-SoundEffect-v2.0",   # this repo, or a local dir
    torch_dtype=torch.bfloat16,
    device="cuda",
)

audio = pipe(
    prompt="A dog barking loudly in a park.",
    seconds=10,
    num_inference_steps=100,
    cfg_scale=4.0,
)                                            # (B, C, T) waveform tensor
pipe.save_audio(audio, "out.wav")
```

> The underlying DiT is wrapped with `torch.compile` + Triton CUDA Graph. The first call may take a few minutes to compile. If you hit `TorchDynamo` / Triton errors, set `TORCHDYNAMO_DISABLE=1` before launching Python.

For a Gradio demo and fine-tuning recipes, see the [GitHub README](https://github.com/OpenMOSS/MOSS-TTS/tree/main/moss_soundeffect_v2#readme).
