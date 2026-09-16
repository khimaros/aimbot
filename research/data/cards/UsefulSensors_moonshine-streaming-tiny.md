---
license: mit
language:
- en
library_name: transformers
pipeline_tag: automatic-speech-recognition
---
# Moonshine Streaming

[[Paper]](https://download.moonshine.ai/docs/moonshine_streaming_paper.pdf)

This is the model card for the Moonshine Streaming automatic speech
recognition (ASR) models trained and released by Useful Sensors. Moonshine Streaming
pairs a lightweight 50~Hz audio frontend with a sliding-window Transformer
encoder to deliver low-latency streaming ASR on edge-class hardware. The encoder
uses bounded local attention and no positional embeddings (an "ergodic"
encoder), while an adapter injects positional information before a standard
autoregressive decoder.

This model card follows the recommendations from Model Cards for Model Reporting
(Mitchell et al.). See the paper draft in this repository for full details.

## Usage

Moonshine Streaming is supported in Hugging Face Transformers. The following example
matches the standard seq2seq ASR API and uses the streaming model checkpoint:

```bash
pip install --upgrade pip
pip install --upgrade git+https://github.com/huggingface/transformers.git#egg=transformers datasets[audio]
```

```python
from transformers import MoonshineStreamingForConditionalGeneration, AutoProcessor
from datasets import load_dataset, Audio
import torch

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = MoonshineStreamingForConditionalGeneration.from_pretrained(
    "usefulsensors/moonshine-streaming-small"
).to(device).to(torch_dtype)
processor = AutoProcessor.from_pretrained("usefulsensors/moonshine-streaming-small")

dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
dataset = dataset.cast_column("audio", Audio(processor.feature_extractor.sampling_rate))
sample = dataset[0]["audio"]

inputs = processor(
    sample["array"],
    return_tensors="pt",
    sampling_rate=processor.feature_extractor.sampling_rate,
)
inputs = inputs.to(device, torch_dtype)

# Limit max output length to avoid hallucination loops.
token_limit_factor = 6.5 / processor.feature_extractor.sampling_rate
seq_lens = inputs.attention_mask.sum(dim=-1)
max_length = int((seq_lens * token_limit_factor).max().item())

generated_ids = model.generate(**inputs, max_length=max_length)
print(processor.decode(generated_ids[0], skip_special_tokens=True))
```

Note: the current Transformers code path does not yet implement fully efficient
streaming for these models. It uses the flash-attention backend's sliding-window
attention when available.

## Model Details

### Model type

Sequence-to-sequence ASR model with a streaming, sliding-window Transformer
encoder and an autoregressive Transformer decoder.

### Supported languages

English (trained and evaluated on English datasets).

### Model sizes

| Size  | Parameters | Encoder / Decoder layers | Encoder dim | Decoder dim |
|:-----:|:----------:|:------------------------:|:-----------:|:-----------:|
| Tiny  | 34M        | 6 / 6                    | 320         | 320         |
| Small | 123M       | 10 / 10                  | 620         | 512         |
| Medium| 245M       | 14 / 14                  | 768         | 640         |

### Architecture summary

- Audio frontend: 50~Hz features using simple time-domain operations, CMVN, and
  two causal stride-2 convolutions.
- Encoder: sliding-window self-attention with no positional embeddings (ergodic
  encoder). Windowing uses $(16,4)$ for the first two and last two layers and
  $(16,0)$ for intermediate layers, giving an 80~ms lookahead in the lookahead
  layers.
- Adapter: adds learned positional embeddings and aligns dimensions before the
  decoder.
- Decoder: causal Transformer with RoPE, autoregressively generating text.

## Model Use

### Intended use

These models are intended for low-latency, on-device English speech
transcription on memory- and compute-constrained platforms (roughly
0.1--1~TOPS and sub-1~GB memory budgets). Typical applications include live
captioning, voice commands, and real-time transcription.

### Out-of-scope use

These models are not intended for non-consensual surveillance, speaker
identification, or high-stakes decision-making contexts. They have not been
robustly evaluated for tasks outside English ASR.

## Training Data

Moonshine Streaming was trained on roughly 300K hours of speech data. This includes the
original Moonshine training sources (about 200K hours of public web data and
open datasets) plus an additional 100K hours of internally prepared speech
data. See the paper for details and dataset sources.

## Performance and Limitations

### Open ASR benchmark results (WER %)

| Dataset               | Tiny (34M) | Small (123M) | Medium (245M) |
|:----------------------|----------:|-------------:|--------------:|
| AMI                   | 19.03     | 12.54        | 10.68         |
| Earnings-22           | 20.27     | 13.53        | 11.90         |
| GigaSpeech            | 13.90     | 10.41        | 9.46          |
| LibriSpeech (clean)   | 4.49      | 2.49         | 2.08          |
| LibriSpeech (other)   | 12.09     | 6.78         | 5.00          |
| SPGISpeech            | 6.16      | 3.19         | 2.58          |
| TED-LIUM              | 6.12      | 3.77         | 2.99          |
| VoxPopuli             | 14.02     | 9.98         | 8.54          |
| **Average**           | **12.01** | **7.84**     | **6.65**      |

### Known limitations

- The decoder is autoregressive, so full-output latency grows with transcript
  length even when TTFT is low.
- The Transformers implementation does not yet perform fully efficient
  streaming; it relies on the flash-attention backend for sliding-window
  attention.
- Like other seq2seq ASR models, Moonshine Streaming can hallucinate words that are not
  present in the audio, and may repeat phrases, especially on short or noisy
  segments.

## Broader Implications

Moonshine Streaming enables low-cost, low-latency transcription, which benefits
accessibility and user interaction on edge devices. At the same time, ASR
capabilities can be misused for surveillance or other harmful purposes. Users
should consider consent, privacy, and domain-specific evaluation before
deployment.

## Citation

**TBD**