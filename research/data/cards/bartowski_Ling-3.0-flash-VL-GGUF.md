---
quantized_by: bartowski
pipeline_tag: image-text-to-text
base_model: inclusionAI/Ling-3.0-flash-VL
license: mit
base_model_relation: quantized
---

## Llamacpp imatrix Quantizations of Ling-3.0-flash-VL by inclusionAI

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11159">b11159</a> for quantization.

Original model: https://huggingface.co/inclusionAI/Ling-3.0-flash-VL

**Model details:**
- Parameter count: 125B
- Input support: text, image (with mmproj file) - [details](#multimodal)
- Speculative decoding: no
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

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_K_M) (78.66GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [Ling-3.0-flash-VL-bf16.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-bf16) | bf16 | 248.94GB | true | Full BF16 weights. |
| [Ling-3.0-flash-VL-Q8_0.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q8_0) | Q8_0 | 132.37GB | true | Extremely high quality, generally unneeded but max available quant. |
| [Ling-3.0-flash-VL-Q6_K.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q6_K) | Q6_K | 109.69GB | true | Very high quality, near perfect, *recommended*. |
| [Ling-3.0-flash-VL-Q6_K_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q6_K_S) | Q6_K_S | 104.57GB | true | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [Ling-3.0-flash-VL-Q5_K_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q5_K_M) | Q5_K_M | 95.88GB | true | High quality, *recommended*. |
| [Ling-3.0-flash-VL-Q5_K_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q5_K_S) | Q5_K_S | 88.96GB | true | High quality, *recommended*. |
| [Ling-3.0-flash-VL-Q4_K_L.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_K_L) | Q4_K_L | 84.88GB | true | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [Ling-3.0-flash-VL-IQ4_NL.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-IQ4_NL) | IQ4_NL | 78.68GB | true | Similar to IQ4_XS, but slightly larger. |
| [Ling-3.0-flash-VL-Q4_K_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_K_M) | Q4_K_M | 78.66GB | true | Good quality, default size for most use cases, *recommended*. |
| [Ling-3.0-flash-VL-Q4_1.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_1) | Q4_1 | 78.47GB | true | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [Ling-3.0-flash-VL-Q4_K_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_K_S) | Q4_K_S | 73.98GB | true | Slightly lower quality with more space savings, *recommended*. |
| [Ling-3.0-flash-VL-Q4_0.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q4_0) | Q4_0 | 71.11GB | true | Legacy format, kept for compatibility with older tools. |
| [Ling-3.0-flash-VL-IQ4_XS.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-IQ4_XS) | IQ4_XS | 69.37GB | true | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [Ling-3.0-flash-VL-IQ3_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-IQ3_M) | IQ3_M | 67.61GB | true | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [Ling-3.0-flash-VL-Q3_K_L.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q3_K_L) | Q3_K_L | 63.35GB | true | Lower quality but usable, good for low RAM availability. |
| [Ling-3.0-flash-VL-Q3_K_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q3_K_M) | Q3_K_M | 59.77GB | true | Low quality. |
| [Ling-3.0-flash-VL-Q3_K_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-Q3_K_S) | Q3_K_S | 56.83GB | true | Low quality, *not* recommended. |
| [Ling-3.0-flash-VL-IQ3_XS.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-IQ3_XS) | IQ3_XS | 56.83GB | true | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [Ling-3.0-flash-VL-IQ3_XXS.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/Ling-3.0-flash-VL-IQ3_XXS) | IQ3_XXS | 53.94GB | true | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [Ling-3.0-flash-VL-Q2_K.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-Q2_K.gguf) | Q2_K | 47.81GB | false | Very low quality but surprisingly usable. |
| [Ling-3.0-flash-VL-IQ2_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ2_M.gguf) | IQ2_M | 45.32GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [Ling-3.0-flash-VL-IQ2_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ2_S.gguf) | IQ2_S | 41.01GB | false | Low quality, uses SOTA techniques to be usable. |
| [Ling-3.0-flash-VL-IQ2_XS.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ2_XS.gguf) | IQ2_XS | 38.60GB | false | Low quality, uses SOTA techniques to be usable. |
| [Ling-3.0-flash-VL-IQ2_XXS.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ2_XXS.gguf) | IQ2_XXS | 36.69GB | false | Very low quality, uses SOTA techniques to be usable. |
| [Ling-3.0-flash-VL-IQ1_M.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ1_M.gguf) | IQ1_M | 31.30GB | false | Extremely low quality, *not* recommended. |
| [Ling-3.0-flash-VL-IQ1_S.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-IQ1_S.gguf) | IQ1_S | 28.07GB | false | Extremely low quality, *not* recommended. |

Download a specific file:

```
hf download bartowski/Ling-3.0-flash-VL-GGUF --include "Ling-3.0-flash-VL-Q4_K_M/*" --local-dir ./
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
hf download bartowski/Ling-3.0-flash-VL-GGUF --include "Ling-3.0-flash-VL-Q4_K_M/*" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/Ling-3.0-flash-VL-GGUF --include "Ling-3.0-flash-VL-Q8_0/*" --local-dir ./
```

You can either specify a new local-dir (Ling-3.0-flash-VL-Q8_0) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/Ling-3.0-flash-VL-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11159 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Multimodal

This model supports image input. Alongside the quants, this repo includes the multimodal projector files [mmproj-Ling-3.0-flash-VL-bf16.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/mmproj-Ling-3.0-flash-VL-bf16.gguf) and [mmproj-Ling-3.0-flash-VL-f16.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/mmproj-Ling-3.0-flash-VL-f16.gguf), which pair with any quant above.

llama.cpp downloads the mmproj automatically when using `-hf` as shown above; if you're loading files manually, pass it with `--mmproj`.

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-93ecba14028d5e4b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.87×, Q3_K_M 0.85× and IQ1_S 0.97× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K | 109.69GB | 7.03 | 7.03 | 71 % |
| Q6_K_S | 104.57GB | 6.70 | 6.70 | 91 % |
| Q5_K_M | 95.88GB | 6.14 | 6.14 | 70 % |
| Q5_K_S | 88.96GB | 5.69 | 5.70 | 91 % |
| Q4_K_L | 84.88GB | 5.42 | 5.44 | 50 % |
| IQ4_NL | 78.68GB | 5.02 | 5.04 | 70 % |
| Q4_K_M | 78.66GB | 5.02 | 5.04 | 70 % |
| Q4_K_S | 73.98GB | 4.72 | 4.74 | 90 % |
| IQ4_XS | 69.37GB | 4.42 | 4.45 | 90 % |
| IQ3_M | 67.61GB | 4.31 | 4.33 | 50 % |
| Q3_K_L | 63.35GB | 4.03 | 4.06 | 50 % |
| Q3_K_M | 59.77GB | 3.80 | 3.83 | 70 % |
| Q3_K_S | 56.83GB | 3.61 | 3.64 | 90 % |
| IQ3_XS | 56.83GB | 3.61 | 3.64 | 90 % |
| IQ3_XXS | 53.94GB | 3.42 | 3.46 | 70 % |
| Q2_K | 47.81GB | 3.02 | 3.06 | 70 % |
| IQ2_M | 45.32GB | 2.86 | 2.90 | 70 % |
| IQ2_S | 41.01GB | 2.58 | 2.63 | 70 % |
| IQ2_XS | 38.60GB | 2.43 | 2.47 | 90 % |
| IQ2_XXS | 36.69GB | 2.31 | 2.35 | 70 % |
| IQ1_M | 31.30GB | 1.96 | 2.01 | 70 % |
| IQ1_S | 28.07GB | 1.75 | 1.80 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0922 ± 0.0022 | 0.1186 ± 0.0025 | 0.87× | +3.4 % |
| Q3_K_M | 0.2095 ± 0.0031 | 0.2745 ± 0.0041 | 0.85× | +4.4 % |
| IQ1_S | 1.2119 ± 0.0101 | 1.4089 ± 0.0111 | 0.97× | +8.6 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [Ling-3.0-flash-VL-calibration-v6.txt](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-calibration-v6.txt). The imatrix is available here: [Ling-3.0-flash-VL-imatrix.gguf](https://huggingface.co/bartowski/Ling-3.0-flash-VL-GGUF/blob/main/Ling-3.0-flash-VL-imatrix.gguf).

<details>
<summary>Calibration render details</summary>

```json
{
  "generator": "auto_quant_v2 calibration renderer",
  "recipe": "calibration-v6",
  "model": "Ling-3.0-flash-VL",
  "encoder": "chat_template",
  "library_versions": {
    "transformers": "5.9.0",
    "tokenizers": "0.22.2",
    "tiktoken": "0.14.0",
    "blobfile": "3.3.0",
    "huggingface_hub": "1.31.0"
  },
  "chunk_size": 512,
  "prose_chunks": 220,
  "tool_chunks": 345,
  "total_chunks": 565,
  "tool_chunk_fraction": 0.611,
  "n_conversations": 137,
  "extension_convs_used": 0,
  "conversation_token_lengths": [
    523,
    1594,
    1195,
    1476,
    1052,
    1303,
    3131,
    756,
    1165,
    1355,
    1020,
    2059,
    836,
    1202,
    2757,
    1193,
    1099,
    948,
    694,
    677,
    1326,
    995,
    1312,
    1167,
    1838,
    1463,
    1602,
    846,
    1376,
    1604,
    1477,
    1163,
    1213,
    1003,
    1019,
    1651,
    1621,
    1147,
    433,
    1912,
    1392,
    1051,
    1359,
    1972,
    2023,
    1233,
    1569,
    828,
    2907,
    1063,
    2811,
    725,
    955,
    915,
    924,
    655,
    2396,
    842,
    1100,
    1045,
    1169,
    1133,
    871,
    1153,
    1116,
    1530,
    874,
    1487,
    2098,
    803,
    333,
    1073,
    3282,
    2860,
    671,
    867,
    975,
    1022,
    1246,
    1052,
    1077,
    753,
    1155,
    988,
    1244,
    1474,
    1324,
    2041,
    799,
    608,
    2717,
    658,
    1345,
    1628,
    1936,
    1168,
    583,
    1336,
    1136,
    1655,
    1759,
    1637,
    782,
    961,
    979,
    2741,
    697,
    679,
    710,
    1352,
    1011,
    1542,
    731,
    361,
    327,
    2571,
    949,
    1087,
    1815,
    1974,
    2654,
    2646,
    759,
    932,
    797,
    888,
    1191,
    946,
    809,
    1270,
    793,
    668,
    1711,
    967,
    880,
    1243,
    1412
  ],
  "warnings": []
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
