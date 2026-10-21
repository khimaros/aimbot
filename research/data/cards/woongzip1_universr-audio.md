---
license: cc-by-4.0
tags:
  - audio
  - audio-super-resolution
  - speech
  - music
  - flow-matching
library_name: pytorch
---

# UniverSR - General Audio (Flagship)

Vocoder-free audio super-resolution model that upsamples **8/12/16/24 kHz → 48 kHz** audio using flow matching in the complex STFT domain. Trained on speech, music, and sound effects.

This is the **recommended model** for general use.
For speech-only evaluation (e.g. VCTK benchmark), see [universr-speech](https://huggingface.co/woongzip1/universr-speech).

**Paper**: [arXiv:2510.00771](https://arxiv.org/abs/2510.00771) | 
**Demo**: [woongzip1.github.io/universr-demo](https://woongzip1.github.io/universr-demo/) | **Code**: [github.com/woongzip1/UniverSR](https://github.com/woongzip1/UniverSR)

## Usage

```python
import torchaudio
from universr import UniverSR

model = UniverSR.from_pretrained("woongzip1/universr-audio", device="cuda")
output = model.enhance("low_res.wav", input_sr=8000)
torchaudio.save("output_48k.wav", output.cpu(), 48000)
```

## Citation

```bibtex
@inproceedings{choi2026universr,
  title     = {{UniverSR}: Unified and Versatile Audio Super-Resolution via Vocoder-Free Flow Matching},
  author    = {Choi, Woongjib and Lee, Sangmin and Lim, Hyungseob and Kang, Hong-Goo},
  booktitle = {IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP)},
  year      = {2026}
}
```