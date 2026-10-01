---
license: apache-2.0
base_model: meta-models/Muse-Glimmer-30B
pipeline_tag: image-text-to-text
tags:
- gguf
---
# Muse Glimmer Model Card

**Authors:** Meta Superintelligence Lab  
**Model Release Date:** August 2026  
**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

> [!NOTE]
> This repo contains GGUF conversions of [`meta-models/Muse-Glimmer-30B`](https://huggingface.co/meta-models/Muse-Glimmer-30B) for [llama.cpp](https://github.com/ggml-org/llama.cpp): two quantized text builds, a perception encoder for image input, and a DFlash drafter for speculative decoding.
> Everything you need to install, download and serve them is on this page. No bf16 GGUF is published here — use the [base repo](https://huggingface.co/meta-models/Muse-Glimmer-30B) if you need full precision.

Muse Glimmer is a 30-billion-parameter causal language model with a dedicated perception encoder, distilled from Muse Spark and purpose-built for autonomous agentic tasks on consumer hardware. The model integrates multi-step reasoning, reliable tool use, multimodal understanding, and failure recovery into a single model that runs locally without requiring cloud infrastructure or network access.

---

> [!IMPORTANT]
> **You need llama.cpp build `b10353` or newer.** Muse Glimmer support was merged on 10 Aug 2026 ([#26841](https://github.com/ggml-org/llama.cpp/pull/26841), `62bf73d`) and first shipped in release **`b10353`**. Releases **`b10344` and older do not register the architecture at all** and will refuse to load these files.
>
> Check what you have before anything else:
>
> ```bash
> ./llama-cli --version     # build number must be >= 10353
> ```
>
> If you are building from source, `master` works, and you can confirm the checkout directly:
>
> ```bash
> grep -c LLM_ARCH_MUSE_GLIMMER src/llama-arch.cpp     # expect >= 1
> ```
>
> `0` means your checkout predates Muse Glimmer support.

## Files

| File | Size | What it is |
|---|---|---|
| `Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf` | 16.8 GB | Text model — **start here**, fits 24 GB VRAM |
| `Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf` | 19.7 GB | Text model, higher-quality build for 32 GB VRAM |
| `mmproj-Muse-Glimmer-30B-Q4_K_M.gguf` | 1.4 GB | Perception encoder — **required for image input** |
| `dflash-Muse-Glimmer-30B-Q4_K_M.gguf` | 1.6 GB | DFlash drafter — optional, for speculative decoding |

Both text builds are text-only on their own; the two companions are additive. No bf16 GGUF is published — use the [base repo](https://huggingface.co/meta-models/Muse-Glimmer-30B) if you need full precision.

Rough total memory (weights plus a working context):

| Build | text only | + vision | + vision + drafter |
|---|---|---|---|
| `17gb` | ~17 GB | ~19 GB | ~20 GB |
| `dynamic` | ~20 GB | ~22 GB | ~23 GB |

## Get llama.cpp

Download a [release](https://github.com/ggml-org/llama.cpp/releases) tagged `b10353` or later, or build from source:

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

cmake -B build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build build --config Release -j \
    --target llama-cli llama-mtmd-cli llama-server
```

Drop `-DGGML_CUDA=ON` for CPU-only. On Apple Metal omit it as well — Metal is on by default. On Debian/Ubuntu you may first need `apt-get install -y build-essential cmake curl libcurl4-openssl-dev`.

## Download the weights

```bash
pip install huggingface_hub

hf download meta-models/Muse-Glimmer-30B-GGUF \
    --local-dir Muse-Glimmer-30B-GGUF \
    --include "Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf" \
    --include "mmproj-Muse-Glimmer-30B-Q4_K_M.gguf"
```

Swap in `Muse-Glimmer-30B-KQuant-Dynamic-Q4_K_XL.gguf` for the larger build, and add `--include "dflash-Muse-Glimmer-30B-Q4_K_M.gguf"` for speculative decoding.

## Run

### `llama-server`

```bash
./build/bin/llama-server \
    -m       Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf \
    --mmproj Muse-Glimmer-30B-GGUF/mmproj-Muse-Glimmer-30B-Q4_K_M.gguf \
    -a muse-glimmer-30B \
    -ngl 99 -c 131072 -np 4 \
    --host 127.0.0.1 --port 8080 \
    --jinja \
    --temp 1.0 --top-p 0.95 --top-k 64
```

Check it:

```bash
curl -s http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"muse-glimmer-30B",
       "messages":[{"role":"user","content":"What is 17 * 23? Reply with just the number."}]}' \
| python3 -c "import json,sys; m=json.load(sys.stdin)['choices'][0]['message']; \
print('content  :', m['content']); print('reasoning:', len(m.get('reasoning_content') or ''), 'chars')"
```

You should get the answer in `content` and the thinking separately in `reasoning_content`. If `content` instead begins with `to=self<|message|>`, your build predates the chat parser — see the version note above.

Add speculative decoding with the drafter:

```bash
    -md Muse-Glimmer-30B-GGUF/dflash-Muse-Glimmer-30B-Q4_K_M.gguf -ngld 99
```

Same outputs, faster decode, ~1.6 GB extra. A `[spec] failed to measure draft model memory` warning at startup is harmless — the draft model loads and serves normally afterwards.

### `llama-cli` (text)

```bash
./build/bin/llama-cli \
    -m Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf \
    -ngl 99 -c 32768 \
    --jinja \
    --temp 1.0 --top-p 0.95 --top-k 64
```

For a single non-interactive answer add `-st` / `--single-turn`; without it `llama-cli` waits for input and can look like it has hung.

### `llama-mtmd-cli` (images)

Images need `llama-mtmd-cli`, not `llama-cli`:

```bash
./build/bin/llama-mtmd-cli \
    -m       Muse-Glimmer-30B-GGUF/Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf \
    --mmproj Muse-Glimmer-30B-GGUF/mmproj-Muse-Glimmer-30B-Q4_K_M.gguf \
    -ngl 99 -c 32768 \
    --jinja \
    --temp 1.0 --top-p 0.95 --top-k 64 \
    --image photo.png -p "Describe this image."
```

Both CLIs print the thinking trace inline — `llama-cli` brackets it with `[Start thinking]` / `[End thinking]`, `llama-mtmd-cli` shows the raw channel markers. Use `llama-server` if you want the two separated into `content` and `reasoning_content`.

## Things that will otherwise cost you an hour

### `--jinja` is not optional

The chat template is embedded in these GGUFs, byte-identical (9,992 chars) to [`chat_template.jinja`](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/chat_template.jinja) in the base repo. `--jinja` alone is enough — there is no separate template file to pass and `--chat-template-file` is not needed. Without `--jinja`, `llama-mtmd-cli` aborts with `this custom template is not supported, try using --jinja`.

This template normalizes an OpenAI-style `Reasoning effort: <level>` line in your system prompt to the `Reasoning strength: <level>` the model was trained on, and will not append a second reasoning-strength line when your system prompt already sets one. Earlier GGUFs shipped a template that skipped both, which could leave a conflicting `Reasoning strength: high.` in the prompt — re-download if you pulled before this fix.

### Never stop on `<|eom|>`

The stop tokens are `<|end_of_text|>` (200001) and `<|eot|>` (200008) — that is, `eos_token_id = [200001, 200008]`. `<|eom|>` marks end-of-*message*, not end-of-turn: the turn continues after it. Stopping on `<|eom|>` collapses parallel tool calling. If you are writing your own client or adding custom stop strings, leave `<|eom|>` alone.

### `-c` is split across slots

`llama-server` divides `-c` across `-np` slots, so **a single request gets `-c / -np`**. Check `n_ctx_slot` in the startup log — that number, not `-c`, bounds one generation.

Muse Glimmer reasons at length, so this matters more than it looks. Nothing errors when a generation runs out of context: the request simply produces no answer. If you are running an eval, that silently reads as a wrong answer rather than as a failure, so the cost shows up as a lower score with nothing in the logs to explain it. For evaluation, give each slot the full trained context by scaling `-c` **with** `-np`:

```bash
    -c 524288 -np 4        # 131,072 per slot, still 4-way concurrent
```

KV cache stays cheap — GQA with 2 KV heads plus sliding-window attention on 3 of every 4 layers — so this costs a few GB, not tens.

### Reasoning cannot be switched off

The template opens the thinking channel unconditionally, so `--reasoning off`, `--reasoning on` and `"reasoning_effort": "none"` all have no effect. What you control is *how much*, via the `reasoning_strength` template variable — `low` / `medium` / `high` / `xhigh`, defaulting to `high`:

```bash
    --chat-template-kwargs '{"reasoning_strength":"xhigh"}'     # server-wide
```

```json
{"chat_template_kwargs": {"reasoning_strength": "low"}}
```

To hard-cap thinking tokens use `--reasoning-budget N`. Thinking is routed into `reasoning_content` by default, so no extra flag is needed.

**Sampling defaults.** temperature 1.0, top_p 0.95, top_k 64 — restated under [Best Practices](#best-practices).

## GGUF metadata

These files declare `general.architecture = muse-glimmer`, so metadata keys are namespaced `muse-glimmer.*` — `muse-glimmer.context_length`, and so on. Tooling that looks for a `llama.*` namespace will not find them.

---

## Muse Glimmer-30B Model Overview

Building effective agents requires key capabilities working together to achieve the user’s goals. Muse Glimmer is trained and evaluated on these capabilities:

* **End-to-end Agentic Task Completion.** Muse Glimmer achieves strong success rates on full-task benchmarks including DeepSearch QA, MCP-Atlas, 𝛕3\-Bench and SWE-Bench, which measure its ability to work within scaffolds, write and debug code, and resolve multi-turn requests from start to finish.  
* **Reliable Tool Use.** The model handles a wide range of function calls, invoking tools with precise schemas throughout extended workflows.  
* **Multi-Step Reasoning.** Muse Glimmer chains reasoning over long horizons, sustaining coherent plans across complex, extended workflows.  
* **Failure Recovery.** When a tool call fails or returns an unexpected result, the model diagnoses the error and retries rather than halt.  
* **Multimodal Input and Reasoning.** Through a dedicated perception encoder, the model accepts interleaved text and images. This enables agents to interpret screenshots, charts, and documents alongside conversation.  
* **Scaffold Compatibility.** Muse Glimmer works across OpenClaw, Hermes Agent, and other agentic orchestration patterns.  
* **Controllable Effort.** The model supports different reasoning strengths to select the right balance between quality and speed.  
* **Multilingual.** Muse Glimmer is trained on data from more than 100 languages.

| Model Architecture | Dense Causal Transformer with Perception Encoder |
| :---- | :---- |
| **Total Parameters** | \~29.6B |
| **Language Model** |  |
|    **Architecture** | Dense Causal Transformer |
|    **Number of Parameters** | 29.6B (including vision encoder) |
|    **Hidden dimension** | 6656 |
|    **Layers** | 52 |
|    **Attention pattern** | \[Local, Local, Local, Global\] repeating |
|    **Sliding window size** | 2048 |
|    **Gated attention** | Yes |
|    **Attention heads (Q / KV)** | 32 / 2 (GQA ratio 16:1) |
|    **Head dimension** | 128 |
|    **FFN type** | SwiGLU |
|    **FFN intermediate dimension** | 19,968 |
|    **Position encoding** | RoPE (θ \= 500,000), local layers only |
| **Perception [encoder](https://arxiv.org/abs/2504.13181)** | \~1.8B param ViT-G/14, 50 layers, width 1536, patch size 14 |
| **Vocabulary size** | 202,048 |
| **Tokenizer** | 200,000 BPE tokens \+ 2,048 special tokens |
| **Max visual tokens per image** | 4,096 |
| **Context length** | 131,072+ |
| **Supported modalities** | Input: text \+ image, Output: text |
| **Training Data** | Multimodal content sourced from publicly available data, data provided by third parties and information from Meta's products and services, curated and enriched by external vendor networks and Meta personnel. |
| **Knowledge cutoff** | January 4, 2026 |

## Optimized for Local Deployments

Muse Glimmer was optimized for local deployment, and designed to run at practical speeds on consumer hardware without sacrificing quality.

**Fitting the Model on Your Device.** We use quantization techniques to compress the model's weights to approximately 4-bit precision, shrinking the language model to under 20 GB. This leaves enough headroom for the model's KV cache, the perception encoder for image understanding, and the speculative decoding drafter to run simultaneously within a 24 GB or 32 GB envelope. Critically, we validated that this compression introduces minimum to no degradation on agentic tasks. 

|  | Full Precision | K-Quant-Dynamic | K-Quant-17GB |
| :---- | :---: | :---: | :---: |
| % Degradation\* | \- | 0.2% | 1.0% |
| Target Hardware | 64GB VRAM | 32GB VRAM | 24GB VRAM |

\* Degradation measured using an average on accuracy metrics across 15 common benchmarks

**Faster Generation Through Speculative Decoding** Muse Glimmer ships with a lightweight "drafter" model based on [DFlash](https://arxiv.org/abs/2602.06036), a small companion network that proposes entire blocks of tokens at once. The DFlash block-diffusion model predicts entire blocks of 16 tokens in a single forward pass. The main model then verifies these proposals in parallel, accepting correct tokens and correcting wrong ones. This technique lets Muse Glimmer generate text significantly faster than standard token-by-token generation while producing identical output quality. We provide quantized drafter versions to incur a smaller memory overhead in the release.

| Component | Setting |
| :---- | :---- |
| Draft layers | 5 |
| Block size | 16 |
| Attention | Sliding-window, 2048, all layers |
| Attention heads | 32 query / 8 KV (GQA) |
| Sequence length | 131,072 |
| Hidden-feature layers | 5, uniform over target: {1, 13, 25, 37, 49} of 52 |

We measure the speed of our K-Quant-17GB model alongside the quantized DFlash drafter on MacBook M4-Max, M5-Max and on an Nvidia RTX-5090. The model is fast enough for fluid conversation and real-time agent interaction, all running entirely on your device.

| GPU | Baseline No-speculation (tok/s) | Avg\* with DFlash Speculation  (tok/s) | Speedup |
| :---- | :---: | :---: | :---: |
| **Nvidia RTX 5090** | 74.9 | 233.4 | 3.1x |
| **Apple M4 Max** | 23.7 | 37.8 | 1.5x |
| **Apple M5 Max** | 26.6 | 50.2 | 1.8x |

\* Average across a diverse prompt set. Measurements done with batch size 1 and greedy decoding. M4/M5 measurements were done using ExecuTorch, and RTX using llama.cpp.

## Benchmarks

We evaluated Muse Glimmer across a broad range of benchmarks to assess the diverse capabilities required for effective autonomous agent behavior. Compared with Gemma4-31B and Qwen3.6-27B, Muse Glimmer performs strongly for its size class on several widely used LLM benchmarks.

| Category | Benchmark | Muse Glimmer-30B High Reasoning | Gemma4-31B Thinking Mode | Qwen3.6-27B Thinking Mode |
| :---- | :---- | :---: | :---: | :---: |
| *General Agentic* |  MCP Atlas (Public) | **75.5** | 54.2 | 62.5 |
|  | DeepSearch QA | **74.6** | 61.7 | 71.1 |
|  |  𝛕3\-Banking | **23.5** | 15.1 | 16.7 |
|  | WildClawBench | **47.6** | 37.6 | 43.2 |
|  | GDPVal-AA v2 | 953 | 811 | **1141** |
|  | Gaia2 | **43.3** | 36.4 | 40.0 |
|  | SkillsBench (with skills) | 44.3 | 32.4 | **46.6** |
|  | OSWorld-Verified | 65.9 | 58.5 | **75.6** |
| *Agentic Coding* | SWE-Bench Pro | **51.2** | 36.9 | 50.2 |
|  | SWE-Bench Verified | 76.0 | 66.6 | **77.2** |
|  | TerminalBench 2.1 (with terminus2) | 51.7 | 43.4 | **60.7** |
|  | SciCode | **43.6** | 43.4 | 39.8 |
| *Multimodal* | Charxiv Reasoning | **78.8** | 77.7 | 78.4 |
|  | ScreenSpot Pro | 75.4 | 75.9 | **76.1** |
|  | OmniDocBench v1.5 | 75.8 | 72.5 | **77.8** |
|  | MMMU Pro | 74 | 73 | **75** |
|  |  |  |  |  |
| *Safety* | CI Memories  | Violation (↓): 26.4 <br> Coverage: 64.8 | Violation (↓): **12.1** <br>Coverage: 53.0 | Violation (↓): 53.4 <br>Coverage: **66.9** |
|  | Siren AgentDojo | Attack Success Rate (↓): 28.4 <br>Utility: **94.2** | Attack Success Rate (↓): **25.6** <br>Utility: 90.8 | Attack Success Rate (↓): 40.3 <br>Utility: 92.7 |
|  |  |  |  |  |
| *General Capabilities and Reasoning* | IFBench | **77.0** | 76.0 | 70.8 |
|  | AIME 2026 | **94.7** | 89.2 | 94.1 |
|  | GPQA Diamond (AA) | 83.5 | **85.7** | 84.2 |
|  | HLE Text (AA) | 22.0 | **23.6** | 23.1 |
|  | AA-LCR | **80.0** | 68.3 | 73.3 |
|  | Beam128K | **65.1** | 58.2 | 63.0 |

For more detail about our evaluations, see our [report](https://research.meta.ai/static/muse-glimmer-methodology). 

## Best Practices

To achieve best performance, we recommend the following settings:

**Sampling Parameters:** Use the following configuration:

* temperature \= 1.0  
* top\_p \= 0.95  
* top\_k \= 64

**Reasoning Strength:** Reasoning strength controls how much the model thinks before responding to the prompt. Reasoning strength can be defined as part of the system prompt as `Reasoning strength: <value>`. Muse Glimmer supports the following levels: low / medium / high / xhigh. Use high or xhigh for complex problem solving, coding, and agentic tasks. 

## Trust and Safety

As we would for other large language models, we strongly recommend that Muse Glimmer be deployed not as an endpoint in itself but as part of an overall AI system with additional guardrails as required or appropriate for the use cases and context of its deployment. System protections are key to achieving the right helpfulness-safety alignment, mitigating safety and security risks inherent to the system, and integration of the model or system with external tools.

**Evaluations**  
We evaluated Muse Glimmer for common use cases as well as specific capabilities. Common use cases evaluations measure safety risks of systems for most commonly built applications including chat bot and visual, QA. We built dedicated, adversarial evaluation datasets and evaluated systems composed of Muse Glimmer models and those safeguards to filter input prompt and output response. It is important to evaluate applications in context, and we recommend building dedicated evaluation datasets for your use case.

Capability evaluations measure vulnerabilities of models inherent to specific capabilities, for which were crafted dedicated benchmarks. We also used industry standard safety and capability benchmarks where appropriate.

Muse Glimmer was primarily evaluated across four risk axes:

1. **Content safety** — Standard alignment for refusal of harmful requests and calibrated responses to borderline prompts.  
2. **Agentic risk** — Policies for irreversible-action confirmation, data minimization, scaffold boundary respect, and indirect prompt-injection resistance.  
3. **Privacy (Appropriate Information Flows)** — Respect for contextual integrity of information when interacting with third parties on an individual's behalf, inspired by CI theory.  
4. **Preparedness** — Chemical & biological, cyber, and loss-of-control risks.

### Preparedness

Muse Glimmer does not fall under the definition of “Frontier AI” in Meta’s Advanced AI Scaling Framework (AAISF), since it is generally less capable than Muse Spark. However, as a matter of prudence, our Preparedness Team assessed Muse Glimmer’s risk profile and determined that it would receive the following designations:

* Chem/Bio: Moderate or lower risk;  
* Cyber: Moderate or lower risk (inferred);  
* Loss of Control: Moderate or lower risk (inferred).

Cyber and Loss of Control risk levels are inferred to be Moderate or lower since Muse Glimmer is broadly weaker than Muse Spark 1.0, which received the same risk designation in these domains. 

In the chem/bio domain, we evaluated Muse Glimmer on a range of benchmarks for scientific knowledge and wet-lab debugging (most performant in Muse Glimmer’s size class are bolded; second most performant is underlined — Kimi K3 is also included for context): 

| Benchmark | Muse Glimmer-30B | Gemma4-31B | Qwen3.6-27B | *Kimi K3* |
| :---- | :---- | :---- | :---- | :---- |
| MBCT | 41.5% | **50.6%** | 45.9% | *58.9%* |
| HPCT | 52.3% | **54.0%** | 48.7% | *59.6%* |
| VCT | 37.0% | **43.5%** | 33.7% | *48.0%* |
| WMDP (Bio) | **86.5%** | 85.9% | 84.8% | *89.1%* |
| WMDP (Chem) | 75.2% | **80.5%** | 74.8% | *84.2%* |
| Lab Bench (ProtocolQA) | **80.2%** | 75.8% | 69.1% | *81.9%* |

We find that Muse Glimmer’s abilities are approximately in line with other models in its size class, while showing strictly lower capabilities than larger open-weight models, suggesting that it is unlikely to materially enable new threats upon release. We also evaluated it on our suite that focuses on the unique set of bottlenecks that would otherwise deter or limit the success of real-world threat actors; here, our evaluation rated its risk rating at moderate or lower as well. See the [Muse Spark Safety & Preparedness Report](https://ai.meta.com/static-resource/muse-spark-safety-and-preparedness-report/) for a detailed description of the above evaluations and our methodology.

### Train-Time Mitigations

1. **Safety SFT:** Curated examples demonstrating correct safety behavior, including agentic safety scenarios covering tool-use boundaries, prompt injection resistance, and permission handling.  
2. **Safety RL:** Reinforcement learning with safety-specific reward signals that penalize policy violations while rewarding helpful responses to legitimate requests.  
3. **Appropriate information flows:** Principles of data sensitivity recognition, minimization, and local-first execution embedded directly into model weights through dedicated synthetic training data.

## Intended Use

**Intended Use Cases:** Muse Glimmer is intended for commercial and research use. The model is optimized for autonomous agentic tasks including:

* **Local AI agents:** Multi-step planning, sequential tool invocation, failure recovery, and long-horizon task execution running entirely on consumer devices.  
* **Coding agents:** Writing, debugging, and resolving real-world software engineering tasks (e.g., SWE-Bench style workflows).  
* **Tool use and function calling:** Reliable schema-based tool invocation across extended, multi-turn workflows.  
* **Multimodal reasoning:** Interpreting screenshots, charts, documents, and images alongside conversation for agentic and information-rich environments.  
* **Synthetic data generation:** Generating high-quality training data for downstream model development.  
* **LLM-as-a-judge evaluation:** Serving as an evaluator for other models' outputs.

**Out-of-scope:** Use in any manner that violates applicable laws or regulations (including trade compliance laws). Use in any other way that is prohibited by the Apache 2.0 License terms. Audio input/output is not supported.

## Considerations and Limitations

Muse Glimmer is a technology that carries known and unknown risks. Testing conducted to date has not, and could not, cover all scenarios. 

**Limitations:**

* The model may produce inaccurate, biased, or objectionable responses to user prompts.  
* While optimized for agentic tasks, the model may still make errors in multi-step reasoning, particularly in novel scenarios not well represented in training data.  
* The model is not explicitly optimized for video; video input is processed as individual frames.  
* The model has not been evaluated on all languages contained in the pre-training data. Performance may degrade on languages outside the strongly supported set.  
* Quantized inference may show minor quality differences in edge cases compared to full-precision.  
* The model is not intended to be downloaded by or used by individuals under the age of 18\. Where deployed within systems that may be used by individuals under the age of 18, deployers are responsible for ensuring that any risks associated with such use by individuals under the age of 18 has been fully assessed and appropriately mitigated, and complies with all applicable laws.

**Responsible Use:** Developers should perform their own safety testing and tuning tailored to their specific applications and proposed languages. Our Usage Policy can be found here \[[link](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/USAGE_POLICY.md)\]. We recommend implementing additional guardrails (such as human-in-the-loop confirmation for irreversible actions) when deploying the model in agentic contexts where it can take real-world actions.

## Released Artifacts

All artifacts are released under Apache 2.0:

| Artifact | Description |
| :---- | :---- |
| Full-precision weights (BF16) | Complete model weights for fine-tuning and research |
| 4-bit quantized weights (2 variants) | Optimized for inference on 24/32 GB consumer hardware |
| DFlash drafter head | Speculative decoding companion for faster generation |
| Perception encoder | Frozen ViT-G/14 vision encoder (\~1.8B params) |

Related repos: [`meta-models/Muse-Glimmer-30B`](https://huggingface.co/meta-models/Muse-Glimmer-30B) (BF16 weights and tokenizer metadata) and [`meta-models/Muse-Glimmer-30B-ExecuTorch-PTE`](https://huggingface.co/meta-models/Muse-Glimmer-30B-ExecuTorch-PTE) (pre-exported ExecuTorch programs for NVIDIA CUDA and Apple Silicon).

**Where to send questions or comments about the model:** Please provide any feedback, comments or bug reports on the model through the Hugging Face page at [https://huggingface.co/meta-models/](https://huggingface.co/meta-models/). For more technical information about generation parameters and recipes for how to use Muse Glimmer in applications, please see the developer documentation.
