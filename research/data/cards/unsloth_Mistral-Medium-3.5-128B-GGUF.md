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
tags:
- mistral
- unsloth
base_model:
- mistralai/Mistral-Medium-3.5-128B
---
We worked with Mistral to fix Mistral Medium 3.5 inference issues affecting some implementations (**not related to Unsloth** or our quants).<br>
The issue came from a YaRN parsing quirk in implementations like transformers and llama.cpp. Setting `mscale_all_dim` from `1` to `0` fixes it, including the model forgetting previous conversations.<br>
Mistral has now pushed these fixes to their official repo.

# Read our How to [Run Mistral 3.5 Guide!](https://unsloth.ai/docs/models/mistral-3.5)
<div>
  <p style="margin: 0 0 0px 0; margin-top: 0px;">
    <em>See <a href="https://unsloth.ai/docs/basics/unsloth-dynamic-v2.0-gguf">Unsloth Dynamic 2.0 GGUFs</a> for our quantization benchmarks.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 0px;">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/models/mistral-3.5">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>

---
# Mistral Medium 3.5 128B

Mistral Medium 3.5 is our first flagship merged model. It is a dense 128B model with a 256k context window, handling instruction-following, reasoning,
and coding in a single set of weights. Mistral Medium 3.5 replaces its predecessor Mistral Medium 3.1 and Magistral in Le Chat. It also replaces Devstral 2 in our
coding agent Vibe. Concretely, expect better performance for instruct, reasoning and coding tasks in a new unified model in comparison with our previous released models.

Reasoning effort is configurable per request, so the same model can answer a quick chat reply or work through a complex agentic run. We trained the vision encoder from
scratch to handle variable image sizes and aspect ratios.

Find more information on our [blog](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5).

> [!Note]
> To speed up local inference using vLLM, check out our released [EAGLE model](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B-EAGLE).

## Key Features

Mistral Medium 3.5 includes the following architectural choices:

- **Dense 128B parameters**.
- **256k context length**.
- **Multimodal input**: Accepts both text and image input, with text output.
- **Instruct and Reasoning functionalities** with function calls (reasoning effort configurable per request).

Mistral Medium 3.5 offers the following capabilities:

- **Reasoning Mode**: Toggle between fast instant reply mode and reasoning mode, boosting performance with test-time compute when requested.
- **Vision**: Analyzes images and provides insights based on visual content, in addition to text.
- **Multilingual**: Supports dozens of languages, including English, French, Spanish, German, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, and Arabic.
- **System Prompt**: Strong adherence and support for system prompts.
- **Agentic**: Best-in-class agentic capabilities with native function calling and JSON output.
- **Large Context Window**: Supports a 256k context window.

We release this model under a **[Modified MIT License]((https://huggingface.co/mistralai/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE))**: Open-source license for both commercial and non-commercial use with exceptions for companies with large revenue.

## Recommended Settings

- **Reasoning Effort**:
  - `'none'` → Do not use reasoning
  - `'high'` → Use reasoning (recommended for complex prompts and agentic usage)
  Use `reasoning_effort="high"` for complex tasks and agentic coding.
- **Temperature**: 0.7 for `reasoning_effort="high"`. Temp between 0.0 and 0.7 for `reasoning_effort="none"` depending on the task.
  Generally, lower means answer that are more to the point and higher allows the model to be more creative. It is a good practice to try different values in order to
  improve the model performance to meet your demands. 

## Benchmarks

### Agentic Benchmarks

Mistral Medium 3.5 supersedes all our previous coding models, namely Devstral, across all benchmarks. It scores **91.4%** on τ³-Telecom and **77.6%** on SWE-Bench Verified. Due to its stronger agentic capabilities, Mistral Medium 3.5 replaces Devstral 2 in our coding agent, Vibe CLI.

![Mistral agentic benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image2.png)
![Mistral agentic benchmark SWE-bench](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image3.png)
![Mistral agentic vs competiting models benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image4.png)

### Instruction Following, Reasoning, and Coding Benchmarks

We compared Mistral Medium 3.5 with competing models on instruction following, reasoning (math), and coding benchmarks. Thanks to its unified capabilities, it achieves strong results across all these tasks and Mistral Medium 3.5 is now powering Le Chat.

![instruct reasoning and agentic benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image1.png)

## License

This model is licensed under a [Modified MIT License](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*