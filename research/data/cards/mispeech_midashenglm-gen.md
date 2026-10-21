---
library_name: transformers
tags:
  - audio-generation
  - text-to-audio
  - flow-matching
  - dasheng
pipeline_tag: text-to-audio
license: apache-2.0
---

<div align="center">
    <h1>
    MiDashengLM-Gen
    </h1>
    <b><em>Unified Audio Scene Generation via LLM-Driven Autoregressive Flow Matching</em></b>
</div>

[![arXiv](https://img.shields.io/badge/arXiv-2608.11804-b31b1b)](https://arxiv.org/abs/2608.11804)&nbsp;&nbsp;[![HuggingFace Model](https://img.shields.io/badge/HuggingFace-Model-FFD21E)](https://huggingface.co/mispeech/midashenglm-gen)&nbsp;&nbsp;[![Demo Page](https://img.shields.io/badge/Demo-Page-0366d6)](https://xingws.github.io/midashenglm-gen-demo/)&nbsp;&nbsp;[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717)](https://github.com/xiaomi-research/midashenglm-gen)

**English** | **[中文](README_zh.md)**

MiDashengLM-Gen is an end-to-end framework that uses a pre-trained Large Language Model and audio tokenizer as the backbone, combined with per-token conditional flow matching for **autoregressive, variable-length mixed-audio scene generation**. It generates coherent 16 kHz audio scenes that simultaneously blend speech, music, sound effects, and environmental acoustics from structured text descriptions.

## Architecture

![Architecture](assets/architecture.png)

*Left: training pipeline with flow matching loss. Right: autoregressive inference pipeline.*

**Key components:**

| Component | Details |
|-----------|---------|
| **Audio Tokenizer** | DashengTokenizer → 768-dim latents @ 25 Hz, downsampled to 5 Hz via audio projector |
| **LLM Backbone** | Qwen3-1.7B, fully fine-tuned |
| **Flow Matching DiT** | 16 layers, hidden dim 2048, 8 heads, MLP ratio 4.0 |
| **Inference** | 10-step Euler ODE solver, CFG scale 2.0 |
| **Stop Head** | Learned binary classifier for variable-length truncation |
| **Output** | 16 kHz mono WAV, auto-truncated |

## Input Format

Input uses structured multi-view captions with special tokens to describe different aspects of an audio scene. Use `<|unknown|>` for absent elements.

| Token | Description | Example |
|-------|-------------|---------|
| `<\|caption\|>` | Overall scene description | A comedian delivering a punchline followed by uproarious crowd laughter and an upbeat jazz band hit |
| `<\|asr\|>` | Speech transcript | And that is why I never buy cheap luggage anymore! |
| `<\|speech\|>` | Speaker characteristics (voice, emotion, style) | expressive comedic male voice |
| `<\|sfx\|>` | Sound effects | uproarious crowd laughter |
| `<\|music\|>` | Music description | sudden upbeat jazz band sting |
| `<\|env\|>` | Environment / ambience | intimate comedy club |

## Installation

```bash
pip install torch torchaudio "transformers>=4.51" einops safetensors soundfile tqdm numpy x-transformers
```

## Quick Start

```python
from transformers import AutoModel
import soundfile as sf

model = AutoModel.from_pretrained("mispeech/midashenglm-gen", trust_remote_code=True)
model = model.cuda()

result = model.generate(
    "<|caption|> A comedian delivering a punchline followed by uproarious crowd laughter and an upbeat jazz band hit "
    "<|asr|> And that is why I never buy cheap luggage anymore! "
    "<|speech|> expressive comedic male voice "
    "<|music|> sudden upbeat jazz band sting "
    "<|sfx|> uproarious crowd laughter "
    "<|env|> intimate comedy club"
)

sf.write("output.wav", result["audio"], result["sample_rate"])
```

### Batch Generation

```python
texts = [
    "<|caption|> A comedian delivering a punchline followed by uproarious crowd laughter and an upbeat jazz band hit <|asr|> And that is why I never buy cheap luggage anymore! <|speech|> expressive comedic male voice <|music|> sudden upbeat jazz band sting <|sfx|> uproarious crowd laughter <|env|> intimate comedy club",
    "<|caption|> Upbeat instrumental music with occasional whistling and low audio quality. <|asr|> <|unknown|> <|speech|> <|unknown|> <|sfx|> Intermittent whistling emerges in later segment alongside persistent instrumental playback. <|music|> Bright melodic composition with guitar, piano, and rhythmic percussion elements, maintaining a consistently upbeat character. <|env|> Low-fidelity recording with compressed dynamics and limited frequency response.",
]
result = model.generate(texts)
for i, audio in enumerate(result["audio"]):
    sf.write(f"output_{i}.wav", audio, result["sample_rate"])
```

### Generation Parameters

```python
result = model.generate(
    "...",
    eval_cfg=2.0,           # Classifier-free guidance scale
    stop_threshold=0.5,     # Stop prediction threshold
    min_stop_step=5,        # Minimum steps before stopping
    seed=42,                # Random seed for reproducibility
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `eval_cfg` | 2.0 | Classifier-free guidance scale |
| `stop_threshold` | 0.5 | Stop probability threshold for audio truncation |
| `min_stop_step` | 5 | Minimum generation steps before stopping |
| `seed` | None | Random seed for reproducibility |

## Citation

```bibtex
@article{sun2026midashenglmgen,
  title={MiDashengLM-Gen: Unified Audio Scene Generation via LLM-Driven Autoregressive Flow Matching},
  author={Sun, Xingwei and Dinkel, Heinrich and Li, Gang and Mei, Jiahao and Niu, Yadong and Han, Zerui and Jiang, Yuepeng and Zhou, Jiahao and Fan, Lichun and Luan, Jian},
  journal={arXiv preprint},
  eprint={2608.11804},
  archivePrefix={arXiv},
  year={2026}
}
```

## License

Apache 2.0

<small>

## Use Restrictions

You are solely responsible for your use of MiDashengLM-Gen and any outputs, actions, or consequences arising therefrom, and you agree not to use MiDashengLM-Gen or any derivatives thereof:

- For any unlawful, fraudulent, or malicious purpose, or in any manner that violates any applicable laws or regulations;
- To infringe upon the intellectual property rights, privacy rights, publicity rights, or other lawful rights or interests of any third party;
- To exploit, harm, harass, defame, unlawfully discriminate against, or otherwise adversely affect any individual or group, including minors or vulnerable persons;
- For any military purpose or application.

</small>
