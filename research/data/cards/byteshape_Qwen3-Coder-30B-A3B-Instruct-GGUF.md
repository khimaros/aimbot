---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct/blob/main/LICENSE
pipeline_tag: text-generation
base_model:
- Qwen/Qwen3-Coder-30B-A3B-Instruct
tags:
- qwen
- qwen3
- qwen3-coder
- byteshape
---

# Qwen3-Coder-30B-A3B-Instruct GGUF (ShapeLearn Quantized)

This is a GGUF-quantized version of Qwen3-Coder-30B-A3B-Instruct produced with **ByteShape's ShapeLearn**, which learns the optimal datatype per tensor to maintain high quality even at very low bitlengths.

To learn more about ShapeLearn and to see detailed benchmarks across GPUs, CPUs, and even the Raspberry Pi, please visit our [blog](https://byteshape.com/blogs/Devstral-Small-2-24B-Instruct-2512/).

If you have questions or want to share feedback, reach us on [Reddit](https://www.reddit.com/r/ByteShape/).


## How to Pick a Model

We provide **CPU and GPU optimized variants** for llama.cpp:

- **CPUs:** Models labeled as KQ, optimized for CPU inference with predominantly KQ quantization.
- **GPUs:** Models labeled as IQ, optimized for GPU inference with a hybrid approach combining KQ and IQ quantization for better throughput.

Each hardware target includes a range of models covering different size and quality tradeoffs.

The chart below shows **quality versus tokens per second (TPS)**, with Unsloth used as the baseline for comparison.
Quality is measured across five benchmarks, including function calling: BFCL-V3, LiveCodeBench V6, HumanEval, Math500, and GSM8K.

**Selection rule:** Choose the model with the highest quality at your target throughput or the fastest model that still meets your required quality.

### CPU Models

![CPU Benchmark - Intel](img/Intel.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size |
|---------|-------------|-----------|
| [KQ-1](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_S-2.65bpw.gguf) | 2.65 | 10.1 GB |
| [KQ-2](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_S-2.66bpw.gguf) | 2.66 | 10.2 GB |
| [KQ-3](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_S-2.69bpw.gguf) | 2.69 | 10.3 GB |
| [KQ-4](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_M-2.69bpw.gguf) | 2.69 | 10.3 GB |
| [KQ-5](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_S-2.90bpw.gguf) | 2.90 | 11.1 GB |
| [KQ-6](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_S-3.00bpw.gguf) | 3.00 | 11.5 GB |
| [KQ-7](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-Q3_K_M-3.31bpw.gguf) | 3.31 | 12.7 GB |
| [KQ-8](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ4_XS-4.20bpw.gguf) | 4.20 | 16.0 GB |


### GPU Models

![GPU Benchmark - RTX 5090](img/RTX5090.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size |
|---------|-------------|-----------|
| [IQ-1](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ3_S-2.66bpw.gguf) | 2.66 | 10.1 GB |
| [IQ-2](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ3_S-2.68bpw.gguf) | 2.68 | 10.2 GB |
| [IQ-3](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ3_S-2.83bpw.gguf) | 2.83 | 10.8 GB |
| [IQ-4](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ3_S-3.12bpw.gguf) | 3.12 | 11.9 GB |
| [IQ-5](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ3_S-3.48bpw.gguf) | 3.48 | 13.3 GB |
| [IQ-6](https://huggingface.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF/blob/main/Qwen3-Coder-30B-A3B-Instruct-IQ4_XS-4.20bpw.gguf) | 4.20 | 16.0 GB |

## Notes on quantization labels

The labels you see (for example `IQ4_XS`) are only there to make Hugging Face show our models in the GGUF table. We do not use the conventional quantization profiles as defined in llama.cpp. In our case, these labels indicate the primary quantization approach and average bit length. Note that both KQ and IQ models may use a mix of quantization techniques optimized for their target hardware, which is why several models can share the same tag.

## Running these models with Ollama

All GGUF files in this repo can be used directly with Ollama.

To run a model with Ollama, use:

```bash
ollama run hf.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF:FILE_NAME.gguf
```

Replace `FILE_NAME.gguf` with the GGUF filename you want. For example:

```bash
ollama run hf.co/byteshape/Qwen3-Coder-30B-A3B-Instruct-GGUF:Qwen3-Coder-30B-A3B-Instruct-IQ4_XS-4.20bpw.gguf
```
