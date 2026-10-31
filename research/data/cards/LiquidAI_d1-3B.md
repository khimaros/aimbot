---
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
language:
- ar
- zh
- en
- fr
- de
- hi
- id
- it
- ja
- ko
- pl
- pt
- ru
- es
- th
- vi
pipeline_tag: image-text-to-text
base_model: LiquidAI/LFM2.5-VL-3B
tags:
- liquid
- lfm2.5
- edge
- decision
- classification
- calibration
- system-one
- multimodal
- decision-model
---

<div align="center">
  <img
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> •
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> •
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# d1-3B

d1-3B is a 3B parameter **decision model** built on [LFM2.5-VL-3B](https://huggingface.co/LiquidAI/LFM2.5-VL-3B).
You give it a state (text, JSON, images, or a mix) and a set of questions. It returns calibrated,
typed answers in **one forward pass with zero output tokens**.

- **Best decision model under 10B on the Decision Index 0.2.1**: 48.57, ahead of every 4B and 9B model
  and of Decider 35B-A3B (47.11).
- **Multimodal**: images and text in the same state. It scores 74.1 on 11 public image benchmarks
  (LFM2.5-VL-3B: 73.9).
- **Fast**: 8 ms a decision on an NVIDIA RTX 4090, 9 ms on an AMD MI325X, 30 ms on an Apple M5 Pro.

Find more information about open d1 in our [blog post](https://www.liquid.ai/blog/open-d1).

![image](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/r2H7UlZ_m48SYAhZWIHiu.png)

> [!NOTE]
> 💻 **Demos**: Try d1-3B in a Hugging Face space without any setup:
> [**Open d1 Arcade**](https://huggingface.co/spaces/LiquidAI/system-one-arcade): Collection of 10 demos using d1-3B


## 🗒️ Model Details

| Model | Parameters | Description |
|---|---|---|
| [LFM2.5-VL-3B](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) | 3.1B | General-purpose vision-language model (base) |
| **[d1-3B](https://huggingface.co/LiquidAI/d1-3B)** | 3.1B | Post-trained for single-pass, calibrated decisions |

d1-3B is a multimodal decision model with the following features:

- **Total parameters**: 3.12B
- **Vision encoder**: SigLIP2 NaFlex shape-optimized 400M
- **Context length**: 32,768 tokens
- **Vocabulary size**: 128,000

We recommend d1-3B wherever a pipeline needs a yes/no, a pick from named options, or a rating:
routing and triage, moderation, intent and topic classification, extraction checks, reranking, LLM-as-a-judge
scoring, agent guardrails, and visual inspection. It is not a chat model and does not write text.

## 🏃 How to use

Install the dependencies (requires `transformers>=5.14`):

```bash
pip install "transformers>=5.14" torch torchvision pillow
```

The model ships its own code, so load it with `trust_remote_code=True`:

```python
import torch
from transformers import AutoModel
from transformers.image_utils import load_image

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float32 if device == "cpu" else torch.bfloat16
model = AutoModel.from_pretrained("LiquidAI/d1-3B", trust_remote_code=True, dtype=dtype).to(device)

# Text: several named questions over one state, answered in one pass
questions = {
    "refund": {
        "type": "noul",
        "instructions": "Is the customer asking for a refund?",
    },
    "team": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {
            "billing": "Charges, refunds, invoices",
            "technical": "App or site faults",
            "fraud": "Suspected unauthorised use",
        },
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["Can wait", "Today", "Blocking the customer now"],
    },
}
print(model.system_one("I was charged twice this month, please refund one of them.", questions))

# Image: the photo is the whole state
image = load_image("http://images.cocodataset.org/val2017/000000039769.jpg")  # two cats on a sofa
cats = {
    "type": "choice",
    "instructions": "How many cats are there?",
    "criteria": {"one": "One", "two": "Two", "more": "Three or more"},
}
print(model.system_one(None, {"cats": cats}, images=[image]))

# Batch: many requests, packed together with no padding
tickets = ["Where is my parcel? It was due Monday.", "The app crashes when I open settings."]
print(model.system_one_batch([(t, {"team": questions["team"]}) for t in tickets]))
```

| call | |
|---|---|
| `system_one(state, questions, images=None)` | Named questions over one state, in one pass. The state and its images are read once for all questions. |
| `system_one_batch([(state, questions[, images]), ...])` | Many requests, packed with no padding. |

A state is a string, any JSON value, or `None` when the images are the whole state.

### Questions and answers

Questions follow the Decision Index schema: `type`, `instructions`, and `criteria`.

| `type` | `criteria` | answer fields |
|---|---|---|
| `noul`: yes or no | optional: `{"true": "...", "false": "..."}` to define each side | `noul`: P(yes) |
| `choice`: one of named options | `{name: description}` | `choice`, `confidence`, `probabilities` |
| `score`: 2 to 10 ordered levels | a list of level descriptions, lowest first | `score` (the expected level), `confidence`, `probabilities`, `legend` |

Each call returns `{"answers": {name: answer}, "usage": {"input_tokens": n, "output_tokens": 0}}`.

## ⚡ Speed

Warm calls, one request at a time: a single question, three questions over one state, a 3.4k-token
state and a 384 px image. The last column is throughput with 64 states packed into one pass.

### Edge Inference

We measure latency on an Apple M5 Pro and, in collaboration with NVIDIA, on an NVIDIA Jetson AGX Thor,
a Jetson AGX Orin 64 GB and a Jetson Orin Nano.

| | one question | 3 questions, one pass | 3.4k-token state | 384 px image | 64 states, packed |
|---|---:|---:|---:|---:|---:|
| Apple M5 Pro (`mps`) | 30 ms | 41 ms | 640 ms | 62 ms | 78 / s |
| NVIDIA Jetson AGX Thor | 16 ms | 20 ms | 220 ms | 35 ms | 262 / s |
| NVIDIA Jetson AGX Orin 64 GB | 26 ms | 35 ms | 560 ms | 83 ms | 110 / s |
| NVIDIA Jetson Orin Nano | 50 ms | 73 ms | 1640 ms | 202 ms | 38 / s |

### GPU Inference

We measure latency on an NVIDIA RTX 4090 and an AMD MI325X, in bf16, median of 20 runs.

| | one question | 3 questions, one pass | 3.4k-token state | 384 px image | 64 states, packed |
|---|---:|---:|---:|---:|---:|
| NVIDIA RTX 4090 | 8 ms | 21 ms | 102 ms | 17 ms | 475 / s |
| AMD MI325X | 9 ms | 14 ms | 44 ms | 18 ms | 1,106 / s |

On NVIDIA GPUs, `model.compile(mode="reduce-overhead")` runs single questions as CUDA graphs (the RTX 4090
row uses it). Without it, a single question takes 16 ms. The first call with a new shape pays for kernel
selection or compilation, so warm up the shapes you serve.

## 📊 Performance

All results are on public benchmarks.

### Decision Index 0.2.1

We scored d1-3B with the official scorer (not a leaderboard submission). All other rows come from the public leaderboard v0.2.1.

| Model | Size | Decision Index | Knowledge | Language | Retrieval | Tools | Arts |
|---|---:|---:|---:|---:|---:|---:|---:|
| Winnow-12B | 12B | 50.02 | 33.8 | 56.0 | 54.0 | 71.0 | 30.0 |
| **d1-3B** | **3B** | **48.57** | 23.8 | 56.4 | 52.8 | **74.5** | **36.3** |
| Decider 35B-A3B | 36B | 47.11 | 31.8 | 55.5 | 54.7 | 56.5 | 32.6 |
| JPT-9B | 9.7B | 46.89 | 31.7 | 56.7 | 44.6 | 67.0 | 28.6 |
| Decision 1.0 Lux | 9.7B | 43.49 | 30.9 | 48.0 | 50.0 | 57.2 | 26.4 |
| JPT-4B | 4.7B | 43.04 | 28.7 | 52.5 | 45.0 | 57.2 | 25.8 |
| Jet v6.2 | 4.7B | 42.60 | 28.7 | 43.9 | 48.2 | 62.9 | 27.0 |
| Decider 4B | 4.7B | 40.70 | 25.7 | 46.0 | 44.7 | 58.6 | 25.0 |
| Winnow-E4B | 8.0B | 39.89 | 22.3 | 45.1 | 43.8 | 62.5 | 22.8 |
| Decider 2B | 2.3B | 28.97 | 14.9 | 32.6 | 37.3 | 42.4 | 14.6 |

### Benchmarks as decisions

Besides the Decision Index, we added a few other internal evaluations based on public benchmarks.

| Benchmark | d1-3B | Decider 4B | Decider 2B |
|---|---:|---:|---:|
| SQuAD 2.0 | **85.3** | 76.0 | 67.7 |
| Civil Comments | 93.0 | 92.8 | **93.6** |
| MASSIVE intent | 87.3 | **88.3** | 81.1 |
| HelpSteer2 | 36.7 | **42.0** | 32.0 |
| PubMedQA | **66.0** | 63.3 | 65.7 |
| BoolQ | 86.7 | **89.0** | 87.3 |
| XNLI | 85.0 | **88.6** | 85.0 |
| PAWS-X | **76.9** | 69.8 | 59.5 |
| **Mean** | **77.1** | 76.2 | 71.5 |

d1-3B also scores 71.8 on [DecisionBench](https://huggingface.co/datasets/Hanno-Labs/decision-bench) (eng v1,
all 23,900 rows) and 69.3 on [Fast Decisions](https://huggingface.co/datasets/fastino/fast-decisions)
(dev split).

### Vision

Eleven public image benchmarks, read as decisions over each benchmark's options (at most 1,000 rows each),
compared with the base model:

| Benchmark | d1-3B | LFM2.5-VL-3B |
|---|---:|---:|
| AI2D | 79.9 | 80.9 |
| BLINK | 59.2 | 58.7 |
| CV-Bench | 82.1 | 87.6 |
| HallusionBench | 65.3 | 65.0 |
| MMBench | 84.9 | 84.3 |
| MME | 82.1 | 82.4 |
| MMStar | 59.9 | 61.2 |
| MMVP | 77.0 | 73.7 |
| POPE | 88.5 | 90.1 |
| VisualWebBench | 71.4 | 78.3 |
| VL-RewardBench | 65.0 | 50.9 |
| **Mean** | **74.1** | 73.9 |
| [ImajevBench](https://huggingface.co/datasets/mohit67890/imajev-bench) (dev and calibration, 253 rows) | 64.0 | 66.8 |

With the images removed, the same questions score 45.1, so the answers come from the images.

## 📬 Contact

- Got questions or want to connect? [Join our Discord community](https://discord.com/invite/liquid-ai)
- If you are interested in custom solutions with edge deployment, please contact [our sales team](https://www.liquid.ai/contact).

## Citation

```bibtex
@article{liquidAI2026opend1,
  author  = {Liquid AI},
  title   = {Open d1: Edge decision models for text, vision, and audio},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {https://www.liquid.ai/blog/d1-open},
}
```

```bibtex
@article{liquidai2025lfm2,
  title   = {LFM2 Technical Report},
  author  = {Liquid AI},
  journal = {arXiv preprint arXiv:2511.23404},
  year    = {2025}
}
```
