---
library_name: transformers
pipeline_tag: text-generation
language:
- en
- ko
tags:
- motif
- motif-3
- mixture-of-experts
- moe
- multilingual
license: mit
base_model:
- Motif-Technologies/Motif-3-Base
---

<div align="center">
  <img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6836935d054aee793ffd78f1/L3Rw_g8vkvD8dqhOYGZhl.png" width="180" alt="Motif">
</div>
<hr>

<div align="center" style="line-height: 1;">
  <a href="https://chat.motiftech.io/chat" target="_blank"><img alt="chatbot" src="https://img.shields.io/badge/chatbot-Chat%20Motif-17831f?logoColor=white"/></a>
  <a href="https://motiftech.io" target="_blank"><img alt="Homepage" src="https://img.shields.io/badge/Homepage-Motif%20Technologies-1783ff?logoColor=white"/></a>
  <a href="https://huggingface.co/Motif-Technologies" target="_blank"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Motif-ffc107?color=ffc107&logoColor=white"/></a>
  <a href="https://arxiv.org/abs/2608.09119" target="_blank"><img alt="Tech Report" src="https://img.shields.io/badge/📄%20Tech%20Report-lightgrey"/></a>
  <a href="https://huggingface.co/Motif-Technologies/Motif-3/blob/main/LICENSE.md" target="_blank"><img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53"/></a>
</div>


## 1. Model Introduction

**Motif 3** is a large-scale, decoder-only Mixture-of-Experts (MoE) language model with **314 billion total parameters** and **13.2 billion parameters activated per token**. It is built from the ground up by [Motif Technologies](https://motiftech.io) following a fully in-house, proprietary design.

Motif 3 is built around **Grouped Differential Latent Attention (GDLA)**, which integrates grouped differential attention with the compressed key–value representation of Multi-head Latent Attention. The architecture further incorporates **modified manifold-constrained hyper-connections (mHC)**, **Expert-Specific PolyNorm** activations, and a **Multi-Token Prediction (MTP)** head to improve optimization stability, expert specialization, and inference efficiency.

The model is pretrained on approximately **12.5 trillion tokens** spanning web documents, STEM, code, mathematics, multilingual content, and domain-specialized corpora, with additional emphasis on Korean, reasoning-intensive, legal, and financial data. Post-training combines general supervised fine-tuning, six RL-trained specialist teachers, a software-engineering teacher, and **Multi-teacher On-Policy Distillation (MOPD)** into a single unified model.

### Key Features
- 🧠 **Fine-grained sparse MoE** — 384 routed experts with only 8 activated per token (plus 1 shared expert), providing a large expert pool at limited per-token compute.
- 📏 **Native 256K context** (262,144 tokens), trained with window-aware context parallelism.
- ⚙️ **Novel architecture** — GDLA attention, Expert-Specific PolyNorm, modified mHC, and a built-in MTP head enabling **self-speculative decoding**.
- 🌐 **Multilingual & general-purpose**, with a strong bytes-per-token tokenizer for English, Korean, code, and math.
- 🎯 **Agentic strengths** — particularly strong on long-horizon agentic tool use and terminal-based problem solving, with calibrated abstention on hallucination-sensitive evaluations.

## 2. Model Summary

<div align="center">
<table>
<tbody>
<tr><td><b>Architecture</b></td><td>Mixture-of-Experts (MoE), decoder-only</td></tr>
<tr><td><b>Total Parameters</b></td><td>~314B</td></tr>
<tr><td><b>Activated Parameters</b></td><td>~13.2B / token</td></tr>
<tr><td><b>Number of Layers</b></td><td>53 (2 dense + 51 MoE)</td></tr>
<tr><td><b>Hidden Dimension</b></td><td>4096</td></tr>
<tr><td><b>Dense FFN Intermediate</b></td><td>12,288 (first 2 layers)</td></tr>
<tr><td><b>Attention</b></td><td>Grouped Differential Latent Attention (GDLA) with gated output</td></tr>
<tr><td><b>Query / KV Heads</b></td><td>80 / 16</td></tr>
<tr><td><b>Routed Experts</b></td><td>384 (top-8)</td></tr>
<tr><td><b>Shared Experts</b></td><td>1</td></tr>
<tr><td><b>Activation</b></td><td>Expert-Specific PolyNorm</td></tr>
<tr><td><b>Residual</b></td><td>Modified manifold-constrained hyper-connections (mHC)</td></tr>
<tr><td><b>MTP Head</b></td><td>1 layer (self-speculative decoding)</td></tr>
<tr><td><b>Context Length</b></td><td>262,144 (256K)</td></tr>
<tr><td><b>Vocabulary Size</b></td><td>220,160</td></tr>
<tr><td><b>Pretraining Tokens</b></td><td>~12.5T</td></tr>
<tr><td><b>Tensor Type</b></td><td>bfloat16</td></tr>
</tbody>
</table>
</div>

## 3. Evaluation Results

For contextual comparison, Motif 3 is compared with strong open-weight models using scores reported on the corresponding benchmark leaderboards. All Motif 3 evaluations were performed with sampling temperature = 1.0, top-p = 0.95, and a maximum sequence length of 262,144 tokens.  
(*: public dataset only)
<div align="center">

| Benchmark | **Motif 3**<br><sup>314B-A13B</sup> | MiniMax-3<br><sup>428B-A23B</sup> | GLM-5.1<br><sup>744B-A40B</sup> | Kimi-K2.6<br><sup>1T-A32B</sup> | Qwen-3.7<br><sup>max<sup> | DS-v4-Pro<br><sup>1.6T-A49B</sup> |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Agentic** | | | | | | |
| GDPVal v2 | 38.7 | 44.4 | 37.8 | 34.4 | 39.0 | 40.2 |
| τ²-Bench Telecom | 94.7 | 88.9 | 97.7 | 95.9 | 94.7 | 96.2 |
| τ³-Banking | 35.3 | 15.3 | 13.6 | 23.3 | 12.0 | 30.1 |
| ITBench* | 51.5 | — | 40.3 | 31.2 | 42.5 | 38.3 |
| **Coding** | | | | | | |
| SWE-Bench Verified | 76.2 | 75.0 | 76.4 | 76.2 | 80.4 | 77.4 |
| Terminal-Bench 2.1 | 74.9 | 65.2 | 61.8 | 65.9 | 75.0 | 64.0 |
| SciCode | 40.6 | 45.4 | 43.8 | 53.5 | 53.5 | 50.0 |
| **Reasoning & Knowledge** | | | | | | |
| IMOAnswerBench | 83.2 | — | 83.8 | 81.8 | 90.0 | 89.8 |
| Apex-Shortlist | 75.5 | — | 71.1 | 77.4 | 44.5 | 85.8 |
| GPQA Diamond | 83.4 | 92.9 | 86.8 | 91.1 | 92.4 | 88.8 |
| HLE | 37.0 | 39.0 | 30.1 | 37.5 | 41.4 | 37.5 |
| CritPt | 6.6 | 3.7 | 4.6 | 8.0 | 11.4 | 12.9 |
| OmniScience — Accuracy | 30.1 | 16.7 | 23.7 | 32.6 | 31.0 | 42.9 |
| OmniScience — Non-Hallucination | 71.6 | 81.6 | 70.1 | 59.5 | 74 | 5.9 |
| **Long Context & Instruction Following** | | | | | | |
| AA-LCR | 72.3 | 80.3 | 68.0 | 76.7 | 75.0 | 70.0 |
| IFBench | 78.2 | 82.9 | 76.3 | 76.0 | 79.1 | 76.5 |

</div>

<sub>Comparison scores are taken from the corresponding benchmark leaderboards.</sub>

Motif 3 performs particularly well on **agentic and tool-oriented** benchmarks, while maintaining competitive performance across coding, mathematical reasoning, and general knowledge. On AA-Omniscience it pairs its accuracy with one of the highest non-hallucination scores, indicating a favorable balance between answering correctly and abstaining when unsupported.

## 4. Architecture

> [!NOTE]
> The architecture and distributed training framework used for Motif 3 are available at [MotifTechnologies/motif3-training-example](https://github.com/MotifTechnologies/motif3-training-example).

Motif 3 is a fully in-house design and introduces several custom components (full details in the technical report):

- **Grouped Differential Latent Attention (GDLA)** — integrates grouped differential attention (asymmetric signal/noise heads with a token-dependent differential coefficient) with the compressed KV latent of Multi-head Latent Attention, plus a query-dependent output gate. Retains the expressive attention dynamics of differential attention while substantially reducing KV-cache requirements.
- **Expert-Specific PolyNorm** — replaces the SiLU gate with a learned polynomial normalization whose coefficients are learned independently per expert, reducing activation outliers while allowing each expert to specialize.
- **Modified manifold-constrained hyper-connections (mHC)** — replaces conventional residual additions with a doubly-stochastic (Birkhoff-polytope) mixing of 4 parallel residual streams; the post-mapping multiplier is annealed from 2 → 1 during pretraining to limit activation-outlier accumulation.
- **Multi-Token Prediction (MTP)** — a 1-layer MTP head (DeepSeek-V3 style) used as an auxiliary pretraining objective and enabling **self-speculative decoding** at inference.

## 5. Deployment — vLLM (Recommended)

> [!Note]
> - Tested on **B200 and H200** GPUs.
> - The model ships with a built-in **MTP head** (`num_nextn_predict_layers=1`), so it supports **self-speculative decoding** — add `--speculative-config` as shown below (`num_speculative_tokens: 1` is optimal for this model).
> - Supports online block-fp8 quantization with ```--quantization modelopt_blockfp8```
> - If you encounter any issues, please open an HF issue.

> [!Tip]
> Looking for a smaller footprint? An **NVFP4-quantized** checkpoint is available at [**Motif-Technologies/Motif-3-NVFP4**](https://huggingface.co/Motif-Technologies/Motif-3-NVFP4).

- **vLLM repo:** [MotifTechnologies/vllm](https://github.com/MotifTechnologies/vllm) — public vLLM fork with Motif-3 support (based on vLLM v0.26.0)
- **Docker image:** `ghcr.io/motiftechnologies/vllm:v0.26.0-motif3`

### 5.1 H200

```bash
vllm serve "Motif-Technologies/Motif-3" \
    --trust-remote-code \
    --quantization modelopt_blockfp8 \
    --speculative-config '{"model": "Motif-Technologies/Motif-3", "num_speculative_tokens": 1}' \
    --tensor-parallel-size 1 \
    --data-parallel-size 8 \
    --data-parallel-size-local 8 \
    --enable-expert-parallel \
    --enable-auto-tool-choice \
    --tool-call-parser motif \
    --reasoning-parser motif \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --max-model-len 262144 \
    --block-size 128 \
    --attention-backend FLASH_ATTN_MLA \
    --host 0.0.0.0 --port 8080
```

### 5.2 B200

```bash
vllm serve "Motif-Technologies/Motif-3" \
    --trust-remote-code \
    --quantization modelopt_blockfp8 \
    --speculative-config '{"model": "Motif-Technologies/Motif-3", "num_speculative_tokens": 1}' \
    --tensor-parallel-size 1 \
    --data-parallel-size 8 \
    --data-parallel-size-local 8 \
    --enable-expert-parallel \
    --enable-auto-tool-choice \
    --tool-call-parser motif \
    --reasoning-parser motif \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --max-model-len 262144 \
    --block-size 128 \
    --host 0.0.0.0 --port 8080
```

## 6. Access

This model is **openly available** — anyone can download the weights, no access request required.

## 7. License

This model is released under the **MIT License**. See the [LICENSE](https://huggingface.co/Motif-Technologies/Motif-3/blob/main/LICENSE.md) file for details.  
If you build on Motif 3, we'd truly appreciate a mention (e.g., "Built with Motif 3") when you share your work. Thanks for building with Motif!

## 8. Citation
```
@misc{lim2026motif3technicalreport,
      title={Motif 3: Technical Report}, 
      author={Junghwan Lim and Joon Son Chung and Sungmin Lee and Wai Ting Cheung and Gihun Cho and Minsu Ha and Sangho Kang and Beomgyu Kim and Dongseok Kim and Jangwoong Kim and Taehyun Kim and Taewhan Kim and Jeesoo Lee and Jeongdoo Lee and Junhyeok Lee and Dongpin Oh and Hyeyeon Cho and Dahye Choi and Jaeheui Her and Hanbin Jung and Changjin Kang and Minjae Kim and Youngrok Kim and Hyukjin Kweon and Hongjoo Lee and Yeongjae Park and Bokki Ryu},
      year={2026},
      eprint={2608.09119},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2608.09119}, 
}
```
---

© Motif Technologies. All rights reserved.