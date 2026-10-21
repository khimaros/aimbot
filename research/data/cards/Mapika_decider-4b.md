---
license: apache-2.0
base_model: Qwen/Qwen3.5-4B-Base
language: [en]
pipeline_tag: text-classification
tags: [decision-model, calibrated, structured-output, multi-task, system-one, one-pass, vision]
---

# decider-4b: typed decisions with calibrated probabilities in one forward pass, 4B dense, text and images

A language model that does not generate text. It reads a state and one or more typed questions, each with an explicit option
list, and returns a probability distribution over the options for every question from one forward pass. It is called from
software, not chatted with. From v3 the state may include images.

**This repository holds v3 (2026-10-20).** v2.1 stays available under the Hub tag `v2.1`, with its own card; v2 and v1 under
`v2` and `v1`.

- **Weights:** the text model at the repository root (Qwen3.5-4B-Base architecture, bf16, 8.4 GB), loaded as before by
  `decider.infer.Decider`, `decider.serve` and the GGUF builds. `vision/` holds the image part: the vision tower of
  Qwen3.5-4B-Base (unchanged, 0.6 GB) and the config of the image-text model. The image path reuses the text model's weights.
- **Code:** [decider-ai](https://github.com/Mapika/decider) 1.10.0 for images; text works with 1.4.0 and later.

## Changes from v2.1

| | v2.1 | v3 |
|---|---|---|
| Decision Index 0.3, 4,500-request sample | 41.55 | **51.02** |
| Image questions, mean of 11 sets | 0.840 (v2.1 + base vision tower) | **0.891** |
| Visual7W / VSR (never trained on) | 0.857 / 0.813 | 0.873 / 0.833 |
| JevBench public items, hard tier | 0.649 | 0.640 |
| JevBench public items, standard tier | 0.986 | 0.986 |
| Fresh held-out yes/no set, scored the JevBench way | −1.9 | **44.3** |

- **Decision Index:** +9.5 on the sample, from the decider-31b training mixture (train splits of benchmarks the index also tests;
  see Training).
- **Images:** new. The gain over the plain base vision tower is mostly on the kinds of image questions trained.
- **JevBench public items:** level (one hard item fewer).
- **Yes/no answers:** the config now uses temperature 0.05 for Noul answers, so they come out near 0 or 1. JevBench counts a yes/no
  probability between 0.2 and 0.8 as wrong; at 0.05 almost none fall there, and our 399-item held-out yes/no set scores 44.3
  instead of −0.3 at the fitted temperature. The cost: the yes/no probabilities are no longer calibrated (ECE 0.265 instead of
  0.102 on that set). For calibrated yes/no probabilities use `temperature_by_type={"choice": 2.098, "noul": 2.795, "score":
  3.152}` (the fitted values).

## The decider family

| model | base | use it for |
|---|---|---|
| [decider-2b](https://huggingface.co/Mapika/decider-2b) v12 | Qwen3.5-2B-Base | the fastest: routing, classification, judgments; text and images |
| **decider-4b** v3 | Qwen3.5-4B-Base | the middle point; text and images |
| [decider-12b](https://huggingface.co/Mapika/decider-12b) v2 | Gemma-4-12B-it | our JevBench model; text |
| [decider-12b-vision](https://huggingface.co/Mapika/decider-12b-vision) | Gemma-4-12B-it | the Decision Index task mix and images; calibrated yes/no |
| [decider-31b](https://huggingface.co/Mapika/decider-31b) v2 | Gemma-4-31B-it, NVFP4 | the strongest; text and images; Blackwell GPU, vLLM |
| [decider-35b-a3b](https://huggingface.co/Mapika/decider-35b-a3b) | Qwen3.5-35B-A3B-Base | text |

All share one interface (`POST /v1/systemone` in TypeSafe's format) and one readout. Code and changelog:
https://github.com/Mapika/decider.

## Usage

Text, as before:

```python
from decider.infer import Decider
d = Decider("Mapika/decider-4b")
d.decide("My card was charged twice for the same purchase.",
         [{"question": "Which department should handle this?", "options": ["billing", "technical support", "sales"]},
          {"question": "Does this need a refund action?", "options": ["no", "yes"]}])
```

Images, through the server (decider-ai 1.10.0; the config's `"images": true` turns image input on):

```bash
pip install "decider-ai>=1.10.0" pillow
DECIDER_MODEL=Mapika/decider-4b uvicorn decider.serve:app --host 127.0.0.1 --port 8000
```

```python
import base64, httpx
img = base64.b64encode(open("chart.png", "rb").read()).decode()
r = httpx.post("http://127.0.0.1:8000/v1/systemone", timeout=60, json={
    "state": {"chart": "q3-chart", "note": "Escalate if any region fell by more than 10%."},
    "assets": {"q3-chart": {"type": "image", "format": "png", "data_base64": img}},
    "questions": {"escalate": {"type": "noul", "instructions": "Does the `chart` call for escalation?",
                               "criteria": {"true": "escalate", "false": "no escalation"}}}})
```

The asset's key is the reference; each place the state names it becomes "the image" in the prompt, and the image goes in front
of the prompt, as in training. PNG and JPEG; up to 4 images (`DECIDER_MAX_IMAGES`); references in question text and box
answers are not supported. Image rows are read one at a time, without batching or CUDA graphs. Requirements as before (`torch`,
`transformers>=5`, `flash-linear-attention`), plus `pillow` for images.

## Training

v3 starts from v2.1. Its text weights were placed into the Qwen3.5-4B-Base image-text model (vision tower from the base); the
language-model weights are identical to the text model's. Then a LoRA stage (rank 64, learning rate 1e-4, 2 epochs, 110 minutes
on one B300) on the language model only:

- **Text, 39.5k rows:** the decider-31b training mixture (train splits of CLINC150, iSarcasmEval, VAST, ACOS, POP909-CL, GSM8K
  and NLI4CT, decontaminated against every Decision Index 0.3 suite row; generated smart-home requests; generated
  state-tracking decisions and decision families; document questions written by Qwen3.6-27B; labelled public rows), plus 6.7k
  rows replayed from v2.1's training data.
- **Images, 18,129 rows:** train splits of seven the_cauldron subsets: AI2D, A-OKVQA, Hateful Memes, IconQA, RAVEN, ScienceQA,
  TQA. Visual7W and VSR were not used.
- Not used: Decision Index test rows, JevBench or ImageJevBench items.

Temperatures were fitted on our own validation rows: Choice 2.098, Score 3.152, Noul 2.795 (the config uses 0.05 for Noul, see
above). They are about twice v2.1's because v3's raw answers are sharper.

## Evaluation

All numbers measured by us; none were verified by the benchmark maintainers.

- **Decision Index 0.3,** 4,500-request sample of the public suite: 51.02 (v2.1 41.55); through `decider.serve` 1.10.0, 50.85.
  Benchmark-weighted ECE on the sample: 0.160 (v2.1 0.150); with about 88 requests per benchmark this number is inflated for
  every model. The full public suite was not run.
- **Image questions,** eval splits of 11 the_cauldron sets, 300 items each: mean 0.891; trained kinds 0.902, never-trained
  (Visual7W, VSR) 0.853. v2.1 with the base vision tower and no image training: 0.841 / 0.835. Stock Qwen3.5-4B with our
  readout: 0.827 mean. Through `decider.serve` 1.10.0 with the image sent as an asset: VSR 0.837, Visual7W 0.873.
- **JevBench public items** (read once, never used for training, fitting or selection): easy 1.000, standard 0.986, hard 0.640.

## Limitations

- **One pass only:** knowledge stays at the base model's level; multi-step tasks are not solved by reading harder.
- **Yes/no calibration** is traded for JevBench's rule in the default config (see Changes).
- **Images:** new image question types read about as well as the stock model. Not measured on ImageJevBench.
- **Latency** was not measured again; the text path is unchanged from v2.1.

## License

The weights are released under Apache 2.0, as the base model. Training sources and their terms:

- Image questions, from the train splits of [the_cauldron](https://huggingface.co/datasets/HuggingFaceM4/the_cauldron) subsets
  (the_cauldron licenses only its own prompts, CC BY 4.0; each source keeps its own terms):
  - AI2D (Kembhavi et al., 2016): CC BY-SA 4.0.
  - A-OKVQA (Schwenk et al., 2022): Apache 2.0 (repository); images from COCO.
  - IconQA (Lu et al., 2021): CC BY-NC-SA 4.0, non-commercial.
  - ScienceQA (Lu et al., 2022): CC BY-NC-SA 4.0, non-commercial research use.
  - TQA (Kembhavi et al., 2017): CC BY-NC 3.0, non-commercial.
  - RAVEN (Zhang et al., 2019): no data licence stated (the code is GPL-3.0).
  - Hateful Memes (Kiela et al., 2020): Facebook's Hateful Memes dataset licence. It permits use of the data to research and
    develop models designed to detect manipulated media, and states that models derived from it may be used for academic and
    commercial purposes. This is a research project; check the licence for your own use.

- CLINC150: CC BY 3.0 (Larson et al., 2019). Credit: "An Evaluation Dataset for Intent Classification and Out-of-Scope
  Prediction", clinc/oos-eval.
- iSarcasmEval: MIT (Abu Farha et al., 2022). The texts are tweets.
- POP909-CL: MIT; built on POP909 (Wang et al., 2020), MIT.
- VAST (Allaway and McKeown, 2020) and ACOS (Cai et al., 2021): no licence stated by the authors.
- GSM8K (Cobbe et al., 2021): MIT.
- NLI4CT (SemEval-2024 Task 2, Jullien et al.): no licence file in the task repository; released for the shared task.
- RACE: non-commercial research use. It is a small part of the replayed data (250 rows).
- ARC, SNLI, LogiQA 2.0 (copy dependent): CC BY-SA 4.0; BoolQ: CC BY-SA 3.0; BANKING77, MedQA: CC BY 4.0; MMLU,
  CommonsenseQA: MIT; MNLI: mixed per genre.
- The sources of v2.1 and earlier, listed on the v2.1 card (Hub tag `v2.1`).
