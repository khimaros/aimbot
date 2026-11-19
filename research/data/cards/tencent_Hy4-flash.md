---
license: other
license_name: tencent-hy-license
license_link: https://huggingface.co/tencent/Hy4-flash/blob/main/LICENSE
library_name: transformers
pipeline_tag: image-text-to-text
tags:
- hunyuan
- hy4-flash
- moe
- multimodal
- instruct
---

<p align="left">
    <a href="https://huggingface.co/tencent/Hy4-flash/blob/main/README_CN.md">中文</a>&nbsp;｜&nbsp;English
</p>
<br>

<p align="center">
  <img src="assets/logo-en.png" alt="Tencent Hy" width="400"/>
</p>

<div align="center" style="line-height: 1;">

[![License](https://img.shields.io/badge/License-Tencent%20Hy%20License-blue)](#license)
&nbsp;&nbsp;
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Tencent%20Hy-ffc107?color=ffc107&logoColor=white)](https://huggingface.co/tencent/Hy4-flash)
&nbsp;&nbsp;
[![ModelScope](https://img.shields.io/badge/ModelScope-Tencent%20Hy-624aff)](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash)
&nbsp;&nbsp;
[![GitCode](https://img.shields.io/badge/GitCode-Tencent%20Hy-red?logoColor=white)](https://ai.gitcode.com/tencent_hunyuan/Hy4-flash)

</div>

<p align="center">
  <a href="https://hy.tencent.ai/research/hy4-flash"><b>Official Website</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://github.com/Tencent-Hunyuan/Hy4-flash"><b>GitHub</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://huggingface.co/AngelSlim/Hy4-flash-GGUF"><b>GGUF</b></a>
</p>

---

## Table of Contents

- [Model Introduction](#model-introduction)
- [Pretrained model capability](#pretrained-model-capability)
- [Practicality and Cost Efficiency](#practicality-and-cost-efficiency)
  - [Optimization Approach](#optimization-approach)
  - [Task Performance and Cost](#task-performance-and-cost)
  - [User Blind Evaluation](#user-blind-evaluation)
- [Appendix: Benchmark results](#appendix-benchmark-results)
- [News](#news)
- [Model Links](#model-links)
- [Quickstart](#quickstart)
  - [Transformers](#transformers)
  - [OpenAI-compatible API](#openai-compatible-api)
- [Deployment](#deployment)
  - [DFly2 for Speculative Decoding](#dfly2-for-speculative-decoding)
  - [Quantization](#quantization)
  - [Inference Frameworks](#inference-frameworks)
    - [vLLM](#vllm)
    - [SGLang](#sglang)
- [Finetuning](#finetuning)
- [License](#license)
- [Contact Us](#contact-us)

## Model Introduction

**Hy4 flash** is our most cost-effective Hy model to date, featuring 220B total parameters (including 64B Engram parameters) with just 12B active parameters per token. It natively accepts text and image inputs, generates text, and supports a context window of up to 1M tokens.

Its 42-layer language backbone consists of one dense feed-forward layer and 41 MoE layers, with identity Hyper-Connections (iHC) supporting inter-layer information flow. A vision encoder (adapted from SigLIP2-So400m-Patch16-Res512) is connected to the backbone through an MLP projector. In addition to the backbone, a built-in 5-layer drafter, [DFly2](#dfly2-for-speculative-decoding) (0.85B parameters), reuses the target model's KV cache and sparse indices to support long-context speculative decoding at a low, constant cost.

Compared with Hy4, Hy4 Flash introduces three notable architectural changes:

1. **Hybrid attention.** Sparse attention (IndexPool) and sliding-window attention (SWA) are interleaved at a 1:3 ratio.
2. **LatentMoE.** Routed experts operate in a lower-dimensional latent space. Each token activates 16 of 512 routed experts, alongside one shared expert.
3. **N-gram embedding (Engram).** The backbone is augmented with learned bigram and trigram representations, retrieved via multi-head hash lookups.

| Property | Value |
| --- | --- |
| **Overview** | |
| Architecture | Mixture-of-Experts (MoE) |
| Total Parameters (excluding Engram, ViT, and DFly2) | 155.5B |
| Engram Parameters | 63.5B |
| ViT Parameters | 0.43B |
| DFly2 Parameters | 0.85B |
| Activated Parameters per Token | Text 11.3B + Vision 0.43B |
| Context Length | 1M (1,048,576 tokens) |
| **Language Backbone** | |
| Backbone Layers | 42 — 1 dense layer and 41 MoE layers |
| Hidden Size | 3,072 |
| Vocabulary Size | 120,832 |
| Residual Connections | iHC (identity Hyper-Connections) with 4 residual streams |
| **Attention — Hybrid Layout** | |
| Attention Architecture | Sparse attention + sliding-window attention (SWA) |
| Backbone Layer Pattern | 2 × Sparse → 10 × (3 × SWA → Sparse) |
| Attention Formulation | Multi-head Latent Attention (MLA) |
| Multimodal Position Encoding | Interleaved MRoPE |
| **Attention — Layers** | **Sparse / SWA** |
| Backbone Layers | 12 / 30 |
| Attention Heads | 32 / 64 |
| MLA q_lora_rank | 1,024 / 1,024 |
| MLA kv_lora_rank | 512 / 512 |
| QK Head Dimension (non-RoPE + RoPE) | 192 + 64 / 192 + 64 |
| Value Head Dimension | 256 / 256 |
| RoPE Base | 10,000,000 / 10,000 |
| Sparse Context Selection | Up to 2,048 tokens via group-level selection |
| SWA Context Window | 512-token causal window (511 preceding + current) |
| **Feed-Forward Networks** | |
| Dense FFN Intermediate Size | 13,824 |
| Routed Experts per MoE Layer | 512 |
| Shared Experts per MoE Layer | 1 |
| Activated Routed Experts per Token | 16 |
| MoE Latent Dimension | 1,536 |
| Expert Intermediate Size | 1,536 |
| **N-gram Embedding** | |
| N-gram Orders | Bigrams and trigrams |
| Backbone Layer Indices (starting from 0) | 1, 11, 21, 31 |
| Hash Heads per N-gram Order | 8 |
| Hash Vocabulary Size per Head | 10.3M |
| Embedding Dimension per N-gram Order | 768 (8 heads × 96 dimensions) |
| Embedding Table Parameters | 63.4B |
| **Vision Encoder** | |
| Vision Encoder Layers | 27 |
| Vision Encoder Hidden Size | 1,152 |
| Vision Encoder Intermediate Size | 4,304 |
| Vision Encoder Attention Heads | 16 |
| Vision Patch Size | 16 × 16 |
| Vision Position Embedding Size | 128 × 128 |
| Visual Feature Merging | 2 x 2 |

## Pretrained model capability

Bits-per-byte (BPB) on internal code & agent validation, lower is better:

<p align="center">
  <a href="pretrained-model-bpb.png"><img src="pretrained-model-bpb.png" alt="Bits-per-byte on internal code and agent validation versus active parameters; lower is better" width="75%"/></a>
</p>

Few-shot pretrain benchmark evaluation:

| Category | Benchmark | #Shots | Hy4 flash Base | Hy4 Base | Hy3 preview Base | DeepSeek-V4-flash-Base | DeepSeek-V4-Pro-Base |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: |
| **Knowledge** | MMLU† | 5 | 88.7 | **91.6** | 87.5 | 89.7 | 91.1 |
|  | MMLU-Pro† | 5 | 71.1 | **73.9** | 65.8 | 68.6 | 73.4 |
|  | MMLU-Redux† | 5 | 87.6 | **90.6** | 87.0 | 88.8 | 90.2 |
|  | SuperGPQA† | 5 | 57.8 | **62.7** | 52.3 | 52.5 | 54.8 |
|  | C-Eval† | 5 | 92.0 | **95.0** | 90.1 | 91.9 | 93.4 |
|  | CMMLU† | 5 | 91.6 | **93.1** | 89.6 | 89.8 | 90.7 |
|  | SimpleQA | 5 | 37.5 | **57.2** | 26.4 | 31.3 | 52.1 |
|  | Chinese-SimpleQA† | 5 | 74.6 | **83.9** | 69.6 | 71.9 | 76.6 |
|  | AGIEval (English)† | 3 | 75.4 | **79.3** | 76.0 | 76.3 | 78.2 |
|  | AGIEval (Chinese)† | 3 | 90.6 | **91.2** | 87.8 | 88.5 | 89.8 |
| **Reasoning** | HellaSwag (3,000-item subset) | 10 | 85.2 | **87.1** | 85.7 | 85.1 | 86.8 |
|  | PIQA | 4 | 84.4 | **85.3** | 84.6 | 83.8 | 84.9 |
|  | ARC-Challenge | 0 | 95.0 | **97.3** | 96.0 | **97.3** | 97.0 |
|  | Social IQa | 0 | 80.1 | **82.7** | 80.5 | 72.5 | 73.1 |
|  | KOR-Bench | 3 | 54.7 | **57.6** | 54.6 | 53.4 | 55.4 |
|  | C³ | 0 | 77.3 | **82.4** | 75.9 | 74.1 | 78.3 |
| **Math** | U-MATH | 5 | 69.8 | **71.6** | 60.9 | 57.4 | 64.8 |
|  | OCW Courses | 5 | 64.0 | 66.7 | 62.6 | 63.3 | **68.2** |
| **Code** | MBPP-plus | 3 | 73.7 | 74.0 | 77.4 | 76.8 | **79.1** |
| **Multilingual** | Belebele (5-language subset)† | 5 | 93.8 | 95.0 | 94.2 | 94.4 | **95.2** |
|  | INCLUDE† | 5 | 82.8 | **88.1** | 84.3 | 84.0 | 84.3 |
| **Multimodal** | MMMU-Pro (Standard, 10 opts) | 4 | 52.0 | **59.6** | — | — | — |
|  | SimpleVQA | 4 | 48.5 | **54.5** | — | — | — |
|  | CVBench | 4 | 83.4 | **86.7** | — | — | — |
|  | RealWorldQA | 4 | 71.1 | **72.3** | — | — | — |
|  | TextVQA | 4 | 73.4 | **78.2** | — | — | — |
|  | CountBenchQA | 4 | 86.6 | **90.6** | — | — | — |

† Macro-averaged accuracy for the marked text benchmarks. Other text rows use the accuracy metric reported by our evaluation suite. Bold marks the highest available numerical score in each row; it does not indicate statistical significance.

Multimodal results are reported only for Hy4 flash Base and Hy4 Base.

ARC-Challenge and HellaSwag use 299-item and 3,000-item subsets, respectively. INCLUDE uses a 5,000-example Lite subset covering 44 languages. Belebele covers German, Korean, Vietnamese, Spanish, and Russian (4,475 examples in total).

**Disclaimer: Because our base model was exposed to a large amount of synthetic instruction data during mid-training, it occasionally fails to follow the expected answer format in few-shot evaluations, which may distort the scores.**

## Practicality and Cost Efficiency

### Optimization Approach

Across training, evaluation, and inference, we aggressively optimized for cost efficiency while preserving intelligence:

- **Pre-training**: Hy4 flash integrates hybrid attention, LatentMoE, and Engram into its architecture—reducing KV cache size to just **1/24 of Hy3** and **1/6 of Hy4**, with extensive scaling ladder experiments ensuring performance meets expectations.
- **Post-training**: Self-distillation from Hy4 establishes strong general intelligence, while reinforcement learning cuts average end-to-end output tokens by **50%**.
- **Evaluation**: We built WorkIndex, an internal benchmark grounded in typical WorkBuddy tasks, and paired it with human evaluation—focusing on **deliverable quality, single-turn output length, and task turnaround time** rather than public benchmark scores detached from everyday work.
- **Inference**: Combining megakernels, 4-bit quantization, and [DFly2](#dfly2-for-speculative-decoding) pushes decoding speed past **150 tokens/s**, enabling low-cost serving at scale.

### Task Performance and Cost

**Hy4 flash delivers overall task performance slightly above Hy4 preview at a much lower cost per task.** On WorkIndex, it scores **42.1**, compared with **39.7** for Hy4 preview, while its average cost per task is just **1/13 of Hy4 preview**, **1/20 of Hy4**, and **1/8 of DeepSeek-V4.1-Flash-1017** (Max tier, peak-hour pricing).

<p align="center">
  <a href="assets/performance-cost-workindex.png"><img src="assets/performance-cost-workindex.png" alt="Performance and cost per task on WorkIndex for Hy4 flash and comparison models" width="49%"/></a>
  <a href="assets/performance-cost-open-benchmarks.png"><img src="assets/performance-cost-open-benchmarks.png" alt="Performance and cost per task on Open Benchmarks for Hy4 flash and comparison models" width="49%"/></a>
</p>
<p align="left"><sub>Figure 1: Performance and cost across internal and external tasks. WorkIndex (internal) comprises 8 evaluation sets covering slide creation, slide editing, human-AI slide co-writing, Markdown human-AI co-writing, document editing, spreadsheet repair, audio/video processing, and visual understanding.<br/>Open Benchmarks includes 7 public agent benchmarks: DeepSWE, ProgramBench, Terminal-Bench 4.0, APEX-Agents, AutomationBench, HLE, and OSWorld 2.1.</sub></p>

<p align="center">
  <a href="assets/workindex-cost.png"><img src="assets/workindex-cost.png" alt="Average cost per task on WorkIndex for Hy4 flash, Hy4 preview, and Hy4" width="100%"/></a>
</p>
<p align="left"><sub>Figure 2: Average cost per task on WorkIndex. Task scores are 42.1 for Hy4 flash, 39.7 for Hy4 preview, and 51.4 for Hy4.</sub></p>

We recommend Hy4 flash for most everyday productivity tasks, including **deep search, document processing, slide creation, simple frontend demos, and computer use**. For complex tasks such as long-horizon software engineering, we recommend Hy4 for its higher intelligence ceiling.

### User Blind Evaluation

In the blind evaluation, **Hy4 flash achieved user satisfaction close to Claude Haiku 5.5, while recording the lowest cost per task and shortest median end-to-end completion time among the evaluated models**. Its user satisfaction score was **2.79/4** (Claude Haiku 5.5: **2.81/4**), with a median end-to-end completion time of **6.7 minutes** and a cost of **RMB 0.26 per task**.

<p align="center">
  <a href="assets/blind-evaluation-en.png"><img src="assets/blind-evaluation-en.png" alt="Blind evaluation comparing user satisfaction, median end-to-end completion time, and cost per task" width="100%"/></a>
</p>
<p align="left"><sub>Figure 3: Blind evaluation with 85 internal WorkBuddy users across 259 tasks spanning 27 categories.</sub></p>

## Appendix: Benchmark results

<p align="center">
  <a href="assets/benchmark.png"><img src="assets/benchmark.png" alt="Full benchmark scores, task costs, and evaluation notes for Hy4 flash and comparison models" width="100%"/></a>
</p>

## News

* We release **Hy4 flash**, **Hy4 flash-FP8**, and the pre-trained **Hy4 flash-base** as open-weight models on [Hugging Face](https://huggingface.co/tencent/Hy4-flash), [ModelScope](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash), and [GitCode](https://ai.gitcode.com/tencent_hunyuan/Hy4-flash).

## Model Links

| Model Name | Description | Hugging Face | ModelScope | GitCode |
|:---|:---|:---:|:---:|:---:|
| Hy4 flash | Instruct model | [Model](https://huggingface.co/tencent/Hy4-flash) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4-flash) |
| Hy4 flash-FP8 | FP8 quantized instruct model | [Model](https://huggingface.co/tencent/Hy4-flash-FP8) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash-FP8) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4-flash-FP8) |
| Hy4 flash-base | Pre-trained base model | [Model](https://huggingface.co/tencent/Hy4-flash-base) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-flash-base) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4-flash-base) |

Hy4 flash-base is a pre-trained base model, not an instruction-tuned chat model. The chat and reasoning examples below apply to Hy4 flash and Hy4 flash-FP8.

## Quickstart

Use [Transformers](#transformers) to load the model for local inference, or deploy a server and access it through the [OpenAI-compatible API](#openai-compatible-api).

> **Reasoning mode (instruct models)**: `reasoning_effort` supports `"high"` (default, thinking enabled) and `"no_think"` (direct responses). Both examples below use `"no_think"`.
>
> **Recommended sampling parameters**: `temperature=0.9`, `top_p=1.0`.

### Transformers

> Support for Hy4 flash will be merged into the `transformers` main branch soon. Until then, install from the commit below.

```bash
pip install "transformers[torch,vision] @ git+https://github.com/huggingface/transformers.git@refs/pull/50903/head"
```

The following example generates a brief image description:

```python
from transformers import AutoModelForImageTextToText, AutoProcessor

model_id = "tencent/Hy4-flash"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(model_id, device_map="auto")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg",
            },
            {"type": "text", "text": "Describe this image in one sentence."},
        ],
    }
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    reasoning_effort="no_think",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=256)
print(processor.decode(outputs[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True))
```

### OpenAI-compatible API

For API access, start a server using the [vLLM deployment instructions](#vllm), then run the following client example:

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="hy4-flash",
    messages=[
        {"role": "user", "content": "Hello! Can you briefly introduce yourself?"},
    ],
    temperature=0.9,
    top_p=1.0,
    extra_body={"chat_template_kwargs": {"reasoning_effort": "no_think"}},
)
print(response.choices[0].message.content)
```

## Deployment

### DFly2 for Speculative Decoding

DFly2 is Hy4 flash's speculative-decoding drafter, trained with [AngelSpec](https://github.com/Tencent/AngelSpec) and built directly on the target model's **Top-k Sparse KV**: each draft layer shares the KV cache (**KV Share**) and the compressed indexer's selection of up to 2,048 positions (**Index Share**) with its corresponding sparse attention layer. This yields three advantages:

- **Constant cost**: each draft token attends to at most ~2K keys, regardless of context length.
- **Zero extra KV memory**: no separate KV cache is maintained for the drafter.
- **PD-disaggregation ready**: not involved in prefill; the prefill-to-decode transfer adds only one last-layer hidden state.

<p align="center">
  <a href="assets/dfly2.png"><img src="assets/dfly2.png" alt="DFly2 architecture: each draft layer reuses the KV cache and the indexer-selected positions of a sparse attention layer of Hy4 flash" width="75%"/></a>
</p>

### Quantization

We provide [AngelSlim](https://github.com/tencent/AngelSlim), a more accessible, comprehensive, and efficient toolkit for large model compression. AngelSlim supports a comprehensive suite of compression tools for large-scale multimodal models, including common quantization algorithms, low-bit quantization, and speculative sampling.

For this model, we have provided a [GGUF](https://huggingface.co/AngelSlim/Hy4-flash-GGUF) compressed version for end-to-end testing purposes.

### Inference Frameworks

For production serving, we recommend using [vLLM](https://github.com/vllm-project/vllm) or [SGLang](https://docs.sglang.io/). Please refer to the recipes:
- [Hy4 flash vLLM Recipe](https://recipes.vllm.ai/tencent/Hy4-flash)
- [Hy4 flash SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/Tencent/Hy4-flash)

#### vLLM

Use official prebuilt image `vllm/vllm-openai:hy4-flash`:

```bash
docker run --gpus all \
  -p 8000:8000 \
  --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:hy4-flash tencent/Hy4-flash-FP8 \
    --tensor-parallel-size 8 \
    --speculative-config '{"num_speculative_tokens":5,"method":"dfly"}' \
    --attention-backend FLASHMLA_SPARSE \
    --tool-call-parser hy_v4 \
    --reasoning-parser hy_v4 \
    --enable-auto-tool-choice \
    --port 8000 \
    --served-model-name hy4-flash
```

#### SGLang

Use the official prebuilt image `lmsysorg/sglang:hy4-flash` (multi-arch, x86 and Arm):

```bash
docker pull lmsysorg/sglang:hy4-flash

docker run --gpus all \
  -p 8000:8000 \
  --ipc=host \
  lmsysorg/sglang:hy4-flash \
  sglang serve \
    --trust-remote-code \
    --model-path tencent/Hy4-flash-FP8 \
    --tp 8 \
    --cuda-graph-backend-prefill disabled \
    --speculative-algorithm DFLY \
    --speculative-dfly-block-size 6 \
    --host 127.0.0.1 \
    --port 8000
```

## Finetuning

Hy4 flash provides a complete model finetuning pipeline. For detailed documentation, please refer to: [Finetuning Guide](https://huggingface.co/tencent/Hy4-flash/blob/main/finetune/README.md)

## License

Hy4 flash is released under the **Tencent Hy License**. See [LICENSE](https://huggingface.co/tencent/Hy4-flash/blob/main/LICENSE) for details.

## Contact Us

If you have any questions or suggestions, feel free to reach out to our R&D and product teams via email:

📧 **hunyuan_opensource@tencent.com**

---

<p align="center">
  <i>Hy4 flash is developed by the Tencent Hy Team.</i>
</p>
