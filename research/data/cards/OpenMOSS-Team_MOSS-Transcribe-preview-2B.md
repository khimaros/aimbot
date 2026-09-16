---
language: en
library_name: transformers
pipeline_tag: automatic-speech-recognition
tags:
  - speech
  - english
  - qwen3
  - audio
  - reinforcement-learning
license: apache-2.0
datasets:
  - openslr/librispeech_asr
  - speechcolab/gigaspeech
  - mozilla-foundation/common_voice_17_0
  - facebook/voxpopuli
  - edinburghcstr/ami
  - anton-l/earnings22
  - kensho/spgispeech
metrics:
  - wer
model-index:
  - name: MOSS-Transcribe-preview-2B
    results:
      - task:
          type: automatic-speech-recognition
        dataset:
          name: Open ASR Leaderboard
          type: hf-audio/open-asr-leaderboard
        metrics:
          - type: wer
            value: 4.87
            name: Average WER
---

# MOSS-Transcribe-preview-2B

<p align="center">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_imgaes_demo/openmoss_x_mosi" height="50" align="middle" />
</p>

<div align="center">

  <a href="https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-preview-2B"><img src="https://img.shields.io/badge/HuggingFace-Model-yellow?logo=huggingface"></a>
  <a href="https://huggingface.co/spaces/hf-audio/open_asr_leaderboard"><img src="https://img.shields.io/badge/Open%20ASR%20Leaderboard-Listing-blue?logo=huggingface"></a>
  <a href="https://mosi.cn/#models"><img src="https://img.shields.io/badge/Blog-View-blue?logo=internet-explorer&amp"></a>
  <a href="https://x.com/Open_MOSS"><img src="https://img.shields.io/badge/Twitter-Follow-black?logo=x&amp"></a>
  <a href="https://discord.gg/fvm5TaWjU3"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&amp"></a>

</div>

MOSS-Transcribe-preview-2B is an English speech-to-text model that pairs a Qwen3-1.7B-base language-model backbone with a Qwen3-Omni-MoE audio encoder. A gated-MLP adapter projects audio features into the language-model embedding space. The model is trained on public English ASR corpora and fine-tuned with reinforcement learning on the Open ASR Leaderboard training splits.

The model has approximately 2.4B parameters and is distributed as a single `bfloat16` safetensors shard of approximately 4.84 GB.

## Model Details

- **Developed by:** OpenMOSS Team
- **Model type:** Automatic Speech Recognition / speech-to-text model
- **Language:** English
- **License:** Apache-2.0
- **Library:** Transformers
- **Backbone:** Qwen3-1.7B-base, 28 layers, hidden size 2048
- **Audio encoder:** Qwen3-Omni-MoE audio encoder
- **Adapter:** Gated-MLP adapter, hidden size 8192
- **Parameter size:** approximately 2.4B
- **Checkpoint format:** `bfloat16` safetensors

## Intended Use

This model is intended for English automatic speech recognition, including transcription of English speech audio for research and evaluation purposes.

## Evaluation

Evaluated on the [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
test sets. Predictions are produced with greedy decoding (`num_beams=1`,
`max_new_tokens=512`), a single dataset-agnostic chat template, and scored with
the leaderboard's standardized scoring (English normalizer + word-level edit
distance with compound merging). TED-LIUM is not currently part of the
leaderboard run and is therefore excluded.

| Dataset | WER (%) |
|---|---|
| AMI | 8.37 |
| Earnings22 | 7.84 |
| GigaSpeech | 6.78 |
| LibriSpeech test.clean | 1.21 |
| LibriSpeech test.other | 2.84 |
| SPGISpeech | 1.63 |
| VoxPopuli | 5.39 |
| **Average** | **4.87** |

## Inference

```python
import librosa
import torch
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.dynamic_module_utils import get_class_from_dynamic_module

REPO = "OpenMOSS-Team/MOSS-Transcribe-preview-2B"
DEVICE = "cuda:0"

model = AutoModelForCausalLM.from_pretrained(
    REPO, dtype=torch.bfloat16, trust_remote_code=True
).to(DEVICE).eval()
tokenizer = AutoTokenizer.from_pretrained(REPO, trust_remote_code=True)

MossProcessor = get_class_from_dynamic_module("processing_Moss.MossProcessor", REPO)
MelConfig = get_class_from_dynamic_module("processing_Moss.MelConfig", REPO)

mel_cfg = MelConfig(
    mel_sr=16000,
    mel_dim=128,
    mel_n_fft=400,
    mel_hop_length=160,
)
processor = MossProcessor(tokenizer, config=mel_cfg, enable_time_marker=False)
processor.load_template(hf_hub_download(REPO, "chat_template_default.py"))

waveform, _ = librosa.load("your_audio.wav", sr=16000)
inputs = processor(audio=waveform, return_tensors="pt").to(DEVICE)
inputs["audio_data"] = inputs["audio_data"].to(model.dtype)

with torch.no_grad():
    out_ids = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False,
        num_beams=1,
        use_cache=True,
        eos_token_id=[processor.end_token_id],
    )

new_ids = out_ids[:, inputs["input_ids"].shape[1]:]
transcript = processor.batch_decode(new_ids, skip_special_tokens=True)[0].strip()
print(transcript)
```

## Audio Frontend

- **Sample rate:** 16 kHz
- **Features:** Whisper log-mel filterbank
- **Mel bins:** 128
- **FFT size:** 400
- **Hop length:** 160

## Training

The model was trained on public English ASR corpora and fine-tuned with reinforcement learning on the Open ASR Leaderboard training splits.

## Limitations

The model is designed for English ASR. It may perform worse on non-English speech, heavy accents, noisy recordings, overlapping speakers, far-field audio, domain-specific terminology, or audio conditions that differ significantly from the training and evaluation data. The output should be manually reviewed before use in high-stakes settings.

## Citation

```bibtex
@misc{moss_transcribe_2025,
  title        = {{MOSS-Transcribe-preview-2B}},
  author       = {{OpenMOSS Team}},
  year         = {2025},
  howpublished = {\url{https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-preview-2B}}
}
```

## License

This model is released under the Apache-2.0 license.
