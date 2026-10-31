---
quantized_by: bartowski
pipeline_tag: text-generation
model_name: K2-Horizon-375B-A23B
tags:
- k2-horizon
- 375b
- moe
- open-weights
- ifm
base_model_relation: quantized
datasets:
- IFM/K2-Horizon-Pretrain-Data
- IFM/K2-Horizon-Midtrain-Data
language:
- en
license: apache-2.0
base_model: IFM/K2-Horizon-375B-A23B
---

## Llamacpp imatrix Quantizations of K2-Horizon-375B-A23B by IFM

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11462">b11462</a> for quantization.

Original model: https://huggingface.co/IFM/K2-Horizon-375B-A23B

**Model details:**
- Parameter count: 379B (source checkpoint)
- Input support: text
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|ifm|begin_of_text|><|ifm|im_start|>system
{system_prompt}<|ifm|im_end|><|ifm|im_start|>user
{prompt}<|ifm|im_end|><|ifm|im_start|>assistant
<ifm|think>
```

<details><summary>Prompt format with tool definitions</summary>

```
<|ifm|begin_of_text|><|ifm|im_start|>system
# Tools
You may call one or more tools to assist with the user query.

Available tools are:

<ifm|tools>
## get_stock_price
Get the current stock price

**Parameters**
- `symbol` *(string, required)* - The stock symbol, e.g. AAPL, GOOG
</ifm|tools>

When calling tools, you MUST follow the tool-call format below:

Wrap all tool calls in a single <ifm|tool_calls></ifm|tool_calls> block. For each call, write the function name at the start of <ifm|tool_call>, followed by paired <ifm|arg_key> and <ifm|arg_value> tags for each argument:

<ifm|tool_calls>
<ifm|tool_call>$FUNCTION_NAME
<ifm|arg_key>$PARAMETER_NAME</ifm|arg_key>
<ifm|arg_value>$PARAMETER_VALUE</ifm|arg_value>
...
</ifm|tool_call>
</ifm|tool_calls>

String and scalar parameters should be written as plain text. Array and object parameters should be written as JSON literals.

{system_prompt}<|ifm|im_end|><|ifm|im_start|>user
{prompt}<|ifm|im_end|><|ifm|im_start|>assistant
<ifm|think>
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q4_K_M) (237.80GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [K2-Horizon-375B-A23B-Q8_0.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q8_0) | Q8_0 | 403.08GB | true | Extremely high quality, generally unneeded but max available quant. |
| [K2-Horizon-375B-A23B-Q6_K.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q6_K) | Q6_K | 334.48GB | true | Very high quality, near perfect, *recommended*. |
| [K2-Horizon-375B-A23B-Q6_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q6_K_S) | Q6_K_S | 319.12GB | true | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [K2-Horizon-375B-A23B-Q5_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q5_K_M) | Q5_K_M | 289.59GB | true | High quality, *recommended*. |
| [K2-Horizon-375B-A23B-Q5_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q5_K_S) | Q5_K_S | 269.72GB | true | High quality, *recommended*. |
| [K2-Horizon-375B-A23B-Q4_1.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q4_1) | Q4_1 | 238.62GB | true | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [K2-Horizon-375B-A23B-IQ4_NL.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ4_NL) | IQ4_NL | 237.85GB | true | Similar to IQ4_XS, but slightly larger. |
| [K2-Horizon-375B-A23B-Q4_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q4_K_M) | Q4_K_M | 237.80GB | true | Good quality, default size for most use cases, *recommended*. |
| [K2-Horizon-375B-A23B-Q4_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q4_K_S) | Q4_K_S | 224.01GB | true | Slightly lower quality with more space savings, *recommended*. |
| [K2-Horizon-375B-A23B-Q4_0.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q4_0) | Q4_0 | 216.15GB | true | Legacy format, kept for compatibility with older tools. |
| [K2-Horizon-375B-A23B-IQ4_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ4_XS) | IQ4_XS | 209.33GB | true | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [K2-Horizon-375B-A23B-IQ3_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ3_M) | IQ3_M | 196.08GB | true | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [K2-Horizon-375B-A23B-Q3_K_L.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q3_K_L) | Q3_K_L | 192.35GB | true | Lower quality but usable, good for low RAM availability. |
| [K2-Horizon-375B-A23B-Q3_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q3_K_M) | Q3_K_M | 182.54GB | true | Low quality. |
| [K2-Horizon-375B-A23B-Q3_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q3_K_S) | Q3_K_S | 173.06GB | true | Low quality, *not* recommended. |
| [K2-Horizon-375B-A23B-IQ3_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ3_XS) | IQ3_XS | 172.09GB | true | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [K2-Horizon-375B-A23B-IQ3_XXS.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ3_XXS) | IQ3_XXS | 161.94GB | true | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [K2-Horizon-375B-A23B-Q2_K.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-Q2_K) | Q2_K | 146.25GB | true | Very low quality but surprisingly usable. |
| [K2-Horizon-375B-A23B-IQ2_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ2_M) | IQ2_M | 138.01GB | true | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [K2-Horizon-375B-A23B-IQ2_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ2_S) | IQ2_S | 124.03GB | true | Low quality, uses SOTA techniques to be usable. |
| [K2-Horizon-375B-A23B-IQ2_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ2_XS) | IQ2_XS | 116.94GB | true | Low quality, uses SOTA techniques to be usable. |
| [K2-Horizon-375B-A23B-IQ2_XXS.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ2_XXS) | IQ2_XXS | 111.00GB | true | Very low quality, uses SOTA techniques to be usable. |
| [K2-Horizon-375B-A23B-IQ1_M.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ1_M) | IQ1_M | 94.72GB | true | Extremely low quality, *not* recommended. |
| [K2-Horizon-375B-A23B-IQ1_S.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/K2-Horizon-375B-A23B-IQ1_S) | IQ1_S | 84.96GB | true | Extremely low quality, *not* recommended. |

Download a specific file:

```
hf download bartowski/K2-Horizon-375B-A23B-GGUF --include "K2-Horizon-375B-A23B-Q4_K_M/*" --local-dir ./
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
hf download bartowski/K2-Horizon-375B-A23B-GGUF --include "K2-Horizon-375B-A23B-Q4_K_M/*" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/K2-Horizon-375B-A23B-GGUF --include "K2-Horizon-375B-A23B-Q8_0/*" --local-dir ./
```

You can either specify a new local-dir (K2-Horizon-375B-A23B-Q8_0) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/K2-Horizon-375B-A23B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11462 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.47×, Q3_K_M 0.50× and IQ1_S 0.88× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K | 334.48GB | 7.04 | 7.06 | 70 % |
| Q6_K_S | 319.12GB | 6.71 | 6.73 | 90 % |
| Q5_K_M | 289.59GB | 6.08 | 6.11 | 70 % |
| Q5_K_S | 269.72GB | 5.66 | 5.69 | 90 % |
| IQ4_NL | 237.85GB | 4.99 | 5.02 | 70 % |
| Q4_K_M | 237.80GB | 4.98 | 5.02 | 70 % |
| Q4_K_S | 224.01GB | 4.69 | 4.73 | 90 % |
| IQ4_XS | 209.33GB | 4.38 | 4.42 | 90 % |
| IQ3_M | 196.08GB | 4.10 | 4.14 | 50 % |
| Q3_K_L | 192.35GB | 4.02 | 4.06 | 50 % |
| Q3_K_M | 182.54GB | 3.81 | 3.85 | 70 % |
| Q3_K_S | 173.06GB | 3.61 | 3.65 | 90 % |
| IQ3_XS | 172.09GB | 3.59 | 3.63 | 90 % |
| IQ3_XXS | 161.94GB | 3.37 | 3.42 | 70 % |
| Q2_K | 146.25GB | 3.04 | 3.09 | 70 % |
| IQ2_M | 138.01GB | 2.86 | 2.91 | 70 % |
| IQ2_S | 124.03GB | 2.56 | 2.62 | 70 % |
| IQ2_XS | 116.94GB | 2.41 | 2.47 | 90 % |
| IQ2_XXS | 111.00GB | 2.29 | 2.34 | 70 % |
| IQ1_M | 94.72GB | 1.94 | 2.00 | 70 % |
| IQ1_S | 84.96GB | 1.73 | 1.79 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0295 ± 0.0007 | 0.0665 ± 0.0012 | 0.47× | +2.7 % |
| Q3_K_M | 0.0482 ± 0.0007 | 0.1023 ± 0.0015 | 0.50× | +4.9 % |
| IQ1_S | 0.2075 ± 0.0019 | 0.2489 ± 0.0024 | 0.88× | +6.7 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [K2-Horizon-375B-A23B-calibration-v6.txt](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/blob/main/K2-Horizon-375B-A23B-calibration-v6.txt). The imatrix is available here: [K2-Horizon-375B-A23B-imatrix.gguf](https://huggingface.co/bartowski/K2-Horizon-375B-A23B-GGUF/blob/main/K2-Horizon-375B-A23B-imatrix.gguf).

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
  "prose_chunks": 207,
  "tool_chunks": 290,
  "total_chunks": 497,
  "n_conversations": 137,
  "conversation_token_lengths": [
    428,
    1343,
    998,
    1117,
    873,
    1181,
    2744,
    596,
    965,
    1073,
    761,
    1748,
    734,
    992,
    2371,
    998,
    905,
    795,
    615,
    563,
    1183,
    804,
    1042,
    1000,
    1516,
    1246,
    1403,
    731,
    1222,
    1240,
    1208,
    944,
    1026,
    837,
    974,
    1290,
    1371,
    972,
    366,
    1635,
    1136,
    875,
    1051,
    1638,
    1612,
    1084,
    1325,
    642,
    2509,
    924,
    2571,
    605,
    788,
    784,
    837,
    557,
    2096,
    679,
    910,
    774,
    987,
    972,
    713,
    977,
    902,
    1165,
    735,
    1168,
    1762,
    728,
    316,
    834,
    2964,
    2387,
    563,
    717,
    819,
    873,
    1019,
    939,
    896,
    623,
    961,
    829,
    1037,
    1274,
    1087,
    1833,
    672,
    496,
    2337,
    618,
    1074,
    1337,
    1607,
    1044,
    472,
    1156,
    1050,
    1239,
    1511,
    1320,
    626,
    848,
    850,
    2282,
    608,
    526,
    617,
    1104,
    940,
    1235,
    591,
    346,
    308,
    2208,
    839,
    871,
    1423,
    1675,
    2273,
    2263,
    606,
    764,
    674,
    741,
    963,
    792,
    702,
    1067,
    634,
    550,
    1430,
    739,
    704,
    1071,
    1198
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
