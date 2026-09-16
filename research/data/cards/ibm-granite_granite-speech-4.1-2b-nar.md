---
license: apache-2.0
language:
- en
- fr
- de
- es
- pt
base_model:
- ibm-granite/granite-4.0-1b-base
library_name: transformers
tags:
- speech
- asr
- non-autoregressive
- ctc
- speech_recognition
- automatic_speech_recognition
---
# Granite-Speech-4.1-2B-NAR

**Model Summary:**
Granite-Speech-4.1-2B-NAR is a non-autoregressive (NAR) speech recognition model that formulates ASR as conditional transcript editing.
Instead of decoding tokens one at a time, it edits a CTC hypothesis in a single forward pass using a bidirectional LLM, achieving competitive accuracy with faster inference than autoregressive alternatives.
The model is based on the **NLE** (Non-autoregressive LLM-based Editing) architecture described in [this paper](https://arxiv.org/abs/2603.08397).

For applications where accuracy is the primary concern, consider [**granite-speech-4.1-2b**](https://huggingface.co/ibm-granite/granite-speech-4.1-2b), an autoregressive model from the Granite Speech 4.1 family which achieves higher transcription accuracy at the cost of increased inference latency. Granite-speech-4.1-2b produces punctuated and capitalized transcripts, supports AST and keyword-biased recognition, and includes Japanese.

When speaker or word-timing information is needed, consider using [**granite-speech-4.1-2b-plus**](https://huggingface.co/ibm-granite/granite-speech-4.1-2b-plus), which extends the above model with speaker-attributed ASR (speaker labels + word transcripts) and word-level timing information.

**Release Date**: April 2026

**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

**Supported Languages:**
English, French, German, Spanish, Portuguese

**Intended Use:**
The model is intended for automatic speech recognition tasks, particularly in latency-sensitive applications where fast inference is critical.

## Evaluation Results
### Open ASR leaderboard results
RTFx-WER results on the [Open ASR leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) (as of Apr 2026).

<img src="rtf_wer.png" alt="RTFx vs WER">

### Additional results
Greedy decoding with bfloat16 inference. WER computed with [jiwer](https://github.com/jitsi/jiwer) after [whisper_normalizer](https://github.com/openai/whisper) `EnglishTextNormalizer` normalization. 
Open ASR Leaderboard results  may differ slightly due to normalization and scoring pipeline differences.
Measured RTFx of ~1820 on a single H100 GPU (batched inference, batch size 128).

| Dataset | WER | Dataset | WER |
|---|---|---|---|
| LibriSpeech clean | 1.29 | MLS EN | 4.77 |
| LibriSpeech other | 2.75 | MLS DE | 4.75 |
| CommonVoice 15 EN | 6.50 | MLS ES | 3.31 |
| CommonVoice 15 DE | 4.73 | MLS FR | 4.52 |
| CommonVoice 15 ES | 4.02 | MLS PT | 11.86 |
| CommonVoice 15 FR | 7.17 | AMI IHM | 7.91 |
| CommonVoice 15 PT | 2.57 | AMI SDM | 19.59 |
| Earnings-22 | 8.48 | GigaSpeech | 10.12 |
| SPGISpeech | 3.04 | TED-LIUM | 3.67 |
| VoxPopuli | 5.83 | | |

## Usage

### Installation
We require `flash_attention_2` for inference, since this backend supports sequence packing and respects the `is_causal=False` flag. 
Requires `transformers>=5.5.3` and `torch>=2.9.1`.

```shell
# Fresh install (CUDA 12.8, Python 3.10+)
pip install torch==2.9.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu128
pip install transformers>=5.5.3 accelerate safetensors huggingface-hub tokenizers
pip install soundfile
pip install flash-attn==2.8.3 --no-build-isolation
```

### Inference with `transformers`

```python
import torch
import torchaudio
from huggingface_hub import hf_hub_download
from transformers import AutoModel, AutoProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "ibm-granite/granite-speech-4.1-2b-nar"
model = AutoModel.from_pretrained(model_name, trust_remote_code=True,
                                  attn_implementation="flash_attention_2", device_map=device,
                                  dtype=torch.bfloat16).eval()
processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)

# Load sample audio from the repo
audio_path = hf_hub_download(repo_id=model_name, filename="10226_10111_000000.wav")
waveform, sr = torchaudio.load(audio_path)
if sr != 16000:
    waveform = torchaudio.functional.resample(waveform, sr, 16000)
if waveform.shape[0] > 1:
    waveform = waveform.mean(dim=0, keepdim=True)
waveform = waveform.squeeze(0)

# Extract features, run transcription, decode
inputs = processor([waveform], device=device)
output = model.transcribe(**inputs)
transcriptions = processor.batch_decode(output.preds)

print(f"Prediction: {transcriptions[0]}")
```

## Model Architecture

The architecture consists of three components:

**(1) CTC Speech Encoder (440M params)**

A 16-layer Conformer encoder trained with CTC on character-level targets. It processes 16kHz audio with stacked log-mel features (80 mel bins, 2-frame stacking) and uses block attention with 4-second audio blocks and self-conditioning at layer 8.
The encoder has a **dual CTC head**: alongside the character-level output, a secondary BPE head produces CTC logits over the LLM's 100K token vocabulary. The BPE head uses posterior-weighted pooling (window size 4) with importance weights derived from mid-layer blank probabilities (`1 - blank_prob`).

**(2) Q-Former Projector (160M params)**

A 2-layer window Q-Former that downsamples the concatenated hidden representations from 4 encoder layers (layers 4, 8, 12, 16) by 5x.
Each 15-frame window is reduced to 3 queries via cross-attention, resulting in a 10Hz acoustic embedding rate for the LLM (2x from encoder + 5x from projector).

**(3) Bidirectional LLM Editor (1B params, LoRA-adapted)**

[granite-4.0-1b-base](https://huggingface.co/ibm-granite/granite-4.0-1b-base) with its causal attention mask removed, enabling bidirectional context.
Adapted with LoRA (rank 128) applied to both attention and MLP layers. The LLM receives concatenated audio embeddings and an interleaved CTC hypothesis with insertion slots, then predicts the edited transcript in a single parallel forward pass using a CTC objective.

### How Granite-speech NAR Works
<img src="diagram.png" alt="Architecture">

1. The frozen CTC encoder produces acoustic embeddings and an initial hypothesis.
2. The hypothesis is interleaved with insertion slots (blank tokens between each token)
3. The projected audio embeddings are concatenated with the interleaved hypothesis embeddings
4. The bidirectional LLM predicts edits (copy, insert, delete, replace) at all positions simultaneously
5. CTC greedy decoding (argmax + collapse) produces the final transcript

This design exploits the **identity mapping bias** of Transformers: residual connections and tied embeddings make the model naturally inclined to copy input tokens, so it focuses learning capacity on corrections rather than full reconstruction.

## Training Data

The model was trained on approximately 130K hours of speech across five languages (English, Spanish, French, German, Portuguese), using publicly available datasets including CommonVoice 15, MLS, LibriSpeech, Libriheavy long, AMI, Granary VoxPopuli, Granary YODAS, Earnings-22, Fisher, CallHome, and SwitchBoard.
For additional training details, see the [paper](https://arxiv.org/abs/2603.08397).

## Infrastructure

Training was completed on IBM's Blue Vela cluster using 16 H100 GPUs (2 nodes) for 5 epochs (3 days).

## Ethical Considerations and Limitations

The model is designed specifically for automatic speech recognition and does not generate free-form text, which limits the risk of hallucination compared to general-purpose speech-language models.
However, transcription accuracy varies across languages and acoustic conditions. Performance may be weaker on languages with less training data (e.g., Portuguese) or in challenging acoustic environments (e.g., far-field, overlapping speech).

The model's editing approach is conservative by design — it prefers deletions over insertions, which reduces hallucination risk but may occasionally drop words in noisy conditions.

To enhance safety, we recommend using granite-speech-4.1-2b-nar alongside Granite Guardian. Granite Guardian is a fine-tuned instruct model designed to detect and flag risks in prompts and responses across key dimensions outlined in the IBM AI Risk Atlas.



## Resources
- 📄 Read our papers: 
    - [NLE: Non-autoregressive LLM-based ASR by Transcript Editing](https://arxiv.org/abs/2603.08397) 
    - [Granite-speech: open-source speech-aware LLMs with strong English ASR capabilities](https://arxiv.org/abs/2505.08699)
    - [Self-Speculative Decoding for LLM-based ASR with CTC Encoder Drafts](https://arxiv.org/abs/2603.11243)
    - [Contextual Biasing for ASR in Speech LLM with Common Word Cues and Bias Word Position Prediction](https://arxiv.org/abs/2604.12398)
    - [In-Sync: Adaptation of Speech Aware Large Language Models for ASR with Word Level Timestamp Predictions](https://arxiv.org/abs/2604.22817)
    - [Speaker Attributed Automatic Speech Recognition Using Speech Aware LLMS](https://arxiv.org/abs/2604.11269)

- ⭐️ Learn about Granite: https://www.ibm.com/granite
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources