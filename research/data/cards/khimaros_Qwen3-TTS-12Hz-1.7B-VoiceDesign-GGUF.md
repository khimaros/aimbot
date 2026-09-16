---
license: apache-2.0
pipeline_tag: text-to-speech
library_name: qwen-tts
tags:
- audio
- tts
- qwen
- multilingual
---

> **GGUF quantizations** for use with [qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (fork of [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp)).
> Converted from [Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign) using `scripts/convert_tts_to_gguf.py`.
> Available quants: F16, Q8_0.

# Qwen3-TTS

<br>

<p align="center">
    <img src="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/qwen3_tts_logo.png" width="400"/>
<p>

<p align="center">
&nbsp&nbsp🤗 <a href="https://huggingface.co/collections/Qwen/qwen3-tts">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://modelscope.cn/collections/Qwen/Qwen3-TTS">ModelScope</a>&nbsp&nbsp | &nbsp&nbsp📑 <a href="https://qwen.ai/blog?id=qwen3tts-0115">Blog</a>&nbsp&nbsp | &nbsp&nbsp📑 <a href="https://huggingface.co/papers/2601.15621">Paper</a>&nbsp&nbsp | &nbsp&nbsp💻 <a href="https://github.com/QwenLM/Qwen3-TTS">GitHub</a>
</p>

We release **Qwen3-TTS**, a series of powerful speech generation models developed by Qwen, offering comprehensive support for voice cloning, voice design, ultra-high-quality human-like speech generation, and natural language-based voice control.

## Overview
Qwen3-TTS covers 10 major languages (Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, and Italian) as well as multiple dialectal voice profiles. Key features:

* **Powerful Speech Representation**: Powered by the self-developed Qwen3-TTS-Tokenizer-12Hz, it achieves efficient acoustic compression and high-dimensional semantic modeling.
* **Universal End-to-End Architecture**: Utilizing a discrete multi-codebook LM architecture to bypass traditional information bottlenecks.
* **Extreme Low-Latency Streaming Generation**: Supports streaming generation with end-to-end synthesis latency as low as 97ms.
* **Intelligent Voice Control**: Supports speech generation driven by natural language instructions for flexible control over timbre, emotion, and prosody.

## Quickstart

### Environment Setup

Install the `qwen-tts` Python package from PyPI:

```bash
pip install -U qwen-tts
```

### Python Package Usage

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# Load the model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# Custom Voice Generation
wavs, sr = model.generate_custom_voice(
    text="其实我真的有发现，我是一个特别善于观察别人情绪的人。",
    language="Chinese",
    speaker="Vivian",
    instruct="用特别愤怒的语气说",
)
sf.write("output.wav", wavs[0], sr)
```

## Evaluation

Zero-shot speech generation on the Seed-TTS test set (Word Error Rate (WER, ↓)):

| Model | test-zh | test-en |
|---|---|---|
| Qwen3-TTS-12Hz-1.7B-Base | 0.77 | 1.24 |

## Citation

If you find our paper and code useful in your research, please consider giving a star ⭐ and citation 📝:

```BibTeX
@article{Qwen3-TTS,
  title={Qwen3-TTS Technical Report},
  author={Hangrui Hu and Xinfa Zhu and Ting He and Dake Guo and Bin Zhang and Xiong Wang and Zhifang Guo and Ziyue Jiang and Hongkun Hao and Zishan Guo and Xinyu Zhang and Pei Zhang and Baosong Yang and Jin Xu and Jingren Zhou and Junyang Lin},
  journal={arXiv preprint arXiv:2601.15621},
  year={2026}
}
```
