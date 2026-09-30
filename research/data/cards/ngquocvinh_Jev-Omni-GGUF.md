---
license: apache-2.0
base_model: akhilaaa3/Jev-Omni
base_model_relation: quantized
library_name: llama.cpp
pipeline_tag: text-classification
tags:
- gguf
- llama.cpp
- jev-omni
- quantized
- multimodal
- text-classification
---

# Jev-Omni GGUF

Community GGUF quantizations of [akhilaaa3/Jev-Omni](https://huggingface.co/akhilaaa3/Jev-Omni).

<div align="center" style="background-color:#f59e0b;color:#ffffff;padding:16px 20px;border-radius:10px;line-height:1.7;">
☕ If this GGUF made your day easier, a coffee would make mine.<br>
<a href="https://ko-fi.com/ngquocvinh" style="color:#ffffff;"><strong style="color:#ffffff;">Send a coffee ☕</strong></a><br>
I build and test these releases myself. Your coffee helps keep me going.<br>
Thank you for supporting this work.
</div>

## About Jev-Omni

[Jev-Omni](https://huggingface.co/akhilaaa3/Jev-Omni) is a multimodal decision classifier built on Gemma 4 12B IT. Given a state, a question, and answer options, it returns a probability for each option rather than a generated explanation. The upstream checkpoint supports text, images, audio, and video; it accepts 2–256 options, with quality best established for up to 20. Its configuration declares a 262,144-token maximum position length; long-context behavior is not validated for these GGUFs.

This package converts the upstream BF16 backbone to GGUF, keeps Jev-Omni's trained decision head in FP32, and ships the vision/audio projector separately. The included adapter requests unnormalized token embeddings from `llama-server` and applies that decision head. A plain text-generation request is not the classifier interface.

[![DecisionBench Medium accuracy](upstream-medium-accuracy.png)](https://huggingface.co/akhilaaa3/Jev-Omni)

Figure: [DecisionBench Medium accuracy reported for the upstream merged checkpoint; these values are not measurements of the GGUF files](https://huggingface.co/akhilaaa3/Jev-Omni).

These are quantizations only; no training or fine-tuning was performed here. Each published backbone quant is built directly from the same locked BF16 GGUF, never from another quantized file. This repository is updated incrementally as each variant passes its runtime smoke test.

## Quick start

Start a local embeddings server with the Q8 variant and its multimodal projector:

```bash
./llama-server \
  -m Jev-Omni-Q8_0.gguf \
  --mmproj mmproj-jev-omni.gguf \
  --embedding --pooling none --embd-normalize -1 \
  --host 127.0.0.1 --port 8080 --no-webui \
  -ngl 8 -c 4096 -b 512 -ub 512
```

In a second terminal, run one English decision:

```bash
python -m pip install numpy
python jev_omni_gguf_decide.py \
  --head decision-head-f32.npz \
  --server http://127.0.0.1:8080 \
  --state 'The meeting starts at 10 AM. It is now 9 AM.' \
  --question 'Has the meeting started?' \
  --options Yes No
```

The adapter returns the selected option, confidence, and normalized option probabilities. The `-ngl` value controls GPU offload; use `-ngl 0` for CPU-only execution or adjust it to available memory. Image, audio, and video inputs use the adapter's `--image`, `--audio`, or `--video` argument. Audio requires `ffmpeg`; video also requires `Pillow` and `opencv-python-headless`. Q8 runtime smoke coverage exercised text and image inference and the audio request path; it is not a task-accuracy evaluation, and video has not been smoke-tested. The llama.cpp runtime also marks audio input experimental.

## Reproducibility and validation

The [reproducibility manifest](reproducibility/manifest.md) records the pinned upstream revision and hashes, BF16 conversion input, llama.cpp revision, model-specific calibration/imatrix provenance, quantization commands, artifact checksums, and smoke-test profile. [SHA256SUMS.txt](SHA256SUMS.txt) verifies the published package files. Raw build and validation logs are retained locally and are not part of this repository.

Calibration is a small, synthetic, text-only set matching Jev-Omni's decision-prompt format. It is provided to reproduce the imatrix, not as evaluation data. No hold-out fidelity evaluation has been run for these GGUFs, so no quantized-quality percentages are claimed.

## License and attribution

The upstream Jev-Omni checkpoint declares Apache-2.0; see [LICENSE](LICENSE). The included GGUF embedding-to-decision adapter and FP32 decision head are carried over unchanged from [Reza2kn/Jev-Omni-Q4_K_M-GGUF](https://huggingface.co/Reza2kn/Jev-Omni-Q4_K_M-GGUF); all four head tensors were verified bit-for-bit against the locked upstream `head.pt`. See [NOTICE.md](NOTICE.md) for details.

These are community GGUF quantizations, not an official Jev-Omni release or endorsement.
