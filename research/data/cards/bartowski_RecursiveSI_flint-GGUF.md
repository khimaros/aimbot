---
quantized_by: bartowski
pipeline_tag: text-generation
base_model: RecursiveSI/flint
base_model_relation: quantized
license: apache-2.0
---

## Llamacpp imatrix Quantizations of flint by RecursiveSI

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11804">b11804</a> for quantization.

Original model: https://huggingface.co/RecursiveSI/flint

**Model details:**
- Parameter count: 40B (source checkpoint)
- Input support: text
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|system|>{system_prompt}<|user|>{prompt}<|assistant|>
```

<details><summary>Prompt format with tool definitions</summary>

```
<|system|>{system_prompt}<|system|>
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>{"name": "get_stock_price", "description": "Get the current stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string", "description": "The stock symbol, e.g. AAPL, GOOG"}}, "required": ["symbol"]}}</tools>

For each function call, output the function name and arguments within the following XML format:
<tool_call>{function-name}<arg_key>{arg-key-1}</arg_key><arg_value>{arg-value-1}</arg_value>...</tool_call>
<|user|>{prompt}<|assistant|>
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_K_M.gguf) (25.35GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [RecursiveSI_flint-bf16.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/tree/main/RecursiveSI_flint-bf16) | bf16 | 79.63GB | true | Full BF16 weights. |
| [RecursiveSI_flint-Q8_0.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q8_0.gguf) | Q8_0 | 42.35GB | false | Extremely high quality, generally unneeded but max available quant. |
| [RecursiveSI_flint-Q6_K_L.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q6_K_L.gguf) | Q6_K_L | 36.95GB | false | The large size of Q6_K, about halfway to Q8_0 in size. Very high quality, near perfect, *recommended*. |
| [RecursiveSI_flint-Q6_K.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q6_K.gguf) | Q6_K | 35.20GB | false | Very high quality, near perfect, *recommended*. |
| [RecursiveSI_flint-Q6_K_S.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q6_K_S.gguf) | Q6_K_S | 33.57GB | false | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [RecursiveSI_flint-Q5_K_M.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q5_K_M.gguf) | Q5_K_M | 30.81GB | false | High quality, *recommended*. |
| [RecursiveSI_flint-Q5_K_S.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q5_K_S.gguf) | Q5_K_S | 28.60GB | false | High quality, *recommended*. |
| [RecursiveSI_flint-Q4_K_L.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_K_L.gguf) | Q4_K_L | 27.29GB | false | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [RecursiveSI_flint-Q4_K_M.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_K_M.gguf) | Q4_K_M | 25.35GB | false | Good quality, default size for most use cases, *recommended*. |
| [RecursiveSI_flint-IQ4_NL.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ4_NL.gguf) | IQ4_NL | 25.32GB | false | Similar to IQ4_XS, but slightly larger. |
| [RecursiveSI_flint-Q4_1.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_1.gguf) | Q4_1 | 25.18GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [RecursiveSI_flint-Q4_K_S.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_K_S.gguf) | Q4_K_S | 23.83GB | false | Slightly lower quality with more space savings, *recommended*. |
| [RecursiveSI_flint-Q4_0.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q4_0.gguf) | Q4_0 | 22.83GB | false | Legacy format, kept for compatibility with older tools. |
| [RecursiveSI_flint-IQ4_XS.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ4_XS.gguf) | IQ4_XS | 22.45GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [RecursiveSI_flint-IQ3_M.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ3_M.gguf) | IQ3_M | 21.05GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [RecursiveSI_flint-Q3_K_L.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q3_K_L.gguf) | Q3_K_L | 20.59GB | false | Lower quality but usable, good for low RAM availability. |
| [RecursiveSI_flint-Q3_K_M.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q3_K_M.gguf) | Q3_K_M | 19.53GB | false | Low quality. |
| [RecursiveSI_flint-Q3_K_S.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q3_K_S.gguf) | Q3_K_S | 18.44GB | false | Low quality, *not* recommended. |
| [RecursiveSI_flint-IQ3_XS.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ3_XS.gguf) | IQ3_XS | 18.32GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [RecursiveSI_flint-IQ3_XXS.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ3_XXS.gguf) | IQ3_XXS | 17.49GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [RecursiveSI_flint-Q2_K.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-Q2_K.gguf) | Q2_K | 15.48GB | false | Very low quality but surprisingly usable. |
| [RecursiveSI_flint-IQ2_M.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ2_M.gguf) | IQ2_M | 14.88GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [RecursiveSI_flint-IQ2_S.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ2_S.gguf) | IQ2_S | 13.39GB | false | Low quality, uses SOTA techniques to be usable. |
| [RecursiveSI_flint-IQ2_XS.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ2_XS.gguf) | IQ2_XS | 12.74GB | false | Low quality, uses SOTA techniques to be usable. |
| [RecursiveSI_flint-IQ2_XXS.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-IQ2_XXS.gguf) | IQ2_XXS | 12.03GB | false | Very low quality, uses SOTA techniques to be usable. |

Download a specific file:

```
hf download bartowski/RecursiveSI_flint-GGUF --include "RecursiveSI_flint-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/RecursiveSI_flint-GGUF --include "RecursiveSI_flint-Q4_K_M.gguf" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/RecursiveSI_flint-GGUF --include "RecursiveSI_flint-bf16/*" --local-dir ./
```

You can either specify a new local-dir (RecursiveSI_flint-bf16) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/RecursiveSI_flint-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11804 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.87×, Q3_K_M 0.88× and IQ2_XXS 1.01× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K_L | 36.95GB | 7.40 | 7.43 | 50 % |
| Q6_K | 35.20GB | 7.04 | 7.08 | 70 % |
| Q6_K_S | 33.57GB | 6.71 | 6.75 | 91 % |
| Q5_K_M | 30.81GB | 6.14 | 6.20 | 70 % |
| Q5_K_S | 28.60GB | 5.69 | 5.75 | 90 % |
| Q4_K_L | 27.29GB | 5.42 | 5.49 | 50 % |
| Q4_K_M | 25.35GB | 5.03 | 5.10 | 70 % |
| IQ4_NL | 25.32GB | 5.02 | 5.09 | 70 % |
| Q4_K_S | 23.83GB | 4.71 | 4.79 | 90 % |
| IQ4_XS | 22.45GB | 4.43 | 4.51 | 90 % |
| IQ3_M | 21.05GB | 4.15 | 4.23 | 50 % |
| Q3_K_L | 20.59GB | 4.05 | 4.14 | 50 % |
| Q3_K_M | 19.53GB | 3.84 | 3.93 | 70 % |
| Q3_K_S | 18.44GB | 3.61 | 3.71 | 90 % |
| IQ3_XS | 18.32GB | 3.59 | 3.68 | 90 % |
| IQ3_XXS | 17.49GB | 3.42 | 3.52 | 70 % |
| Q2_K | 15.48GB | 3.01 | 3.11 | 70 % |
| IQ2_M | 14.88GB | 2.89 | 2.99 | 70 % |
| IQ2_S | 13.39GB | 2.58 | 2.69 | 70 % |
| IQ2_XS | 12.74GB | 2.45 | 2.56 | 90 % |
| IQ2_XXS | 12.03GB | 2.30 | 2.42 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.1496 ± 0.0042 | 0.1919 ± 0.0046 | 0.87× | +3.8 % |
| Q3_K_M | 0.3019 ± 0.0055 | 0.3913 ± 0.0066 | 0.88× | +5.7 % |
| IQ2_XXS | 0.9915 ± 0.0101 | 1.1292 ± 0.0109 | 1.01× | +8.6 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [RecursiveSI_flint-calibration-v6.txt](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-calibration-v6.txt). The imatrix is available here: [RecursiveSI_flint-imatrix.gguf](https://huggingface.co/bartowski/RecursiveSI_flint-GGUF/blob/main/RecursiveSI_flint-imatrix.gguf).

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
  "prose_chunks": 211,
  "tool_chunks": 290,
  "total_chunks": 501,
  "n_conversations": 137,
  "conversation_token_lengths": [
    403,
    1383,
    983,
    1186,
    872,
    1142,
    2788,
    546,
    986,
    1098,
    836,
    1848,
    709,
    969,
    2422,
    984,
    916,
    802,
    576,
    521,
    1167,
    777,
    1088,
    992,
    1600,
    1281,
    1372,
    663,
    1161,
    1309,
    1264,
    905,
    1011,
    847,
    966,
    1391,
    1349,
    956,
    321,
    1661,
    1111,
    867,
    1131,
    1722,
    1756,
    1046,
    1363,
    619,
    2570,
    877,
    2592,
    569,
    783,
    740,
    820,
    527,
    2094,
    660,
    911,
    868,
    956,
    971,
    687,
    944,
    844,
    1225,
    709,
    1241,
    1843,
    680,
    309,
    897,
    2915,
    2392,
    538,
    688,
    788,
    829,
    1017,
    889,
    890,
    593,
    913,
    816,
    1077,
    1232,
    1097,
    1782,
    652,
    467,
    2392,
    593,
    1092,
    1376,
    1652,
    1010,
    440,
    1124,
    1023,
    1409,
    1516,
    1383,
    618,
    793,
    837,
    2385,
    571,
    487,
    579,
    1079,
    882,
    1209,
    587,
    330,
    289,
    2263,
    777,
    856,
    1437,
    1744,
    2326,
    2316,
    565,
    774,
    671,
    717,
    955,
    779,
    671,
    1087,
    640,
    544,
    1423,
    765,
    735,
    1031,
    1170
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
