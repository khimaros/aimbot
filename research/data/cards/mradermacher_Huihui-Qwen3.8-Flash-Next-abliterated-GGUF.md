---
base_model: huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated
language:
- en
library_name: transformers
license: other
license_link: LICENSE
license_name: qwen-community-1.0
mradermacher:
  readme_rev: 1
quantized_by: mradermacher
tags:
- abliterated
- uncensored
- huihui
- qwen3
---
## About

<!-- ### quantize_version: 2 -->
<!-- ### output_tensor_quantised: 1 -->
<!-- ### convert_type: hf -->
<!-- ### vocab_type:  -->
<!-- ### tags:  -->
<!-- ### quants:  x-f16 Q4_K_S Q2_K Q8_0 Q6_K Q3_K_M Q3_K_S Q3_K_L Q4_K_M Q5_K_S Q5_K_M IQ4_XS -->
<!-- ### quants_skip:  -->
<!-- ### skip_mmproj:  -->
static quants of https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated

<!-- provided-files -->

***For a convenient overview and download list, visit our [model page for this model](https://hf.tst.eu/model#Huihui-Qwen3.8-Flash-Next-abliterated-GGUF).***

weighted/imatrix quants are available at https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-i1-GGUF
## Usage

If you are unsure how to use GGUF files, refer to one of [TheBloke's
READMEs](https://huggingface.co/TheBloke/KafkaLM-70B-German-V0.1-GGUF) for
more details, including on how to concatenate multi-part files.

## Provided Quants

(sorted by size, not necessarily quality. IQ-quants are often preferable over similar sized non-IQ quants)

| Link | Type | Size/GB | Notes |
|:-----|:-----|--------:|:------|
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.mmproj-Q8_0.gguf) | mmproj-Q8_0 | 0.7 | multi-modal supplement |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.mmproj-f16.gguf) | mmproj-f16 | 1.0 | multi-modal supplement |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q2_K.gguf) | Q2_K | 80.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q3_K_S.gguf) | Q3_K_S | 88.9 |  |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q3_K_M.gguf) | Q3_K_M | 94.2 | lower quality |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q3_K_L.gguf) | Q3_K_L | 96.8 |  |
| [GGUF](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.IQ4_XS.gguf) | IQ4_XS | 98.5 |  |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_S.gguf.part1of3) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_S.gguf.part2of3) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_S.gguf.part3of3) | Q4_K_S | 111.9 | fast, recommended |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_M.gguf.part1of3) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_M.gguf.part2of3) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q4_K_M.gguf.part3of3) | Q4_K_M | 119.3 | fast, recommended |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_S.gguf.part1of3) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_S.gguf.part2of3) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_S.gguf.part3of3) | Q5_K_S | 127.8 |  |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_M.gguf.part1of3) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_M.gguf.part2of3) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q5_K_M.gguf.part3of3) | Q5_K_M | 134.2 |  |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q6_K.gguf.part1of4) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q6_K.gguf.part2of4) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q6_K.gguf.part3of4) [PART 4](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q6_K.gguf.part4of4) | Q6_K | 167.7 | very good quality |
| [PART 1](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q8_0.gguf.part1of4) [PART 2](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q8_0.gguf.part2of4) [PART 3](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q8_0.gguf.part3of4) [PART 4](https://huggingface.co/mradermacher/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/resolve/main/Huihui-Qwen3.8-Flash-Next-abliterated.Q8_0.gguf.part4of4) | Q8_0 | 188.3 | fast, best quality |

Here is a handy graph by ikawrakow comparing some lower-quality quant
types (lower is better):

![image.png](https://www.nethype.de/huggingface_embed/quantpplgraph.png)

And here are Artefact2's thoughts on the matter:
https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9

## FAQ / Model Request

See https://huggingface.co/mradermacher/model_requests for some answers to
questions you might have and/or if you want some other model quantized.

## Thanks

I thank my company, [nethype GmbH](https://www.nethype.de/), for letting
me use its servers and providing upgrades to my workstation to enable
this work in my free time.

<!-- end -->
