---
base_model: netease-youdao/Confucius4-R2T2
base_model_relation: quantized
library_name: audio.cpp
pipeline_tag: automatic-speech-recognition
license: other
license_name: netease-youdao-model-use-license
license_link: https://github.com/netease-youdao/Confucius4-R2T2/blob/master/MODEL_LICENSE
language:
  - zh
  - en
  - yue
  - ar
  - de
  - fr
  - es
  - pt
  - id
  - it
  - ko
  - ru
  - th
  - vi
  - ja
  - tr
  - hi
  - ms
  - nl
  - sv
  - da
  - fi
  - pl
  - cs
  - fil
  - fa
  - el
  - hu
  - mk
  - ro
tags:
  - gguf
  - asr
  - automatic-speech-recognition
  - streaming
  - real-time
  - low-latency
  - quantized
  - qwen3-asr
  - confucius4
  - r2t2
  - audio.cpp
---

# Confucius4-R2T2 — GGUF (audio.cpp)

GGUF conversions of **NetEase Youdao Confucius4-R2T2**, a low-latency,
append-only streaming ASR model (a Qwen3-ASR-1.7B fine-tune with Longest Stable
Prefix decoding), ready to run with
[audio.cpp](https://github.com/0xShug0/audio.cpp) — no Python, no PyTorch,
local inference on Metal / CUDA / CPU.

* Original model: [netease-youdao/Confucius4-R2T2](https://huggingface.co/netease-youdao/Confucius4-R2T2)
  · [source code](https://github.com/netease-youdao/Confucius4-R2T2) · [demo](https://r2t2.youdao.com/demo)
* Runtime: [audio.cpp](https://github.com/0xShug0/audio.cpp) (`ggml`), family `confucius4_r2t2`

## Runtime compatibility

These files use the **`confucius4_r2t2`** family and embed its schema-v1 model
specification. Use a build containing the family rename and streaming-delta
fix from [audio.cpp PR #604](https://github.com/0xShug0/audio.cpp/pull/604)
(validated at commit `40dec7147128649a4180a5c982a7808cd272fc3e`). Older builds that
only register `r2t2_asr` need to be updated. Model-manager package IDs and
session-option prefixes use `confucius4_r2t2` as shown below; the GGUF filenames
remain unchanged.

Both precisions were regenerated from the original upstream safetensors using
the updated converter and explicit model spec. Tensor names, shapes, types,
and weight payloads are unchanged from the previous GGUF files; the update
refreshes embedded package metadata. This is not a model retraining.
VAD endpointing is separate work in progress and is not enabled by this update.

## Files

| File | Quantization | Size | Notes |
|---|---|---:|---|
| `r2t2-q8_0.gguf` | Q8_0 | 2.31 GiB | Recommended compact format; verified on the English sample |
| `r2t2-f16.gguf` | F16 | 3.81 GiB | Maximum fidelity |

Both files are **self-contained**: the tokenizer, processor config, generation
config, chat template and the audio.cpp model spec are embedded, so the runtime
needs nothing but the binary and the single `.gguf` (the embedded files are
unpacked into a temporary directory at load time). The embedded spec carries the
**schema-v1 option contract**, so option validation comes from the file itself
rather than from a spec installed next to the runtime.

Precision policy: **Q8_0 and higher are supported**. 4-bit and 5-bit
quantizations (legacy and k-quant) are rejected at load time with an actionable
error, because this graph's kernels are not validated below Q8_0 and otherwise
decode to empty text.

SHA-256:

```
19f5ccd624484bcb5d44301437de41560b0ecc40c430e8850dfeefefbe82ccf5  r2t2-q8_0.gguf
d1b531ceaf5640d98352d3a9180238d99d36d393e160afd4692031077e7bae2c  r2t2-f16.gguf
```

## Usage

### Install

```bash
# via the audio.cpp model manager
python3 tools/model_manager_v2.py install confucius4_r2t2_q8_0     # or confucius4_r2t2_f16

# or directly
hf download davidxifeng/Confucius4-R2T2-gguf r2t2-q8_0.gguf \
  --local-dir models/Confucius4-R2T2-GGUF
```

### Offline transcription

```bash
audiocpp_cli --task asr --family confucius4_r2t2 \
  --model models/Confucius4-R2T2-GGUF/r2t2-q8_0.gguf \
  --backend metal --audio speech_16k.wav --text-out transcript.txt
```

### Streaming (real-time, append-only)

```bash
audiocpp_cli --task asr --mode streaming --family confucius4_r2t2 \
  --model models/Confucius4-R2T2-GGUF/r2t2-q8_0.gguf \
  --backend metal --audio speech_16k.wav \
  --session-option confucius4_r2t2.chunk_size_ms=320 \
  --text-out transcript.txt
```

Chunk sizes from 80 ms to 2 s are supported; 320 ms is a good default on Apple
Silicon. `--audio -` streams raw 16 kHz mono PCM from stdin for live sources.
Pass `--language Chinese` to skip language detection and `--text "hotword, term"`
for a context/hotword prompt.

### Server

```json
{
  "id": "r2t2-asr",
  "family": "confucius4_r2t2",
  "path": "models/Confucius4-R2T2-GGUF/r2t2-q8_0.gguf",
  "task": "asr",
  "mode": "streaming",
  "session_options": { "confucius4_r2t2.chunk_size_ms": "320" }
}
```

```bash
curl http://127.0.0.1:8488/v1/audio/transcriptions -F model=r2t2-asr -F file=@speech.wav
curl -N http://127.0.0.1:8488/v1/audio/transcriptions \
  -F model=r2t2-asr -F stream=true -F file=@speech.wav     # SSE transcript deltas
```

See the [audio.cpp model documentation](https://github.com/davidxifeng/audio.cpp/blob/40dec7147128649a4180a5c982a7808cd272fc3e/docs/community_models/r2t2.md)
for the full option reference, the LSP streaming contract, and GGUF details.

## Conversion recipe

```bash
audiocpp_gguf \
  --input /path/to/Confucius4-R2T2/model.safetensors \
  --root  /path/to/Confucius4-R2T2 \
  --family confucius4_r2t2 \
  --model-spec model_specs/confucius4_r2t2.json \
  --output r2t2-q8_0.gguf \
  --type q8_0
```

No weight-name or head flags are needed: the checkpoint ties the LM head to the
token embedding (`lm_head.weight` is absent) and the loader detects that.
Quantization only; no other weight modification.

## Verification

The refreshed Q8_0 and F16 files are validated with the `confucius4_r2t2`
runtime against the audio.cpp English sample (`assets/resources/sample_16k.wav`):
offline and final streaming transcripts must match the MPS reference golden,
and the concatenated streaming deltas must be a nonempty prefix of the expected
transcript. Automatic language detection is explicitly exercised.

Streaming deltas contain transcript text only. Rollback fragments such as
`language` are suppressed and do not advance the published text offset. The
uncommitted tail is returned in the final transcript, not as a final delta.
The old reference behavior that leaked language metadata is not preserved.

## Language support

Optimized for Chinese and English, with support for Cantonese, Arabic, German,
French, Spanish, Portuguese, Indonesian, Italian, Korean, Russian, Thai,
Vietnamese, Japanese, Turkish, Hindi, Malay, Dutch, Swedish, Danish, Finnish,
Polish, Czech, Filipino, Persian, Greek, Romanian, Hungarian and Macedonian.

## License and attribution

This is a **quantized Derivative Work** of
[NetEase Youdao Confucius4-R2T2](https://huggingface.co/netease-youdao/Confucius4-R2T2),
distributed under the **NetEase Youdao Model Use License Agreement** — full text
in [`LICENSE`](LICENSE) (English) and [`LICENSE_zh`](LICENSE_zh) (Chinese); see
also [`NOTICE`](NOTICE). The source code of the original model is Apache-2.0,
the model weights are not.

Required statement (license section 4.1(a)):

> Any modifications made to the original model in this Derivative Work are not
> endorsed, warranted, or guaranteed by the original right-holder of the
> original model, and the original right-holder disclaims all liability related
> to this Derivative Work.

Key restrictions: a separate commercial license is required above 100 M monthly
active users or RMB 1 B annual revenue (section 2.2); the model may not be used
to improve other AI models except Confucius4-R2T2, its derivatives, or
non-commercial models (section 3.4(c)); high-risk uses such as medical
diagnosis, autonomous driving, military, critical-infrastructure control,
large-scale biometric surveillance and automated decision-making are prohibited
(section 4.2). No trademark rights are granted (section 5.2).

## Citation

```bibtex
@misc{Confucius4-R2T2,
  title        = {Confucius4-R2T2: A Low Latency and High Accuracy Real-Time Speech Recognition Model},
  author       = {NetEase Youdao},
  year         = {2026},
  howpublished = {https://github.com/netease-youdao/Confucius4-R2T2}
}
```
