---
quantized_by: bartowski
pipeline_tag: image-text-to-text
language:
- en
- ar
- zh
- fr
- de
- it
- ja
- ko
- pt
- es
- vi
- th
- id
- hi
- ru
- pl
base_model: LiquidAI/LFM3-VL-2B
license: other
license_link: LICENSE
tags:
- liquid
- lfm3
- edge
- conversational
- custom_code
base_model_relation: quantized
license_name: lfm1.0
---

## Llamacpp imatrix Quantizations of LFM3-VL-2B by LiquidAI

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11969">b11969</a> for quantization.

Original model: https://huggingface.co/LiquidAI/LFM3-VL-2B

**Model details:**
- Parameter count: 2B (source checkpoint)
- Input support: text, image (with mmproj file) - [details](#multimodal)
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|startoftext|><|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
<think>
```

<details><summary>Prompt format with tool definitions</summary>

```
<|startoftext|><|im_start|>system
{system_prompt}

<tools>
{"name": "get_stock_price", "description": "Get the current stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string", "description": "The stock symbol, e.g. AAPL, GOOG"}}, "required": ["symbol"]}}
</tools><|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
<think>
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_K_M.gguf) (1.12GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [LFM3-VL-2B-bf16.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-bf16.gguf) | bf16 | 3.47GB | false | Full BF16 weights. |
| [LFM3-VL-2B-Q8_0.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q8_0.gguf) | Q8_0 | 1.85GB | false | Extremely high quality, generally unneeded but max available quant. |
| [LFM3-VL-2B-Q6_K_L.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q6_K_L.gguf) | Q6_K_L | 1.58GB | false | The large size of Q6_K, about halfway to Q8_0 in size. Very high quality, near perfect, *recommended*. |
| [LFM3-VL-2B-Q6_K.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q6_K.gguf) | Q6_K | 1.52GB | false | Very high quality, near perfect, *recommended*. |
| [LFM3-VL-2B-Q6_K_S.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q6_K_S.gguf) | Q6_K_S | 1.46GB | false | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [LFM3-VL-2B-Q5_K_M.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q5_K_M.gguf) | Q5_K_M | 1.35GB | false | High quality, *recommended*. |
| [LFM3-VL-2B-Q5_K_S.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q5_K_S.gguf) | Q5_K_S | 1.27GB | false | High quality, *recommended*. |
| [LFM3-VL-2B-Q4_K_L.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_K_L.gguf) | Q4_K_L | 1.19GB | false | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [LFM3-VL-2B-Q4_1.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_1.gguf) | Q4_1 | 1.15GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [LFM3-VL-2B-Q4_K_M.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_K_M.gguf) | Q4_K_M | 1.12GB | false | Good quality, default size for most use cases, *recommended*. |
| [LFM3-VL-2B-IQ4_NL.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ4_NL.gguf) | IQ4_NL | 1.12GB | false | Similar to IQ4_XS, but slightly larger. |
| [LFM3-VL-2B-Q4_0.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_0.gguf) | Q4_0 | 1.06GB | false | Legacy format, kept for compatibility with older tools. |
| [LFM3-VL-2B-Q4_K_S.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q4_K_S.gguf) | Q4_K_S | 1.05GB | false | Slightly lower quality with more space savings, *recommended*. |
| [LFM3-VL-2B-IQ4_XS.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ4_XS.gguf) | IQ4_XS | 1.00GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [LFM3-VL-2B-IQ3_M.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ3_M.gguf) | IQ3_M | 0.93GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [LFM3-VL-2B-Q3_K_L.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q3_K_L.gguf) | Q3_K_L | 0.89GB | false | Lower quality but usable, good for low RAM availability. |
| [LFM3-VL-2B-Q3_K_M.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q3_K_M.gguf) | Q3_K_M | 0.85GB | false | Low quality. |
| [LFM3-VL-2B-IQ3_XS.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ3_XS.gguf) | IQ3_XS | 0.81GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [LFM3-VL-2B-Q3_K_S.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q3_K_S.gguf) | Q3_K_S | 0.81GB | false | Low quality, *not* recommended. |
| [LFM3-VL-2B-IQ3_XXS.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ3_XXS.gguf) | IQ3_XXS | 0.78GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [LFM3-VL-2B-Q2_K.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-Q2_K.gguf) | Q2_K | 0.70GB | false | Very low quality but surprisingly usable. |
| [LFM3-VL-2B-IQ2_M.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-IQ2_M.gguf) | IQ2_M | 0.65GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |

Download a specific file:

```
hf download bartowski/LFM3-VL-2B-GGUF --include "LFM3-VL-2B-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/LFM3-VL-2B-GGUF --include "LFM3-VL-2B-Q4_K_M.gguf" --local-dir ./
```

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/LFM3-VL-2B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11969 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Multimodal

This model supports image input. Alongside the quants, this repo includes the multimodal projector files [mmproj-LFM3-VL-2B-bf16.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/mmproj-LFM3-VL-2B-bf16.gguf) and [mmproj-LFM3-VL-2B-f16.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/mmproj-LFM3-VL-2B-f16.gguf), which pair with any quant above.

llama.cpp downloads the mmproj automatically when using `-hf` as shown above; if you're loading files manually, pass it with `--mmproj`.

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-3bf8b43e20a68f0b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on [bartowski/LFM3-1.7B-GGUF](https://huggingface.co/bartowski/LFM3-1.7B-GGUF) (same architecture and tensor shapes) before any of these files were released: Q4_K_M reached 0.84×, Q3_K_M 0.63× and IQ2_M 0.76× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K_L | 1.58GB | 7.40 | 7.32 | 50 % |
| Q6_K | 1.52GB | 7.04 | 7.02 | 70 % |
| Q6_K_S | 1.46GB | 6.71 | 6.74 | 90 % |
| Q5_K_M | 1.35GB | 6.15 | 6.26 | 70 % |
| Q5_K_S | 1.27GB | 5.69 | 5.87 | 90 % |
| Q4_K_L | 1.19GB | 5.45 | 5.51 | 50 % |
| Q4_K_M | 1.12GB | 5.04 | 5.16 | 70 % |
| IQ4_NL | 1.12GB | 5.04 | 5.16 | 70 % |
| Q4_K_S | 1.05GB | 4.71 | 4.88 | 90 % |
| IQ4_XS | 1.00GB | 4.40 | 4.62 | 90 % |
| IQ3_M | 0.93GB | 4.18 | 4.28 | 50 % |
| Q3_K_L | 0.89GB | 3.98 | 4.11 | 50 % |
| Q3_K_M | 0.85GB | 3.76 | 3.92 | 70 % |
| IQ3_XS | 0.81GB | 3.57 | 3.76 | 90 % |
| Q3_K_S | 0.81GB | 3.56 | 3.76 | 90 % |
| IQ3_XXS | 0.78GB | 3.40 | 3.61 | 70 % |
| Q2_K | 0.70GB | 2.96 | 3.25 | 70 % |
| IQ2_M | 0.65GB | 2.88 | 3.02 | 70 % |

Checked on [bartowski/LFM3-1.7B-GGUF](https://huggingface.co/bartowski/LFM3-1.7B-GGUF), which shares this model's architecture and tensor shapes: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0767 ± 0.0011 | 0.0926 ± 0.0012 | 0.84× | equal |
| Q3_K_M | 0.2226 ± 0.0020 | 0.2641 ± 0.0024 | 0.63× | −8.2 % |
| IQ2_M | 0.5807 ± 0.0041 | 0.6121 ± 0.0042 | 0.76× | −8.0 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [LFM3-VL-2B-calibration-v6.txt](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-calibration-v6.txt). The imatrix is available here: [LFM3-VL-2B-imatrix.gguf](https://huggingface.co/bartowski/LFM3-VL-2B-GGUF/blob/main/LFM3-VL-2B-imatrix.gguf).

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
  "prose_chunks": 216,
  "tool_chunks": 270,
  "total_chunks": 486,
  "n_conversations": 137,
  "conversation_token_lengths": [
    350,
    1366,
    650,
    1086,
    866,
    1141,
    2307,
    387,
    975,
    926,
    793,
    1805,
    665,
    733,
    2157,
    996,
    895,
    783,
    538,
    468,
    1155,
    786,
    1087,
    984,
    1485,
    1250,
    816,
    480,
    756,
    1184,
    1281,
    549,
    1011,
    807,
    1046,
    1411,
    1364,
    938,
    275,
    1654,
    1077,
    859,
    1133,
    1539,
    1681,
    1062,
    1332,
    521,
    2186,
    865,
    2436,
    531,
    753,
    523,
    858,
    487,
    2021,
    500,
    893,
    829,
    968,
    952,
    694,
    766,
    649,
    1080,
    715,
    1231,
    1604,
    638,
    315,
    857,
    2806,
    2596,
    507,
    505,
    792,
    564,
    1029,
    897,
    893,
    587,
    795,
    802,
    1041,
    1254,
    1100,
    1138,
    635,
    434,
    2223,
    640,
    852,
    1360,
    1712,
    991,
    396,
    1080,
    1047,
    1379,
    1500,
    1402,
    610,
    562,
    806,
    2585,
    521,
    349,
    556,
    961,
    849,
    1052,
    550,
    351,
    311,
    2068,
    510,
    857,
    1441,
    1461,
    2114,
    2135,
    444,
    723,
    624,
    614,
    980,
    786,
    637,
    1125,
    597,
    509,
    1154,
    723,
    691,
    1058,
    1193
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
