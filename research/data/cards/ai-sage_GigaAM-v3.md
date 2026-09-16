---
license: mit
language:
- ru
- en
pipeline_tag: automatic-speech-recognition
---

# GigaAM-v3

GigaAM-v3 is a Conformer-based foundation model with 220–240M parameters, pretrained on diverse Russian speech data using the HuBERT-CTC objective.
It is the third generation of the GigaAM family and provides state-of-the-art performance on Russian ASR across a wide range of domains.

GigaAM-v3 includes the following model variants:
- `ssl` — self-supervised HuBERT–CTC encoder pre-trained on 700,000 hours of Russian speech  
- `ctc` — ASR model fine-tuned with a CTC decoder  
- `rnnt` — ASR model fine-tuned with an RNN-T decoder 
- `e2e_ctc` — end-to-end CTC model with punctuation and text normalization  
- `e2e_rnnt` — end-to-end RNN-T model with punctuation and text normalization  

`GigaAM-v3` training incorporates new internal datasets: callcenter conversations, speech with background music, natural speech, and speech with atypical characteristics.
the models perform on average **30%** better on these new domains, while maintaining the same quality as previous GigaAM generations on public benchmarks.

The table below reports the Word Error Rate (%) for `GigaAM-v3` and other existing models over diverse domains.

| Set Name          | V3_CTC | V3_RNNT | T-One + LM | Whisper |
|:------------------|-------:|--------:|-----------:|--------:|
| Open Datasets     |   3.0  |     2.6 |        5.7 |    12.0 |
| Golos Farfield    |   4.5  |     3.9 |       12.2 |    16.7 |
| Natural Speech    |   7.8  |     6.9 |       14.5 |    13.6 |
| Disordered Speech |  20.6  |    19.2 |       51.0 |    59.3 |
| Callcenter        |  10.3  |     9.5 |       13.5 |    23.9 |
| **Average**       | **9.2**| **8.4** |       19.4 |    25.1 |

The end-to-end ASR models (`e2e_ctc` and `e2e_rnnt`) produce punctuated, normalized text directly.
In end-to-end ASR comparisons of `e2e_ctc` and `e2e_rnnt` against Whisper-large-v3, using Gemini 2.5 Pro as an LLM-as-a-judge, GigaAM-v3 models win by an average margin of **70:30**.

For detailed results, see [metrics](https://github.com/salute-developers/GigaAM/blob/main/evaluation.md).

## Usage
```python
from transformers import AutoModel

revision = "e2e_rnnt"  # can be any v3 model: ssl, ctc, rnnt, e2e_ctc, e2e_rnnt
model = AutoModel.from_pretrained(
    "ai-sage/GigaAM-v3",
    revision=revision,
    trust_remote_code=True,
)

transcription = model.transcribe("example.wav")
print(transcription)
```

Recommended versions:
- `torch==2.8.0`, `torchaudio==2.8.0`
- `transformers==4.57.1`
- `pyannote-audio==4.0.0`, `torchcodec==0.7.0`
- (any) `hydra-core`, `omegaconf`, `sentencepiece`

Full usage guide can be found in the [example](https://github.com/salute-developers/GigaAM/blob/main/colab_example.ipynb).

**License:** MIT

**Paper:** [GigaAM: Efficient Self-Supervised Learner for Speech Recognition (InterSpeech 2025)](https://arxiv.org/abs/2506.01192)