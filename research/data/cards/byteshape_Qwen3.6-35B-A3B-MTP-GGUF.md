---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/LICENSE
pipeline_tag: image-text-to-text
base_model:
- Qwen/Qwen3.6-35B-A3B
tags:
- qwen3.6
- byteshape
- mtp
---

# Qwen3.6-35B-A3B MTP GGUF (ShapeLearn Quantized)

This is a GGUF-quantized version of Qwen3.6-35B-A3B with **Multi-Token Prediction (MTP)** support, produced with **ByteShape's ShapeLearn**, which learns the optimal datatype per tensor to maintain high quality even at very low bitlengths.

MTP allows the model to predict multiple tokens per forward pass, accelerating decoding on GPUs by accepting speculative tokens that match what the base model would have produced. These models are optimized for **GPU-only** inference.

To learn more about ShapeLearn and to see detailed benchmarks across GPUs, please visit our [blog](https://byteshape.com/blogs/Qwen3.6-35B-A3B/).

If you have questions or want to share feedback, reach us on [Reddit](https://www.reddit.com/r/ByteShape/).

## Quick Start

Pick a model from the table below and click **Get llama.cpp command** to get a ready-to-run command with all the correct sampling parameters for this model.

You can also copy the **Model Tag** from the table and use it directly:

| Tool | Command |
|------|---------|
| **llama.cpp** | `llama-server -hf <MODEL_TAG> --mmproj-auto --spec-type draft-mtp --spec-draft-n-max 4` |

This is a **vision capable** model. llama.cpp auto-downloads the model and vision projector on first run.

The MTP head is bundled inside the GGUF, so no separate draft model is required — just pass `--spec-type draft-mtp` to enable MTP-based speculative decoding. `--spec-draft-n-max` controls how many tokens are drafted per step (see [A Note on MTP Performance](#a-note-on-mtp-performance) below for tuning guidance).

> **Build requirement:** MTP support requires a recent build of llama.cpp (the `draft-mtp` value for `--spec-type` was added in late 2025). If your `llama-server --help` output does not list `draft-mtp` under `--spec-type`, please update to a newer build from the [llama.cpp releases](https://github.com/ggml-org/llama.cpp/releases).

Once you run the llama-server, you can access the web interface at `http://localhost:<PORT>`.


## A Note on MTP Performance

**MTP throughput is workload dependent.** The realized speedup depends on how predictable your prompt and decoded tokens are — code completion, structured output, and repetitive content benefit the most, while highly creative or out-of-distribution generation benefits less.

The TPS numbers reported in our benchmarks are **effective TPS**, i.e. the throughput observed when running the benchmark suite end-to-end (including acceptance/rejection of speculative tokens). Your own workload may see higher or lower TPS than the chart.

From our measurements, predicting **2 to 4 tokens ahead** offers the best quality/throughput tradeoff for most workloads. The optimal `n` again depends on the workload — feel free to sweep this value for your specific use case.

## How to Pick a Model

All MTP variants are **GPU-optimized** with a hybrid approach combining KQ and IQ quantization for better throughput. Each model covers a different size and quality tradeoff.

The chart below compares this **MTP release** against our standard **NTP (Next Token Prediction) release** of the same model to illustrate the speedup MTP provides, plotting **quality versus effective tokens per second (TPS)**.
Quality is measured across six benchmarks, including function calling: BFCL-V3, LiveCodeBench V6, HumanEval, GSM8K, IFEVAL, and GSM8K_V in both thinking and instruct modes.

### GPU Models
Interactive plots for RTX 4090, 4080, 5060Ti, 5090, and RTX Pro 6000 Blackwell are available [here](https://byteshape.com/blogs/Qwen3.6-35B-A3B/).

![GPU Benchmark - RTX 4090](img/RTX4090.png)

**Table sorted by model size** (match the chart numbers to model IDs):

| Model ID | Bits/Weight | Model Size | Use This Model | Model Tag |
|---------|-------------|-----------|-----|-----------|
| [GPU-1](https://huggingface.co/byteshape/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-IQ2_S-2.25bpw.gguf) | 2.25 | 10 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ2_S-2.25bpw&platform=llamacpp) | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ2_S-2.25bpw` |
| [GPU-2](https://huggingface.co/byteshape/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-IQ3_S-3.06bpw.gguf) | 3.06 | 13.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ3_S-3.06bpw&platform=llamacpp) | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ3_S-3.06bpw` |
| [GPU-3](https://huggingface.co/byteshape/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-IQ4_XS-3.53bpw.gguf) | 3.53 | 15.7 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-3.53bpw&platform=llamacpp) | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-3.53bpw` |
| [GPU-4](https://huggingface.co/byteshape/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-IQ4_XS-3.97bpw.gguf) | 3.97 | 17.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-3.97bpw&platform=llamacpp) | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-3.97bpw` |
| [GPU-5](https://huggingface.co/byteshape/Qwen3.6-35B-A3B-MTP-GGUF/blob/main/Qwen3.6-35B-A3B-IQ4_XS-4.19bpw.gguf) | 4.19 | 18.6 GB | [Get llama.cpp command](https://byteshape.com/run-hf-model/?tag=byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-4.19bpw&platform=llamacpp) | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF:Qwen3.6-35B-A3B-IQ4_XS-4.19bpw` |

## Notes on quantization labels

The labels you see (for example `IQ4_XS`) are only there to make Hugging Face show our models in the GGUF table. We do not use the conventional quantization profiles as defined in llama.cpp. In our case, these labels indicate the primary quantization approach and average bit length. Note that both KQ and IQ models may use a mix of quantization techniques optimized for their target hardware, which is why several models can share the same tag.
