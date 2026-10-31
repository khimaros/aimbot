---
quantized_by: bartowski
pipeline_tag: text-generation
base_model_relation: quantized
language:
- en
license: apache-2.0
base_model: JetBrains/Mellum2.1-12B-A2.5B-Thinking
model-index:
- name: Mellum2.1 Thinking
  results:
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: LiveCodeBench v6
      type: livecodebench
    metrics:
    - type: pass@1
      value: 82.0
      name: pass@1
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: HumanEval+
      type: humaneval-plus
    metrics:
    - type: pass@1
      value: 91.5
      name: pass@1
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MBPP+
      type: mbpp-plus
    metrics:
    - type: pass@1
      value: 79.4
      name: pass@1
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: AIME 25/26
      type: aime
    metrics:
    - type: exact_match
      value: 83.3
      name: exact match
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: GSM-Plus
      type: gsm-plus
    metrics:
    - type: exact_match
      value: 88.3
      name: exact match
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: SWE-bench Verified
      type: swe-bench-verified
    metrics:
    - type: resolved
      value: 47.0
      name: resolved rate
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: Terminal-Bench 2.1
      type: terminal-bench
    metrics:
    - type: resolved
      value: 17.4
      name: resolved rate
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: SWE-bench Pro
      type: swe-bench-pro
    metrics:
    - type: resolved
      value: 28.0
      name: resolved rate
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: BFCL v4
      type: bfcl
    metrics:
    - type: acc
      value: 62.3
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: WorkBench
      type: workbench
    metrics:
    - type: task_completion
      value: 44.6
      name: task completion
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: ToolHop
      type: toolhop
    metrics:
    - type: acc
      value: 49.1
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: IFEval
      type: ifeval
    metrics:
    - type: acc
      value: 90.6
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: GPQA Diamond
      type: gpqa
    metrics:
    - type: acc
      value: 64.6
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MMLU-Redux
      type: mmlu-redux
    metrics:
    - type: acc
      value: 87.8
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MixEval-Hard
      type: mixeval
    metrics:
    - type: acc
      value: 46.4
      name: accuracy
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: XSTest
      type: xstest
    metrics:
    - type: safe_compliance
      value: 88.8
      name: safe compliance
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: HarmBench (harmful rate, lower is better)
      type: harmbench
    metrics:
    - type: harmful_rate
      value: 8.5
      name: harmful rate
      verified: false
---

## Llamacpp imatrix Quantizations of Mellum2.1-12B-A2.5B-Thinking by JetBrains

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11490">b11490</a> for quantization.

Original model: https://huggingface.co/JetBrains/Mellum2.1-12B-A2.5B-Thinking

**Model details:**
- Parameter count: 12B (source checkpoint)
- Input support: text
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
```

<details><summary>Prompt format with tool definitions</summary>

```
<|im_start|>system
{system_prompt}

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "get_stock_price", "description": "Get the current stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string", "description": "The stock symbol, e.g. AAPL, GOOG"}}, "required": ["symbol"]}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call><|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf) (8.82GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [Mellum2.1-12B-A2.5B-Thinking-bf16.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-bf16.gguf) | bf16 | 24.31GB | false | Full BF16 weights. |
| [Mellum2.1-12B-A2.5B-Thinking-Q8_0.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q8_0.gguf) | Q8_0 | 12.93GB | false | Extremely high quality, generally unneeded but max available quant. |
| [Mellum2.1-12B-A2.5B-Thinking-Q6_K_L.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q6_K_L.gguf) | Q6_K_L | 11.81GB | false | The large size of Q6_K, about halfway to Q8_0 in size. Very high quality, near perfect, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf) | Q6_K | 11.45GB | false | Very high quality, near perfect, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q6_K_S.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q6_K_S.gguf) | Q6_K_S | 11.13GB | false | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q5_K_M.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q5_K_M.gguf) | Q5_K_M | 9.97GB | false | High quality, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q4_K_L.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_K_L.gguf) | Q4_K_L | 9.23GB | false | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q5_K_S.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q5_K_S.gguf) | Q5_K_S | 8.96GB | false | High quality, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf) | Q4_K_M | 8.82GB | false | Good quality, default size for most use cases, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q4_K_S.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_K_S.gguf) | Q4_K_S | 7.86GB | false | Slightly lower quality with more space savings, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q4_1.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_1.gguf) | Q4_1 | 7.71GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ4_NL.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ4_NL.gguf) | IQ4_NL | 7.66GB | false | Similar to IQ4_XS, but slightly larger. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ3_M.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ3_M.gguf) | IQ3_M | 7.24GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [Mellum2.1-12B-A2.5B-Thinking-Q3_K_L.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q3_K_L.gguf) | Q3_K_L | 7.13GB | false | Lower quality but usable, good for low RAM availability. |
| [Mellum2.1-12B-A2.5B-Thinking-Q4_0.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q4_0.gguf) | Q4_0 | 7.00GB | false | Legacy format, kept for compatibility with older tools. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ4_XS.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ4_XS.gguf) | IQ4_XS | 6.97GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [Mellum2.1-12B-A2.5B-Thinking-Q3_K_M.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q3_K_M.gguf) | Q3_K_M | 6.70GB | false | Low quality. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ3_XS.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ3_XS.gguf) | IQ3_XS | 6.29GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ3_XXS.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ3_XXS.gguf) | IQ3_XXS | 6.28GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [Mellum2.1-12B-A2.5B-Thinking-Q3_K_S.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q3_K_S.gguf) | Q3_K_S | 6.05GB | false | Low quality, *not* recommended. |
| [Mellum2.1-12B-A2.5B-Thinking-Q2_K.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-Q2_K.gguf) | Q2_K | 5.53GB | false | Very low quality but surprisingly usable. |
| [Mellum2.1-12B-A2.5B-Thinking-IQ2_M.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-IQ2_M.gguf) | IQ2_M | 5.40GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |

Download a specific file:

```
hf download bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF --include "Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf" --local-dir ./
```

## Downloading using the Hugging Face CLI

<details>
  <summary>Click to view download instructions</summary>

First, make sure you have the Hugging Face CLI installed:

```
pip install -U "huggingface_hub[cli]"
```

Download a specific file:

```
hf download bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF --include "Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf" --local-dir ./
```

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11490 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.91×, Q3_K_M 0.92× and IQ2_M 1.09× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K_L | 11.81GB | 7.38 | 7.77 | 51 % |
| Q6_K | 11.45GB | 7.03 | 7.54 | 71 % |
| Q6_K_S | 11.13GB | 6.71 | 7.33 | 91 % |
| Q5_K_M | 9.97GB | 6.12 | 6.56 | 71 % |
| Q4_K_L | 9.23GB | 5.49 | 6.07 | 50 % |
| Q5_K_S | 8.96GB | 5.69 | 5.90 | 90 % |
| Q4_K_M | 8.82GB | 5.08 | 5.81 | 70 % |
| Q4_K_S | 7.86GB | 4.70 | 5.18 | 90 % |
| IQ4_NL | 7.66GB | 5.08 | 5.05 | 70 % |
| IQ3_M | 7.24GB | 4.32 | 4.77 | 50 % |
| Q3_K_L | 7.13GB | 4.20 | 4.69 | 50 % |
| IQ4_XS | 6.97GB | 4.39 | 4.59 | 90 % |
| Q3_K_M | 6.70GB | 3.98 | 4.41 | 70 % |
| IQ3_XS | 6.29GB | 3.57 | 4.14 | 90 % |
| IQ3_XXS | 6.28GB | 3.47 | 4.14 | 70 % |
| Q3_K_S | 6.05GB | 3.56 | 3.99 | 90 % |
| Q2_K | 5.53GB | 3.04 | 3.64 | 70 % |
| IQ2_M | 5.40GB | 2.90 | 3.56 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0321 ± 0.0004 | 0.0509 ± 0.0006 | 0.91× | +8.0 % |
| Q3_K_M | 0.1059 ± 0.0013 | 0.1537 ± 0.0017 | 0.92× | +8.5 % |
| IQ2_M | 0.2690 ± 0.0028 | 0.2983 ± 0.0031 | 1.09× | +6.0 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [Mellum2.1-12B-A2.5B-Thinking-calibration-v6.txt](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-calibration-v6.txt). The imatrix is available here: [Mellum2.1-12B-A2.5B-Thinking-imatrix.gguf](https://huggingface.co/bartowski/Mellum2.1-12B-A2.5B-Thinking-GGUF/blob/main/Mellum2.1-12B-A2.5B-Thinking-imatrix.gguf).

<details>
<summary>Calibration render details</summary>

```json
{
  "recipe": "calibration-v6",
  "encoder": "chat_template",
  "library_versions": {
    "transformers": "5.9.0",
    "tokenizers": "0.22.2",
    "tiktoken": "0.14.0",
    "blobfile": "3.3.0",
    "huggingface_hub": "1.31.0"
  },
  "chunk_size": 512,
  "prose_chunks": 239,
  "tool_chunks": 314,
  "total_chunks": 553,
  "n_conversations": 137,
  "conversation_token_lengths": [
    476,
    1553,
    814,
    1340,
    1021,
    1293,
    2525,
    558,
    1140,
    1116,
    989,
    1994,
    788,
    896,
    2367,
    1143,
    1041,
    901,
    644,
    629,
    1283,
    933,
    1341,
    1127,
    1651,
    1483,
    959,
    606,
    894,
    1434,
    1484,
    739,
    1187,
    963,
    1042,
    1659,
    1557,
    1106,
    378,
    1865,
    1359,
    1036,
    1298,
    1717,
    1910,
    1196,
    1539,
    668,
    2401,
    1026,
    2562,
    689,
    913,
    653,
    937,
    619,
    2191,
    640,
    1044,
    998,
    1147,
    1098,
    844,
    927,
    869,
    1334,
    834,
    1469,
    1785,
    771,
    326,
    1035,
    3024,
    2841,
    635,
    641,
    929,
    692,
    1212,
    1003,
    1046,
    711,
    979,
    970,
    1206,
    1428,
    1319,
    1314,
    738,
    559,
    2426,
    666,
    1066,
    1598,
    1950,
    1117,
    533,
    1310,
    1140,
    1625,
    1594,
    1587,
    735,
    673,
    941,
    2745,
    657,
    491,
    669,
    1166,
    970,
    1285,
    675,
    355,
    330,
    2276,
    620,
    1057,
    1751,
    1606,
    2317,
    2344,
    591,
    887,
    746,
    759,
    1147,
    919,
    766,
    1252,
    740,
    635,
    1345,
    929,
    825,
    1226,
    1379
  ]
}
```

</details>

## ARM/AVX information

llama.cpp automatically "repacks" weights into an interleaved layout at load time for faster inference on ARM and AVX machines - details in [this PR](https://github.com/ggml-org/llama.cpp/pull/9921). This once required downloading special Q4_0_4_4/4_8/8_8 files; those are long gone. Online repacking now covers Q4_0, IQ4_NL, and most K-quants, so no special quant choice is needed for CPU inference.

## Which file should I choose?

<details>
  <summary>Click here for details</summary>

An older (early 2024) but still useful write-up with charts comparing quant performances is provided by Artefact2 [here](https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9)

The first thing to figure out is how big a model you can run. To do this, you'll need to figure out how much RAM and/or VRAM you have.

If you want your model running as FAST as possible, you'll want to fit the whole thing on your GPU's VRAM. Aim for a quant with a file size 1-2GB smaller than your GPU's total VRAM.

If you want the absolute maximum quality, add both your system RAM and your GPU's VRAM together, then similarly grab a quant with a file size 1-2GB Smaller than that total.

Hugging Face can also do this math for you: add your hardware in your [Local Apps settings](https://huggingface.co/settings/local-apps) and the model page will show which files fit.

Next, you'll need to decide if you want to use an 'I-quant' or a 'K-quant'.

If you don't want to think too much, grab one of the K-quants. These are in format 'QX_K_X', like Q5_K_M.

If you want to get more into the weeds, you can check out this extremely useful feature chart:

[llama.cpp feature matrix](https://github.com/ggml-org/llama.cpp/wiki/Feature-matrix)

But basically, if you're aiming for below Q4, and you're running cuBLAS (Nvidia) or rocBLAS (AMD), you should look towards the I-quants. These are in format IQX_X, like IQ3_M. These are newer and offer better performance for their size.

These I-quants can also be used on CPU, but will be slower than their K-quant equivalent, so speed vs performance is a tradeoff you'll have to decide.

</details>

## Credits

Thank you kalomaze and Dampf for assistance in creating the imatrix calibration dataset.

Want to support my work? Visit my ko-fi page here: https://ko-fi.com/bartowski
