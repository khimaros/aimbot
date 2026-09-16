---
license: apache-2.0
base_model: google/gemma-4-12B-it
library_name: transformers
pipeline_tag: text-generation
tags: [gemma4, coding, agentic, terminal, tool-use, reasoning, thinking, safetensors, transformers]
---

# 💻🤖 Gemma4-12B **v2** — **safetensors master (full precision)** ✨
### Coding + Agentic Edition · Composer 2.5 × Fable 5 · v2

> **This is the full-precision `safetensors` master** for my Gemma 4 12B **coding + agentic** fine-tune — the same
> model many of you have been running as GGUF, now in its original weights. 🧠🛠️ v2 is the big **agentic** upgrade:
> it reads, reasons, *uses tools*, and works through multi-step technical tasks before it acts. This repo is for
> *builders* — roll your own quants, fine-tune further, or run it in `transformers`.

---

## 🎉 Surprise!

A huge thank-you for all the attention this project has gotten — really, thank you. 🙏 I only managed to get out
**tonight** to upload the **full-precision original (safetensors master)** of this model, so sorry for the wait — I'd
planned to put it up last week. But the delay comes with **two big surprises** I've been dying to share:

**1. v3 is coming soon.** 🔮 The next version is on its way and will fix several of the known issues you've reported.

**2. I'm now working with a top-tier AI lab to give back to the open-source community.** 🤝 Many of you have already
noticed the side effects in v1 and v2 — and honestly they come down to just two things: **(1) not enough compute, and
(2) one person with limited expertise** behind the whole thing. This collaboration **solves both of those completely.**
And the **benchmarks you care about will absolutely be addressed** — the things I simply couldn't fully pull off before
because of time and compute limits. The people working on this with me are **PhDs from top universities, with seriously
strong papers and citation records.** Just think about that for a second: the people who *actually build large models*
are now contributing to the open-source community *together with me* — that is genuinely **wild**. 🤯 We're in active
discussions right now, and the project is still in the **R&D phase**, so I can't share specifics yet — but the **moment**
I have news, **you'll be the first to know.** 🚀

---

## 🎯 What this repo is for

This repo holds the **un-quantized master weights** (`model.safetensors`, bf16). Use it to:

- 🔧 **Roll your own quants** — make custom GGUF / **MLX** / AWQ / GPTQ builds from full precision.
- 🧪 **Fine-tune further** — it's a clean base for your own LoRA / continued training.
- 🤗 **Run it in `transformers`** (needs a recent build with `gemma4_unified` support).

> 🏃 **Just want to run it?** You don't need this repo — grab a ready-made quant from the
> **[GGUF repo →](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF)** (runs in
> ~4.5 GB of VRAM / unified memory in LM Studio, Ollama, llama.cpp, Jan…). This master is for *builders*. 💚

---

## 📊 The headline — it works as an agent (tau2-bench)

v2 is built for **coding + agentic** work — writing code, running commands, using tools, debugging, multi-step
technical tasks. The clearest signal is **tau2-bench `telecom`**, an agentic tool-use benchmark whose
*diagnose → fix → verify* loop mirrors real terminal/debugging work:

| tau2-bench **telecom** · 20 tasks · local, same harness, **all Q8_0** | score |
|---|---|
| official `gemma-4-12B-it` (base) | **~15%** |
| 🟢 **Gemma4-12B v2 (this model)** | **~55%** |

→ Roughly **3.5× higher** than the base model on technical-agentic tasks. 🎯

> 🔬 *Honest methodology:* these are **local, same-harness, relative** numbers (**all models tested at Q8_0**, greedy
> decoding, self-simulated user, 20 tasks). They are **not** directly comparable to published tau2-bench leaderboard
> figures (different user-simulator, full task sets, full precision) — local self-eval runs *systematically lower* than
> published scores. Read them as **"v2 vs the base model under identical conditions"**, which is the comparison that
> actually matters here.

**Grounded, not made-up.** A coding/terminal *fabrication probe* (tasks that deliberately tempt the model to invent
file paths / function signatures / values) found v2 **grounds before it acts** just like the base — it `grep`/`read`/`ls`
first, and **doesn't make things up** (0% fabrication, on par with the base).

**The trade-off — no free lunch.** On a general-knowledge benchmark (**MMLU-Pro**), v2 lands a little **below** the base —
completely normal for a focused fine-tune: you trade a sliver of broad-knowledge breadth for coding + agentic strength.
Need a generalist? Try my general-purpose
**[Claude Opus 4.6/4.8 distillation](https://huggingface.co/yuxinlu1/gemma-4-12B-it-Claude-4.6-4.8-Opus-GGUF)** or the
base `google/gemma-4-12B-it`. Need a **local coding/agentic** worker? That's what v2 is tuned for. 💚

---

## 🤗 Run it in transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

repo = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo, torch_dtype=torch.bfloat16, device_map="auto")

msgs = [{"role": "user", "content": "Write a Python function to check if a string is a valid IPv4 address."}]
inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(model.device)
out = model.generate(inputs, max_new_tokens=1024)
print(tok.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True))
```

> 🧠 **Thinking mode:** it thinks in Gemma's native thought channel before answering (keep `enable_thinking=true`, the
> default chat template handles it). Recommended sampling: `temp 1.0, top_p 0.95, top_k 64`; for coding you can also go
> greedy (`temp 0`). Needs a **recent `transformers`** that knows the `gemma4_unified` architecture.
>
> 🛠️ **Agentic / tool use:** v2 emits structured tool-calls in Gemma 4's **native** protocol. The smoothest agent
> setup is a GGUF quant served with llama.cpp `--jinja` (pass your tools via the OpenAI `tools` field) — see the GGUF
> repo for the full command.

---

## 📦 Ready-made GGUF quants

All from the **[GGUF repo](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF)**:

| Quant | Size | Vibe |
|------|------|------|
| 🟡 [**Q3_K_M**](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF/blob/main/gemma4-v2-Q3_K_M.gguf) | **5.7 GB** | great for 8 GB VRAM |
| 🔵 [**Q4_K_M**](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF/blob/main/gemma4-v2-Q4_K_M.gguf) | **6.87 GB** | the sweet spot 👌 (recommended) |
| 🟣 [**Q6_K**](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF/blob/main/gemma4-v2-Q6_K.gguf) | **9.11 GB** | near-lossless |
| ⚪ [**Q8_0**](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF/blob/main/gemma4-v2-Q8_0.gguf) | **11.8 GB** | basically full quality |

> ⚠️ GGUF needs a **recent llama.cpp** — this is the `gemma4_unified` architecture, older builds won't load it.
> ℹ️ **No Q2_K this release** — it didn't pass real stress-testing (2-bit is too lossy for 12B coding). Smallest
> reliable quant = **Q3_K_M**.

---

## 📚 What's new in v2 (training)

v2 continues from the v1 coder and adds a big **agentic** push — the piece v1 was missing:

- **🛠️ Agentic / terminal** — real **multi-step tool-use** trajectories (*read → reason → act → verify*), in Gemma 4's
  native tool protocol. This is what drove the tau2-bench telecom jump, and it fixes v1's "stops after the first step"
  behavior.
- **💻 Coding** — verified chain-of-thought over Python tasks (**real CoT, gated on passing tests**) plus the
  Fable-5-redo set for the hard cases.
- **📚 General** — a curated slice of reasoning/instruction data to keep broad competence.

All reasoning is **distilled CoT**. A bittersweet note: none of us saw it coming that **Fable 5 would be retired**, and
only my own dataset holds Fable 5's genuine, self-authored traces — so for the community-contributed data I **rebuilt the
missing reasoning from scratch with Opus 4.8 (xhigh)**. It may diverge from the original Fable 5 traces, but it was the
only workable path — and the improvement turned out **really huge**. 💚

---

## ⚡ Speculative decoding (MTP draft) — verified build

The GGUF repo's `MTP/` folder ships the Gemma 4 multi-token-prediction draft (unsloth's GGUF conversion of Google's
official `gemma-4-12B-it-assistant`) for speculative decoding. Gemma 4 MTP is in **llama.cpp mainline** (PR #23398) — no
fork needed — but the `gemma4-assistant` loader is **build-sensitive right now**, so use the exact build below:

- ✅ **Verified working: llama.cpp `b9553` (commit `9e3b928fd`).** Reproduced with `gemma4-v2-Q8_0` + the `MTP-Q8_0`
  draft: loads cleanly and accelerates generation (~88 → ~180 tok/s on a simple deterministic prompt; expect ~1.2–1.3×
  on real coding/thinking). **Lossless** either way.
- ⚠️ **Newer builds (e.g. b9702 / b9717) currently crash** while loading the draft with `invalid vector subscript` — an
  **upstream regression** in the `gemma4-assistant` loader path, *not* a problem with the GGUFs. Stick with **b9553**
  until it's fixed upstream.

```bat
llama-server -m gemma4-v2-Q8_0.gguf ^
  --model-draft MTP\gemma-4-12B-it-MTP-Q8_0.gguf ^
  --spec-type draft-mtp --spec-draft-n-max 4 ^
  -ngl 99 -ngld 99 -fa on --jinja
```

> ℹ️ The draft is the generic Gemma 4 assistant (not retrained for v2), so acceptance is a touch lower than a
> model-specific draft would give — still 100% lossless.

---

## ⚠️ Good to know
- **Specialized for coding / terminal / agentic.** General-knowledge facts/numbers should still be double-checked.
- **Reduced refusals:** task-focused training, not safety-aligned — add your own guardrails for production. Use
  responsibly. 🙏
- English-centric.

---

## 📚 Base & License
- **License: Apache 2.0.** Gemma 4 is released by Google under
  **[Apache 2.0](https://ai.google.dev/gemma/apache_2)** (unlike the older Gemma 1/2/3 terms), so this fine-tune is
  **Apache 2.0** too — free to use, modify, and redistribute. 🎉
- **Base model:** [`google/gemma-4-12B-it`](https://huggingface.co/google/gemma-4-12B-it).
- Personal/hobby project — shared as-is, no warranty. Built with time, care, and a lot of coffee. Have fun, and happy
  hacking! 🐾✨
