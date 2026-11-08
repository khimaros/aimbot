---
license: other
track_downloads: true
pipeline_tag: audio-to-audio
library_name: mamba-ssm
tags:
- streaming speech-enhancement
- speech-enhancement
- universal speech enhancement
- multiple input sampling rates
- language-agnostic
---
# **<span style="color:#76b900;"> 🚀+🤫 Real-time RE-USE: Real-time Multilingual Universal Speech Enhancement</span>**
# Model Overview


## Description

<p align="center">
    <img src="./img/fig1.png" width="80%"/>
<p>

Real-time RE-USE is a unified, real-time universal speech enhancement framework that explicitly controls both **algorithmic** and **computational** latency within a single model. 
The proposed framework supports **30** distinct latency configurations while maintaining performance close to specialized models, making it easy to adapt to **different latency budgets**.


<p align="center">
    <img src="./img/fig2.png" width="80%"/>
<p>

For **Non Real-time applications**, check this model => [RE-USE](https://huggingface.co/nvidia/RE-USE)

In universal speech enhancement, the goal is to restore the **quality** of diverse degraded speech while preserving **fidelity**, ensuring that all other factors remain unchanged, e.g., linguistic content, speaker identity, emotion, accent, and other paralinguistic attributes. Inspired by the **distortion–perception trade-off theory**, our proposed single model achieves a good balance between these two objectives and has the following desirable properties:

- Robustness to **diverse degradations**, including additive noise, reverberation, clipping, bandwidth limitation, codec artifacts, packet loss and low-quality mics .
- Support for **multiple input sampling rates**, including 8, 16, 22.05, 24, 32, 44.1, and 48 kHz.
- Strong **language-agnostic** capability, enabling effective performance across different languages.

This model is for research and development only.

## Usage
Directly try our [**Gradio Interactive Demo**](https://huggingface.co/spaces/nvidia/Real-time_RE-USE) by uploading your noisy audio/video !!

!! Note that this demo page uses offline inference, so you can easily check the audio quality not the latency.
Please refer to `online_inference.py` and `online_inference.sh` for streaming inference.

## Environment Setup
1. (For **Mamba** setup)Pre-built Docker environments can be downloaded [here](https://github.com/RoyChao19477/SEMamba?tab=readme-ov-file#-docker-support) to simplify **Mamba** setup.

2. If you need bandwidth extension:

```bash
pip install resampy 
```
3. Download and navigate to the HuggingFace repository:
```
huggingface-cli download nvidia/Real-time_RE-USE --local-dir ./Realtime_REUSE --local-dir-use-symlinks False
cd ./Realtime_REUSE
```

## Inference
Follow the simple steps below to generate enhanced speech using our model:
1. Place your noisy speech files in the folder `noisy_audio/`
2. Run the following command:
```bash
sh offline_inference.sh
```
3. The enhanced speech files will be saved in `offline_enhanced_audio/`.

That's all !

**Note:**

a. You can enable bandwidth extension by setting the target bandwidth using the `BWE argument` in the script.

b. You can set `Exit_layer` (between 3 and 12), and `look_ahead_frames` (between 0 and 2), to achieve different **quality–latency** trade-offs.

c. We also provide the **Online Inference (one frame in, one frame out) code** for streaming model:
Please refer to `online_inference.py` and `online_inference.sh`.

=> The output of offline inference and online inference should be almost the same!!

---

## License/Terms of Use
This model is released under the [NVIDIA One-Way Noncommercial License (NSCLv1)](https://github.com/NVlabs/HMAR/blob/main/LICENSE).

## Deployment Geography
Global.

## Use Case
Researchers and general users can use this model to enhance the quality of their speech data. 
For example, ASR front-ends for improved noise robustness, TTS back-ends for enhanced output quality, and video conferencing.

## Release Date
Hugging Face 2026/04/14 (private)

## References
[1] [Rethinking Training Targets, Architectures and Data Quality for Universal Speech Enhancement](https://arxiv.org/abs/2603.02641), (NeurIPS 2026).

[2] [One Model, Many Latencies: Universal Speech Enhancement for Diverse Real-Time Applications](http://arxiv.org/abs/2606.25621), (IEEE SLT 2026).

(Note: The released model checkpoint differs from the one reported in the paper. It incorporates additional degradation types (e.g., microphone response and more codecs) and is fine-tuned on a smaller, high-quality clean subset.)

## Model Architecture
**Architecture Type:** Convolutional encoder, Convolutional decoder, and Mamba for time–frequency modeling <br>
**Network Architecture:** Mamba with up to 12 layers <br>
**Number of model parameters:** 3.7M <br>
 
## Input
Input Type(s): Audio <br>
Input Format(s): .wav files <br>
Input Parameters: One-Dimensional (1D) <br>
Other Properties Related to Input: 8000 Hz - 48000 Hz Mono-channel Audio <br>

## Output
Output Type(s): Audio <br>
Output Format: .wav files <br>
Output Parameters: One-Dimensional (1D) <br>
Other Properties Related to Output: 8000 Hz - 48000 Hz Mono-channel Audio <br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration
**Runtime Engine(s):**
* Not Applicable (N/A)

**Supported Hardware Microarchitecture Compatibility:**
* NVIDIA Ampere (A100)

**Preferred Operating System(s):**
* Linux

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s)
Current version: 12_random_layer_ahead_sep_conv2_1010k

## Training Datasets
**Data Modality:**
Audio

**Audio Training Data Size:**
Less than 10,000 Hours

* [LibriVox data from DNS5 challenge (EN)](https://github.com/microsoft/DNS-Challenge/tree/master) (~350 hours of speech data)
* [LibriTTS (EN)](https://openslr.org/60/) (~200 hours of speech data)
* [VCTK (EN)](https://datashare.ed.ac.uk/handle/10283/3443) (~80 hours of speech data)
* [WSJ (EN)](https://catalog.ldc.upenn.edu/LDC93S6A) (~85 hours of speech data)
* [EARS (EN)](https://sp-uhh.github.io/ears_dataset/) (~100 hours of speech data)
* [Multilingual Librispeech (De, En, Es, Fr)](https://www.openslr.org/94/) (~450 hours of speech data)
* [CommonVoice 19.0 (De, En, Es, Fr, zh-CN)](https://huggingface.co/datasets/fsicoli/common_voice_19_0) (~1300 hours of speech data)
* [Audioset+FreeSound noise in DNS5 challenge](https://github.com/microsoft/DNS-Challenge/tree/master) (~180 hours of noise data)
* [WHAM! Noise](http://wham.whisper.ai/) (~80 hours of noise data)
* [FSD50K (human voice filtered)](https://huggingface.co/datasets/Fhrozen/FSD50k) (~100 hours of non-speech data)
* [(Part of) Free Music Archive (medium)](https://github.com/mdeff/fma) (~200 hours of non-speech data)
* [Simulated RIRs from DNS5 challenge](https://github.com/microsoft/DNS-Challenge/tree/master) (~60k samples of room impulse response)
* [MicIRP](https://micirp.blogspot.com/p/about-micirp.html) (~70 samples of microphone impulse response)

## Inference
**Acceleration Engine:** None <br>
**Test Hardware:** NVIDIA A100

## Ethical Considerations
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.
Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://app.intigriti.com/programs/nvidia/nvidiavdp/detail).

## Citation
Please consider to cite our paper and this framework, if they are helpful in your research.

```bibtex
@article{fu2026rethinking,
  title={Rethinking Training Targets, Architectures and Data Quality for Universal Speech Enhancement},
  author={Fu, Szu-Wei and Chao, Rong and Yang, Xuesong and Huang, Sung-Feng and Zezario, Ryandhimas E and Nasretdinov, Rauf and Juki{\'c}, Ante and Tsao, Yu and Wang, Yu-Chiang Frank},
  journal={arXiv preprint arXiv:2603.02641},
  year={2026}
}
```

and 

```bibtex
@article{fu2026one,
  title={One Model, Many Latencies: Universal Speech Enhancement for Diverse Real-Time Applications},
  author={Fu, Szu-Wei and Chao, Rong and Yang, Xuesong and Huang, Sung-Feng and Juki{\'c}, Ante and Tsao, Yu and Wang, Yu-Chiang Frank},
  journal={arXiv preprint arXiv:2606.25621},
  year={2026}
}
```