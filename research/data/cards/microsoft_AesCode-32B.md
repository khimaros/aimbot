---
license: apache-2.0
base_model:
  - Qwen/Qwen3-VL-32B-Instruct
library_name: transformers
pipeline_tag: image-text-to-text
language:
  - en
tags:
  - code-generation
  - html
  - multimodal
  - reinforcement-learning
  - design
  - arxiv:2610.18860
---

# AesCode-32B

AesCode generates information-rich visual artifacts such as slides, posters, and
dashboards as HTML/CSS. The output remains **structured, editable, and verifiable**, but
the task poses a distinct challenge: code models cannot see how layout, hierarchy, and
color come together on the canvas.

Image generators offer the opposite strength. They compose visually compelling pages but
often misrender text, numbers, and logical relationships. AesCode uses an image generated
from the same prompt as an aesthetic reference while following the prompt for the required
content.

Reference input alone does not solve the problem. Off-the-shelf vision-language models may
copy hallucinated content or ignore the reference layout. AesCode separates semantic
requirements from visual cues through **graph-structured supervision and decoupled
cross-modal rewards**.

AesCode-32B starts from **Qwen3-VL-32B-Instruct** and is trained with cold-start SFT
followed by GDPO across seven reward channels. It is the larger released checkpoint and
leads the aggregate benchmark results.

- 📄 Paper: [arXiv:2610.18860](https://arxiv.org/abs/2610.18860)
- 🤗 Paper page: https://huggingface.co/papers/2610.18860
- 🌐 Project page: https://microsoft.github.io/AesCode/
- 💻 Code: https://github.com/microsoft/AesCode
- 🤗 Companion model: [`microsoft/AesCode-8B`](https://huggingface.co/microsoft/AesCode-8B)

<p align="center">
  <img src="https://huggingface.co/microsoft/AesCode-32B/resolve/main/assets/teaser.png" width="92%" alt="Infographics generated as editable HTML and CSS by AesCode">
</p>

## Intended Use

AesCode is designed to generate information-rich visual artifacts as structured HTML/CSS.
It is suited for creating editable slides, posters, dashboards, and reports, as well as
for research on multimodal code generation and verifiable visual design.

## Results

We evaluate on 300 infographic samples. `Rule` averages the programmatic Text, Bound, and Chart checks. `Visual` averages the Content, Layout, and Style checklist dimensions. `Overall` is the mean of Rule and Visual. Scores are percentages averaged over three generations per prompt with no selection.

`Ref.` indicates whether the model receives an image-generated reference together with the prompt. **Bold** marks the best score in each column and <u>underline</u> the second best.

| Model | Ref. | Text | Bound | Chart | Rule | Content | Layout | Style | Visual | Overall |
|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.5 | No | 88.67 | 86.18 | 82.85 | 85.90 | 79.27 | 68.09 | 52.80 | 66.72 | 76.31 |
| GPT-5.5 | Yes | 89.22 | 86.85 | 81.35 | 85.80 | 82.44 | <u>89.93</u> | **57.91** | 76.76 | 81.28 |
| Claude Opus 4.8 | No | 91.40 | 85.03 | 87.69 | 88.04 | 84.98 | 64.88 | 46.72 | 65.53 | 76.78 |
| Claude Opus 4.8 | Yes | 92.45 | 84.43 | 73.75 | 83.55 | **86.42** | 89.76 | 55.51 | <u>77.23</u> | 80.39 |
| Qwen3-VL-8B | No | 58.32 | 77.23 | 43.30 | 59.61 | 38.33 | 23.97 | 13.22 | 25.17 | 42.39 |
| Qwen3-VL-8B | Yes | 64.07 | 70.99 | 42.35 | 59.14 | 52.90 | 51.33 | 29.92 | 44.72 | 51.93 |
| Qwen3-VL-32B | No | 66.00 | 80.31 | 41.36 | 62.55 | 49.81 | 34.85 | 19.34 | 34.67 | 48.61 |
| Qwen3-VL-32B | Yes | 71.19 | 79.61 | 50.77 | 67.19 | 62.04 | 64.59 | 38.43 | 55.02 | 61.10 |
| **AesCode-8B** | **Yes** | <u>94.06</u> | <u>88.36</u> | <u>87.79</u> | <u>90.07</u> | <u>86.41</u> | 87.80 | 53.21 | 75.80 | <u>82.94</u> |
| **AesCode-32B** | **Yes** | **95.34** | **97.27** | **90.37** | **94.33** | 85.76 | **90.58** | <u>55.99</u> | **77.44** | **85.89** |

AesCode-32B improves Visual over its reference-conditioned Qwen3-VL-32B backbone by
**22.4 points** and Overall by **24.8**. It leads the comparison on Overall at **85.89**
and reaches Rule **94.33**, compared with 85.90 for GPT-5.5 and 88.04 for Claude Opus 4.8.

Two results stand out. Table/Chart at **90.37** leads all models: requiring tables to use
HTML table structures and charts to use ECharts constrains the solution space to
executable, directly verifiable implementations. Boundary at **97.27** reflects a sharp
reduction in canvas overflow: a severe boundary failure recurs on 4.3% of the 300
samples, against 34.7% for GPT-5.5.

Style is the shared ceiling for every system. It awards credit only when a design needs
no further visual revision before delivery, and no model clears 60.

## Usage

The model follows the Qwen3-VL chat interface and requires `transformers>=4.57`. Supply a
detailed content prompt and, when available, a reference image for layout and style
guidance. The weights are bf16; plan for roughly 65 GB of accelerator memory for the
parameters alone.

```python
from transformers import AutoProcessor, AutoModelForImageTextToText

model_id = "microsoft/AesCode-32B"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(
    model_id, dtype="auto", device_map="auto"
)

messages = [{
    "role": "user",
    "content": [
        {"type": "image", "image": "reference.png"},
        {"type": "text", "text": "<your content prompt>"},
    ],
}]

inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt",
).to(model.device)

out = model.generate(
    **inputs, do_sample=True, temperature=0.8, top_p=0.95, max_new_tokens=12000
)
print(processor.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

For batched generation, serve with vLLM and allow two images per prompt:

```bash
vllm serve microsoft/AesCode-32B --tensor-parallel-size 4 \
  --limit-mm-per-prompt image=2 --max-model-len 24576
```

Reported scores use three rollouts per prompt at temperature 0.8, top-p 0.95, up to
12,000 output tokens and a 24,576-token context.

The model emits a complete HTML document. Tables use HTML table structures and charts use
ECharts specifications, keeping both directly inspectable and verifiable.

**The reference image is optional.** Reference-conditioned training internalizes visual
planning into the policy. Measured on AesCode-8B, withholding the reference at inference
costs only **1.00 Visual point**, against 19.55 for the Qwen3-VL-8B-Instruct backbone and
10.04 for GPT-5.5. Quality is still highest when a reference is supplied.

The repository provides the training prompt template and a pipeline that turns a short
idea into the prompt and reference pair the model expects.

## Training

**Cold-start SFT.** 3,000 demonstrations at learning rate 1e-5.

**Reinforcement learning.** GDPO over 7,408 prompts for 520 steps, using verl's
FSDP-vLLM hybrid engine with no critic and no separately trained reward model. AdamW at
a constant 5e-6, no warmup, weight decay 0.01, 128 prompts per step with 8 rollouts
each, KL and entropy coefficients both 0.001, rollout temperature 1.0 and top-p 1.0,
prompt and response each capped at 8,192 tokens. AesCode-8B uses the same recipe and a
shorter 400-step run.

The reward is not a single scalar. Each target is represented as a **design graph**
describing the whole canvas, which makes every property individually attributable. From
that graph come two complementary reward families: deterministic verifiers score the
properties parsable from the code and its rendering, while a VLM judge scores the
non-parsable ones using a sample-specific **Visual Graph Rubric** tied to the graph's
elements and relations. These form seven channels: execution, text, boundary,
tablechart, layout, whitespace, and design. Each is normalized within its rollout group
before aggregation, so a dominant signal cannot drown out a weaker one.

Candidate HTML is scored by rendering it in a sandboxed Playwright browser with external
requests blocked, which exports the DOM, computed styles, bounding boxes, console status
and a screenshot.

Training code, the verifier stack and the Visual Graph Rubric builder are released at
https://github.com/microsoft/AesCode.

## Citation

```bibtex
@article{gao2026aescode,
  title   = {AesCode: Aesthetic Code Generation with Decoupled Cross-Modal Rewards},
  author  = {Gao, Xin and Yang, Yifan and Li, Xin and Wang, Pan and Li, Yan and Tian, Muzhao and Cheng, Mingxi and Liu, Bei and Qiu, Kai and Dai, Qi and Chen, Dong and Dong, Yue and Tassiulas, Leandros and Ying, Rex and Li, Ji and Luo, Chong},
  journal = {arXiv preprint arXiv:2610.18860},
  year    = {2026}
}
```

## License

Released under the Apache 2.0 license, following the Qwen3-VL backbone.
