---
datasets:
- espnet/yodas_owsmv4
language: multilingual
license: cc-by-4.0
tags:
- espnet
- audio
- automatic-speech-recognition
- speech-translation
- language-identification
library_name: espnet
pipeline_tag: automatic-speech-recognition
---

## Usage

```python
import librosa
from espnet2.bin.s2t_inference import Speech2Text

s2t = Speech2Text.from_pretrained(
    model_tag="espnet/owsm_v4_medium_1B", lang_sym="<eng>", task_sym="<asr>", beam_size=5
)
# OWSM is trained on 16 kHz; each call decodes 30 s, padded or trimmed
speech, rate = librosa.load("audio.wav", sr=16000, mono=True)
text, token, token_int, text_nospecial, hyp = s2t(speech)[0]
print(text_nospecial)  # `text` keeps OWSM's own <eng><asr> markers
# for a recording longer than 30 s: s2t.decode_long(speech) -> (start, end, text)
```

🏆 **News:** Our [OWSM v4 paper](https://www.isca-archive.org/interspeech_2025/peng25c_interspeech.html) won the [Best Student Paper Award](https://isca-speech.org/ISCA-Awards) at INTERSPEECH 2025!


[Open Whisper-style Speech Model (OWSM)](https://www.wavlab.org/activities/2024/owsm/) is the first **fully open** Whisper-style speech foundation model. 
It reproduces and advances OpenAI's Whisper-style training using publicly available data and open-source toolkits. 
The code, pre-trained model weights, and training logs are publicly released to promote open science in speech foundation models.

Inference examples can be found on our [project page](https://www.wavlab.org/activities/2024/owsm/).
The Gradio demo is [here](https://huggingface.co/spaces/espnet/owsm-v4).

[OWSM v4](https://arxiv.org/abs/2506.00338) is the latest version in the OWSM series, which significantly outperforms OWSM v3.1 in LID and multilingual ASR.
Additionally, OWSM v4 applies 8 times subsampling (instead of 4 times in OWSM v3.1) to the log Mel features, leading to a final resolution of 80 ms in the encoder.
When running inference, we recommend setting `maxlenratio=1.0` (default) instead of smaller values.

This repo contains a medium-sized model with 1B parameters, developed by [Yifan Peng](https://pyf98.github.io/) (CMU). 
It is trained on 320k hours of public speech data. 
The newly curated data are publicly released: https://huggingface.co/datasets/espnet/yodas_owsmv4

It supports the following speech-to-text tasks:
- Language identification
- Speech recognition
- Speech translation
- Utterance-level timestamp prediction
- Long-form recognition or translation



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