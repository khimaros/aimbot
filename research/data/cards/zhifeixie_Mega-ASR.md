---
base_model:
  - Qwen/Qwen3-ASR-1.7B
license: apache-2.0
language:
- en
- zh
tags:
- automatic-speech-recognition
- speech-recognition
- audio
- robust-asr
- qwen3-asr
pipeline_tag: automatic-speech-recognition
---

# Mega-ASR

<p align="center">
  <img src="assets/figures/mega_asr_logo.png" alt="Mega-ASR overview" width="70%">
</p>

Mega-ASR is a robust automatic speech recognition system designed for real-world audio with severe acoustic degradation. It targets noisy, reverberant, clipped, band-limited, overlapping, and otherwise difficult recording conditions where standard ASR systems often produce empty outputs, omissions, repetitions, or hallucinated text.

The release contains the Qwen3-ASR-1.7B foundation model files, Mega-ASR adaptation weights, and an audio quality router. The router decides whether to use the robust Mega-ASR path or the base recognition path for each input, which helps preserve clean-speech recognition quality while improving robustness on degraded speech.

## Model Details

- **Model name:** Mega-ASR
- **Task:** Automatic speech recognition
- **Backbone:** Qwen3-ASR-1.7B
- **Primary use case:** In-the-wild ASR under challenging acoustic conditions
- **Default decoding:** Greedy decoding
- **Default max new tokens:** 256 in the Mega-ASR inference wrapper
- **Router:** Audio quality classifier with a default threshold of 0.5
- **License:** Apache-2.0

## Repository Contents

```text
Mega-ASR/
├── Qwen3-ASR-1.7B/              # Backbone model, tokenizer, processor, and generation config
├── mega-asr-merged/             # Mega-ASR adaptation weights used by the inference wrapper
├── audio_quality_router/        # Audio quality router checkpoint
└── README.md                    # Model card
```

## Intended Use

Mega-ASR is intended for speech-to-text transcription of real-world audio, especially audio affected by compound acoustic distortions. Example scenarios include far-field recording, environmental noise, reverberation, low-quality microphones, compression artifacts, partial signal corruption, and mixed acoustic conditions.

## Quick Start

Install the Mega-ASR codebase and dependencies:

```bash
git clone https://github.com/xzf-thu/Mega-ASR.git
cd Mega-ASR

conda create -n mega-asr python=3.10 -y
conda activate mega-asr
pip install -r requirements.txt
```

Place this checkpoint directory at:

```text
ckpt/Mega-ASR
```

Run inference:

```bash
python infer.py --audio /path/to/audio.wav --ckpt_dir ckpt/Mega-ASR
```

Disable routing if you want to always use the robust recognition path:

```bash
python infer.py --audio /path/to/audio.wav --ckpt_dir ckpt/Mega-ASR --routing false
```

Python usage:

```python
from MegaASR.model.megaASR import MegaASR

model = MegaASR(
    model_path="ckpt/Mega-ASR/Qwen3-ASR-1.7B",
    router_checkpoint="ckpt/Mega-ASR/audio_quality_router/best_acc_model.pt",
    routing_enabled=True,
)

result = model.infer("/path/to/audio.wav", return_route=True)
print(result)
```

## Decoding Defaults

The Mega-ASR wrapper uses Qwen3-ASR generation defaults unless explicitly overridden. In the provided wrapper, `max_new_tokens` is set to 256.

The default generation configuration is deterministic:

```text
do_sample: false
num_beams: 1
repetition_penalty: 1.0
top_p: 1.0
top_k: 50
```

Because `do_sample` is false, decoding is greedy by default and sampling controls such as temperature, top-p, and top-k do not affect normal inference.

## Training Summary

Mega-ASR is trained for robust speech recognition in realistic acoustic environments. The training pipeline uses acoustic-to-semantic supervised fine-tuning, where the model is exposed to progressively harder speech examples and learns to recover both local acoustic details and sentence-level semantics under degradation.

The system is designed to improve recognition robustness on difficult audio while using a routing mechanism to reduce unnecessary changes on clean audio.

<p align="center">
  <img src="assets/figures/method_overview.png" alt="Mega-ASR training and inference overview" width="100%">
</p>

## Evaluation

Mega-ASR is evaluated on standard ASR benchmarks, noisy robustness benchmarks, and in-the-wild compound acoustic scenarios. The recommended evaluation metrics are:

- **WER** for English and whitespace-tokenized languages
- **CER** for Chinese and character-based evaluation

<p align="center">
  <img src="assets/figures/radar_results.png" alt="Mega-ASR evaluation results" width="100%">
</p>

The Mega-ASR repository includes an evaluation script:

```bash
python src/MegaASR/eval/evaluate_wer.py \
  --ckpt_dir ckpt/Mega-ASR \
  --input_jsonl examples/test.jsonl \
  --output_jsonl outputs/pred_with_wer.jsonl
```

Input JSONL format:

```json
{"audio": "examples/audio/noise.wav", "answer": "I usually take the quieter road home because the main street gets crowded after work."}
```

## Citation

If you use Mega-ASR, please cite the project:

```bibtex
@misc{xie2026megaasrinthewild2speechrecognition,
      title={Mega-ASR: Towards In-the-wild^2 Speech Recognition via Scaling up Real-world Acoustic Simulation},
      author={Zhifei Xie and Kaiyu Pang and Haobin Zhang and Deheng Ye and Xiaobin Hu and Shuicheng Yan and Chunyan Miao},
      year={2026},
      eprint={2605.19833},
      archivePrefix={arXiv},
      primaryClass={cs.SD},
      url={https://arxiv.org/abs/2605.19833},
}
```

## Acknowledgements

Mega-ASR builds on Qwen3-ASR. We thank the Qwen3-ASR team and the creators of public speech and audio datasets used in the project.
