---
license: apache-2.0
language:
  - multilingual
  - en
  - fr
  - de
  - es
  - pt
base_model:
  - ibm-granite/granite-4.0-1b-base
library_name: transformers
pipeline_tag: automatic-speech-recognition
tags:
  - vllm
---

# Granite-Speech-4.1-2B-Plus

## Model update (October 2026)

We have updated the model weights and configuration. The updated model is more accurate, especially for keyword biasing and for word-level timestamps on long samples. It is a drop-in replacement for the previous version, but we have also updated our usage recommendations to get the best performance.

In the tables below, GSP v2610 refers to the updated model and GSP v2604 to the original release.

## Model Summary

Granite-Speech-4.1-2B-Plus (GSP) has similar capabilities to the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) model. The plus model adds two new community-requested rich transcription features that can be activated with a simple prompt change: speaker-attributed ASR (speaker labels and word transcripts) and word-level timing information. Unlike the base model, the plus model doesn't provide punctuation and capitalization.

The model was trained on corpora similar to the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) model which were augmented with speaker turns and word-level timestamp tags. This allows the model to provide different modes of functionality controlled by different prompts.

Two additional model variants explore different capabilities and inference optimization:

- [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) for applications where accuracy is the primary concern with support for punctuated, capitalized transcripts, AST and keyword-biased recognition, and includes Japanese.
- [Granite-Speech-4.1-2B-NAR](https://huggingface.co/ibm-granite/granite-speech-4.1-2b-nar) introduces a novel non-autoregressive architecture for higher throughput

### ASR only mode

In this mode the model generates only the text transcript similar to the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) model.

### Speaker attributed ASR (SAA)

In this mode, the model adds speaker tags in the format of `[Speaker N]:` where $N$ is the speaker number, before each speaker turn. The speakers are numbered by their order of appearance so the first speaker will always be marked with `[Speaker 1]:` and the second with `[Speaker 2]:`, etc. For example: `"[Speaker 1]: Hello how are you [Speaker 2]: I'm fine and how are you feeling [Speaker 1]: I feel wonderful"`.

See [Resources](#resources) for more information about SAA.

### Word-level timestamps

In this mode, the model adds timestamp tags after each word indicating the end of the word in the audio. Silences are transcribed as `_` and a timestamp tag also indicates their end. The format of the tag is `[T:N]` where $N$ is an integer number indicating the time in centiseconds (1/100th of a second). To reduce the amount of generated tokens, only the last three digits of $N$ are provided. This causes a rollover after 10 seconds.

The conversion from time $t$ in seconds to timestamp is $N = round(t*100) \mod 1000$. To convert back to seconds, use $t = N/100 + 10R$ where $R$ is the rollover counter. See code below for example implementation in Python.

See [Resources](#resources) for more information about timestamps.

### Incremental decoding

There are cases where we want to transcribe a new audio segment along with previous segments that we've already transcribed. This can be useful for providing longer context for the model in order to improve transcription accuracy or to maintain the speaker numbering in SAA mode. To avoid re-decoding the previous segments, we can provide the previous transcription in the `prefix_text` field of the conversation template. The model will decode the parts after that. See the code below for examples.

### Keyword list biasing (KWB)

Keyword list biasing capability is available to enhance the recognition of keywords, such as names and technical terms.
This is particularly useful in tasks where complex terms may otherwise be misrecognized.
Keyword biasing can be applied by including the keywords directly in the prompt; for example, in ASR mode: `Can you transcribe the speech into a written format? Keywords: …`

Users may provide either a single keyword or a list of keywords, which may also include terms that do not appear in the input audio, making them well suited for batch processing or recurring domain-specific use cases.

See [Resources](#resources) for more information about keyword list biasing.

## Evaluations

Our evaluations showed that this model works well with audio segments up to 9 minutes long for ASR and SAA, and up to 3.5 minutes for timestamps.

### ASR

**Performance on** [**HuggingFace Open ASR leaderboard**](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)**:**

| **model**                                  | **Average WER** | **AMI** | **Earnings22** | **Gigaspeech** | **LS Clean** | **LS Other** | **SPGISpeech** | **Tedlium** | **Voxpopuli** |
| :----------------------------------------- | :-------------: | :-----: | :------------: | :------------: | :----------: | :----------: | :------------: | :---------: | :-----------: |
| **ibm-granite/granite-speech-4.1-2b-plus v2604**|      5.71       |  8.63   |      8.68      |     10.38      |     1.44     |     3.06     |      3.72      |    3.89     |      5.9      |
| ibm-granite/granite-speech-4.1-2b          |      5.33       |  8.09   |      8.37      |      9.8       |     1.33     |     2.5      |      3.78      |    3.07     |      5.7      |
| ibm-granite/granite-speech-4.1-2b-nar      |      5.44       |  8.03   |      8.44      |     10.16      |     1.28     |     2.77     |      3.33      |    3.62     |     5.86      |


(Using [speculative decoding](https://github.com/huggingface/open_asr_leaderboard/blob/main/granite/run_eval_speculative.py))

**Performance on the updated Open ASR leaderboard test sets:**

The leaderboard has since changed its test sets: AMI, Earnings22, Gigaspeech and Voxpopuli were replaced by cleaned versions, Tedlium was removed, and URGENT2024 and Voice Arena Monsoon (en_IN) were added. The results above are therefore not comparable with the current leaderboard, so we compare the two model versions on the new sets here (WER %, ↓ lower is better):

| **model**     | **Average WER** | **AMI**  | **Earnings22** | **Gigaspeech** | **LS Clean** | **LS Other** | **SPGISpeech** | **URGENT2024** | **Monsoon (en_IN)** | **Voxpopuli** |
| :------------ | :-------------: | :------: | :------------: | :------------: | :----------: | :----------: | :------------: | :------------: | :-----------------: | :-----------: |
| GSP v2604     |    **6.01**     | **7.88** |      8.03      |      9.02      |     1.21     |     2.75     |    **3.48**    |   **12.27**    |        5.22         |   **4.23**    |
| **GSP v2610** |      6.10       |   9.04   |    **7.43**    |    **8.70**    |   **1.09**   |   **2.69**   |      3.65      |     12.74      |      **4.88**       |     4.71      |

(Using beam search with `num_beams=4` and `repetition_penalty=2.0`, without speculative decoding)

**Keyword list biasing accuracy - Keyword F1 score (%, ↑ higher is better):**


| Mode                    | Gigaspeech | LS Clean     | LS Other     | SPGISpeech | Voxpopuli      | TED_LIUM |  CV-en    | CV-de    | CV-es    | CV-fr    | CV-pt    |
| -----------             | ---------- | -------- | -------- | ---------- | -------- | ---------- | -------- | -------- | -------- | -------- | -------- |
| GSP v2604 without KWB   | 73.3       | 89.0     | 77.6     | 79.5       | 93.9     | 87.7     |  72.8     | 76.1     | 80.9     | 72.6     | 89.5 |
| GSP v2610 without KWB   | 74.1       | 89.6     | 77.2     | 79.9       | 94.1     | 88.7     |  72.7     | 76.9     | 81.6     | 73.1     | 90.8 |
| GSP v2604 with KWB      | 81.4       | 96.2     | 92.5     | 91.1       | **95.2** | 92.5     |  **85.5** | 94.1     | 94.6     | 91.7     | 94.7 |
| **GSP v2610 with KWB**  | **84.4**   | **98.4** | **97.4** | **92.2**   | 95.0     | **94.3** |  82.4     | **95.5** | **96.1** | **95.3** | **97.0** |

### Speaker Attributed ASR

**Speaker Attributed ASR performance - WDER (%, ↓ lower is better):**

| **Model**                      | **FISHER** | **CALLHOME English** | **AMI-SDM** | **GALE** |
| :----------------------------- | :--------: | :------------------: | :---------: | :------: |
| VibeVoice ASR [1]              |    2.8     |         7.1          |    27.4     |   44.8   |
| GSP v2604                      |  **0.9**   |       **2.2**        |    14.6     |   30.2   |
| **GSP v2610**                  |    1.0     |         3.0          |  **13.9**   | **28.3** |

The results are averaged over 2-5 minute speech segments.

(The evaluation metric: Word Diarization Error Rate [WDER] is the percentage of words attributed to the wrong speaker)

### Timestamps

**Word-level timestamp accuracy - AAS (ms, ↓ lower is better):**

| **Model**                      | **AMI-I** | **AMI-S** | **LS-C** | **LS-O** | **VOX**  |  **CV**  | **MLS**  | **TMT**  | **En Avg** | **MLS-fr** | **MLS-es** | **MLS-de** | **MLS-pt** | **CV-fr** | **CV-es** | **CV-de** | **CV-pt** | **ML Avg** |
| :----------------------------- | :-------: | :-------: | :------: | :------: | :------: | :------: | :------: | :------: | :--------: | :--------: | :--------: | :--------: | :--------: | :-------: | :-------: | :-------: | :-------: | :--------: |
| Qwen3-FA [2]                   |   48.1    |   82.5    |   27.8   |   29.3   | **41.0** |   48.4   |   34.3   |   29.9   |    42.7    |    38.1    |    27.0    |  **31.2**  |  **26.3**  |   30.3    |   40.0    |   29.4    |   34.2    |    33.3    |
| CrisperWhisper [3]             |   55.7    | **64.3**  |   35.9   |   40.1   |   47.2   |   97.4   |   46.4   |   42.7   |    53.7    |  **35.6**  |    28.0    |  **31.2**  |    36.8    |   62.9    |   58.9    |   60.9    |   83.8    |    50.1    |
| Canary-v2 [4]                  |   127.8   |   129.7   |   92.5   |   89.2   |  109.9   |  110.3   |   94.3   |   86.1   |   105.0    |    85.0    |    81.1    |    80.2    |     –      |   86.8    |   88.5    |   91.5    |     –     |     –      |
| WhisperX [5]                   |   107.1   |   150.2   |   71.7   |   72.0   |   78.8   |   91.2   |   79.2   |   63.6   |    89.2    |   117.3    |    84.7    |   132.2    |    75.0    |   104.2   |   88.1    |   126.8   |   79.5    |   101.0    |
| GSP v2604                      |   43.4    |   69.0    |   11.4   |   14.6   |   80.2   |   43.3   |   24.3   |   24.5   |    38.8    |    45.4    |    23.0    |    41.3    |    47.1    |   18.6    |   19.3    |   19.5    |   24.2    |    29.8    |
| **GSP v2610**                  | **39.2**  |   69.0    | **10.1** | **13.4** |   66.5   | **35.4** | **22.5** | **20.7** |  **34.6**  |    42.5    |  **18.8**  |    38.0    |    40.6    | **16.2**  | **16.6**  | **17.3**  | **22.0**  |  **26.5**  |

(The evaluation metric: Accumulated Average Shift [AAS] is measuring the average time shift of each word)

**Word-level timestamps on long segments - AAS per test set, v2604 vs. v2610 (ms, ↓ lower is better):**

The test sets were created by concatenating the short test segments into 2-5 minute samples.

| **Test set** | **GSP v2604** | **GSP v2610** |
| :----------- | :-----------: | :-----------: |
| CV-en        |     2339.4    |   **925.3**   |
| CV-fr        |     119.0     |    **71.3**   |
| CV-de        |     131.3     |    **96.1**   |
| MLS-es       |     407.9     |   **192.5**   |
| MLS-pt       |     1073.8    |   **356.2**   |
| **Average**  |     814.3     |   **328.3**   |

## Release Date

April 28, 2026. Updated October 19, 2026.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Supported Languages

English, French, German, Spanish, Portuguese

## Intended Use

The model is intended to be used in enterprise applications that involve processing of speech input especially when a rich transcript adding speaker turns and time stamps is desired. In particular, the model is well-suited for English, French, German, Spanish, and Portuguese speech-to-text.

## Usage

The Granite Speech Plus model is supported natively in `transformers>=5.8`. Below is a simple example of how to use the different modes of the model. 

### Usage with `transformers`

First [install pytorch](https://pytorch.org/get-started/locally/) and [transformers](https://huggingface.co/docs/transformers/installation).

```shell
pip install torchaudio datasets accelerate torchcodec
```

**Setup** — load the model and a test audio clip:

```python
import re
import torch
from datasets import Audio, load_dataset
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
```

Load the model and define a general function for decoding the audio:

```python
MODEL_NAME = "ibm-granite/granite-speech-4.1-2b-plus"

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained(MODEL_NAME)
tokenizer = processor.tokenizer
model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_NAME, device_map=device, dtype=torch.bfloat16)
model.eval()

SYSTEM_PROMPT = "Knowledge Cutoff Date: April 2024.\nToday's Date: December 19, 2024.\nYou are Granite, developed by IBM. You are a helpful AI assistant"
SAMPLE_RATE = 16000

@torch.inference_mode()
def transcribe(audio, prompt, tokens_per_second=12, prefix_text=None, repetition_penalty=2.0, num_beams=1):
    chat = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    extra = {"prefix_text": prefix_text} if prefix_text is not None else {}
    prompt_text = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True, **extra)
    inputs = processor(prompt_text, audio, device=device, return_tensors="pt").to(device)
    # Limit the output length relative to the audio length to stop runaway generation
    max_new_tokens = max(256, int(tokens_per_second * audio.shape[-1] / SAMPLE_RATE))
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
    )
    new_tokens = outputs[0, inputs["input_ids"].shape[-1]:]
    output_text = tokenizer.decode(new_tokens, add_special_tokens=False, skip_special_tokens=True)
    return output_text
```

`repetition_penalty=2.0` prevents the model from getting stuck in a repetition loop, which happens mostly on long audio and in the SAA and timestamp modes.
`tokens_per_second` sets the maximum output length per second of audio (at least 256 tokens); the examples below use 12 for ASR, 16 for SAA and 48 for timestamps.
The results on the updated Open ASR leaderboard test sets were obtained with `num_beams=4`; `num_beams=1` is faster.

Load some example audio data from the AMI dataset

```python
ds = load_dataset("diarizers-community/ami", "ihm", split="test")
ds = ds.cast_column("audio", Audio(sampling_rate=SAMPLE_RATE, num_channels=1))

TEST_SAMPLE = 0
START_TIME, END_TIME = 5 * 60, 6 * 60
audio = ds["audio"][TEST_SAMPLE].get_samples_played_in_range(START_TIME, END_TIME)
```

**Task 1: ASR** — plain speech-to-text transcription:

```python
ASR_PROMPT = "<|audio|> can you transcribe the speech into a written format?"

asr_text = transcribe(audio.data, ASR_PROMPT)
print(asr_text)
```

**Task 2: Speaker Attributed ASR** — transcription with speaker labels:

```python
SAA_PROMPT = "<|audio|> Speaker attribution: Transcribe and denote who is speaking by adding [Speaker 1]: and [Speaker 2]: tags before speaker turns."

saa_text = transcribe(audio.data, SAA_PROMPT, tokens_per_second=16)
for segment in re.split(r"(\[Speaker \d+\]:)", saa_text):
    print(segment.strip())
```

**Task 3: Word-level timestamps** — transcription with per-word timing:

The timestamps are given in centiseconds and are modulo 1000 (=10 seconds)
so we need to unwrap them by adding multiples of 10 seconds.

```python
TS_PROMPT = "<|audio|> Timestamps: Transcribe the speech. After each word, add a timestamp tag showing the end time in centiseconds, e.g. hello [T:45] world [T:82]"

ts_text = transcribe(audio.data, TS_PROMPT, tokens_per_second=48)
ts_words = re.split(r"\[T:(\d+)\]", ts_text)
last_word_end_time = 0
offset_time = 0
for word, ts in zip(ts_words[::2], ts_words[1::2]):
    word_end_time = float(ts) / 100
    while word_end_time + offset_time < last_word_end_time:
        offset_time += 10
    last_word_end_time = word_end_time + offset_time
    print(f"{word}\t{last_word_end_time:.2f}s")
```

**Task 4: Incremental decoding** — transcribe segments while accumulating audio context:

```python
NUM_SEGMENTS = 3
previous_transcript = ""
all_audio = None

for k in range(NUM_SEGMENTS):
    t1 = START_TIME + (END_TIME - START_TIME) * k / NUM_SEGMENTS
    t2 = START_TIME + (END_TIME - START_TIME) * (k + 1) / NUM_SEGMENTS
    new_audio = ds["audio"][TEST_SAMPLE].get_samples_played_in_range(t1, t2)
    all_audio = new_audio.data if all_audio is None else torch.cat([all_audio, new_audio.data], dim=-1)
    saa_text = transcribe(all_audio, SAA_PROMPT, tokens_per_second=16, prefix_text=previous_transcript)
    print(f"{t1:06.2f}-{t2:06.2f}:\t{saa_text}")
    previous_transcript = (previous_transcript + " " + saa_text).strip()
```

### Usage with `vLLM`

For vLLM usage follow the instructions for the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b#usage-with-vllm). The Granite-Speech-Plus model requires vLLM [v0.23.0](https://github.com/vllm-project/vllm/releases/tag/v0.23.0) or later.

## Model Architecture

The model shares the same architecture as the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) model.

## Training Data

The model was trained on the same datasets as [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b).

Additional training data for SAA was created using audio segments from datasets that have speaker identification (e.g. Multilingual-Librispeech). Segments with alternating speakers were concatenated to create a long multi-speaker sample.


### Training Data for Timestamps

Word-level timestamping capabilities are achieved by using a combination of publicly available speech corpora: LibriSpeech, MLS (en, fr, de, pt, es), CommonVoice (en, fr, de, pt, es), VoxPopuli (en, fr, de, es), AMI-IHM, Switchboard, TIMIT and YODAS. For AMI-IHM, Switchboard and TIMIT, we use the available timestamp annotations. For all other datasets, we obtain word-level alignments using the Montreal Forced Aligner (MFA), a GMM-HMM based forced alignment tool. We also use MFA to insert silence boundaries into the manually annotated datasets.

To ensure high-quality training data, we validate the MFA-derived alignments using forced alignments with our CTC-based speech encoder. We compute the Accumulated Average Shift (AAS), the mean absolute error between timestamps in milliseconds, for the CTC and MFA alignments and retain only samples with the lowest alignment error: the top 95% for English and top 70% for non-English data. For the larger datasets (YODAS and MLS-en), we cap the training data at 4M and 5M samples, respectively.

Additional training data containing long audio samples with timestamps were generated by concatenation of short segments.

The model was trained on audio samples up to 10 minutes for ASR and SAA, and up to 5 minutes for timestamps.

## Infrastructure

We train Granite Speech using IBM's supercomputing cluster, Blue Vela, which is outfitted with NVIDIA H100 GPUs. This cluster provides a scalable
and efficient infrastructure for training our models over thousands of GPUs. The training of this particular model was completed in about 5 days on 32
H100 GPUs.

## Ethical Considerations and Limitations

The use of Large Speech and Language Models can trigger certain risks and ethical considerations. Although our alignment processes include safety considerations,
the model may in some cases produce inaccurate, biased, offensive or unwanted responses to user prompts. Additionally, whether smaller models may exhibit increased
susceptibility to hallucination in generation scenarios due to their reduced sizes, which could limit their ability to generate coherent and contextually accurate responses, remains uncertain.
This aspect is currently an active area of research, and we anticipate more rigorous exploration, comprehension, and mitigations in this domain.

IBM recommends using this model for automatic speech recognition, speaker annotation and word alignment. The model's design improves safety by limiting how audio inputs can influence the system.
If an unfamiliar or malformed prompt is received, the model simply ignores it and performs transcription, which is the default fallback mode.
This minimizes the risk of adversarial inputs, unlike integrated models that directly interpret audio and may be more exposed to such attacks. Note that more general speech tasks may pose higher inherent risks of triggering unwanted outputs.

To enhance safety, we recommend using Granite-Speech-4.1-2B-Plus alongside Granite Guardian. Granite Guardian is a fine-tuned instruct model designed to detect and flag risks in prompts and responses across key dimensions outlined in the IBM AI Risk Atlas.

## Resources

- 📄 Read the papers:
  - [Speaker Attributed Automatic Speech Recognition Using Speech Aware LLMS](https://arxiv.org/abs/2604.11269)
  - [In-Sync: Adaptation of Speech Aware Large Language Models for ASR with Word Level Timestamp Predictions](https://arxiv.org/abs/2604.22817)
  - [Contextual Biasing for ASR in Speech LLM with Common Word Cues and Bias Word Position Prediction](https://arxiv.org/abs/2604.12398)
  - [Granite-speech: open-source speech-aware LLMs with strong English ASR capabilities](https://arxiv.org/abs/2505.08699)
  - [Self-Speculative Decoding for LLM-based ASR with CTC Encoder Drafts](https://arxiv.org/abs/2603.11243)
  - [NLE: Non-autoregressive LLM-based ASR by Transcript Editing](https://arxiv.org/abs/2603.08397) 
- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 🚀 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources

## References

[1] VibeVoice-ASR (Transformers-compatible version). Available online: https://huggingface.co/microsoft/VibeVoice-ASR-HF.

[2] X. Shi et al., "Qwen3-ASR technical report," 2026. arXiv

[3] M. Zusag, L. Wagner, and B. Thallinger, "CrisperWhisper: Accurate timestamps on verbatim speech transcriptions," in Proc. Interspeech, 2024.

[4] M. Sekoyan, N. R. Koluguri, N. Tadevosyan, P. Zelasko, T. Bartley, N. Karpov, J. Balam, and B. Ginsburg, "Canary-1B-v2 & Parakeet-TDT-0.6B-v3: Efficient and high-performance models for multilingual ASR and AST," 2025. arXiv

[5] M. Bain, J. Huh, T. Han, and A. Zisserman, "WhisperX: Time-accurate speech transcription of long-form audio," 2023. arXiv

