---
quantized_by: bartowski
pipeline_tag: image-text-to-text
base_model_relation: quantized
tags:
- mimo_v2
- agentic
- distillation
- supervised-fine-tuning
- code
- tool-use
base_model: XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B
---

## Llamacpp imatrix Quantizations of MiMo-V2.6-Distill-Qwen-9B by XiaomiMiMo

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b10964">b10964</a> for quantization.

Original model: https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Distill-Qwen-9B

**Model details:**
- Parameter count: 9B
- Input support: text, image (with mmproj file) - [details](#multimodal)
- Speculative decoding: no
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## Prompt format

```
<|im_start|>system
{system_prompt}<|im_end|><|im_start|>user
{prompt}<|im_end|><|im_start|>assistant
```

<details><summary>Prompt format with tool definitions</summary>

```
<|im_start|>system
You are provided with the following tools:

<tools>
{"type": "function", "function": {"name": "get_stock_price", "description": "Get the current stock price", "parameters": {"type": "object", "properties": {"symbol": {"type": "string", "description": "The stock symbol, e.g. AAPL, GOOG"}}, "required": ["symbol"]}}}
</tools><|im_end|><|im_start|>system
{system_prompt}<|im_end|><|im_start|>user
{prompt}<|im_end|><|im_start|>assistant
```

</details>

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_K_M.gguf) (5.84GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [MiMo-V2.6-Distill-Qwen-9B-bf16.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-bf16.gguf) | bf16 | 17.92GB | false | Full BF16 weights. |
| [MiMo-V2.6-Distill-Qwen-9B-Q8_0.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q8_0.gguf) | Q8_0 | 9.55GB | false | Extremely high quality, generally unneeded but max available quant. |
| [MiMo-V2.6-Distill-Qwen-9B-Q6_K_L.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q6_K_L.gguf) | Q6_K_L | 8.11GB | false | The large size of Q6_K, about halfway to Q8_0 in size. Very high quality, near perfect, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q6_K.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q6_K.gguf) | Q6_K | 7.79GB | false | Very high quality, near perfect, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q6_K_S.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q6_K_S.gguf) | Q6_K_S | 7.51GB | false | Very high quality, near perfect, a little smaller than Q6_K with almost all of the model at Q6_K precision, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q5_K_M.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q5_K_M.gguf) | Q5_K_M | 6.88GB | false | High quality, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q5_K_S.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q5_K_S.gguf) | Q5_K_S | 6.50GB | false | High quality, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q4_K_L.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_K_L.gguf) | Q4_K_L | 6.20GB | false | The large size of Q4_K, between Q4_K_M and Q5_K_S: more of the most sensitive weights kept at higher precision, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q4_1.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_1.gguf) | Q4_1 | 5.94GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [MiMo-V2.6-Distill-Qwen-9B-Q4_K_M.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_K_M.gguf) | Q4_K_M | 5.84GB | false | Good quality, default size for most use cases, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ4_NL.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ4_NL.gguf) | IQ4_NL | 5.83GB | false | Similar to IQ4_XS, but slightly larger. |
| [MiMo-V2.6-Distill-Qwen-9B-Q4_K_S.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_K_S.gguf) | Q4_K_S | 5.48GB | false | Slightly lower quality with more space savings, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-Q4_0.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q4_0.gguf) | Q4_0 | 5.48GB | false | Legacy format, kept for compatibility with older tools. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ4_XS.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ4_XS.gguf) | IQ4_XS | 5.23GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ3_M.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ3_M.gguf) | IQ3_M | 4.85GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [MiMo-V2.6-Distill-Qwen-9B-Q3_K_L.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q3_K_L.gguf) | Q3_K_L | 4.66GB | false | Lower quality but usable, good for low RAM availability. |
| [MiMo-V2.6-Distill-Qwen-9B-Q3_K_M.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q3_K_M.gguf) | Q3_K_M | 4.48GB | false | Low quality. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ3_XS.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ3_XS.gguf) | IQ3_XS | 4.27GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [MiMo-V2.6-Distill-Qwen-9B-Q3_K_S.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q3_K_S.gguf) | Q3_K_S | 4.26GB | false | Low quality, *not* recommended. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ3_XXS.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ3_XXS.gguf) | IQ3_XXS | 4.14GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [MiMo-V2.6-Distill-Qwen-9B-Q2_K.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-Q2_K.gguf) | Q2_K | 3.64GB | false | Very low quality but surprisingly usable. |
| [MiMo-V2.6-Distill-Qwen-9B-IQ2_M.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-IQ2_M.gguf) | IQ2_M | 3.54GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |

Download a specific file:

```
hf download bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF --include "MiMo-V2.6-Distill-Qwen-9B-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF --include "MiMo-V2.6-Distill-Qwen-9B-Q4_K_M.gguf" --local-dir ./
```

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b10964 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Multimodal

This model supports image input. Alongside the quants, this repo includes the multimodal projector files [mmproj-MiMo-V2.6-Distill-Qwen-9B-bf16.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/mmproj-MiMo-V2.6-Distill-Qwen-9B-bf16.gguf) and [mmproj-MiMo-V2.6-Distill-Qwen-9B-f16.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/mmproj-MiMo-V2.6-Distill-Qwen-9B-f16.gguf), which pair with any quant above.

llama.cpp downloads the mmproj automatically when using `-hf` as shown above; if you're loading files manually, pass it with `--mmproj`.

## Per-tensor layouts

Some of these files were built with a layout computed for this model instead of llama.cpp's standard one-size-fits-all rules. A Q4_K_M is still mostly Q4_K; the extra precision goes to the weights this particular model is most sensitive to. The S, M or L in a name says how much of the model stays at the base precision: about 90 % for S, 70 % for M and 50 % for L. An `_L` name is simply the large size of its family. Q4_K_L is to Q4_K_M what Q4_K_M is to Q4_K_S; Q6_K_S, Q6_K and Q6_K_L are the small, medium and large sizes of Q6_K, with Q6_K_L about halfway to Q8_0. In earlier releases an `_L` name meant the embedding and output weights were kept at Q8_0; in these files it means the larger size of the base type. There is no size target, so each file's bits per weight is reported rather than promised.

The layout each of these files was built with is published in the [`layouts/`](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/tree/main/layouts) folder: `<file>.tensor-types.txt` is the exact `--tensor-type-file` given to `llama-quantize`, and `<file>.layout.json` records how it was computed, including the generator version, the llama.cpp release and the commit, so any of them can be rebuilt. The code that computed them is public at [`quantization-config`](https://github.com/bartowski1182/quantization-config); its tag `key-93ecba14028d5e4b` is the exact snapshot these files record. The method is described in [this write-up](https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization).

Checked on this model before any of these files were released: Q4_K_M reached 0.87×, Q3_K_M 0.86× and IQ2_M 0.83× the KL divergence of the standard layout at the same file size.

<details>
<summary>Layout details</summary>

Files built from a computed layout:

| Quant | Size | Body bits/weight | File bits/weight | Body kept at base type |
| ----- | ---- | ---------------- | ---------------- | ---------------------- |
| Q6_K_L | 8.11GB | 7.40 | 6.89 | 50 % |
| Q6_K | 7.79GB | 7.04 | 6.63 | 70 % |
| Q6_K_S | 7.51GB | 6.71 | 6.38 | 90 % |
| Q5_K_M | 6.88GB | 6.14 | 5.85 | 70 % |
| Q5_K_S | 6.50GB | 5.70 | 5.52 | 90 % |
| Q4_K_L | 6.20GB | 5.50 | 5.27 | 50 % |
| Q4_K_M | 5.84GB | 5.09 | 4.97 | 70 % |
| IQ4_NL | 5.83GB | 5.07 | 4.95 | 70 % |
| Q4_K_S | 5.48GB | 4.67 | 4.66 | 90 % |
| IQ4_XS | 5.23GB | 4.41 | 4.44 | 90 % |
| IQ3_M | 4.85GB | 4.24 | 4.12 | 50 % |
| Q3_K_L | 4.66GB | 4.02 | 3.96 | 50 % |
| Q3_K_M | 4.48GB | 3.81 | 3.81 | 70 % |
| IQ3_XS | 4.27GB | 3.57 | 3.63 | 90 % |
| Q3_K_S | 4.26GB | 3.56 | 3.62 | 90 % |
| IQ3_XXS | 4.14GB | 3.42 | 3.52 | 70 % |
| Q2_K | 3.64GB | 3.00 | 3.10 | 70 % |
| IQ2_M | 3.54GB | 2.88 | 3.01 | 70 % |

Checked on this model: the computed layout against the standard one, measured by KL divergence against the unquantized model. The ratio compares each computed file with the standard ladder read at that file's own size, so it can differ from the two KLD columns when the two files differ in size.

| Quant | Computed layout KLD | Standard layout KLD | Ratio at equal size | Size vs standard file |
| ----- | ------------------- | ------------------- | ------------------- | --------------------- |
| Q4_K_M | 0.0303 ± 0.0014 | 0.0319 ± 0.0014 | 0.87× | −1.2 % |
| Q3_K_M | 0.1291 ± 0.0027 | 0.1037 ± 0.0025 | 0.86× | −8.9 % |
| IQ2_M | 0.2711 ± 0.0037 | 0.2698 ± 0.0035 | 0.83× | −6.2 % |

How it works: the base type is a floor for every body tensor and a fixed share of the body bytes stays at it (90 % for S, 70 % for M, 50 % for L); the remaining bytes go where a cross-model sensitivity prior, measured by KL divergence against the unquantized model, says they buy the most quality. The embedding and output tensors are sized by their share of the file: a small table is kept at Q8_0, a large one follows the file's bitrate. A K-quant and the IQ quant with the same base bitrate (Q3_K_S and IQ3_XS, Q3_K_M and IQ3_S, Q3_K_L and IQ3_M) come out at about the same size; the IQ file is the GPU-oriented twin.

</details>

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [MiMo-V2.6-Distill-Qwen-9B-calibration-v6.txt](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-calibration-v6.txt). The imatrix is available here: [MiMo-V2.6-Distill-Qwen-9B-imatrix.gguf](https://huggingface.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF/blob/main/MiMo-V2.6-Distill-Qwen-9B-imatrix.gguf).

<details>
<summary>Calibration render details</summary>

```json
{
  "generator": "auto_quant_v2 calibration renderer",
  "recipe": "calibration-v6",
  "model": "MiMo-V2.6-Distill-Qwen-9B",
  "encoder": "chat_template",
  "library_versions": {
    "transformers": "5.9.0",
    "tokenizers": "0.22.2",
    "tiktoken": "0.14.0",
    "blobfile": "3.3.0"
  },
  "chunk_size": 512,
  "prose_chunks": 214,
  "tool_chunks": 304,
  "total_chunks": 518,
  "tool_chunk_fraction": 0.587,
  "n_conversations": 137,
  "extension_convs_used": 0,
  "conversation_token_lengths": [
    380,
    1443,
    1022,
    1296,
    910,
    1150,
    2919,
    595,
    1009,
    1191,
    871,
    1912,
    697,
    1020,
    2536,
    1056,
    936,
    802,
    553,
    534,
    1178,
    818,
    1172,
    1018,
    1654,
    1314,
    1425,
    677,
    1191,
    1423,
    1336,
    989,
    1059,
    853,
    1013,
    1484,
    1440,
    991,
    293,
    1726,
    1227,
    913,
    1190,
    1784,
    1865,
    1081,
    1425,
    668,
    2695,
    918,
    2644,
    587,
    814,
    747,
    900,
    514,
    2266,
    682,
    964,
    903,
    999,
    987,
    693,
    988,
    950,
    1365,
    708,
    1335,
    1908,
    657,
    318,
    919,
    3102,
    2592,
    525,
    709,
    806,
    846,
    1070,
    898,
    922,
    594,
    972,
    843,
    1099,
    1296,
    1181,
    1841,
    665,
    456,
    2508,
    635,
    1180,
    1466,
    1746,
    1019,
    443,
    1172,
    1122,
    1519,
    1621,
    1457,
    616,
    792,
    832,
    2569,
    556,
    512,
    567,
    1197,
    868,
    1362,
    584,
    345,
    314,
    2373,
    786,
    929,
    1647,
    1791,
    2437,
    2424,
    593,
    784,
    656,
    719,
    1015,
    783,
    658,
    1131,
    646,
    526,
    1519,
    818,
    733,
    1083,
    1255
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
