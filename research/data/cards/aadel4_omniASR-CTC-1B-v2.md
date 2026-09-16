---
library_name: transformers
tags:
- speech
- audio
- wav2vec2
- automatic-speech-recognition
pipeline_tag: automatic-speech-recognition
---

# omniASR-CTC-1B-v2

Wav2Vec2 CTC ASR model (v2) converted from the [OmniLingual](https://github.com/facebookresearch/omnilingual-asr) fairseq2 checkpoint `omniASR_CTC_1B_v2`.

This model outputs CTC logits over a SentencePiece vocabulary and can transcribe speech in multiple languages.

# Code Base

The code base for the conversion can be found [here](https://github.com/ahmedadelattia/omnilingual_to_hf). I was only able to convert the 300M and 1B models due to GPU limitations. Contributions are welcome.

## Model details

| Property             | Value |
|---|---|
| HF class             | `Wav2Vec2ForCTC` |
| Encoder layers       | 48 |
| Hidden size          | 1280 |
| Attention heads      | 16 |
| FFN intermediate     | 5120 |
| Vocabulary size      | 10288 |
| Source framework     | fairseq2 |
| Source card          | `omniASR_CTC_1B_v2` |
| Parity verification  | ✅ Verified |


Numerical parity against the original fairseq2 checkpoint has been confirmed: outputs match to within `atol=1e-4` on a held-out audio sample.

Sample transcriptions on the held-out audio clip:

| Model | Transcript |
|---|---|
| fairseq2 (source) | `concord returned to its place amidst the tents` |
| HuggingFace (this repo) | `concord returned to its place amidst the tents` |

## Usage

```python
from transformers import Wav2Vec2ForCTC, AutoProcessor
import torch, torchaudio

processor = AutoProcessor.from_pretrained("aadel4/omniASR-CTC-1B-v2")
model     = Wav2Vec2ForCTC.from_pretrained("aadel4/omniASR-CTC-1B-v2")
model.eval()

waveform, sr = torchaudio.load("audio.wav")
if sr != 16_000:
    waveform = torchaudio.functional.resample(waveform, sr, 16_000)

inputs = processor(
    waveform.squeeze().numpy(), sampling_rate=16_000, return_tensors="pt"
)
with torch.no_grad():
    logits = model(**inputs).logits          # (1, T, vocab)

pred_ids   = torch.argmax(logits, dim=-1)
transcript = processor.decode(pred_ids[0])
print(transcript)
```
