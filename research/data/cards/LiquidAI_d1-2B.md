---
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: image-text-to-text
base_model: LiquidAI/LFM3-VL-2B
tags:
- liquid
- lfm3
- edge
- decision
- classification
- extraction
- calibration
- system-one
- multimodal
- decision-model
- custom_code
language:
- en
- ar
- zh
- fr
- de
- it
- ja
- ko
- pt
- es
- vi
- th
- id
- hi
- ru
- pl
---

<div align="center">
  <img
    src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/liquid-ai-banner.webp"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0;"
  />
  <div align="center" style="display: flex; justify-content: center; align-items: center; gap: 1.25em; margin: 8px 0 1.7rem; padding: 0; line-height: 1.3;">
    <a href="https://console.liquid.ai/dashboard" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/icons/api.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>API</strong></a>
    <a href="https://playground.liquid.ai/" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/icons/try.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Try</strong></a>
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/icons/docs.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Docs</strong></a>
    <a href="https://www.liquid.ai/blog/open-d1" style="display: inline-flex; align-items: center; gap: 6px;"><img src="https://huggingface.co/LiquidAI/d1-2B/resolve/main/assets/icons/blog.svg" width="16" height="16" alt="" aria-hidden="true" style="display: block; flex: 0 0 16px; width: 16px; height: 16px; margin: 0;" /><strong>Blog</strong></a>
  </div>
</div>

# d1-2B

d1-2B is a **decision model for text, pictures, and video**, built on [LFM3-VL-2B](https://huggingface.co/LiquidAI/LFM3-VL-2B). It returns calibrated answers in one forward pass, without generating tokens.

- **Best-in-class:** it leads the open d1 models on average and on our board of over a hundred decision benchmarks, ahead of d1-3B at under two thirds of its size.
- **Beyond classification:** it also extracts text, numbers, and dates with their span, locates objects in pictures, and estimates quantities with an interval.
- **Millisecond decisions:** 5.7 ms per decision on an NVIDIA H100 and 3.8 ms on an AMD MI325X, with any number of questions about one state in one call.

Find more information about open d1 in [our release blog post](https://www.liquid.ai/blog/open-d1).

## Model details
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

The [LFM3 family](https://huggingface.co/collections/LiquidAI/lfm3) includes base, text, vision, audio, omni, and decision models. d1-2B decides over text, pictures, and video, and [d1-Omni-2B](https://huggingface.co/LiquidAI/d1-Omni-2B) adds audio.

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Property</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Specification</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Checkpoint</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Post-trained decision model, built on <a href="https://huggingface.co/LiquidAI/LFM3-VL-2B">LFM3-VL-2B</a></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Parameters</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">1.92B</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Architecture</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">LFM3 backbone, 24 layers: 13 gated short convolutions, 5 sliding-window attention, 6 global attention</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Context length</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">128K tokens</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Vocabulary</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">128,000 tokens</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Input</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">A state (text or JSON), pictures or a video, and any number of named questions</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Output</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">Typed answers with their probabilities, with no generated tokens</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>Languages</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;">English, Arabic, Chinese, French, German, Italian, Japanese, Korean, Portuguese, Spanish, Vietnamese, Thai, Indonesian, Hindi, Russian, Polish</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><strong>License</strong></td>
<td style="border: 0; padding: 0.55em 0.75em;"><a href="LICENSE">LFM Open License v1.0</a></td>
</tr>
</tbody>
</table>

d1-2B is designed for any pipeline step that needs a decision: routing and triage, moderation and guardrails, intent and topic classification, extraction from documents and forms, judging and reranking, and visual inspection. It is not a chat model.

Knowledge-heavy questions favor larger models, and answers get less reliable past about 64K tokens of state. Estimates are reliable on counts and scores, less so on free quantities.

## Inference
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

d1-2B runs in [Transformers](https://docs.liquid.ai/deployment/gpu-inference/transformers) with its own model code. It reads its answers from a single forward pass, so there are no sampling parameters to set.

**Transformers quick start:**

```bash
pip install "transformers>=5.19" torch torchvision pillow
```

```python
import torch
from transformers import AutoModel

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float32 if device == "cpu" else torch.bfloat16
model = AutoModel.from_pretrained("LiquidAI/d1-2B", trust_remote_code=True, dtype=dtype).to(device)

# Several named questions over one state, answered in one pass
questions = {
    "refund": {"type": "noul", "instructions": "Is the customer asking for a refund?"},  # yes/no: P(yes)
    "team": {"type": "choice", "instructions": "Which team should handle this?",
             "criteria": {"billing": "Charges, refunds, invoices", "shipping": "Delivery and parcels",
                          "technical": "App or site faults"}},
    "topics": {"type": "choice", "multiple": True, "instructions": "Which topics does the message raise?",
               "criteria": {"billing": "Payments and charges", "delivery": "Shipping and parcels",
                            "login": "Signing in to the account"}},
    "urgency": {"type": "score", "instructions": "How urgent is this ticket?", "criteria": ["low", "medium", "high"]},
}
out = model.system_one("I was charged twice and my parcel never arrived. Please refund one charge.", questions)
a = out["answers"]
urgency = a["urgency"]["legend"][str(int(a["urgency"]["score"]))]
print(round(a["refund"]["noul"], 2), a["team"]["choice"], a["topics"]["choices"], urgency)
# 1.0 billing ['billing', 'delivery'] medium
```

<details>
<summary><strong>Values from a document</strong></summary>

```python
invoice = "ACME SA\nInvoice 2026-117\nTotal due: 1 234,50 EUR\nPay before 03/04/2026 (day/month/year)"
out = model.system_one(invoice, {
    "payee": {"type": "text", "instructions": "Who issued the invoice?"},
    "total": {"type": "number", "instructions": "How much is due?"},
    "due": {"type": "date", "instructions": "By when must it be paid?"},
    "vat": {"type": "number", "instructions": "How much VAT is charged?"},
})
a = out["answers"]
print(a["payee"]["text"], a["total"]["number"], a["due"]["date"], a["vat"]["number"])
# ACME SA 1234.5 2026-04-03 None
```

</details>

<details>
<summary><strong>Pictures and boxes</strong></summary>

Count, locate one object, or list every instance (`max` reads at most that many):

```python
from transformers.image_utils import load_image

image = load_image("http://images.cocodataset.org/val2017/000000039769.jpg")  # two cats on a sofa
out = model.system_one(None, {
    "cats": {"type": "number", "instructions": "How many cats are there?", "range": [0, 10], "step": 1},
    "remote": {"type": "box", "instructions": "Where is the remote control on the left?"},
    "every_cat": {"type": "boxes", "instructions": "Every cat.", "max": 4},
}, media=[image])
a = out["answers"]
print(a["cats"]["number"], a["every_cat"]["count"], {k: round(v, 2) for k, v in a["remote"]["box"].items()})
# 2.0 2 {'top': 0.15, 'bottom': 0.24, 'left': 0.06, 'right': 0.28}
```

</details>

<details>
<summary><strong>Many requests in one call</strong></summary>

```python
tickets = ["Where is my parcel? It was due Monday.", "The app crashes when I open settings."]
for out in model.system_one_batch([(t, {"team": questions["team"]}) for t in tickets]):
    print(out["answers"]["team"]["choice"])
# shipping
# technical
```

</details>

<details>
<summary><strong>Calls</strong></summary>

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Call</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">What it does</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>system_one(state, questions, media=None)</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">Named questions over one state, in one pass. <code>media</code> lists pictures (PIL images or <code>{&quot;type&quot;: &quot;image&quot;, &quot;path&quot;: ...}</code>) and videos as their frames (<code>{&quot;type&quot;: &quot;video&quot;, &quot;video&quot;: [PIL images], &quot;fps&quot;: 24}</code>).</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>system_one_batch([(state, questions[, media]), ...])</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">Many requests in one call, batched.</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>set_size=</code> (either call)</td>
<td style="border: 0; padding: 0.55em 0.75em;">Questions read together after the state. The default is the model's trained size (16). Larger is faster and costs some accuracy on text.</td>
</tr>
</tbody>
</table>

A state is a string, any JSON value, or `None` when the media are the whole state. Each call returns `{"answers": {name: answer}, "usage": {"input_tokens": n, "output_tokens": 0}}`.

</details>

<details>
<summary><strong>Question types</strong></summary>

<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><code>type</code></th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Question</th>
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Answer</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>noul</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">Yes or no</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>noul</code>: P(yes)</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>choice</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">One of the options <code>criteria</code> names (<code>{name: description}</code>)</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>choice</code>, <code>confidence</code>, <code>probabilities</code></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>choice</code> with <code>multiple: true</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">Any of the options <code>criteria</code> names</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>choices</code>, <code>probabilities</code> (each option's own P(yes))</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>score</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">One of 2 to 10 ordered levels, with <code>criteria</code> listing them lowest first</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>score</code> (the median level), <code>confidence</code>, <code>probabilities</code>, <code>legend</code></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>text</code>, <code>number</code>, <code>date</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">A value to read from the state</td>
<td style="border: 0; padding: 0.55em 0.75em;">The field of its type (a number with its <code>unit</code>, a date in ISO 8601), <code>span</code>, <code>found</code></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>number</code> with <code>range</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">An estimate, <code>step</code> apart</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>number</code> (the median), <code>interval</code> (p10, p90)</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><code>box</code>, <code>boxes</code></td>
<td style="border: 0; padding: 0.55em 0.75em;">One object, or every instance (16 at most, or <code>max</code>), in the one picture</td>
<td style="border: 0; padding: 0.55em 0.75em;"><code>box</code> (<code>top</code>, <code>bottom</code>, <code>left</code>, <code>right</code> as fractions of the picture), <code>found</code>, <code>confidence</code>, or <code>boxes</code> and <code>count</code></td>
</tr>
</tbody>
</table>

A value or a box is missing when `found` is under 0.5, and it is then `None`. Calibrate any decision threshold on data from your own use.

</details>

## Performance
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

### Benchmarks

d1-2B leads the open d1 models on our decision board, on average, and on most single benchmarks, ahead of d1-3B with under two thirds of its parameters.

<div role="region" tabindex="0" style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse;">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Benchmark</th>
<th scope="col" style="text-align: center; background-color: rgba(108, 79, 224, 0.08); padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);"><strong>d1<br>2B</strong></th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">d1-omni<br>600M</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">d1-Omni<br>2B</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">d1<br>3B</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em;">Decisions</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em;"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/spaces/multimodalart/jev-decision-index">Decision Index</a> public suite (v0.3)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>51.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">18.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>49.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>49.0</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/datasets/Hanno-Labs/decision-bench">DecisionBench (Hanno Labs)</a> v1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>77.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>76.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">73.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://decisionbench.ai">Decision Bench (decisionbench.ai)</a> v4</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>85.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>84.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">83.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/datasets/fastino/fast-decisions">Fast Decisions</a></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>58.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">–</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">56.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>59.3</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://github.com/fstandhartinger/jevbench">JevBench</a> v1.4.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>77.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">75.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>76.2</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/datasets/mohit67890/imajev-bench">ImajevBench</a> v2.0-lite</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>75.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">21.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>72.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">64.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://evals.typesafe.ai">WorkflowEvals</a></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>81.6</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>77.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">74.4</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;"><a href="https://huggingface.co/datasets/LocalLLaMA/typed-decisions">Typed Decisions</a></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;">61.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">57.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>63.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>65.0</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Our board (over a hundred public and private benchmarks)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>63.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">–</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>61.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.8</td>
</tr>
</tbody>
<tbody style="border: 0;">
<tr style="border: 0;"><th scope="rowgroup" style="text-align: left; background-color: transparent; padding: 0.55em 0.75em; border: 0; font-weight: 600; padding-top: 1em; padding-bottom: 0.5em; border-top: 1px solid rgba(127, 127, 127, 0.25);">Vision</th><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; background-color: rgba(108, 79, 224, 0.08); border-top: 1px solid rgba(127, 127, 127, 0.25);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"></td><td aria-hidden="true" style="border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"></td></tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">AI2D</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>76.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.5</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>79.9</strong></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">BLINK</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>66.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">37.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>63.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.2</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CountQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>51.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>45.4</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">42.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">CV-Bench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>86.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">40.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>84.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">ERQA</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>45.8</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">27.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>42.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">39.8</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">HallusionBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>72.1</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>67.5</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.3</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>87.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>85.2</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">84.9</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MME</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>85.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">61.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>83.9</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.1</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMMU-Pro</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>26.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">11.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>24.1</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">18.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMRB2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>54.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.3</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>52.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">49.5</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMStar</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>67.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">31.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>61.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">59.9</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">MMVP</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>82.7</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">54.0</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>81.3</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">77.0</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">NaturalBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>81.5</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">58.8</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>80.0</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">79.8</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">POPE</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><u>88.7</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">82.7</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>89.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">88.6</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">V*</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>76.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">35.6</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><strong>76.4</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>73.8</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">VisualPuzzles</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>29.9</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.2</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>29.5</u></td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">VisualWebBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>96.2</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">14.9</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>88.6</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">71.4</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">VL-RewardBench</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em;"><strong>69.3</strong></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">48.1</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;"><u>68.8</u></td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">65.0</td>
</tr>
</tbody>
<tbody style="border: 0;">
<tr style="border: 0;"><td style="border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><strong>Average</strong></td><td style="text-align: center; font-variant-numeric: tabular-nums; background-color: rgba(108, 79, 224, 0.08); border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><strong>70.2</strong></td><td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">42.8</td><td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);"><u>67.7</u></td><td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em; border-top: 1px solid rgba(127, 127, 127, 0.25);">65.4</td></tr>
</tbody>
</table>
</div>

<details>
<summary><small>Evaluation details</small></summary>

<p><small>All four models are scored on the same items with the same scoring, so a few of d1-3B's and d1-omni-600M's numbers differ slightly from their own cards. d1-omni-600M has no Fast Decisions or board score. Average is the unweighted mean of the public benchmarks that all four models have, so it leaves out Fast Decisions and our board. Image benchmarks are read as decisions over each benchmark's options, on at most 1,000 rows each. Three of them are saturated: POPE, MME, and VisualWebBench.</small></p>

</details>

### Speed

Warm calls after `model.compile()` in bf16, median of 20 calls, and best of three runs on the H100 and the M5 Pro. Compiling takes about a minute on the first calls.

<div role="region" tabindex="0" style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;">
<table style="width: 100%; display: table; border: 0; border-radius: 0; border-collapse: collapse; min-width: 40rem; font-size: calc(0.875em - 1pt);">
<thead style="border: 0;">
<tr style="border: 0;">
<th scope="col" style="text-align: left; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Hardware</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">One question</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">3 questions</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">5K-token state</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">384 px picture</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Box</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">Boxes</th>
<th scope="col" style="text-align: center; padding: 0.55em 0.75em; border: 0; border-bottom: 1px solid rgba(127, 127, 127, 0.55);">64 states in one call</th>
</tr>
</thead>
<tbody style="border: 0;">
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">NVIDIA H100 PCIe</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">5.7 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">7.6 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">52 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">12.3 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">16.1 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">24.4 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">1,132 / s</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">AMD MI325X</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">3.8 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">5.6 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">44 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">8.7 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">11.2 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">16.5 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">1,699 / s</td>
</tr>
<tr style="border: 0;">
<td style="border: 0; padding: 0.55em 0.75em;">Apple M5 Pro (<code>mps</code>)</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">18.6 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">26.5 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">753 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">45.2 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">53.5 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">100 ms</td>
<td style="text-align: center; font-variant-numeric: tabular-nums; border: 0; padding: 0.55em 0.75em;">109 / s</td>
</tr>
</tbody>
</table>
</div>

## Citation
<hr style="margin: -0.7em 0 1.2em 0; border: 0; border-top: 1px solid rgba(127, 127, 127, 0.3);" />

```bibtex
@article{liquidAI2026opend1,
  author  = {Liquid AI},
  title   = {Open d1: Edge decision models for text, vision, and audio},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {https://www.liquid.ai/blog/open-d1},
}
```

```bibtex
@article{liquidAI2026LFM3,
  author  = {Liquid AI},
  title   = {Introducing LFM3: Every Modality for Specialized Intelligence},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {https://www.liquid.ai/blog/lfm3},
}
```

For questions and feedback, join [Discord](https://discord.com/invite/liquid-ai). For custom deployment and fine-tuning support, [contact Liquid AI](https://www.liquid.ai/contact).
