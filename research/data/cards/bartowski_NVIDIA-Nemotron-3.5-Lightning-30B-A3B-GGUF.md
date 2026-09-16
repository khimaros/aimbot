---
quantized_by: bartowski
pipeline_tag: text-generation
license_link: https://openmdw.ai/license/1-1/
license: other
datasets:
- nvidia/nemotron-post-training-v3
- nvidia/nemotron-pre-training-datasets
base_model: nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
language:
- en
- es
- fr
- de
- it
- ja
tags:
- nvidia
- nemotron-3.5
track_downloads: true
base_model_relation: quantized
license_name: openmdw-1.1
---

## Llamacpp imatrix Quantizations of NVIDIA-Nemotron-3.5-Lightning-30B-A3B by nvidia

Using <a href="https://github.com/ggml-org/llama.cpp/">llama.cpp</a> release <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b10362">b10362</a> for quantization.

Original model: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16

**Model details:**
- Parameter count: 33B
- Input support: text
- MTP: yes - [details](#mtp)
- imatrix: yes - [details](#imatrix)

[How to run](#how-to-run)

## What's new:

Now actually with MTP!

The earlier upload incorrectly claimed to have MTP added, NOW it does.. For those who downloaded earlier versions and don't want to fully redownload, I've included the separated files for Q8_0 and Q4_0, sorry about that!

## Prompt format

```
<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
<think>
```

**Don't know which to choose?** Grab [Q4_K_M](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_M.gguf) (25.48GB) - usually a good mix of size and performance. Download instructions available [here](#downloading-using-the-hugging-face-cli)

## Available files:

| Filename | Quant type | File Size | Split | Description |
| -------- | ---------- | --------- | ----- | ----------- |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-bf16.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/tree/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-bf16) | bf16 | 65.85GB | true | Full BF16 weights. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q8_0.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q8_0.gguf) | Q8_0 | 35.00GB | false | Extremely high quality, generally unneeded but max available quant. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q6_K_L.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q6_K_L.gguf) | Q6_K_L | 34.31GB | false | Uses Q8_0 for embed and output weights. Very high quality, near perfect, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q6_K.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q6_K.gguf) | Q6_K | 34.31GB | false | Very high quality, near perfect, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_L.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_L.gguf) | Q5_K_L | 27.07GB | false | Uses Q8_0 for embed and output weights. High quality, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_M.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_M.gguf) | Q5_K_M | 26.96GB | false | High quality, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_L.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_L.gguf) | Q4_K_L | 25.61GB | false | Uses Q8_0 for embed and output weights. Good quality, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_M.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_M.gguf) | Q4_K_M | 25.48GB | false | Good quality, default size for most use cases, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_S.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q5_K_S.gguf) | Q5_K_S | 24.76GB | false | High quality, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_S.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_S.gguf) | Q4_K_S | 23.20GB | false | Slightly lower quality with more space savings, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_1.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_1.gguf) | Q4_1 | 20.87GB | false | Legacy format, similar performance to Q4_K_S but with improved tokens/watt on Apple silicon. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_XL.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_XL.gguf) | Q3_K_XL | 20.43GB | false | Uses Q8_0 for embed and output weights. Lower quality but usable, good for low RAM availability. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_M.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_M.gguf) | IQ3_M | 20.25GB | false | Medium-low quality, new method with decent performance comparable to Q3_K_M. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_L.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_L.gguf) | Q3_K_L | 20.25GB | false | Lower quality but usable, good for low RAM availability. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_M.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_M.gguf) | Q3_K_M | 19.82GB | false | Low quality. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_XS.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_XS.gguf) | IQ3_XS | 19.80GB | false | Lower quality, new method with decent performance, slightly better than Q3_K_S. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_XXS.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ3_XXS.gguf) | IQ3_XXS | 19.80GB | false | Lower quality, new method with decent performance, comparable to Q3 quants. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q2_K_L.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q2_K_L.gguf) | Q2_K_L | 19.09GB | false | Uses Q8_0 for embed and output weights. Very low quality but surprisingly usable. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_0.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_0.gguf) | Q4_0 | 19.06GB | false | Legacy format, kept for compatibility with older tools. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_S.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q3_K_S.gguf) | Q3_K_S | 18.94GB | false | Low quality, not recommended. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ4_NL.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ4_NL.gguf) | IQ4_NL | 18.92GB | false | Similar to IQ4_XS, but slightly larger. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ4_XS.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ4_XS.gguf) | IQ4_XS | 18.92GB | false | Decent quality, smaller than Q4_K_S with similar performance, *recommended*. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q2_K.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q2_K.gguf) | Q2_K | 18.91GB | false | Very low quality but surprisingly usable. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_M.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_M.gguf) | IQ2_M | 18.85GB | false | Relatively low quality, uses SOTA techniques to be surprisingly usable. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_S.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_S.gguf) | IQ2_S | 18.85GB | false | Low quality, uses SOTA techniques to be usable. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_XS.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_XS.gguf) | IQ2_XS | 18.84GB | false | Low quality, uses SOTA techniques to be usable. |
| [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_XXS.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-IQ2_XXS.gguf) | IQ2_XXS | 18.84GB | false | Very low quality, uses SOTA techniques to be usable. |

Download a specific file:

```
hf download bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF --include "NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_M.gguf" --local-dir ./
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
hf download bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF --include "NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_K_M.gguf" --local-dir ./
```

The files marked `true` in the Split column above are stored as multiple parts in a folder. To download all the parts to a local folder, run:

```
hf download bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF --include "NVIDIA-Nemotron-3.5-Lightning-30B-A3B-bf16/*" --local-dir ./
```

You can either specify a new local-dir (NVIDIA-Nemotron-3.5-Lightning-30B-A3B-bf16) or download them all in place (./)

</details>

## How to run

These quants run with [llama.cpp](https://github.com/ggml-org/llama.cpp) - installable in one line via [llama.app](https://llama.app/):

```
curl -LsSf https://llama.app/install.sh | sh
llama-server -hf bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF:Q4_K_M
```

llama-server includes a built-in chat web UI, served at http://localhost:8080 by default.

These quants were made with llama.cpp release b10362 - if this model's architecture is newly supported, you'll need that release or newer to run them.

They also work in: [LM Studio](https://lmstudio.ai/) · [koboldcpp](https://github.com/LostRuins/koboldcpp) · [ramalama](https://github.com/containers/ramalama) · [Jan AI](https://www.jan.ai/) · [Text Generation Web UI](https://github.com/oobabooga/text-generation-webui) · [LoLLMs](https://github.com/ParisNeo/lollms) · [Atomic Chat](https://atomic.chat/)

## MTP

This model has MTP (Multi-Token Prediction) layers, and they are included in these quants

MTP layers act as a built-in draft model, letting llama.cpp run speculative decoding for faster generation. To use them, add the following flag to your llama.cpp command:

```
--spec-type draft-mtp
```

Note: the MTP layers are stored at Q4_0 in the imatrix quants (except for the Q8_0 quant), since imatrix calibration does not exercise them. Q4_0 is chosen for its speed which massively benefits MTP performance.

## imatrix

All quants made using imatrix option with dataset from [here](https://gist.github.com/bartowski1182/82ae9b520227f57d79ba04add13d0d0d). The imatrix is available here: [NVIDIA-Nemotron-3.5-Lightning-30B-A3B-imatrix.gguf](https://huggingface.co/bartowski/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/blob/main/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-imatrix.gguf).

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
