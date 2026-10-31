---
license: other
license_name: muse-model-license
license_link: LICENSE.md
language:
- en
library_name: transformers
pipeline_tag: image-text-to-text
tags:
- facebook
- meta
- pytorch
- muse
- muse-spark
- unsloth
base_model:
- meta-models/Muse-Spark-Open-816B-A42B
---

# Read our How to [Run Muse Spark Open Guide!](https://unsloth.ai/docs/models/muse-spark-open)

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
    <a href="https://unsloth.ai/docs/models/muse-spark-open">
      <img src="https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/documentation%20green%20button.png" width="143">
    </a>
  </div>
</div>

---
## Muse Spark Open
**Authors**: Meta Superintelligence Labs  
**Model Release Date:** October 2026  
**License**: [Muse Model License](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md)

Muse Spark Open is an 816B total/42B active parameter open weights model with a context window of 1M tokens. Built for coding and agentic work, Muse Spark Open is natively multimodal. This open weights version has additional safety post-training to make it more robust against misuse as a standalone model without system guardrails.  We recommend deploying Muse Spark Open as part of a broader AI system, with additional guardrails suited to the specific use case.

The model can perform well across a wide variety of use cases including:

1. **Multi-Step Reasoning** \- chains reasoning over long horizons, sustaining coherent plans across complex, extended workflows.  
2. **End to End Agentic Task Completion** \- multi-step planning, sequential tool invocation, failure recovery, and long-horizon task execution, working within scaffolds, write and debug code, and resolve multi-turn requests from start to finish.  
3. **Coding Agents** \- writing, debugging, and resolving real-world software engineering tasks.  
4. **Tool Use** \- tool invocation across extended multi-turn workflows, diagnosing error and retrying with tool call failures  
5. **Multimodal Reasoning** \- interpreting screenshots, charts, documents, images, audio and video recordings, alongside conversation for agentic and information-rich environments.  
6. **Synthetic Data Generation** \- generating high-quality training data for downstream model development.  
7. **LLM-as-a-judge Evaluation** \- serving as an evaluator for other models' outputs.

#### Muse Spark Open Model Overview

| Name | Muse Spark Open |
| :---- | :---- |
| Model Provider | Meta Platforms, Inc. or Meta Platforms Ireland Limited  |
| Date of Release | October 15th, 2026 |
| License | Muse Model License |
| Parameters | 816B total / 42B active |
| Type | Mixture-of-Experts Transformer, with Perception Encoder |
| Context Length | 1M at inference |
| Vocabulary Size | 202,048 |
| Modalities | Input: Text \+ Image \+ Video \+ Audio  /  Output: Text  |
| Languages | Multilingual, trained on data from more than 100 languages |
| Recommended inference parameters | Temperature \= 1.0   Top\_p \= 1.0   Top\_k \= disabled It is recommended to use Reasoning Effort of high or xhigh for complex problem solving, coding, and agentic tasks. |
| Language Model | **Hidden Dimension:** 8192 **Token Embedding:** untied input/output embeddings, vocab × dim \= 202,048 × 8192 ≈ \~1.66B **Output layer (unembedding layer):**  vocab × dim \= 202,048 × 8192 ≈ \~1.66B **Number of Layers:** 62 **Gated Attention:** Yes (output gate and output norm on the attention block; QK-norm enabled) Number of Attention Heads: 128 for Q and 16 for KV (grouped-query attention) Head Dimension: 64 **Mixture of Experts:** Yes Number of Experts: 256 Experts Activated per Token: 8 (top-k routing) |
| Perception Encoder | **Architecture:** 1.8B param, 50 layers, 1536 hidden dim, 16 heads, 14x14 patch size, 4096 output dim Learned Absolute \+ 2D RoPE for positional embedding, LayerNorm \+ GELU for FFN Sparse attention with factor 4 (every 4th \+ last layer are full attention) |

#### Model Access and Best Practices

**Access via API**  
The model is available via API through third party inference providers.

**Open Weights on your own system**  
The weights are available for download through Hugging Face. The model is available in BF16 and NVFP4  versions. To run on your own system, the model requires a GPU with at least 700GB of VRAM for NVFP4 and 2TB for BF16. It also requires an inference deployment framework \- supported frameworks are SGLang, vLLM, Hugging Face, TensorRT-LLM, Unsloth and Llama.cpp. It is also optimized to run on two Mac Studios with M5 Ultra using MLX.

Please see the [developer documentation](https://dev.meta.ai/resources/blog/build-with-muse-spark-open) for more information on how to deploy and use the model.

**Inference Parameters**  
You can customize inference parameters to achieve the best performance for your use case.

* **Reasoning Effort:** Reasoning effort controls how much the model thinks before it responds. Set it with the reasoning\_effort request parameter, or with chat\_template\_kwargs={"reasoning\_effort": ...}, to low, medium, high, or xhigh. The default is xhigh. Use high or xhigh for complex problem solving, coding, and agentic tasks, and low or medium for faster, shorter responses. Any other value returns an error.  
* **Sampling Parameters:** The following settings are recommended for most deployments: temperature \= 1.0, top\_p \= 1.0, top\_k \= disabled

#### Training data

Training data includes text, images, audio, and video. It includes data drawn from public sources, crawled from the Internet, acquired from third parties, derived from Meta’s products and services, and synthetically generated, curated and enriched by external vendor networks and Meta personnel. Data curation methodologies include cleaning, processing, modifying, deduplication, and filtering, among others. 

#### Benchmarks

We compare Muse Spark Open to other leading open-weight models of similar size and architecture. For Muse Spark Open we use xhigh reasoning effort, temperature \= 1.0, top\_p=1.0, top\_k=disabled across benchmarks. 

| Benchmark | Muse  Spark Open (xhigh) | Inkling (xhigh) | Nemotron 3 Ultra (thinking on) | Beam | Mistral Large 4 | Qwen3.8-2.4T-A95B (xhigh) | GLM 5.3 (max) | Kimi K3 (max) |
| :---: | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **General** |  |  |  |  |  |  |  |  |
| **Artificial Analysis Intelligence Index** | 39 | 26 | 23 | \- | 38 | 40 | **45** | 44 |
| **Agentic** |  |  |  |  |  |  |  |  |
| **JobBench** | **61.8** | 31.1 | 27.2 | \- | \- | 52.7 | 61.4 | 54.3 |
| **MCP-Atlas** | **89.2** | 76.0 | 63.1 | 78.7 | \- | 84.5 | 84.2 | 82.3 |
| **GDPVal-AA v2** | 1401 | 1079 | 1016 | \- | 1424 | 1613 | **1653** | 1537 |
| **OSWorld Verified** | 80.4 | 40.1 | \- | **\-** | \- | \- | \- | **84.8** |
| **Toolathlon Verified** | 72.8 | 45.5 | 34.3 | **\-** | \- | 72.5 | 73.0 | **76.5** |
| **Knowledge & Reasoning** |  |  |  |  |  |  |  |  |
| **HLE-Diamond (no tools)** | **26.1** | 11.2 | 8.9 | \- | \- | 17.3 | 16.4 | 22.2 |
| **AA Omniscience** | **25** | 2 | 0 | 13 | \-5 | 4 | 14 | 20 |
| **SciCode** | 58.5 | 47.0 | 40.3 | 49.7 | 54.2 | 54.1 | 59.0 | **59.5** |
| **HLE (w/ tools)** | 61.0 | 46.0 | 37.4 | 51.2 | \- | 56.2 | **62.5** | 56.0 |
| **GPQA Diamond** | 89.0 | 87.2 | 86.7 | 90.5 | \- | **93.5** | 91.7 | **93.5** |
| **Coding** |  |  |  |  |  |  |  |  |
| **DeepSWE 1.1** Preferred harness | 60  | \- | \- | 44 | 62  | 57 | 67  | **68** |
| **SWE-Atlas-QnA** Preferred harness | 58  | \- | \- | 35  | 59  | 62  | 59  | **66**  |
| **Terminal-Bench 2.1** Terminus 2 agent | 76.4 | 55.1 | 53.9 | 80.1 | \- | 82.0 | 83.9 | **85.0** |
| **Multimodal** |  |  |  |  |  |  |  |  |
| **ZeroBench (w/ tools)** | **50.0** | 14.0 | \- | \- | \- | \- | \- | 41.0 |
| **BabyVision (w/ tools)** | 80.2 | 34.2 | \- | \- | \- | \- | \- | **85.7** |
| **SimpleVQA (w/ tools)** | **73.6** | 52.3 | \- | \- | \- | \- | \- | 71.9 |
| **WorldVQA (w/ tools)** | 49.4 | 18.0 | \- | \- | \- | \- | \- | **51.0** |
| **IntPhys2** | **68.3** | 55.2 | \- | \- | \- | \- | \- | 60.3 |
| **VideoMMEv2** | 61.5 | 36.9 | \- | \- | \- | \- | \- | **65.4** |
| **Safety** |  |  |  |  |  |  |  |  |
| **FORTRESS  adversarial (static)** lower is better | ARS: 5.8 ORS: 17.4 | ARS: 25.0 ORS: 7.4 | ARS: 26.4 ORS: 13.3 | \- | \- | ARS: 21.6 ORS: 12.8 | ARS: 28.2 ORS: 3.2 | ARS: 26.7 ORS: 2.7 |
| **StrongREJECT v2 (adaptive)** lower is better | **0.5** | 86.4 | 80.7 | \- | \- | 65.6 | 62.9 | 66.6 |

For more details about our evaluations, see [our report.](https://research.meta.ai/static/muse-spark-open-evaluation-methodology)

#### Safety and Preparedness 

We strongly recommend deploying Muse Spark Open as part of an AI system with guardrails tailored to your intended use cases. These system-level protections should balance helpfulness and safety and address safety and security risks, including those arising from integration with external tools.

Muse Spark Open has been evaluated across four complementary safety areas, and met our safety criteria for release based on model evaluations and an assessment of residual risks:

1. Content safety: Harmful-content generation and refusal behavior, alongside response quality and ideological balance.  
2. Agentic risk: Harmful or unauthorized actions when using tools or acting on users' behalf, including unsafe code execution and destructive changes in coding-agent workflows.  
3. Privacy: Evaluation of how the model handles personal and sensitive information, including inappropriate disclosure and information sharing when acting on users' behalf.  
4. Preparedness: Evaluation of chemical and biological, cyber, and loss-of-control risks in line with  the Meta Superintelligence Scaling Framework.  
   1. Cybersecurity: We tested it against internal and public cyber misuse benchmarks using adaptive attackers querying the model the way a developer would query an API model, with no system-level safeguards in place. The model refused 99.2% of jailbreaks on our internal benchmark and 94.8% when aggregating across PolyGuard (cyber subset), RedCode, and CyberBench 2024\. In the same setup, Kimi K3 refused only 75.5% and 70.2% respectively.  
   2. Chemical and biological: It showed strong refusal behavior on both single-turn and multi-turn benchmarks, refusing over 98% of harmful requests on SecureBio's BioTIER refusal benchmark and over 99% on our internal single-turn chemistry refusal benchmark. On newly developed internal multi-turn agentic benchmarks, it refused over 97% of harmful biology requests and 98% of harmful chemistry requests.  
   3. Loss of control: On our misalignment evaluations, the model showed low propensity for deceptive or unilateral harmful behavior, with a 98.1% honesty rate on the MASK benchmark and a 0% misbehavior rate on the Agentic Misalignment benchmark.

These evaluations characterized the released checkpoint under the tested conditions and do not cover every downstream configuration or use case. Downstream modifications could degrade safety, and results for the released checkpoint should not be assumed to apply to modified models.

#### Considerations and Limitations

Muse Spark Open is a technology that carries known and unknown risks. Testing conducted to date has not, and could not, cover all scenarios. Muse Spark Open must not be used in any manner that violates applicable laws or regulations (including trade compliance laws) or in any other way that is prohibited by the [Muse Model License](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md), including the Usage Policy.

**Limitations**

1. The model may produce inaccurate, biased, or objectionable responses to user prompts.  
2. While optimized for agentic tasks, the model may still make errors in multi-step reasoning, particularly in novel scenarios not well represented in training data.  
3. The model has not been evaluated on all languages contained in the pre-training data. Performance may degrade on languages outside the strongly supported set.  
4. Quantized inference may show minor quality differences in edge cases compared to full-precision.  
5. The model is not intended to be downloaded by or used by individuals under the age of 18\. Where deployed within systems that may be used by individuals under the age of 18, deployers are responsible for ensuring that any risks associated with such use by individuals under the age of 18 has been fully assessed and appropriately mitigated, and complies with all applicable laws.  
6. When using very short or low-resolution videos (a few seconds at around 100 px), the model may sometimes reply that it can't view the video. Use longer clips or higher resolution (448 px or more on the short side) for reliable results.

**Responsible Use**  
Developers should perform their own safety testing and tuning tailored to their specific applications and proposed languages. Our Usage Policy can be found in the Muse Model License [here](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md) and provides further information on intended and unintended uses. We recommend implementing additional guardrails (such as human-in-the-loop confirmation for irreversible actions) when deploying the model in agentic contexts where it can take real-world actions.

For user-facing applications, developers should avoid exposing raw chain-of-thought and apply appropriate safety checks to any reasoning summaries. Developers should also protect internal assistant messages from user manipulation and use layered safeguards against jailbreaks and other adversarial inputs.

**Where to send questions or comments about the model:** Please provide any feedback, comments or bug reports on the model through the Hugging Face page at [https\://huggingface.co/meta-models/](https://huggingface.co/meta-models/) or through email at [museoss@meta.com](mailto:museoss@meta.com). For more technical information about generation parameters and recipes for how to use Muse Spark Open in applications, please see the developer documentation.
