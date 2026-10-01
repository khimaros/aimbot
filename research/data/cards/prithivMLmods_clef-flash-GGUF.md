---
base_model:
- Cloudflare/clef-flash
tags:
- text-generation-inference
- llama-cpp
- clef
- cloudflare
- systemone
- qwen3.5
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
library_name: transformers
---

# **clef-flash-GGUF**

> Clef-Flash is Cloudflare's 9B-parameter multimodal decision model, post-trained from Qwen/Qwen3.5-9B (Apache-2.0). Instead of generating free-form text, it takes a state (text, JSON, images, or video) plus a schema of typed questions (`noul` true/false, `choice`, or `score`) and, in a single forward pass, outputs a logit for every allowed option of every question via a joint schema head on top of the backbone's final hidden states. A per-question softmax then gives probabilities, so no output parsing is needed. It is compatible with the Jev/SystemOne API (`systemone` helper) and supports mixed text and multimodal batches. On the Decision Index 0.2.1 suite it leads or ties on many benchmarks (e.g., BFCL, API-Bank, ARC, WinoGrande, HellaSwag, MuSR, CLadder, ForecastBench) and has a much lower median latency (38.8 ms) than its larger sibling Clef (209.3 ms). It trails on others such as CLINC150, RAGTruth, GSM8K, POP909-CL, GPQA Diamond, and MMLU-Pro. Workflow evals show it roughly on par with Clef and Jev, being best on customer service and slightly behind on invoice processing.

## Model Files

| File Name | Quant Type | File Size | File Link | Description |
|-----------|------------|-----------|-----------|-------------|
| clef-flash.BF16.gguf | BF16 | 17.9 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.BF16.gguf) | Full BF16 weights. Highest quality, largest file size. |
| clef-flash.F16.gguf | F16 | 17.9 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.F16.gguf) | Full FP16 weights. Highest quality, same size as BF16. |
| clef-flash.Q3_K_L.gguf | Q3_K_L | 4.93 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q3_K_L.gguf) | Lower quality but usable, good for low RAM availability. |
| clef-flash.Q3_K_M.gguf | Q3_K_M | 4.62 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q3_K_M.gguf) | Low quality. |
| clef-flash.Q4_K_M.gguf | Q4_K_M | 5.63 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q4_K_M.gguf) | Good quality, default size for most use cases, *recommended*. |
| clef-flash.Q4_K_S.gguf | Q4_K_S | 5.35 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q4_K_S.gguf) | Slightly lower quality with more space savings, *recommended*. |
| clef-flash.Q5_K_M.gguf | Q5_K_M | 6.47 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q5_K_M.gguf) | High quality, *recommended*. |
| clef-flash.Q5_K_S.gguf | Q5_K_S | 6.31 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q5_K_S.gguf) | High quality, *recommended*. |
| clef-flash.Q6_K.gguf | Q6_K | 7.36 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q6_K.gguf) | Very high quality, near perfect, *recommended*. |
| clef-flash.Q8_0.gguf | Q8_0 | 9.53 GB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.Q8_0.gguf) | Extremely high quality, generally unneeded but max available quant. |
| clef-flash.mmproj-bf16.gguf | mmproj-bf16 | 922 MB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.mmproj-bf16.gguf) | Multimodal projection file in BF16 format. Used for vision/language models. |
| clef-flash.mmproj-f16.gguf | mmproj-f16 | 922 MB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.mmproj-f16.gguf) | Multimodal projection file in FP16 format. Used for vision/language models. |
| clef-flash.mmproj-q8_0.gguf | mmproj-q8_0 | 624 MB | [Link](https://huggingface.co/prithivMLmods/clef-flash-GGUF/blob/main/clef-flash.mmproj-q8_0.gguf) | Multimodal projection file in Q8_0 quantization. Smaller size for vision capabilities. |

## llama.cpp

LLM inference in C/C++ — https://github.com/ggml-org/llama.cpp