---
license: mit
tags:
- unsloth
- deepseek_v4
- deepseek
base_model:
- deepseek-ai/DeepSeek-V4-Pro-0813
base_model_relation: quantized
---
## Read our How to [Run DeepSeek-V4 Guide!](https://unsloth.ai/docs/models/deepseek-v4)
<p style="margin-top: 0;margin-bottom: 0;">
    <em><a href="https://unsloth.ai/docs/basics/unsloth-dynamic-v2.0-gguf">Unsloth Dynamic 2.0</a> achieves superior accuracy & outperforms other leading quants.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; ">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/models/deepseek-v4">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
  </div>
    <ul style="margin: 0;">
    <li>See our <a href="https://unsloth.ai/docs/models/deepseek-v4">DeepSeek-V4 guide</a> for quantization analysis and run instructions.</li>
    <li>DeepSeek-V4-Pro-0813 is a 1.57T parameter model with 48B active parameters per token, so it needs substantially more memory than DeepSeek-V4-Flash-0731.</li>
    <li>For DeepSeek-V4-Flash-0731 GGUFs, see <a href="https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF">unsloth/DeepSeek-V4-Flash-0731-GGUF</a>.</li>
  </ul>

Quants are uploaded to this repository as they finish converting.

---
# DeepSeek-V4-Pro-0813

<div align="center">
  <img src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/logo.svg?raw=true" width="60%" alt="DeepSeek-V4" />
</div>
<hr>
<div align="center" style="line-height: 1;">
  <a href="https://www.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/badge.svg?raw=true" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://chat.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-DeepSeek%20V4-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/deepseek-ai" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-DeepSeek%20AI-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://twitter.com/deepseek_ai" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-deepseek_ai-white?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<p align="center">
  <a href="https://arxiv.org/abs/2606.19348"><b>Technical Report</b>👁️</a>
</p>

## Introduction

**DeepSeek-V4-Pro-0813** is the official release of **DeepSeek-V4-Pro**, superseding the preview version, with greatly enhanced agentic capabilities and performance improvements that are especially pronounced in production environments. It is built on the DeepSeek-V4-Pro (Preview) model structure, with a DSpark speculative decoding module attached.

DeepSeek-V4-Pro-0813 outperforms DeepSeek-V4-Pro (Preview) on the benchmarks listed below, and is broadly competitive with the strongest proprietary models available.

<div align="center">

| Benchmark | DeepSeek-V4-Pro-0813 | DeepSeek-V4-Flash-0731 | DeepSeek-V4-Pro (Preview) | DeepSeek-V4-Flash (Preview) | GLM-5.2 | Kimi K3 | Opus-4.8 | Fable-5 (w/ fallback) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| HLE (wo / w tools) | 42.7 / 60.0 | 37.8 / 51.5 | 37.7 / 48.2 | 34.8 / 45.1 | 40.5 / 54.7 | 43.5 / 56.0 | 49.8 / 57.9 | 53.3 / 63.0 |
| Terminal Bench 2.1 | 87.9 | 82.7 | 72.1 | 61.8 | 81.0 | 88.3 | 85.0 | 88.0 |
| NL2Repo | 61.5 | 54.2 | 38.5 | 39.4 | 48.9 | - | 69.7 | - |
| Cybergym | 83.3 | 76.7 | 52.7 | 38.7 | - | 80.0 | 78.3 | 83.1 |
| DeepSWE | 62.7 | 54.4 | 12.8 | 7.3 | 46.2 | 67.5 | 58.0 | 70.0 |
| Toolathlon-Verified | 74.1 | 70.3 | 55.9 | 49.7 | 59.9 | 76.5 | 76.2 | 77.9 |
| Agents' Last Exam | 25.7 | 25.2 | 16.5 | 15.8 | 23.8 | 27.6 | 25.7 | - |
| AutomationBench (Public) | 31.8 | 25.1 | 12.8 | 10.8 | 12.9 | 30.8 | 27.2 | 29.1 |
| DSBench-FullStack † | 71.1 | 68.7 | 41.8 | 37.0 | 61.8 | 73.7 | 71.6 | 77.2 |
| DSBench-Hard † | 67.2 | 59.6 | 31.1 | 25.8 | 54.5 | 63.0 | 71.7 | 68.3 |

</div>

Notes:

1. For the code-agent tasks among the public benchmarks above, DeepSeek-V4-Pro-0813 is evaluated with the minimal mode of DeepSeek Harness as the agent framework, using the `max` reasoning effort level with `temperature = 1.0, top_p = 0.95`.
2. † DSBench-FullStack is an internal full-stack development test set; DSBench-Hard is an internal test set of difficult coding-agent problems.

## Chat Template

This release does not include a Jinja-format chat template. Instead, we provide a dedicated `encoding` folder with Python scripts and test cases demonstrating how to encode messages in OpenAI-compatible format into input strings for the model, and how to parse the model's text output. Please refer to the [`encoding`](encoding/README.md) folder for full documentation.

The `reasoning_effort` parameter now supports three levels — `low`, `high`, and `max` — which control how much deliberation the model spends before answering.

A brief example:

```python
from encoding_dsv4 import encode_messages, parse_message_from_completion_text

messages = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hello! I am DeepSeek.", "reasoning_content": "thinking..."},
    {"role": "user", "content": "1+1=?"}
]

# messages -> string
prompt = encode_messages(messages, thinking_mode="thinking", reasoning_effort="max")

# string -> tokens
import transformers
tokenizer = transformers.AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V4-Pro-0813")
tokens = tokenizer.encode(prompt)
```

## License

This repository and the model weights are licensed under the [MIT License](LICENSE).

## Citation

```
@misc{deepseekai2026deepseekv4,
      title={DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence},
      author={DeepSeek-AI},
      year={2026},
}
```

## Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](service@deepseek.com).
