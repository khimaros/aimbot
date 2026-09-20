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
- Nanbeige/Nanbeige4-3B-Base
---
<div align="center">

<img src="figures/nbg.png" width="220" alt="Nanbeige Logo">
</div>



# Introduction

Nanbeige4.1-3B is built upon Nanbeige4-3B-Base and represents an enhanced iteration of our previous reasoning model, Nanbeige4-3B-Thinking-2511, achieved through further post-training optimization with supervised fine-tuning (SFT) and reinforcement learning (RL). As a highly competitive open-source model at a small parameter scale, Nanbeige4.1-3B illustrates that compact models can simultaneously achieve robust **reasoning**, **preference alignment**, and **effective agentic behaviors**.

<div align="center">

<img src="figures/model_performance_comparison.png">
</div>

Specifically, Nanbeige4.1-3B exhibits the following key strengths:

* **Strong Reasoning:** Nanbeige4.1-3B is capable of solving complex, multi-step problems through sustained and coherent reasoning within a single forward pass, and reliably produces correct final answers on challenging tasks such as LiveCodeBench-Pro, IMO-Answer-Bench, and AIME 2026 I.
* **Robust Preference Alignment:** Nanbeige4.1-3B achieves solid alignment performance, outperforming not only same-scale models such as Qwen3-4B-2507 and Nanbeige4-3B-2511, but also substantially larger models including Qwen3-30B-A3B and Qwen3-32B on Arena-Hard-v2 and Multi-Challenge.
* **Agentic Capability:** Nanbeige4.1-3B is the first general small model to natively support deep-search tasks and reliably sustain complex problem solving involving more than 500 rounds of tool invocations. It fills a long-standing gap in the small-model ecosystem where models are typically optimized for either general reasoning or agentic scenarios, but rarely excel at both.
  
> **Technical Report:** [Link](https://arxiv.org/abs/2602.13367)




# Performances

We evaluate Nanbeige4.1-3B across a broad and diverse set of benchmarks covering **general reasoning**, and **deep-search capabilities**. 

### General Reasoning Tasks

On general reasoning tasks including **code**, **math**, **science**, **alignment**, and **tool-use** benchmarks, Nanbeige4.1-3B not only significantly outperforms same-scale models such as **Qwen3-4B**, but also demonstrates overall superior performance compared to larger models including **Qwen3-30B-A3B-2507** and **Qwen3-32B**.


| Benchmark                   | Qwen3-4B-2507 | Qwen3-8B | Qwen3-14B | Qwen3-32B | Qwen3-30B-A3B-2507 | Nanbeige4-3B-2511 | **Nanbeige4.1-3B** |
| --------------------------- | ------------- | -------- | --------- | --------- | ------------------ | ----------------- | ------------------ |
| **Code**                    |               |          |           |           |                    |                   |                    |
| Live-Code-Bench-V6          | 57.4          |  49.4    |   55.9    | 55.7      | <u>66.0<u>         | 46.0              | **76.9**           |
| Live-Code-Bench-Pro-Easy    | 40.2             |   41.2   |   33.0    | 42.3      | <u>60.8<u>         | 40.2              | **81.4**           |
| Live-Code-Bench-Pro-Medium | 5.3             |   3.5    |    1.8    | 3.5       | 3.5                | <u>5.3<u>         | **28.1**           |
| **Math**                    |               |          |           |           |                    |                   |                    |
| AIME 2026 I                   | 81.46         | 70.42    | 76.46     | 75.83     | <u>87.30<u>        | 84.1              | **87.40**          |
| HMMT Nov                    | 68.33         |  48.33   |  56.67    | 57.08     | <u>71.25<u>        | 66.67             | **77.92**          |
| IMO-Answer-Bench            | 48.00         |   36.56  | 41.81     | 43.94     | **54.34**          | 38.25             | 53.38              |
| **Science**                 |               |          |           |           |                    |                   |                    |
| GPQA                        | 65.8          |   62.0   |    63.38  | 68.4      | 73.4               | <u>82.2<u>        | **83.8**           |
| HLE (Text-only)             | 6.72          | 5.28     |   7.00    | 9.31      | <u>11.77<u>        | 10.98             | **12.60**          |
| **Alignment**               |               |          |           |           |                    |                   |                    |
| Arena-Hard-v2               | 34.9          |  26.3    |   36.9    | 56.0      | <u>60.2<u>         | 60.0              | **73.2**           |
| Multi-Challenge             | 41.14         |  36.30   |   36.97   | 38.72     | <u>49.40<u>        | 41.20             | **52.21**          |
| **Tool Use**                |               |          |           |           |                    |                   |                    |
| BFCL-V4             | 44.87         |   42.20  |  45.14   |  47.90     |     48.6           | <u>53.8<u>        | **56.50**          |
| Tau2-Bench                 |  45.9        | 42.06    |  44.96    |    45.26  |  <u> 47.70<u>   |    41.77         |    **48.57**           |



### Deep Search Tasks

As a general small model, Nanbeige4.1-3B achieves deep-search performance comparable to specialized agents under 10B parameters. 
In contrast to existing small general models, which typically exhibit little to no deep-search capability, Nanbeige4.1-3B represents a substantial qualitative improvement over prior small general models.

#### Deep Search and Agent Benchmarks
| Model | xBench-DeepSearch-2505 | xBench-DeepSearch-2510 | Browse-Comp | Browse-Comp-ZH | GAIA (Text-only) | HLE | SEAL-0 |
|------|-------------------|-------------------|-------------|----------------|------------------|-----|--------|
| **Search-Specialized Small Agents** ||||||||
| MiroThinker-v1.0-8B | 61 | – | 31.1 | 40.2 | 66.4 | 21.5 | 40.4 |
| AgentCPM-Explore-4B | 70 | – | 25.0 | 29.0 | 63.9 | 19.1 | 40.0 |
| **Large Foundation Models (with Tools)** ||||||||
| GLM-4.6-357B | 70 | – | 45.1 | 49.5 | 71.9 | 30.4 | – |
| Minimax-M2-230B | 72 | – | 44.0 | 48.5 | 75.7 | 31.8 | – |
| DeepSeek-V3.2-671B | 71 | – | 67.6 | 65.0 | 63.5 | 40.8 | 38.5 |
| **Small Foundation Models (with Tools)** ||||||||
| Qwen3-4B-2507 | 34 | 5 | 1.57 | 7.92 | 28.33 | 11.13 | <u>15.74<u> |
| Qwen3-8B | 31 | 2 | 0.79 | 5.15 | 19.53 | 10.24 | 6.34 |
| Qwen3-14B | 34 | 9 | 2.36 | 7.11 | 30.23 | 10.17 | 12.64 |
| Qwen3-32B | <u>39<u> | 8 | <u>3.15<u> | <u>7.34<u> | 30.17 | 9.26 | 8.15 |
| Qwen3-30B-A3B-2507 | 25 | 10| 1.57 | 4.12 | <u>31.63<u> | <u>14.81<u> | 9.24 |
| **Ours (with Tools)** ||||||||
| Nanbeige4-3B-2511 | 33 | <u>11<u>  | 0.79 | 3.09 | 19.42 | 13.89 | 12.61 |
| **Nanbeige4.1-3B** | **75** | **39** | **19.12** | **31.83** | **69.90** | **22.29** | **41.44** |


## <span id="Inference">Quickstart</span>

For inference hyperparameters, we recommend the following settings:
* Temperature: 0.6
* Top-p: 0.95
* Repeat penalty: 1.0
* Max New Tokens: 131072

For the chat scenario:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(
  'Nanbeige/Nanbeige4.1-3B',
  use_fast=False,
  trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
  'Nanbeige/Nanbeige4.1-3B',
  torch_dtype='auto',
  device_map='auto',
  trust_remote_code=True
)
messages = [
  {'role': 'user', 'content': 'Which number is bigger, 9.11 or 9.8?'}
]
prompt = tokenizer.apply_chat_template(
  messages,
  add_generation_prompt=True,
  tokenize=False
)
input_ids = tokenizer(prompt, add_special_tokens=False, return_tensors='pt').input_ids
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=166101)
resp = tokenizer.decode(output_ids[0][len(input_ids[0]):], skip_special_tokens=True)
print(resp)
```

For the tool use scenario:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(
  'Nanbeige/Nanbeige4.1-3B',
  use_fast=False,
  trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
  'Nanbeige/Nanbeige4.1-3B',
  torch_dtype='auto',
  device_map='auto',
  trust_remote_code=True
)
messages = [
    {'role': 'user',  'content': 'Help me check the weather in Beijing now'}
]
tools = [{'type': 'function',
  'function': {'name': 'SearchWeather',
   'description': 'Find out the current weather in a place on a certain day.',
   'parameters': {'type': 'dict',
    'properties': {'location': {'type': 'string',
      'description': 'A city in China.'},
    'required': ['location']}}}}]
prompt = tokenizer.apply_chat_template(
  messages,
  tools,
  add_generation_prompt=True,
  tokenize=False
)
input_ids = tokenizer(prompt, add_special_tokens=False, return_tensors='pt').input_ids
output_ids = model.generate(input_ids.to('cuda'), max_new_tokens=512, eos_token_id=166101)
resp = tokenizer.decode(output_ids[0][len(input_ids[0]):], skip_special_tokens=True)
print(resp)
```

For the deep-search scenario:

* Inference Framework: [**miroflow-framework**](https://github.com/MiroMindAI/MiroThinker)!
* Switch tokenizer configuration to **tokenizer_config_search.json**
* Tools Configuration:

| Server                      | Description                                                                 | Tools Provided                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| tool-python                 | Execution environment and file management ([E2B sandbox](https://e2b.dev/)) | create_sandbox, run_command, run_python_code, upload_file_from_local_to_sandbox, download_file_from_sandbox_to_local, download_file_from_internet_to_sandbox |
| search_and_scrape_webpage   | Google search via [Serper API](https://google.serper.dev)                   | google_search                                                                 |
| jina_scrape_llm_summary     | Web scraping with LLM-based information extraction with [Jina](https://r.jina.ai) | scrape_and_extract_info                                                       |

* Summary model: Qwen3-14B-thinking
* Temperature: 1.0
* Note, access to HuggingFace has been explicitly disabled in these tools.

# <span id="Limitations">Limitations</span>

While we place great emphasis on the safety of the model during the training process, striving to ensure that its outputs align with ethical and legal requirements, it may not completely avoid generating unexpected outputs due to the model's size and probabilistic nature. These outputs may include harmful content such as bias or discrimination. Please don't propagate such content. We do not assume any responsibility for the consequences resulting from the dissemination of inappropriate information.
<br>

# <span id="Limitations">Citation</span>
If you find our model useful or want to use it in your projects, please cite as follows:
```
@misc{yang2026nanbeige413bsmallgeneralmodel,
      title={Nanbeige4.1-3B: A Small General Model that Reasons, Aligns, and Acts}, 
      author={Chen Yang and Guangyue Peng and Jiaying Zhu and Ran Le and Ruixiang Feng and Tao Zhang and Xiyun Xu and Yang Song and Yiming Jia and Yuntao Wen and Yunzhi Xu and Zekai Wang and Zhenwei An and Zhicong Sun and Zongchao Chen},
      year={2026},
      eprint={2602.13367},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2602.13367}, 
}
```
<br>

# <span id="Limitations">Contact</span>
If you have any questions, please raise an issue or contact us at nanbeige@kanzhun.com.
<br>