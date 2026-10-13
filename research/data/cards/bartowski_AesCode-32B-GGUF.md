---
quantized_by: bartowski
pipeline_tag: image-text-to-text
base_model_relation: quantized
license: apache-2.0
language:
- en
tags:
- code-generation
- html
- multimodal
- reinforcement-learning
- design
base_model: microsoft/AesCode-32B
---

## Llamacpp imatrix Quantizations of AesCode-32B by microsoft

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11490">b11490</a> for quantization.

Original model: https://huggingface.co/microsoft/AesCode-32B

**Model details:**
- Parameter count: 33B (source checkpoint)
- Input support: text, image (with mmproj file) - [details](#multimodal)
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

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_K_M.gguf) (20.49GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [AesCode-32B-bf16.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/tree/main/AesCode-32B-bf16) | bf16 | 65.53GB | true | Full BF16 weights. |
| [AesCode-32B-Q8_0.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q8_0.gguf) | Q8_0 | 34.82GB | false | Extremely high quality, generally unneeded but max available quant. |
| [AesCode-32B-Q6_K_L.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q6_K_L.gguf) | Q6_K_L | 28.36GB | false | Uses Q8_0 for embed and output weights. Very high quality, near perfect, *recommended*. |
| [AesCode-32B-Q6_K.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q6_K.gguf) | Q6_K | 27.98GB | false | Very high quality, near perfect, *recommended*. |
| [AesCode-32B-Q5_K_M.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q5_K_M.gguf) | Q5_K_M | 23.79GB | false | High quality, *recommended*. |
| [AesCode-32B-Q5_K_S.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q5_K_S.gguf) | Q5_K_S | 22.81GB | false | High quality, *recommended*. |
| [AesCode-32B-Q4_K_L.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_K_L.gguf) | Q4_K_L | 21.06GB | false | Uses Q8_0 for embed and output weights. Good quality, *recommended*. |
| [AesCode-32B-Q4_1.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_1.gguf) | Q4_1 | 20.90GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [AesCode-32B-Q4_K_M.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_K_M.gguf) | Q4_K_M | 20.49GB | false | Good quality, default size for most use cases, *recommended*. |
| [AesCode-32B-Q4_K_S.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_K_S.gguf) | Q4_K_S | 19.14GB | false | Slightly lower quality with more space savings, *recommended*. |
| [AesCode-32B-IQ4_NL.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ4_NL.gguf) | IQ4_NL | 19.07GB | false | Similar to IQ4_XS, but slightly larger. |
| [AesCode-32B-Q4_0.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q4_0.gguf) | Q4_0 | 19.05GB | false | Legacy format, kept for compatibility with older tools. |
| [AesCode-32B-IQ4_XS.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ4_XS.gguf) | IQ4_XS | 18.12GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [AesCode-32B-Q3_K_L.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q3_K_L.gguf) | Q3_K_L | 17.52GB | false | Lower quality but usable, good for low RAM availability. |
| [AesCode-32B-Q3_K_M.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q3_K_M.gguf) | Q3_K_M | 16.52GB | false | Low quality. |
| [AesCode-32B-IQ3_M.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ3_M.gguf) | IQ3_M | 15.50GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [AesCode-32B-Q3_K_S.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q3_K_S.gguf) | Q3_K_S | 14.91GB | false | Low quality, *not* recommended. |
| [AesCode-32B-IQ3_XS.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ3_XS.gguf) | IQ3_XS | 14.37GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [AesCode-32B-IQ3_XXS.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ3_XXS.gguf) | IQ3_XXS | 13.60GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [AesCode-32B-Q2_K.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-Q2_K.gguf) | Q2_K | 13.01GB | false | Very low quality but surprisingly usable. |
| [AesCode-32B-IQ2_M.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ2_M.gguf) | IQ2_M | 12.71GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [AesCode-32B-IQ2_S.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ2_S.gguf) | IQ2_S | 12.02GB | false | Low quality, uses SOTA techniques to be usable. |
| [AesCode-32B-IQ2_XS.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ2_XS.gguf) | IQ2_XS | 11.41GB | false | Low quality, uses SOTA techniques to be usable. |
| [AesCode-32B-IQ2_XXS.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-IQ2_XXS.gguf) | IQ2_XXS | 10.63GB | false | Very low quality, uses SOTA techniques to be usable. |

Download a specific file:

```
hf download bartowski/AesCode-32B-GGUF --include "AesCode-32B-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/AesCode-32B-GGUF --include "AesCode-32B-Q4_K_M.gguf" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/AesCode-32B-GGUF --include "AesCode-32B-bf16/*" --local-dir ./
```

You can either specify a new local-dir (AesCode-32B-bf16) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/AesCode-32B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11490 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## Multimodal

This model supports image input. Alongside the quants, this repo includes the multimodal projector files [mmproj-AesCode-32B-bf16.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/mmproj-AesCode-32B-bf16.gguf) and [mmproj-AesCode-32B-f16.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/mmproj-AesCode-32B-f16.gguf), which pair with any quant above.

llama.cpp downloads the mmproj automatically when using `-hf` as shown above; if you're loading files manually, pass it with `--mmproj`.

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [AesCode-32B-calibration-v6.txt](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-calibration-v6.txt). The imatrix is available here: [AesCode-32B-imatrix.gguf](https://huggingface.co/bartowski/AesCode-32B-GGUF/blob/main/AesCode-32B-imatrix.gguf).

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
  "prose_chunks": 218,
  "tool_chunks": 268,
  "total_chunks": 486,
  "n_conversations": 164,
  "conversation_token_lengths": [
    319,
    847,
    573,
    1180,
    806,
    635,
    719,
    2084,
    1087,
    410,
    612,
    967,
    810,
    1200,
    481,
    669,
    2076,
    771,
    696,
    633,
    695,
    367,
    316,
    637,
    667,
    615,
    1009,
    580,
    547,
    785,
    1530,
    807,
    637,
    477,
    622,
    1229,
    999,
    455,
    509,
    718,
    425,
    1262,
    1075,
    703,
    244,
    778,
    645,
    646,
    984,
    1545,
    879,
    1713,
    680,
    944,
    536,
    2326,
    2079,
    450,
    2395,
    489,
    666,
    456,
    332,
    377,
    1978,
    518,
    607,
    661,
    636,
    729,
    579,
    716,
    651,
    559,
    706,
    689,
    595,
    1115,
    401,
    786,
    1583,
    816,
    265,
    130,
    345,
    731,
    2760,
    1947,
    357,
    1277,
    472,
    621,
    500,
    718,
    317,
    691,
    398,
    791,
    621,
    846,
    1036,
    799,
    636,
    846,
    827,
    539,
    617,
    368,
    483,
    1158,
    2144,
    2082,
    328,
    318,
    1248,
    847,
    844,
    2071,
    1357,
    613,
    295,
    581,
    1115,
    1091,
    1406,
    1115,
    522,
    676,
    508,
    242,
    651,
    2069,
    406,
    926,
    418,
    435,
    925,
    248,
    1071,
    458,
    147,
    124,
    1977,
    452,
    650,
    1695,
    1386,
    2020,
    2057,
    467,
    636,
    497,
    528,
    620,
    563,
    358,
    786,
    548,
    404,
    1095,
    617,
    516,
    739,
    1011
  ]
}
```

</details>

## Embed/output weights

Some of these quants (Q3_K_XL, Q4_K_L etc) are the standard quantization method with the embeddings and output weights quantized to Q8_0 instead of what they would normally default to.

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

Thank you ZeroWw for the inspiration to experiment with embed/output.

Want to support my work? Visit my ko-fi page here: https://ko-fi.com/bartowski
