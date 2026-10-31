---
quantized_by: bartowski
pipeline_tag: text-generation
language:
- en
tags:
- mixture-of-experts
- reasoning
- code
- tool-use
base_model_relation: quantized
license: apache-2.0
base_model: reflection/Beam-1.0-501B-A23B
---

## Llamacpp imatrix Quantizations of Beam-1.0-501B-A23B by reflection

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11804">b11804</a> for quantization.

Original model: https://huggingface.co/reflection/Beam-1.0-501B-A23B

**Model details:**
- Parameter count: 501B (source checkpoint)
- Input support: text
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|start|>system<|message|>You are Beam, an AI assistant trained by Reflection.

Reasoning effort: 512

# Valid channels: analysis, final. Channel must be included for every message.<|end|><|start|>developer<|message|># Instructions

{system_prompt}<|end|><|start|>user<|message|>{prompt}<|end|><|start|>assistant
```

<details><summary>Prompt format with tool definitions</summary>

```
<|start|>system<|message|>You are Beam, an AI assistant trained by Reflection.

Reasoning effort: 512

# Valid channels: analysis, final. Channel must be included for every message.<|end|><|start|>developer<|message|># Instructions

{system_prompt}

# Tools

// Get the current stock price
type get_stock_price = (_: {
// The stock symbol, e.g. AAPL, GOOG
symbol: string,
}) => any;<|end|><|start|>user<|message|>{prompt}<|end|><|start|>assistant
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q4_K_M) (314.53GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [Beam-1.0-501B-A23B-Q8_0.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q8_0) | Q8_0 | 532.79GB | true | Extremely high quality, generally unneeded but max available quant. |
| [Beam-1.0-501B-A23B-Q6_K.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q6_K) | Q6_K | 441.78GB | true | Very high quality, near perfect, *recommended*. |
| [Beam-1.0-501B-A23B-Q6_K_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q6_K_S) | Q6_K_S | 420.65GB | true | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [Beam-1.0-501B-A23B-Q5_K_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q5_K_M) | Q5_K_M | 380.78GB | true | High quality, *recommended*. |
| [Beam-1.0-501B-A23B-Q5_K_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q5_K_S) | Q5_K_S | 355.09GB | true | High quality, *recommended*. |
| [Beam-1.0-501B-A23B-Q4_K_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q4_K_M) | Q4_K_M | 314.53GB | true | Good quality, default size for most use cases, *recommended*. |
| [Beam-1.0-501B-A23B-Q4_1.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q4_1) | Q4_1 | 314.07GB | true | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [Beam-1.0-501B-A23B-IQ4_NL.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ4_NL) | IQ4_NL | 311.91GB | true | Similar to IQ4_XS, but slightly larger. |
| [Beam-1.0-501B-A23B-Q4_K_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q4_K_S) | Q4_K_S | 293.38GB | true | Slightly lower quality with more space savings, *recommended*. |
| [Beam-1.0-501B-A23B-Q4_0.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q4_0) | Q4_0 | 284.16GB | true | Legacy format, kept for compatibility with older tools. |
| [Beam-1.0-501B-A23B-IQ4_XS.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ4_XS) | IQ4_XS | 273.06GB | true | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [Beam-1.0-501B-A23B-IQ3_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ3_M) | IQ3_M | 255.66GB | true | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [Beam-1.0-501B-A23B-Q3_K_L.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q3_K_L) | Q3_K_L | 249.52GB | true | Lower quality but usable, good for low RAM availability. |
| [Beam-1.0-501B-A23B-Q3_K_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q3_K_M) | Q3_K_M | 236.62GB | true | Low quality. |
| [Beam-1.0-501B-A23B-Q3_K_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q3_K_S) | Q3_K_S | 225.88GB | true | Low quality, *not* recommended. |
| [Beam-1.0-501B-A23B-IQ3_XS.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ3_XS) | IQ3_XS | 224.54GB | true | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [Beam-1.0-501B-A23B-IQ3_XXS.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ3_XXS) | IQ3_XXS | 211.10GB | true | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [Beam-1.0-501B-A23B-Q2_K.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-Q2_K) | Q2_K | 190.66GB | true | Very low quality but surprisingly usable. |
| [Beam-1.0-501B-A23B-IQ2_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ2_M) | IQ2_M | 178.49GB | true | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [Beam-1.0-501B-A23B-IQ2_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ2_S) | IQ2_S | 161.27GB | true | Low quality, uses SOTA techniques to be usable. |
| [Beam-1.0-501B-A23B-IQ2_XS.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ2_XS) | IQ2_XS | 151.72GB | true | Low quality, uses SOTA techniques to be usable. |
| [Beam-1.0-501B-A23B-IQ2_XXS.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ2_XXS) | IQ2_XXS | 145.28GB | true | Very low quality, uses SOTA techniques to be usable. |
| [Beam-1.0-501B-A23B-IQ1_M.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ1_M) | IQ1_M | 123.56GB | true | Extremely low quality, *not* recommended. |
| [Beam-1.0-501B-A23B-IQ1_S.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/Beam-1.0-501B-A23B-IQ1_S) | IQ1_S | 109.59GB | true | Extremely low quality, *not* recommended. |

Download a specific file:

```
hf download bartowski/Beam-1.0-501B-A23B-GGUF --include "Beam-1.0-501B-A23B-Q4_K_M/*" --local-dir ./
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
hf download bartowski/Beam-1.0-501B-A23B-GGUF --include "Beam-1.0-501B-A23B-Q4_K_M/*" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/Beam-1.0-501B-A23B-GGUF --include "Beam-1.0-501B-A23B-Q8_0/*" --local-dir ./
```

You can either specify a new local-dir (Beam-1.0-501B-A23B-Q8_0) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/Beam-1.0-501B-A23B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11804 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.98×, Q3_K_M 0.94× and IQ1_S 1.03× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K | 441.78GB | 7.04 | 7.05 | 70 % |
| Q6_K_S | 420.65GB | 6.70 | 6.71 | 91 % |
| Q5_K_M | 380.78GB | 6.07 | 6.08 | 70 % |
| Q5_K_S | 355.09GB | 5.66 | 5.67 | 90 % |
| Q4_K_M | 314.53GB | 5.00 | 5.02 | 70 % |
| IQ4_NL | 311.91GB | 4.96 | 4.98 | 70 % |
| Q4_K_S | 293.38GB | 4.67 | 4.68 | 90 % |
| IQ4_XS | 273.06GB | 4.34 | 4.36 | 90 % |
| IQ3_M | 255.66GB | 4.06 | 4.08 | 50 % |
| Q3_K_L | 249.52GB | 3.96 | 3.98 | 50 % |
| Q3_K_M | 236.62GB | 3.76 | 3.78 | 70 % |
| Q3_K_S | 225.88GB | 3.59 | 3.60 | 90 % |
| IQ3_XS | 224.54GB | 3.56 | 3.58 | 90 % |
| IQ3_XXS | 211.10GB | 3.35 | 3.37 | 70 % |
| Q2_K | 190.66GB | 3.02 | 3.04 | 70 % |
| IQ2_M | 178.49GB | 2.83 | 2.85 | 70 % |
| IQ2_S | 161.27GB | 2.55 | 2.57 | 70 % |
| IQ2_XS | 151.72GB | 2.40 | 2.42 | 90 % |
| IQ2_XXS | 145.28GB | 2.29 | 2.32 | 70 % |
| IQ1_M | 123.56GB | 1.95 | 1.97 | 70 % |
| IQ1_S | 109.59GB | 1.72 | 1.75 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0250 ± 0.0005 | 0.0294 ± 0.0006 | 0.98× | +3.2 % |
| Q3_K_M | 0.0747 ± 0.0014 | 0.0904 ± 0.0016 | 0.94× | +3.8 % |
| IQ1_S | 0.6917 ± 0.0078 | 0.7719 ± 0.0083 | 1.03× | +8.0 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [Beam-1.0-501B-A23B-calibration-v6.txt](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/blob/main/Beam-1.0-501B-A23B-calibration-v6.txt). The imatrix is available here: [Beam-1.0-501B-A23B-imatrix.gguf](https://huggingface.co/bartowski/Beam-1.0-501B-A23B-GGUF/blob/main/Beam-1.0-501B-A23B-imatrix.gguf).

<details>
<summary>Calibration render details</summary>

```json
{
  "recipe": "calibration-v6",
  "encoder": "chat_template",
  "library_versions": {
    "transformers": "5.20.2",
    "tokenizers": "0.23.3",
    "tiktoken": "0.14.0",
    "blobfile": "3.3.0",
    "huggingface_hub": "1.31.0"
  },
  "chunk_size": 512,
  "prose_chunks": 218,
  "tool_chunks": 279,
  "total_chunks": 497,
  "n_conversations": 137,
  "conversation_token_lengths": [
    352,
    1276,
    943,
    1120,
    804,
    1106,
    2706,
    578,
    876,
    1099,
    682,
    1641,
    662,
    958,
    2327,
    909,
    808,
    702,
    532,
    518,
    1106,
    743,
    976,
    932,
    1442,
    1193,
    1364,
    692,
    1151,
    1247,
    1163,
    946,
    957,
    756,
    1056,
    1296,
    1396,
    928,
    288,
    1612,
    1170,
    804,
    966,
    1565,
    1670,
    1030,
    1285,
    606,
    2480,
    897,
    2565,
    538,
    707,
    728,
    940,
    485,
    2205,
    612,
    868,
    654,
    931,
    888,
    641,
    938,
    957,
    1256,
    663,
    1101,
    1690,
    648,
    363,
    732,
    3115,
    2434,
    482,
    651,
    777,
    818,
    963,
    891,
    860,
    568,
    944,
    735,
    946,
    1204,
    1036,
    1803,
    587,
    425,
    2296,
    671,
    1104,
    1313,
    1596,
    959,
    404,
    1120,
    1161,
    1125,
    1549,
    1194,
    557,
    804,
    773,
    2297,
    531,
    478,
    531,
    1139,
    852,
    1305,
    491,
    391,
    359,
    2159,
    789,
    845,
    1521,
    1640,
    2229,
    2219,
    559,
    688,
    574,
    659,
    924,
    698,
    631,
    977,
    561,
    467,
    1498,
    699,
    595,
    1027,
    1175
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
