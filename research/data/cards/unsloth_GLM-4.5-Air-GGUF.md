---
tags:
- unsloth
base_model:
- zai-org/GLM-4.5-Air
license: mit
language:
- en
- zh
pipeline_tag: text-generation
library_name: transformers
---
> [!NOTE]
>  Includes Unsloth **chat template fixes**! <br> For `llama.cpp`, use `--jinja`
>

<div>
<p style="margin-top: 0;margin-bottom: 0;">
    <em><a href="https://docs.unsloth.ai/basics/unsloth-dynamic-v2.0-gguf">Unsloth Dynamic 2.0</a> achieves superior accuracy & outperforms other leading quants.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; ">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://docs.unsloth.ai/">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>


# GLM-4.5-Air

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 Join our <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> community.
    <br>
    📖 Check out the GLM-4.5 <a href="https://z.ai/blog/glm-4.5" target="_blank">technical blog</a>.
    <br>
    📍 Use GLM-4.5 API services on <a href="https://docs.z.ai/guides/llm/glm-4.5">Z.ai API Platform (Global)</a> or <br> <a href="https://docs.bigmodel.cn/cn/guide/models/text/glm-4.5">Zhipu AI Open Platform (Mainland China)</a>.
    <br>
    👉 One click to <a href="https://chat.z.ai">GLM-4.5</a>.
</p>
  
## Model Introduction

The **GLM-4.5** series models are foundation models designed for intelligent agents. GLM-4.5 has **355** billion total parameters with **32** billion active parameters, while GLM-4.5-Air adopts a more compact design with **106** billion total parameters and **12** billion active parameters. GLM-4.5 models unify reasoning, coding, and intelligent agent capabilities to meet the complex demands of intelligent agent applications.

Both GLM-4.5 and GLM-4.5-Air are hybrid reasoning models that provide two modes: thinking mode for complex reasoning and tool usage, and non-thinking mode for immediate responses.

We have open-sourced the base models, hybrid reasoning models, and FP8 versions of the hybrid reasoning models for both GLM-4.5 and GLM-4.5-Air. They are released under the MIT open-source license and can be used commercially and for secondary development.

As demonstrated in our comprehensive evaluation across 12 industry-standard benchmarks, GLM-4.5 achieves exceptional performance with a score of **63.2**, in the **3rd** place among all the proprietary and open-source  models. Notably, GLM-4.5-Air delivers competitive results at **59.8** while maintaining superior efficiency.

![bench](https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/bench.png)

For more eval results, show cases, and technical details, please visit
our [technical blog](https://z.ai/blog/glm-4.5). The technical report will be released soon.


The model code, tool parser and reasoning parser can be found in the implementation of [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4_moe), [vLLM](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/models/glm4_moe_mtp.py) and [SGLang](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/models/glm4_moe.py).

## Quick Start

Please refer our [github page](https://github.com/zai-org/GLM-4.5) for more detail.
