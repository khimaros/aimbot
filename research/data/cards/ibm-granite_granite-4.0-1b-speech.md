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
# Granite-4.0-1b-speech

**Model Summary:**
Granite-4.0-1b-speech is a compact and efficient speech-language model, specifically designed for multilingual automatic speech recognition (ASR) and bidirectional automatic speech translation (AST).

The model was trained on a collection of public corpora comprising of diverse datasets for ASR and AST as well as synthetic datasets tailored to support Japanese ASR, keyword-biased ASR and speech translation. 
Granite-4.0-1b-speech was trained by modality aligning [granite-4.0-1b-base](https://huggingface.co/ibm-granite/granite-4.0-1b-base) to speech on publicly available open source corpora containing audio inputs and text targets.
Compared to [granite-speech-3.3-2b](https://huggingface.co/ibm-granite/granite-speech-3.3-2b) and [granite-speech-3.3-8b](https://huggingface.co/ibm-granite/granite-speech-3.3-8b), this model has the following additional capabilities and improvements:
* Supports multilingual speech inputs in English, French, German, Spanish, Portuguese and Japanese,
* Provides higher transcription accuracy for English ASR and faster inference through better encoder training and speculative decoding,
* Has half the number of parameters of [granite-speech-3.3-2b](https://huggingface.co/ibm-granite/granite-speech-3.3-2b) for running on resource-constrained devices,
* Adds keyword list biasing capability for enhanced name and acronym recognition

**Evaluations:**

We evaluated granite-4.0-1b-speech alongside other speech-language models in the less than 8b parameter range as well as dedicated ASR and AST systems on standard benchmarks. The evaluation spanned multiple public benchmarks, with particular emphasis on English ASR tasks while also including multilingual ASR and AST for X-En and En-X translations. 
<br>
![granite-4.0-1b-speech-wer1-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/KvRYoVoAWlMm0GrcdBWkR.png)
<br>
![granite-4.0-1b-speech-wer2-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/YHX5qS7_8NlhuAA2bQ5FL.png)
<br>
![granite-4.0-1b-speech-bleu1-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/HO3bmHqWXnMisIKPMAmSw.png)
<br>
![granite-4.0-1b-speech-bleu2-crop](https://cdn-uploads.huggingface.co/production/uploads/666ec38102791b3b49f453e8/QTaXEl4PcygKiw_1zaYjO.png)
<br>

**Performance on** [**HuggingFace Open ASR leaderboard**](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)**:**
| **model**     | **Average WER** | **RTFx**   | **AMI**   | **Earnings22**   | **Gigaspeech** | **LS Clean**   | **LS Other**   | **SPGISpeech**   | **Tedlium**   | **Voxpopuli**   |
|:-------------:|:---------------:|:----------:|:---------:|:----------------:|:--------------:|:--------------:|:--------------:|:----------------:|:-------------:|:---------------:|
| ibm-granite/granite-4.0-1b-speech | 5.52    | 280.02     | 8.44      | 8.48             | 10.14          | 1.42           | 2.85           | 3.89             | 3.1           | 5.84 |

**Release Date**: March 6, 2026 

**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

**Supported Languages:**
English, French, German, Spanish, Portuguese, Japanese

**Intended Use:** 
The model is intended to be used in enterprise applications that involve processing of speech inputs. 
In particular, the model is well-suited for English, French, German, Spanish, Portuguese and Japanese speech-to-text and speech translations 
to and from English for the same languages, plus English-to-Italian and English-to-Mandarin. 

## Generation:

Granite Speech model is supported natively in `transformers>=4.52.1`. Below is a simple example of how to use the `granite-4.0-1b-speech` model.

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

model_name = "ibm-granite/granite-4.0-1b-speech"
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
user_prompt = "<|audio|>can you transcribe the speech into a written format?"
# Add "Keywords: <kw1>, <kw2> ..." at the end for keyword biasing
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

model_id = "ibm-granite/granite-4.0-1b-speech"
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
        temperature=0.2,
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

vllm serve ibm-granite/granite-4.0-1b-speech \
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

model_name = "ibm-granite/granite-4.0-1b-speech"
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
    temperature=0.2,
    max_tokens=64,
    model=model_name,
)


print(f"Audio Example - Question: {question}")
print(f"Generated text: {chat_completion_with_audio.choices[0].message.content}")
```

### Usage with `mlx-audio` for Apple Silicon M series chips

First, install a recent version of mlx-audio (0.4.1 or later):
```shell
pip install -U mlx-audio
```
* CLI:
```shell
python -m mlx_audio.stt.generate --model ibm-granite/granite-4.0-1b-speech --verbose --audio "audio.wav" --output-path "transcript"
```
* Python:
```python
from mlx_audio.stt.utils import load_model
from mlx_audio.stt.generate import generate_transcription

model = load_model("mlx-community/granite-4.0-1b-speech-8bit")
transcription = generate_transcription(
    model=model,
    audio="audio.wav",
    output_path="transcript.txt",
    format="txt",
    verbose=True,
)
print(transcription.text)
```
(other quantizations available at [mlx-community](https://huggingface.co/mlx-community))

**Model Architecture:** 

The architecture of granite-4.0-1b-speech consists of the following components:

(1) Speech encoder: 16 conformer blocks trained with Connectionist Temporal Classification (CTC) on character-level targets on the subset containing
only ASR corpora (see configuration below). The character vocabulary consists of the first 256 ASCII entries for the European languages plus a 92 phonetic Katakana character set for Japanese. In addition, our CTC encoder uses block-attention with 4-seconds audio blocks and self-conditioned CTC
from the middle layer.

| Configuration parameter  | Value                | 
|-----------------|----------------------|
| Input dimension | 160 (80 logmels x 2) | 
| Nb. of layers   | 16                   | 
| Hidden dimension | 1024                | 
| Nb. of attention heads | 8             | 
| Attention head size    | 128           | 
| Convolution kernel size | 15           | 
| Output dimension        | 348          | 

(2) Speech projector and temporal downsampler (speech-text modality adapter): we use a 2-layer window query transformer (q-former) operating on
blocks of 15 1024-dimensional acoustic embeddings coming out of the last conformer block of the speech encoder that get downsampled by a factor of 5
using 3 trainable queries per block and per layer. The total temporal downsampling factor is 10 (2x from the encoder and 5x from the projector)
resulting in a 10Hz acoustic embeddings rate for the LLM. The projector and LLM LoRA adapters were trained jointly on all the
corpora mentioned under **Training Data**.

(3) Large language model: granite-4.0-1b-base with 128k context length (https://huggingface.co/ibm-granite/granite-4.0-1b-base) finetuned on all 
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
| VoxPopuli En,De,Fr,Es       | ASR | 1100 |  https://huggingface.co/datasets/facebook/voxpopuli | 
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

To enhance safety, we recommend using granite-4.0-1b-speech alongside Granite Guardian. Granite Guardian is a fine-tuned instruct model designed to detect and flag risks in prompts and responses across key dimensions outlined in the IBM AI Risk Atlas.

**Resources**
- 📄 Read the papers: https://arxiv.org/abs/2505.08699, https://arxiv.org/abs/2603.11243
- 🔧 Notebooks: [Speculative decoding](https://colab.research.google.com/github/ibm-granite/granite-speech-models/blob/main/notebooks/speculative_decoding_notebook.ipynb), [finetune on custom data](https://colab.research.google.com/github/ibm-granite/granite-speech-models/blob/main/notebooks/fine_tuning_granite_speech.ipynb)
- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 🚀 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources

**Citation**

```bibtex
@misc{granite-4.0-1b-speech,
  title={Granite 4.0 Speech},
  author={IBM Granite Speech Team},
  year={2026},
  url={https://huggingface.co/ibm-granite/granite-4.0-1b-speech}
}
```