---
datasets:
- k2-fsa/OpenDialog
- amphion/Emilia-Dataset
- k2-fsa/TTS_eval_datasets
language:
- en
- zh
pipeline_tag: text-to-speech
tags:
- text-to-speech
---

# ZipVoice⚡: Fast and High-Quality Zero-Shot Text-to-Speech with Flow Matching</center>

This model consists of checkpoints for two fast and high-quality non-autoregressive zero-shot text-to-speech models:

- **ZipVoice**, for single-speaker speech generation. Details in [paper](https://arxiv.org/abs/2506.13053) and [demo](https://zipvoice.github.io).


- **ZipVoice-Dialog**, for spoken dialogue generation. Details in [paper](https://arxiv.org/abs/2507.09318) and [demo](https://zipvoice-dialog.github.io).

See our Github repository [ZipVoice](https://github.com/k2-fsa/ZipVoice) for instructions on using our models.


## 1. Explanation of each directory

| Directory                      | Model Type                | Training Data                     | Initialized from           |
| :---------------------------- | :-----------------------: | :-------------------------------: | :------------------------: |
| zipvoice                       | ZipVoice                  | Emilia                            | -                          |
| zipvoice_libritts              | ZipVoice                  | LibriTTS                          | -                          |
| zipvoice_distill               | ZipVoice-Distill          | Emilia                            | zipvoice/model.pt          |
| zipvoice_distill_libritts      | ZipVoice-Distill          | LibriTTS                          | zipvoice_libritts/model.pt |
| zipvoice_dialog                | ZipVoice-Dialog           | OpenDialog + in-house dataset     | zipvoice/model.pt          |
| zipvoice_dialog_opendialog     | ZipVoice-Dialog           | OpenDialog                        | zipvoice/model.pt          |
| zipvoice_dialog_stereo         | ZipVoice-Dialog-Stereo    | in-house dataset                  | zipvoice_dialog/model.pt   |


## 2. Discussion & Communication

You can directly discuss on [Github Issues](https://github.com/k2-fsa/ZipVoice/issues).

You can also scan the QR code to join our wechat group or follow our wechat official account.

| Wechat Group | Wechat Official Account |
| ------------ | ----------------------- |
|![wechat](https://k2-fsa.org/zh-CN/assets/pic/wechat_group.jpg) |![wechat](https://k2-fsa.org/zh-CN/assets/pic/wechat_account.jpg) |


## 3. Citation

```bibtex
@article{zhu2025zipvoice,
      title={ZipVoice: Fast and High-Quality Zero-Shot Text-to-Speech with Flow Matching},
      author={Zhu, Han and Kang, Wei and Yao, Zengwei and Guo, Liyong and Kuang, Fangjun and Li, Zhaoqing and Zhuang, Weiji and Lin, Long and Povey, Daniel},
      journal={arXiv preprint arXiv:2506.13053},
      year={2025}
}

@article{zhu2025zipvoicedialog,
      title={ZipVoice-Dialog: Non-Autoregressive Spoken Dialogue Generation with Flow Matching},
      author={Zhu, Han and Kang, Wei and Guo, Liyong and Yao, Zengwei and Kuang, Fangjun and Zhuang, Weiji and Li, Zhaoqing and Han, Zhifeng and Zhang, Dong and Zhang, Xin and Song, Xingchen and Lin, Long and Povey, Daniel},
      journal={arXiv preprint arXiv:2507.09318},
      year={2025}
}
```

## 4. License
Our code is released under the Apache 2.0 License. The pre-trained model is licensed under the CC-BY-NC due to constraints from its training data (Emilia).

