---
license: cc-by-4.0
language:
- en
pipeline_tag: automatic-speech-recognition
tags:
- audio
- speech-recognition
- transcription
- ggml
- gguf
- parakeet
- ctc
- fastconformer
library_name: ggml
base_model: nvidia/parakeet-ctc-1.1b
---

# Parakeet CTC 1.1B — GGUF (ggml-quantised)

GGUF / ggml conversions of [`nvidia/parakeet-ctc-1.1b`](https://huggingface.co/nvidia/parakeet-ctc-1.1b) for use with the `crispasr` CLI from **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR/)**.

Parakeet CTC 1.1B is NVIDIA's 1.1 B-parameter English ASR model — the deeper sibling of `parakeet-ctc-0.6b`:

- **English-only**, lowercase output
- **FastConformer encoder** — 42 layers (vs 24 in 0.6b), d_model=1024, 8 heads + single CTC head; trained on 64K hours of English (40K private + 24K public)
- **CC-BY-4.0** licence
- WERs (slightly better than 0.6b across the board): LibriSpeech-clean **1.83 %**, LibriSpeech-other **3.54 %**, TEDLIUM-v3 **4.20 %**, GigaSpeech **10.27 %**, Common Voice **6.53 %**

This repo provides four quantisations, all converted from the upstream `.nemo` checkpoint via `models/convert-stt-fastconformer-ctc-to-gguf.py` and quantised with `crispasr-quantize`.

## Files

| File | Size | Notes |
| --- | ---: | --- |
| `parakeet-ctc-1.1b.gguf`        | ~2.13 GB | F16, full precision |
| `parakeet-ctc-1.1b-q8_0.gguf`   | ~1.26 GB | Q8_0, near-lossless |
| `parakeet-ctc-1.1b-q5_0.gguf`   | ~910 MB  | Q5_0 |
| `parakeet-ctc-1.1b-q4_k.gguf`   | ~795 MB  | **Q4_K — recommended default** |

All quantisations produce the same JFK 11 s transcript.

## Quick start

```bash
# 1. Build the runtime
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc) --target crispasr-cli

# 2. Run — the CLI auto-downloads Q4_K from this repo by friendly name:
./build/bin/crispasr -m parakeet-ctc-1.1b -f your-audio.wav

# Or pre-download a specific quant via huggingface_hub and point to it:
python -c "from huggingface_hub import hf_hub_download; print(hf_hub_download('cstr/parakeet-ctc-1.1b-GGUF', 'parakeet-ctc-1.1b-q8_0.gguf'))"
./build/bin/crispasr -m parakeet-ctc-1.1b-q8_0.gguf -f your-audio.wav
```

The `crispasr` CLI auto-detects the backend from filename — `parakeet-ctc-*.gguf` routes to `fastconformer-ctc` because the architecture is identical to the `stt_en_fastconformer_ctc_*` family. Registry key `parakeet-ctc-1.1b` triggers Q4_K auto-download.

## Model architecture

| Component | Details |
| --- | --- |
| Encoder       | **42-layer** FastConformer, d=1024, 8 heads, head_dim=128, FFN=4096, conv kernel=9, attention biases ON |
| Subsampling   | dw_striding stack, 8× temporal (50 → 12.5 fps) |
| CTC head      | Conv1d(1024 → 1025), k=1; vocab 1024 SentencePiece + 1 blank |
| Audio         | 16 kHz mono, 80 mel bins, n_fft=512, hop=160, win=400 |
| Parameters    | ~1.1 B |

Identical to the 0.6b variant in every dimension *except* encoder depth (42 vs 24 layers). The crispasr `fastconformer-ctc` backend reads `n_layers` from the GGUF metadata and resizes per-layer state at load time, so no code changes are needed for the deeper model.

## Output convention

Lowercase, un-punctuated English. For cased + punctuated, see [`cstr/parakeet-tdt-0.6b-v3-GGUF`](https://huggingface.co/cstr/parakeet-tdt-0.6b-v3-GGUF) (multilingual TDT, slightly higher WER but cased+punct out-of-the-box) or post-process via crispasr's `--punc-model`.

## Attribution

- **Original model:** [`nvidia/parakeet-ctc-1.1b`](https://huggingface.co/nvidia/parakeet-ctc-1.1b) (CC-BY-4.0). NVIDIA NeMo team.
- **GGUF conversion + ggml runtime:** [`CrispStrobe/CrispASR`](https://github.com/CrispStrobe/CrispASR) — FastConformer-CTC backend, see `src/canary_ctc.cpp`.

## Related

- C++ runtime: **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**
- Smaller CTC variant: [`cstr/parakeet-ctc-0.6b-GGUF`](https://huggingface.co/cstr/parakeet-ctc-0.6b-GGUF)
- TDT counterpart (multilingual, cased+punct): [`cstr/parakeet-tdt-0.6b-v3-GGUF`](https://huggingface.co/cstr/parakeet-tdt-0.6b-v3-GGUF)

## License

CC-BY-4.0, inherited from the base model. Use of these GGUF files must comply with the CC-BY-4.0 license including attribution.
