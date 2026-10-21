---
datasets:
- espnet/yodas_owsmv4
language: multilingual
library_name: espnet
license: cc-by-4.0
metrics:
- cer
- bleu
- accuracy
tags:
- espnet
- audio
- automatic-speech-recognition
- speech-translation
- language-identification
pipeline_tag: automatic-speech-recognition
---

🏆 **News:** Our [OWSM v4 paper](https://www.isca-archive.org/interspeech_2025/peng25c_interspeech.html) won the [Best Student Paper Award](https://isca-speech.org/ISCA-Awards) at INTERSPEECH 2025!

[Open Whisper-style Speech Model (OWSM)](https://www.wavlab.org/activities/2024/owsm/) is the first **fully open** Whisper-style speech foundation model. 
It reproduces and advances OpenAI's Whisper-style training using publicly available data and open-source toolkits. 
The code, pre-trained model weights, and training logs are publicly released to promote open science in speech foundation models.

[OWSM-CTC](https://aclanthology.org/2024.acl-long.549/) (Peng et al., ACL 2024) is a novel encoder-only speech foundation model based on hierarchical multi-task self-conditioned CTC.
It supports multilingual speech recognition, speech translation, and language identification within a single non-autoregressive model.

[OWSM-CTC v4](https://www.isca-archive.org/interspeech_2025/peng25c_interspeech.html) is trained for three epochs on 320k hours of public audio data covering multilingual speech recognition, any-to-any speech translation, and language identification.
The newly curated data are publicly released: https://huggingface.co/datasets/espnet/yodas_owsmv4

The Gradio demo is [here](https://huggingface.co/spaces/espnet/owsm-ctc-v4). The encoder-decoder [OWSM v4](https://huggingface.co/spaces/espnet/owsm-v4) has its own, offering the same tasks, so the two models can be compared on the same audio.

To use the pre-trained model, please install `espnet` and `espnet_model_zoo`. The requirements are:
```
librosa
torch
espnet
espnet_model_zoo
```

**The recipe can be found in ESPnet:** https://github.com/espnet/espnet/tree/master/egs2/owsm_ctc_v4/s2t1

### Example script for batched inference

`Speech2Text.decode_long` decodes one recording of any length with CTC best-path decoding. Audio shorter than 30s is padded to 30s; anything longer is split into overlapping buffers. It returns `(start_time, end_time, text)` per segment, and a CTC-only model such as this one has no timestamps, so it returns a single entry covering the recording.

```python
from espnet2.bin.s2t_inference import Speech2Text

s2t = Speech2Text.from_pretrained(
    "espnet/owsm_ctc_v4_1B",
    device="cuda",
    use_flash_attn=False,   # set to True for better efficiency if flash attn is installed and dtype is float16 or bfloat16
    lang_sym='<eng>',
    task_sym='<asr>',
)

segments = s2t.decode_long(
    "audio.wav",    # a single audio (path or 1-D array/tensor) as input
    batch_size=16,
    context_len_in_secs=4,
)
text = " ".join(segment for _, _, segment in segments)

# For several recordings, call it once per recording:
texts = [
    " ".join(t for _, _, t in s2t.decode_long(path, batch_size=16))
    for path in ["audio1.wav", "audio2.wav", "audio3.wav"]
]
```

### Example script for short-form ASR/ST/LID

Our models are trained on 16kHz audio with a fixed duration of 30s. When using the pre-trained model, please ensure the input speech is 16kHz and pad or truncate it to 30s.

```python
import librosa
from espnet2.bin.s2t_inference import Speech2Text

s2t = Speech2Text.from_pretrained(
    "espnet/owsm_ctc_v4_1B",
    device="cuda",
    generate_interctc_outputs=False,
    lang_sym='<eng>',
    task_sym='<asr>',
)

# NOTE: OWSM-CTC is trained on 16kHz audio with a fixed 30s duration. Please ensure your input has the correct sample rate; otherwise resample it to 16k before feeding it to the model
speech, rate = librosa.load("xxx.wav", sr=16000)
speech = librosa.util.fix_length(speech, size=(16000 * 30))

# best_path is CTC best-path (greedy) decoding: one encoder pass, no search.
# Calling s2t(speech) instead runs a CTC prefix beam search, which is far
# slower and takes beam_size, lm_weight and the rest.
res = s2t.best_path(speech)[0]
print(res)
```

### Example script for long-form ASR/ST

```python
import soundfile as sf
import torch
from espnet2.bin.s2t_inference import Speech2Text

context_len_in_secs = 4   # left and right context when doing buffered inference
batch_size = 32   # depends on the GPU memory
s2t = Speech2Text.from_pretrained(
    "espnet/owsm_ctc_v4_1B",
    device='cuda' if torch.cuda.is_available() else 'cpu',
    generate_interctc_outputs=False,
    lang_sym='<eng>',
    task_sym='<asr>',
)

speech, rate = sf.read(
    "xxx.wav"
)

segments = s2t.decode_long(
    speech,
    batch_size=batch_size,
    context_len_in_secs=context_len_in_secs,
)
print(" ".join(text for _, _, text in segments))
```

### Example of CTC forced alignment using `ctc-segmentation`

CTC segmentation can be efficiently applied to audio of an arbitrary length.

```python
import soundfile as sf
from espnet2.bin.s2t_ctc_align import CTCSegmentation
from espnet_model_zoo.downloader import ModelDownloader

# Download model first
d = ModelDownloader()
downloaded = d.download_and_unpack("espnet/owsm_ctc_v4_1B")

aligner = CTCSegmentation(
    **downloaded,
    fs=16000,
    ngpu=1,
    batch_size=32,    # batched parallel decoding; reduce it if your GPU memory is smaller
    kaldi_style_text=True,
    time_stamps="auto",     # "auto" can be more accurate than "fixed" when converting token index to timestamp
    lang_sym="<eng>",
    task_sym="<asr>",
    context_len_in_secs=2,  # left and right context in buffered decoding
)

speech, rate = sf.read(
    "./test_utils/ctc_align_test.wav"
)
print(f"speech duration: {len(speech) / rate : .2f} seconds")
text = """
utt1 THE SALE OF THE HOTELS
utt2 IS PART OF HOLIDAY'S STRATEGY
utt3 TO SELL OFF ASSETS
utt4 AND CONCENTRATE ON PROPERTY MANAGEMENT
"""

segments = aligner(speech, text)
print(segments)
```

### OWSM series

#### Encoder-decoder OWSM

| Name | Size | Hugging Face Repo |
| :--- | ---: | :---------------- |
| OWSM v3.1 base | 101M | https://huggingface.co/espnet/owsm_v3.1_ebf_base |
| OWSM v3.1 small | 367M | https://huggingface.co/espnet/owsm_v3.1_ebf_small |
| OWSM v3.1 medium | 1.02B | https://huggingface.co/espnet/owsm_v3.1_ebf |
| OWSM v3.2 small | 367M | https://huggingface.co/espnet/owsm_v3.2 |
| OWSM v4 base | 102M | https://huggingface.co/espnet/owsm_v4_base_102M |
| OWSM v4 small | 370M | https://huggingface.co/espnet/owsm_v4_small_370M |
| OWSM v4 medium | 1.02B | https://huggingface.co/espnet/owsm_v4_medium_1B |

#### CTC-based OWSM

| Name | Size | Hugging Face Repo |
| :--- | ---: | :---------------- |
| OWSM-CTC v3.1 medium | 1.01B | https://huggingface.co/espnet/owsm_ctc_v3.1_1B |
| OWSM-CTC v3.2 medium | 1.01B | https://huggingface.co/espnet/owsm_ctc_v3.2_ft_1B |
| OWSM-CTC v4 medium | 1.01B | https://huggingface.co/espnet/owsm_ctc_v4_1B |

### Citations

#### OWSM v4

```BibTex
@inproceedings{owsm-v4,
  title={{OWSM} v4: Improving Open Whisper-Style Speech Models via Data Scaling and Cleaning},
  author={Yifan Peng and Shakeel Muhammad and Yui Sudo and William Chen and Jinchuan Tian and Chyi-Jiunn Lin and Shinji Watanabe},
  booktitle={Proceedings of the Annual Conference of the International Speech Communication Association (INTERSPEECH)},
  year={2025},
}
```

#### OWSM-CTC

```BibTex
@inproceedings{owsm-ctc,
    title = "{OWSM}-{CTC}: An Open Encoder-Only Speech Foundation Model for Speech Recognition, Translation, and Language Identification",
    author = "Peng, Yifan  and
      Sudo, Yui  and
      Shakeel, Muhammad  and
      Watanabe, Shinji",
    booktitle = "Proceedings of the Annual Meeting of the Association for Computational Linguistics (ACL)",
    year = "2024",
    month= {8},
    url = "https://aclanthology.org/2024.acl-long.549",
}
```

#### OWSM v3.1 and v3.2

```BibTex
@inproceedings{owsm-v32,
  title={On the Effects of Heterogeneous Data Sources on Speech-to-Text Foundation Models},
  author={Jinchuan Tian and Yifan Peng and William Chen and Kwanghee Choi and Karen Livescu and Shinji Watanabe},
  booktitle={Proceedings of the Annual Conference of the International Speech Communication Association (INTERSPEECH)},
  year={2024},
  month={9},
  pdf="https://arxiv.org/pdf/2406.09282"
}
@inproceedings{owsm-v31,
  title={{OWSM v3.1: Better and Faster Open Whisper-Style Speech Models based on E-Branchformer}},
  author={Yifan Peng and Jinchuan Tian and William Chen and Siddhant Arora and Brian Yan and Yui Sudo and Muhammad Shakeel and Kwanghee Choi and Jiatong Shi and Xuankai Chang and Jee-weon Jung and Shinji Watanabe},
  booktitle={Proceedings of the Annual Conference of the International Speech Communication Association (INTERSPEECH)},
  year={2024},
  month={9},
  pdf="https://arxiv.org/pdf/2401.16658",
}
```

#### Initial OWSM (v1, v2, v3)

```BibTex
@inproceedings{owsm,
  title={Reproducing Whisper-Style Training Using An Open-Source Toolkit And Publicly Available Data},
  author={Yifan Peng and Jinchuan Tian and Brian Yan and Dan Berrebbi and Xuankai Chang and Xinjian Li and Jiatong Shi and Siddhant Arora and William Chen and Roshan Sharma and Wangyou Zhang and Yui Sudo and Muhammad Shakeel and Jee-weon Jung and Soumi Maiti and Shinji Watanabe},
  booktitle={Proceedings of the IEEE Automatic Speech Recognition and Understanding Workshop (ASRU)},
  year={2023},
  month={12},
  pdf="https://arxiv.org/pdf/2309.13876",
}
```