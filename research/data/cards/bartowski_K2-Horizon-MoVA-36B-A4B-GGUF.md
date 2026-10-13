---
quantized_by: bartowski
pipeline_tag: text-generation
model_name: K2-Horizon-MoVA-36B-A4B
tags:
- k2-horizon
- 36b
- mova
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
base_model: IFM/K2-Horizon-MoVA-36B-A4B
---

## Llamacpp imatrix Quantizations of K2-Horizon-MoVA-36B-A4B by IFM

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b11462">b11462</a> for quantization.

Original model: https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B

**Model details:**
- Parameter count: 37B (source checkpoint)
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

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_K_M.gguf) (22.70GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [K2-Horizon-MoVA-36B-A4B-bf16.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/tree/main/K2-Horizon-MoVA-36B-A4B-bf16) | bf16 | 74.92GB | true | Full BF16 weights. |
| [K2-Horizon-MoVA-36B-A4B-Q8_0.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q8_0.gguf) | Q8_0 | 39.83GB | false | Extremely high quality, generally unneeded but max available quant. |
| [K2-Horizon-MoVA-36B-A4B-Q6_K_L.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q6_K_L.gguf) | Q6_K_L | 32.40GB | false | Uses Q8_0 for embed and output weights. Very high quality, near perfect, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q6_K.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q6_K.gguf) | Q6_K | 32.09GB | false | Very high quality, near perfect, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q5_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q5_K_M.gguf) | Q5_K_M | 26.71GB | false | High quality, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q5_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q5_K_S.gguf) | Q5_K_S | 26.03GB | false | High quality, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q4_1.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_1.gguf) | Q4_1 | 23.76GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [K2-Horizon-MoVA-36B-A4B-Q4_K_L.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_K_L.gguf) | Q4_K_L | 23.18GB | false | Uses Q8_0 for embed and output weights. Good quality, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q4_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_K_M.gguf) | Q4_K_M | 22.70GB | false | Good quality, default size for most use cases, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q4_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_K_S.gguf) | Q4_K_S | 22.04GB | false | Slightly lower quality with more space savings, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-Q4_0.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q4_0.gguf) | Q4_0 | 21.56GB | false | Legacy format, kept for compatibility with older tools. |
| [K2-Horizon-MoVA-36B-A4B-IQ4_NL.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ4_NL.gguf) | IQ4_NL | 21.54GB | false | Similar to IQ4_XS, but slightly larger. |
| [K2-Horizon-MoVA-36B-A4B-IQ4_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ4_XS.gguf) | IQ4_XS | 20.42GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [K2-Horizon-MoVA-36B-A4B-IQ3_M.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ3_M.gguf) | IQ3_M | 17.93GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [K2-Horizon-MoVA-36B-A4B-Q3_K_L.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q3_K_L.gguf) | Q3_K_L | 17.82GB | false | Lower quality but usable, good for low RAM availability. |
| [K2-Horizon-MoVA-36B-A4B-Q3_K_M.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q3_K_M.gguf) | Q3_K_M | 17.35GB | false | Low quality. |
| [K2-Horizon-MoVA-36B-A4B-IQ3_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ3_XS.gguf) | IQ3_XS | 17.32GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [K2-Horizon-MoVA-36B-A4B-Q3_K_S.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q3_K_S.gguf) | Q3_K_S | 16.76GB | false | Low quality, *not* recommended. |
| [K2-Horizon-MoVA-36B-A4B-IQ3_XXS.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ3_XXS.gguf) | IQ3_XXS | 15.80GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [K2-Horizon-MoVA-36B-A4B-Q2_K.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-Q2_K.gguf) | Q2_K | 13.57GB | false | Very low quality but surprisingly usable. |
| [K2-Horizon-MoVA-36B-A4B-IQ2_M.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ2_M.gguf) | IQ2_M | 13.09GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [K2-Horizon-MoVA-36B-A4B-IQ2_S.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ2_S.gguf) | IQ2_S | 11.97GB | false | Low quality, uses SOTA techniques to be usable. |
| [K2-Horizon-MoVA-36B-A4B-IQ2_XS.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ2_XS.gguf) | IQ2_XS | 11.72GB | false | Low quality, uses SOTA techniques to be usable. |
| [K2-Horizon-MoVA-36B-A4B-IQ2_XXS.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-IQ2_XXS.gguf) | IQ2_XXS | 10.64GB | false | Very low quality, uses SOTA techniques to be usable. |

Download a specific file:

```
hf download bartowski/K2-Horizon-MoVA-36B-A4B-GGUF --include "K2-Horizon-MoVA-36B-A4B-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/K2-Horizon-MoVA-36B-A4B-GGUF --include "K2-Horizon-MoVA-36B-A4B-Q4_K_M.gguf" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/K2-Horizon-MoVA-36B-A4B-GGUF --include "K2-Horizon-MoVA-36B-A4B-bf16/*" --local-dir ./
```

You can either specify a new local-dir (K2-Horizon-MoVA-36B-A4B-bf16) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/K2-Horizon-MoVA-36B-A4B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b11462 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## imatrix

All quants made using imatrix option, with a calibration corpus rendered through this model's own chat template. The corpus pairs plain prose with tool-calling and reasoning conversations ([corpus source data](https://gist.github.com/bartowski1182/e26453c0404e24eb317543ec5360f87a)), encoded exactly as this model sees them at inference and processed with `--parse-special`, so chat-format special tokens contribute to the importance matrix. The corpus rendered for this model is included in this repo: [K2-Horizon-MoVA-36B-A4B-calibration-v6.txt](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-calibration-v6.txt). The imatrix is available here: [K2-Horizon-MoVA-36B-A4B-imatrix.gguf](https://huggingface.co/bartowski/K2-Horizon-MoVA-36B-A4B-GGUF/blob/main/K2-Horizon-MoVA-36B-A4B-imatrix.gguf).

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
