---
license: apache-2.0
language:
- multilingual
- en
- fr
- de
- es
- pt
- ja
base_model:
- ibm-granite/granite-4.0-1b-base
library_name: transformers
---
# Granite-Speech-4.1-2B

**Model Summary:**
Granite Speech 4.1 2B is a compact and efficient speech-language model, specifically designed for multilingual automatic speech recognition (ASR) and bidirectional automatic speech translation (AST) for English, French, German, Spanish, Portuguese and Japanese.

The model was trained on 174,000 hours of audio from public corpora for ASR and AST as well as synthetic datasets tailored to support Japanese ASR, keyword-biased ASR and speech translation. 
Granite Speech 4.1 2B was trained by modality aligning an intermediate checkpoint of [granite-4.0-1b-base](https://huggingface.co/ibm-granite/granite-4.0-1b-base) to speech on publicly available open source corpora containing audio inputs and text targets.
Compared to its predecessor [granite-4.0-1b-speech](https://huggingface.co/ibm-granite/granite-4.0-1b-speech), this model has the same parameter count (the new naming convention reflects actual instead of base LLM size) and provides additional capabilities and improvements:
* Higher transcription accuracy for multilingual ASR due to a novel dual-head CTC encoder with both graphemic and BPE outputs and frame importance sampling to focus on informative parts of the audio
* Punctuation and truecasing for ASR and AST in all languages (including German noun capitalization) with a simple prompt change
* Better keyword list biasing capability for enhanced recognition of names, acronyms and technical jargon

Two additional model variants explore different capabilities and inference optimization:
* [granite-speech-4.1-2b-plus](https://huggingface.co/ibm-granite/granite-speech-4.1-2b-plus) adds speaker-attributed ASR and word-level time stamps
* [granite-speech-4.1-2b-nar](https://huggingface.co/ibm-granite/granite-speech-4.1-2b-nar) introduces a novel non-autoregressive architecture for higher throughput

**Evaluations:**

We evaluated granite-speech-4.1-2b alongside other speech-language models in the less than 8b parameter range as well as dedicated ASR and AST systems on standard benchmarks. The evaluation spanned multiple public benchmarks, with particular emphasis on English ASR tasks while also including multilingual ASR and AST for X-En and En-X translations. 
<br>
![granite-speech-4.1-2b-wer1-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/wY8LOsUVOcb0k204YpdL7.png)
<br>
![granite-speech-4.1-2b-wer2-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/5nnbHPrni3qCNjzkHfod0.png)
<br>
![granite-speech-4.1-2b-bleu1-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/vSmku2veF23Sn0JWplD3j.png)
<br>
![granite-speech-4.1-2b-bleu2-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/AEasS_ygOZpqsDoQVL9BC.png)
<br>
Performance on the [Open ASR leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard) (as of April 2026):
![rtfx_wer](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/uLLMMTQD8CTpvJtou7do9.png)
<br>

We evaluated the model’s keyword list biasing (KWB) capability by comparing performance with and without KWB applied at inference time. 
We report the F1 scores of transcribed keywords during ASR tasks, excluding common words from the evaluation.
![kwb-f1.v2](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/nNb161Sc_DKC3TONbkbGK.jpeg)

We also evaluated our model on a variety of corpora to assess its punctuation and capitalization capabilities. We report the metrics as defined in [LibriSpeech-PC](https://arxiv.org/abs/2310.02943). PER (punctuation error rate) measures errors in the insertion, deletion, or substitution of punctuation marks (periods, commas, and question marks). Cap-F1 (capitalization F1) measures how accurately the model capitalizes relevant words in the output. Note that our Cap-F1 is computed on Levenshtein-aligned matching word pairs rather than fully matching sentences, allowing evaluation even in the presence of ASR errors.

| Test Set | PER (&darr;) | Cap-F1 (&uarr;) |
|:---------|:----:|:------:|
| LScln | 25.70 | 89.71 |
| LSoth | 22.27 | 91.26 |
| VoxPopuli | 24.86 | 95.35 |
| Earnings-22 | 22.87 | 95.19 |
| CV-EN | 9.13 | 96.75 |
| CV-DE | 3.66 | 99.50&dagger; |
| CV-ES | 11.61 | 95.68 |
| CV-FR | 11.00 | 97.25 |
| CV-PT | 7.86 | 98.51 |

&dagger; *We report a Cap-F1 of 99.5 on German, where noun capitalization is required.*

<br>

**Release Date**: April 29, 2026 

**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

**Supported Languages:**
English, French, German, Spanish, Portuguese, Japanese

**Intended Use:** 
The model is intended to be used in enterprise applications that involve processing of speech inputs. 
In particular, the model is well-suited for English, French, German, Spanish, Portuguese and Japanese speech-to-text and speech translations 
to and from English for the same languages, plus English-to-Italian and English-to-Mandarin. 

## Usage:

Granite Speech model is supported natively in `transformers>=4.52.1`. Below is a simple example of how to use the `granite-speech-4.1-2b` model.

### Usage with `transformers`

First, make sure to install a recent version of transformers:
```shell
pip install transformers torchaudio soundfile
```

Then run the code:
```python
import torch
import torchaudio
from huggingface_hub import hf_hub_download
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "ibm-granite/granite-speech-4.1-2b"
processor = AutoProcessor.from_pretrained(model_name)
tokenizer = processor.tokenizer
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_name, device_map=device, torch_dtype=torch.bfloat16
)

# Load audio
audio_path = hf_hub_download(repo_id=model_name, filename="multilingual_sample.wav")
wav, sr = torchaudio.load(audio_path, normalize=True)
assert wav.shape[0] == 1 and sr == 16000  # mono, 16kHz

# Create text prompt
user_prompt = "<|audio|>transcribe the speech with proper punctuation and capitalization."
chat = [
    {"role": "user", "content": user_prompt},
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

# Run the processor + model
model_inputs = processor(prompt, wav, device=device, return_tensors="pt").to(device)
model_outputs = model.generate(
    **model_inputs, max_new_tokens=200, do_sample=False, num_beams=1
)

# Transformers includes the input IDs in the response
num_input_tokens = model_inputs["input_ids"].shape[-1]
new_tokens = model_outputs[0, num_input_tokens:].unsqueeze(0)
output_text = tokenizer.batch_decode(
    new_tokens, add_special_tokens=False, skip_special_tokens=True
)
print(f"STT output = {output_text[0]}")
```

### Usage with `vLLM`

First, make sure to install vLLM:
```shell
pip install vllm
```
* Code for offline mode:
```python
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
from vllm.assets.audio import AudioAsset

model_id = "ibm-granite/granite-speech-4.1-2b"
tokenizer = AutoTokenizer.from_pretrained(model_id)

def get_prompt(question: str, has_audio: bool):
    """Build the input prompt to send to vLLM."""
    if has_audio:
        question = f"<|audio|>{question}"
    chat = [
        {
            "role": "user",
            "content": question
        }
    ]
    return tokenizer.apply_chat_template(chat, tokenize=False)

model = LLM(
    model=model_id,
    max_model_len=2048, # This may be needed for lower resource devices.
    limit_mm_per_prompt={"audio": 1},
)

question = "can you transcribe the speech into a written format?"
prompt_with_audio = get_prompt(
    question=question,
    has_audio=True,
)
audio = AudioAsset("mary_had_lamb").audio_and_sample_rate

inputs = {
    "prompt": prompt_with_audio,
    "multi_modal_data": {
        "audio": audio,
    }
}

outputs = model.generate(
    inputs,
    sampling_params=SamplingParams(
        temperature=0.0,
        max_tokens=64,
    ),
)
print(f"Audio Example - Question: {question}")
print(f"Generated text: {outputs[0].outputs[0].text}")
```

* Code for online mode:
```python
"""
Launch the vLLM server with the following command:

vllm serve ibm-granite/granite-speech-4.1-2b \
    --api-key token-abc123 \
    --max-model-len 2048
"""

import base64

import requests
from openai import OpenAI

from vllm.assets.audio import AudioAsset

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model_name = "ibm-granite/granite-speech-4.1-2b"
# Any format supported by librosa is supported
audio_url = AudioAsset("mary_had_lamb").url

# Use base64 encoded audio in the payload
def encode_audio_base64_from_url(audio_url: str) -> str:
    """Encode an audio retrieved from a remote url to base64 format."""
    with requests.get(audio_url) as response:
        response.raise_for_status()
        result = base64.b64encode(response.content).decode("utf-8")
    return result

audio_base64 = encode_audio_base64_from_url(audio_url=audio_url)

question = "can you transcribe the speech into a written format?"
chat_completion_with_audio = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": question
            },
            {
                "type": "audio_url",
                "audio_url": {
                    # Any format supported by librosa is supported
                    "url": f"data:audio/ogg;base64,{audio_base64}"
                },
            },
        ],
    }],
    temperature=0.0,
    max_tokens=64,
    model=model_name,
)


print(f"Audio Example - Question: {question}")
print(f"Generated text: {chat_completion_with_audio.choices[0].message.content}")
```
### Usage with `llama.cpp`

Installation instructions for macOS using `homebrew`:
```shell
brew install llama.cpp
```
* Offline mode:
```shell
llama-cli -st -hf ibm-granite/granite-speech-4.1-2b-GGUF:Q8_0 --audio "audio.wav" -p "transcribe the speech with proper punctuation and capitalization."
```
* Online mode:
```shell
llama-server -hf ibm-granite/granite-speech-4.1-2b-GGUF:Q8_0 --port 9797
```
Then launch a request with:
```shell
curl http://localhost:9797/v1/audio/transcriptions -F "model=ibm-granite/granite-speech-4.1-2b-GGUF:Q8_0" -F "file=audio.wav" -F "prompt=transcribe the speech with proper punctuation and capitalization." | jq -r .text
```

### Usage with `mlx-audio` for Apple Silicon M series chips

Install a recent version of mlx-audio (0.4.1 or later):
```shell
pip install -U mlx-audio
```
Sample use:
```shell
python -m mlx_audio.stt.generate --model ibm-granite/granite-speech-4.1-2b --verbose --audio "audio.wav" --output-path "transcript"
```

**Preferred prompt by task:**
| Task | Prompt | Notes |
|---------|----|------|
| ASR (raw transcripts)  | ```can you transcribe the speech into a written format?``` | Multilingual prompts supported e.g. ```Pouvez‑vous reconnaître le contenu de la parole ?```|
| ASR (with punctuation) | ```transcribe the speech with proper punctuation and capitalization.``` | Non-English ASR requires English prompt |
| ASR (with keyword biasing) | ```transcribe the speech to text. Keywords: <kw1>, <kw2>, ...``` | Non-English ASR requires English prompt | 
| AST (raw transcripts)  | ```translate the speech to <language>.``` | ```<language>```= English, French, German, Spanish, Japanese, Italian, Mandarin |
| AST (with punctuation) | ```translate the speech to <language> with proper punctuation and capitalization.``` | Only English prompt supported | 
| AST (with keyword biasing) | ```translate the speech to <language>. Keywords: <kw1>, <kw2>, ...``` | Only English prompt supported | 

**Model Architecture:** 

The architecture of granite-speech-4.1-2b consists of the following components:

(1) Speech encoder: 16 conformer blocks trained with Connectionist Temporal Classification (CTC) with two classification heads (characters and BPE units) on the subset containing
only ASR corpora (see configuration below). The character vocabulary consists of the first 256 ASCII entries for the European languages plus a 92 phonetic Katakana character set for Japanese whereas the BPE units come from the granite 4.0 tokenizer.
In addition, our CTC encoder uses block-attention with 4-seconds audio blocks and self-conditioned CTC from the middle layer. 
The middle layer also provides non-blank probabilities that are used for frame-level posterior-weighted pooling with a window size of 4 for BPE classification.

| Configuration parameter  | Value                | 
|-----------------|----------------------|
| Input dimension | 160 (80 logmels x 2) | 
| Nb. of layers   | 16                   | 
| Hidden dimension | 1024                | 
| Nb. of attention heads | 8             | 
| Attention head size    | 128           | 
| Convolution kernel size | 15           | 
| Output dimension (characters)       | 348          | 
| Output dimension (BPE) | 100353  |

(2) Speech projector and temporal downsampler (speech-text modality adapter): we use a 2-layer window query transformer (q-former) operating on
blocks of 15 1024-dimensional acoustic embeddings coming out of the last conformer block of the speech encoder that get downsampled by a factor of 5
using 3 trainable queries per block and per layer. The total temporal downsampling factor is 10 (2x from the encoder and 5x from the projector)
resulting in a 10Hz acoustic embeddings rate for the LLM. The projector and LLM LoRA adapters were trained jointly on all the
corpora mentioned under **Training Data**.

(3) Large language model: intermediate checkpoint of granite-4.0-1b-base with 128k context length (https://huggingface.co/ibm-granite/granite-4.0-1b-base) finetuned on all 
the corpora mentioned under **Training Data**.

**Training Data:** 

Overall, our training data is largely comprised of two key sources: (1) publicly available datasets (2) Synthetic data created from publicly
available datasets specifically targeting Japanese ASR, keyword list-prompted ASR and the speech translation task. 
A detailed description of the training datasets can be found in the table below:

| Name | Task | Nb. hours | Source |
|-----------|--------------|----------------|--------------|
| CommonVoice-17 En,De,Es,Fr,Pt,Ja  | ASR | 5700 |   https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0 |
| MLS En,De,Es,Fr,Pt             | ASR | 48000 |   https://huggingface.co/datasets/facebook/multilingual_librispeech |
| Librispeech English            | ASR | 1000 |  https://huggingface.co/datasets/openslr/librispeech_asr | 
| Librispeech-PC English     | ASR | 1000 | https://huggingface.co/datasets/yoom618/librispeech_pc |
| LibriHeavy Large English    | ASR | 46000 | https://huggingface.co/datasets/anyspeech/libri-heavy |
| VoxPopuli En,De,Fr,Es       | ASR | 1100 |  https://huggingface.co/datasets/facebook/voxpopuli | 
| VoxPopuli Granary English   | ASR | 24000 | https://huggingface.co/datasets/nvidia/Granary |
| AMI English                    | ASR | 100 | https://huggingface.co/datasets/edinburghcstr/ami | 
| YODAS English           | ASR | 10000 |  https://huggingface.co/datasets/espnet/yodas |
| YODAS Japanese           | ASR | 1400 |  https://huggingface.co/datasets/espnet/yodas |
| Earnings-22 English            | ASR | 105 | https://huggingface.co/datasets/esb/datasets | 
| Switchboard English     | ASR | 260 | https://catalog.ldc.upenn.edu/LDC97S62 |
| CallHome English        | ASR | 18  | https://catalog.ldc.upenn.edu/LDC97T14 | 
| Fisher English                 | ASR | 2000 | https://catalog.ldc.upenn.edu/LDC2004S13 | 
| Voicemail part I English       | ASR | 40 | https://catalog.ldc.upenn.edu/LDC98S77 | 
| Voicemail part II English      | ASR | 40 | https://catalog.ldc.upenn.edu/LDC2002S35 |
| ReazonSpeech | ASR | 3000 | https://huggingface.co/datasets/reazon-research/reazonspeech |
| Fineweb-2 TTS Japanese | ASR | 9600 | https://huggingface.co/datasets/HuggingFaceFW/fineweb-2 and Kokoro-82M TTS |
| CommonVoice-17 De,Es,Fr,Pt->En          | AST | 3000  | Translations with Granite-3 and Phi-4 | 
| CommonVoice-17 En->De,Es,Fr,It,Ja,Pt,Zh | AST | 18000 | Translations with Phi-4 and MADLAD |

**Infrastructure:**
We train Granite Speech using IBM's super computing cluster, Blue Vela, which is outfitted with NVIDIA H100 GPUs. This cluster provides a scalable
and efficient infrastructure for training our models over thousands of GPUs. The training of this particular model was completed in 30 days (26 encoder + 4 projector) on 8
H100 GPUs.

**Ethical Considerations and Limitations:**

The use of Large Speech and Language Models can trigger certain risks and ethical considerations. Although our alignment processes include safety considerations, 
the model may in some cases produce inaccurate, biased, offensive or unwanted responses to user prompts. Additionally, whether smaller models may exhibit increased 
susceptibility to hallucination in generation scenarios due to their reduced sizes, which could limit their ability to generate coherent and contextually accurate responses, remains uncertain.
 This aspect is currently an active area of research, and we anticipate more rigorous exploration, comprehension, and mitigations in this domain.

IBM recommends using this model for automatic speech recognition and translation tasks. The model's design improves safety by limiting how audio inputs can influence the system. 
If an unfamiliar or malformed prompt is received, the model simply ignores it and performs transcription which is the default fallback mode. 
This minimizes the risk of adversarial inputs, unlike integrated models that directly interpret audio and may be more exposed to such attacks. Note that more general speech tasks may pose higher inherent risks of triggering unwanted outputs. 

To enhance safety, we recommend using granite-speech-4.1-2b alongside Granite Guardian. Granite Guardian is a fine-tuned instruct model designed to detect and flag risks in prompts and responses across key dimensions outlined in the IBM AI Risk Atlas.

**Resources**
- 📄 Read our papers: 
    - [Granite-speech: open-source speech-aware LLMs with strong English ASR capabilities](https://arxiv.org/abs/2505.08699)
    - [Self-Speculative Decoding for LLM-based ASR with CTC Encoder Drafts](https://arxiv.org/abs/2603.11243)
    - [Contextual Biasing for ASR in Speech LLM with Common Word Cues and Bias Word Position Prediction](https://arxiv.org/abs/2604.12398)
    - [In-Sync: Adaptation of Speech Aware Large Language Models for ASR with Word Level Timestamp Predictions](https://arxiv.org/abs/2604.22817)
    - [Speaker Attributed Automatic Speech Recognition Using Speech Aware LLMS](https://arxiv.org/abs/2604.11269)
    - [NLE: Non-autoregressive LLM-based ASR by Transcript Editing](https://arxiv.org/abs/2603.08397) 
- 🔧 Notebooks: [Speculative decoding](https://colab.research.google.com/github/ibm-granite/granite-speech-models/blob/main/notebooks/speculative_decoding_bpe.ipynb), [finetune on custom data](https://colab.research.google.com/github/ibm-granite/granite-speech-models/blob/main/notebooks/fine_tuning_granite_speech.ipynb)
- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 🚀 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources

**Citation**

```bibtex
@misc{granite-speech-4.1-2b,
  title={Granite 4.1 Speech},
  author={IBM Granite Speech Team},
  year={2026},
  url={https://huggingface.co/ibm-granite/granite-speech-4.1-2b}
}
```
