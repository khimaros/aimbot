---
license: mit
language:
- multilingual
datasets:
- google/fleurs-r
- parler-tts/libritts_r_filtered
tags:
- speech-restoration
- speech-enhancement
- dereverberation
- gguf
- crispasr
base_model: sarulab-speech/sidon-v0.1
base_model_relation: quantized
pipeline_tag: audio-to-audio
---

# Sidon GGUF

GGUF quantization of [SaruLab Sidon v0.1](https://huggingface.co/sarulab-speech/sidon-v0.1), a multilingual
speech-restoration model that removes noise and reverberation and restores speech bandwidth. This repository packages
the model for native inference with [CrispASR](https://github.com/CrispStrobe/CrispASR).

The model contains the first eight layers of w2v-BERT 2.0 with the Sidon LoRA adapter merged, followed by Sidon's
continuous DAC decoder. The exact SeamlessM4T log-mel window and filter bank are embedded in the GGUF.

## Model

| File | Precision | Size | Input | Output |
| --- | --- | ---: | --- | --- |
| `sidon-v0.1-f16.gguf` | FP16 weights, FP32 norms/biases | 469.8 MiB | 16 kHz mono | 48 kHz mono |

SHA-256:

```text
7E27282A09BE71E2F37E87731A074B291A2CAB0D3F1DE4A8F8EB48421587E912  sidon-v0.1-f16.gguf
```

## CrispASR usage

```powershell
crispasr --s2s `
  -m sidon-v0.1-f16.gguf `
  -f input.wav `
  --s2s-output restored-48khz.wav
```

CrispASR detects the `sidon` architecture from GGUF metadata. The current S2S interface processes a complete clip and
returns a complete restored clip; it is not a streaming interface.

GPU execution can be selected explicitly with `--gpu-backend cuda` or `--gpu-backend vulkan`. The Vulkan predictor
uses native decompositions for operations that GGML's Vulkan backend does not currently fuse.

## Conversion

```powershell
python models/convert-sidon-to-gguf.py `
  --base w2v-bert-2.0 `
  --sidon sidon_raw_weight `
  --output sidon-v0.1-f16.gguf `
  --dtype f16
```

The converter consumes the original
[`sidon_raw_weight`](https://huggingface.co/sarulab-speech/sidon_raw_weight) adapter/decoder and
[`facebook/w2v-bert-2.0`](https://huggingface.co/facebook/w2v-bert-2.0) base weights.

## Validation

On a one-second validation clip, native CrispASR output matched a PyTorch reconstruction of the same merged raw
checkpoint at waveform cosine similarity `0.999966` for both the FP32 diagnostic conversion and this FP16 GGUF.

Sidon's separately published TorchScript bundle is a slightly different checkpoint revision, so direct comparison to
that bundle is not an exact raw-checkpoint parity test.

The complete native pipeline was also tested on an NVIDIA GeForce RTX 5070 Ti with a 9.14-second input:

| Backend | Total time | Relative to realtime | Validation |
| --- | ---: | ---: | --- |
| CPU | 10.53 s | 0.87x | Reference |
| CUDA | 0.32 s | 28.2x | Vulkan waveform cosine `0.999490` |
| Vulkan | 0.66–0.74 s | 12.3–13.9x | Predictor 701/701 and DAC 704/704 graph nodes native |

Vulkan-to-CPU waveform cosine was `0.999559`. Backend timings include feature extraction, graph setup, inference, and
output transfer; they are hardware- and driver-dependent.

## License and attribution

Sidon, w2v-BERT 2.0, and the DAC decoder are released under the MIT license. See the
[Sidon repository](https://github.com/sarulab-speech/Sidon) and
[Sidon paper](https://arxiv.org/abs/2509.17052) for authorship and training details.

### Contributors

- Wataru Nakata
- Yuki Saito

### Acknowledgements

The development of the original model was supported by project gamma of the National Institute of Advanced Industrial
Science and Technology.
