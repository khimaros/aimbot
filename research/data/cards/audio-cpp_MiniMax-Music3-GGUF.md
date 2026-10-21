---
library_name: audio.cpp
pipeline_tag: text-to-audio
license: other
license_name: minimax-music3-community-license
base_model:
  - MiniMaxAI/MiniMax-Music3
tags:
  - audio.cpp
  - gguf
  - minimax-music3
---

# MiniMax Music 3 GGUF

GGUF package for MiniMax Music 3 for audio.cpp.

Star our repo so you don't miss important updates! https://github.com/0xShug0/audio.cpp

Upstream model: https://huggingface.co/MiniMaxAI/MiniMax-Music3
Upstream license: https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE

Compatible Q8 GGUF package: https://huggingface.co/joemattie/MiniMax-Music3-GGUF

## Notes

- The implementation is available on the `main` branch and release 0.6.1.
- The current runtime uses model-local resource loading instead of treating the v1 spec as the runtime contract. This keeps component selection flexible while the package layout and option surface settle.
- The default component mix favors Q4_0 for the large language model and flow transformer, with Q8_0 for the RVQ depth decoder.
- BF16, Q8_0, and Q4_0 component variants are included for quality/performance comparison.
- Longer generations such as five-minute songs are supported as long-form runs, but they are currently tuned for completion and quality checks rather than realtime throughput.
- Memory usage remains an active optimization target for larger durations and alternate component mixes.

## Performance Snapshot

Measured on an RTX 5090 with CUDA using a 30-second lyric generation request, 30 flow steps, flow guidance scale 1.7, AR guidance scale 1.5, and top-k 50. Peak VRAM is the observed `nvidia-smi` process peak during a warmup-plus-measured-request run.

| Component mix | Language model | RVQ depth decoder | Flow transformer | RTF | Speed | Peak VRAM |
|---|---|---|---|---:|---:|---:|
| Default Q4/Q8/Q4 | `q4_0` | `q8_0` | `q4_0` | 0.738 | 1.35x realtime | 9.8 GiB |
| Q8 | `q8_0` | `q8_0` | `q8_0` | 0.832 | 1.20x realtime | 13.4 GiB |
| BF16 | `bf16` | `bf16` | `bf16` | 1.389 | 0.72x realtime | 19.4 GiB |

## Quick Start

The prompt is for smoke end-to-end test only. 

```bash
audiocpp_cli \
  --task gen \
  --family minimax_music3 \
  --model MiniMax-Music3-GGUF \
  --backend cuda \
  --text "A bright pop rock song with clean drums and a clear male vocal." \
  --request-option 'lyrics=City lights are shining low. I keep moving with the glow. Turn it up and let it fly. Sing the melody tonight.' \
  --request-option duration_sec=10 \
  --request-option num_inference_steps=30 \
  --out output.wav
```

## Components

Default audio.cpp component mix:

- `language_model_q4_0.gguf`
- `rvq_depth_decoder_q8_0.gguf`
- `transformer_q4_0.gguf`
- `condition_encoder.gguf`
- `vocoder.gguf`

The BF16, Q8_0, and Q4_0 component variants are included for measurement and quality/performance comparison.

Component GGUFs can be selected explicitly for experiments:

```bash
--session-option minimax_music3.language_model_gguf=language_model_bf16.gguf
--session-option minimax_music3.language_model_gguf=language_model_q8_0.gguf
--session-option minimax_music3.rvq_depth_decoder_gguf=rvq_depth_decoder_bf16.gguf
--session-option minimax_music3.rvq_depth_decoder_gguf=rvq_depth_decoder_q8_0.gguf
--session-option minimax_music3.flow_transformer_gguf=transformer_bf16.gguf
--session-option minimax_music3.flow_transformer_gguf=transformer_q8_0.gguf
```

## License

This GGUF package follows the upstream MiniMax-Music3 COMMUNITY LICENSE. The
license text is included in `LICENSE`; review it before use, especially for
commercial deployment.
