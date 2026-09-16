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
---

# Granite-Speech-4.1-2B-Plus

## Model Summary

Granite-Speech-4.1-2B-Plus has similar capabilities to the [Granite-Speech-4.1-2B](https://huggingface.co/ibm-granite/granite-speech-4.1-2b) model. The plus model adds two new community-requested rich transcription features that can be activated with a simple prompt change: speaker-attributed ASR (speaker labels and word transcripts) and word-level timing information. Unlike the base mode, the plus model doesn't provide punctuation and capitalization.

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
| **ibm-granite/granite-speech-4.1-2b-plus** |      5.71       |  8.63   |      8.68      |     10.38      |     1.44     |     3.06     |      3.72      |    3.89     |      5.9      |
| ibm-granite/granite-speech-4.1-2b          |      5.33       |  8.09   |      8.37      |      9.8       |     1.33     |     2.5      |      3.78      |    3.07     |      5.7      |
| ibm-granite/granite-speech-4.1-2b-nar      |      5.44       |  8.03   |      8.44      |     10.16      |     1.28     |     2.77     |      3.33      |    3.62     |     5.86      |


(Using [speculative decoding](https://github.com/huggingface/open_asr_leaderboard/blob/main/granite/run_eval_speculative.py))

**Keyword list biasing accuracy - Keyword F1 score (%, ↑ higher is better):**

| Mode        | Gigaspeech | LS-C     | LS-O     | SPGISpeech | VOX      | TED_LIUM | Earnings22 | CV-en    | CV-de    | CV-es    | CV-fr    | CV-pt    |
| ----------- | ---------- | -------- | -------- | ---------- | -------- | -------- | ---------- | -------- | -------- | -------- | -------- | -------- |
| Without KWB | 74.2       | 89.1     | 78.2     | 80.8       | 93.9     | 87.9     | 68.8       | 74.6     | 78.5     | 83.1     | 74.5     | 90.0     |
| With KWB    | **84.1**   | **96.1** | **93.0** | **92.5**   | **96.3** | **94.9** | **81.5**   | **91.5** | **92.9** | **93.9** | **90.6** | **95.0** |

### Speaker Attributed ASR

**Speaker Attributed ASR performance - WDER (%, ↓ lower is better):**

| **Model**                      | **FISHER** | **CALLHOME English** | **AMI-SDM** | **GALE** |
| :----------------------------- | :--------: | :------------------: | :---------: | :------: |
| VibeVoice ASR [1]              |    2.8     |         7.1          |    27.4     |   44.8   |
| **Granite-speech-4.1-2b-plus** |  **0.9**   |       **2.2**        |  **14.6**   | **30.2** |

The results are averaged over 2-5 minute speech segments.

(The evaluation metric: Word Diarization Error Rate [WDER] is the percentage of words attributed to the wrong speaker)

### Timestamps

**Word-level timestamp accuracy - AAS (ms, ↓ lower is better):**

| **Model**                      | **AMI-I** | **AMI-S** | **LS-C** | **LS-O** | **VOX**  |  **CV**  | **MLS**  | **TMT**  | **En Avg** | **MLS-fr** | **MLS-es** | **MLS-de** | **MLS-pt** | **CV-fr** | **CV-es** | **CV-de** | **CV-pt** | **ML Avg** |
| :----------------------------- | :-------: | :-------: | :------: | :------: | :------: | :------: | :------: | :------: | :--------: | :--------: | :--------: | :--------: | :--------: | :-------: | :-------: | :-------: | :-------: | :--------: |
| Qwen3-FA [2]                   |   48.1    |   82.5    |   27.8   |   29.3   | **41.0** |   48.4   |   34.3   |   29.9   |    42.7    |  **38.1**  |    27.0    |  **31.2**  |  **26.3**  |   30.3    |   40.0    |   29.4    |   34.2    |    33.3    |
| CrisperWhisper [3]             |   55.7    | **64.3**  |   35.9   |   40.1   |   47.2   |   97.4   |   46.4   |   42.7   |    53.7    |    35.6    |    28.0    |  **31.2**  |    36.8    |   62.9    |   58.9    |   60.9    |   83.8    |    50.1    |
| Canary-v2 [4]                  |   127.8   |   129.7   |   92.5   |   89.2   |  109.9   |  110.3   |   94.3   |   86.1   |   105.0    |    85.0    |    81.1    |    80.2    |     –      |   86.8    |   88.5    |   91.5    |     –     |     –      |
| WhisperX [5]                   |   107.1   |   150.2   |   71.7   |   72.0   |   78.8   |   91.2   |   79.2   |   63.6   |    89.2    |   117.3    |    84.7    |   132.2    |    75.0    |   104.2   |   88.1    |   126.8   |   79.5    |   101.0    |
| **Granite-speech-4.1-2b-plus** | **43.4**  |   69.0    | **11.4** | **14.6** |   80.2   | **43.3** | **24.3** | **24.5** |  **38.8**  |    45.4    |  **23.0**  |    41.3    |    47.1    | **18.6**  | **19.3**  | **19.5**  | **24.2**  |  **29.8**  |

(The evaluation metric:  Accumulated Averaging Shift [AAS] is measuring the average time shift of each word)

## Release Date

April 28, 2026

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Supported Languages

English, French, German, Spanish, Portuguese

## Intended Use

The model is intended to be used in enterprise applications that involve processing of speech input especially when a rich transcript adding speaker turns and time stamps is desired. In particular, the model is well-suited for English, French, German, Spanish, and Portuguese speech-to-text.

## Usage

The Granite Speech model is supported natively in `transformers>=5.8`. Below is a simple example of how to use the different modes of the model. 

### Usage with `transformers`

First [install pytorch](https://pytorch.org/get-started/locally/).

Install [transformers](https://huggingface.co/docs/transformers/installation). The code for the granite-speech-plus model was added recently so you might need to install from the sources until the PyPI package is updated.

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

@torch.inference_mode()
def transcribe(audio, prompt, max_new_tokens=2000, prefix_text=None):
    chat = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    extra = {"prefix_text": prefix_text} if prefix_text is not None else {}
    prompt_text = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True, **extra)
    inputs = processor(prompt_text, audio, device=device, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, num_beams=1)
    new_tokens = outputs[0, inputs["input_ids"].shape[-1]:]
    output_text = tokenizer.decode(new_tokens, add_special_tokens=False, skip_special_tokens=True)
    return output_text
```

Load some example audio data from the AMI dataset

```python
SAMPLE_RATE = 16000

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

saa_text = transcribe(audio.data, SAA_PROMPT)
for segment in re.split(r"(\[Speaker \d+\]:)", saa_text):
    print(segment.strip())
```

**Task 3: Word-level timestamps** — transcription with per-word timing:

The timestamps are given in centiseconds and are modulo 1000 (=10 seconds)
so we need to unwrap them by adding multiples of 10 seconds.

```python
TS_PROMPT = "<|audio|> Timestamps: Transcribe the speech. After each word, add a timestamp tag showing the end time in centiseconds, e.g. hello [T:45] world [T:82]"

ts_text = transcribe(audio.data, TS_PROMPT, max_new_tokens=10000)
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
    saa_text = transcribe(all_audio, SAA_PROMPT, prefix_text=previous_transcript)
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

IBM recommends using this model for automatic speech recognition and translation tasks. The model's design improves safety by limiting how audio inputs can influence the system.
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

