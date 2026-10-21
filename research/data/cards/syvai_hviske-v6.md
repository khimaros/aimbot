---
license: cc-by-nc-4.0
language:
- da
library_name: transformers
pipeline_tag: automatic-speech-recognition
tags:
- asr
- speech-recognition
- danish
- whisper
- qwen3
base_model:
- capacit-ai/saga-2-m
- Qwen/Qwen3-0.6B-Base
datasets:
- syvai/danish-asr-unified
metrics:
- wer
- cer
---

<p align="center">
  <a href="https://syv.ai" target="_blank"><img src="https://img.shields.io/badge/syv.ai-4A90E2?logoColor=white" alt="syv.ai"></a>
  <a href="https://platform.syv.ai" target="_blank"><img src="https://img.shields.io/badge/API-platform.syv.ai-1c1c1f" alt="API — platform.syv.ai"></a>
  <a href="https://github.com/Rye-A1/danish-asr-leaderboard" target="_blank"><img src="https://img.shields.io/badge/Danish%20ASR%20leaderboard-%231-4A90E2" alt="Danish ASR leaderboard"></a>
  <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank"><img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-4CAF50?logo=creativecommons&logoColor=white" alt="License CC BY-NC 4.0"></a>
</p>

# hviske-v6

**hviske-v6** is a 1.24B-parameter Danish ASR model: a RoPE-adapted Whisper-large-v3-turbo
encoder fused to a Qwen3-0.6B decoder through a frame-stacking projector. It scores a
**10.19 mean WER** on the [Danish ASR leaderboard](https://github.com/Rye-A1/danish-asr-leaderboard),
the best result on the board at the time of submission.

Audio is expected at 16 kHz mono. Clips longer than 30 s are split at silences and
re-joined automatically. Danish only, offline transcription (no timestamps, diarization,
or streaming).

Unlike other models on the board, hviske-v6 lets you **choose the output format** —
casing and punctuation are controllable at inference through four dedicated tokens.

## Accuracy

Measured with the leaderboard harness, unmodified, on a single RTX 3090. Full test
splits, no subsetting.

| Dataset | WER | CER |
|---|---|---|
| CoRal conversation | 18.26 | 10.63 |
| CoRal read-aloud | 12.43 | 4.91 |
| Common Voice 17 (da) | 6.21 | 2.06 |
| FLEURS (da) | 8.14 | 3.24 |
| FTSpeech | **5.91** | 3.25 |
| **Mean** | **10.19** | **4.82** |

For comparison, the previous best on the board scores 10.68 / 5.10. FTSpeech 5.91 and
Common Voice 6.21 are the best open-weights scores on the leaderboard at submission.

Throughput is 48× real-time on a 3090 at batch 4.

## Usage

```python
from processing_whisper_qwen import HviskeASR

asr = HviskeASR.from_pretrained("syvai/hviske-v6")

asr.transcribe("meeting.wav")
asr.transcribe(["a.wav", "b.mp3"], batch_size=8)
```

The model is custom-architecture, so `trust_remote_code=True` is required if you load it
through `AutoModel` directly.

### Controlling casing and punctuation

Danish ASR corpora disagree with themselves about formatting. Weighted across this
model's training mix, only **8.9%** of rows carry punctuation and **36.5%** carry
casing — FTSpeech is entirely lowercase and unpunctuated, CoRal is cased but
unpunctuated, FLEURS and Common Voice are fully formatted.

Left alone, a model trained on that mix infers the format from the *acoustics* — it will
give you lowercase, unpunctuated text for parliamentary audio no matter what you wanted.
hviske-v6 makes the choice explicit instead:

```python
asr.transcribe("clip.wav")                                  # auto — model decides
asr.transcribe("clip.wav", cased=True,  punctuated=True)    # "Han drog til Paris."
asr.transcribe("clip.wav", cased=True,  punctuated=False)   # "Han drog til Paris"
asr.transcribe("clip.wav", cased=False, punctuated=False)   # "han drog til paris"
```

| token | id |
|---|---|
| `<\|nocase\|>` | 151669 |
| `<\|cased\|>` | 151670 |
| `<\|nopunc\|>` | 151671 |
| `<\|punc\|>` | 151672 |

They occupy embedding rows that were allocated but unused (the matrix is
`[151936, 1024]`; the tokenizer stops at 151,668), so nothing was resized to add them.
They are **input-only** — conditioning, never a prediction target. One further row is
reserved the same way: `<|audio_pad|>` (151673) marks where audio sits in a prompt when
the model is served on vLLM, and is likewise never produced.

The benchmark numbers above use the automatic path, because forcing a global style costs
accuracy on domains it does not suit: `cased+punc` on parliamentary audio is worth +1.56
WER on FTSpeech, since that combination never occurs in training.

## Serving with vLLM

`trust_remote_code=True` is not enough here. It loads this repo's *config* class; it does
not run the modelling code for inference — vLLM resolves the architecture against its own
registry and runs its own layers. So the repo carries a second implementation under
[`vllm/`](vllm), separate from the `transformers` path above and registered through
vLLM's plugin entry point:

```bash
hf download syvai/hviske-v6 --local-dir hviske-v6
pip install -e hviske-v6/vllm
vllm serve syvai/hviske-v6
```

The hub id serves directly — no converted config and no separate model directory. The
`transformers` path above is untouched: `AutoModel` still gets the implementation in this
repo, because `transformers` only prefers a locally registered class when remote code is
not trusted, which is exactly vLLM's case.

One caveat worth the two lines it takes to avoid. vLLM's own
`/v1/audio/transcriptions` endpoint spends ~674 ms per request on audio decoding,
resampling and response assembly against ~26 ms of engine work, which holds the model at
about 16× realtime however many requests are in flight. Submitting prompts straight to
`AsyncLLM` measures 281 / 370 / 445× realtime at 16 / 32 / 64 concurrent windows on one
RTX 3090. [`vllm/README.md`](vllm/README.md) has the details, and a working server lives in
[syv-ai/transcribe](https://github.com/syv-ai/transcribe).

## Architecture

```
16 kHz → log-mel(128) → Whisper-large-v3-turbo encoder, RoPE-adapted   0.635 B
                      → stack 4 frames (one token / 80 ms)
                      → RMSNorm(5120) + Linear(5120 → 1024)            0.005 B
                      → Qwen3-0.6B-Base decoder                        0.596 B
```

The encoder's fixed 1500-position sinusoid table is zeroed and replaced with partial
rotary embeddings over the frame index (rotary width 56 of 64 per head, θ=10000). That
removes Whisper's hard 30-second window: a 4-second clip and a 27-second clip become the
same problem, and the mel window can be any even length. The encoder arrives in that
state as part of `capacit-ai/saga-2-m`.

## Training

The encoder is initialised from the **first release of
[`capacit-ai/saga-2-m`](https://huggingface.co/capacit-ai/saga-2-m)** by Capacit A/S,
published under the Apache License 2.0, and is trained further on the corpus below. The
decoder is initialised from `Qwen/Qwen3-0.6B-Base`, and the projector is randomly
initialised.

Trained on the cleaned [`syvai/danish-asr-unified`](https://huggingface.co/datasets/syvai/danish-asr-unified)
corpus — 2,755 hours across FTSpeech, CoRal read-aloud and conversation, NST, Nota,
FLEURS and Common Voice, filtered to rows whose transcripts survived a two-model
agreement audit. Two full epochs, 106,689 steps on a single RTX 3090.

- Muon (encoder matrices) + AdamW (decoder, projector), warmup-stable-decay schedule
- fp32 master weights under bf16 parameters (Kahan-compensated)
- bias-corrected EMA; the released weights are the EMA
- All five benchmark test sets excluded from training by transcript hash (24,375 hashes)

## Limitations

- **Danish only.** Other languages are not supported and will not degrade gracefully.
- **Conversational speech is the weak spot** (18.26 WER). Dialect drives most of it:
  measured across CoRal, WER ranges from 5.3 on østjysk to 23.2 on østligt sønderjysk,
  and older speakers score worse than younger ones. The training mix is 58% parliamentary
  standard Danish, which cannot teach that variation.
- **Forced punctuation is weak on parliamentary audio**, for the reason given above.
- No timestamps, no diarization, no streaming.

## License

CC BY-NC 4.0 for this repository's own weights and card.

This model is a **derivative work of [`capacit-ai/saga-2-m`](https://huggingface.co/capacit-ai/saga-2-m),
Copyright (c) 2026 Capacit A/S**, in both its inference code and its encoder weights. It was
derived from a revision published under the Apache License, Version 2.0; a copy is in
[`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt), and the modifications are recorded in
[`NOTICE`](NOTICE) as section 4(b) requires.

It also derives from `Qwen/Qwen3-0.6B-Base` (Apache-2.0) and, through saga-2-m, from
`openai/whisper-large-v3-turbo` (MIT). Check those repositories for their own terms before
commercial use.
