---
license: other
license_name: applied-brain-research-open-license
license_link: https://www.appliedbrainresearch.com/license
language:
- en
metrics:
- wer
tags: [asr, speech, state-space-model, ssm, edge-ai, audio, on-device, real-time, low-power, low-latency, cpu, embedded]
pipeline_tag: automatic-speech-recognition
library_name: transformers
---

# ABR's niagara-38m-batch.en SSM

**38M parameters. 9.36% average WER.**

**[Try it in your browser](https://huggingface.co/spaces/abr-ai/niagara-asr-demo)**. Runs on a free CPU instance, no GPU.

The niagara-38m-batch.en model is a
[State Space Model](https://huggingface.co/blog/lbourdois/get-on-the-ssm-train) (SSM) with attention
that performs automatic speech recognition (ASR), trained and released by
[Applied Brain Research](http://www.appliedbrainresearch.com/) (ABR). This model contains
\~38m parameters, transcribes speech in English, and was trained on \~50k
hours of speech data (competitors use about 200k hours). This is a batch model variant designed for
direct comparison with other models on the Open ASR Leaderboard. SSMs are an ideal solution for
streaming contexts, but to provide a more direct comparison with other models in the leaderboard
this model is not streaming. A live streaming variant of this english ASR model with sub-120ms
latency and features such as punctuation, capitalization and custom vocabulary along with other
similar models for other languages is available under commercial license from
[ABR](https://www.appliedbrainresearch.com/state-space-models).

## Why “Niagara”?

ABR names its model families after rivers. State space models process sequential data as a
continuous flow, much like a river — always moving forward, maintaining state efficiently over time.
Niagara is ABR’s ASR model family, named for the river in our home province of Ontario, Canada.

## Usage

### Install requirements

```bash
pip install datasets torch torchcodec transformers sentencepiece
```

### Automatically instantiate the model

```python
from datasets import load_dataset
from transformers import AutoFeatureExtractor, AutoModel, AutoTokenizer

model_id = "abr-ai/niagara-38m-batch.en"
feature_extractor = AutoFeatureExtractor.from_pretrained(
    model_id, trust_remote_code=True
)
model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
```

### Transcribing using Python

First, we need a sample of english speech data

```python
dataset = load_dataset("librispeech_asr", "clean", split="test", streaming=True)
samples = list(dataset.take(3))  # Take 3 examples
```

Then run the model:

```python
audio = samples[0]["audio"]["array"]
inputs = feature_extractor(audio)
outputs = model(**inputs)
transcription = tokenizer.decode_from_logits(outputs.logits, outputs.attention_mask)
print(transcription[0])
```

### Transcribing many audio files

```python
audio_list = [sample["audio"]["array"] for sample in samples]
inputs = feature_extractor(audio_list)
outputs = model(**inputs)
transcriptions = tokenizer.decode_from_logits(outputs.logits, outputs.attention_mask)
for t in transcriptions:
    print(t)
```

### Using the pipeline

The model also works with the standard transformers pipeline (using the
speech data loaded above):

```python
from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="abr-ai/niagara-38m-batch.en",
    trust_remote_code=True,
)
print(pipe(audio)["text"])
```

### Using a GPU

The model runs on CPU by default. To use a GPU, move both the model and the
feature extractor:

```python
model = model.to("cuda")
feature_extractor = feature_extractor.to("cuda")
```

or pass `device="cuda"` when constructing the pipeline.

Note that the first forward pass loads the compiled graph, which takes some
time; subsequent calls are fast.

### Input

This model accepts 16000 Hz Mono-channel Audio (wav files) as input.

### Output

This model provides transcribed speech as a string for a given audio sample.

## Model Details

The SSM ASR model is trained for English speech recognition and transcribes audio into text. ABR
developed the model to demonstrate small, efficient, real-time, accurate speech recognition can be
performed with SSMs and run on low cost third party hardware. The model uses
38m parameters. The version posted here is a non-causal model (like most on
the leaderboard), to give fair performance comparisons. It is also available as a cascaded model,
meaning it produces extremely low latency (\<120ms from first audio to token) causal outputs as well
as 1s latency non-causal outputs. These two streams can be merged to have a quick response that
updates after 1s with the final result.

Release Date: April 15, 2026

### Model Type

Automatic speech recognition model transcribing speech audio to text in English.

### Model Use

The intended use of the model is for evaluation by AI developers who want extremely small but
performant ASR. We recognize that it is not possible to enforce our intended use guidelines. The
models should not be used to transcribe individuals without their explicit consent, or be used to
infer any particular human features as only text output is generated by the model. Other
capabilities have not been evaluated. We recommend against using the model in high-risk settings
(such as making important decisions) where errors in the model output can result in significant
consequences for users. We strongly recommend that users perform extensive evaluations for their use
cases.

## Training

The model was trained on datasets partially listed below. It uses MFCC preprocessing on the input
and is trained with CTC loss. It uses greedy CTC decoding and sentencepiece tokenization.

### Datasets

The training datasets contain \~50k hours of English speech, including:

- LibriSpeech (clean)
- VoxPopuli
- GigaSpeech
- Common Voice
- TED-LIUM
- Europarl
- Earnings-22
- AMI-IHM
- SPGISpeech

## Performance

The posted model transcribes audio to lower case english with no punctuation. Performance is
reported in terms of Word Error Rate (WER%) for the non-causal model.

| Benchmark | niagara-9m | niagara-19m | niagara-38m | niagara-84m |
| :--- | ---: | ---: | ---: | ---: |
| AMI | 23.57% | 18.86% | 15.87% | 13.87% |
| Earnings22 | 17.88% | 14.52% | 12.09% | 11.15% |
| GigaSpeech | 16.24% | 13.99% | 12.56% | 11.57% |
| LibriSpeech test.clean | 6.59% | 4.81% | 3.84% | 3.05% |
| LibriSpeech test.other | 14.74% | 11.19% | 9.35% | 7.62% |
| SPGISpeech | 5.25% | 3.77% | 3.10% | 2.62% |
| VoxPopuli | 11.89% | 9.92% | 8.73% | 7.78% |
| **Average WER** | **13.74%** \* | **11.01%** | **9.36%** | **8.24%** \* |
| RTFx | — | 2,840 | 2,623 | — |

Word Error Rate (WER), lower is better. RTFx is inverse real-time factor, higher is better. All
figures are from the [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
([as of 2026-06-13](https://huggingface.co/datasets/hf-audio/open-asr-leaderboard-results/blob/b27154be631663d5af6d166883f519e7f63b7243/english_short_latest.csv), measured on NVIDIA A100-SXM4-80GB).

\* Not on the Open ASR Leaderboard yet. Figures marked this way were measured by ABR with the
leaderboard's evaluation code; benchmarks marked — were not measured, and the average covers
only the benchmarks shown, so it is not directly comparable with the leaderboard's Average WER.

## Related models

| Model | Parameters | Average WER |
| :--- | :--- | ---: |
| [abr-ai/niagara-9m-batch.en](https://huggingface.co/abr-ai/niagara-9m-batch.en) | 9M | 13.74% \* |
| [abr-ai/niagara-19m-batch.en](https://huggingface.co/abr-ai/niagara-19m-batch.en) | 19M | 11.01% |
| [abr-ai/niagara-38m-batch.en](https://huggingface.co/abr-ai/niagara-38m-batch.en) | 38M | 9.36% |
| [abr-ai/niagara-84m-batch.en](https://huggingface.co/abr-ai/niagara-84m-batch.en) | 84M | 8.24% \* |

## Competitive Comparisons

Open models on the [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) with fewer than 100M parameters
as of 2026-06-13, sorted by accuracy (100% minus Average WER). Sizes are as reported by the
leaderboard. Rows marked \* are not on the leaderboard yet (see the note above).

| Model | Size (B) | Accuracy (%) |
| :--- | ---: | ---: |
| abr-ai/niagara-84m-batch.en | 0.08 | 91.76 \* |
| abr-ai/niagara-38m-batch.en | 0.04 | 90.64 |
| usefulsensors/moonshine-base | 0.06 | 89.39 |
| nvidia/stt_en_conformer_transducer_small | 0.014 | 89.16 |
| abr-ai/niagara-19m-batch.en | 0.02 | 88.99 |
| openai/whisper-base.en | 0.07 | 88.90 |
| nvidia/stt_en_conformer_ctc_small | 0.01 | 88.27 |
| usefulsensors/moonshine-streaming-tiny | 0.03 | 87.16 |
| usefulsensors/moonshine-tiny | 0.03 | 86.35 |
| abr-ai/niagara-9m-batch.en | 0.01 | 86.26 \* |
| openai/whisper-tiny.en | 0.04 | 86.22 |
| facebook/data2vec-audio-base-960h | 0.09 | 70.44 |
| facebook/wav2vec2-base-960h | 0.09 | 69.40 |

## Limitations

Since this model was trained on publicly available speech datasets, the performance of this model
might degrade for speech which includes technical terms, significant noise, or vernacular that the
model has not been trained on. The model might also perform worse for accented speech. The model
might generate text that was not actually spoken in the input audio.

## Broader Implications

We intend for the SSM ASR model to be used for beneficial purposes, including low cost transcription
on low cost hardware, providing accessibility, and improving real-time voice user interfaces. As
with all AI technology, there are also reasons to be concerned about dual-use. For instance,
lowering the cost may allow broader deployment of undesired surveillance technology or the
inexpensive scaling of existing technology. Related safety concerns come from the model being used
to identify individuals or being deployable in very small footprint hardware.

## License

This model is made available under
[ABR's open license](https://www.appliedbrainresearch.com/license).

## Citation

```bibtex
@misc{
  AppliedBrainResearch2026,
  author = {Applied Brain Research, Inc},
  title = {niagara-38m-batch.en},
  year = {2026},
  publisher = {HuggingFace},
  journal = {HuggingFace repository},
  howpublished = {\url{https://huggingface.co/abr-ai/niagara-38m-batch.en}},
}
```

## Also available from ABR

This open-source batch model demonstrates ABR’s SSM architecture for ASR. ABR also offers
commercially licensed models with additional capabilities: real-time streaming inference (sub-120ms
first-token latency from first audio), speech recognition for other languages, punctuation and
capitalization, custom vocabulary, hardware-optimized deployment for many leading edge processors,
Text-to-Speech (TTS) models, and enterprise support with SLAs. For more information, visit
appliedbrainresearch.com or contact
[info@appliedbrainresearch.com](mailto:info@appliedbrainresearch.com).

## About Applied Brain Research

Applied Brain Research (ABR) is based in Waterloo, Ontario, Canada. ABR develops efficient speech
and language AI using its proprietary and patented state space model architectures. More at
[appliedbrainresearch.com](http://appliedbrainresearch.com).
