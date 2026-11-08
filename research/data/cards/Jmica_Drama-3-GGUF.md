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
  - moe
  - mixed-quantization
---

# Drama 3 GGUF V2 for audio.cpp

Built with Fish Audio.

**V2 is the current default release in this repository.** These experimental
conversions use the October 29, 2026 replacement checkpoint,
[`fishaudio/drama-3` revision `78e5ab7`](https://huggingface.co/fishaudio/drama-3/tree/78e5ab79e49aa9a25abe8799eff2c4d73a1c3216).
All six profiles use that checkpoint and retain the complete output head.
No fine-tuning or compact-head runtime changes are used.

## V1 and V2 releases

| GGUF release | Fish Audio checkpoint | Where to download |
| --- | --- | --- |
| **V2, current default** | October 29, 2026, `78e5ab7` | [Default files on main](https://huggingface.co/Jmica/Drama-3-GGUF/tree/main) |
| **V1, original release** | October 13, 2026, `dd64a85` | [All six original files](https://huggingface.co/Jmica/Drama-3-GGUF/tree/original-2026-10-13), revision `original-2026-10-13` |

V1 remains available at that preserved revision. V2 replaces the default files
on `main` and keeps the same filenames and component precision profiles.
Select `original-2026-10-13` in the revision selector, or use the V1 download
command below, to reproduce work performed with the original weights.
Store the releases in separate local directories to keep both.

V1 and V2 are this GGUF repository's release labels, not official Fish Audio
model-version names. Both releases use the same trained model architecture.

## Files and precision

| File | Size | Routed experts | Routers / gates | Text embedding | Speech head | Other backbone matrices |
| --- | ---: | --- | --- | --- | --- | --- |
| [drama-3-backbone-8bit-experts-Q4_K_S.gguf](./drama-3-backbone-8bit-experts-Q4_K_S.gguf) | 22.91 GiB | Q4_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [drama-3-backbone-8bit-experts-Q3_K_S.gguf](./drama-3-backbone-8bit-experts-Q3_K_S.gguf) | 18.93 GiB | Q3_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [drama-3-backbone-8bit-experts-Q2_K.gguf](./drama-3-backbone-8bit-experts-Q2_K.gguf) | 15.88 GiB | Q2_K | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| [drama-3-backbone-4bit-experts-Q4_K_S.gguf](./drama-3-backbone-4bit-experts-Q4_K_S.gguf) | 21.77 GiB | Q4_K | Q4_K | Q4_0 | Q4_K | Q4_K |
| [drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf](./drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf) | 22.97 GiB | Q4_K | FP32 | Q8_0 | Q8_0 | Q8_0 |
| [drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf](./drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf) | 23.87 GiB | Q4_K | FP32 | BF16 | BF16 | Q8_0 |

Q3_K_S and Q4_K_S identify the file profiles. All 120 routed expert projection
banks have uniform Q3_K or Q4_K storage, respectively. This uses pure expert
banks with explicit component overrides, rather than higher-bit promotion
heuristics from a general-purpose quantization preset. Q8_0 is scaled integer
quantization, distinct from the original checkpoint's scaled FP8 experts.

Audio-tower matrices and waveform codec weights remain FP16. Backbone and
audio-tower normalization vectors remain FP32; codec normalization remains
FP16. The FP32-router profiles restore the new checkpoint's 40 routers and
40 shared-expert gates directly from their original BF16 values, retaining
those values exactly in FP32. The BF16 embedding/head profile additionally
restores the original embedding and complete 252,288-row output head.
These are selected precision changes within Q4-expert models, not entirely
FP32 or BF16 models.

## Runtime and use

These packages use GGUF architecture `audiocpp` and require the native
`fish_drama3` backend in [audio.cpp](https://github.com/0xShug0/audio.cpp).
They include configuration, tokenizer, codec, model contract, and license
resources. General-purpose GGUF text-model runtimes cannot load this model.
See the [Drama 3 runtime documentation](https://github.com/0xShug0/audio.cpp/blob/main/docs/models/fish_drama3.md).

Download a V2 profile from the default revision:

```powershell
uv run --no-project --python 3.12 --with huggingface_hub hf download Jmica/Drama-3-GGUF `
  drama-3-backbone-8bit-experts-Q4_K_S.gguf --local-dir models/Drama-3-GGUF-V2
```

To download the V1 weights instead, keep the same filename and select the
preserved revision:

```powershell
uv run --no-project --python 3.12 --with huggingface_hub hf download Jmica/Drama-3-GGUF `
  drama-3-backbone-8bit-experts-Q4_K_S.gguf --revision original-2026-10-13 `
  --local-dir models/Drama-3-GGUF-V1
```

Use separate local directories to keep both versions. For example:

```powershell
.\audiocpp_cli.exe --task tts --family fish_drama3 --backend cuda `
  --mode streaming --model .\models\Drama-3-GGUF-V2\drama-3-backbone-8bit-experts-Q4_K_S.gguf `
  --text 'Hello there.' --seed 123 --max-tokens 512 --threads 8 `
  --session-option fish_drama3.cpu_expert_layers=40 `
  --session-option fish_drama3.context_length=8192 `
  --request-option top_k=4097 --request-option top_p=0.9 `
  --request-option temperature=1.0 --request-option text_chunk_size=128 --out speech.wav
```

Forty CPU expert layers is the conservative configuration used for the new
functional checks, not a speed recommendation. Offloaded experts need host RAM.
File size is not required VRAM. Context, reference history, backend, and CPU
offload affect memory and may change sampled output.

## Validation limits

All six files passed structural checks for tensor count, component storage
types, expert banks, the full output head, and metadata privacy. Every retained
tensor payload in the FP32-router variants was compared byte-for-byte with the
new Q4/Q8 package, and restored components were checked against the new source
checkpoint.

The local functional check generated English and Japanese audio with every profile using the native CUDA runtime at audio.cpp commit `4faef969850e2dd485e717fe2159875b91cfa3dc`. The check used 40 CPU expert layers to preserve concurrent GPU workloads. It does not establish speed, perceptual parity, voice similarity, or correct words in every take. An old-checkpoint control request lost its connection during validation and was retained without retry. Remaining requests used fresh server processes with unchanged runtime and sampling settings. Server reuse and uninterrupted multi-request operation are not established by this check.

The earlier listening comparisons and 5,000-case silence/EOS studies used the
original checkpoint. Those results do not describe this replacement checkpoint.
The new files are not claimed to eliminate trailing silence, missing speech,
generation-cap stops, or inconsistent emotion and whisper delivery. Higher
precision is not a guarantee of better individual takes. Broader multilingual,
long-form, streaming, and perceptual validation remain separate from these
small functional checks.

## Conversion

The native [conversion script](https://github.com/0xShug0/audio.cpp/blob/main/tools/community_models/convert_fish_drama3.py)
reconstructs the scaled FP8 experts using their original 128-by-128 block scales,
then prepares expert banks, mixed quantization, codec normalization, and runtime
resources. Python dependencies are managed with uv and conversion runs on CPU.
The reusable FP16 intermediate is approximately 68.2 GiB and is not distributed.
The FP32-router and BF16 embedding/head profiles also require restoring the
corresponding original checkpoint values after standard conversion.

## License and attribution

The model materials and these independent conversions are subject to the
Fish Audio Community License, Version 1.0. See [LICENSE](LICENSE) and
[NOTICE](NOTICE). Conversion and validation preparation were assisted by
Codex (OpenAI).
