---
license: apache-2.0
pipeline_tag: text-generation
base_model:
- RecursiveSI/flint
tags:
- flint
- unsloth
---

# Read our How to [Run Flint Guide!](https://unsloth.ai/docs/models/flint)

<div>
<p style="margin-top: 0;margin-bottom: 0;">
   <em>See <a href="https://unsloth.ai/docs/basics/unsloth-dynamic-v3.0-gguf">Unsloth Dynamic 3.0 GGUFs</a> for our quantization benchmarks.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; ">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/models/flint">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>
    <li>See further below for quant benchmarks.</li>
    <li>See below for Flint running in Unsloth Desktop with thinking controls:</li>
</div>

<img width="600" alt="Flint unsloth desktop" src="https://unsloth.ai/docs/~gitbook/image?url=https%3A%2F%2F3215535692-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxhOjnexMCB3dmuQFQ2Zq%252Fuploads%252FGXYEQqEXseTna162HHNa%252Fflint%2520pic.webp%3Falt%3Dmedia%26token%3Dbcddff05-8e5d-4026-a05e-02cab135af2e&width=768&dpr=3&quality=100&sign=24cac22b3cd83ea2ce836d006edc43a1&sv=3" />

## Flint Unsloth GGUF Benchmarks
<div style="display: flex; gap: 8px; align-items: flex-start;">
  <img src="assets/size_vs_kld.png" alt="Flint Unsloth GGUF KLD vs size" style="width: 50%; min-width: 0; margin: 0;">
  <img src="assets/size_vs_top1.png" alt="Flint Unsloth GGUF top-1 accuracy vs size" style="width: 50%; min-width: 0; margin: 0;">
</div>

---

<p align="center">
  <img src="assets/flint-logo.png" width="160" alt="Flint logo">
</p>

<h1 align="center">Recursive Flint</h1>

<p align="center">
  <a href="https://www.recursive.com/updates/introducing-recursive-flint">Blog</a> |
  <a href="https://huggingface.co/RecursiveSI">Hugging Face</a> |
  <a href="https://github.com/recursive-oss/rec">Local engine</a> |
  <a href="https://docs.recursive.com/getting-started">Documentation</a>
</p>

Flint is Recursive’s mixture-of-experts language model for coding agents, with 39.8 billion total parameters and approximately 2.5 billion active per token. It is designed to investigate codebases, fix bugs, implement features, and write tests.

Flint supports text input and output, reasoning, and multi-turn tool use. In our release evaluations, it scores 54.9% on Terminal-Bench 2.1, 89.7% on SWE-bench Pro v2, and 74.2% on SWE-bench Verified.

This repository contains the BF16 checkpoint, model configuration, tokenizer, chat template, and an SGLang serving kit. Quantized variants are prepared separately for NVIDIA and Apple Silicon runtimes.

## Evaluation

![Flint benchmark performance: BF16 and NVFP4 checkpoints compared with local models that run on similar hardware](https://huggingface.co/RecursiveSI/flint/resolve/main/assets/flint_benchmarks_nvfp4.png)

Flint results use temperature 1.0, top-p 0.95, and top-k 20. Terminal-Bench uses Terminus 2; SWE-bench uses mini-swe-agent. Agentic scores report average pass@1 over at least five attempts. † marks scores measured by Recursive; other comparison scores are developer-reported.

Evaluation setups vary across sources. Flint’s Terminal-Bench score counts solutions obtained through web retrieval as unsuccessful; developer-reported scores may not apply the same adjustment.

## Model specifications

| Property | Flint |
| :---- | :---- |
| Developer | Recursive |
| Architecture | Decoder-only mixture-of-experts Transformer |
| Total parameters | 39.8B |
| Active parameters per token | Approximately 2.5B, including the output head¹ |
| Layers | 49: 2 dense layers followed by 47 MoE layers |
| Attention | 35 sliding-window layers and 14 full-attention layers |
| Sliding window | 513 tokens: the current token and 512 preceding tokens |
| Attention heads | 32 query heads and 4 key/value heads; head dimension 128 |
| Attention normalization | Per-head QK RMSNorm and learned per-head attention sinks |
| Position encoding | RoPE on sliding-window layers; no positional encoding on full-attention layers |
| Experts per MoE layer | 256 routed experts, with 6 selected per token, plus an always-active shared expert |
| Documented context configuration | 262,144 tokens, including prompt and generated output |
| Vocabulary | 150,144 tokens |
| Input / output | Text / text |
| Stated knowledge cutoff | June 2026 |

¹ The active-parameter convention includes the output head and excludes the full input embedding matrix. The active body alone is approximately 2.2B parameters. “40B-A2.5B” is the rounded model-size designation.

### Recommended generation settings

| Setting | Value |
| :---- | :---- |
| Temperature | 1.0 |
| Top-p / top-k | 0.95 / 20 |
| Output budget for hard problems | At least 32768 tokens, including reasoning |

The server applies these sampling settings when a request omits them. Flint supports OpenAI-compatible tool calls. Use the checkpoint’s chat template and preserve returned `reasoning_content` in conversation history. Prompt and output share the context window.

## Training

Flint was trained from scratch through pretraining, mid-training, supervised fine-tuning, and reinforcement learning. Training includes text and code, instruction following, and agentic tasks.

## Limitations and responsible use

Flint’s supervised fine-tuning included safety-oriented examples, but the model can still produce incorrect or harmful content, faulty code, or inappropriate tool calls. Test generated code and review consequential changes before applying them. Tool-using applications should enforce their own permissions and execution boundaries; structured tool-call grammar does not prevent the model from choosing an unsafe or incorrect action.

Long reasoning can increase latency and exhaust the output budget before an answer is complete. The context configuration is a capacity limit, not a guarantee of uniform accuracy across all sequence lengths or tasks. Results can vary with checkpoint precision and inference runtime; evaluate the specific checkpoint and runtime you intend to deploy.

## License and reporting

Flint is released under the [Apache 2.0 license](LICENSE). Hosted API terms and data practices are separate from the weight license.

For model and serving issues, contact support@recursive.com and include the checkpoint revision, runtime version, hardware, launch command, and a minimal reproduction. Report safety concerns or suspected misuse to safety@recursive.com, and security vulnerabilities to security@recursive.com.