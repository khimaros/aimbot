---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE
pipeline_tag: image-text-to-text
base_model:
- Qwen/Qwen3.5-9B
tags:
- qwen3.5
- byteshape
---

# Qwen3.5-9B GGUF (ShapeLearn Quantized)

This is a GGUF-quantized version of Qwen3.5-9B produced with **ByteShape's ShapeLearn**, which learns the optimal datatype per tensor to maintain high quality even at very low bitlengths.

To learn more about ShapeLearn and to see detailed benchmarks across GPUs, CPUs, and even the Raspberry Pi, please visit our [blog](https://byteshape.com/blogs/Qwen3.5-9B/).

If you have questions or want to share feedback, reach us on [Reddit](https://www.reddit.com/r/ByteShape/).

## Quick Start

Pick a model from the tables below and click **Get llama.cpp command** to get a ready-to-run command with all the correct sampling parameters for this model.

You can also copy the **Model Tag** from the table and use it directly:

| Tool | Command |
|------|---------|
| **llama.cpp** | `llama-server -hf <MODEL_TAG> --mmproj-auto` |

This is a **vision capable** model. llama.cpp auto-downloads the model and vision projector on first run.

Once you run the llama-server, you can access the web interface at `http://localhost:<PORT>`.


> **Note on Ollama:** As of this release, Ollama does not support Qwen3.5-9B based on Llama.cpp GGUFs. We suggest using [llama.cpp](https://github.com/ggml-org/llama.cpp) or [LM Studio](https://lmstudio.ai/) as an alternative.


## How to Pick a Model

We provide **CPU and GPU optimized variants** for llama.cpp:

- **GPUs:** optimized with a hybrid approach combining KQ and IQ quantization for better throughput.
- **CPUs:** optimized with predominantly KQ quantization.

Each hardware target includes a range of models covering different size and quality tradeoffs.

The chart below shows **quality versus tokens per second (TPS)**, with Unsloth used as the baseline for comparison.
Quality is measured across seven benchmarks, including function calling: BFCL-V3, LiveCodeBench V6, HumanEval, GSM8K, IFEVAL and MMLU, and GSM8K_V in both thinking and instruct modes.

**Selection rule:** Choose the model with the highest quality at your target throughput or the fastest model that still meets your required quality.

### GPU Models
Interactive plots for RTX 5090, 4080, 3090, 5060Ti are available [here](https://byteshape.com/blogs/Qwen3.5-9B/).

![GPU Benchmark - RTX 5090](img/RTX5090.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size | Use This Model | Model Tag |
|---------|-------------|-----------|-----|-----------|
| [GPU-1](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-2.81bpw.gguf) | 2.81 | 3.15 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-2.81bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-2.81bpw.gguf` |
| [GPU-2](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-3.00bpw.gguf) | 3.00 | 3.37 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.00bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.00bpw.gguf` |
| [GPU-3](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-3.15bpw.gguf) | 3.15 | 3.53 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.15bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.15bpw.gguf` |
| [GPU-4](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ4_XS-3.60bpw.gguf) | 3.60 | 4.04 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-3.60bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-3.60bpw.gguf` |
| [GPU-5](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ4_XS-4.20bpw.gguf) | 4.20 | 4.71 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.20bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.20bpw.gguf` |
| [GPU-6](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ4_XS-4.43bpw.gguf) | 4.43 | 4.97 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.43bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.43bpw.gguf` |
| [GPU-7](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q5_K_S-5.10bpw.gguf) | 5.10 | 5.72 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-5.10bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-5.10bpw.gguf` |


### CPU Models
Interactive plots for Ryzen 9 5900X, Intel Core i7 12700KF, Intel Ultra 7 265KF, and Raspberry Pi 5 are available [here](https://byteshape.com/blogs/Qwen3.5-9B/).
![CPU Benchmark - Ryzen 9 5900X](img/Ryzen9.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size | Use This Model | Model Tag |
|---------|-------------|-----------|-----|-----------|
| [CPU-1](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-2.81bpw.gguf) | 2.81 | 3.15 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-2.81bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-2.81bpw.gguf` |
| [CPU-2](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-3.00bpw.gguf) | 3.00 | 3.37 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.00bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.00bpw.gguf` |
| [CPU-3](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ3_S-3.15bpw.gguf) | 3.15 | 3.53 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.15bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ3_S-3.15bpw.gguf` |
| [CPU-4](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q3_K_S-3.46bpw.gguf) | 3.46 | 3.88 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q3_K_S-3.46bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q3_K_S-3.46bpw.gguf` |
| [CPU-5](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ4_XS-3.60bpw.gguf) | 3.60 | 4.04 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-3.60bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-3.60bpw.gguf` |
| [CPU-6](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q4_K_S-3.92bpw.gguf) | 3.92 | 4.4 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q4_K_S-3.92bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q4_K_S-3.92bpw.gguf` |
| [CPU-7](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-IQ4_XS-4.20bpw.gguf) | 4.20 | 4.71 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.20bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-IQ4_XS-4.20bpw.gguf` |
| [CPU-8](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q5_K_S-4.60bpw.gguf) | 4.60 | 5.16 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-4.60bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-4.60bpw.gguf` |
| [CPU-9](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q5_K_S-4.75bpw.gguf) | 4.75 | 5.32 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-4.75bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-4.75bpw.gguf` |
| [CPU-10](https://huggingface.co/byteshape/Qwen3.5-9B-GGUF/blob/main/Qwen3.5-9B-Q5_K_S-5.10bpw.gguf) | 5.10 | 5.72 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-5.10bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-9B-GGUF:Qwen3.5-9B-Q5_K_S-5.10bpw.gguf` |

## Notes on quantization labels

The labels you see (for example `IQ4_XS`) are only there to make Hugging Face show our models in the GGUF table. We do not use the conventional quantization profiles as defined in llama.cpp. In our case, these labels indicate the primary quantization approach and average bit length. Note that both KQ and IQ models may use a mix of quantization techniques optimized for their target hardware, which is why several models can share the same tag.
