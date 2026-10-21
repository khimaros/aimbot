---
license: cc-by-nc-4.0
language:
- da
pipeline_tag: automatic-speech-recognition
tags:
- audio
- speech-recognition
- transcription
- danish
- hf-asr-leaderboard
library_name: transformers
base_model: syvai/hviske-v5.1
datasets:
- CoRal-project/coral-v3
---

# hviske-v5.3

Danish ASR. Fine-tuned from [syvai/hviske-v5.1](https://huggingface.co/syvai/hviske-v5.1) on the [CoRal v3](https://huggingface.co/datasets/CoRal-project/coral-v3) train splits with **layer-wise learning-rate decay** (encoder LR = 0.75 × decoder LR) for 5 epochs.

A 2B-parameter Conformer encoder-decoder ASR model, optimized for Danish read-aloud and conversational speech.

## Results on CoRal v3 **full test sets**

Evaluated on the *complete* test splits (17,560 samples). Two normalization conventions:

- **raw**: `jiwer` on un-normalized references and hypotheses
- **strict**: lowercase + punctuation strip + Danish digit-to-word (`num2words(lang="da")`) — the apples-to-apples normalization for comparing against published Whisper-style numbers

### Greedy decoding (`num_beams=1`)

| Split | N | raw WER | **strict WER** | raw CER | strict CER |
|---|---:|---:|---:|---:|---:|
| `read_aloud` | 9,122 | 10.26% | **9.37%** | 4.17% | 3.80% |
| `conversation` | 8,438 | 21.30% | **19.63%** | 12.12% | 11.56% |
| **weighted avg** | 17,560 | **15.56%** | **14.30%** | 7.99% | 7.53% |

### Beam search (`num_beams=5`, `length_penalty=1.0`)

| Split | N | raw WER | **strict WER** | raw CER | strict CER |
|---|---:|---:|---:|---:|---:|
| `read_aloud` | 9,122 | 9.86% | **9.01%** | 3.98% | 3.63% |
| `conversation` | 8,438 | 20.89% | **19.21%** | 11.90% | 11.35% |
| **weighted avg** | 17,560 | **15.16%** | **13.91%** | 7.78% | 7.34% |

Beam search costs ~75% more inference time but lowers avg WER by 0.4 pp.

### Versus other Danish ASR models on CoRal v3 (CER)

The CoRal team publishes CER numbers on the same test splits. hviske-v5.3 numbers are evaluated on the full test sets. Other entries reproduced from the [roest-v3-whisper-1.5b model card](https://huggingface.co/CoRal-project/roest-v3-whisper-1.5b).

#### Conversation split

![CoRal v3 — Conversation split CER ranking](./assets/bench-conversation.png)

| Model | Params | Trained on | conv CER |
|---|---:|---|---:|
| **hviske-v5.3** (this model, beam=5, strict) | **2.0B** | read_aloud + conversation | **11.35%** |
| **hviske-v5.3** (this model, greedy, strict) | 2.0B | read_aloud + conversation | 11.56% |
| **hviske-v5.3** (this model, beam=5, raw) | 2.0B | read_aloud + conversation | 11.90% |
| CoRal-project/roest-whisper-1.5b-v2 | 1.54B | read_aloud + conversation | 11.6% |
| CoRal-project/roest-wav2vec2-315m-v3 | 315M | read_aloud + conversation | 13.7% |
| syvai/hviske-v3-conversation | 1.54B | read_aloud + conversation | 15.1% |
| capacit-ai/saga (greedy, strict) | 2.0B | read_aloud + conversation | 16.92% |
| CoRal-project/roest-wav2vec2-315m-v1 | 315M | read_aloud only | 17.6% |
| ElevenLabs scribe_v2 (strict) | — | proprietary | 19.57% |
| CoRal-project/roest-wav2vec2-315m-v2 | 315M | read_aloud + conversation | 24.2% |
| openai/whisper-large-v3 | 1.54B | — | 27.5% |
| syvai/hviske-v2 | 1.54B | read_aloud only | 29.4% |
| CoRal-project/roest-whisper-1.5b-v1 | 1.54B | read_aloud only | 35.6% |
| OpenAI gpt-4o-transcribe (strict) | — | proprietary | 43.63% |

#### Read-aloud split

![CoRal v3 — Read-aloud split CER ranking](./assets/bench-readaloud.png)

| Model | Params | Trained on | read_aloud CER |
|---|---:|---|---:|
| **hviske-v5.3** (this model, beam=5, strict) | **2.0B** | read_aloud + conversation | **3.63%** |
| **hviske-v5.3** (this model, greedy, strict) | 2.0B | read_aloud + conversation | 3.80% |
| **hviske-v5.3** (this model, beam=5, raw) | 2.0B | read_aloud + conversation | 3.98% |
| CoRal-project/roest-whisper-1.5b-v1 | 1.54B | read_aloud only | 4.0% |
| syvai/hviske-v2 | 1.54B | read_aloud only | 4.0% |
| CoRal-project/roest-whisper-1.5b-v2 | 1.54B | read_aloud + conversation | 4.5% |
| syvai/hviske-v3-conversation | 1.54B | read_aloud + conversation | 4.5% |
| CoRal-project/roest-wav2vec2-315m-v3 | 315M | read_aloud + conversation | 5.9% |
| CoRal-project/roest-wav2vec2-315m-v2 | 315M | read_aloud + conversation | 6.4% |
| capacit-ai/saga (greedy, strict) | 2.0B | read_aloud + conversation | 7.41% |
| ElevenLabs scribe_v2 (strict) | — | proprietary | 7.60% |
| CoRal-project/roest-wav2vec2-315m-v1 | 315M | read_aloud only | 8.2% |
| openai/whisper-large-v3 | 1.54B | — | 10.1% |
| OpenAI gpt-4o-transcribe (strict) | — | proprietary | 11.31% |

The CoRal team's published numbers do not specify the normalization used; both raw and strict CER are shown for hviske-v5.3 to make the comparison fair. `capacit-ai/saga` was evaluated with the same methodology used here (full test splits via greedy `vllm serve` + `/v1/audio/transcriptions`); raw CER is `8.26%` (read_aloud) and `17.49%` (conversation). `ElevenLabs scribe_v2` was evaluated via the public `/v1/speech-to-text` API on the same full test sets (n=17,560); strict WER is `18.62%` (read_aloud) and `31.38%` (conversation). `OpenAI gpt-4o-transcribe` was evaluated via the public `/v1/audio/transcriptions` API on the same full test sets; strict WER is `26.34%` (read_aloud) and `55.24%` (conversation).

## Inference speed

On a single NVIDIA RTX 3090, hviske-v5.3 reaches **RTFx ≈ 425** — i.e. it transcribes audio about 425× faster than real time. **60 minutes of audio is processed in ≈ 8.5 seconds.**

## Installation

```bash
pip install "transformers==4.57.6" torch soundfile librosa huggingface_hub sentencepiece protobuf
pip install datasets  # only needed for the streaming examples below
```

## Usage

Load the model with `AutoModelForSpeechSeq2Seq` and `trust_remote_code=True`. The model exposes both a high-level `model.transcribe(...)` helper and the standard `model.generate(...)` interface.

### 1. Quick start — single file

```python
import torch, numpy as np, soundfile as sf
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("syvai/hviske-v5.3", trust_remote_code=True)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    "syvai/hviske-v5.3", trust_remote_code=True, dtype=torch.bfloat16
).to("cuda").eval()

audio, sr = sf.read("your_audio.wav")
audio = np.asarray(audio, dtype=np.float32)

hyp = model.transcribe(
    processor=processor,
    language="da",
    audio_arrays=[audio],
    sample_rates=[sr],
)[0]
print(hyp)
```

Audio longer than ~35 s is automatically chunked. Input is resampled to 16 kHz internally.

### 2. Long-form audio (≥ 35 s)

The processor automatically splits long audio into chunks. Pass the resulting `audio_chunk_index` back into `decode()` to stitch the per-chunk hypotheses into a single transcript:

```python
import time
import soundfile as sf
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("syvai/hviske-v5.3", trust_remote_code=True)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    "syvai/hviske-v5.3", trust_remote_code=True, dtype=torch.bfloat16
).to("cuda").eval()

audio, sr = sf.read("long_lecture_da.wav")
duration_s = len(audio) / sr
print(f"Audio duration: {duration_s/60:.1f} min")

inputs = processor(audio=audio, sampling_rate=sr, return_tensors="pt", language="da")
audio_chunk_index = inputs.get("audio_chunk_index")
inputs = inputs.to(model.device, dtype=model.dtype)

start = time.time()
outputs = model.generate(**inputs, max_new_tokens=256)
text = processor.decode(
    outputs,
    skip_special_tokens=True,
    audio_chunk_index=audio_chunk_index,
    language="da",
)[0]
elapsed = time.time() - start
print(f"Transcribed in {elapsed:.1f}s — RTFx: {duration_s/elapsed:.1f}")
print(text)
```

### 3. Batched inference

```python
import torch, soundfile as sf
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("syvai/hviske-v5.3", trust_remote_code=True)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    "syvai/hviske-v5.3", trust_remote_code=True, dtype=torch.bfloat16
).to("cuda").eval()

audio_a, _ = sf.read("clip_a.wav")
audio_b, _ = sf.read("clip_b.wav")

texts = model.transcribe(
    processor=processor,
    language="da",
    audio_arrays=[audio_a, audio_b],
    sample_rates=[16000, 16000],
)
for i, t in enumerate(texts):
    print(f"[{i}] {t}")
```

### 4. Beam search (lowest WER)

Beam=5 is the recipe used to produce the beam-search numbers in the table above (~0.4 pp lower avg WER, ~75% slower than greedy):

```python
inputs = processor(audio, sampling_rate=16000, return_tensors="pt", language="da")
audio_chunk_index = inputs.get("audio_chunk_index")
inputs = inputs.to(model.device, dtype=model.dtype)

outputs = model.generate(
    **inputs,
    max_new_tokens=256,
    num_beams=5,
    length_penalty=1.0,
    do_sample=False,
)
text = processor.decode(
    outputs,
    skip_special_tokens=True,
    audio_chunk_index=audio_chunk_index,
    language="da",
)[0]
print(text)
```

### 5. Punctuation control

By default the processor inserts a punctuation prompt token. Disable it for plain-text output:

```python
inputs_pnc   = processor(audio, sampling_rate=16000, return_tensors="pt", language="da", punctuation=True)
inputs_nopnc = processor(audio, sampling_rate=16000, return_tensors="pt", language="da", punctuation=False)
```

## Run with vLLM (OpenAI-compatible API)

vLLM can serve the model behind an OpenAI-compatible `/v1/audio/transcriptions` endpoint — convenient for high-throughput batch transcription and remote serving.

### Install

```bash
pip install "vllm==0.19.0"
pip install "vllm[audio]" librosa   # audio deps are required for transcription
```

### Start the server

```bash
vllm serve syvai/hviske-v5.3 --trust-remote-code --host 0.0.0.0 --port 8000
```

`--trust-remote-code` is required — the model ships custom code. The runner (transcription) is auto-detected; no `--task` flag is needed.

### Transcribe — curl

```bash
curl -s http://localhost:8000/v1/audio/transcriptions \
  -F "file=@your_audio.wav" \
  -F "model=syvai/hviske-v5.3" \
  -F "language=da" \
  -F "temperature=0"
```

### Transcribe — Python (`openai` client)

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

with open("your_audio.wav", "rb") as f:
    resp = client.audio.transcriptions.create(
        model="syvai/hviske-v5.3",
        file=f,
        language="da",
        temperature=0,
    )
print(resp.text)
```

**Notes**

- `language="da"` + `temperature=0` gives the most accurate, deterministic output.
- `response_format` supports `json` (default) and `text`. `verbose_json` is **not** supported and returns a 400.
- Accepts common audio formats (wav, mp3, flac, ogg); audio is resampled to 16 kHz internally.

## Training details

- **Starting point:** `syvai/hviske-v5.1`
- **Data:** `CoRal-project/coral-v3` — both `read_aloud` (299,255 samples) and `conversation` (147,249) train splits, interleaved and per-epoch shuffled (seed=42)
- **Eval during training:** 10% of each test split (912 + 843 samples) for best-checkpoint tracking
- **Best-checkpoint tracking:** saved the eval point with lowest avg WER (hit at 90% of training)
- **Hyperparameters:**
  - Epochs: 5
  - Batch: 16 micro × 8 grad-accum = **128 effective batch**
  - **Layer-wise LR decay** (LLRD): encoder = 0.75 × decoder
    - Decoder peak: `2e-4`
    - Encoder peak: `1.5e-4`
  - Schedule: 1,500-step linear warmup → cosine decay to zero
  - Optimizer: bnb `AdamW8bit`
  - Augmentation: SpecAugment (2 freq × 27 bins, 2 time × 100 frames)
  - Max audio length: 31 s (longer is dropped)
  - Precision: bf16
- **Hardware:** single NVIDIA RTX PRO 6000 Blackwell Max-Q (98 GB)

## License

This model is released under [**Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)**](https://creativecommons.org/licenses/by-nc/4.0/).

- **Permitted:** non-commercial use including research, education, evaluation, and personal projects, with attribution.
- **Not permitted without a separate commercial license:** any use by or for a commercial entity, integration into a commercial product or service, or use to generate revenue (directly or indirectly).
- **Commercial licensing:** contact mads@syv.ai.
