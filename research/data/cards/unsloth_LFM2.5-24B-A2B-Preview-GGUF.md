---
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
language:
- en
- ar
- zh
- fr
- de
- ja
- ko
- es
- pt
- it
pipeline_tag: text-generation
tags:
- liquid
- lfm2.5
- edge
- moe
- unsloth
base_model: LiquidAI/LFM2.5-24B-A2B
---

# Run and train LFM2.5 via the [Unsloth Desktop app](https://unsloth.ai/docs/desktop)
<div>
  <p style="margin: 0 0 0px 0; margin-top: 0px;">
    <em><a href="https://unsloth.ai/docs/basics/dynamic-3.0-ggufs">Unsloth Dynamic 3.0</a> achieves superior accuracy & outperforms other leading quants.</em>
  </p>
  <div style="display: flex; gap: 5px; align-items: center; margin-bottom: 0px;">
    <a href="https://github.com/unslothai/unsloth/">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/unsloth%20new%20logo.png" width="133">
    </a>
    <a href="https://discord.gg/unsloth">
      <img src="https://github.com/unslothai/unsloth/raw/main/images/Discord%20button.png" width="173">
    </a>
    <a href="https://unsloth.ai/docs/">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>

<div align="center">
  <img 
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png" 
    alt="Liquid AI" 
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> • 
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> • 
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# LFM2.5-24B-A2B-Preview

LFM2.5-24B-A2B-Preview is a 24B-parameter reasoning model with only 2B active parameters, built for **fast, private agents on-device**. It is the largest and final model in the LFM2.5 family, and builds on [LFM2-24B-A2B](https://huggingface.co/LiquidAI/LFM2-24B-A2B) with a 128K context window, scaled-up pre-training, and large-scale reinforcement learning.

- **Best-in-class agent**: Agentic performance [TBD: on par with / close to] Qwen3.6-35B-A3B, a model with ~50% more total and active parameters, scoring [TBD: X on agentic benchmark versus Y].
- **Reasoning at MoE speed**: Always thinks before it answers. With only 2B active parameters per token, each reasoning token is cheap.
- **Efficient inference**: [TBD: X tok/s on edge device] and up to [TBD: X] output tok/s on a single H100.

Find more information about LFM2.5-24B-A2B-Preview in our [blog post](https://www.liquid.ai/blog/lfm2-5-24b-a2b).

> [!NOTE]
> 💻 **Demo**: Our open-source desktop agent, [LocalCowork](https://github.com/Liquid4All/cookbook/tree/main/examples/localcowork), runs on LFM2.5-24B-A2B-Preview: a single laptop, 67 tools across 13 MCP servers, no cloud, no API keys, no data leaving the machine.

## 🗒️ Model Details

| Model                                                                        | Parameters      | Description                            |
| ---------------------------------------------------------------------------- | --------------- | -------------------------------------- |
| [LFM2.5-24B-A2B-Base](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-Base)   | 24B (2B active) | Pre-trained base model for fine-tuning |
| **[LFM2.5-24B-A2B-Preview](https://huggingface.co/lq-preview/LFM2.5-24B-A2B-Preview)**         | 24B (2B active) | Post-trained for agentic workloads     |

LFM2.5-24B-A2B-Preview is a general-purpose text-only reasoning model with the following features:

- **Total parameters**: 24.0B
- **Active parameters**: 2.45B
- **Number of layers**: 40 (30 double-gated short convolution blocks + 10 GQA)
- **Experts**: 64 per MoE block, top-4 routing
- **Training budget**: 33 trillion tokens
- **Vocabulary size**: 128,000
- **Context length**: 131,072 tokens
- **Languages**: [TBD]
- **Generation parameters**:
  - `temperature: [TBD]`
  - `top_k: [TBD]`
  - `repetition_penalty: [TBD]`


We recommend using it for agents that need to reason, call tools, and run reliably on your device. [TBD: other recommended use cases]. It is not recommended for [TBD].

### Chat Template

LFM2.5 uses a ChatML-like format. See the [Chat Template documentation](https://docs.liquid.ai/lfm/key-concepts/chat-template) for details. Example:

```
<|startoftext|><|im_start|>system
You are a helpful assistant trained by Liquid AI.<|im_end|>
<|im_start|>user
What is C. elegans?<|im_end|>
<|im_start|>assistant
```

You can use [`tokenizer.apply_chat_template()`](https://huggingface.co/docs/transformers/en/chat_templating#using-applychattemplate) to format your messages automatically.

> [!TIP]
> 💡 **Note**: Unlike LFM2-24B-A2B, LFM2.5-24B-A2B-Preview is a pure reasoning model that always thinks before it answers. It adds a `<think>` tag directly in the [chat template](https://huggingface.co/lq-preview/LFM2.5-24B-A2B-Preview/blob/main/chat_template.jinja#L124) when starting an assistant answer.

### Tool Use

LFM2.5 supports function calling in four steps:

1. **Function definition**: Provide the list of tools as a JSON object in the system prompt, or use [`tokenizer.apply_chat_template()`](https://huggingface.co/docs/transformers/en/chat_extras#passing-tools) with `tools=...`.
2. **Function call**: By default, LFM2.5 writes Pythonic function calls (a Python list between `<|tool_call_start|>` and `<|tool_call_end|>` special tokens), as the assistant answer. You can override this behavior by asking the model to output JSON function calls in the system prompt.
3. **Function execution**: Execute the call and return the result with the `tool` role.
4. **Final answer**: LFM2.5 interprets the tool output and returns a plain-text answer addressing the original prompt.

See the [Tool Use documentation](https://docs.liquid.ai/lfm/key-concepts/tool-use) for the full guide. Example:

```
<|startoftext|><|im_start|>system
List of tools: [{"name": "get_candidate_status", "description": "Retrieves the current status of a candidate in the recruitment process", "parameters": {"type": "object", "properties": {"candidate_id": {"type": "string", "description": "Unique identifier for the candidate"}}, "required": ["candidate_id"]}}]<|im_end|>
<|im_start|>user
What is the current status of candidate ID 12345?<|im_end|>
<|im_start|>assistant
<|tool_call_start|>[get_candidate_status(candidate_id="12345")]<|tool_call_end|>Checking the current status of candidate ID 12345.<|im_end|>
<|im_start|>tool
[{"candidate_id": "12345", "status": "Interview Scheduled", "position": "Clinical Research Associate", "date": "2023-11-20"}]<|im_end|>
<|im_start|>assistant
The candidate with ID 12345 is currently in the "Interview Scheduled" stage for the position of Clinical Research Associate, with an interview date set for 2023-11-20.<|im_end|>
```

### Training

LFM2.5-24B-A2B-Preview keeps the LFM2-24B-A2B architecture: 40 layers, 64 experts per MoE block with top-4 routing, and the same hybrid of gated short convolutions and GQA. The two architectural changes are a context window extended from 32K to 128K, and a vocabulary doubled from 65K to 128K tokens with an [in-place tokenizer expansion](https://www.liquid.ai/blog/tokenizer-expansion) for better non-Latin tokenization.

- **Pre-training** was scaled up from ~17T to ~33T tokens.
- **Mid-training** has two phases: 2T tokens at 32K context on curated data weighted toward reasoning, math, code, instruction following, and multilingual text, then 300B tokens at 128K context weighted toward long-context data. Tool calls and multi-turn trajectories appear throughout both phases.
- **Post-training** turns the base model into an agent in five stages: supervised fine-tuning, teacher specialization, two multi-domain on-policy distillation stages (one non-agentic, one agentic), and agentic reinforcement learning.

## Citation

```bibtex
@article{liquidAI202624BA2B,
  author  = {Liquid AI},
  title   = {LFM2.5-24B-A2B-Preview: Built for Fast On-Device Agents},
  journal = {Liquid AI Blog},
  year    = {2026},
  note    = {www.liquid.ai/blog/lfm2-5-24b-a2b},
}
```

```bibtex
@article{liquidai2025lfm2,
  title   = {LFM2 Technical Report},
  author  = {Liquid AI},
  journal = {arXiv preprint arXiv:2511.23404},
  year    = {2025}
}
```
