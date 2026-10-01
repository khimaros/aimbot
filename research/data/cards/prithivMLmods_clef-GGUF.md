---
library_name: transformers
base_model:
- Cloudflare/clef
tags:
- text-generation-inference
- llama-cpp
- clef
- cloudflare
- systemone
- qwen3.8
- post-train
- image-text-to-typed-output
- multimodal
- structured-output
- classification
- custom-code
license: apache-2.0
language:
- en
pipeline_tag: image-text-to-text
---

# **clef-GGUF**

> Clef is Cloudflare's 27B multimodal decision model, post-trained from Qwen/Qwen3.8-27B (as listed in the card) and released under Apache-2.0. It is the larger sibling of Clef-Flash. Instead of generating free-form text, it reads a state (text, JSON, images, or video) plus a schema of typed questions (`noul` true/false, `choice`, or `score`). In a single forward pass, a small joint schema head on the backbone's final hidden states outputs a logit for every allowed option of every question, and a per-question softmax gives probabilities, so no output parsing is needed. It is compatible with the Jev/SystemOne API through the `systemone` helper and supports mixed text and multimodal batches, with a default input limit of 16,384 tokens. On the Decision Index 0.2.1 suite, it posts the best scores on benchmarks such as ToolRet, BANKING77, CLINC150+OOS (97.4 macro-F1, far above Clef-Flash's 66.8), GSM8K, ChessBench, ACOS, CRUXEval, and RAGTruth. It trails Jev on GPQA Diamond, MMLU-Pro, BBH, HoVer, and When2Call. Its median latency is 209.3 ms, slower than Clef-Flash (38.8 ms) but faster than Jev (524.1 ms). On the Typesafe workflow evals it is strongest on invoice processing (64.7 exact actions, 86.2 primary action) and security incidents, and roughly on par elsewhere.

## Model Files

| File Name | Quant Type | File Size | File Link | Description |
|-----------|------------|-----------|-----------|-------------|
| clef.BF16.gguf | BF16 | 53.8 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.BF16.gguf) | Full BF16 weights. Highest quality, largest file size. |
| clef.Q4_K_M.gguf | Q4_K_M | 16.5 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q4_K_M.gguf) | Good quality, default size for most use cases, *recommended*. |
| clef.Q5_K_M.gguf | Q5_K_M | 19.2 GB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.Q5_K_M.gguf) | High quality, *recommended*. |
| clef.mmproj-bf16.gguf | mmproj-bf16 | 931 MB | [Link](https://huggingface.co/prithivMLmods/clef-GGUF/blob/main/clef.mmproj-bf16.gguf) | Multimodal projection file in BF16 format. Used for vision/language models. |

## llama.cpp

LLM inference in C/C++ — https://github.com/ggml-org/llama.cpp