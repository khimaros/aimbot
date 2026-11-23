---
quantized_by: bartowski
pipeline_tag: text-generation
base_model: inclusionAI/Ling-3.1-flash-1019
base_model_relation: quantized
license: mit
---

## Llamacpp imatrix Quantizations of Ling-3.1-flash-1019 by inclusionAI

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11913">b11913</a> for quantization.

Original model: https://huggingface.co/inclusionAI/Ling-3.1-flash-1019

**Model details:**
- Parameter count: 572B (source checkpoint)
- Input support: text
- Speculative decoding: yes (MTP) - [details](#mtp)
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<role>SYSTEM</role>{system_prompt}
detailed thinking on<|role_end|><role>HUMAN</role>{prompt}<|role_end|><role>ASSISTANT</role>
<think>
```

<details><summary>Prompt format with tool definitions</summary>

```
<role>SYSTEM</role>{system_prompt}
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "get_stock_price", "description": "Get the current stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string", "description": "The stock symbol, e.g. AAPL, GOOG"}}, "required": ["symbol"]}}}
</tools>

If none of the functions can be used, point it out. If the given question lacks the parameters required by the function, also point it out.
If you need to use a function, for each function call, output the function name and arguments within the following XML format:
<tool_call>{function-name}
<arg_key>{arg-key-1}</arg_key>
<arg_value>{arg-value-1}</arg_value>
<arg_key>{arg-key-2}</arg_key>
<arg_value>{arg-value-2}</arg_value>
...
</tool_call>
detailed thinking on<|role_end|><role>HUMAN</role>{prompt}<|role_end|><role>ASSISTANT</role>
<think>
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q4_K_M) (357.97GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [Ling-3.1-flash-1019-Q8_0.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q8_0) | Q8_0 | 608.38GB | true | Extremely high quality, generally unneeded but max available quant. |
| [Ling-3.1-flash-1019-Q6_K.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q6_K) | Q6_K | 501.58GB | true | Very high quality, near perfect, *recommended*. |
| [Ling-3.1-flash-1019-Q6_K_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q6_K_S) | Q6_K_S | 478.83GB | true | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [Ling-3.1-flash-1019-Q5_K_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q5_K_M) | Q5_K_M | 436.32GB | true | High quality, *recommended*. |
| [Ling-3.1-flash-1019-Q5_K_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q5_K_S) | Q5_K_S | 406.06GB | true | High quality, *recommended*. |
| [Ling-3.1-flash-1019-Q4_1.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q4_1) | Q4_1 | 360.12GB | true | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [Ling-3.1-flash-1019-IQ4_NL.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ4_NL) | IQ4_NL | 358.01GB | true | Similar to IQ4_XS, but slightly larger. |
| [Ling-3.1-flash-1019-Q4_K_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q4_K_M) | Q4_K_M | 357.97GB | true | Good quality, default size for most use cases, *recommended*. |
| [Ling-3.1-flash-1019-Q4_K_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q4_K_S) | Q4_K_S | 336.63GB | true | Slightly lower quality with more space savings, *recommended*. |
| [Ling-3.1-flash-1019-Q4_0.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q4_0) | Q4_0 | 326.64GB | true | Legacy format, kept for compatibility with older tools. |
| [Ling-3.1-flash-1019-IQ4_XS.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ4_XS) | IQ4_XS | 317.08GB | true | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [Ling-3.1-flash-1019-IQ3_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ3_M) | IQ3_M | 297.30GB | true | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [Ling-3.1-flash-1019-Q3_K_L.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q3_K_L) | Q3_K_L | 288.00GB | true | Lower quality but usable, good for low RAM availability. |
| [Ling-3.1-flash-1019-Q3_K_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q3_K_M) | Q3_K_M | 275.06GB | true | Low quality. |
| [Ling-3.1-flash-1019-Q3_K_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q3_K_S) | Q3_K_S | 261.57GB | true | Low quality, *not* recommended. |
| [Ling-3.1-flash-1019-IQ3_XS.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ3_XS) | IQ3_XS | 260.39GB | true | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [Ling-3.1-flash-1019-IQ3_XXS.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ3_XXS) | IQ3_XXS | 247.37GB | true | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [Ling-3.1-flash-1019-Q2_K.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-Q2_K) | Q2_K | 219.17GB | true | Very low quality but surprisingly usable. |
| [Ling-3.1-flash-1019-IQ2_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ2_M) | IQ2_M | 213.03GB | true | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [Ling-3.1-flash-1019-IQ2_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ2_S) | IQ2_S | 188.47GB | true | Low quality, uses SOTA techniques to be usable. |
| [Ling-3.1-flash-1019-IQ2_XS.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ2_XS) | IQ2_XS | 177.38GB | true | Low quality, uses SOTA techniques to be usable. |
| [Ling-3.1-flash-1019-IQ2_XXS.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ2_XXS) | IQ2_XXS | 170.79GB | true | Very low quality, uses SOTA techniques to be usable. |
| [Ling-3.1-flash-1019-IQ1_M.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ1_M) | IQ1_M | 145.09GB | true | Extremely low quality, *not* recommended. |
| [Ling-3.1-flash-1019-IQ1_S.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/Ling-3.1-flash-1019-IQ1_S) | IQ1_S | 131.01GB | true | Extremely low quality, *not* recommended. |

Download a specific file:

```
hf download bartowski/Ling-3.1-flash-1019-GGUF --include "Ling-3.1-flash-1019-Q4_K_M/*" --local-dir ./
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
hf download bartowski/Ling-3.1-flash-1019-GGUF --include "Ling-3.1-flash-1019-Q4_K_M/*" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/Ling-3.1-flash-1019-GGUF --include "Ling-3.1-flash-1019-Q8_0/*" --local-dir ./
```

You can either specify a new local-dir (Ling-3.1-flash-1019-Q8_0) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/Ling-3.1-flash-1019-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11913 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## MTP

This model has MTP (Multi-Token Prediction) layers, and they are included in these quants

MTP layers act as a built-in draft model, letting llama.cpp run speculative decoding for faster generation. To use them, add the following flag to your llama.cpp command:

```
--spec-type draft-mtp
```

Note: the MTP layers are stored at Q4_0 in every quant except Q8_0. Imatrix calibration does not exercise them, so the imatrix has nothing to offer these layers, and Q4_0 is chosen for its speed, which massively benefits MTP performance.

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on [bartowski/Ling-3.1-flash-GGUF](https://huggingface.co/bartowski/Ling-3.1-flash-GGUF) (same architecture and tensor shapes) before any of these files were released: Q4_K_M reached 0.93×, Q3_K_M 0.95× and IQ1_S 1.01× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K | 501.58GB | 7.04 | 7.01 | 70 % |
| Q6_K_S | 478.83GB | 6.71 | 6.70 | 90 % |
| Q5_K_M | 436.32GB | 6.11 | 6.10 | 70 % |
| Q5_K_S | 406.06GB | 5.68 | 5.68 | 90 % |
| IQ4_NL | 358.01GB | 5.00 | 5.01 | 70 % |
| Q4_K_M | 357.97GB | 5.00 | 5.01 | 70 % |
| Q4_K_S | 336.63GB | 4.69 | 4.71 | 90 % |
| IQ4_XS | 317.08GB | 4.42 | 4.43 | 90 % |
| IQ3_M | 297.30GB | 4.13 | 4.16 | 50 % |
| Q3_K_L | 288.00GB | 4.00 | 4.03 | 50 % |
| Q3_K_M | 275.06GB | 3.82 | 3.85 | 70 % |
| Q3_K_S | 261.57GB | 3.62 | 3.66 | 90 % |
| IQ3_XS | 260.39GB | 3.61 | 3.64 | 90 % |
| IQ3_XXS | 247.37GB | 3.42 | 3.46 | 70 % |
| Q2_K | 219.17GB | 3.02 | 3.06 | 70 % |
| IQ2_M | 213.03GB | 2.94 | 2.98 | 70 % |
| IQ2_S | 188.47GB | 2.59 | 2.64 | 70 % |
| IQ2_XS | 177.38GB | 2.43 | 2.48 | 90 % |
| IQ2_XXS | 170.79GB | 2.33 | 2.39 | 70 % |
| IQ1_M | 145.09GB | 1.97 | 2.03 | 70 % |
| IQ1_S | 131.01GB | 1.77 | 1.83 | 70 % |

Checked on [bartowski/Ling-3.1-flash-GGUF](https://huggingface.co/bartowski/Ling-3.1-flash-GGUF), which shares this model's architecture and tensor shapes: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0249 ± 0.0005 | 0.0300 ± 0.0006 | 0.93× | +2.7 % |
| Q3_K_M | 0.0694 ± 0.0012 | 0.0841 ± 0.0014 | 0.95× | +4.4 % |
| IQ1_S | 0.7909 ± 0.0080 | 0.9214 ± 0.0088 | 1.01× | +8.1 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [Ling-3.1-flash-1019-calibration-v6.txt](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/blob/main/Ling-3.1-flash-1019-calibration-v6.txt). The imatrix is available here: [Ling-3.1-flash-1019-imatrix.gguf](https://huggingface.co/bartowski/Ling-3.1-flash-1019-GGUF/blob/main/Ling-3.1-flash-1019-imatrix.gguf).

<details>
<summary>Calibration render details</summary>

```json
{
  "recipe": "calibration-v6",
  "encoder": "chat_template",
  "library_versions": {
    "transformers": "4.57.6",
    "tokenizers": "0.22.2",
    "tiktoken": "0.14.0",
    "blobfile": "3.3.0",
    "huggingface_hub": "0.36.2"
  },
  "chunk_size": 512,
  "prose_chunks": 220,
  "tool_chunks": 345,
  "total_chunks": 565,
  "n_conversations": 137,
  "conversation_token_lengths": [
    523,
    1594,
    1193,
    1476,
    1046,
    1300,
    3127,
    754,
    1163,
    1353,
    1019,
    2059,
    836,
    1200,
    2755,
    1189,
    1099,
    948,
    694,
    677,
    1326,
    990,
    1308,
    1167,
    1839,
    1463,
    1601,
    844,
    1376,
    1604,
    1472,
    1161,
    1211,
    1003,
    1019,
    1650,
    1619,
    1147,
    433,
    1912,
    1392,
    1048,
    1355,
    1973,
    2023,
    1230,
    1569,
    824,
    2903,
    1063,
    2811,
    723,
    955,
    915,
    924,
    655,
    2396,
    840,
    1100,
    1045,
    1166,
    1133,
    868,
    1151,
    1114,
    1530,
    873,
    1483,
    2099,
    803,
    333,
    1071,
    3285,
    2856,
    671,
    865,
    974,
    1022,
    1244,
    1052,
    1074,
    753,
    1152,
    983,
    1244,
    1468,
    1321,
    2041,
    795,
    608,
    2714,
    658,
    1345,
    1626,
    1936,
    1168,
    581,
    1336,
    1136,
    1653,
    1759,
    1625,
    782,
    961,
    976,
    2730,
    697,
    679,
    709,
    1354,
    1011,
    1544,
    731,
    361,
    327,
    2569,
    947,
    1085,
    1815,
    1970,
    2651,
    2644,
    759,
    931,
    797,
    884,
    1190,
    944,
    809,
    1266,
    793,
    668,
    1711,
    965,
    880,
    1240,
    1409
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
