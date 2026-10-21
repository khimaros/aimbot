---
license: apache-2.0
base_model:
  - OpenMOSS-Team/MOSS-TTSD-v1.0
  - OpenMOSS-Team/MOSS-Audio-Tokenizer
library_name: audio.cpp
pipeline_tag: text-to-speech
language:
  - en
  - zh
tags:
  - gguf
  - text-to-speech
  - dialogue
  - voice-cloning
  - moss
---

# MOSS-TTSD — GGUF for audio.cpp

Self-contained GGUF packages of [OpenMOSS-Team/MOSS-TTSD-v1.0](https://huggingface.co/OpenMOSS-Team/MOSS-TTSD-v1.0),
for [audio.cpp](https://github.com/0xShug0/audio.cpp). Each file carries the 8B
delay-pattern backbone, the MOSS-Audio-Tokenizer v1 codec (**both** encoder and
decoder, because cloning needs the encoder), the tokenizer and the model spec —
nothing else to download.

MOSS-TTSD speaks a speaker-tagged dialogue in one take: `[S1]` and `[S2]` mark
who is talking, and each tag can carry its own reference recording.

| file | backbone | codec | size |
|---|---|---|---|
| `moss_ttsd_q8_0_codec_f16.gguf` | q8_0 | f16 | 12.2 GB |
| `moss_ttsd_q4_k_codec_f16.gguf` | q4_k (f16 heads) | f16 | 9.5 GB |
| `moss_ttsd_bf16_codec_f16.gguf` | bf16 | f16 | 18.9 GB |

`OpenMOSS-Team/MOSS-TTSD-v1.0` ships no codec weights — its processor resolves
`OpenMOSS-Team/MOSS-Audio-Tokenizer` at load time — so both are listed as parent
models. This checkpoint reads the first 16 of that codec's 32 RVQ layers.

## Performance and VRAM

Measured on an RTX 3090 (24 GiB) with audio.cpp at
[0xShug0/audio.cpp#690](https://github.com/0xShug0/audio.cpp/pull/690) or later.
Peak VRAM is the process's own allocation. The cloning case is a two-speaker
dialogue with a short reference for each speaker. RTF is session time over
output duration, which leaves out loading the package.

| package | peak VRAM, plain TTS | peak VRAM, cloning | RTF, plain TTS | RTF, cloning |
|---|---|---|---|---|
| q4_k | 8.2 GiB | 10.1 GiB | 0.18 | 0.27–0.30 |
| q8_0 | 10.9 GiB | 12.7 GiB | 0.23 | 0.26–0.39 |
| bf16 | 17.6 GiB | 19.4 GiB | 0.33 | 0.41–0.52 |

Every package clones on a 24 GiB card, bf16 included. Cloning fits in 12 GB with
q4_k and in 16 GB with q8_0. The RTF ranges come from three seeds that produced
takes of different lengths. The first clone in a session also loads the codec
encoder, so the shorter takes, where that fixed cost weighs more, sit at the
high end.

**Use a recent audio.cpp for bf16 cloning.** Older builds loaded the codec at f32
on the GPU, which doubled its footprint. There, bf16 cloning fails on a 24 GiB
card while allocating `moss.audio_tokenizer.encoder`. Since #687 the codec decoder
and the KV cache run at f16. Since #690 the encoder weights stay in VRAM at f16
and are widened to f32 only while they are in use. The encoder computes exactly as
an f32 load would, so cloning output does not change; only the memory it takes does.

## The q4_k package keeps its heads at f16

A plain q4_k of this model is broken, and quietly: it speaks the first turn of a
dialogue and stops. `lm_heads.0` is the text head, which decides when the turn
ends, and at four bits it ends it early.

```
q4_k, heads quantised   2.6-3.2s  first turn only, sometimes with a garbled tail
q4_k, heads at f16      9.1-16.5s full script
q8_0                    10-12.5s  full script
```

So this package is built with `--keep-type "model_weights/lm_heads*=f16"`, which
costs 0.95 GB over a plain q4_k and is the difference between usable and not.

## ⚠ Speaker identity drifts across turns

This is the model, not the conversion or the engine. Measuring median F0 per
turn against two references 84 Hz apart, over three runs of the reference
PyTorch implementation and one of audio.cpp:

```
run                S1 turn1  S1 turn2  S2 turn1  S2 turn2
reference run 1      200.0     110.3     154.8     131.9
reference run 2      203.4     102.8     179.1     160.0
reference run 3      208.8     104.8     161.1     152.5
audio.cpp (seed 7)   210.5     120.6     166.7     164.4
references:          S1 = 201.7 Hz, S2 = 117.6 Hz
```

The first speaker's first turn matches its reference closely. By that speaker's
second turn the pitch has fallen to roughly the *other* reference's, and the
second speaker sits between the two throughout. The reference implementation
does this in every run and audio.cpp reproduces the pattern at the same
magnitude — which is the parity result, on a feature that does not hold up.

Median F0 is a crude stand-in for speaker identity, and this is four runs of one
configuration with short references (3.4 s and 4.2 s) where the model card's own
example uses much longer ones. Read it as "identity drifts across turns", not as
a measured rate.

## Usage

```bash
audiocpp_cli --task tts --family moss_ttsd --model /path/to/MOSS-TTSD-GGUF \
  --backend cuda --language English \
  --text "[S1] So what did you make of it? [S2] Honestly, I was not expecting that ending." \
  --out dialogue.wav
```

Cloning takes one reference per speaker, positional, plus what those recordings
say — the model continues from the reference audio, so the transcript has to line
up with it:

```bash
audiocpp_cli --task clon --family moss_ttsd --model /path/to/MOSS-TTSD-GGUF \
  --backend cuda --language English \
  --request-option voice_samples=/path/to/s1.wav,/path/to/s2.wav \
  --request-option "reference_text=[S1] First voice here. [S2] Second voice here." \
  --text "[S1] The train leaves at four. [S2] I packed already." \
  --out dialogue.wav
```

The number of entries is the number of speakers, and an entry with no path is a
speaker that is named but not cloned:

| `voice_samples=` | speakers |
|---|---|
| `s1.wav,s2.wav` | both cloned |
| `s1.wav,` | `[S1]` cloned, `[S2]` invented |
| `,s2.wav` | `[S1]` invented, `[S2]` cloned |
| `s1.wav` | one speaker only — no `[S2]` is implied |

So the trailing separator is meaningful, not a typo.
