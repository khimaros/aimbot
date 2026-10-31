---
license: other
language:
- en
- fr
- de
- es
- pt
- it
- ja
- ko
- ru
- zh
- ar
- fa
- id
- ms
- ne
- pl
- ro
- sr
- sv
- tr
- uk
- vi
- hi
- bn
- bg
- hr
- cs
- da
- nl
- et
- fi
- el
- hu
- ga
- lv
- lt
- mt
- sk
- sl
tags:
- vLLM
- SGLang
- transformers
- llama.cpp
- unsloth
- mistral
base_model:
- mistralai/Mistral-Large-4-1T-A52B
license_name: mistral-ecosystem-open-weight
license_link: https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE
---
# Read our How to [Run Mistral Large 4 Guide!](https://unsloth.ai/docs/models/mistral-large-4)

<div>
<p style="margin-top: 0;margin-bottom: 0;">
   <em>See <a href="https://unsloth.ai/docs/basics/unsloth-dynamic-v3.0-gguf">Unsloth Dynamic 3.0 GGUFs</a> for our quantization benchmarks.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; ">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/models/mistral-large-4">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
    <ul style="margin: 0;">
    <li>Run the smallest 1-bit (233 GB) on a 256GB RAM device, 2-bit (302-378 GB) on 384-512GB, or near full precision (Q8, 1.1 TB) on 1.2TB+. <a href="https://unsloth.ai/docs/models/mistral-large-4">Read Guide</a></li>
    <li>To run, please use our llama.cpp build or the <a href="https://unsloth.ai/docs/desktop">Unsloth Desktop</a> app.</li>
    <li>Includes the vision projector (mmproj) and the DSpark speculative decoding draft.</li>
</div>
</div>

<div style="display: flex; gap: 8px; align-items: flex-start;">
  <img src="assets/size_vs_kld.png" alt="Mistral-Large-4-1T-A52B Unsloth GGUF KLD vs size" style="width: 50%; min-width: 0; margin: 0;">
  <img src="assets/size_vs_top1.png" alt="Mistral-Large-4-1T-A52B Unsloth GGUF top-1 accuracy vs size" style="width: 50%; min-width: 0; margin: 0;">
</div>

**Speculative decoding:** add `-md dspark-Mistral-Large-4-1T-A52B-Q8_0.gguf --spec-type draft-dspark --spec-draft-n-max 3`
(mean acceptance length about 2.5, about 2x decode speed at batch 1).

**Vision:** add `--mmproj mmproj-BF16.gguf` (or `mmproj-F16.gguf`).

---

# Mistral Large 4 - Le Chonk

Mistral Large 4 is our largest and most capable model to date: a 1 trillion-parameter natively multimodal Mixture-of-Experts model with 49 billion active parameters per token (52 billion including embeddings and output layers), trained from scratch on 3,800 NVIDIA Grace Blackwell GPUs in Mistral's own datacenters in Europe.

Mistral Large 4 unifies instruction following, reasoning, coding, and agentic workflows in a single set of weights. While a generalist model, it shows especially good performance on workloads such as cybersecurity, finance, and law, and it surpasses frontier closed models on visual grounding. It is natively fluent in 160+ languages, including every official language of the European Union.

Find more information on our [blog](https://mistral.ai/news/mistral-large-4-oss/). The model is also served on the [Mistral API](https://docs.mistral.ai/models/mistral-large-4-0) as `mistral-large-4`.

> [!Note]
> A quantized [NVFP4 checkpoint](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4) is also available, with a smaller memory footprint, faster inference and same performance. It targets Blackwell GPUs and supports vLLM and SGLang.

## Key Features

Mistral Large 4 includes the following architectural choices:

- **~1T total / ~52B active parameters**: granular Mixture-of-Experts with 128 routed experts (4 active per token) and 1 shared expert.
- **1M context length**, for long-context workloads.
- **Multimodal input**: accepts text and image input, with text output. Pixtral-style vision encoder trained to handle variable image sizes and aspect ratios.
- **Instruct and Reasoning functionalities** with function calls, reasoning effort configurable per request.

Mistral Large 4 offers the following capabilities:

- **Reasoning Mode**: three reasoning efforts — `low`, `medium`, `high` (default) — so the same model can answer a quick chat reply or work through a complex agentic run.
- **Vision**: analyzes images, charts, technical drawings, and documents, with state-of-the-art visual grounding among open weights.
- **Multilingual**: natively fluent in 160+ languages, including all official languages of the European Union.
- **System Prompt**: strong adherence and support for system prompts.
- **Agentic**: native function calling, JSON output, and strict JSON schema enforcement.
- **Cybersecurity**: state of the art among open-weight models for security work, while refusing malicious requests.
- **Large Context Window**: supports a 1M context window.

We release this model under the [**Mistral Ecosystem Open-Weight License**](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE): a modified version of the MIT license, for both commercial and non-commercial use — operating a Model-as-a-Service business requires a separate commercial license with Mistral.

## Recommended Settings

- **Reasoning Effort**:
  - `'low'` / `'medium'` / `'high'` — default is `'high'`.
  - Use `reasoning_effort="high"` for complex prompts and agentic usage, `'low'` for fast chat replies and `'medium'` for day to day usage.
- **Sampling**: for all reasoning efforts, we recommend the following sampling parameters:
  - `temperature=1.0`
  - `top_p=0.95`
- **System Prompt**: define a clear environment and use case, including guidance on how to effectively leverage tools in agentic systems.
- **Tools**: keep the set of tools well-defined and limit their number to the minimum required for the use case.
- **Context**: the checkpoint supports a 1M context window.

## Benchmarks

We compared Mistral Large 4 with recent open-weight models. We report results on agentic coding and global intelligence here; for more benchmarks, especially on cybersecurity, finance and law, see our [blog post](https://mistral.ai/news/mistral-large-4-oss/).

### Agentic Coding

Mistral Large 4 delivers frontier coding performance with significantly fewer tokens, making sophisticated coding agents more economical to run at scale.

On the Artificial Analysis Coding Agent Index, ML4 scores **48%**, effectively tied with the leading open-weight model, GLM-5.3, while using **47%** fewer tokens per task on average.

![Artificial Analysis - Coding Agent Index](images/coding_index.png)

### Global Intelligence

On the Artificial Analysis Intelligence Index v5, Mistral Large 4 scores **26**, the highest among western open-weight models. The leading open-weight models from China score higher on this aggregate index, but Mistral Large 4 is particularly strong on coding and cybersecurity, as shown in our [blog post](https://mistral.ai/news/mistral-large-4-oss/).

![Artificial Analysis - Intelligence Index v5](images/intelligence_index.png)

## Demo Gallery

The [ML4 Demo Hub](https://huggingface.co/spaces/mistralai/ml4-hub) is a live gallery of demo Spaces built with Mistral Large 4, from us and from the community: coding, vision and grounding, tool calls, JSON schema, multilingual, and more. Any Space tagged `Le_chonk` appears there.

Official demos run on the Mistral API with a small shared free budget per visitor for the first week of the release, so you can try the model without paying. You can also use your own Mistral API key.

To build a demo, we recommend [Mistral Vibe](https://github.com/mistralai/mistral-vibe), our coding agent powered by Mistral Large 4.

## License

This model is licensed under the [Mistral Ecosystem Open-Weight License](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*
