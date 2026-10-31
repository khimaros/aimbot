---
license: mit
base_model:
  - deepseek-ai/DeepSeek-V4.1-Flash-1017
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
tags:
  - gguf
  - deepseek
  - deepseek-v4
  - moe
  - mxfp4
  - dspark
  - speculative-decoding
  - llama.cpp
  - mx-llama.cpp
---

# DeepSeek-V4.1-Flash-1017 (GGUF)

| | |
|---|---|
| **Model version** | **DeepSeek-V4.1-Flash-1017**, released by DeepSeek on 2026-10-17 |
| Source checkpoint | [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017), commit `1bae0e10` |
| Previous version | DeepSeek-V4.1-Flash (the first V4.1 release), on the [`v4.1-flash-previous`](https://huggingface.co/mxxm-t/DeepSeek-V4.1-Flash-GGUF/tree/v4.1-flash-previous) branch |

The file names did not change between versions. The 1017 files carry `general.version = 1017` in the
GGUF header, the previous files have no `general.version`.

> These files are built for **[mx-llama.cpp](https://github.com/mxxm-t/mx-llama.cpp)**, a fork of
> llama.cpp focused on multi-GPU inference: layer pipeline parallelism, tensor parallelism
> (`-sm tensor`) with a custom AllReduce, and DSpark / MTP speculative decoding. Prebuilt AMD / ROCm
> and NVIDIA / CUDA images are on Docker Hub at
> **[mxxm/mx-llama.cpp](https://hub.docker.com/r/mxxm/mx-llama.cpp)**.

[deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
converted to GGUF, plus its DSpark draft stages as a separate sidecar file. These files hold the text
model only: the vision tower and its projector are not included, and there is no `mmproj`. DeepSeek's
original model card follows below.

## Files

| file | size | notes |
|---|---|---|
| `DeepSeek-V4.1-Flash-MXFP4-00001-of-00012.gguf` .. `-00012-of-00012.gguf` | 375.8 GiB total | main model, routed experts MXFP4 |
| `DeepSeek-V4.1-Flash-DSpark-MXFP4.gguf` | 7.43 GiB | DSpark draft stages, not a standalone model |

Shards `00009` and `00011` each hold one Engram table (about 97 GiB together). They are read at random
during prompt processing and stay on disk rather than in VRAM, so they belong on the fastest storage
you have.

The sidecar holds the three `mtp.*` draft stages, 128 routed experts each with 3 active, plus the
DSpark heads. It taps the attention input of target layers 37, 38 and 39. It is a draft model for
speculative decoding against the main file and cannot generate on its own.

## Running it

The weights occupy roughly 302 GiB once loaded. An example command:

```
GGML_ENABLE_CUSTOM_AR=1 HSA_FORCE_FINE_GRAIN_PCIE=1 GPU_MAX_HW_QUEUES=8 \
llama-server -m DeepSeek-V4.1-Flash-MXFP4-00001-of-00012.gguf \
  -sm layer -ngl 99 -fit off \
  -c 32768 -b 8192 -ub 256 -fa 1 -lm dio
```

- Add `-md DeepSeek-V4.1-Flash-DSpark-MXFP4.gguf --spec-type draft-dspark --spec-draft-n-max 3` for
  DSpark speculative decoding.
- `-sm tensor -tps N` also works, for `N` of 1, 2, 4 or 8. On ten MI50 over PCIe `-sm layer` is faster
  for both prompt processing and generation.
- Chat completions place the reply in `reasoning_content`.

## Quantization

Routed experts are repacked from the checkpoint's own FP4 to MXFP4, a format change rather than a
requantization. FP8 block-scaled tensors are dequantized and stored Q8_0. Norms, hyper-connection
coefficients and the router bias stay F32. The router, markov and confidence weights stay BF16.
No weights were retrained, fine-tuned or otherwise altered.

Checked against the source checkpoint: every declared tensor is present, FP8 tensors dequantize to the
source values, the sidecar accounts for all 69 `mtp.*` tensors, and the Engram hash tables reproduce
the reference `engram.py` derivation.

## License

MIT, inherited from the base model. A copy is included in this repository as `LICENSE`, as its terms
require. Copyright (c) 2023 DeepSeek.

---

## Original model card

Reproduced from [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017),
unchanged except that its relative links now point to that repository.

# DeepSeek-V4.1-Flash-1017

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/logo.svg?raw=true" width="60%" alt="DeepSeek-V4.1" />
</div>
<hr>
<div align="center" style="line-height: 1;">
  <a href="https://www.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/badge.svg?raw=true" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://chat.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-DeepSeek%20V4.1-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/deepseek-ai" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-DeepSeek%20AI-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://twitter.com/deepseek_ai" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-deepseek_ai-white?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/main/LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<p align="center">
  <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf"><b>Technical Report</b> 👁️</a>
</p>

## Introduction

**DeepSeek-V4.1-Flash-1017** is a minor update to [**DeepSeek-V4.1-Flash**](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash), delivering substantial improvements across reasoning, coding, agentic tasks, and visual benchmarks. Alongside these gains, the model reduces task execution time and output length, enabling users to complete tasks faster and at lower cost and advancing the performance–cost Pareto frontier across multiple agent harnesses.

<div align="center">

| Benchmark | DS-V4.1-Flash-1017 | DS-V4.1-Flash | K3 | GLM-5.3 | GPT-5.6 Sol | Opus 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| HLE w/o tools | 42.6 (44.0†) | 36.8 (39.1†) | 43.5 | 42.0† | 44.5 | 56.3 |
| Terminal-Bench 4.0 | 42.3 | 31.2 | 12.6 | 37.9 | 39.9 | 51.8 |
| DeepSWE v1.1 | 77.0 | 74.2 | 67.5 | 66.9 | 73.0 | 74.0 |
| ProgramBench | 29.1 | 20.3 | 17.5 | 19.0 | 23.0 | 37.0 |
| NL2Repo-Bench | 68.2 | 65.4 | 58.0 | 58.0 | 56.8 | 75.3 |
| Automation-Bench v1.0.6 | 60.5 | 54.8 | 46.7 | 48.8 | 45.8 | 50.3 |
| Agents’ Last Exam | 35.4 | 31.8 | 27.6 | 28.5 | 26.7 | 28.6 |
| Apex Bench v1.1 | 72.1 | 64.6 | 47.8 | 56.6 | 54.3 | 65.8 |
| Chartography (w/tools) | 83.0 | 78.9 | 68.1 | — | 79.9 | 84.0 |
| BabyVision (w/tools) | 92.5 | 89.6 | 85.7 | — | 88.9 | 94.1 |
| ZeroBench-main (w/tools) | 51.0 | 49.0 | 41.0 | — | 53.0 | 52.0 |

</div>

*† denotes the text-only subset of HLE. We use the Claude Code harness for Terminal-Bench 4.0 and the Mini-SWE-V2 harness for DeepSWE v1.1.*

## Prompt Encoding

This release does not include a Jinja-format chat template. The [`encoding`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/main/encoding/README.md) folder contains a self-contained Python reference implementation (`encoding.py`) with test cases for multi-turn conversations, tool calling, thinking mode, numeric reasoning effort, mid-conversation system messages, and interleaved image content.

For production use, we additionally release [deepseek-recipe](https://github.com/deepseek-ai/deepseek-recipe), a set of Rust libraries with Python bindings that provides the same prompt format as a maintained, protocol-aware toolkit. It converts Messages, Chat Completions, and Responses API requests into the Conversation format, encodes them into DeepSeek V4 and V4.1 prompts or token IDs, and parses model output back into complete or streamed responses — covering thinking, tool calls, images, and generation settings. Model inference, tool execution, and HTTP transport are left to the caller.

## Minimal Inference

Please refer to the [`inference`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/main/inference/README.md) folder for instructions on weight conversion and running inference locally.

**Recommended sampling parameters:**

| Parameter | Value |
| :--- | :--- |
| `temperature` | 1.0 |
| `top_p` | 1.0 |
| `context_window` | 1M tokens |
| `max_tokens` | ≥ 256K |

## License

This repository and the model weights are licensed under the [MIT License](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/main/LICENSE).

## Citation

```bibtex
@misc{deepseekai2026deepseekv41flash,
      title={DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression},
      author={DeepSeek-AI},
      year={2026},
}
```

## Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](mailto:service@deepseek.com).
