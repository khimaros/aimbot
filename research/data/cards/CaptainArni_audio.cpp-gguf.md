---
license: mit
pipeline_tag: text-to-audio
library_name: gguf
tags:
  - audio
  - music
  - text2music
  - ace-step
  - gguf
  - audio.cpp
  - quantized
base_model:
  - ACE-Step/acestep-v15-xl-turbo
  - ACE-Step/acestep-v15-xl-sft
base_model_relation: quantized
---

# audio.cpp GGUF

GGUF conversions of music and speech models for
[audio.cpp](https://github.com/0xShug0/audio.cpp), the ggml-based native audio
inference framework.

## ACE-Step 1.5 XL

| File | Size | Package | Upstream |
|---|---:|---|---|
| `ACE-Step1.5-GGUF/xl-turbo/ace-step-1.5-xl-turbo-bf16.gguf` | 14.2 GiB | `ace_step_xl_turbo_bf16` | [acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) |
| `ACE-Step1.5-GGUF/xl-sft/ace-step-1.5-xl-sft-bf16.gguf` | 14.2 GiB | `ace_step_xl_sft_bf16` | [acestep-v15-xl-sft](https://huggingface.co/ACE-Step/acestep-v15-xl-sft) |
| `ACE-Step1.5-GGUF/xl-turbo-q8dit/ace-step-1.5-xl-turbo-q8dit.gguf` | 9.97 GiB | `ace_step_xl_turbo_q8dit` * | as above |
| `ACE-Step1.5-GGUF/xl-sft-q8dit/ace-step-1.5-xl-sft-q8dit.gguf` | 9.97 GiB | `ace_step_xl_sft_q8dit` * | as above |

\* proposed in [audio.cpp#464](https://github.com/0xShug0/audio.cpp/pull/464); until that lands, download the file and point `--model` at its directory.

The XL DiT is the larger ACE-Step 1.5 transformer: 32 layers of 2560 against
turbo's 24 of 2048, with 32 attention heads of 128. Each file is self-contained
the way audio.cpp's other ACE-Step GGUFs are — XL DiT, planner LM, text encoder
and VAE in one file — so none of them needs another download.

XL Turbo is guidance-distilled and ignores `guidance_scale`; XL SFT takes the
CFG path. Both were converted from the float32 upstream snapshots.

## The `q8dit` builds

`ace_step` is graded `No (planner sampling can fail)` for q8_0 in audio.cpp's
[gguf.md](https://github.com/0xShug0/audio.cpp/blob/main/docs/gguf.md#support-and-test-status),
and that grade is about the **planner LM**, not the DiT. The `q8dit` files
quantise the DiT to q8_0 and keep the planner LM, text encoder and VAE at bf16:

```bash
audiocpp_gguf ... \
  --keep-type "lm_weights*=bf16" \
  --keep-type "text_encoder_weights*=bf16" \
  --keep-type "vae_weights*=bf16" \
  --keep-type "dit_xl_turbo_silence_latent*=bf16" \
  --type q8_0 --output ace-step-1.5-xl-turbo-q8dit.gguf
```

Measured on an RTX 5090 (CUDA), against the bf16 file at the same prompt and
seed:

| | size | 20 s of audio | RTF | waveform correlation vs bf16 |
|---|---:|---:|---:|---:|
| XL Turbo bf16 | 14.2 GiB | 14.2 s | 0.71 | reference |
| XL Turbo q8dit | 9.97 GiB | 9.3 s | 0.46 | **0.989** |
| XL Turbo, everything q8_0 | 8.36 GiB | 8.2 s | 0.41 | 0.094 |

Every build is deterministic at a fixed seed (run-to-run correlation 1.0000), so
the last column isolates what quantisation changes. On a sung 40 s take the
q8dit build scores **0.997** for XL Turbo and **0.999** for XL SFT, and an ASR
pass over both returns the same lyric line. A fully quantised build returns a
different song from the same seed — it plays, it just isn't the same model.

Validated on three prompts on one machine. Treat these as a preview: they are
not covered by audio.cpp's path-test matrix.

## Install

```bash
python tools/model_manager_v2.py install ace_step_xl_turbo_bf16
```

The `q8dit` ids arrive with [audio.cpp#464](https://github.com/0xShug0/audio.cpp/pull/464);
until then, download the file and point `--model` at its directory.

## Run

The DiT variant is a load option, so name it explicitly:

```bash
audiocpp_cli --task gen --family ace_step --model models/ACE-Step1.5-GGUF/xl-turbo \
  --backend cuda --task-route text2music \
  --text "warm lo-fi hip hop with a soft rhodes piano" --duration-seconds 60 \
  --load-option ace_step.dit_model_path=acestep-v15-xl-turbo --out song.wav
```

For sung vocals, pass the lyrics *and* a language, and give the DiT more steps
than the turbo default:

```bash
  --lyrics "[verse]
City lights are falling slow" --language en --num-inference-steps 24
```

XL support landed in audio.cpp via
[PR #235](https://github.com/0xShug0/audio.cpp/pull/235); see
`docs/models/ace_step.md` there for the full option reference and for rebuilding
these files yourself.

Weights are MIT-licensed by ACE-Step; this repository only redistributes them in
a different container format.
