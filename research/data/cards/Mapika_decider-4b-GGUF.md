---
license: apache-2.0
base_model: Mapika/decider-4b
base_model_relation: quantized
language: [en]
pipeline_tag: text-classification
tags: [gguf, llama.cpp, decision-model, calibrated, structured-output, one-pass]
---

# decider-4b GGUF

GGUF files of [Mapika/decider-4b](https://huggingface.co/Mapika/decider-4b) v2.1 (Hub main `eb5fbdf`), for llama.cpp. decider-4b
does not generate text. It reads a state and one or more questions, each with an explicit option list, and returns a probability
for every option from one forward pass. See the [decider-4b card](https://huggingface.co/Mapika/decider-4b) for what the model
is, how it was trained, and where it is weak.

| file | size | use |
|---|---|---|
| `decider-4b-v2.1-Q4_K_M.gguf` | 2.7 GB | smallest; about 0.2 points lower in-task accuracy (table below) |
| `decider-4b-v2.1-Q8_0.gguf` | 4.5 GB | same quality as the bf16 weights |
| `decider-4b-v2.1-BF16.gguf` | 8.4 GB | unquantized, for making other quantizations |

The tokenizer, `decider_config.json` (temperatures) and `decide_gguf.py` (the readout on llama.cpp) are in this repository too.

## This is not a chat model

Loading a file in `llama-cli`, `llama-server`, Ollama or LM Studio gives you a text model that continues prompts. That is not how
decider-4b is used, and its generated text is not its answer. The answer is read from the logits of the option-letter tokens at
each answer slot of a prompt built by `decider.prompt`, divided by the fitted temperature. `Decider` (decider-ai 1.6.0) and
`decide_gguf.py` do this with llama-cpp-python.

## Usage

With decider-ai 1.6.0 or newer, `Decider` loads the GGUF file directly: `decide`, `system_one` and the per-type temperatures
of `decider_config.json`, scored by llama.cpp.

```
pip install "decider-ai[gguf]"       # llama-cpp-python; GPU: CMAKE_ARGS="-DGGML_CUDA=on" (Apple Silicon: -DGGML_METAL=on)
```

```python
from decider.infer import Decider

d = Decider("Mapika/decider-4b-GGUF", gguf_file="decider-4b-v2.1-Q4_K_M.gguf")
d.decide("My card was charged twice for the same purchase.",
         [{"question": "Which department should handle this?", "options": ["billing", "technical", "sales"]}])
```

`gguf_options=dict(n_gpu_layers=0, n_threads=8)` runs on the CPU. The standalone script below does the same `decide()` readout
with decider-ai 1.5.0.

### Standalone script (`decide_gguf.py`)

```
pip install decider-ai==1.5.0 llama-cpp-python      # llama-cpp-python 0.3.35 or newer
# GPU: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python   (Apple Silicon: -DGGML_METAL=on)
hf download Mapika/decider-4b-GGUF --local-dir decider-4b-gguf \
  --include "*Q4_K_M.gguf" --include "*.json" --include "*.jinja" --include "*.py"
cd decider-4b-gguf
```

```python
from decide_gguf import GGUFDecider

d = GGUFDecider("decider-4b-v2.1-Q4_K_M.gguf")      # n_gpu_layers=-1 (all on the GPU if the build has one), n_threads=...
d.decide("My card was charged twice for the same purchase.",
         [{"question": "Which department should handle this?", "options": ["billing", "technical", "sales"]},
          {"question": "How urgent is this?", "options": ["low", "medium", "high"]}])
# [{'choice': 'billing', 'confidence': 0.85, 'probs': {...}}, {'choice': 'medium', 'confidence': 0.43, 'probs': {...}}]
```

`decide_gguf.py` covers `decide()` (choice questions); `system_one` with score and yes/no answers needs decider-ai 1.6.0 (above).
The HTTP server does not serve GGUF files.

On 8 CPU threads (server CPU), Q4_K_M takes 0.3 to 0.7 s for a request of 40 to 120 tokens; Q8_0 is about 20% slower.

## Measured quality

The regression set of the decider-4b card (95 tasks, 144,226 questions, 67 in-task and 28 held-out tasks) at the shipped
temperature 1.099, read through llama.cpp (CUDA build, one prompt per decode) and compared row by row with the bf16 weights in
PyTorch. Accuracy, NLL and ECE are means over tasks.

| | in-task acc / NLL / ECE | held-out acc / NLL / ECE | same answer as bf16 PyTorch |
|---|---|---|---|
| bf16 weights, PyTorch | 0.8308 / 0.4145 / 0.0308 | 0.7838 / 0.5703 / 0.0781 | |
| BF16 GGUF | 0.8308 / 0.4145 / 0.0308 | 0.7837 / 0.5700 / 0.0782 | 99.45% |
| Q8_0 | 0.8310 / 0.4145 / 0.0309 | 0.7829 / 0.5699 / 0.0778 | 99.31% |
| Q4_K_M | 0.8288 / 0.4194 / 0.0324 | 0.7834 / 0.5691 / 0.0733 | 97.06% |

The BF16 GGUF differs from PyTorch only on near-ties (median probability difference 0.001). Q8_0 is equal to the bf16 weights
within that noise; its tasks move up on 31 and down on 39, by at most 0.9 points. Q4_K_M is 0.2 points lower on in-task accuracy
with slightly higher NLL; held-out accuracy is unchanged. It is lower than bf16 on 54 tasks and higher on 36; the largest drop is
fin_phrasebank (−3.5 points), then medmcqa and mmlu (−1.3). In Q4_K_M the embedding matrix, which is also the output matrix that
holds the option-letter rows, is stored in Q6_K.

## Notes

- Score one prompt per `llama_decode`, as `decide_gguf.py` does. With several prompts in one decode (as separate sequences),
  llama.cpp in September 2026 gives probabilities that change with the other prompts in the batch, by up to 0.02 in BF16 and 0.16
  in Q4_K_M on this model. One prompt per decode gives the same numbers on every run.
- CPU and GPU builds give slightly different probabilities on the same file (for example 0.846 and 0.830 for "billing" above,
  against 0.844 in PyTorch).
- Conversion: llama.cpp `c9064dded` (2026-09-27), `convert_hf_to_gguf.py --no-mtp --outtype bf16`, then `llama-quantize` to
  Q8_0 and Q4_K_M. `--no-mtp` is required: the checkpoint has no multi-token-prediction weights, but its config declares one
  MTP layer, and without the flag the converter writes a file that llama.cpp cannot load.
- The measurements above use the CUDA build. The CPU and Metal builds were not run over the regression set.

License: Apache-2.0, as decider-4b and its base model Qwen/Qwen3.5-4B-Base.
