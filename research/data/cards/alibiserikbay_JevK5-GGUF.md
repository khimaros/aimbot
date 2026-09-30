---
license: apache-2.0
base_model:
- alibiserikbay/JevK5
- alibiserikbay/JevK5-9B
- alibiserikbay/JevK5-2B
base_model_relation: quantized
language:
- en
library_name: gguf
tags:
- gguf
- llama.cpp
- decision-model
- system-one
- jev
- jev-alternative
- typed-decisions
- jevbench
- calibration
---

# JevK5 GGUF: typed decisions on almost any GPU, or on a CPU

GGUF builds of [JevK5](https://huggingface.co/alibiserikbay/JevK5) (4B),
[JevK5-9B](https://huggingface.co/alibiserikbay/JevK5-9B) and
[JevK5-2B](https://huggingface.co/alibiserikbay/JevK5-2B) for [llama.cpp](https://github.com/ggml-org/llama.cpp),
which runs on NVIDIA, AMD, Intel and Apple GPUs and on plain CPUs.

JevK5 is an Apache-2.0 open alternative to TypeSafe's Jev. It reads a document and a yes/no, choice,
or score question and returns **a probability for every option in one forward pass, with nothing
generated**. It is not affiliated with TypeSafe AI.

## Files

Every file was checked against its unquantized model on JevBench's 231 public decisions, scored
the same way: how often it gives the same answer, and its accuracy per tier. We publish a file only
if at least 95% of its answers match. **Each model has its own temperatures; pass them to the
client as shown under "Run it".**

| File | Model | Size | Same answer as bf16 | Easy | Standard | Hard |
|---|---|---:|---:|---:|---:|---:|
| `jevk5-4b-v0.3-Q8_0.gguf` | JevK5 v0.3 (4B) | 4.48 GB | **229 / 231** | 1.000 | 0.944 | 0.784 |
| `jevk5-4b-v0.3-Q5_K_M.gguf` | JevK5 v0.3 (4B) | 3.07 GB | 224 / 231 | 1.000 | 0.944 | 0.784 |
| `jevk5-4b-v0.3-Q4_K_M.gguf` | JevK5 v0.3 (4B) | 2.71 GB | 221 / 231 | 1.000 | 0.917 | 0.766 |
| `jevk5-9b-v0.3.3-Q8_0.gguf` | JevK5-9B v0.3.3 | 9.53 GB | **229 / 231** | 1.000 | 0.958 | 0.766 |
| `jevk5-9b-v0.3.3-Q5_K_M.gguf` | JevK5-9B v0.3.3 | 6.47 GB | 228 / 231 | 1.000 | 0.958 | 0.757 |
| `jevk5-9b-v0.3-Q8_0.gguf` | JevK5-9B v0.3 | 9.53 GB | **229 / 231** | 1.000 | 0.944 | 0.721 |
| `jevk5-9b-v0.3-Q5_K_M.gguf` | JevK5-9B v0.3 | 6.47 GB | 225 / 231 | 1.000 | 0.944 | 0.703 |
| `jevk5-4b-v0.2-Q8_0.gguf` | JevK5 v0.2 (4B) | 4.48 GB | **228 / 231** | 1.000 | 0.958 | 0.721 |
| `jevk5-4b-v0.2-Q4_K_M.gguf` | JevK5 v0.2 (4B) | 2.71 GB | 219 / 231 | 1.000 | 0.931 | 0.730 |
| `jevk5-2b-v0.2-Q8_0.gguf` | JevK5-2B | 2.01 GB | **226 / 231** | 1.000 | 0.792 | 0.622 |
| *bf16 reference* | JevK5 v0.3 (4B) | 8.4 GB | | 1.000 | 0.944 | 0.784 |
| *bf16 reference* | JevK5-9B v0.3.3 | 17.9 GB | | 1.000 | 0.958 | 0.775 |
| *bf16 reference* | JevK5-9B v0.3 | 17.9 GB | | 1.000 | 0.944 | 0.730 |
| *bf16 reference* | JevK5 v0.2 (4B) | 8.4 GB | | 1.000 | 0.958 | 0.739 |
| *bf16 reference* | JevK5-2B | 3.8 GB | | 1.000 | 0.806 | 0.604 |

- **Q8_0 is effectively lossless.** For every model, the few answers that change are borderline
  items, and hard accuracy moves by two items at most: v0.3 4B unchanged, v0.2 4B two lower, 2B two
  higher. A v0.2 4B Q8_0, built the same way and run on an M1 Pro with Metal, matched 230 / 231.
- **v0.3 4B Q5_K_M and Q4_K_M** both passed. Q5_K_M changes 7 answers, all on the hard tier, with
  the same accuracy; Q4_K_M changes 10 (8 on the hard tier) and is two hard items lower.
- **9B v0.3.3** (1.5 epochs; see JevK5-9B's card): Q8_0 changes 2 answers and Q5_K_M 3, all on the
  hard tier, one and two hard items lower than bf16 (0.766 and 0.757 against 0.775).
- **Not published:** the 9B v0.3.3 Q4_K_M agreed on 222 / 231 but was five hard items lower (0.730).
- **9B v0.3 Q5_K_M** passed at 225 / 231. It changes 6 answers, all on the hard tier, and is three hard
  items lower than bf16 (0.703 against 0.730).
- **Not published:** the 9B v0.3 Q4_K_M changed 13 answers (218 / 231, below 95%).
- **Not published:** the 2B Q4_K_M changed 29 answers and dropped hard accuracy from 0.604 to
  0.514.

Which one to pick:
- the 9B, if a 9.5 GB file fits: `jevk5-9b-v0.3.3-Q8_0` (or `-Q5_K_M`, 6.5 GB) (see JevK5-9B's card for where it is and isn't
  better than the 4B)
- a GPU with 6 GB or more: `jevk5-4b-v0.3-Q8_0`
- less GPU memory: `jevk5-4b-v0.3-Q5_K_M` (3.07 GB) or `jevk5-4b-v0.3-Q4_K_M` (2.71 GB)
- no GPU: `jevk5-2b-v0.2-Q8_0` (fastest), or `jevk5-4b-v0.3-Q8_0` at about 0.6 s per short
  decision

## Run it

JevK5's answer is a probability over the options, read from the next-token log-probabilities of
the answer letters. That needs `llama-server`, which exposes them. Start it with one of the files:

```bash
llama-server --hf-repo alibiserikbay/JevK5-GGUF --hf-file jevk5-4b-v0.3-Q8_0.gguf -c 8192 -ngl 99
```

The simplest client is the JevK5 runtime's `JevK5GGUF` (standard library only). It also answers
questions with more than 16 options. Create it with the file's own temperatures:

| File | Client |
|---|---|
| `jevk5-4b-v0.3-Q8_0.gguf`, `-Q5_K_M`, `-Q4_K_M` | `JevK5GGUF(temperature=1.22, knockout_temperature=0.93)` |
| `jevk5-9b-v0.3.3-Q8_0.gguf`, `-Q5_K_M` | `JevK5GGUF(temperature=1.316, knockout_temperature=1.05)` |
| `jevk5-9b-v0.3-Q8_0.gguf`, `-Q5_K_M` | `JevK5GGUF(temperature=1.049, knockout_temperature=1.2)` |
| `jevk5-4b-v0.2-Q8_0.gguf`, `-Q4_K_M` | `JevK5GGUF(temperature=1.532, knockout_temperature=0.77)` |
| `jevk5-2b-v0.2-Q8_0.gguf` | `JevK5GGUF(temperature=1.42, knockout_temperature=0.77)` |

`temperature` calibrates every pass. `knockout_temperature` only applies to questions with more
than 16 options (it needs jevk5 0.3.0). Without arguments, `JevK5GGUF()` uses v0.2's values.

```bash
pip install --no-deps "jevk5 @ git+https://github.com/allebee/jevk5@v0.3.3"
```

```python
from jevk5 import JevK5GGUF

model = JevK5GGUF(temperature=1.22, knockout_temperature=0.93)   # jevk5-4b-v0.3-*.gguf
model.decide("Order #7120 shows delivered to No. 17; the customer lives at No. 71.",
             {"type": "choice", "instructions": "What happened to the parcel?",
              "criteria": ["delivered", "misdelivered", "unknown"]})
```

Or use this standalone client (Python standard library only, up to 16 options, so only
`temperature` matters):

```python
import json, math, urllib.request

URL = "http://127.0.0.1:8080"  # llama-server
T = 1.22                        # the file's `temperature` (table above)
LETTERS = "ABCDEFGHIJKLMNOP"
SYSTEM = ("Apply the supplied criterion to the supplied evidence. Choose exactly one listed option. "
          "Respond with only its uppercase letter, with no explanation or reasoning.")

def post(path, body):
    req = urllib.request.Request(URL + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def decide(evidence, criterion: str, options: dict) -> dict:
    """options maps an id to its description; returns a calibrated probability per id."""
    ids = list(options)
    user = json.dumps({"evidence": evidence, "criterion": criterion,
                       "options": [{"letter": LETTERS[i], "description": f"{k}: {options[k]}"}
                                   for i, k in enumerate(ids)]}, ensure_ascii=False)
    prompt = (f"<|im_start|>system\n{SYSTEM}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n"
              "<|im_start|>assistant\n<think>\n\n</think>\n\n")
    tokens = post("/tokenize", {"content": prompt, "add_special": False, "parse_special": True})["tokens"]
    top = post("/completion", {"prompt": tokens, "n_predict": 1, "n_probs": 40, "temperature": 0,
                               "cache_prompt": False})["completion_probabilities"][0]["top_logprobs"]
    seen = {t["token"]: t["logprob"] for t in top}
    z = [seen.get(LETTERS[i], min(seen.values()) - 2.0) for i in range(len(ids))]
    w = [math.exp((v - max(z)) / T) for v in z]
    return {k: x / sum(w) for k, x in zip(ids, w)}

decide("I was billed twice for order #4411. Please refund the duplicate charge today.",
       "Which team should handle this?",
       {"billing": "Payments and refunds", "tech": "Bugs", "sales": "New purchases"})
```

- **Yes/no questions:** pass `{"true": ..., "false": ...}` in that order, for example
  `{"true": "The proposition is true.", "false": "The proposition is false."}`.
- **Score questions:** pass the levels in order as `{"0": ..., "1": ..., ...}`.
- The prompt is tokenized with `parse_special` before it is sent, so the chat markers stay single
  tokens. This client gives exactly the same probabilities as the reference implementation used for
  the table above (largest difference 0.0 on yes/no, choice and score items).

We have only tested `llama-server`. Apps built on llama.cpp, such as Ollama or LM Studio, can load
the files, but the calibrated probabilities need an API that returns the answer letters'
log-probabilities for a tokenized prompt; we have not checked whether theirs do.

## Speed

Measured, one decision at a time, over HTTP:

| Hardware | JevK5-2B Q8_0 | JevK5 4B Q8_0 | JevK5-9B Q8_0 |
|---|---:|---:|---:|
| CPU only, 48 threads (server) | ~0.23–0.27 s | ~0.57 s | not measured |
| CPU only, 32 threads, three checks at once (server) | | ~0.6 s (v0.3) | ~0.8 s (v0.3) |
| Apple M1 Pro, Metal | not measured | ~0.6 s | not measured |

Times are for short documents (~170 tokens) and rise with document length: about 0.7–1.0 s (2B)
and 1.8 s (4B) on the CPU for the benchmark's hard items. Consumer NVIDIA, AMD and Intel GPUs have
not been measured yet. For the lowest latency on an NVIDIA GPU, the transformers runtime at
[github.com/allebee/jevk5](https://github.com/allebee/jevk5) uses CUDA graphs (about 13 ms per
decision for the 4B on an H100).

## How the files were made

`convert_hf_to_gguf.py` from llama.cpp commit `9575389` with `--no-mtp` (Qwen3.5 configs otherwise
gain a speculative block); Q5_K_M and Q4_K_M with `llama-quantize` from a bf16 GGUF. No patches.
The v0.3 files were made with the same llama.cpp build as the v0.2 files. All checks ran on
llama.cpp's CPU backend. SHA-256 sums are in `SHA256SUMS`.

## Evaluation and training disclosure

The numbers above are our own runs on JevBench's 231 public items, not official JevBench results.
JevK5 v0.2 (4B) is ranked #3 of 89 on [JevBench](https://github.com/fstandhartinger/jevbench) v1.4.2
(#2 in v1.4); v0.3 (4B), JevK5-9B and JevK5-Lite are submitted there and to the Jev Decision Index,
and JevK5-2B has not been submitted. No JevBench item and no output of Jev was used
for training, tuning or selection. The models' cards describe the training data and its licenses,
the declared overlap with the Jev Decision Index, the known weak spots, and two corrections for
v0.2: echoes of JevBench wording in our hand-written calibration set, and MMLU-Pro test items in
the training data (both in the repository's `CHANGELOG.md`). v0.3 uses no test split of any
dataset.

## Credits

Qwen3.5 by the Qwen team (Apache-2.0). The one-pass readout and prompt come from SemIf by
TheoLeeCJ (MIT). llama.cpp by ggml-org (MIT). Evaluated with JevBench (MIT).
