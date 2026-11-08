---
license: apache-2.0
language:
- de
- fr
- it
- pt
- es
base_model:
- Qwen/Qwen3-4B-Instruct-2507
---
# Hojo-ASR-Multi-V1

## Overview

### Introduction

Hojo‑ASR‑Multi‑V1 is a high‑performance conversational speech recognition model built upon the Qwen3 LLM decoder. It adopts the classic Encoder‑Adapter‑LLM architecture with a customized multi‑frame acoustic fusion structure, making full use of fine‑grained acoustic features and the powerful semantic capabilities of the large language model.

Optimized via multi‑stage modular training and reinforcement learning, the model performs well in complex real‑world scenarios such as noisy conditions, informal pronunciation and oral correction. Building on its recognition capabilities, the model further expands its full‑coverage multilingual recognition capacity, fully supporting major languages including German, French, Spanish, Portuguese, Japanese, Italian, Arabic, Korean and Russian.


## Quickstart

### Environment Setup

The easiest way to use Hojo-ASR is to install the `hojo-asr` Python package from PyPI.

```bash
conda create -n hojo-asr python=3.10
conda activate hojo-asr
```

Run the following command to get the minimal installation with transformers-backend support:

```bash
pip install -U hojo-asr
```

### Sample Usage

```python
from hojo_asr import HOJO_ASR
parser = argparse.ArgumentParser()
parser.add_argument(
    "--batch_size", type=int, default=10, help="batch size for inference"
)
parser.add_argument("--device", type=str, default="cuda:0")
args = parser.parse_args()
model = HOJO_ASR.load_model("HojoAI/Hojo-ASR-Multi-V1", device=args.device)
# Transcribe
# List of wav paths; for a single scp file pass a str (see dataset.resolve_infer_audio_input)
wav_paths = [
    "/path/to/audio.wav",
]
wav_scp = "test.scp"
with open(wav_paths[0], "rb") as f:
    wav_bytes = f.read()
#LIST OF BYTES
wav_bytes_list = [wav_bytes, wav_bytes]
res = model.run_infer(wav_scp, batch_size=args.batch_size)
# res = model.run_infer(wav_paths, batch_size=args.batch_size)
# res = model.run_infer(wav_bytes_list, batch_size=args.batch_size)
for val in res:
    print("key :", val["key"], " text :", val["text"])
```


## Evaluation

ASR Benchmarks on Public Multilingual Datasets (WER ↓)

| Dataset | Hojo-ASR-Multi-V1 |
|:--------:|:-----------------:|
| German CoVoST | 3.85 |
| German FLEURS | 4.08 |
| French CoVoST | 4.53 |
| French MLS | 2.95 |
| French FLEURS | 3.33 |
| Italian CoVoST | 2.44 |
| Italian MLS | 5.35 |
| Italian FLEURS | 2.3 |
| Spanish CoVoST | 3.27 |
| Spanish MLS | 3.31 |
| Spanish FLEURS | 2.66 |
| Portuguese MLS | 4.07 |
| Portuguese FLEURS | 3.61 |

## Roadmap
- [x] release Hojo-ASR-4B model and inference engine
- [x] support Mandarin, English, Cantonese, and Sichuan dialect
- [x] support multi-lingual and multi-dialect

  
## Commercial Support
We offer commercial support for teams integrating Hojo ASR into their products. This includes integration assistance, custom voice development, and enterprise licensing.

Contact us or email developer@hojoai.com to discuss your requirements.
  
## Credits
Thanks to the following open-source works:
- [Qwen](https://huggingface.co/Qwen)
- [WenetSpeech-Yue](https://github.com/ASLP-lab/WenetSpeech-Yue)
- [WenetSpeech-Chuan](https://github.com/ASLP-lab/WenetSpeech-Chuan)


## Licence
This project is open-sourced under the [Apache 2.0 License](LICENSE.txt), which can be freely used for academic research, personal projects, and commercial secondary development.