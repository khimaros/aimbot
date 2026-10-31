---
quantized_by: bartowski
pipeline_tag: text-generation
base_model: Aleph-Alpha/Kolibri-1-BF16
language:
- de
- en
base_model_relation: quantized
license: apache-2.0
tags:
- reasoning
- moe
---

## Llamacpp imatrix Quantizations of Kolibri-1 by Aleph-Alpha

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11716">b11716</a> for quantization.

Original model: https://huggingface.co/Aleph-Alpha/Kolibri-1-BF16

**Model details:**
- Parameter count: 78B (source checkpoint)
- Input support: text
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|im_start|>system
{system_prompt}

# Reasoning effort

Reasoning effort is set to high. Think carefully through the task in the user's language, validate key assumptions, consider plausible alternatives, and prioritize correctness and clarity.<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
```

<details><summary>Prompt format with tool definitions</summary>

```
<|im_start|>system
{system_prompt}

# Reasoning effort

Reasoning effort is set to high. Think carefully through the task in the user's language, validate key assumptions, consider plausible alternatives, and prioritize correctness and clarity.

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

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_K_M.gguf) (49.76GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [Kolibri-1-bf16.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-bf16) | bf16 | 156.31GB | true | Full BF16 weights. |
| [Kolibri-1-Q8_0.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q8_0) | Q8_0 | 83.14GB | true | Extremely high quality, generally unneeded but max available quant. |
| [Kolibri-1-Q6_K_L.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q6_K_L) | Q6_K_L | 72.53GB | true | The large size of Q6_K, about halfway to Q8_0 in size. Very high quality, near perfect, *recommended*. |
| [Kolibri-1-Q6_K.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q6_K) | Q6_K | 69.00GB | true | Very high quality, near perfect, *recommended*. |
| [Kolibri-1-Q6_K_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q6_K_S) | Q6_K_S | 65.83GB | true | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [Kolibri-1-Q5_K_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q5_K_M) | Q5_K_M | 60.30GB | true | High quality, *recommended*. |
| [Kolibri-1-Q5_K_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/Kolibri-1-Q5_K_S) | Q5_K_S | 55.78GB | true | High quality, *recommended*. |
| [Kolibri-1-Q4_K_L.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_K_L.gguf) | Q4_K_L | 53.51GB | false | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [Kolibri-1-Q4_K_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_K_M.gguf) | Q4_K_M | 49.76GB | false | Good quality, default size for most use cases, *recommended*. |
| [Kolibri-1-IQ4_NL.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ4_NL.gguf) | IQ4_NL | 49.76GB | false | Similar to IQ4_XS, but slightly larger. |
| [Kolibri-1-Q4_1.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_1.gguf) | Q4_1 | 49.24GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [Kolibri-1-Q4_K_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_K_S.gguf) | Q4_K_S | 46.40GB | false | Slightly lower quality with more space savings, *recommended*. |
| [Kolibri-1-Q4_0.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q4_0.gguf) | Q4_0 | 44.61GB | false | Legacy format, kept for compatibility with older tools. |
| [Kolibri-1-IQ4_XS.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ4_XS.gguf) | IQ4_XS | 43.63GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [Kolibri-1-IQ3_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ3_M.gguf) | IQ3_M | 40.68GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [Kolibri-1-Q3_K_L.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q3_K_L.gguf) | Q3_K_L | 39.81GB | false | Lower quality but usable, good for low RAM availability. |
| [Kolibri-1-Q3_K_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q3_K_M.gguf) | Q3_K_M | 37.62GB | false | Low quality. |
| [Kolibri-1-Q3_K_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q3_K_S.gguf) | Q3_K_S | 35.95GB | false | Low quality, *not* recommended. |
| [Kolibri-1-IQ3_XS.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ3_XS.gguf) | IQ3_XS | 35.50GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [Kolibri-1-IQ3_XXS.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ3_XXS.gguf) | IQ3_XXS | 33.65GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [Kolibri-1-Q2_K.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-Q2_K.gguf) | Q2_K | 29.92GB | false | Very low quality but surprisingly usable. |
| [Kolibri-1-IQ2_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ2_M.gguf) | IQ2_M | 28.08GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [Kolibri-1-IQ2_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ2_S.gguf) | IQ2_S | 25.63GB | false | Low quality, uses SOTA techniques to be usable. |
| [Kolibri-1-IQ2_XS.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ2_XS.gguf) | IQ2_XS | 24.34GB | false | Low quality, uses SOTA techniques to be usable. |
| [Kolibri-1-IQ2_XXS.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ2_XXS.gguf) | IQ2_XXS | 22.77GB | false | Very low quality, uses SOTA techniques to be usable. |
| [Kolibri-1-IQ1_M.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ1_M.gguf) | IQ1_M | 19.77GB | false | Extremely low quality, *not* recommended. |
| [Kolibri-1-IQ1_S.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-IQ1_S.gguf) | IQ1_S | 17.61GB | false | Extremely low quality, *not* recommended. |

Download a specific file:

```
hf download bartowski/Kolibri-1-GGUF --include "Kolibri-1-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/Kolibri-1-GGUF --include "Kolibri-1-Q4_K_M.gguf" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/Kolibri-1-GGUF --include "Kolibri-1-Q8_0/*" --local-dir ./
```

You can either specify a new local-dir (Kolibri-1-Q8_0) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/Kolibri-1-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11716 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/Kolibri-1-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.67×, Q3_K_M 0.60× and IQ1_S 0.86× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K_L | 72.53GB | 7.40 | 7.43 | 50 % |
| Q6_K | 69.00GB | 7.04 | 7.07 | 70 % |
| Q6_K_S | 65.83GB | 6.71 | 6.74 | 90 % |
| Q5_K_M | 60.30GB | 6.14 | 6.18 | 70 % |
| Q5_K_S | 55.78GB | 5.67 | 5.71 | 90 % |
| Q4_K_L | 53.51GB | 5.44 | 5.48 | 50 % |
| Q4_K_M | 49.76GB | 5.05 | 5.10 | 70 % |
| IQ4_NL | 49.76GB | 5.05 | 5.10 | 70 % |
| Q4_K_S | 46.40GB | 4.70 | 4.75 | 90 % |
| IQ4_XS | 43.63GB | 4.42 | 4.47 | 90 % |
| IQ3_M | 40.68GB | 4.11 | 4.17 | 50 % |
| Q3_K_L | 39.81GB | 4.02 | 4.08 | 50 % |
| Q3_K_M | 37.62GB | 3.80 | 3.85 | 70 % |
| Q3_K_S | 35.95GB | 3.62 | 3.68 | 90 % |
| IQ3_XS | 35.50GB | 3.58 | 3.64 | 90 % |
| IQ3_XXS | 33.65GB | 3.38 | 3.45 | 70 % |
| Q2_K | 29.92GB | 3.00 | 3.06 | 70 % |
| IQ2_M | 28.08GB | 2.81 | 2.88 | 70 % |
| IQ2_S | 25.63GB | 2.56 | 2.63 | 70 % |
| IQ2_XS | 24.34GB | 2.42 | 2.49 | 90 % |
| IQ2_XXS | 22.77GB | 2.26 | 2.33 | 70 % |
| IQ1_M | 19.77GB | 1.95 | 2.03 | 70 % |
| IQ1_S | 17.61GB | 1.73 | 1.80 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0696 ± 0.0024 | 0.1122 ± 0.0034 | 0.67× | +4.1 % |
| Q3_K_M | 0.0982 ± 0.0030 | 0.1743 ± 0.0043 | 0.60× | +4.6 % |
| IQ1_S | 0.3417 ± 0.0051 | 0.4162 ± 0.0056 | 0.86× | +6.4 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [Kolibri-1-calibration-v6.txt](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-calibration-v6.txt). The imatrix is available here: [Kolibri-1-imatrix.gguf](https://huggingface.co/bartowski/Kolibri-1-GGUF/blob/main/Kolibri-1-imatrix.gguf).

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
  "prose_chunks": 226,
  "tool_chunks": 309,
  "total_chunks": 535,
  "n_conversations": 137,
  "conversation_token_lengths": [
    484,
    1533,
    798,
    1309,
    1011,
    1253,
    2455,
    559,
    1104,
    1117,
    985,
    2015,
    784,
    867,
    2304,
    1134,
    1048,
    909,
    653,
    631,
    1254,
    940,
    1258,
    1125,
    1643,
    1419,
    950,
    613,
    884,
    1408,
    1434,
    731,
    1169,
    961,
    1031,
    1610,
    1521,
    1088,
    396,
    1815,
    1324,
    1007,
    1285,
    1687,
    1857,
    1172,
    1528,
    679,
    2332,
    1014,
    2527,
    677,
    916,
    662,
    949,
    616,
    2145,
    649,
    1055,
    1000,
    1128,
    1091,
    836,
    924,
    862,
    1332,
    822,
    1441,
    1755,
    754,
    365,
    1010,
    2861,
    2725,
    627,
    652,
    930,
    691,
    1204,
    989,
    1027,
    720,
    964,
    942,
    1201,
    1406,
    1282,
    1261,
    748,
    574,
    2362,
    673,
    1066,
    1591,
    1881,
    1114,
    549,
    1249,
    1152,
    1600,
    1561,
    1541,
    731,
    674,
    933,
    2656,
    659,
    506,
    668,
    1165,
    968,
    1278,
    690,
    394,
    359,
    2221,
    635,
    1028,
    1725,
    1596,
    2261,
    2283,
    600,
    891,
    752,
    752,
    1142,
    896,
    766,
    1225,
    748,
    624,
    1316,
    930,
    833,
    1198,
    1356
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
