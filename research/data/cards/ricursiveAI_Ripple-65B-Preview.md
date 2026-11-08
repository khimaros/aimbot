---
license: apache-2.0
---
# Ripple-65B Preview

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://framerusercontent.com/images/rSaJGoPP1Saln5kpScZNGCw.png" width="30%">
  <source media="(prefers-color-scheme: light)" srcset="https://framerusercontent.com/images/3rFANSmoZuSBhjRwxZolyEU5guo.png" width="30%">
  <img alt="Ricursive Logo" src="https://framerusercontent.com/images/3rFANSmoZuSBhjRwxZolyEU5guo.png" width="30%">
</picture>
</div>

<p align="center">
  <a href="https://huggingface.co/ricursiveAI/Ripple-65B-Preview">BF16</a> |
  <a href="https://huggingface.co/ricursiveAI/Ripple-65B-Preview-NVFP4">NVFP4</a> |
  <a href="https://huggingface.co/ricursiveAI/Ripple-65B-Base-Preview">Base Model</a> |
  <a href="https://huggingface.co/ricursiveAI/Ripple-65B-Preview-DFlash2">DFlash2</a> |
  <a href="https://www.ricursive.com/ripple">Launch Blog</a> | 
  License: <a href="https://huggingface.co/ricursiveAI/Ripple-65B-Preview/blob/main/LICENSE">Apache 2.0</a>
</p>

Ricursive Intelligence introduces **Ripple-65B Preview**, a 65B parameter dense Transformer model pretrained on 12 trillion tokens with support for up to 1Mi (1,048,576 tokens) of context. 
Ripple-65B Preview delivers strong results on agentic coding, scoring **80.52 on TerminalBench 2.1** and
surpassing significantly-larger US open-weight models such as Reflection Beam 501B (**80.1**), Meta Muse Spark Open 816B (**76.4**), 
Thinking Machines Inkling 975B (**63.8**), and NVIDIA Nemotron 3 Ultra 550B (**56.4**). 

Our Preview release includes an instruction-tuned model in BF16 and NVFP4 numerics, and a BF16 base model. **This repo contains the BF16 instruction-tuned model.**

Starting from an initial Olmo 3 baseline, we iteratively improved all aspects of the training recipe including pretraining scaling laws, model architecture, data, and posttraining stack.
Our final Ripple v1 model ladder improves Compute Efficiency (CE) on code by **16x** relative to the Olmo 3 ladder, with the advantage further increasing with scale up to 
**55x** for the full hero run. 

Ripple-65B was codesigned to be trained and served efficiently on NVIDIA hardware.
For our first model, a key objective was to make design decisions which reduce pretraining and posttraining
infrastructure complexity while still enabling strong reasoning and agentic performance.
Therefore, we chose to train a modernized dense Transformer model rather than use Mixture-of-Experts (MoE) like other labs.
This decision quickly paid off, and we were able to train a strong model from scratch with a small team that scaled from 1 to 5 people during development, 
while maintaining solid MFU (40%) throughout pretraining and posttraining with simple sharding, no custom kernels, and no quantization (BF16).

Ripple-65B uses a **thin-and-deep** model aspect ratio, with a narrow d_model (5120) and 80 total layers.
We switch from the Olmo 3 llama-like architecture to a Gemma 3N-like architecture to improve training stability at scale. 
To improve reasoning performance, we **overprovision the number of attention heads** while increasing the SWA-to-global layer ratio 
and reducing SWA window size to compensate for the increased cost.
In addition, we added FFN activation clipping, gated attention, global NoPE, and value residuals.

The end result is a model that is especially capable at reasoning and agentic tasks given its model size, matching or exceeding other 
US open-weight models with more than 10x the number of total parameters.
At only 65B total parameters, the model can fit on consumer hardware such as the NVIDIA DGX Spark. 
To encourage local model development, we provide an NVFP4 checkpoint and colab to help you get started. 
The model is also fast at token generation when running on datacenter GPUs, reaching 250 tok/s on 2xB200 batch=8 prior to quantization or custom kernels. 

**Pre-training.** Ripple-65B Preview is pretrained from scratch on our 12T text-only predominantly-English and code corpus at 8K sequence length. 
Ripple-65B Base Preview is a **pretrain-only checkpoint** without any midtraining or synthetic QA data.

**Post-training.** We use a standard post-training recipe consisting of midtraining, long context, SFT, long context SFT, and mixed domain RL. 
Our Preview release has gone through relatively light posttraining, with a focus on agentic coding.

We show a brief overview of each stage below:

<div align="center">

| Stage | Tokens | Step | Seqlen | Batch Size | 
| ----- | ------ | ------ | ---- | ----- |
| Pretrain | 12T | 877,500 | 8K | 1408 -> 3072 |
| Midtrain | 200B | 8,000 | 64K | 384 |
| Long Context | 6.5B | 389 | 2M | 8 |
| SFT | 183B | 7,274 | 128K | 192 |
| LC SFT | 13.5B | 802 | 2M | 8 | 
| RL  | N/A  | 700 | 128K | 2048 |

</div>

## Instruct Model Benchmarks

We compare Ripple-65B Preview against currently-available US open-weight frontier models.
All models are tested at full BF16 precision with maximum effort levels.

Each lab typically only provides a limited subset of available benchmarks.
Our table below shows official model card scores where available, and we use our own in-house eval flow for missing evals (italized).
For SWE-bench Pro v2.0 Hard and DeepSWE 1.1, we use Terminus 2 for Ripple-65B Preview.
In other cases where the harness is not specified, we use OpenCode.
A higher number is better for all benchmarks.

Replicating benchmark scores has been challenging, particularly for modern agentic evals, due to the number of factors which can cause 
eval scores to shift. 
For example, we found that Terminal-Bench 2.1 scores were universally lower (with the exception of Muse Spark Open) 
when using the official Terminus 2 harness at 128K sequence length with summarization.
Therefore, our results represent a best-effort attempt at a fair comparison.

<div align="center">

  | Benchmark | Ripple-65B<br>Preview | Nemotron 3<br>Ultra 550B | Inkling<br>975B | Muse Spark<br>Open 816B | Reflection<br>Beam 501B |
  |---|---|---|---|---|---|
  | **Model** | | | | | |
  | Architecture | Dense | MoE | MoE | MoE | MoE |
  | Total params | 65B | 550B | **975B** | 816B | 501B |
  | Active params | **65B** | 55B | 41B | 42B | 23B |
  | Pre-training tokens | 12T | 20T | **45T** | N/A | 23.8T |
  | **Knowledge** | | | | | |
  | MMLU | 89.6 | *92.0* | *91.3* | ***92.6*** | *92.4* |
  | MMLU-Pro | 84.2 | 86.8 | *87.3* | ***87.9*** | *76.5* |
  | GPQA Diamond | 85.2 | 87.0 | 87.2 | 89.0 | **90.6** |
  | **Math** | | | | | |
  | AIME 2024 | 97.1 | *94.2* | *97.5* | ***97.9*** | *96.7* | 
  | AIME 2025 | 98.3 | *94.2* | *91.7* | ***100.0*** | *99.6* |
  | AIME 2026 | 95.0 | *95.4* | 97.1 | ***98.3*** | 97.7 |
  | HMMT Feb 2026 | 90.5 | *80.3* | 86.3 | ***93.9*** | ***93.9*** | 
  | **Coding & Agentic** | | | | | |
  | Terminal-Bench 2.1 (self-reported) | **80.5** | 56.4 | 63.8 | 76.4 | 80.1 |
  | Terminal-Bench 2.1 (Terminus 2) | **80.5** | *55.1* | *56.2* | *78.7* | *70.8* |
  | SWE-bench Verified | 76.5 | 71.9 | 77.6 | *78.7* | **81.6** |
  | SWE-bench Pro v1.0 | 61.42 | *46.9* | 54.3 | *58.2* | **66.1** |
  | SWE-bench Pro v2.0 Hard | **79.1** | *30.7* | *39.6* | *72.4* | 76.5 |
  | DeepSWE 1.1 | 44.3 | *0.2* | *1.8* | **60.0** | 43.3 |
  | SciCode (Inspect AI) | 39.4 | 44.6 | 46.1 | **58.5** | 49.2 | 
  | τ³-bench banking | 31.27 | 22.6 | 23.7 | *14.4* | **36.1** |
  | AutomationBench (Public) | 36.4 | *8.4* | *14.6* | *42.4* | 39.3 | 
  | MCP Atlas | 71.67 | *62.2* | 76.0 | **89.2** | 80.8 |
  | **Safety** | | | | | |
  | FORTRESS Adversarial | 83.8 | *79.3* | 78.0 | **94.2** | *92.1* |
  | FORTRESS Benign | 95.5 | *89.1* | **95.9** | *82.6* | *86.4* |
  | StrongREJECT | 97.5 | *98.2* | **98.6** | *94.7* | *95.8* |
  | **Instruction Following**  | | | | | |
  | IFBench | 79.2 | **81.7** | 79.8 | *78.6* | 79.6 |
  | **Long Context**  | | | | | |
  | AA-LCR | 75.0 | 65.4 | *78.3* | ***80.7*** | 78.2 |

</div>


## Base Model Benchmarks

We show traditional pretraining evals comparing Ripple-65B Base Preview against a selection of open-weight base models. Although we would have liked to 
compare against the same set of models throughout the model card, many companies are now choosing to only open-source their instruction-tuned models.

With the rise of the importance of posttraining, many modern LLM recipes now blend posttraining data earlier into the training process, including during pretraining.
For our first model, we kept our pretraining data clean with minimal synthetic data, focusing on high quality natural data rather than aggressively targeting evals.
We instead added significantly more synthetic data during midtraining, which allowed us to quickly iterate on our synthetic data recipe without blocking pretraining.

Ripple-65B Base Preview is a pretrain-only checkpoint. The base model overall beats Poolside Laguna M.1,
and is comparable with DeepSeek V3.1 and V4 Flash on reasoning, math, and code.
Nemotron 3 Ultra dominates on traditional pretraining evals, likely due to their heavy use of [task-seeded synthetic data](https://huggingface.co/blog/nvidia/task-seeded-sdg).
However, its pretraining eval performance did not translate to modern agentic tasks, likely due to their synthetic data being out of distribution relative to these tasks.

We report official model results where available.
For our own model and for missing evals, we use our internal fork of [Olmes](https://github.com/allenai/olmes).

<div align="center">

  | Benchmark (Metric) | # Shots | Ripple-65B<br>Preview | Laguna<br>M.1 225B | DeepSeek<br>V3.1 671B | DeepSeek<br>V4 Flash 284B | Nemotron 3<br>Ultra 550B |
  |---|---|---|---|---|---|---|
  | **Model** | | | | | | |
  | Architecture | — | Dense | MoE | MoE | MoE | MoE |
  | Total params | — | 65B | 225B | **671B** | 284B | 550B |
  | Active params | — | **65B** | 23B | 37B | 13B | 55B |
  | Training tokens (T) | — | 12T | 30T+ | 15.6T | **32T+** | 20T |
  | **World Knowledge** | | | | | | |
  | MMLU (MC acc) | 5-shot | *83.7* | *76.6* | *88.3* | 88.7 | **89.1** |
  | MMLU-Pro (CoT EM) | 5-shot | *61.5* | *52.2* | *57.8* | 68.3 | **79.1** |
  | AGIEval-En (acc) | 3-5-shot | *74.4* | *66.2* | *81.9* | **83.9** | 78.7 |
  | GPQA main (CoT EM) | 5-shot | *37.7* | *31.7* | *30.8* | *44.0* | ***49.6*** |
  | GPQA-Diamond (CoT EM) | 5-shot | *38.4* | *27.8* | *37.4* | *44.4* | ***53.0*** |
  | C-Eval (MC acc) | 5-shot | *69.6* | *59.3* | *90.7* | **92.1** | *82.2* |
  | SuperGPQA (MC acc) | 5-shot | *34.2* | *24.5* | *43.1* | 46.5 | ***52.9*** |
  | SimpleQA-Verified (EM) | 25-shot | *10.1* | *10.8* | *17.3* | **30.1** | *27.1* |
  | **Language & Reasoning** | | | | | | | 
  | BBH (CoT EM) | 3-shot | *85.6* | *79.6* | *87.2* | 86.9 | ***88.0*** | 
  | BBEH (EM) | 1-shot | *17.9* | *14.2* | *18.4* | **25.4** | *21.2* |
  | DROP (F1) | 1-shot | *77.8* | *66.8* | *81.2* | **88.6** | *87.6* |
  | HellaSwag (acc_norm) | 0-shot | *84.6* | *86.2* | *86.8* | 85.7 | ***89.1*** |
  | HellaSwag (acc_norm) | 10-shot | *87.2* | *88.1* | *89.4* | *88.8* | **90.5** |
  | ARC-Challenge (MC acc) | 25-shot | *95.7* | *90.8* | *95.1* | *95.8* | **97.4** |
  | OpenBookQA (acc_norm) | 0-shot | *47.4* | *48.6* | ***50.4*** | *48.0* | 48.6 |
  | PIQA (acc_norm) | 0-shot | *83.6* | *84.8* | ***85.2*** | *84.7* | 83.8 |
  | WinoGrande (acc) | 5-shot | ***83.4*** | *83.2* | *83.2* | *81.4* | 79.3 |
  | **Code & Math** | | | | | | |
  | HumanEval (pass@1, n=20, T=0.2) | 0-shot | *70.9* | *83.4* | *69.8* | 69.5 | **83.8** |
  | MBPP Sanitized (pass@1, n=32, T=0.2) | 3-shot | *81.5* | *81.1* | *75.2* | *74.6* | **86.0** |
  | BigCodeBench (pass@1, n=5, T=0.8) | 3-shot | *49.2* | *50.5* | ***59.9*** | 56.8 | *55.6* |
  | GSM8K (CoT EM) | 8-shot | *88.5* | *80.4* | *79.6* | **90.8** | 88.1 |
  | GSM1K (CoT EM) | 8-shot | *88.4* | *79.7* | *81.8* | *83.2* | ***90.2*** |
  | MATH (flex EM) | 4-shot | *59.1* | *52.5* | *59.7* | 57.4 | **82.0** |
  | MGSM (CoT EM, 11-lang avg) | 8-shot | *78.2* | *65.4* | *81.7* | 85.7 | **87.7** |


</div>

## Citation

```bibtex
@misc{ricursive2026ripple65b,
      title={Ripple-65B: Pushing the Frontier of Local Intelligence},
      author={Ricursive Intelligence},
      year={2026},
}
```

## Contact

For questions and comments, please contact us at [info@ricursive.com](mailto:info@ricursive.com). To learn more, please visit our [website](https://www.ricursive.com).