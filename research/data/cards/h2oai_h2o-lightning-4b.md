---
license: apache-2.0
base_model: Qwen/Qwen3.5-4B
library_name: transformers
pipeline_tag: image-text-to-text
tags:
- decision-model
- decision-making
- calibration
- jevbench
- multimodal
- typed-decisions
---

![H2O Lightning: Decision Models](assets/banner.png)

# H2O-Lightning-4B

H2O-Lightning-4B is a 4B-parameter decision model from H2O.ai, built on
[Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B). It answers typed decision questions about a record (a
document, a ticket, a policy, a conversation) and about images that come with the record (photos,
screenshots, scanned documents, charts). It returns a probability for every option:

- **choice**: picks one of a set of named options;
- **yes/no** (`noul`): gives the probability that a statement is true;
- **score**: gives an ordinal level on a stated scale, with its probability distribution.

## Leading on Benchmarks

![Leading on Benchmarks: #1 of 46, Composite (open-weight Jev-class models; #2 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #2 of 46, Intelligence (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #2 of 46, Capability (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #2 of 170, Composite (open-weight Jev-class models; #12 of 201 Jev-class models, open or API), JevBench board of 2026-10-28; #1 of 4, Box Capability (open-weight Jev-class models; #1 of 5 Jev-class systems, open or API), ImageJevBench Box track (PREVIEW); #1 of 46, Composite (open-weight Jev-class models; #3 of 55 Jev-class systems, open or API), ImageJevBench computer-use track](assets/leading_on_benchmarks_4b.png)

- **#1 of 46 — Composite** (open-weight Jev-class models; #2 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-31, its row for release v1.4.1 @d7f1b05a, measured 2026-10-28 at image temperature
  1.0; ahead of
  Drex Max (Nace AI, 44.65),
  Jev 1.13.0 + images (TypeSafe, 26.43),
  Clef-Flash (Cloudflare, 20.41) and
  Liquid d1-3B (4.10) ([details](#imagejevbench))
- **#2 of 46 — Intelligence** (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-31, its row for release v1.4.1 @d7f1b05a, measured 2026-10-28 at image temperature
  1.0; ahead of
  Clef (Cloudflare, 47.40) and
  Liquid d1-3B (16.31) ([details](#imagejevbench))
- **#2 of 46 — Capability** (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-31, its row for release v1.4.1 @d7f1b05a, measured 2026-10-28 at image temperature
  1.0; ahead of
  Clef (Cloudflare, 58.08) and
  Liquid d1-3B (47.78) ([details](#imagejevbench))
- **#2 of 170 — Composite** (open-weight Jev-class models; #12 of 201 Jev-class models, open or API), JevBench board
  of 2026-10-28, its row for release v1.1, measured 2026-10-04; ahead of
  d1 (Liquid AI, 72.82),
  Microsoft-Decision-1 (69.08),
  OpenAI Decisions (62.37) and
  pplx-decider-flash (Perplexity, 54.01) ([details](#leading-on-benchmarks))
- **#1 of 4 — Box Capability** (open-weight Jev-class systems; #1 of 5 Jev-class systems, open or API; Jev-class on this
  track: within 2x the latency and cost of Jev 1.14.0), ImageJevBench Box track (PREVIEW), edition v0.3.0, page read
  2026-10-29, its row for release v1.4.1 through the H2O serving package, measured 2026-10-29; ahead of
  Jev 1.14.0 (TypeSafe, 75.71) ([details](#for-benchmark-maintainers-imagejevbench-box-track))
- **#1 of 46 — Computer-use Composite** (open-weight Jev-class systems; #3 of 55 Jev-class systems, open or API,
  behind two API systems scored on the board's smaller hosted-API item set), ImageJevBench computer-use track, edition
  v0.3.0, page read 2026-10-31, its row for release v1.4.1 @d7f1b05a, measured 2026-10-28 at image temperature 1.0;
  ahead of
  Liquid d1-3B (Liquid AI, 66.22) and
  Clef-Flash (Cloudflare, 55.29) ([details](#imagejevbench))

**How to run it** (recommended setup first):

- **Recommended: our vLLM build, two-way reading.** Our per-request attention build of vLLM 0.30.0, with the
  standard-library shim (`h2o_lightning_shim.py`) in front, reads each request two-way. Start it with
  `bash h2o-lightning-4b/serve.sh` (the default). It scores 206 of JevBench's 231 public items this way; see
  [Measured](#measured) and [Two-way reading](#two-way-reading-recommended).
- **For benchmark maintainers:** one command each for
  [JevBench](#for-benchmark-maintainers-jevbench), [the Decision Index](#for-benchmark-maintainers-decision-index) and
  [ImageJevBench's Box track](#for-benchmark-maintainers-imagejevbench-box-track).
- Fallback: stock vLLM 0.30.0, one-way reading, when you cannot install the build:
  `TWO_WAY=0 bash h2o-lightning-4b/serve.sh`. It uses the prefix cache and serves more requests per second under
  load; it scores 202 of the 231 items. See [Run it](#run-it).
- Cost: each decision is one forward pass and one output token, so the cost is input tokens only.
- Options: choosing the reading per request, and serving many requests, are under
  [One engine, both modes](#one-engine-both-modes) and [Serving at scale](#serving-at-scale).

**Try it in your browser:** [live demo on Hugging Face Spaces](https://huggingface.co/spaces/h2oai/h2o-lightning-4b) (text and images; built by the Hugging Face team and running on ZeroGPU).

**Other formats:** GGUF for llama.cpp: [h2oai/h2o-lightning-4b-gguf](https://huggingface.co/h2oai/h2o-lightning-4b-gguf). MLX for Apple silicon, built by NetProjects:
[netprojects/h2o-lightning-4b-mlx-q8](https://huggingface.co/netprojects/h2o-lightning-4b-mlx-q8) (8-bit; two-way and
one-way) and [netprojects/h2o-lightning-4b-mlx-q4](https://huggingface.co/netprojects/h2o-lightning-4b-mlx-q4) (4-bit;
one-way only). They carry this release's weights and serving files; NetProjects reports 205 / 231 on JevBench's public items two-way and 201
one-way for the 8-bit build. A variant on a different base:
[h2oai/h2o-lightning-4b-nemotron-nano](https://huggingface.co/h2oai/h2o-lightning-4b-nemotron-nano), built on NVIDIA
Nemotron 3 Nano 4B; text only; NVIDIA Nemotron Open Model License.

On JevBench (board v1.7.15, read 2026-10-28) the board lists v1.4.1's row, composite 75.98, without a rank: its
draw is not yet equated to the board's reference scale. This release is not yet on the board.

### ImageJevBench

On the board's [ImageJevBench page](https://benchmarkheaven.com/image-jev-bench) (edition v0.3.0, read 2026-10-31), the board's run
of v1.4.1 @d7f1b05a (the same weights), measured on 2026-10-28 with images at temperature 1.0 and v1.4.1's image cap, scores:

| Intelligence | Calibration | Speed | Cost | Capability | Composite |
|---|---|---|---|---|---|
| 55.48 | 88.19 | 88.72 | 56.34 | 71.84 | **68.51** |

On Composite it is the first of 46 open-weight Jev-class models and second of 55 Jev-class models, open or API; the one ahead
of it is an API system (75.38). On Capability it is the second of 46 open-weight Jev-class models, behind H2O-Lightning-31B,
and sixth of 55 Jev-class models, open or API. It is ahead of Drex Max (Nace AI, 44.65) and
Jev 1.13.0 + images (TypeSafe, 26.43). Image temperature: see [Image calibration](#image-calibration).

## Run it

The weights (`model.safetensors`) are 9.3 GB; measured on one NVIDIA L40S (48 GB). Install vLLM
0.30.0 with pip in a fresh virtual environment, and download the model (on a fresh Ubuntu, `python3 -m venv` first needs
`sudo apt install python3-venv`):

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "vllm==0.30.0" "torchcodec==0.17.0" "transformers==5.20.2"
hf download h2oai/h2o-lightning-4b --local-dir h2o-lightning-4b
```

(The default build needs a CUDA 13 driver, R580 or later; on an older driver, install the CUDA 12.9 build instead: `pip install "vllm==0.30.0+cu129"
"torchcodec==0.16.0+cu129" "transformers==5.20.2" --extra-index-url https://wheels.vllm.ai/0.30.0/cu129 --extra-index-url
https://download.pytorch.org/whl/cu129`.) `transformers==5.20.2` is the tested version; without the pin pip
takes the newest. That is stock vLLM: enough for one-way reading. **Two-way reading
(recommended) needs our vLLM build** with per-request attention, [h2oai/vllm](https://github.com/h2oai/vllm) at commit
`b05cc29ab813895947954c268c4ec41ca0da1306`: vLLM 0.30.0 plus 30 changed Python files under `vllm/` (no compiled
code). Copy them over the vLLM installed above; `engine/vllm_per_request_attention.SHA256SUMS` lists each file with
its sha256:

```bash
SUMS="$PWD/h2o-lightning-4b/engine/vllm_per_request_attention.SHA256SUMS"
SRC="$(mktemp -d)"; git -C "$SRC" init -q && git -C "$SRC" fetch -q --depth 1 https://github.com/h2oai/vllm b05cc29ab813895947954c268c4ec41ca0da1306 && git -C "$SRC" checkout -q FETCH_HEAD
SITE="$(python -c 'import os, vllm; print(os.path.dirname(os.path.dirname(vllm.__file__)))')"
while read -r sha path; do mkdir -p "$SITE/$(dirname "$path")" && cp "$SRC/$path" "$SITE/$path"; done < "$SUMS"
(cd "$SITE" && sha256sum -c --quiet "$SUMS") && echo "per-request attention build installed"
```

Use pip as above: a uv virtual environment hard-links installed files to a shared cache, and copying over them would
change every environment linked to it. `serve.sh` checks the build before it starts vLLM, on every start: it stops
with a message on a stock vLLM, or when a listed file does not match its sha256 (one-way, `TWO_WAY=0`, needs no
build). The shim needs Python 3.8 or later and nothing else.

That is `main`: the weights, both reading modes, the Box question and image references.

**Checking this card against the files.** `test_card.py` (with `card_common.py`, shipped here) runs what the card
says and compares it with what the card says: `CARD_REV=<commit> python3 -m pytest test_card.py -m static` checks
files, pins, tags, layout, links and the registered claims in seconds; `CARD_LIVE=1` adds the launch commands and
example requests above on a GPU (the two-way launches need
`CARD_ONE_ENGINE_VLLM`, a `vllm` command of the build above); `-m slow` with `CARD_BENCH231_DIR` recomputes
the benchmark numbers in [Measured](#measured). Every release is gated on it.

**Recommended: two-way reading, one command** (one GPU; the vLLM build above):

```bash
bash h2o-lightning-4b/serve.sh
```

That starts one generate-mode vLLM on the weights (`--attention-backend TRITON_ATTN`) and the shim in front of it,
warms up every path the card uses (both modes; a yes/no question, a three-question request, a long record and an image),
and only then prints `ready` with `http://127.0.0.1:8741/v1/systemone`. Until then the shim's `/health` answers HTTP 503
with `"warming": true` (`/health?live=1` answers 200 as soon as the shim is up), so a load balancer polling `/health`
sends no traffic to a cold server. Requests are read two-way unless they ask for
`"attention_mode": "causal"`; the same engine answers one-way requests and Box questions. The fallback for a stock
vLLM is one-way:

```bash
TWO_WAY=0 bash h2o-lightning-4b/serve.sh
```

(or `ATTENTION=one-way`): one stock generate-mode vLLM. What each mode is and when to use
which: [Two-way reading](#two-way-reading-recommended). The two steps behind the command, for a manual start:

**1. Serve the model.** Keep `config.json` as shipped: its `"head_dtype": "float32"` makes vLLM compute the logits in
fp32. `--tokenizer ./h2o-lightning-4b/tokenizer` keeps the tokenizer the model was trained with (`Qwen2Tokenizer`;
without it, recent transformers versions load a tokenizer that splits some Devanagari and Arabic text differently, and
the shim refuses to start). Inputs longer than the context are shortened to fit (see [Long inputs](#long-inputs)); they never get an error. The `--limit-mm-per-prompt` / `--mm-processor-kwargs` options set
the image limits (up to 4 images per request, each scaled to at most 1,638,400 pixels inside vLLM, the cap the shim
sends with every request); `--mm-processor-cache-gb 0`, `--allowed-media-domains` and the one-way server's
`--max-cudagraph-capture-size 2048` are explained under [Serving at scale](#serving-at-scale).

Two-way (the vLLM build; the Triton attention backend, and a batch budget of the whole context so a two-way prompt
is prefilled in one step):

```bash
vllm serve ./h2o-lightning-4b --served-model-name h2oai/h2o-lightning-4b --host 127.0.0.1 --port 8000 \
  --tokenizer ./h2o-lightning-4b/tokenizer \
  --max-model-len 40960 --gpu-memory-utilization 0.90 \
  --attention-backend TRITON_ATTN --max-num-batched-tokens 40960 \
  --limit-mm-per-prompt '{"image": 4, "video": 0}' --mm-processor-kwargs '{"max_pixels": 1638400}' \
  --mm-processor-cache-gb 0 --allowed-media-domains media.invalid
```

One-way (a stock generate-mode server):

```bash
vllm serve ./h2o-lightning-4b --served-model-name h2oai/h2o-lightning-4b --host 127.0.0.1 --port 8000 \
  --tokenizer ./h2o-lightning-4b/tokenizer \
  --max-model-len 40960 --gpu-memory-utilization 0.90 \
  --limit-mm-per-prompt '{"image": 4, "video": 0}' --mm-processor-kwargs '{"max_pixels": 1638400}' \
  --mm-processor-cache-gb 0 --allowed-media-domains media.invalid --max-cudagraph-capture-size 2048
```

If vLLM stops at startup because FlashInfer cannot compile its sampling kernels (an older system CUDA toolkit), start it
with `VLLM_USE_FLASHINFER_SAMPLER=0` in the environment: the decisions do not use the sampler.

**2. Start the shim** on the same machine, telling it which kind of server it talks to:

```bash
# two-way (the vLLM build above): the shim flags each two-way read
SHIM_TWO_WAY_FLAG=1 python3 h2o-lightning-4b/h2o_lightning_shim.py --config h2o-lightning-4b/serve_config.json --vllm http://127.0.0.1:8000 --port 8741
# one-way (the stock generate-mode server)
python3 h2o-lightning-4b/h2o_lightning_shim.py --config h2o-lightning-4b/serve_config.json --vllm http://127.0.0.1:8000 --port 8741
```

Run the shim as shipped for evaluations and benchmarks (including JevBench): `serve_config.json` is the evaluated
configuration. Yes/no answers carry their calibrated probability; see [Yes/no floor](#yesno-floor).

Before answering, the shim checks that vLLM serves `h2oai/h2o-lightning-4b` and that every label is one token at the
answer slot; a two-way deployment also checks the engine's flagged answers to three fixed probes against the
release's recorded answers and against its own unflagged answers; if any check fails it answers 503, so a
misconfigured server stops a run instead of scoring it. Before the first image request it also checks that vLLM's
chat template renders the same prompt as the text path.

**3. Warm up** until this returns HTTP 200:

```bash
curl -s http://127.0.0.1:8741/v1/systemone -H 'Content-Type: application/json' -d '{"state": "warm-up",
  "questions": {"decision": {"type": "noul", "instructions": "Is this a warm-up?",
  "criteria": {"true": "yes", "false": "no"}}}}'
```

**Example requests.** Against the server above (`bash h2o-lightning-4b/serve.sh`, or steps 1 and 2). It serves the
model as `h2oai/h2o-lightning-4b` (`GET /v1/models`); the OpenAI route also accepts `h2o-lightning-4b`.
The `/v1/systemone` API, one yes/no (`noul`), one choice and one score question about one record:

```bash
curl -s http://127.0.0.1:8741/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": {"ticket": "Checkout returns HTTP 500 for every customer since 09:12.", "plan": "enterprise"},
  "questions": {
    "outage":   {"type": "noul", "instructions": "Is this a full outage?",
                 "criteria": {"true": "yes", "false": "no"}},
    "team":     {"type": "choice", "instructions": "Which team should take it?",
                 "criteria": {"payments": "Payments", "web": "Web frontend", "support": "Customer support"}},
    "urgency":  {"type": "score", "instructions": "How urgent is it?", "criteria": ["Low", "Medium", "High"]}}}'
```

The same from Python (`pip install requests`):

```python
import requests

r = requests.post("http://127.0.0.1:8741/v1/systemone", json={
    "state": {"ticket": "Checkout returns HTTP 500 for every customer since 09:12.", "plan": "enterprise"},
    "questions": {
        "outage": {"type": "noul", "instructions": "Is this a full outage?",
                   "criteria": {"true": "yes", "false": "no"}},
        "team": {"type": "choice", "instructions": "Which team should take it?",
                 "criteria": {"payments": "Payments", "web": "Web frontend", "support": "Customer support"}},
        "urgency": {"type": "score", "instructions": "How urgent is it?", "criteria": ["Low", "Medium", "High"]}}})
answers = r.json()["answers"]
print(answers["outage"]["noul"], answers["team"]["choice"], answers["urgency"]["score"])
# 0.690... payments 1.90...  (team: payments 0.918, web 0.043, support 0.038; urgency: High 0.911)
```

OpenAI's Decisions API (`POST /v1/decisions`) with OpenAI's Python client (`pip install "openai>=3.26"`), pointed at
the local server: a predicate, a choice and a score question.

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8741/v1", api_key="unused")  # the local shim ignores the key
decision = client.decisions.create(
    model="h2o-lightning-4b",
    input="Ticket: checkout returns HTTP 500 for every customer since 09:12. Plan: enterprise.",
    questions=[
        {"type": "predicate", "name": "outage", "instructions": "Is this a full outage?"},
        {"type": "choice", "name": "team", "instructions": "Which team should take it?",
         "choices": [{"value": "payments", "description": "Payments"}, {"value": "web", "description": "Web frontend"},
                     {"value": "support", "description": "Customer support"}]},
        {"type": "score", "name": "urgency", "instructions": "How urgent is it?",
         "levels": [{"label": "Low"}, {"label": "Medium"}, {"label": "High"}]},
    ],
)
print(decision.model_dump_json(indent=1))
```

Each answer comes back in OpenAI's shape (rounded): `{"type": "predicate", "name": "outage", "probability": 0.659}`,
`{"type": "choice", "name": "team", "choice": "payments", "confidence": 0.861, "probabilities": [{"value": "payments",
"probability": 0.907}, ...]}`, `{"type": "score", "name": "urgency", "score": 1.893, "confidence": 0.904,
"probabilities": [{"label": "Low", "value": 0, "probability": 0.011}, ...]}`. The OpenAI route asks the model through the same
decision as `/v1/systemone`, in the same option format: a choice's value is the option and its description the
option's text, a score level is its label, and a predicate is a yes/no question with the default wording ("the
statement holds" / "it does not"). Its numbers differ from the call above because the input is a sentence rather than
the same record and the predicate has no yes/no descriptions.
Yes/no answers are reported as read (see [Yes/no floor](#yesno-floor)). A choice's `confidence` is the normalized maximum (0 for
a uniform answer, 1 for a certain one); a score's is the probability of its most likely level. An image goes in an
`input` message as `{"type": "input_image", "image_url": "data:image/png;base64,..."}` next to
`{"type": "input_text", "text": ...}`.

**4. Benchmarks.** To run JevBench, the Decision Index or ImageJevBench's Box track the way our numbers were measured,
follow [For benchmark maintainers: JevBench](#for-benchmark-maintainers-jevbench),
[For benchmark maintainers: Decision Index](#for-benchmark-maintainers-decision-index) or
[For benchmark maintainers: ImageJevBench Box track](#for-benchmark-maintainers-imagejevbench-box-track) below, literally.

**The API.** Send requests to `POST /v1/systemone`. One request can carry several questions about the same state:

```json
{"state": "Ticket 4471: since 09:10 the checkout page returns HTTP 500 for every customer; no orders have gone through in 40 minutes. Severity guide: P1 = a revenue path fully down; P2 = degraded but working; P3 = cosmetic.",
 "questions": {
   "priority":  {"type": "choice", "instructions": "Which priority does the severity guide assign?",
                 "criteria": {"p1": "Revenue path fully down", "p2": "Degraded but working", "p3": "Cosmetic"}},
   "all_users": {"type": "noul", "instructions": "The problem affects every customer.",
                 "criteria": {"true": "Affects everyone", "false": "Affects only some"}},
   "urgency":   {"type": "score", "instructions": "How urgent is this ticket?", "criteria": ["Low", "Medium", "High"]}}}
```

The response (rounded here):

```json
{"model": "h2oai/h2o-lightning-4b",
 "answers": {
   "all_users": {"type": "noul", "noul": 0.932},
   "priority": {"type": "choice", "choice": "p1", "confidence": 0.921, "probabilities": {"p1": 0.948, "p2": 0.029, "p3": 0.023}},
   "urgency": {"type": "score", "legend": {"0": "Low", "1": "Medium", "2": "High"}, "score": 1.919, "confidence": 0.931, "probabilities": {"0": 0.012, "1": 0.057, "2": 0.931}}},
 "probability_source": "native", "effort_used": {"passes_per_decision": 1, "tier": "fast"},
 "usage": {"input_tokens": 231, "latency_ms": 87.8, "output_tokens": 3, "processed_input_tokens": 437},
 "attention_mode": "bidirectional"}
```

`usage.input_tokens` counts the prompt head that the questions share once; `usage.output_tokens` is one label
token read per answered question. A record shortened to fit the context (see [Long inputs](#long-inputs)) is still counted whole in
`usage.input_tokens`; `usage.processed_input_tokens` is what vLLM read.

**Images.** Put each image in the request as a `data:image/...;base64,...` URI. It can go anywhere inside `state` (as a
string, an object value or a list item), or in a top-level `images` list next to `state` and `questions`. The `images`
list also takes bare base64 strings and `https` image links (the shim fetches a link itself, from public addresses
only and with size and time limits, and does not store it; the server needs network access for those, and a link it
cannot fetch gets HTTP 422). Chat-style parts (`{"type": "image_url", "image_url": {"url": ...}}`) and multipart/form-data (the JSON in a
`request` field, each image as a file part) work too.
- Each image taken out of `state` leaves `[image N]` in its place, so the record can refer to it. Images in the
  top-level list are numbered first.
- Up to 4 images per request and 20 MB per image.
- Image links: `https` on port 443 (plain `http` needs `LIGHTNING_IMAGE_URL_ALLOW_HTTP=true`), an `image/*` answer with HTTP 200 after at most 3 redirects, 5 s and 20 MB per link (`LIGHTNING_IMAGE_FETCH_SECONDS`, `LIGHTNING_IMAGE_FETCH_MAX_BYTES`); `LIGHTNING_IMAGE_URLS=off` refuses links.
- Each image is scaled to at most 1,638,400 pixels, and image answers use their own temperature, 1.0 (`serve_config.json`,
  `"image"`; see [Image calibration](#image-calibration)); text answers use per-type temperatures (`serve_config.json`).
- A request without an image takes exactly the text path above.

This example uses `example_receipt.png` from this repository:

```python
import base64, json, urllib.request
img = base64.b64encode(open("h2o-lightning-4b/example_receipt.png", "rb").read()).decode()
req = {"state": {"receipt": "data:image/png;base64," + img,
                 "claim": {"employee": "J. Ortiz", "category": "office supplies", "amount": "444.26"}},
       "questions": {
         "matches":  {"type": "noul", "instructions": "The receipt total equals claim.amount.",
                      "criteria": {"true": "Same amount", "false": "Different amount"}},
         "items":    {"type": "choice", "instructions": "How many item lines are on the receipt?",
                      "criteria": {"three": "3", "four": "4", "five": "5", "six": "6"}},
         "legible":  {"type": "score", "instructions": "How legible is the receipt?",
                      "criteria": ["Unreadable", "Partly readable", "Fully readable"]}}}
r = urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8741/v1/systemone", json.dumps(req).encode(),
                                                  {"Content-Type": "application/json"}))
print(json.dumps(json.load(r), indent=1))
```

The response (rounded here):

```json
{"model": "h2oai/h2o-lightning-4b",
 "answers": {
   "items": {"type": "choice", "choice": "six", "confidence": 0.730, "probabilities": {"five": 0.130, "four": 0.043, "six": 0.798, "three": 0.029}},
   "legible": {"type": "score", "legend": {"0": "Unreadable", "1": "Partly readable", "2": "Fully readable"}, "score": 1.818, "confidence": 0.866, "probabilities": {"0": 0.048, "1": 0.086, "2": 0.866}},
   "matches": {"type": "noul", "noul": 0.894}},
 "probability_source": "native", "effort_used": {"passes_per_decision": 1, "tier": "fast"},
 "usage": {"images": 1, "input_tokens": 585, "latency_ms": 141.0, "output_tokens": 3, "processed_input_tokens": 1489},
 "attention_mode": "bidirectional"}
```

`usage.input_tokens` includes the image tokens; `usage.images` counts the images read.

**Status codes.** An input the shim cannot take gets HTTP 422, which the runner scores as one wrong answer. That covers:
- more than 255 options;
- an unknown question type or a malformed question;
- more than 4 images, or an image that is not valid base64 image data.

An empty request gets 400. vLLM's 401, 403 and 429 pass through. Any other vLLM failure is a 502, which counts toward the
runner's three-consecutive-failures stop.

**Tests** (no GPU): `python3 h2o-lightning-4b/test_shim.py` and `python3 h2o-lightning-4b/test_security.py`.

### Long inputs

A request whose prompt fits the server's context (`MAX_LEN`, 40,960 tokens by default) is read whole.
When a question's prompt would not fit, the shim shortens the record for that question only. It uses BM25 to keep the
parts of the record most relevant to the question and its options, with their headings, until the prompt fits. If no
part of the record matches, it keeps the record's head and tail around a `...` line. The question and its options are
never shortened in this step. Each question in a request is fitted separately, and image tokens are counted. In the
rare case where a question does not fit even without its record, the shim answers it without the record and shortens
its instructions, then the option descriptions, until it fits. The option names, their order and the answer keys stay
as sent. A long input never gets an error. `effort_used.state_selection` reports what was shortened, and
`usage.input_tokens` still counts the full input. To keep more of a long record, start the server with a larger
`MAX_LEN`. `SHIM_SELECTOR=headtail` uses a head-and-tail cut at 32,000 record tokens instead, for comparison
only. Under it, a question whose prompt would not fit with that cut gets the record cut further, to the room its own
prompt leaves, so it also never gets an error.

**Measured (our padded test, not a benchmark).** We padded 331 Decision Index and JevBench public items to 60,000
tokens each, with the original record placed at the start, the middle or the end (993 requests), and read them on one
GPU at the default 40,960-token context. Read unpadded, the same items score 61.3 % correct.

| over-long record handling | correct | start | middle | end |
|---|---|---|---|---|
| BM25 selection (default) | **46.0 %** | 45.9 % | 38.7 % | 53.5 % |
| head and tail, 32,000 tokens (`SHIM_SELECTOR=headtail`) | 41.9 % | 46.8 % | 27.5 % | 51.4 % |
| head and tail at the context (39,000 tokens) | 40.9 % | 46.5 % | 26.4 % | 49.8 % |

The last row was read without the per-question fit: 6 of its 993 requests were refused for length, and its
percentages are over the 987 that were answered.

BM25 selection is ahead mostly where the relevant text sits in the middle of the record. On the same requests it is
right where the 32,000-token head-and-tail cut is wrong 60 times, and wrong where that cut is right 19 times (paired
exact test, p = 4 × 10⁻⁶). It reads more of the record than the 32,000-token cut: a median of 38,495 tokens processed
per request against 32,133.

### Tokenizer

The model was trained with `Qwen2Tokenizer` (`tokenizer_config.json`). From transformers 5.18, a checkpoint whose
`config.json` names Qwen3.5 is loaded with `Qwen3_5Tokenizer` instead, which splits some Devanagari and Arabic text
differently (8 of the 24 probes in `tokenizer_contract.json`). `tokenizer/` holds the same five tokenizer files without
a `config.json`, so it loads as `Qwen2Tokenizer`; `serve.sh` passes it to vLLM with `--tokenizer`, and at start-up the
shim checks that vLLM reproduces all 24 probes (otherwise every request is a 503 that names `--tokenizer`, and
`serve.sh` stops with that reason).
transformers may log a warning about an "incorrect regex pattern" for this tokenizer; leave `fix_mistral_regex` unset:
the shipped split is the one the model was trained with.

Every result above was read with `Qwen2Tokenizer`, as `serve.sh` serves it.

### For benchmark maintainers: JevBench

**For benchmark maintainers: run it this way for our measured score.** This is the configuration behind the 206 / 231 in [Measured](#measured): two-way reading on one
engine, one read per question, the shipped calibration, with images and Box questions on as in normal serving (there
is no setting to turn them off). Use it as written; there is nothing to choose.

**GPU.** The 206 / 231 was read with this harness on one NVIDIA L40S (48 GB).

**1. Install** vLLM 0.30.0 and our per-request attention build, and download the model, exactly as in
[Run it](#run-it) (the pip block, then the 30-file block checked against
`engine/vllm_per_request_attention.SHA256SUMS`).

**2. Serve** with the one shipped command, and wait for its ready line:

```bash
bash h2o-lightning-4b/serve.sh
```

It starts one engine (`ONE_ENGINE=1`, `--attention-backend TRITON_ATTN`, `MAX_LEN` 40960), reads every question
two-way, and warms up every path before it prints `H2O-Lightning-4B ready on http://127.0.0.1:8741/v1/systemone`.
Until then `/health` answers HTTP 503 with `"warming": true`, so a runner that waits for `/health` 200 (or for the ready
line) never times a cold server.

**3. Run JevBench's harness** against it:

```bash
cd <JEVBENCH> && python3 -m jevbench.cli run \
  --tasks datasets/public/easy.jsonl,datasets/public/original.jsonl,datasets/public/hard.jsonl \
  --adapter typesafe --endpoint http://127.0.0.1:8741 --key-env '' --model h2oai/h2o-lightning-4b \
  --cost-basis self_hosted_gpu --reserve-usd 0 --results <OUT>/results.jsonl --raw-dir <OUT>/raw \
  --ledger <OUT>/ledger.jsonl --manifest <OUT>/manifest.json --run-label h2o-lightning-4b --delay-s 0
```

**Expected result:** 206 / 231 correct (easy 48/48, standard 72/72, hard 86/111), all 231 answered and valid. A
setup that gives clearly less is not the configuration above.

**Timing and cost.** One decision per request, sent one at a time. Each decision is one forward pass with one output token (no second read); `usage.input_tokens` is the
decision's prompt, counted once; `usage.output_tokens` is one per answered question.

**Do not change:** the engine (no `TWO_WAY=0`, which reads one-way and scores lower: 202 / 231; no two-engine layout); the
temperatures and yes/no floor in `serve_config.json` (as shipped); `VLLM_PATCHES` (for stock vLLM only; `serve.sh`
refuses it here); the batch budget (`serve.sh` keeps `--max-num-batched-tokens` at `MAX_LEN`, because a two-way prompt
is prefilled whole); any request option that reads a question more than once.

### For benchmark maintainers: Decision Index

**For benchmark maintainers: run it this way for our measured score.** This is the configuration behind our Decision Index 0.3 results in [Measured](#measured) (text 63.21, vision 69.87): two-way reading
on one engine, one read per question, every record read whole, with images and Box questions on as in normal serving
(there is no setting to turn them off). Use it as written.

**GPU.** Measured on NVIDIA L40S (48 GB) GPUs. The text settings (`MAX_LEN` 131072 at `GPU_UTIL` 0.70) assume a
48 GB GPU; a smaller one may need a higher `GPU_UTIL` (or a lower `MAX_LEN`, which then cuts long records).

**1. Install** exactly as in [Run it](#run-it) (vLLM 0.30.0 with the 30-file per-request attention build).

**2. Serve** with `serve.sh`'s default one engine (two-way; `TWO_WAY=1`, `ONE_ENGINE=1`) and
these settings, restarting the server between the two halves; wait for the ready line each time:

| setting | text | vision |
|---|---|---|
| `MAX_LEN` | 131072 | 40960 (the default) |
| `serve_config.json` `prompt.max_state_tokens` | 1000000 (shipped: 32000), so no record is trimmed | 32000 as shipped (vision rows carry no record) |
| `GPU_UTIL` | 0.70 | 0.70 |
| images and Box questions | on (as shipped; no setting) | on (as shipped; no setting) |

```bash
# text: raise the state limit (keep a copy of the shipped file and put it back afterwards), then serve
cp h2o-lightning-4b/serve_config.json h2o-lightning-4b/serve_config.json.shipped
python3 -c "import json; p='h2o-lightning-4b/serve_config.json'; c=json.load(open(p)); c['prompt']['max_state_tokens']=1000000; json.dump(c, open(p, 'w'), indent=1)"
MAX_LEN=131072 GPU_UTIL=0.70 bash h2o-lightning-4b/serve.sh
# vision: stop the text server, put the shipped serve_config.json back, then serve
mv h2o-lightning-4b/serve_config.json.shipped h2o-lightning-4b/serve_config.json
GPU_UTIL=0.70 bash h2o-lightning-4b/serve.sh
```

The `max_state_tokens` edit is optional: a record that fits `MAX_LEN` is never cut.

**3. Run the kit** (edition 0.3, the official scorer; Python 3.11 or later), in its own environment, against the server:

```bash
python3 -m venv kit && kit/bin/pip install "decision-index[vision] @ git+https://github.com/apolinario/decision-index@f8552a13b643d39f61185f5951bb5fed16bedf51" pillow==13.0.0 numpy
kit/bin/decision-index suite download --edition 0.3 --dir suite-0.3
kit/bin/decision-index run --edition 0.3 --suite-dir suite-0.3 --engine http --option base_url=http://127.0.0.1:8741 --option model=h2oai/h2o-lightning-4b --out runs/text
kit/bin/decision-index score --edition 0.3 --suite-dir suite-0.3 --results runs/text/results.jsonl --engine http --out runs/text/score
kit/bin/decision-index vision run --dir WORK/vision --engine decide --option base_url=http://127.0.0.1:8741 --option path=/v1/systemone --option protocol=decisions --option model=h2oai/h2o-lightning-4b --option max_pixels=1638400 --workers 16 --out runs/vision
kit/bin/decision-index vision score --dir WORK/vision --results runs/vision/results.jsonl --out runs/vision/score
```

- The text index is `runs/text/score/index.json` (`"index"`), the vision index `runs/vision/score/vision-scores.json`
  (`"public_vision_index"`).
- One text run in a single process is slow on one GPU. The measured text run was split as a speed-up only: the
  kit's row list (rows unchanged) into 16 files round-robin (row i to file i mod 16), each read by its own
  `decision-index run --rows` against the same server, the untouched results concatenated and scored by
  `decision-index score`:

  ```bash
  kit/bin/python -c "
  import gzip, json, pathlib
  from decision_index.suite.io import Suite
  s = Suite(pathlib.Path('suite-0.3'), '0.3'); s.verify(strict=True); out = pathlib.Path('shards'); out.mkdir(exist_ok=True)
  rows = [l if l.endswith('\\n') else l + '\\n' for p in (s.row_paths if isinstance(s.row_paths, (list, tuple)) else [s.row_paths])
          for l in (gzip.open if str(p).endswith('.gz') else open)(p, 'rt', encoding='utf-8') if s.in_edition(json.loads(l)['_evaluation'])]
  fs = [open(out / f'shard{i:02d}.jsonl', 'w', encoding='utf-8') for i in range(16)]
  [fs[i % 16].write(r) for i, r in enumerate(rows)]"
  for i in $(seq -f %02g 0 15); do
    kit/bin/decision-index run --edition 0.3 --suite-dir suite-0.3 --engine http --option base_url=http://127.0.0.1:8741 \
      --option model=h2oai/h2o-lightning-4b --rows shards/shard$i.jsonl --out runs/text/shard$i > runs/text.shard$i.log 2>&1 &
  done; wait
  cat runs/text/shard*/results.jsonl > runs/text/results.jsonl    # then the score command above
  ```

- Build the vision suite (`WORK/vision`) with the kit's own builder and Microsoft's core-fonts Arial Bold: the kit
  draws Mind2Web's box labels in Arial Bold, and only that font reproduces the pinned images (see the vision note
  under Measured). The file is `arialbd.ttf` from `arial32.exe` (https://downloads.sourceforge.net/corefonts/arial32.exe;
  sha256 of `arial32.exe` `85297a4d146e9c87ac6f74822734bdee5f4b2a722d7eaa584b7f2cbf76f478f6`, of `arialbd.ttf`
  `4044aa6b5bebbc36980206b45b0aaaaa5681552a48bcadb41746d5d1d71fd7b4`):

  ```bash
  curl -L -o arial32.exe https://downloads.sourceforge.net/corefonts/arial32.exe   # check its sha256 against the one above
  cabextract -L -F '*.ttf' arial32.exe        # gives arialbd.ttf; check its sha256 against the one above
  kit/bin/decision-index suite rebuild --vision --work WORK --font "$PWD/arialbd.ttf"
  kit/bin/decision-index vision verify --dir WORK/vision
  ```

  `vision verify` must pass on all 11 benchmarks; never run vision with `--no-verify`. For the measured suite only
  Mind2Web was rebuilt with this font by the kit's own builder (the other ten sets come from an earlier build of the
  same kit), and the suite passed `vision verify` on all 11.

**Expected result:** text index 63.21 (140,178 scored rows) and public vision index 69.87 (12,210 rows); run-to-run
differences of up to about 0.3 are normal.

**Do not change:** the engine (no `TWO_WAY=0`); the temperatures and yes/no floor in `serve_config.json` (as shipped);
`VLLM_PATCHES`; the batch budget; `--no-verify` for vision; the font for the vision suite (Arial Bold, as above).

### For benchmark maintainers: ImageJevBench Box track

Ask a Box question through the package, not a chat prompt. On a stock vLLM chat endpoint the weights answer a box but
usually without a stated confidence: in this model the box's confidence is not a number it writes, it is computed by
the shim from the box generation's own token probabilities and calibrated (the `confidence` field below). A chat
harness that reads a self-stated `"confidence"` key will find it missing on most answers.

Run it like this, one request at a time on one GPU:

```bash
hf download h2oai/h2o-lightning-4b --revision v1.4.2 --local-dir h2o-lightning-4b
bash h2o-lightning-4b/serve.sh          # no flags; serves http://127.0.0.1:8741
```

One request per item, the image in the record and one `box` question that names it:

```bash
curl -s http://127.0.0.1:8741/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": {"photo": "data:image/jpeg;base64,<the image, unchanged>"},
  "questions": {"where": {"type": "box", "instructions": "the leftmost dog in `photo`"}}}'
```

Read `answers.where.box` (`left`, `top`, `right`, `bottom`, fractions of the image from the top-left corner) and
`answers.where.confidence` (the calibrated probability that the box overlaps the target with IoU >= 0.5). If
`answers.where.found` is false, the box is the whole image and the confidence is 0. `present` is the probability that the named
object is visible, a probability from 0 to 1; it is not the box's score. This is the same request our hosted service answers.

Measured on our own out-of-distribution box set (RefCOCOg val, 600 referring expressions, no board images), through
exactly this request on this package: mean IoU 79.8, Acc@0.5 85.7 %, confidence ECE 0.0695 against IoU >= 0.5
(100 x (1 - ECE/0.5) = 86.1).

### Decision Index profile (`PROFILE=di`)

`PROFILE=di bash h2o-lightning-4b/serve.sh` serves the same weights with one extra step, for the Decision Index. It is
off unless you set it; the default serving, JevBench and the examples on this card do not use it.

**What it does.** A choice or score question whose top answer probability is under 0.8 is read a second time, in the
same reading mode, with the request written twice in the prompt (the second copy follows the line "Read the same input
again before answering:"). Its answer is 2/3 of the first reading's probabilities plus 1/3 of the second's. Yes/no
questions are read once (their served probability is never under 0.8). Image requests are read once. A second reading
that would not fit the context window (for example a record that was already shortened to fit) is skipped, and the
first answer stands; a request never fails because of the profile. With the profile on, each response carries
`effort_used.reread`, an object with `below` (0.8), `first_weight` (0.6667) and `questions` (how many of the request's
questions were read again).

**Measured** on one NVIDIA RTX PRO 6000 (96 GB) per arm, the same build and weights, the profile against the default
serving at the profile's yes/no floor (0.801; the shipped default has it off):

| | `PROFILE=di` | default |
|---|---|---|
| Decision Index 0.3 public text index (the kit's own scorer; the whole text run, 140,620 rows) | **63.64** | 63.19 |
| calibration error, all 140,620 text rows (274,729 questions with a gold answer; lower is better) | **0.0686** | 0.0706 |
| input tokens per request, mean, all 140,620 text rows | 1,819 | **956** |
| questions read a second time, all 140,620 text rows | 21.9 % (70,814 of 323,259) | — |
| latency, one request at a time, a 500-row sample of the text rows: median / mean / 80th / 95th percentile (nearest rank), ms | 44 / 121 / 142 / 453 | **25 / 80 / 122 / 349** |
| input tokens per request, mean, the same 500-row sample (333 of its 2,270 questions read a second time) | 2,360 | **1,296** |

The default column reproduces the L40S text run at the same floor (63.16 and 0.0705) within 0.03 and 0.0001. Paired over the same rows, the text index gain is +0.45 [+0.29, +0.63] (the kit's scorer; bootstrap over
request groups within each benchmark, 200 draws, 95 % interval), and every area's point estimate is up (arts +0.32
[−0.10, +0.78]). Benchmark by benchmark, the profile is lower on MuSR (−1.2 points; within run-to-run noise, paired
exact test p = 0.11), ACOS (−1.1) and, outside the index, schema-guided dialogue (SGD, −2.1), the last two beyond
noise (p < 10⁻⁶); every other benchmark is within 0.2 points of the default or higher, the largest gains on CRUXEval
(+1.8), GPQA Diamond (+1.5), NLI4CT (+1.2) and HoVer (+1.0). Latency stays far under the Decision Index's 1,000 ms
single-request rule; the cost is 1.9× the input tokens over the whole text run (1.8× on the 500-row sample, which is
every 249th row of the suite's selected rows, both arms reading the same rows on one engine).

**Held-out new-domain proxy (ours, not the Decision Index).** On a second held-out new-domain set of ours (7,107
questions in 12 task families: ten LegalBench tasks, medical abstracts and TREC-COVID retrieval; not the
3,724-question, 13-family set in Measured), re-reading below 0.8 with this 2:1 weighting scored +1.18 [+0.55, +1.82]
on the skill composite (paired bootstrap, 95 % interval), and +1.31 [+0.53, +2.14] with the plain mean of the two
readings. The gain is concentrated in the LegalBench tasks: medical abstracts +0.4 [−0.5, +1.2] and TREC-COVID −0.4
[−1.3, +0.6], neither significant. The 2:1 weighting was selected on held-out Decision Index slices after the
plain-mean rule passed. The Decision Index numbers in [Measured](#measured) are the package as shipped.

**How to run it for the Decision Index text half:** exactly the recipe above, with `PROFILE=di` added to the text
server's command: `MAX_LEN=131072 GPU_UTIL=0.70 PROFILE=di bash h2o-lightning-4b/serve.sh`. The vision half is
unchanged (images are read once), so serve it without the profile.

## See it in action

Three demos recorded with an earlier version of the model: an operations inbox deciding claims against a written
policy, a web agent choosing vendors in real browsers, and DOOM played to the exit. Companies, people and amounts are
fictional.

<video src="https://huggingface.co/h2oai/h2o-lightning-4b/resolve/main/assets/demos/demos_reel.mp4" poster="https://huggingface.co/h2oai/h2o-lightning-4b/resolve/main/assets/demos/demos_reel_poster.jpg" controls autoplay muted loop playsinline width="100%"></video>

[![H2O-Lightning-4B: full-length demo runs on YouTube](https://img.youtube.com/vi/2Qp04Wu0A14/maxresdefault.jpg)](https://youtu.be/2Qp04Wu0A14)

## Measured

**This card describes v1.4.2** (`main`; pin `--revision v1.4.2`). Each image is scaled to at most 1,638,400 pixels (see
[Image calibration](#image-calibration)); the Decision Index profile is opt-in (see
[Decision Index profile](#decision-index-profile-profiledi)); under the non-default `SHIM_SELECTOR=headtail` the record
is fitted to the context per question (see [Long inputs](#long-inputs)); and a request's `kwargs.attention_mode` sets its
attention mode (see [One engine, both modes](#one-engine-both-modes)). How each number was read is under Results.

The weights are a fine-tune of Qwen3.5-4B (see
[What it was trained on](#what-it-was-trained-on)), for both attention patterns (see
[Two-way reading](#two-way-reading-recommended)), served two-way on one engine of our vLLM build, with Box questions
always on. Text answers use the per-type temperatures in `serve_config.json`; image answers use their own temperature,
1.0 (see [Image calibration](#image-calibration)). The vLLM build includes a fix for a crash in the Gated DeltaNet
prefill graphs with 16 or fewer sequences in flight, and `serve.sh` stops with the shim's reason when vLLM's tokenizer is
not the one the model was trained with (see [Tokenizer](#tokenizer)). Over-long records are BM25-selected to fit and a
request never fails for length; inputs that fit are read whole (0 Decision Index 0.3 public text rows and 0 JevBench
public items exceed the limit; see [Long inputs](#long-inputs)). Older versions: see the repo's tags.

**Results**, against the previous release (v1.4.0), with vLLM 0.30.0 on NVIDIA L40S (48 GB) GPUs, each release through
its own `serve.sh` with no flags (two-way, one engine of the vLLM build) unless a row says otherwise, every question
answered. v1.4.2's default was read on 2026-10-26 on v1.4.1's serving (the same answers for text), the Decision Index text
rows on 2026-10-28 with the yes/no floor off as shipped, the vision index on 2026-10-28 at v1.4.2's image cap; v1.4.0 on
2026-10-24.

| | **v1.4.2 default** | v1.4.0 |
|---|---|---|
| JevBench's 231 public items, JevBench's own CLI: correct | **206 / 231 (89.2 %)** · 48/48 · 72/72 · 86/111 | 206 / 231 |
| held-out decisions on the Decision Index's skills (2,351 questions, 15 task families): skill (difference not significant) | 81.54 | 81.45 |
| the new-domain set (3,724 questions, 13 task families): skill (difference not significant) | 59.86 | 59.44 |
| six task families that the added training data covers (2,891 questions): skill | **67.99** | 50.08 |
| Decision Index 0.3 public suite, the kit's own scorer: text index (140,178 rows) / vision index (12,210 rows) | **63.21 / 69.87** | 62.38 / 69.03 |
| calibration error on the Decision Index text rows (274,729 questions; lower is better) | 0.0701 | **0.0640** |
| one-way reading (`TWO_WAY=0`): JevBench 231 correct · Decision Index text / vision index · calibration error | 202 / 231 · 60.86 / 67.56 · 0.0801 | not measured |
| mean input tokens per decision on JevBench's 231 items | 654 | 654 |

The held-out set on the Decision Index's skills is dev slices of the public training data behind the Decision Index's
tasks, plus our own authored dev set. These tasks' training splits are in our mix, so every question was removed that
is an exact twin of a training row, shares a word 9-gram with one, or shares at least 80 % of its word 13-grams with
one (at least 50 % against the rows added in this release): of 4,789 questions, 1,233 were removed against the earlier
training data and 1,205 more against the added rows, leaving 2,351 in 15 task families. A stricter cut (at least 50 %
of 13-grams shared throughout) leaves 2,067 questions; there v1.4.1 is +0.02 [−0.68, +0.69] against v1.4.0. Most of the
9-grams behind the second removal are instruction and option wording that the added rows share with whole dev tasks;
counting only matches of each question itself (9-grams that occur in five or more dev questions set aside) keeps 3,130
questions, where v1.4.1 is −0.78 [−1.74, +0.26] against v1.4.0, and lower on schema-guided dialogue (−12.3
[−19.9, −6.1] on that task), a task whose dev questions the main cut removes.

The new-domain set is 13 task families whose datasets do not occur in the training data, checked against every
training row by word 13-gram overlap. The six families in the row below it (argument quality, choosing a function to
call, table fact checks with one and with several claims, multi-intent detection, vulnerability severity) come from
datasets the earlier training data did not include; this release's added training data covers them, so they are
reported on their own. Skill: per
task family, accuracy rescaled so that chance is 0 and every answer right is 100; averaged within each area, then
combined with fixed area weights (knowledge 0.258, language 0.258, retrieval 0.200, tools 0.183, arts 0.100,
renormalised over the areas a set has: the new-domain set has no arts tasks).

v1.4.1 against v1.4.0 (paired bootstrap over requests within each task family, 2,000 draws, 95 % intervals):
+0.09 [−0.50, +0.68] on the held-out set and +0.42 [−0.70, +1.49] on the new-domain set, both within noise; +17.90
[+14.74, +21.01] on the six covered families; on JevBench's public items the same count, one item gained and one lost.
v1.4.1 is stronger on retrieval in both sets (product-search relevance in the held-out set +2.0 [+0.5, +3.9]; lobbying
relevance +6.9 [+2.1, +12.4] and legal definitions +4.8 [+1.6, +8.9] in the new-domain set) and weaker on language in
the held-out set as a whole (−1.49 [−3.08, −0.14]); no task in either set is significantly worse. One-way reading of the
same weights scores lower than two-way: −2.17 [−3.72, −0.70] on the held-out set against v1.4.0 two-way, +0.45
[−1.74, +2.62] on the new-domain set.

The Decision Index rows are our own runs of the public 0.3 kit (not a leaderboard result), read on the files
published here as [the maintainers' section above](#for-benchmark-maintainers-decision-index) describes. Text: the shipped
`serve_config.json` (yes/no floor off) with `max_state_tokens` raised to 1,000,000 (so no record was cut) and `MAX_LEN`
131072, the kit's rows read in 16 round-robin shards, one L40S per reading mode; the kit scores 140,178 of the 140,620
answered rows. Vision: the shipped package (`serve.sh`, no flags; image cap 1,638,400
pixels) at `MAX_LEN` 40960, on one NVIDIA RTX PRO 6000. The score is the kit's index (0-100), not percent correct. The calibration error is over every question of the
text rows with a gold answer, the top option's probability in 15 equal-width bins; v1.4.0's value was read with the
yes/no floor of 0.801. A screening against the training rows other than those this release adds (word 9-grams) found
1,444 of the 140,178 text rows sharing text with them; on the text run at the floor of 0.801 (text index 63.16) the index
without them was 63.09 (−0.07).

Per-row results and the Decision Index toolkit's score files are public for v1.4.1's text run (63.16, yes/no floor 0.801)
and vision run at v1.4.1's image cap (69.42), and for v1.4.2's text run with the Decision Index profile (63.64) and
vision run at the 1,638,400-pixel cap (69.87):
[h2oai/h2o-lightning-4b-decision-index](https://huggingface.co/datasets/h2oai/h2o-lightning-4b-decision-index).

### Image calibration

Image answers use their own temperature, 1.0, fitted out of distribution (`serve_config.json`, `"image"`
and `two_way.image_temperature`; text answers keep their per-type temperatures). A temperature
rescales the option scores, so every image answer keeps its choice; only the probabilities move. At 0.65 the top
option's probability ran ahead of how often it was right on unfamiliar images. Calibration error of the top option
(10 equal-width bins; lower is better), 0.65 → 1.0, the same answers re-scored:

| image questions | questions | correct | 0.65 | 1.0 |
|---|---|---|---|---|
| Decision Index 0.3 public vision rows (the run above, at the 1,638,400-pixel cap) | 12,210 | 76.2 % | 0.112 | **0.059** |
| MMStar, four-option questions | 1,493 | 68.3 % | 0.175 | **0.081** |
| image questions of the kinds it was trained on | 3,961 | 91.6 % | **0.018** | 0.078 |

On images like those it was trained on, where it is right more than 90 % of the time, 1.0 leaves the probabilities
somewhat below the accuracy; on the rest they track it. The temperature cannot move the Decision Index vision index,
which counts answers only; the larger image cap below does. The MMStar and trained-kinds rows were read with images scaled to at most 1,048,576 pixels.

**Image cap.** Each image is scaled to at most 1,638,400 pixels, so an image costs up to about 1,600 prompt tokens (about
1,000 at a cap of 1,048,576 pixels); 5,742 of the 12,210 Decision Index vision rows have a larger image than 1,048,576
pixels. The Decision Index 0.3 public vision index is
69.87 at this cap against 69.42 at 1,048,576 pixels; in two paired runs of the same weights at the two caps the difference
was +0.67 [+0.08, +1.34] and +0.62 [+0.04, +1.31] (95 % intervals), with no benchmark of the suite worse beyond noise, and
image requests used about 25 % more input tokens. On MMStar (1,493 four-option questions, two-way) accuracy is 68.65 % at
both caps and the calibration error 0.0788 at this cap and 0.0769 at 1,048,576 pixels (+0.002 [−0.004, +0.008]). Only 41 MMStar
images are larger than 1,048,576 pixels; on those, five answers changed over the two reading modes (two two-way, three
one-way), all five from right to wrong.

ImageJevBench v0.3.0 ran v1.4.1's 2026-10-28 files (these weights at image temperature 1.0, with v1.4.1's image cap of
1,048,576 pixels) on 2026-10-28 ([results](https://benchmarkheaven.com/api/decision-results/imagejevbench/v0.3.0/json)): capability 71.84, intelligence 55.48, calibration 88.19, composite
68.51. This release is not yet on the board.

## Two-way reading (recommended)

**What it is.** A decoder reads a prompt one way: each token attends only to what comes before it, and the answer is
read at the last position. The weights are trained to answer under two patterns: **one-way** (causal, as
every text generator and stock vLLM read a prompt) and **two-way**: bidirectional attention on the model's
full-attention layers, so the answer position sees the record, the question and the options in both directions
before the readout (the Gated DeltaNet layers, the model's linear-attention layers, stay causal). It is one forward
pass and one readout in both modes, and the same shim, request format and calibration.

**Why both.** Two-way reads better: the answer position sees the whole prompt. One-way needs nothing beyond stock
vLLM's generate mode and uses the prefix cache. The weights were trained to handle both, and on the one engine each request can
choose (`"attention_mode": "bidirectional"` or `"causal"`, also `"two-way"` / `"one-way"`; without it, two-way).

**When to use which.** Two-way (the default) for decisions, text or images, on one GPU with the vLLM build: the
recommended choice. One-way when you cannot install the build (stock vLLM), when many questions share one long record
and every read should use the prefix cache (a two-way read does not).

### One engine, both modes

`bash h2o-lightning-4b/serve.sh` serves two-way, one-way and the Box question from **one** generate-mode vLLM of our
build, [h2oai/vllm](https://github.com/h2oai/vllm) at commit `b05cc29ab813895947954c268c4ec41ca0da1306` (vLLM 0.30.0
plus 30 changed Python files; installation under [Run it](#run-it)), each request choosing its mode. A request
carrying `vllm_xargs {"attention_mode": "bidirectional"}` is prefilled with the full-attention layers reading both ways
and the Gated DeltaNet layers (the model's linear-attention layers) causal, and the answer comes back through the
ordinary `logprob_token_ids` path, the same readout as one-way. The shim sends that flag for every two-way read
(`SHIM_TWO_WAY_FLAG=1`, set by `serve.sh`), nothing for a one-way read or a Box generation. What the build does for a
flagged request: it schedules the whole prompt in one step (no chunked prefill, no block-aligned split of the
linear-attention state; a prompt longer than `--max-num-batched-tokens` is refused for that request, so `serve.sh`
sets it to `--max-model-len`), reads nothing from and writes nothing to the prefix cache (a two-way prefix is not
reusable; unflagged requests keep the cache), and allows one output token (`max_tokens` 1: the readout). Unflagged
requests are untouched: the engine is stock vLLM for them. The build runs the Triton attention backend
(`--attention-backend TRITON_ATTN`; the FlashAttention backend needs FA4 for a per-sequence causal flag); `serve.sh`
sets it. The two-way calibration (`serve_config.json` `two_way.temperature`, `two_way.noul_floor`,
`two_way.image_temperature`) ships with the one-way values, the ones every number above was measured with (the image
temperature is 1.0 in both modes; one-way and two-way reads of the same images fit the same value).

**Launching each mode.**

```bash
bash h2o-lightning-4b/serve.sh                              # two-way (default) and one-way per request: one engine of the build + the shim
TWO_WAY=0 bash h2o-lightning-4b/serve.sh                    # one-way only: one stock generate-mode vLLM + the shim
```

Every response states the mode it was read in (`"attention_mode"`). On the one-way fallback (`TWO_WAY=0`) a request
asking for `"attention_mode": "bidirectional"` gets HTTP 400 (there is no two-way engine), never a silent one-way
answer. The mode can also be given as `"kwargs": {"attention_mode": ...}` (the form the hosted service takes); a
request that gives both with different values gets HTTP 400. The `/v1/decisions` route takes the same `attention_mode`
field. By hand: step 1's two-way command under
[Run it](#run-it) and the shim with `SHIM_TWO_WAY_FLAG=1` (step 2).

```bash
curl -s http://127.0.0.1:8741/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": {"ticket": "Checkout returns HTTP 500 for every customer since 09:12.", "plan": "enterprise"},
  "attention_mode": "causal",
  "questions": {"outage": {"type": "noul", "instructions": "Is this a full outage?",
                           "criteria": {"true": "yes", "false": "no"}}}}'
```

**The start-up guard.** Before its first answer the shim reads three fixed probes flagged and unflagged on the same
engine: the flagged answers must be within 0.05 of the answers recorded on the release weights (`serve_config.json`
`two_way.probe_reference`) and must differ from the unflagged ones. An engine without the build ignores the flag and
answers one-way; an engine on other weights or another dtype answers differently: either is refused with HTTP 503 and
the reason, re-checked after 10 s (`SHIM_TWO_WAY_RETRY_SECONDS`).

### Image references and the Box question

Images can be sent by reference: put each image once under `"assets"`
(`{"<ref>": {"type": "image", "format": "png", "data_base64": "..."}}`, `"jpg"` for JPEG) and write `<ref>` wherever
the image belongs in `state`; the shim replaces the reference with the image. References match as plain text, so
every occurrence counts, even inside a longer word (`photo` also matches "a photo of"); each distinct reference is
sent to the model once, and every occurrence points at that image. Pick references that cannot occur in your text,
such as `IMG_1`. PNG and JPEG only, 16 MiB per file,
every asset referenced at least once, no URL fetching; a malformed asset map is a 400.

A `box` question, ``{"type": "box", "instructions": "the coffee mug in `photo`"}``, answers with a bounding box
`{"left", "top", "right", "bottom"}` in fractions of the image, `confidence` (calibrated from the box generation's own token
probabilities), `present` (whether the named object is visible) and `found` (whether a box was
located; if not, the box is the whole image with confidence 0). `present` answers whether the named object is visible; it is not a score of the box. `confidence` is the score of the box. Box questions are on by default, in normal serving and in both benchmark runbooks above (there is no on/off setting): the box comes from one guided (JSON-schema)
generation, so the engine needs structured outputs (vLLM has them on by default); an engine without them refuses a
request with a box question with HTTP 422, and requests without one are unaffected. `box.mode` chooses how the box is found: `"generate"` (the default: one constrained generation of the box),
`"edges"` (each edge read as a distribution over positions, the coordinate its expected value) or `"hybrid"` (both,
the tighter box answered). `edges` and `hybrid` need a model trained on edge readouts; keep `generate` with this
release.

## Serving at scale

**Measured speed, H100 and L40S.** Each H100 figure carries its source; the speed of an engine does not depend on the
weight values (every release here is the same Qwen3.5-4B architecture), but answer-level figures (flips, bit-identity)
are specific to the weights they were read on.

| | H100 (80 GB) | L40S (48 GB) |
|---|---|---|
| one-way, one question per request, one at a time: p50 / requests per s | 20.9 ms / 42.7 [a] | 28.0 ms / 32.9 at 100-300 tokens; 69.3 ms / 15.1 at 800-1,200 tokens [c] |
| one-way, three questions per request, one at a time: p50 / decisions per s | 30.1 ms / 84.0 [a] | 89.7 ms / 10.6, records of 600-6,000 characters [c] |
| two-way, one question per request, one at a time: p50 | not measured | 28.2 ms at 100-300 tokens; 59.7 ms at 800-1,200 tokens [c] |
| step graphs 2048 instead of 512, one-way, about 1,000 tokens | 38.5 -> 34.6 ms; +7 / +4 / −1 % requests/s at 1 / 8 / 32 in flight; start +50 s; KV cache −1.2 % [b] | 71.1 -> 69.3 ms; within noise at 1 / 8 / 32 in flight; start 195 -> 391 s; KV cache −2.4 % [c] |
| image-processor cache off instead of on, three-question image decisions | unchanged one at a time; at most about 12 % fewer at 8 in flight [b] | 9.0 vs 8.9/s one at a time; 15.0 vs 14.8/s at 8 in flight [c] |
| `SHIM_CACHE_WRITE=first` instead of `all`, one-way | one request about 25 % faster; 8-18 % fewer decisions/s on three-question loads [b] | one request 65.1 -> 51.1 ms; three-question loads 8.5 / 12.1 / 12.2 / 9.5 vs 10.6 / 14.3 / 13.4 / 11.7 decisions/s at 1 / 8 / 16 / 32 [c] |
| patch A in the vLLM build, three-question one-way decisions | +7 % at 16, +10 % at 32 in flight; 600 of 600 reads bit-identical [b] | not measured |
| stock vLLM 0.30.0 with both patches, three-question decisions | 29.0 -> 78.1/s at 16 in flight, 81.0 at 64 [d] | not measured |
| `--quantization fp8` | 81.6 -> 99.2 decisions/s at 64 in flight; 21 of 687 answers flipped (McNemar p = 0.63) [d] | not measured |
| `--mamba-ssm-cache-dtype bfloat16` | 78.1 -> 81.7 decisions/s at 16 in flight; no answer flipped [d] | not measured |
| Box JSON under llguidance without free whitespace | 15 ms less per Box question [d] | 44 ms less per Box question [d] |
| another CPU job on the engine's physical cores | one request 26.6 -> 32.3 ms; 176 -> 155 decisions/s at 16 in flight [e] | not measured |
| GPU clocks locked | no measurable gain [b] | not measured |
| stock vLLM 0.30.0 (`TWO_WAY=0`) against our build, JevBench 231 one-way | 201 = 201, every answer identical; 600 of 600 reads bit-identical with this shim and the previous one [b] | 202 / 231, no failed request [c] |

Sources: [a] our live US host, 2026-10-26: this vLLM build (h2oai/vllm `b05cc29ab8`, prefill graphs on), one-way reads
under live traffic, on earlier weights of this model. [b] one H100, 2026-10-25: the previous vLLM build (h2oai/vllm
`a874119ca6` and `a0acf966cb`; the build here adds only the prefill-graph fix for 16 or fewer sequences in flight), v1.4.0
weights. [c] one L40S, 2026-10-26: this build and these weights. [d] our hosted engine, one H100, 2026-10-13: stock vLLM
0.30.0 (with both patches unless the row says otherwise), earlier weights, 687 graded development questions. [e] one
H100 host, 2026-10-20: an earlier build and earlier weights.

**Prefill graphs.** The vLLM build replays CUDA graphs for the Gated DeltaNet layers' prefill of steps up to 2,048
tokens, and `serve.sh` captures every graph shape during its warm-up (`VLLM_GDN_PREFILL_GRAPH_PRECAPTURE=1`), so no real
request pays a capture. The graphs take about 1.1 GB of GPU memory beyond the KV cache; on a 24 GB GPU set
`VLLM_GDN_PREFILL_GRAPH_MAX_TOKENS=1024` (about 0.5 GB) or a lower `GPU_UTIL`; `VLLM_GDN_PREFILL_GRAPH_MAX_TOKENS=0`
turns the graphs off.

**Step graphs.** vLLM replays CUDA graphs for whole steps up to `--max-cudagraph-capture-size` tokens (512 by
default); `serve.sh` sets it from `CUDA_GRAPH_MAX_TOKENS`: 512 when two-way is the default reading, 2048 with
`TWO_WAY=0`, the setting our hosted one-way engines use. Measured on one L40S with 800-1,200-token
prompts, 2048 instead of 512 on the one-way server: one request at a time 71.1 -> 69.3 ms, and 14.8 / 54.8 / 65.8 ->
15.1 / 53.2 / 66.4 requests/s at 1 / 8 / 32 in flight, within run-to-run noise; at 100-300-token prompts and 8 in
flight, 73.2 -> 57.7 requests/s (one run). On the two-way default 2048 reads no faster (59.7 -> 59.8 ms for one
request). With 2048 the server is ready in 391 s instead of 195 s, with 2.4 % less KV cache; label probabilities move
by at most 0.019 (600 questions, no answer changed). On this GPU 2048 bought nothing measurable: set
`CUDA_GRAPH_MAX_TOKENS=512` for a faster start. One more note from a profile on an L40S: a prompt just past 1,024 tokens
(1,025-1,031) adds a GEMM tile row and costs about 10 % more than one just under it.

**Engine settings `serve.sh` passes**, as our hosted engines run them: `--mm-processor-cache-gb 0` (vLLM's front-end
image-processor cache off: on our engines it went out of step with the engine's own cache on the first image after a
start and answered HTTP 500; on one L40S, with the cache on (4 GB) instead, three-question image decisions ran 8.9
instead of 9.0/s one at a time and 14.8 instead of 15.0/s at 8 in flight, JevBench's 231 items gave 206 either way, and
label probabilities moved by at most 0.036 on 600 questions (one answer changed), the same spread as between two
engines that differ only in their compiled graphs), and `--allowed-media-domains media.invalid`
(vLLM never fetches a URL: the shim downloads image URLs with its own checks and sends the engine data URIs). Each
engine configuration gets its own compile cache (`VLLM_CACHE_ROOT`, default `~/.cache/vllm/h2o-lightning-4b/<key>`, the
key a hash of the engine build, the reading mode, `MAX_LEN`, the step-graph size, the image settings and `VLLM_ARGS`):
vLLM 0.30.0 keys its compiled graphs without some of what changes them, so a graph compiled for one configuration
(images off, for one) was reused by another and failed or read differently. If you start `serve.sh` from a wrapper that
clears the environment (`env -i`), pass `VLLM_CACHE_ROOT` or `HOME` through.

**CPU.** At short prompts the engine is bound by its host CPU, not the GPU. Keep other CPU-heavy work off the cores the
engine runs on (opt-in: for example start `serve.sh` under `taskset -c <cores>`, whole physical cores).

**Clocks (opt-in, needs root).** One request at a time lets the GPU drop its clocks between steps. Locking them
(`sudo nvidia-smi -lgc <max graphics clock>`, the value from `nvidia-smi -q -d SUPPORTED_CLOCKS`; `sudo nvidia-smi
-rgc` resets) and the CPU's `performance` governor keep a step from starting slow; worth trying on GPUs that down-clock between requests.

**Prefix-cache writes (one-way reads).** With prefix caching on, vLLM splits a one-way prefill at the last 528-token
block of this model's linear-attention state, so the state there can be cached, and runs the rest as a second step. The
shim can ask the vLLM build not to write (`prefix_cache_write` false) where nothing would read it:
`SHIM_CACHE_WRITE=first` lets only the first question of a multi-question request write (the others read the record
from it) and a single question writes nothing, so it runs in one step. As shipped, `SHIM_CACHE_WRITE=all`: every read
writes (stock behaviour); `none`: no read writes. Measured on one L40S, one-way reads on the one engine: `first` takes
one 800-1,200-token request from 65.1 to 51.1 ms, but with three questions per request it serves fewer decisions per
second at every load (8.5 / 12.1 / 12.2 / 9.5 vs 10.6 / 14.3 / 13.4 / 11.7 at 1 / 8 / 16 / 32 in flight), so keep `all`
unless you send one question at a time at low load. A one-step read and the split read differ by at most 0.021 in
label probability (600 questions, no answer changed).

**Stock vLLM and our build.** The shim works the same against both. Stock vLLM 0.30.0 (`TWO_WAY=0`) accepts the
`prefix_cache_write` request field and ignores it, so there every read writes to the prefix cache and is split as
before; only our build runs the one-step read. Both return each prompt's token ids with the answer
(`return_token_ids`, a stock vLLM option), which the shim uses to count a shared record once in `usage` without
`/tokenize` calls; an engine that does not return them gets the `/tokenize` calls as before. Checked on one L40S
against plain stock vLLM 0.30.0 (`TWO_WAY=0`): JevBench's 231 items, 202 correct one-way, with no failed request.

**Images.** `MAX_IMAGES` above 4 costs no KV cache (vLLM reserves the same encoder budget for 4, 8 or 16 images per
prompt, measured), only prompt tokens: up to about 1,600 per image at the 1,638,400-pixel cap the shim sends. `serve.sh` passes the same count to the
shim (`SHIM_MAX_IMAGES`, at most 16), which refuses a request with more images.

These notes are for the one-way (generate-mode) engine on stock vLLM; the one-engine two-way default reads each
prompt whole and does not use the prefix cache. `VLLM_ARGS` reaches the engine with `serve.sh`.

**Why a stock server stalls.** Qwen3.5 interleaves 24 Gated DeltaNet (linear-attention) layers with 8 full-attention
layers. With prefix caching on, vLLM 0.30.0 keeps their recurrent state only at 528-token block boundaries (272 with
the bfloat16 state below), and its scheduler defers a request whose cached prefix ends on a state block written in the
same step, then stops scanning the waiting queue. The shim sends a decision's questions together over one shared record, so under load the engine runs
about one decision per scheduler step, however many are waiting. Zeroing the state of new sequences also synchronises
the GPU in each linear-attention layer in every step that starts new sequences.

**Two patches fix it**, in [`vllm_patches/`](vllm_patches/) (sha256 in `vllm_patches/SHA256SUMS`; vLLM 0.30.0 only):
`vllm030_scheduler_skip_same_step_mamba.patch` skips the deferred request for that step instead of ending the scan
(scheduling only), and `vllm030_gdn_initial_state_no_sync.patch` zeroes those states with `torch.where` (no GPU sync,
identical values). Patch A changes only which requests share a step, so under load results can differ by ordinary
BF16 batching noise, as they do on stock vLLM. Our vLLM build (`serve.sh`'s default engine) has both built in, so the
one engine needs no patches.
The patch files are for stock vLLM: `VLLM_PATCHES=1 bash h2o-lightning-4b/serve.sh` applies them to a stock vLLM 0.30.0 in the active
environment before starting it; it edits that install, so use a dedicated virtual environment. `serve.sh` refuses
`VLLM_PATCHES=1` on the one engine (the build's sha256 check would refuse every later start); use it with `TWO_WAY=0`.
Without `VLLM_PATCHES=1`, serve.sh leaves vLLM as installed.

**Flags** for many decisions in flight on the one-way engine: `--max-num-batched-tokens 8192` (on the two-way default,
`serve.sh` keeps `--max-num-batched-tokens` at `MAX_LEN`, because a two-way prompt is prefilled whole). With serve.sh,
pass flags in `VLLM_ARGS`, for example `TWO_WAY=0 VLLM_PATCHES=1 VLLM_ARGS="--max-num-batched-tokens 8192" bash
h2o-lightning-4b/serve.sh`. Through the shim, raise `SHIM_QUESTION_THREADS` (default 64) to at least three times the
decisions in flight.

**Optional, each one opt-in:**

- `--quantization fp8` (an FP8-capable GPU: Ada, Hopper or Blackwell; not the A6000): more decisions per second under
  load, but it changes some answers, mostly where the BF16 answer led by less than 0.1. The calibration temperatures in
  `serve_config.json` were fitted on BF16 output.
- `--mamba-ssm-cache-dtype bfloat16`: the linear-attention state in bfloat16 (prefix-cache blocks of 272 tokens instead
  of 528). Not measured with the build's prefill graphs.
- `--structured-outputs-config {"backend":"guidance","disable_any_whitespace":true}` (no spaces, so it fits `VLLM_ARGS`):
  the Box generation's JSON under llguidance without free whitespace, 15 ms less per Box question on an H100, 44 ms
  on an L40S and 54-58 ms on an A6000, valid boxes 20 of 20 on each. The Box confidence calibration was fitted with vLLM's default backend.

What we measured and did not adopt: vLLM's fine-grained Mamba prefix cache (`--enable-mamba-fine-grained-prefix-cache`,
fewer decisions per second), vLLM 0.31.0 (still one decision per step without the patches), and SGLang 0.5.21 (slower at
1-16 in flight; faster only at saturation, with FP8-like answer drift). For mixed traffic with long records, our hosted
service runs a second engine on the same GPU for records above 16K tokens, so long records do not hold up the short
decisions.

## Yes/no floor

As shipped, each yes/no answer carries its calibrated probability (`"noul_floor": 0` in `serve_config.json`, both
modes): an uncertain yes/no answer reads near 0.5, so a deployment that escalates uncertain answers to a larger model or
a person can flag it directly. The Decision Index profile (`PROFILE=di`) keeps the floor of 0.801 it was measured
with: there each yes/no answer is reported at no less than 0.801 on its chosen side. Out of distribution, on the
Decision Index 0.3 public text rows, the floor of 0.801 raised the yes/no calibration error (0.0413 two-way, 0.0485
one-way, against 0.0165 and 0.0197 with no floor), so it is off by default.

To set a floor yourself (a value in (0.5, 1); 0 turns it off), for both modes:

```bash
SHIM_NOUL_FLOOR=0.801 bash h2o-lightning-4b/serve.sh
```

The floor never changes the yes/no choice; threshold decisions use the calibrated probability (with a floor set, the
floored one). Choice and score answers are unaffected.

## What it was trained on

The weights are a fine-tune of Qwen3.5-4B in three stages: a text foundation (126,232 examples), a text
stage with some replay of the first (51,220), and a final stage that adds images, continued twice with amended mixes
(360,217 examples before the first amendment, 992,789 between the two, 692,693 after the second). In all, 2,223,151
training examples were read, 29,023 of them replays of earlier stages. Every example is a record (a document, ticket,
policy, conversation, game state, image...) with one typed question about it and a graded answer or a Box grounding
target, and the weights were trained for both attention patterns.

**Text and images.** 495,282 of the examples (22.3 %) carry images, 518,544 images in all, read through Qwen3.5-4B's
vision encoder, which fine-tuning did not change.

| Use case | Share of examples | Text examples | Image examples |
|---|---:|---:|---:|
| Everyday language and images | 44.4 % | 521,433 | 464,613 |
| Rules, policies and reasoning | 20.3 % | 421,458 | 30,519 |
| Support and operations | 7.9 % | 175,543 | 0 |
| Maths and numbers | 7.9 % | 174,539 | 150 |
| Coding, tools and software | 7.0 % | 155,972 | 0 |
| Games, simulations and music | 6.8 % | 150,592 | 0 |
| Safety | 4.5 % | 101,046 | 0 |
| Finance and commerce | 1.2 % | 27,286 | 0 |

Use cases are assigned per task family (over 900 families), so the split is approximate; nearly all image examples fall
under everyday language and images.

**Question types.** Choice 72.1 %, yes/no 18.5 %, score 5.9 %, and Box grounding (generating a box for a named object)
3.5 %.

## Limitations

- Evaluated mostly in English. Up to 255 options per question are accepted.
- The probabilities are calibrated for decision questions of this kind, not for open-ended text.
- Not a chat model: it answers one decision per question and does not generate explanations.
- Images: no video input.

## Disclosures

- No JevBench or ImageJevBench data, public or otherwise, was used for training.
- No rules keyed to any benchmark item's wording, id or answer; no network calls at serving time (except fetching an
  image URL a request supplies).
- Price basis for an evaluator: Qwen3.5-4B at bf16, one output token per decision; 654 mean input tokens on the
  public text set. Image tokens are counted in `usage.input_tokens`.

## Credits

The shim's handling of a client that hangs up before its answer arrives was contributed by mjvk in
[PR #5](https://huggingface.co/h2oai/h2o-lightning-4b/discussions/5).

## License

Apache-2.0. Built on [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) by the Qwen team (Alibaba Cloud),
Apache-2.0. Served by default with our build of [vLLM](https://github.com/vllm-project/vllm) 0.30.0 with per-request
attention, [h2oai/vllm](https://github.com/h2oai/vllm) at commit `b05cc29ab813895947954c268c4ec41ca0da1306`
(Apache-2.0); the one-way fallback (`TWO_WAY=0`) uses unmodified vLLM 0.30.0 (Apache-2.0).
