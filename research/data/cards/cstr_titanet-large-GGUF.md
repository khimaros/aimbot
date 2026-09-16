---
license: cc-by-4.0
tags:
  - speaker-verification
  - speaker-identification
  - speaker-embedding
  - gguf
  - crispasr
base_model: nvidia/speakerverification_en_titanet_large
pipeline_tag: audio-classification
---

# TitaNet-Large — GGUF

GGUF conversion of [nvidia/speakerverification_en_titanet_large](https://huggingface.co/nvidia/speakerverification_en_titanet_large) (CC-BY-4.0) for native C/C++ inference via [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Model

| Detail | Value |
|---|---|
| Architecture | TitaNet-Large — depthwise separable Conv1D encoder + ASP decoder |
| Parameters | 23M |
| Embedding dim | 192 (L2-normalized) |
| EER | 0.66% on VoxCeleb1-O cleaned |
| Input | 16 kHz mono PCM |
| GGUF size | ~45 MB (F16 weights, F32 batch-norm) |
| License | CC-BY-4.0 |

## Architecture

```
Preprocessor: 16kHz → 80-bin mel spectrogram (Hann window, n_fft=512, hop=160, win=400)

Encoder (Jasper-style):
  Block 0 (prolog):  DW-Conv(80, k=3) + PW-Conv(80→1024) + BN + SE + ReLU
  Block 1:           3× DW-Sep-Conv(1024, k=7)  + SE + residual + ReLU
  Block 2:           3× DW-Sep-Conv(1024, k=11) + SE + residual + ReLU
  Block 3:           3× DW-Sep-Conv(1024, k=15) + SE + residual + ReLU
  Block 4 (epilog):  DW-Conv(1024, k=1) + PW-Conv(1024→3072) + BN + SE + ReLU

Decoder:
  ASP (Attentive Statistics Pooling): 3072 → 6144
  BN + Linear: 6144 → 192
  L2-normalize
```

## Usage with CrispASR

### Speaker enrollment

```bash
# Enroll a speaker from a reference audio clip
crispasr --enroll-speaker alice \
         --speaker-db ./speakers \
         -f alice_reference.wav
```

### Speaker identification during transcription

```bash
# Transcribe with speaker identification
crispasr --backend parakeet \
         --speaker-db ./speakers \
         -f meeting.wav
# Output: (alice) Hello everyone...
```

### Standalone embedding extraction

```bash
# Extract speaker embedding (test binary)
test-titanet titanet-large.gguf audio1.wav audio2.wav
# Prints cosine similarity matrix
```

### Python

```python
from crispasr import TitaNet, SpeakerDB

with TitaNet("titanet-large.gguf") as model:
    emb = model.embed(pcm_16k_float32)

db = SpeakerDB("./speakers")
db.enroll("alice", emb)
name, score = db.match(emb, threshold=0.7)
```

## Conversion

```bash
python models/convert-titanet-to-gguf.py \
    --input nvidia/speakerverification_en_titanet_large \
    --output titanet-large.gguf
```

## Verification

Encoder + decoder parity with NeMo reference: **cos = 0.999997** (mel-injected).
End-to-end parity: **cos = 0.917** (STFT float32 precision gap in mel front-end).

## Citation

```bibtex
@inproceedings{koluguri2022titanet,
  title={TitaNet: Neural Model for Speaker Representation with 1D Depth-wise Separable Convolutions and Global Context},
  author={Koluguri, Nithin Rao and Park, Taejin and Ginsburg, Boris},
  booktitle={ICASSP 2022},
  year={2022}
}
```

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [nvidia/speakerverification_en_titanet_large](https://huggingface.co/nvidia/speakerverification_en_titanet_large) — published by `nvidia`.
- **Upstream licence:** `cc-by-4.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
