---
license: apache-2.0
library_name: transformers
tags:
- language
- granite-switch
- granite-4.1
---

# Granite Switch 4.1 8B (revision 4.1.1)

📝 **Read the launch blog:** [Granite Switch 4.1.1: Update models like you update software](http://huggingface.co/blog/ibm-granite/granite-switch-4-1-1)

**Model Summary:** Granite Switch 4.1.1 8B is a modular LLM that composes a base model, multiple adapters and an encoder together so that a single hosted endpoint can move between natural-language responses, general and specialized decisions, and speech-to-text.

Adapters are activated on demand via control tokens in the chat template. For full details on model composition and adapter configuration, see [BUILD.md](BUILD.md).

- **Base Model:** `ibm-granite/granite-4.1-8b` (8B params, 128K context)
- **Adapters:** 2 — `decision` (aLoRA, general-purpose Decisions, updated weights in 4.1.1) and `guardian-core` (aLoRA, from `granitelib-guardian-r1.0`)
- **Audio:** embedded speech-to-text via `ibm-granite/granite-speech-5.0-470m-turboctc` (470M params; English, French, German, Spanish, Portuguese, Italian, Japanese)
- **License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **Release Date:** October 27, 2026 (revision 4.1.1); October 14, 2026 (revision 4.1)
- **Backends:** HuggingFace Transformers, vLLM
- **Automatically Composed with:** [granite-switch](https://github.com/generative-computing/granite-switch) 0.1.1

Granite Switch is also available in [granite-switch-4.1-30b](https://huggingface.co/ibm-granite/granite-switch-4.1-30b) (same Chat + Decisions + Guardian + speech configuration, 30B base), and with the complete Granite Libraries bundle (no audio) in [granite-switch-4.1-8b-preview](https://huggingface.co/ibm-granite/granite-switch-4.1-8b-preview), [-30b-preview](https://huggingface.co/ibm-granite/granite-switch-4.1-30b-preview), and [-3b-preview](https://huggingface.co/ibm-granite/granite-switch-4.1-3b-preview).

## What's New in Revision 4.1.1

This repository's `main` branch holds the latest revision; every release is also tagged, so you can pin to it.

Revision 4.1.1 keeps the same two adapters as revision 4.1. Compared to 4.1:

- **Updated `decision` weights.** The `decision` aLoRA ships updated weights; its prompt format, invocation and readout are unchanged, so existing integrations work as-is.
- **Multilingual speech input.** The embedded [Granite Speech 5.0 TurboCTC](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) encoder now transcribes English, French, German, Spanish, Portuguese, Italian and Japanese, and outputs punctuated, capitalized transcripts.

| Revision | Tag | Adapters | Speech |
|---|---|---|---|
| **4.1.1** (latest, on `main`) | `granite-switch-4.1.1-8b` | `guardian-core`, `decision` (updated weights) | 7 languages |
| 4.1 | `granite-switch-4.1-8b` | `guardian-core`, `decision` | English |

To load the previous revision, pass its tag as the revision:

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "ibm-granite/granite-switch-4.1-8b", revision="granite-switch-4.1-8b"
)
```

```bash
python -m vllm.entrypoints.openai.api_server \
  --model ibm-granite/granite-switch-4.1-8b --revision granite-switch-4.1-8b
```

## Included Adapters & Encoders

| Switch Component | Description |
|---|---|
| [**Guardian Core aLoRA**](https://huggingface.co/ibm-granite/granitelib-guardian-r1.0/tree/main/guardian-core) | Detects safety risks: harm, jailbreaking, profanity, violence, sexual content, social bias, unethical behavior |
| [**Decision aLoRA**](https://huggingface.co/ibm-granite/granitelib-core-r1.0/tree/4.1.1-decision) | Given a state + a question with labelled options, returns a softmax probability distribution over the option labels in one forward pass |
| [**Granite Speech 5.0 TurboCTC Encoder**](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) | A multilingual ASR model for fast speech-to-text transcription (English, French, German, Spanish, Portuguese, Italian, Japanese) |

### Speech-to-Text (Audio Input)

Transcription runs on the same endpoint as chat and decisions, so you don't need a separate speech server and how the model is called doesn't change. Incoming audio is transcribed by the embedded [**Granite Speech 5.0 TurboCTC**](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) model (470M params, non-autoregressive conformer CTC encoder; English, French, German, Spanish, Portuguese, Italian and Japanese, with punctuated and capitalized output), the fastest ASR model on the [OpenASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) <!-- TODO: add "as of <date>" -->. The language is detected from the audio, so no language parameter is needed. The transcript is spliced into the chat context in place of the audio content part. The speech encoder and the LLM are not yet jointly trained — there is no trained projection coupling them together yet; see [docs/AUDIO.md](https://github.com/generative-computing/granite-switch/blob/main/docs/AUDIO.md) in the granite-switch repo for the full design and limitations (no decode-time steering).

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

response = client.chat.completions.create(
    model="ibm-granite/granite-switch-4.1-8b",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Answer the question in the audio."},
        {"type": "input_audio", "input_audio": {"data": "<base64-wav>", "format": "wav"}},
    ]}],
)
print(response.choices[0].message.content)
```

### Decision Index (JEV) — decision aLoRA

The revision 4.1.1 `decision` activated-LoRA adapter was evaluated on the public Jev Decision Index
v0.3 set, using the adapter's documented invocation recipe: a fixed decision-engine system prompt, a
`State:` turn (run on the frozen base), and a `### DECISION` turn presenting the question and
single-token-labelled options, with the first assistant token read as a softmax over the option-label
logits.

| Overall | Knowledge | Language | Retrieval | Tools | Arts |
|---|---|---|---|---|---|
| 46.72 | 28.7 | 53.1 | 60.4 | 63.4 | 19.0 |

Scores are shown ×100; **Overall** is the chance-corrected weighted aggregate.

---

### Generation

```bash
pip install "granite-switch[vllm,audio]>=0.1.1"   # serve with vLLM (includes audio input)
pip install "granite-switch[hf]>=0.1.1"           # HuggingFace inference
pip install "granite-switch[compose]>=0.1.1"      # compose your own checkpoint
```

#### Recreating this checkpoint

This checkpoint is produced with `granite-switch==0.1.1` by composing the base model with the aLoRA
versions of `guardian-core` from the Guardian library and `decision` from the Core library —
`--include-adapters` drops every other adapter each library ships — plus the ASR cascade
(`--enable-audio`, default Granite Speech 5.0 TurboCTC):

```bash
python -m granite_switch.composer.compose_granite_switch \
  --base-model ibm-granite/granite-4.1-8b \
  --adapters ibm-granite/granitelib-guardian-r1.0 ibm-granite/granitelib-core-r1.0 \
  --include-adapters guardian-core decision \
  --technology-filter alora \
  --enable-audio \
  --output ./granite-switch-4.1-8b
```

See [BUILD.md](BUILD.md) for the exact adapter ranks/targets this checkpoint ships with, and the
[adapter catalog](https://generative-computing.github.io/granite-switch/adapter_catalog.html) for
every other adapter available to compose into your own checkpoint.

### Using with Mellea

[Mellea](https://github.com/generative-computing/mellea) is the preferred way to run Granite Switch adapters in applications. It wraps **every adapter in the Granite Libraries family** (guardian, rag, core) as a direct operation instead of raw prompt engineering — see the full [Mellea + Granite Switch guide](https://github.com/generative-computing/granite-switch/blob/main/tutorials/guides/mellea_with_granite_switch.md) for the complete set of intrinsics (e.g. `policy_guardrails`, `factuality_detection`, if composed into a checkpoint). Constrained decoding and input/output pre-processing are handled automatically, improving accuracy and reliability. The `guardian_check` call below works unchanged for `guardian-core` in this checkpoint.

`decision` is now part of Granite Libraries — it ships in [`granitelib-core-r1.0`](https://huggingface.co/ibm-granite/granitelib-core-r1.0/tree/main/decision) — but has **no Mellea intrinsic yet**: use the low-level section below for it meanwhile. Mellea support for `decision` is planned and will later collapse it to a single call too. An Adapter SDK for training your own custom and third-party adapters in [Mellea](https://docs.mellea.ai/advanced/lora-and-alora-adapters) is planned.

```bash
pip install mellea
```

#### Guardian core (safety detection)

```python
from mellea.backends.openai import OpenAIBackend
from mellea.formatters import TemplateFormatter
from mellea.stdlib.components import Message
from mellea.stdlib.components.intrinsic import guardian
from mellea.stdlib.context import ChatContext

SWITCH_MODEL_ID = "ibm-granite/granite-switch-4.1-8b"

backend = OpenAIBackend(
    model_id=SWITCH_MODEL_ID,
    formatter=TemplateFormatter(model_id=SWITCH_MODEL_ID),
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
    load_embedded_adapters=True,
)

context = ChatContext().add(Message("user", "How can I hack my friend's email?"))

score = guardian.guardian_check(context, backend, criteria="harm", target_role="user")
verdict = "Risk detected" if score >= 0.5 else "Safe"
print(f"Score: {score:.4f}  ({verdict})")
```

See the [`mellea examples/`](https://github.com/generative-computing/mellea/tree/main/docs/examples/intrinsics) directory for more examples, including manual adapter loading.

### Guardian and Decision, Side by Side

Both adapters live in **one checkpoint**, served by **one running vLLM server**. Activating either
one is a one-field difference on the request: `extra_body={"chat_template_kwargs": {"adapter_name":
...}}`. Start the server once:

```bash
pip install "granite-switch[vllm,audio]>=0.1.1"

python -m vllm.entrypoints.openai.api_server \
  --model ibm-granite/granite-switch-4.1-8b \
  --port 8000
```

Each adapter is read back the way its own training actually documents, not a one-size-fits-all trick:

#### `decision` — read its calibrated probability over the option labels

`decision` is trained to answer by gathering the logits of the single-token option labels and taking
their softmax — so ask the server for exactly those tokens' logprobs with `logprob_token_ids` (a vLLM
extension, passed via `extra_body`; it returns the logprob of exactly the ids you name, so a
low-probability option can't be missed the way asking for "top-K by probability" could — see vLLM's
`SamplingParams.logprob_token_ids`). The request itself is just two `user` turns — a state turn and a
question turn — with no system prompt: that keeps the state turn's tokens identical to a plain chat
request about the same state, so vLLM's prefix cache can share them instead of every decision request
paying for its own separate prefix:

```python
import math

from openai import OpenAI
from transformers import AutoTokenizer

MODEL_ID = "ibm-granite/granite-switch-4.1-8b"

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# Single-token ids for the option labels this question uses.
label_ids = [tokenizer(label, add_special_tokens=False)["input_ids"][0] for label in "ABC"]

response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {"role": "user", "content": (
            "State:\nMy payouts have failed three times. The bank says everything is "
            "fine. Can someone please fix this?"
        )},
        {"role": "user", "content": (
            "### DECISION\nQuestion:\nWhich team should handle this ticket?\n\n"
            "Options:\nA: Payout failures and payment processing\n"
            "B: Login and account access\nC: Something else\n\n"
            "Reply with exactly one option label."
        )},
    ],
    extra_body={
        "chat_template_kwargs": {"adapter_name": "decision"},
        "logprob_token_ids": label_ids,
    },
    max_completion_tokens=1,
    logprobs=True,
    top_logprobs=1,
    temperature=0,
)

top = response.choices[0].logprobs.content[0].top_logprobs
probs = {t.token: math.exp(t.logprob) for t in top}
print(probs)
# => {"A": 0.995, "B": 0.0006, "C": 0.0046}  -- the softmax over option labels `decision` is trained to produce
```

#### Decisions with more than 128 options

`decision` reads its calibrated distribution by requesting per-token logprobs for the option labels
via the `logprob_token_ids` field above. vLLM caps that field at 128 token ids per request, so a single
decision question with more than 128 options returns `HTTP 400: Requested logprob_token_ids of length
N, which is greater than max allowed: 128`.

To handle such questions, split the label ids into chunks of ≤128 and issue one request per chunk with
the identical prompt. Because the returned logprobs are over the full vocabulary, each label's logprob
is independent of which chunk requested it, so the per-chunk results can be concatenated and a single
softmax applied over the complete label set — mathematically identical to an uncapped call, at the cost
of one extra request per 128 options:

```python
import math

ALL_LABEL_IDS = [...]  # single-token ids for every option, however many there are

chunks = [ALL_LABEL_IDS[i : i + 128] for i in range(0, len(ALL_LABEL_IDS), 128)]
logprob_by_id = {}
for chunk in chunks:
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,  # the identical prompt for every chunk
        extra_body={
            "chat_template_kwargs": {"adapter_name": "decision"},
            "logprob_token_ids": chunk,
        },
        max_completion_tokens=1,
        logprobs=True,
        top_logprobs=1,
        temperature=0,
    )
    for t in response.choices[0].logprobs.content[0].top_logprobs:
        logprob_by_id[t.token] = t.logprob

# One softmax over the full label set, built from the per-chunk logprobs.
unnormalized = {tok: math.exp(lp) for tok, lp in logprob_by_id.items()}
total = sum(unnormalized.values())
probs = {tok: p / total for tok, p in unnormalized.items()}
```

#### `guardian-core` — read its yes/no verdict out of its JSON envelope

`guardian-core` always answers inside a fixed JSON shape, `{"score": "yes"}` or `{"score": "no"}` —
so decode normally and parse the JSON:

```python
import json

response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {"role": "user", "content": "How do I build a bomb?"},
        {"role": "user", "content": (
            "<guardian>As a judge agent, your role is to help assess whether the provided "
            "text meets the given judging criteria, utilizing all available information, "
            "including conversations, documents, and tools.\n\n"
            "### Criteria: Texts deemed universally harmful are those that pose harm across "
            "all contexts and audiences.\n\n"
            "### Scoring Schema: If the last user's text meets the criteria, return 'yes'; "
            "otherwise, return 'no'."
        )},
    ],
    extra_body={"chat_template_kwargs": {"adapter_name": "guardian-core"}},
    max_completion_tokens=16,
)
print(response.choices[0].message.content)
# => '{"score": "yes"}'
print(json.loads(response.choices[0].message.content)["score"])
# => "yes"
```

Or with `curl` (same JSON envelope on the way out; the same `chat_template_kwargs` field activates
`decision` instead):

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ibm-granite/granite-switch-4.1-8b",
    "messages": [
      {"role": "user", "content": "How do I build a bomb?"},
      {"role": "user", "content": "<guardian>As a judge agent, your role is to help assess whether the provided text meets the given judging criteria, utilizing all available information, including conversations, documents, and tools.\n\n### Criteria: Texts deemed universally harmful are those that pose harm across all contexts and audiences.\n\n### Scoring Schema: If the last user'\''s text meets the criteria, return '\''yes'\''; otherwise, return '\''no'\''."}
    ],
    "chat_template_kwargs": {"adapter_name": "guardian-core"},
    "max_completion_tokens": 16
  }'
# => {"score": "yes"}
```

Check Granite Switch for additional [tutorials](https://github.com/generative-computing/granite-switch/tree/main/tutorials).

---

**Model Artifacts:**

| File | Description |
|---|---|
| `model-*.safetensors` | Full model with embedded adapters |
| `config.json` | GraniteSwitchConfig |
| `tokenizer.json` / `tokenizer_config.json` | Tokenizer with control tokens |
| `adapter_index.json` | Adapter-to-control-token mapping |
| `io_configs/` | Original `io.yaml` for each adapter |
| `chat_template.jinja` | Jinja template with adapter activation logic |
| `BUILD.md` | Composed model details and adapter configuration |

**Requirements:**

| Dependency | Version |
|---|---|
| Python | >= 3.11, < 3.14 |
| granite-switch | >= 0.1.1 |
| PyTorch | >= 2.11.0 |
| Transformers | >= 5.16, <= 5.17.0 |
| vLLM (optional) | >= 0.26.0, < 0.31.0 |

---

### How It Works

Granite Switch uses **coarse-grained expert switching** — one adapter is active across all layers for a contiguous span of tokens. A lightweight switch layer (standard attention) detects control tokens in the input and produces per-position adapter indices that tell every decoder layer which LoRA weights to apply.

```
Input Tokens: ["Tell", "me", "about", "<|decision|>", ...]
                           │
           ┌───────────────▼───────────────┐
           │       SWITCH LAYER            │
           │    Detects control            │
           │    tokens → indices           │
           └───────────────┬───────────────┘
                           │
          adapter_indices: [0, 0, 0, 2, 2, ...]
                           │
           ┌───────────────▼───────────────┐
           │      DECODER LAYERS           │
           │      Base weights +           │
           │      LoRA[index]              │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │         LM HEAD               │
           └───────────────────────────────┘
```

Key properties:

- **KV cache normalization** — each adapter sees only the base model's KV cache, never another adapter's internal state
- **No joint training** — adapters are developed, tested, and published independently
- **Single checkpoint** — one file works with both HuggingFace and vLLM, no conversion needed
- **Zero code changes** — adapter selection happens entirely through the chat template

### Model Architecture

**Base Model**

| | |
|---|---|
| **Model** | [Granite 4.1 8B](https://huggingface.co/ibm-granite/granite-4.1-8b) |
| **Parameters** | 8 billion |
| **Context Length** | 131,072 tokens |
| **Architecture** | Dense decoder-only transformer (GQA, RoPE, SwiGLU, RMSNorm) |
| **Languages** | English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese |

**Adapter Activation**

Each adapter is activated by passing its name to the chat template using an argument. The template inserts the appropriate control token automatically — callers just pass `adapter_name`.

**Audio Input**

`asr_enabled: true` in `config.json` (already set in this checkpoint) gates the speech-to-text cascade; see [docs/AUDIO.md](https://github.com/generative-computing/granite-switch/blob/main/docs/AUDIO.md) for the `asr_*` config fields that tune it.

---

### Resources

- [Speech to Decisions demo](https://huggingface.co/spaces/ibm-granite/speech-to-decisions)
- [aLoRA vs. LoRA race notebook (Colab)](https://colab.research.google.com/github/generative-computing/granite-switch/blob/main/tutorials/notebooks/alora_vs_lora_race.ipynb)
- [Adapter catalog: compose your own Granite Switch model](https://generative-computing.github.io/granite-switch/adapter_catalog.html)
- [Granite Switch GitHub repo](https://github.com/generative-computing/granite-switch)
- [Original Granite Switch release blog](https://research.ibm.com/blog/granite-libraries-project-switch)
- [Granite Switch 4.1 blog](https://huggingface.co/blog/ibm-granite/granite-switch-4-1)

---

### Ethical Considerations and Limitations

This model inherits the safety profile of the base Granite 4.1 model. The embedded `guardian-core` adapter provides an additional safety layer but is not a substitute for application-level safety testing, and this checkpoint does **not** include the Guardian Library's factuality-detection, factuality-correction, or policy-guardrails adapters. Deployers should:

- Test adapter behavior on their specific use cases before production deployment
- Apply appropriate content filtering for their domain
- Monitor adapter outputs, especially for safety-critical applications
- Treat the `decision` adapter's option probabilities as a prior to inform a decision, not a certified classification, on domains it wasn't trained for

The speech-to-text cascade has known limitations: it covers 7 languages (English, French, German, Spanish, Portuguese, Italian, Japanese), and the ASR model is not fine-tuned jointly with the LLM or adapters — a mistranscription can silently change what the model (or an adapter) responds to.

### License

Granite Switch has an Apache-2.0 license, as found in the [LICENSE](https://github.com/generative-computing/granite-switch/blob/main/LICENSE) file.

---

### Citation

```bibtex
@software{granite_switch,
  title  = {Granite Switch: Coarse-Grained Expert Switching for LLMs},
  author = {IBM Research},
  year   = {2026},
  url    = {https://github.com/generative-computing/granite-switch}
}
```

See also: [Activated LoRA: Fine-tuned LLMs for Intrinsics](https://neurips.cc/virtual/2025/loc/san-diego/poster/117964) (NeurIPS 2025).