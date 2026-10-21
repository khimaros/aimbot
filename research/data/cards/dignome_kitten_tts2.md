---
license: other
license_name: stellon-labs-community-license
license_link: LICENSE
pipeline_tag: text-to-speech
base_model: KittenML/kitten-tts-2
base_model_relation: quantized
language:
  - en
  - ar
  - zh
  - fr
  - de
  - hi
  - it
  - pt
  - ru
  - es
tags:
  - audio.cpp
  - gguf
  - text-to-speech
  - voice-cloning
  - multilingual
---

# Kitten TTS 2 for audio.cpp

**Powered by Stellon Labs.**

Self-contained multilingual GGUF exports of KittenML/kitten-tts-2 weights at
revision `f2eee74f4467855ad58fe16f1fb7b7df473263fd`. Each file includes an S3
MeanFlow decoder, speaker encoders, tokenizer, and all 48 prepared voice entries.

Use an audio.cpp build containing the updated Kitten TTS 2 BF16/Q8/Q4 support.
The model family is `kitten_tts2`. BF16/Q8/Q4 model-manager installations share
`models/kitten-tts2-v2/`, with a distinct filename for each precision. Leave `kitten_tts2.weight_type` unset, or use
`native`, to preserve each file's stored precision. Inference needs no Python
or LibTorch installation.

## Downloads

**Q8 is the default and recommended package.** Q4 is experimental.

| File | LM body / embedding | Size |
| --- | --- | --- |
| [kitten-tts2-bf16-multilingual.gguf](./kitten-tts2-bf16-multilingual.gguf) | BF16 / BF16 | 4,603,407,040 bytes |
| [kitten-tts2-q8-v2-multilingual.gguf](./kitten-tts2-q8-v2-multilingual.gguf) | Q8_0 / BF16 | 3,282,201,248 bytes |
| [kitten-tts2-q4-multilingual.gguf](./kitten-tts2-q4-multilingual.gguf) | Q4_0 / Q8_0 | 2,273,735,456 bytes |
| [kitten-tts2-nvfp4-multilingual.gguf](./kitten-tts2-nvfp4-multilingual.gguf) | NVFP4 / Q8_0 | 2,273,736,960 bytes |
| [kitten-tts2-tq2_1-default-multilingual.gguf](./kitten-tts2-tq2_1-default-multilingual.gguf) | TQ2_1 / Q8_0, default decoder | 1,855,355,872 bytes |
| [kitten-tts2-tq2_1-student-w8-multilingual.gguf](./kitten-tts2-tq2_1-student-w8-multilingual.gguf) | TQ2_1 / Q8_0, student W8 decoder | 1,437,030,016 bytes |
| [kitten-tts2-tq2_1-student-w4-multilingual.gguf](./kitten-tts2-tq2_1-student-w4-multilingual.gguf) | TQ2_1 / Q8_0, student W4 decoder | 1,413,363,424 bytes |

Verify downloads with [SHA256SUMS](./SHA256SUMS). Names describe LM storage,
not the precision of every tensor in the file.

**NVFP4 and TQ2_1 require the [new package-support branch](https://github.com/dignome/audio.cpp-custom/tree/kitten-tts2-nvfp4-tq2-student).**
The WebUI labels are **GGUF NVFP4**, **GGUF TQ2_1 (CPU)** for the default decoder,
**GGUF TQ2_1 (CPU w4)** for the W4 student, and **GGUF TQ2_1 (CPU w8)** for the W8
student. Their model-manager folders are `models/kitten-tts2-nvfp4/`,
`models/kitten-tts2-tq2_1-default/`, `models/kitten-tts2-tq2_1/`, and
`models/kitten-tts2-tq2_1-w8/`, respectively. W8 requires a build with W8 support;
earlier versions of the package-support branch do not recognize it.

NVFP4 uses the existing GGML NVFP4 CUDA kernels and the default decoder. Its
body-weight reconstruction error is approximately 2.3954% relative L2, not a
speech-quality score. All body projections retain NVFP4 on CUDA. Local testing
uses an RTX 4060 Ti; other generations have not been validated here.

TQ2_1 uses this branch's type ID 44 and CPU kernels; it is not compatible with
stock audio.cpp or Kitten's separate type-43 GGUF files. Select `--backend cpu`.
Its ternary body storage is exact relative to the supplied BF16 checkpoint.
The default-decoder package retains the original S3 MeanFlow decoder and its
voice conditioning. The W4 student package stores 474 decoder matrices in packed
W4 and runs 426 linears as INT8 on CPU automatically; 48 convolutions use F32.
Both preset speech and cloning use the decoder selected by the package. These
packages do not use the upstream emb4 embedding.

The W8 package uses the shipped frozen one-step student_w8 decoder. Its 457
remaining quantized matrices are stored as INT8 codes with F32 per-channel
scales, reconstructing the exported weights exactly. The frozen time-conditioning
constants are retained. At runtime, 409 linears use INT8; 48 convolutions use F32.
It supports preset voices and cloning, retains all 48 voice entries, and needs
no Python or LibTorch at runtime. These checks do not establish better speed or
perceptual quality than W4.

Q8 and Q4 preserve the supplied ternary body weights exactly. Q4 quantizes the
embedding directly from full BF16 to Q8_0, with about 0.44% relative L2 weight
error. This is a weight reconstruction measurement, not an audio quality score.
On CUDA, Q4 down projections load as BF16 to avoid non-finite computation,
adding about 483 MiB compared with retaining those projections as Q4.

## Speech and cloning

```sh
audiocpp_cli --family kitten_tts2 --model models/kitten-tts2-v2/kitten-tts2-q8-v2-multilingual.gguf --backend cpu --threads 8 --task tts --voice-id Bruno --text "Hello from Kitten TTS 2." --out hello.wav
```

Use `--backend cuda` for a CUDA-enabled build and a package other than TQ2_1. For custom voice cloning:

```sh
audiocpp_cli --family kitten_tts2 --model models/kitten-tts2-v2/kitten-tts2-q8-v2-multilingual.gguf --backend cpu --threads 8 --task clon --voice-ref reference.wav --reference-text "The exact words in the reference recording." --text "The new words to say." --out cloned.wav
```

Cloning requires a 1–30 second reference recording and its transcript. Preset
synthesis needs no separate voice recordings. Output is mono 24 kHz.

The package includes 47 upstream presets and the `PreparedBruno` alias. Named
English voices include Bruno, Bella, Jasper and Luna. Language presets cover
Arabic, Chinese, French, German, Hindi, Italian, Portuguese, Russian and Spanish.
Choose a matching preset or reference clip for the target language. Generation
checks cover these ten languages including English; they do not establish
native-speaker pronunciation quality.

## Validation and limitations

CPU and NVIDIA CUDA synthesis and cloning are checked locally. Q4 remains
experimental: longer samples sometimes omitted words. Broader listening review
is needed before relying on it for long-form speech. File sizes do not describe
runtime RAM or VRAM requirements.

TQ2_1 offers default, student_w4 and student_w8 decoders; the other exports use
the default decoder. The upstream TL2/emb4 embedding format is not included. Long chunked
speech can omit words with the default or student decoder. Streaming and
automatic reference transcription are not supported. Write numbers and
abbreviations as spoken words when needed.

## Sources and license

- Kitten weights: KittenML/kitten-tts-2, revision `f2eee74f4467855ad58fe16f1fb7b7df473263fd`.
- Default S3 decoder: ResembleAI/chatterbox-turbo, revision `749d1c1a46eb10492095d68fbcf55691ccf137cd`.
- Speaker encoder: the Kitten-distributed speaker model, attributed upstream to pyannote/embedding.

Model materials retain the Stellon Labs Community License in [LICENSE](./LICENSE).
Bundled components retain their respective terms in [native/LICENSE](./native/LICENSE)
and [speaker/LICENSE](./speaker/LICENSE). See [NOTICE](./NOTICE) for attribution
and conversion details.

Conversion and native integration by **dignome**. Prepared with AI assistance
and validated locally.
