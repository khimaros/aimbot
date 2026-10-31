---
license: apache-2.0
base_model: h2oai/h2o-lightning-4b
library_name: llama-cpp
pipeline_tag: image-text-to-text
tags:
  - decision-making
  - calibration
  - jevbench
  - multimodal
  - qwen3_5
  - typed-decisions
  - decision-model
  - gguf
  - llama-cpp
---

![H2O Lightning: Decision Models](assets/banner.png)

# H2O Lightning 4B GGUF

GGUF files of [H2O-Lightning-4B](https://huggingface.co/h2oai/h2o-lightning-4b) for llama.cpp. For the model description,
training and general benchmarks, see the model page.

Requests with images use a temperature of 1.0, set in the native files' metadata (the `stock-` path reads it from the
shim's configuration).

The model answers typed decisions with probabilities: named `choice` options, true/false `noul`, ordered `score`
levels, and `box` (a bounding box in an image).

## Leading on Benchmarks

![Leading on Benchmarks: #1 of 46, Composite (open-weight Jev-class models; #2 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #2 of 46, Intelligence (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #4 of 46, Capability (open-weight Jev-class models; #10 of 55 Jev-class models, open or API), ImageJevBench edition v0.3.0; #2 of 170, Composite (open-weight Jev-class models; #12 of 201 Jev-class models, open or API), JevBench board of 2026-10-28; #1 of 4, Box Capability (open-weight Jev-class models; #1 of 5 Jev-class systems, open or API), ImageJevBench Box track (PREVIEW); #1 of 46, Composite (open-weight Jev-class models; #3 of 55 Jev-class systems, open or API), ImageJevBench computer-use track](assets/leading_on_benchmarks_4b.png)

- **#1 of 46 — Composite** (open-weight Jev-class models; #2 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-29, its row for release v1.4.1, measured 2026-10-27 at image
  temperature 0.65; ahead of
  Drex Max (Nace AI, 44.65),
  Jev 1.13.0 + images (TypeSafe, 26.43),
  Clef-Flash (Cloudflare, 20.41) and
  GPT-6 Luna via OpenAI Decisions (17.30) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#imagejevbench))
- **#2 of 46 — Intelligence** (open-weight Jev-class models; #6 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-29, its row for release v1.4.1, measured 2026-10-27 at image
  temperature 0.65; ahead of
  Clef (Cloudflare, 47.40),
  GPT-6 Luna via OpenAI Decisions (45.00) and
  Liquid d1-3B (16.31) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#imagejevbench))
- **#4 of 46 — Capability** (open-weight Jev-class models; #10 of 55 Jev-class models, open or API), ImageJevBench
  edition v0.3.0, page read 2026-10-29, its row for release v1.4.1, measured 2026-10-27 at image
  temperature 0.65; ahead of
  GPT-6 Luna via OpenAI Decisions (62.87),
  Clef (Cloudflare, 58.08) and
  Liquid d1-3B (47.78) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#imagejevbench))
- **#2 of 170 — Composite** (open-weight Jev-class models; #12 of 201 Jev-class models, open or API), JevBench board
  of 2026-10-28, its row for release v1.1, measured 2026-10-04; ahead of
  d1 (Liquid AI, 72.82),
  Microsoft-Decision-1 (69.08),
  OpenAI Decisions (62.37) and
  pplx-decider-flash (Perplexity, 54.01) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#leading-on-benchmarks))
- **#1 of 4 — Box Capability** (open-weight Jev-class systems; #1 of 5 Jev-class systems, open or API; Jev-class on this
  track: within 2x the latency and cost of Jev 1.14.0), ImageJevBench Box track (PREVIEW), edition v0.3.0, page read
  2026-10-29, its row for release v1.4.1 through the H2O serving package, measured 2026-10-29; ahead of
  Jev 1.14.0 (TypeSafe, 75.71) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#for-benchmark-maintainers-imagejevbench-box-track))
- **#1 of 46 — Computer-use Composite** (open-weight Jev-class systems; #3 of 55 Jev-class systems, open or API, behind
  two API systems scored on the board's smaller hosted-API item set), ImageJevBench computer-use track, edition v0.3.0,
  page read 2026-10-29, its row for release v1.4.1, measured 2026-10-27 at image temperature 0.65; ahead of
  Liquid d1-3B (Liquid AI, 66.22) and
  Clef-Flash (Cloudflare, 55.29) ([details](https://huggingface.co/h2oai/h2o-lightning-4b#imagejevbench))

Benchmarks are for the BF16 model these GGUF files are built from.

## Which file should I use

| Precision (`-hf` tag) | Size | Same answer as BF16 | Decision Index slice vs BF16 (95 % CI) | Correct / 231 |
|---|---:|---:|---:|---:|
| `:BF16` | 8.42 GB | (reference) | (reference: 59.98) | 201 |
| **`:Q8_0` (recommended)** | **4.48 GB** | **99.6%** | **−0.36 (−0.94 to +0.11), within noise** | **202** |
| `:Q5_K_M` | 3.07 GB | 99.1% | −0.12 (−1.43 to +0.97), within noise | 205 |
| `:Q4_K_M` | 2.71 GB | 98.5% | −0.86 (−2.34 to +0.48), within noise | 201 |
| `:mixed-IQ3_XXS` | 2.16 GB | 96.9% | +0.34 (−1.55 to +2.02), within noise | 199 |
| `:IQ3_XXS` | 1.90 GB | 96.4% | −0.44 (−2.71 to +1.39), within noise | 201 |

**Blackwell GPUs and the IQ3_XXS files.** On NVIDIA Blackwell GPUs, llama.cpp built with CUDA toolkit 13.2.0 or 13.2.1
gives near-random answers for `:IQ3_XXS` and `:mixed-IQ3_XXS` (`h2o-lightning-4b-IQ3_XXS.gguf` and
`h2o-lightning-4b-mixed-IQ3_XXS.gguf`; both contain IQ2_S tensors, and the IQ3_XXS file also IQ3_S tensors). This is a
compiler fault in those two toolkit releases, llama.cpp issue
[#28581](https://github.com/ggml-org/llama.cpp/issues/28581). Affected: compute capability 12.0 (GeForce RTX 50 series, RTX PRO 6000; we measured an RTX PRO 6000) and, as reported upstream (not tested by us), 10.x
(B200, GB200, GB300). On our RTX PRO 6000 with llama.cpp build 11773 built with CUDA 13.2.0, the two files scored 67 and
81 of JevBench's 231 questions; built with CUDA 12.9 they score 201 and 199, as in the table. The other four files
answered normally with CUDA 13.2.0 (BF16 201, Q8_0 202, Q5_K_M 205, Q4_K_M 201). The official llama.cpp release
downloads and Docker images are built with other toolkits and are not affected (see
[Blackwell GPUs](#blackwell-gpus)). Other GPUs, such as the L40S and H100, are not affected according to the issue; we
have not re-measured these two files on them.

Files are named `h2o-lightning-4b-<TAG>.gguf`, for example `h2o-lightning-4b-Q8_0.gguf` for `:Q8_0`. Q8_0 is the
recommended file for its size: half the size of BF16, with 99.6 % of answers the same as BF16 and a Decision Index
score within noise of it. Q5_K_M and Q4_K_M are smaller and also within noise of BF16, but change more answers. The
two IQ3_XXS files fit tight memory but change 3 to 4 % of answers; on this sample their index differences are within noise,
with wide intervals.

*Same answer as BF16*: the share of questions whose top answer equals `:BF16`'s, both read by llama.cpp build 11773
(commit `7e3eeee04`), so the column measures quantization alone. *Decision Index slice vs BF16*: the difference in the
Decision Index 0.3 index (0-100) on a fixed 2,000-row sample of the public text suite (14,996 questions, all 43
benchmarks; drawn with the Decision Index toolkit's own sampler, seed 20261024, and scored with its 0.3 scorer), with the
yes/no floor of 0.801 applied to both sides (see [Yes/no floor](#yesno-floor)); `:BF16` scores 59.98. 95 % confidence
intervals from a paired bootstrap over the toolkit's groups within each benchmark, 1,000 draws; "within noise" where
the interval includes 0. All six files were read on one NVIDIA RTX PRO 6000 (Blackwell). *Correct / 231*: JevBench's 231
public questions answered correctly, with JevBench's own CLI, on the same GPU (the release on vLLM, one-way: 202).

Against the release as served on vLLM 0.30.0 (one-way; llama.cpp reads one-way), `:BF16` on llama.cpp gives the same
top answer on 99.9 % of questions, with an index 0.10 higher (95 % CI +0.00 to +0.27) on the same 2,000-row
sample: that is the engine difference, separate from the quantization above.

These files need llama.cpp build 11773 (commit `7e3eeee04`) or later (see [How to run](#how-to-run)); with an older
llama.cpp, use the `stock-` file of the same precision through the shim (the IQ3_XXS files have none). Image decisions
also need the vision projector, `mmproj-lightning-f16.gguf` (0.67 GB, loaded automatically by `-hf`).

## How to run

There are two ways; both use the same weights.

- **llama.cpp, build 11773 (commit `7e3eeee04`) or later**: `llama-server` answers decisions itself on
  `POST /v1/systemone`, using the files in the table. Run `llama-server -hf h2oai/h2o-lightning-4b-gguf:Q8_0 ...` with
  the tag of the file you chose ([details](#llamacpp)). It reads images; it has no `box` question type.
- **The included Python shim on a pinned llama.cpp**: an unmodified `llama-server` at a pinned earlier revision runs
  the model and the shim serves the decision API. Use the `stock-` file of the same precision, for example
  `h2o-lightning-4b-stock-Q8_0.gguf` (BF16, Q8_0, Q5_K_M and Q4_K_M have one). The
  [one-command launcher](#run-with-one-command) downloads, checks and starts everything for any of these, and reads
  images and Box questions by default.

llama.cpp builds older than 11773 cannot load the files in the table (they do not know the decision type), and
`llama-server` with a `stock-` file alone gives ordinary chat, not the decision API.

## About the files

Each file in the table has the same weights, tensor for tensor, as its `stock-` copy where there is one, plus decision
metadata: the decision type `h2o-lightning`, the option labels, the per-type temperatures, the temperature for
requests with images, the prompt template, the Qwen2 pre-tokenizer setting and the NFC normalization flag (see
[Differences from the shim](#differences-from-the-shim)). The files are quantized from the released weights with
llama.cpp's default per-tensor types and an importance matrix; the mixed IQ3_XXS file keeps a few small projections
at 6 to 8 bits: in the recurrent layers, the decay and update-strength projections (8-bit) and the output gate and
output projections (6-bit); in the attention layers, the output projection (6-bit). The model's multi-token-prediction
head, which decisions never use, is not included.

With no tag, `llama-server -hf h2oai/h2o-lightning-4b-gguf` picks Q4_K_M (llama.cpp's default when no tag is given,
not our recommendation); add `:Q8_0` for the recommended file. A `stock-` copy is picked with its full tag, for example
`:stock-Q4_K_M`.

Storage sizes exclude runtime memory. Sizes and SHA-256 hashes of all files are in
[artifact_manifest_v5.json](artifact_manifest_v5.json); if your copy's SHA-256 does not match, download it again.
Older versions: see the repo's tags.

## llama.cpp

### Get llama-server

Use llama.cpp build 11773 (commit `7e3eeee04`) or later: a release tagged b11773 or higher from
[github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases), or a build from source.
Building needs Git, CMake and a C++ compiler; CUDA also needs a CUDA toolkit; `-hf` downloads need OpenSSL headers (for
example `libssl-dev`).

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# CPU
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j --target llama-server

# or CUDA
cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j --target llama-server
```

`./build/bin/llama-server --version` shows the build number (it counts the commits, so it needs a full clone; a
shallow one reports build 1).

### Blackwell GPUs

On a Blackwell GPU (GeForce RTX 50 series, RTX PRO 6000, B200, GB200, GB300), a build made with CUDA toolkit 13.2.0 or
13.2.1 gives wrong results for the IQ3_XXS files (see [the note under the table](#which-file-should-i-use)). Check the
toolkit before building:

```bash
nvcc --version
```

If it says `release 13.2, V13.2.51` (13.2.0) or `release 13.2, V13.2.78` (13.2.1), install CUDA 12.9 (or 13.2.2 or
later, per the issue) next to it, for example on Ubuntu with NVIDIA's CUDA apt repository set up, and build with that compiler:

```bash
sudo apt install cuda-toolkit-12-9

git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.9/bin/nvcc -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j --target llama-server test-backend-ops
```

Then check the GPU's matrix-multiplication kernels:

```bash
./build/bin/test-backend-ops -b CUDA0 test -o MUL_MAT
```

A good build ends with `Backend CUDA0: OK` and no `FAIL` lines. On our RTX PRO 6000, a CUDA 12.9 build of the current
llama.cpp (build 11923) passed all 2,445 MUL_MAT tests; the same source built with CUDA 13.2.0 failed 147 of them, all on
`type_a=iq1_s`, `type_a=iq2_s` and `type_a=iq3_s` lines.

The release downloads need no rebuild: the Ubuntu CUDA 12.8 and CUDA 13.4 builds on
[github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases) (they need glibc 2.38, for
example Ubuntu 24.04) and the Docker images `ghcr.io/ggml-org/llama.cpp:server-cuda` (CUDA 12.8) and `:server-cuda13`
(CUDA 13.4) scored 201 of 231 with `:IQ3_XXS` on our RTX PRO 6000 (release b11773; the images as pulled on
2026-10-27).

### Run

```bash
./build/bin/llama-server -hf h2oai/h2o-lightning-4b-gguf:Q8_0 --alias h2oai/h2o-lightning-4b \
    -c 40960 -np 1 --no-kv-unified --image-max-tokens 1024 --port 8080

# or with downloaded files
hf download h2oai/h2o-lightning-4b-gguf h2o-lightning-4b-Q8_0.gguf mmproj-lightning-f16.gguf --local-dir .
./build/bin/llama-server -m h2o-lightning-4b-Q8_0.gguf --mmproj mmproj-lightning-f16.gguf --alias h2oai/h2o-lightning-4b \
    -c 40960 -np 1 --no-kv-unified --image-max-tokens 1024 --port 8080
```

These are the settings the numbers on this card were measured with. `-c 40960` leaves room for a 32,000-token state
plus the question; `-np 1 --no-kv-unified` gives one slot the whole context (with more slots, the questions of one
request share the state's prompt and their probabilities can differ slightly); `--image-max-tokens 1024` is the image
token budget the model was validated with; `--alias` sets the `model` field of the response. Use another tag from
[the table](#which-file-should-i-use) for another precision. llama.cpp offloads to a GPU when it finds one; `-ngl`
controls it. `-hf` also loads the vision projector; pass `--no-mmproj` for text only.

### Request

```bash
curl http://127.0.0.1:8080/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": {"customer": "I was charged twice for order 1182 and nobody has replied.", "plan": "pro"},
  "questions": {
    "route":   {"type": "choice", "instructions": "Which team should handle this?", "criteria": {"billing": "payments and refunds", "shipping": "delivery problems", "technical": "app or website errors"}},
    "angry":   {"type": "noul",   "instructions": "Is the customer upset?"},
    "urgency": {"type": "score",  "instructions": "How urgent is this?", "criteria": ["can wait", "this week", "today", "right now"]}}}'
```

Response, measured with the Q8_0 file on one NVIDIA RTX PRO 6000 (numbers rounded to 4 digits here):

```json
{
  "model": "h2oai/h2o-lightning-4b",
  "answers": {
    "route":   {"type": "choice", "choice": "billing",
                "probabilities": {"billing": 0.9548, "shipping": 0.0234, "technical": 0.0218}, "confidence": 0.9322},
    "angry":   {"type": "noul", "noul": 0.9259},
    "urgency": {"type": "score", "score": 2.3988,
                "legend": {"0": "can wait", "1": "this week", "2": "today", "3": "right now"},
                "probabilities": {"0": 0.0084, "1": 0.0553, "2": 0.4652, "3": 0.4710}, "confidence": 0.3988}
  },
  "usage": {"input_tokens": 321, "output_tokens": 0}
}
```

Images go in a top-level `images` array of data URLs (`"images": ["data:image/png;base64,..."]`).

### Yes/no floor

`noul` probabilities are the raw calibrated values. llama-server applies no yes/no floor (it ignores a `"noul_floor"`
request field), as the model's vLLM serving does by default, where only the opt-in Decision Index profile
(`PROFILE=di`) applies 0.801. The included shim applies a floor of 0.801 by default: a `noul`
probability between 0.199 and 0.801 is moved to the nearer of the two, so the answer does not change; set
`SHIM_NOUL_FLOOR=0` in the launcher's environment to turn it off. To get the floored numbers from llama-server, apply
the floor to the returned value: `if max(p, 1 - p) < 0.801: p = 0.801 if p >= 0.5 else 0.199`.

### Parity with the shim

On the same llama.cpp server (build 11773), with the same prompts, llama-server's own `/v1/systemone` and the shim
give the same answer on all 231 public JevBench text questions and on the request above, for each of the six files in
the table, with probabilities within 2.3e-6. On 26 further edge cases (including states cut at 32,000 tokens) they
also agree within 1.6e-6; a deliberately non-NFC state can differ (it did for four of the six files), as described in
[Differences from the shim](#differences-from-the-shim). The shim's yes/no floor was off for this comparison.

### Differences from the shim

- Text normalization: the shim converts text to the standard composed Unicode form (NFC) before tokenizing it;
  llama.cpp tokenizes it as sent, so text that is not in NFC (for example "é" written as "e" plus a separate accent
  mark) can give different tokens and different answers. Most text is already NFC. To be safe, normalize every string
  you send, including JSON keys and nested values, with `unicodedata.normalize("NFC", text)` in Python. The files in
  the table carry the `tokenizer.ggml.normalizer.nfc` flag, which llama.cpp does not yet apply for this model's
  tokenizer type.
- Numbers: integers beyond 64 bits in a JSON state are written as floats.
- Response: llama.cpp's shape, `model`, `answers` and `usage` (`input_tokens`, `output_tokens`). The shim's extra
  fields (`probability_source`, `effort_used`, `usage.latency_ms`, `threshold`/`decision` for a `noul` threshold) are
  not returned.
- Floor: not applied by llama-server; the shim applies 0.801 by default (see [Yes/no floor](#yesno-floor)).
- Images: send them as data URLs in the top-level `images` array (or as `image_url` parts of chat messages in
  `state`). Images elsewhere in `state`, http(s) URLs, multipart uploads and the shim's other image fields (`image`,
  `image_url`, `image_urls`, `image_data`, `image_base64`) are not read as images; there is no 4-image cap (llama.cpp
  takes up to 8) and no `[image N]` placeholder in the state.
- Box questions and image references (`assets`) are answered by the shim only: llama-server's own `/v1/systemone` has
  no `box` question type. The [launcher](#run-with-one-command) answers both by default.

## The shim on a pinned llama.cpp

### Run with one command

Requires Python 3.12, Git, CMake and a C++ compiler. Install `huggingface_hub` and Pillow with `python -m pip install
huggingface_hub pillow` (Pillow draws the found box for the Box confidence: the launcher reads images and Box questions
by default and stops at once without Pillow, naming it; `--text-only` needs no Pillow).
CUDA additionally requires a compatible CUDA toolkit. No Hugging Face login is required.

```bash
python -c 'import hashlib,runpy; from huggingface_hub import hf_hub_download; p=hf_hub_download("h2oai/h2o-lightning-4b-gguf","bootstrap.py",revision="38fad5ea5a1fe7f4c9f6f1ef22a36b833acbd3fd",token=False); assert hashlib.sha256(open(p,"rb").read()).hexdigest()=="40c1c8fb1b9995b92e5dc6fd746441624c93e4308ba4672012e24337e4eed34d"; runpy.run_path(p,run_name="__main__")' --backend cpu
```

BF16 is the default; `--variant` picks another precision: `Q8_0` (the recommended smaller file), `Q5_K_M` or
`Q4_K_M` (see [Which file should I use](#which-file-should-i-use)). Use
`--backend cuda --gpu 0` for CUDA. Images and Box questions are on by default (the launcher downloads the vision
projector); `--text-only` leaves it out, and then image and Box questions are refused. `--prepare-only` downloads and
verifies without building or starting a server.

The launcher downloads pinned code and the `stock-` file of the chosen precision (checked by SHA-256), builds stock
llama.cpp at `10a60cf303566e10d6a7a2774c17d2085503d87b`, checks provenance and 24 tokenizer probes, then starts the
stock backend and the shim. For decisions, use the launcher; a `stock-` file loaded directly into `llama-server` gives
ordinary chat. Ctrl-C stops its owned children. Logs remain in `lightning-llamacpp-logs/`.

In another terminal:

```bash
curl http://127.0.0.1:8761/v1/systemone -H 'Content-Type: application/json' -d '{"state":{"status":"paid"},"questions":{"status":{"type":"choice","instructions":"What status is recorded?","criteria":{"a":"paid","b":"unpaid"}}}}'
```

The backend has one 40,960-token slot; concurrent requests queue. State text is capped at 32,000 tokens with head/tail
truncation. Full question/instruction overhead still needs to fit. Images are scaled to at most 1,048,576 pixels. Reserved control strings are escaped and the
required Qwen2/NFC tokenizer normalization is applied by the shim; direct completion calls do not apply that contract.

With the `stock-` Q8_0 file the launcher, as it starts by default (images and Box questions on), scored 202 of JevBench's
231 public questions (one NVIDIA RTX PRO 6000, CUDA).

### Image references and the Box question

Images can be sent by reference: put each image once under `"assets"`
(`{"<ref>": {"type": "image", "format": "png", "data_base64": "..."}}`, `"jpg"` for JPEG) and write `<ref>` wherever
the image belongs in `state`; the shim replaces the reference with the image. References match as plain text, so
every occurrence counts, even inside a longer word (`photo` also matches "a photo of"); each distinct reference is
sent to the model once, and every occurrence points at that image. Pick references that cannot occur in your text,
such as `IMG_1`. PNG and JPEG only, 16 MiB per file,
every asset referenced at least once, no URL fetching; a malformed asset map is a 400.

A `box` question, ``{"type": "box", "instructions": "the coffee mug in `photo`"}``, answers with a bounding box
`{"left", "top", "right", "bottom"}` in fractions of the image, `confidence`, `present` (the probability that the
target is in the image) and `found` (whether a box was located; if not, the box is the whole image with confidence 0).
Box questions are on by default: the launcher reads images unless `--text-only`, and there is no other on/off
setting. The box comes
from one constrained generation, so the backend must accept a JSON-schema response format; one that does not refuses a
request with a box question with HTTP 422, and requests without one are unaffected. On a `--text-only` launch, a box
question is refused with HTTP 422 and a message naming images. Both go through the shim; the `/v1/systemone` endpoint of llama-server reads
neither.

ImageJevBench's Box track is measured on the main model through its own `serve.sh`, not on these files: see
[For benchmark maintainers: ImageJevBench Box track](https://huggingface.co/h2oai/h2o-lightning-4b#for-benchmark-maintainers-imagejevbench-box-track).

## License

Apache-2.0. Built on [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) (Apache-2.0, Qwen team, Alibaba Cloud);
runs on [llama.cpp](https://github.com/ggml-org/llama.cpp) (MIT).
