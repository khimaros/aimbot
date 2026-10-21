---
license: apache-2.0
base_model: Mapika/decider-2b
base_model_relation: quantized
language: [en]
pipeline_tag: text-classification
tags: [gguf, llama.cpp, decision-model, calibrated, structured-output, one-pass]
---

# decider-2b GGUF

GGUF files of [Mapika/decider-2b](https://huggingface.co/Mapika/decider-2b) v12, for llama.cpp. decider-2b
does not generate text. It reads a state and one or more questions, each with an explicit option list, and returns a probability
for every option from one forward pass. See the [decider-2b card](https://huggingface.co/Mapika/decider-2b) for what the model
is, how it was trained, and where it is weak.

**This repository holds the v12 files (2026-10-20).** The v11 files stay available under the Hub tag `v11`. The GGUF files
hold the text model only: image input needs the PyTorch weights of [Mapika/decider-2b](https://huggingface.co/Mapika/decider-2b)
and decider-ai 1.10.0. `decider_config.json` reads yes/no (Noul) answers at temperature 0.05, as the model's own config does (see
its card); `decide_gguf.py` reads every question as Choice, at the Choice temperature.

| file | size | use |
|---|---|---|
| `decider-2b-v12-Q4_K_M.gguf` | 1.3 GB | smallest; 0.3 points lower in-task and 0.4 held-out (table below) |
| `decider-2b-v12-Q8_0.gguf` | 2.0 GB | same quality as the bf16 weights; the recommended file |
| `decider-2b-v12-BF16.gguf` | 3.8 GB | unquantized, for making other quantizations |

The tokenizer, `decider_config.json` (temperatures) and `decide_gguf.py` (the readout on llama.cpp) are in this repository too.

## This is not a chat model

Loading a file in `llama-cli`, `llama-server`, Ollama or LM Studio gives you a text model that continues prompts. That is not how
decider-2b is used, and its generated text is not its answer. The answer is read from the logits of the option-letter tokens at
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

d = Decider("Mapika/decider-2b-GGUF", gguf_file="decider-2b-v12-Q8_0.gguf")
d.decide("My card was charged twice for the same purchase.",
         [{"question": "Which department should handle this?", "options": ["billing", "technical", "sales"]}])
```

`gguf_options=dict(n_gpu_layers=0, n_threads=8)` runs on the CPU. The standalone script below does the same `decide()` readout
with decider-ai 1.5.0.

### Standalone script (`decide_gguf.py`)

```
pip install decider-ai==1.5.0 llama-cpp-python      # llama-cpp-python 0.3.35 or newer
# GPU: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python   (Apple Silicon: -DGGML_METAL=on)
hf download Mapika/decider-2b-GGUF --local-dir decider-2b-gguf \
  --include "*Q4_K_M.gguf" --include "*.json" --include "*.jinja" --include "*.py"
cd decider-2b-gguf
```

```python
from decide_gguf import GGUFDecider

d = GGUFDecider("decider-2b-v12-Q4_K_M.gguf")      # n_gpu_layers=-1 (all on the GPU if the build has one), n_threads=...
d.decide("My card was charged twice for the same purchase.",
         [{"question": "Which department should handle this?", "options": ["billing", "technical", "sales"]},
          {"question": "How urgent is this?", "options": ["low", "medium", "high"]}])
```

`decide_gguf.py` covers `decide()` (choice questions); `system_one` with score and yes/no answers needs decider-ai 1.6.0 (above).
The HTTP server does not serve GGUF files.


## Measured quality

The regression set of the decider-2b card (95 tasks, 144,226 questions, 67 in-task and 28 held-out tasks) at the Choice
temperature 2.465, read through llama.cpp (CUDA build, one prompt per decode) and compared row by row with the bf16 weights in
PyTorch. Accuracy, NLL and ECE are means over tasks.

| | in-task acc / NLL / ECE | held-out acc / NLL / ECE | same answer as bf16 PyTorch |
|---|---|---|---|
| bf16 weights, PyTorch | 0.7906 / 0.5205 / 0.0532 | 0.7478 / 0.6440 / 0.0902 | |
| Q8_0 | 0.7912 / 0.5205 / 0.0530 | 0.7481 / 0.6440 / 0.0915 | 99.22% |
| Q4_K_M | 0.7873 / 0.5304 / 0.0549 | 0.7442 / 0.6522 / 0.0907 | 95.08% |

Q8_0 is equal to the bf16 weights within noise. Q4_K_M is 0.3 points lower in-task and 0.4 held-out. Use Q8_0 unless the smaller file matters. The BF16 GGUF was
not read over this set. Long states (tens of thousands of tokens) move more under Q4_K_M than this table shows (measured on v11).

## Notes

- Score one prompt per `llama_decode`, as `decide_gguf.py` does. With several prompts in one decode (as separate sequences),
  llama.cpp in September 2026 gives probabilities that change with the other prompts in the batch, by up to 0.02 in BF16 and 0.16
  in Q4_K_M on the earlier version of this model. One prompt per decode gives the same numbers on every run.
- CPU and GPU builds give slightly different probabilities on the same file.
- Conversion: llama.cpp `c9064dded` (2026-09-27), `convert_hf_to_gguf.py --no-mtp --outtype bf16`, then `llama-quantize` to
  Q8_0 and Q4_K_M. `--no-mtp` is required: the checkpoint has no multi-token-prediction weights, but its config declares one
  MTP layer, and without the flag the converter writes a file that llama.cpp cannot load.
- The measurements above use the CUDA build. The CPU and Metal builds were not run over the regression set.

License: as decider-2b (see its card for the training sources and their terms); base model Qwen/Qwen3.5-2B-Base.
