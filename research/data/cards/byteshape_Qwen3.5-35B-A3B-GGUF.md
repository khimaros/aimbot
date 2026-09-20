---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3.5-35B-A3B/blob/main/LICENSE
pipeline_tag: image-text-to-text
base_model:
- Qwen/Qwen3.5-35B-A3B
tags:
- qwen3.5
- byteshape
---

# Qwen3.5-35B-A3B GGUF (ShapeLearn Quantized)

This is a GGUF-quantized version of Qwen3.5-35B-A3B produced with **ByteShape's ShapeLearn**, which learns the optimal datatype per tensor to maintain high quality even at very low bitlengths.

To learn more about ShapeLearn and to see detailed benchmarks across GPUs, CPUs, and even the Raspberry Pi, please visit our [blog](https://byteshape.com/blogs/Qwen3.5-35B-A3B/).

We also prepared a tutorial on how to use these models for agentic coding: [Opencode Tutorial](https://byteshape.com/blogs/tutorial-opencode/).

If you have questions or want to share feedback, reach us on [Reddit](https://www.reddit.com/r/ByteShape/).

## Quick Start

Pick a model from the tables below and click **Get llama.cpp command** to get a ready-to-run command with all the correct sampling parameters for this model.

You can also copy the **Model Tag** from the table and use it directly:

| Tool | Command |
|------|---------|
| **llama.cpp** | `llama-server -hf <MODEL_TAG> --mmproj-auto` |

This is a **vision capable** model. llama.cpp auto-downloads the model and vision projector on first run.

Once you run the llama-server, you can access the web interface at `http://localhost:<PORT>`.


> **Note on Ollama:** As of this release, Ollama does not support Qwen3.5-35B-A3B based on Llama.cpp GGUFs. We suggest using [llama.cpp](https://github.com/ggml-org/llama.cpp) or [LM Studio](https://lmstudio.ai/) as an alternative.


## How to Pick a Model

We provide **CPU and GPU optimized variants** for llama.cpp:

- **GPUs:** optimized with a hybrid approach combining KQ and IQ quantization for better throughput.
- **CPUs:** optimized with predominantly KQ quantization.

Each hardware target includes a range of models covering different size and quality tradeoffs.

The chart below shows **quality versus tokens per second (TPS)**, with Unsloth used as the baseline for comparison.
Quality is measured across seven benchmarks, including function calling: BFCL-V3, LiveCodeBench V6, HumanEval, GSM8K, IFEVAL and MMLU, and GSM8K_V in both thinking and instruct modes.

**Selection rule:** Choose the model with the highest quality at your target throughput or the fastest model that still meets your required quality.

### GPU Models
Interactive plots for RTX 4090, 4080, 5090, 5060 Ti, and RTX Pro 6000 Blackwell are available [here](https://byteshape.com/blogs/Qwen3.5-35B-A3B/).

**Note:** Greyed-out models are better suited for other GPUs (see the [blog](https://byteshape.com/blogs/Qwen3.5-35B-A3B/)). Stripped-infill models prioritize token generation speed over prompt processing and are also marked with a dagger (†) in the table below.
![GPU Benchmark - RTX 4090](img/RTX4090.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size | Use This Model | Model Tag |
|---------|-------------|-----------|-----|-----------|
| [GPU-1](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ2_S-2.17bpw.gguf) | 2.17 | 9.41 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ2_S-2.17bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ2_S-2.17bpw.gguf` |
| [GPU-2†](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-2.73bpw.gguf) | 2.73 | 11.8 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.73bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.73bpw.gguf` |
| [GPU-3†](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf) | 2.89 | 12.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf` |
| [GPU-4](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ3_S-3.01bpw.gguf) | 3.01 | 13.0 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ3_S-3.01bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ3_S-3.01bpw.gguf` |
| [GPU-5](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ3_S-3.26bpw.gguf) | 3.26 | 14.1 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ3_S-3.26bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ3_S-3.26bpw.gguf` |
| [GPU-6†](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf) | 3.40 | 14.7 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf` |
| [GPU-7](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf) | 4.06 | 17.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf` |
| [GPU-8](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf) | 4.12 | 17.9 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf` |


### CPU Models
Interactive plots for Ryzen 9 5900X, Intel Core i7 12700KF, Ultra 7 265KF, and Raspberry Pi 5 (16 GB) are available [here](https://byteshape.com/blogs/Qwen3.5-35B-A3B/).
![CPU Benchmark - Ryzen 9 5900X](img/Ryzen9.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size | Use This Model | Model Tag |
|---------|-------------|-----------|-----|-----------|
| [CPU-1](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-2.69bpw.gguf) | 2.69 | 11.7 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.69bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.69bpw.gguf` |
| [CPU-2](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf) | 2.89 | 12.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-2.89bpw.gguf` |
| [CPU-3](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf) | 3.40 | 14.7 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q3_K_S-3.40bpw.gguf` |
| [CPU-4](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-Q4_K_S-3.51bpw.gguf) | 3.51 | 15.2 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q4_K_S-3.51bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-Q4_K_S-3.51bpw.gguf` |
| [CPU-5](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf) | 4.06 | 17.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.06bpw.gguf` |
| [CPU-6](https://huggingface.co/byteshape/Qwen3.5-35B-A3B-GGUF/blob/main/Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf) | 4.12 | 17.9 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf&platform=llamacpp) | `byteshape/Qwen3.5-35B-A3B-GGUF:Qwen3.5-35B-A3B-IQ4_XS-4.12bpw.gguf` |

## Notes on quantization labels

The labels you see (for example `IQ4_XS`) are only there to make Hugging Face show our models in the GGUF table. We do not use the conventional quantization profiles as defined in llama.cpp. In our case, these labels indicate the primary quantization approach and average bit length. Note that both KQ and IQ models may use a mix of quantization techniques optimized for their target hardware, which is why several models can share the same tag.
