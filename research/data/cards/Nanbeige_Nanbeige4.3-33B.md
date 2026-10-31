---
license: apache-2.0
language:
- en
- zh
library_name: transformers
pipeline_tag: text-generation
tags:
- llm
- nanbeige
base_model:
- Nanbeige/Nanbeige4.3-33B-Base
---

<div align="center">
<img src="figures/nbg.png" width="200" alt="Nanbeige Logo">
</div>

# <span id="Introduction">1. Introduction</span>

In Nanbeige4.3, we take a foundational step toward pushing the boundaries of lightweight agents. Our strategy centers on building a high-capacity teacher agent first, which will subsequently anchor the distillation of advanced agentic capabilities into smaller models.

To this end, we first introduce Nanbeige4.3-33B, designed as the flagship teacher model for the Nanbeige4.3 series. Delivering state-of-the-art agentic performance among open models in the ~30B parameter class, Nanbeige4.3-33B excels at complex coding and professional cowork tasks. It not only offers a powerful, cost-effective option for immediate real-world deployment, but also lays the necessary foundation to power our upcoming small model distillation pipeline (e.g., for Nanbeige4.3-3B).


<div align="center">
<img src="figures/nanbeige43-benchmarks.png" width="1000">
</div>

# <span id="Model-Performance">2. Model Performance</span>

We compare Nanbeige4.3-33B with recently released frontier models at around the 30B-parameter scale: Qwen3.8-27B, Muse-Glimmer-30B, and Gemma4-31B. All models are evaluated at their highest thinking effort. For each benchmark, we use the same inference hyperparameters and harness across models.
<table>
  <thead>
    <tr>
      <th>Category</th><th>Benchmark</th><th>Nanbeige4.3-33B<sup>1</sup></th><th>Qwen3.8-27B</th><th>Muse-Glimmer-30B</th><th>Gemma4-31B</th>
    </tr>
  </thead>
  <tbody>
    <tr><td rowspan="8">Agentic Coding</td><td>Terminal-Bench 2.1<sup>2</sup></td><td><strong>80.9</strong></td><td>73.0</td><td>61.8</td><td>47.2</td></tr>
    <tr><td>Terminal-Bench 4.0<sup>3</sup></td><td><strong>23.8</strong></td><td>6.3</td><td>1.6</td><td>0.0</td></tr>
    <tr><td>DeepSWE<sup>3</sup></td><td><strong>65.5</strong></td><td>42.5</td><td>4.4</td><td>2.7</td></tr>
    <tr><td>SWE-Bench Pro<sup>3</sup></td><td>60.3</td><td><strong>61.7</strong></td><td>51.2</td><td>36.9</td></tr>
    <tr><td>SWE-Atlas-QnA<sup>4</sup></td><td><strong>50.8</strong></td><td>41.9</td><td>17.7</td><td>3.3</td></tr>
    <tr><td>NL2Repo<sup>5</sup></td><td><strong>53.0</strong></td><td>48.3</td><td>27.4</td><td>33.8</td></tr>
    <tr><td>Scicode</td><td><strong>52.6</strong></td><td>46.7</td><td>44.9</td><td>45.5</td></tr>
    <tr><td>SkillsBench</td><td><strong>61.1</strong></td><td>56.4</td><td>39.7</td><td>28.9</td></tr>
    <tr><td rowspan="9">Agentic Cowork</td><td>Automation Bench<sup>6</sup></td><td><strong>54.2</strong></td><td>38.3</td><td>15.2</td><td>9.7</td></tr>
    <tr><td>JobBench<sup>7</sup></td><td><strong>44.8</strong></td><td>34.5</td><td>16.6</td><td>9.0</td></tr>
    <tr><td>GDPval<sup>8</sup></td><td>84.8</td><td><strong>86.4</strong></td><td>75.8</td><td>71.4</td></tr>
    <tr><td>Claw-Eval<sub>pass^3</sub><sup>9</sup></td><td><strong>78.3</strong></td><td>75.2</td><td>57.3</td><td>44.2</td></tr>
    <tr><td>Toolathlon-Verified<sup>10</sup></td><td><strong>70.4</strong></td><td>68.5</td><td>47.2</td><td>27.8</td></tr>
    <tr><td>DeepPlanning<sup>12</sup></td><td><strong>63.3</strong></td><td>49.2</td><td>21.4</td><td>19.4</td></tr>
    <tr><td>EnterpriseOps-Gym<sup>12</sup></td><td><strong>41.0</strong></td><td>40.2</td><td>30.5</td><td>27.3</td></tr>
    <tr><td>YC-bench<sup>11</sup></td><td><strong>$1,025,437</strong></td><td>$641,290</td><td>$513,978</td><td>$265,152</td></tr>
    <tr><td>Tau3-Bench<sup>12</sup></td><td><strong>48.8</strong></td><td>48.5</td><td>33.7</td><td>18.6</td></tr>
    <tr><td rowspan="3">Reasoning</td><td>GPQA Diamond</td><td>89.5</td><td>89.2</td><td>83.5</td><td><strong>91.3</strong></td></tr>
    <tr><td>AIME 2026</td><td><strong>95.2</strong></td><td>94.5</td><td>94.7</td><td>89.2</td></tr>
    <tr><td>AA-LCR</td><td><strong>84.0</strong></td><td>82.0</td><td>83.3</td><td>72.0</td></tr>
  </tbody>
</table>

<small>
<sup>1</sup> Nanbeige4.3-33B is evaluated with <code>preserve_thinking=true</code> in the chat template.<br>
<sup>2</sup> Terminal-Bench 2.1 is evaluated using Terminus 2.<br>
<sup>3</sup> Terminal-Bench 4 and DeepSWE are evaluated using mini-swe-agent v2.4.6.<br>
<sup>4</sup> SWE-Atlas-QnA is evaluated using mini-swe-agent v2.4.6. Answers are evaluated against 1,304 task-specific rubrics using GPT-6 Sol as the judge, with medium reasoning effort.<br>
<sup>5</sup> NL2Repo is evaluated using Claude Code.<br>
<sup>6</sup> Automation Bench v1.0.6 includes 600 publicly released tasks.<br>
<sup>7</sup> JobBench is evaluated with the Claude Code harness equipped with a search tool.<br>
<sup>8</sup> GDPval is scored using revised rubrics.<br>
<sup>9</sup> Claw-Eval is evaluated exclusively on the Claw-Eval General subset (comprising 157 single-turn user interaction tasks).<br>
<sup>10</sup> Toolathlon-Verified sets no max_tokens limit for individual model requests.<br>
<sup>11</sup> YC-bench retains only the most recent 10 turns of user dialogue as historical context before each model call.<br>
<sup>12</sup> DeepPlanning, EnterpriseOps-Gym, Tau3-Bench are evaluated using their official repositories.<br>
</small>

Nanbeige4.3-33B leads on most of the benchmarks, showing strong performance in both agentic coding and cowork tasks. 
Beyond its breadth across benchmarks, Nanbeige4.3-33B shows strong performance on **agent tasks across a wide range of professions and industries**. For example, on JobBench, it outperforms the baseline in most of the 35 occupations evaluated.

<div align="center">
  <img src="figures/occupation.png" width="1000" alt="occupation">
</div>




# <span id="Quickstart">3. Quickstart</span>

The tokenizer provides a configurable chat template for reasoning and tool-use scenarios:

- `enable_thinking` controls whether the model generates reasoning for the current response. It is enabled by default; set it to `False` for non-thinking mode.
- `preserve_thinking` controls whether reasoning from previous assistant turns is retained in a multi-turn conversation. We recommend `False` for general chat and question answering, and `True` for multi-turn tool use, office tasks, and code-agent workflows.
- Passing `tools` enables the tool-use template. We recommend `tool_call_format="xml"` for the best tool-calling performance; `json` is also supported for compatibility.

The model supports a context length of up to 524,288 tokens (512K).

We recommend adjusting the inference settings according to the target scenario:

| Scenario | Temperature | Top_p | Max New Tokens |
|---|---:|---:|---:|
| Agentic and tool-use tasks | 1.0 | 0.95 | 65,536 |
| Reasoning and chat tasks | 0.6 | 0.95 | 262,144 |


You can run the model with Transformers, SGLang, or vLLM:

## Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = 'Nanbeige/Nanbeige4.3-33B'
tokenizer = AutoTokenizer.from_pretrained(
  model_id,
  use_fast=False,
  trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
  model_id,
  torch_dtype='auto',
  device_map='auto',
  trust_remote_code=True
)

messages = [{'role': 'user', 'content': 'Which number is bigger, 9.11 or 9.8?'}]
inputs = tokenizer.apply_chat_template(
  messages,
  add_generation_prompt=True,
  return_tensors='pt'
).to(model.device)
output_ids = model.generate(inputs, max_new_tokens=1024)
response = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True)
print(response)
```

## SGLang

```bash
MODEL_PATH=/path/to/your/Nanbeige4.3-33B
python -m sglang.launch_server \
  --model-path ${MODEL_PATH} \
  --host 0.0.0.0 \
  --port 8000 \
  --tp-size 4 \
  --mem-fraction-static 0.8 \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder
```

## vLLM

```bash
MODEL_PATH=/path/to/your/Nanbeige4.3-33B
vllm serve ${MODEL_PATH} \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.8 \
  --enable-auto-tool-choice \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_coder
```

# <span id="Contact">4. Contact</span>

If you have any questions, please open an issue in this repository or contact us at nanbeige@kanzhun.com.

We also welcome collaborations to build domain-specific and industry-focused agents, including joint work on data and training.

# <span id="Citation">5. Citation</span>

If you find our model useful or would like to use it in your own work, please cite this Hugging Face project:

```bibtex
@misc{nanbeige43chat2026,
  title        = {Nanbeige4.3-33B},
  author       = {Nanbeige Team},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/Nanbeige/Nanbeige4.3-33B}}
}
```
