---
base_model: fishaudio/drama-3
base_model_relation: quantized
pipeline_tag: text-to-speech
license: other
license_name: fish-audio-community-license-v1.0
license_link: https://huggingface.co/fishaudio/drama-3/blob/main/LICENSE
tags:
  - gguf
  - audio.cpp
  - fish-audio
  - text-to-speech
  - voice-cloning
  - audio-editing
  - moe
  - mixed-quantization
---

# Drama 3 GGUF for audio.cpp

Built with Fish Audio.

Experimental native audio.cpp conversions of
[Fish Audio Drama 3](https://huggingface.co/fishaudio/drama-3), prepared from
checkpoint revision `dd64a85cd82e9521f7202610ede97b367fc83946`.
All packages use the same trained model architecture and checkpoint.

**Standard GGML K-quants with mixed precision.** The packages use Q2_K,
Q3_K_S and Q4_K_S file profiles with pure expert banks and explicit precision
overrides. Routed expert tensors use Q2_K, Q3_K and Q4_K storage respectively.
`backbone-8bit` means Q8_0 language-backbone matrices; `backbone-4bit` means
Q4_K matrices with a Q4_0 text embedding. The table below lists the precision overrides. Audio-tower matrices and waveform codec
weights remain FP16; audio-tower normalization and other retained FP32 vectors are unchanged.

## Files and precision

| Profile / file | Size | Routed experts | Routers / gates | Text embedding | Speech head | Other backbone matrices |
| --- | ---: | --- | --- | --- | --- | --- |
| [Q4 experts / Q8 backbone](./drama-3-backbone-8bit-experts-Q4_K_S.gguf) | 22.91 GiB | Q4_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [Q3 experts / Q8 backbone](./drama-3-backbone-8bit-experts-Q3_K_S.gguf) | 18.93 GiB | Q3_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [Q2 experts / Q8 backbone](./drama-3-backbone-8bit-experts-Q2_K.gguf) | 15.88 GiB | Q2_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [Q4 experts / Q4 backbone](./drama-3-backbone-4bit-experts-Q4_K_S.gguf) | 21.78 GiB | Q4_K | Q4_K | Q4_0 | Q4_K | Q4_K |
| [Q4 + FP32 routers](./drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf) | 22.97 GiB | Q4_K | FP32 | Q8_0 | Q8_0 | Q8_0 |
| [Q4 + FP32 routers + BF16 embedding/head](./drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf) | 23.87 GiB | Q4_K | FP32 | BF16 | BF16 | Q8_0 |

The Q3_K_S and Q4_K_S file profiles use pure expert banks: all 120 routed
expert projection banks have uniform Q3_K or Q4_K storage. Their storage-type
selection corresponds to a standard `--pure` K profile with explicit precision
overrides for the dense backbone, text embedding and audio components.
Architecture-specific higher-bit promotion heuristics are not applied; an
unmodified default llama.cpp preset can choose different types for some tensors.
See the standard converter's [pure and per-tensor options](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/quantize.cpp).
The native audio.cpp converter takes `--expert-type q3_k` or
`--expert-type q4_k`. The table above lists each component's actual storage type.

Q2, Q3 and Q4 are mixed quantizations. Q8_0 stores scaled 8-bit integer weights;
it is different from the FP8 representation of the original checkpoint's experts.
All packages retain FP16 audio-tower matrices and waveform codec weights. Backbone
and audio-tower normalization vectors remain FP32; codec normalization remains FP16. They embed the configuration, tokenizer, codec,
model contract and license, so inference does not require the original checkpoint
directory.

This repository distributes six standalone packages. All six retain the original
full-size speech head and work with the standard Drama 3 loader in current audio.cpp main.
Other quantizations can be prepared locally from the original checkpoint.

### FP32-router profiles

Both are **4-bit Q4_K_S expert profiles with mixed precision**. Their
filenames end in `Q4_K_S` so Hugging Face groups them under 4-bit in the
GGUF picker. The table above specifies each component's precision.

The two FP32-router files keep all 120 routed expert projection banks at **Q4_K**
and the other backbone matrices at **Q8_0**. Both restore the 40 expert routers and
40 shared-expert gates from the original checkpoint and store their values as FP32.
The BF16 profile additionally restores the original **BF16 text embedding and full speech head**.
The original router tensors were BF16; expanding those values into FP32 retains
them exactly and avoids Q8 rounding. These labels describe selected components
of a mixed-precision model. They do not describe an entirely FP32 or BF16 model.

Both files retain the complete 252,288-row `lm_head.weight` tensor. No compact-head
runtime changes or upstream pull request are needed to use these downloads.

* FP32 routers, Q8_0 text embedding/head: `drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf`
* FP32 routers, BF16 text embedding/head: `drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf`

## Runtime compatibility

Drama 3 support is merged into [audio.cpp main](https://github.com/0xShug0/audio.cpp).
Build a current checkout with the `fish_drama3` backend enabled. Validation of the
two FP32-router packages used unmodified upstream commit
[`e065d66b`](https://github.com/0xShug0/audio.cpp/commit/e065d66b7aa70bb697e39b1e7a952197f017baef)
on Windows CPU and CUDA, with no compact-head patch.

Follow the [Windows build and server instructions](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/fish_drama3.md).
The runtime is a native C++ CLI and HTTP server. No Python inference process is required.
Releases from before Drama 3 was merged do not include this backend.

These packages have GGUF architecture `audiocpp` and require its model loader
and embedded resource contract. Stock audio.cpp builds without the Drama 3 port
and general-purpose GGUF text-model runtimes cannot run this architecture.

The port implements offline and streaming speech, voice references, speaker and
event directions, long-form chunking and continuation/edit history through take
artifacts. It remains experimental.

## Run with a compatible audio.cpp build

Download either new precision profile directly, then pass its path with `--model`.
A runtime package catalogue may still list only the original four download presets.

```powershell
uv run --no-project --python 3.12 --with huggingface_hub hf download Jmica/Drama-3-GGUF `
  drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf --local-dir models/Drama-3-GGUF
```

For the BF16 embedding/head profile, substitute `drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf`.

Example using Q2 experts and the tested smaller-memory offload configuration:

```powershell
.\audiocpp_cli.exe --task tts --family fish_drama3 --backend cuda `
  --mode streaming --model .\drama-3-backbone-8bit-experts-Q2_K.gguf `
  --text 'A quick test of Drama Three.' --max-tokens 500 --seed 123 --threads 8 `
  --session-option fish_drama3.cpu_expert_layers=8 `
  --session-option fish_drama3.context_length=2048 --out speech.wav
```

For the original four files, the tested lower-memory configurations use 24 CPU expert layers with Q4 experts,
12 with Q3 experts, 8 with Q2 experts, or 20 with Q4 backbone. These are suggested
starting configurations, rather than enforced memory limits. Host RAM is needed
for the offloaded expert banks; model file size does not equal required VRAM.

The configurations were exercised on an RTX PRO 6000 Blackwell with 96 GB VRAM,
CUDA 12.8, Windows and eight CPU threads. Physical 16 GB and 24 GB GPUs have
not been tested. Increasing context length or adding longer references/history
increases memory use.

For cloning, supply `--voice-ref reference.wav` and
`--request-option 'reference_text=The reference transcript.'`.
For editing, pass a previously returned `drama3_take` artifact through the
library/API, or saved take JSON through `previous_takes_file`.

## Validation limits

English speech, reference-conditioned cloning, streaming, long-form output and
continuation/edit artifacts were exercised locally. Quantized expert tensor
types and independent small-model math controls were also checked.

The two full-head FP32-router packages were checked for offline and streaming
generation on unmodified upstream CPU/CUDA builds. Their unchanged tensor payloads
were compared byte-for-byte with the source package, and restored weights were
checked against the tested precision variants and original checkpoint. The
layout change preserves the same trained weight values for all speech-token rows.

Earlier blind listening comparisons used compact-head versions of these precision
profiles. Those preferences alone do not establish that either full-head profile
has better voice quality or more reliable stage-direction delivery. Higher precision
is not a guarantee of better individual takes.

Emotion and nonverbal directions are not consistently reliable. Some tagged
takes produce prolonged reactions, omit dialogue or reach the generation cap.
This occurred with the original Q4-expert package as well as smaller variants.
The Q3 offload profile omitted dialogue after laughter in one tagged test, and a
Q2 long-form trial with heavier CPU offload reached the cap; the documented Q2
eight-layer offload profile completed that long-form case.

These checks do not establish perceptual parity with the original checkpoint,
consistent emotion delivery or broad multilingual quality. Transcript checks
verify words, rather than voice similarity or acting quality. Seeds reproduce a
take within the same execution configuration; changing quantization or offload
placement can change the sampled audio. The full-head FP32-router profiles use
more memory than their compact experimental counterparts; the BF16 embedding/head
profile also uses more memory than the original Q4/Q8 file.

## Conversion

The converter reconstructs the scaled FP8 experts with their original
128-by-128 scales and packs their projections into three-dimensional banks.
The native GGUF converter applies the chosen expert, backbone and embedding
weight types, folds codec weight normalization and embeds the runtime resources.
Expert banks remain quantized during native execution.

The converter exposes separate expert, backbone and embedding precision options.
Conversion uses CPU dependencies managed with uv. The new FP32-router profiles
restore router values directly from the original checkpoint; the BF16 profile
also restores the original text embedding and full output head. They retain
the remaining quantized payloads and the standard full-head tensor names/shapes.
The default conversion example below creates an ordinary expert/backbone profile;
it does not perform these additional original-weight restorations.

With a compatible port checkout and native GGUF converter, download the original
checkpoint and choose the desired precision. For example, to prepare Q5 experts:

```powershell
uv run tools/community_models/convert_fish_drama3.py `
  --checkpoint .\drama-3 --output .\drama3-f16-local.gguf `
  --quantized-output .\drama-3-backbone-8bit-experts-Q5_K.gguf `
  --gguf-tool .\audiocpp_gguf.exe `
  --expert-type q5_k --backbone-type q8_0 --embedding-type q8_0
```

The converter creates a local FP16 intermediate of approximately 68.2 GiB before
producing the runnable package. It can be reused for another precision through
`--input-gguf` instead of `--output`. The intermediate is not distributed here.

## License and attribution

The model materials and these conversions are subject to the Fish Audio Community
License, Version 1.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for the original
terms, required attribution and description of modifications. This repository
is an independent conversion of Fish Audio Drama 3.
