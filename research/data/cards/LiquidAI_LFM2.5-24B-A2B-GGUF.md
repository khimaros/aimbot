---
library_name: gguf
license: other
license_name: lfm1.0
license_link: LICENSE
language:
- en
- ar
- zh
- fr
- de
- ja
- ko
- es
- pt
- it
pipeline_tag: text-generation
base_model: LiquidAI/LFM2.5-24B-A2B
tags:
- liquid
- lfm2.5
- gguf
- llama.cpp
---

<div align="center">
  <img
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> •
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> •
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# LFM2.5-24B-A2B-GGUF

LFM2 is a new generation of hybrid models developed by [Liquid AI](https://www.liquid.ai/), specifically designed for edge AI and on-device deployment. It sets a new standard in terms of quality, speed, and memory efficiency.

Find more details in the original model card: https://huggingface.co/LiquidAI/LFM2.5-24B-A2B

## 🏃 How to run LFM2

Example usage with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```
llama-cli -hf LiquidAI/LFM2.5-24B-A2B-GGUF \
    --temp 0.1 --top-k 50 --repeat-penalty 1.05
```

The sampling parameters are the ones recommended for the base model (its `generation_config.json`); each GGUF also carries them as `general.sampling.*` metadata, so llama.cpp applies them by default.

## QAD Q4_0 GGUF

The Q4_0 build in this repository is the Quantization-Aware Distillation (QAD) checkpoint,
[`LFM2.5-24B-A2B-QAD-Q4_0.gguf`](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-GGUF/blob/main/LFM2.5-24B-A2B-QAD-Q4_0.gguf).
It was trained to recover the accuracy lost to Q4_0 quantization.

Example usage with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```
llama-cli -hf LiquidAI/LFM2.5-24B-A2B-GGUF \
    --hf-file LFM2.5-24B-A2B-QAD-Q4_0.gguf \
    --temp 0.1 --top-k 50 --repeat-penalty 1.05
```
