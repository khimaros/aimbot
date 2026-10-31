---
library_name: gguf
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: text-generation
tags:
- liquid
- lfm3
- gguf
- llama.cpp
language:
- en
- ar
- zh
- fr
- de
- it
- ja
- ko
- pt
- es
- vi
- th
- id
- hi
- ru
- pl
base_model: LiquidAI/LFM3-1.7B
---

<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/api.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/try.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/docs.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/lfm3" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/LFM3-1.7B/resolve/main/assets/icons/blog.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>


# LFM3-1.7B-GGUF

GGUF version of [LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) for local inference on CPUs and GPUs.

Find architecture and usage details in the [original model card](https://huggingface.co/LiquidAI/LFM3-1.7B).

## How to run LFM3-1.7B
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

Recommended sampling: temperature 0.1, top_k 50, repeat penalty 1.1. For math and science: temperature 1.0, top_p 0.95, top_k 20.

- [Llama.app](https://llama.app) (**Use this model > Llama** in the menu), for macOS and Windows. Requires llama.cpp version [v0.8.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.8.0) or newer.
- [LM Studio](https://lmstudio.ai) (**Use this model > LM Studio** in the menu), for macOS, Windows and Linux. Requires LM Studio with llama.cpp engine 2.65.1 or newer.
- [Ollama](https://ollama.com) (`ollama run lfm3`), for macOS. Requires Ollama version [v0.40.12](https://github.com/ollama/ollama/releases/tag/v0.40.12) or newer.

## Use with llama.cpp
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

> [!NOTE]
> Supported in [llama.cpp](https://github.com/ggml-org/llama.cpp) [b11960](https://github.com/ggml-org/llama.cpp/releases/tag/b11960) ([v0.8.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.8.0)) and newer.

Add a quantization tag to pick a file.

```bash
llama-cli -hf LiquidAI/LFM3-1.7B-GGUF:Q4_K_M \
  --temp 0.1 --top-k 50 --repeat-penalty 1.1
```

For math and science, use `--temp 1.0 --top-p 0.95 --top-k 20` instead. More options in the [llama.cpp guide](https://docs.liquid.ai/deployment/on-device/llama-cpp).

## QAD Q4_0 GGUF
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

The Q4_0 build in this repository is the Quantization-Aware Distillation (QAD) checkpoint,
[`LFM3-1.7B-QAD-Q4_0.gguf`](https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF/blob/main/LFM3-1.7B-QAD-Q4_0.gguf).
It was trained to recover the accuracy lost to Q4_0 quantization.

Example usage with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```bash
llama-cli -hf LiquidAI/LFM3-1.7B-GGUF \
  --hf-file LFM3-1.7B-QAD-Q4_0.gguf \
  --temp 0.1 --top-k 50 --repeat-penalty 1.1
```
