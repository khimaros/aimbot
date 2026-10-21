---
license: apache-2.0
tags:
- speech-translation
- audio-translation
- index
---

# Index-Echo-S2TT-2B

<p><a style="display:inline" href="https://index-translate.bilibili.com/">🌐 Online demo</a> · <a style="display:inline" href="https://github.com/bilibili/Index-Translate"><img src="https://raw.githubusercontent.com/bilibili/Index-Translate/main/docs/assets/github.svg" width="16" height="16" alt="" style="display:inline;vertical-align:middle;margin:0"> GitHub</a> · <a style="display:inline" href="https://arxiv.org/abs/2609.40181">📚 Technical report</a> · <a style="display:inline" href="https://huggingface.co/collections/IndexTeam/index-translate">🤗 Hugging Face collection</a> · <a style="display:inline" href="https://www.modelscope.cn/collections/IndexTeam/Index-Translate"><img src="https://raw.githubusercontent.com/bilibili/Index-Translate/main/docs/assets/modelscope.svg" width="16" height="16" alt="" style="display:inline;vertical-align:middle;margin:0"> ModelScope collection</a></p>

**Index-Echo-S2TT-2B** translates speech into text using a Qwen3-Omni AuT audio encoder, an audio connector, and an Index-Translate-2B decoder. The released package accepts audio or video files and writes bilingual subtitles with sentence timestamps. Its packaged inference interface supports **Chinese → English, Japanese, or Spanish**.

This is the speech-to-text member of the Index-Translate family. The [9B sibling](https://huggingface.co/IndexTeam/Index-Echo-S2TT-9B) provides the same packaged interface at a different model size.

## Architecture

![Index-Echo speech-to-text and speech-to-speech architecture](https://raw.githubusercontent.com/bilibili/Index-Translate/main/docs/assets/index-echo-architecture.png)

The report's upper path shows the S2TT model: source audio → Qwen3-Omni AuT encoder → audio connector → Index-Translate decoder → translated target text. This card covers that speech-to-text path; the lower path adds speech generation for S2ST.

## Model and training

The [technical report](https://arxiv.org/abs/2609.40181) describes end-to-end training on speech translation: acoustic input, target-language instructions, and translated text are represented in a single sequence. The model learns to interpret source audio directly while using the multilingual text decoder for translation. It produces the source transcript and target translation together with per-sentence timestamps.

The self-contained export includes the trained audio encoder and connector as safetensors, plus the Qwen3.5-family decoder in Hugging Face format under `llm/`. See `MODEL_INFO.json` for the export's checkpoint details. The name's **2B** refers to the decoder size; the package also contains the audio components.

## Inference

Install the Hugging Face CLI, download the package, and install its inference requirements. System `ffmpeg` must be available on `PATH`.

```bash
pip install -U huggingface_hub
hf download IndexTeam/Index-Echo-S2TT-2B --local-dir ./Index-Echo-S2TT-2B
pip install -r Index-Echo-S2TT-2B/requirements.txt
python3 Index-Echo-S2TT-2B/infer.py input.mp4 --target-lang en --out out_dir
```

The official inference guide uses `torch==2.11.0` and `transformers==5.6.0`, with `safetensors`, `librosa`, `soundfile`, and `silero-vad`. Keep the packaged requirements and a CUDA-compatible PyTorch build when setting up the environment. See the [S2TT guide](https://github.com/bilibili/Index-Translate/tree/main/inference/echo-s2tt) for the GitHub wrapper and additional examples.

Outputs are `out_dir/input.srt` (Chinese transcript and target translation in each cue) and `out_dir/input.windows.jsonl` (raw per-window output and a final summary).

### Default inference settings

| Setting / CLI option | Released default | Meaning |
|---|---|---|
| `inputs` | Required, one or more files | Audio/video paths, processed sequentially |
| `--out` | Required | Directory for SRT and per-window JSONL outputs |
| `--temperature` | `0.0` | Greedy decoding (`do_sample=False`); positive values enable sampling |
| `--max-new-tokens` | `2000` | Output-token budget per audio window |
| `--max-win` | `60.0` seconds | VAD audio-window cap |
| `--ctx-k` | `5` | Maximum number of previous output windows used as context |
| `--target-lang` | `en` | Target choices: `en`, `ja`, `es` |
| `--glossary` | Empty string | Inline terminology; for example `原名:Translated name` |
| `--glossary-file` | Empty string | UTF-8 terminology file; takes priority over `--glossary` |
| `--device` | `cuda:0` | Device used to load the model |
| Model dtype | `torch.bfloat16` | Set by the package loader, not a CLI option |
| Text stopping | Tokenizer EOS or `<|im_end|>` | Stops generation; padding uses tokenizer EOS |

These defaults are identical for the 2B and 9B subtitle scripts. The package does not explicitly override `top_p`, `top_k`, or repetition penalties; values for those settings follow the decoder generation configuration. The prompt prefills an empty `<think>` block, as in the released script. The greedy speech-transcription/translation settings belong to the speech package; they are distinct from the text-model client settings.

```bash
python3 Index-Echo-S2TT-2B/infer.py input.mp4 \
  --target-lang ja --out out_ja \
  --temperature 0 --max-new-tokens 2000 --max-win 60 --ctx-k 5 \
  --glossary "原名1:訳名1,原名2:訳名2" --device cuda:0
```

`ffmpeg` converts input to 16 kHz mono audio. Silero VAD divides it into windows; inference runs sequentially and feeds previous transcript/translation windows into the context slot. `--glossary` supplies terminology, and `--glossary-file` reads the same format from a file with priority over the inline value. Context and glossary instructions help with consistency but do not guarantee exact compliance.

## Evaluation

On the report's in-house video translation set, Index-Echo-2B achieves **0.825 MT judge**, **0.088 median ASR error**, and **0.395 s start-time MAE**. Its ASR and timestamp errors are the lowest in this comparison.

The set contains **140 total windows**, each 50–60 seconds long: **20 windows per direction** for Chinese → English/Japanese/Korean/Spanish/Portuguese/Arabic and English → Chinese. This broader evaluation setup is separate from the released `infer.py` interface, which exposes Chinese → English/Japanese/Spanish.

| Model | MT judge ↑ | ASR error (median) ↓ | Start-time MAE (s) ↓ |
|---|---:|---:|---:|
| Qwen3.8-Omni-Flash | **0.887** | 0.112 | 1.004 |
| Index-Echo-9B | 0.857 | 0.102 | 0.488 |
| Gemini-3.1-Pro (thinking) | 0.849 | 0.169 | 1.824 |
| Qwen3.8-LiveTranslate | 0.833 | 0.186 | — |
| **Index-Echo-2B** | 0.825 | **0.088** | **0.395** |
| Gemini-2.5-Flash (thinking) | 0.817 | 0.201 | 2.402 |
| Gemini-2.5-Flash | 0.757 | 0.479 | 1.746 |
| Qwen3-Omni | 0.700 | 0.139 | 1.145 |
| FireRed Audio | 0.448 | 0.128 | 0.765 |
| SeamlessM4T-v2 | 0.060 | 1.000 | — |

The MT judge averages Gemini-3.1-Pro's per-line quality ratings on a 0/0.5/1 scale. ASR error compares the source transcription with the reference transcript; the table reports its median. Start-time MAE is the mean absolute difference between predicted and reference sentence start times, in seconds. Bold metric values mark the best result in each column.

Qwen3.8-LiveTranslate was evaluated in streaming mode. Dashes indicate unavailable timestamp outputs. SeamlessM4T-v2 received unchunked inputs of approximately 57 seconds, beyond its approximately 30-second effective range, and does not support the line-level timestamp instructions used here. Its score should be interpreted under those input conditions. These are in-house results, not a universal ranking across speech tasks or deployment settings. See the [report](https://arxiv.org/abs/2609.40181) and [evaluation tables](https://github.com/bilibili/Index-Translate/blob/main/docs/evaluation.md) for the protocol.

## Package files and limitations

| File or directory | Purpose |
|---|---|
| `config.json` | Package configuration: component paths and inference entry point |
| `infer.py`, `requirements.txt` | Packaged subtitle inference and dependencies |
| `llm/` | Index-Translate-derived decoder and tokenizer |
| `audio_tower.safetensors`, `audio_config.json` | Trained AuT audio encoder |
| `connector.safetensors` | Audio-to-decoder connector |
| `MODEL_INFO.json` | Source checkpoint and export information |

The root `config.json` describes the complete S2TT package. Use `infer.py` to load it; the decoder’s Transformers configuration remains at `llm/config.json`.

The packaged 2B script reports approximately 10 GB VRAM with bf16; allow additional memory headroom for your input and runtime. Processing is sequential within each input file; separate files can be assigned to separate GPUs.

Timestamp accuracy and transcript/translation quality can vary with audio conditions and content. Greedy decoding may repeat on out-of-distribution inputs; the script accepts a positive `--temperature` to enable sampling, which can change both translation and timing. Review subtitles when precise alignment or terminology is required. The package is a file-based subtitle interface; its windowing does not establish a real-time latency guarantee.

For speech generation and long-video dubbing, use the separate [S2ST packages](https://github.com/bilibili/Index-Translate/tree/main/inference/echo-s2st) or the [video dubbing pipeline](https://github.com/bilibili/Index-Translate/tree/main/video-dub).

## Related models

| Family | Task | Released sizes |
|---|---|---|
| Index-Translate | Text translation and translation instructions across 150 languages | [2B](https://huggingface.co/IndexTeam/Index-Translate-2B), [9B](https://huggingface.co/IndexTeam/Index-Translate-9B), [35B-A3B (preview)](https://huggingface.co/IndexTeam/Index-Translate-35B-A3B-preview) |
| Index-Echo S2TT | Speech-to-text translation and subtitles | [2B](https://huggingface.co/IndexTeam/Index-Echo-S2TT-2B), [9B](https://huggingface.co/IndexTeam/Index-Echo-S2TT-9B) |
| Index-Echo S2ST | Speech-to-speech translation with source-voice conditioning | [2B](https://huggingface.co/IndexTeam/Index-Echo-S2ST-2B), [9B](https://huggingface.co/IndexTeam/Index-Echo-S2ST-9B) |
| Index-Homura | Translation with a target syllable count | [2B](https://huggingface.co/IndexTeam/Index-Homura-2B), [9B](https://huggingface.co/IndexTeam/Index-Homura-9B) |
| Index-NativeLong | Native long-document translation; released as Index-Nailong | [2B](https://huggingface.co/IndexTeam/Index-Nailong-2B), [9B](https://huggingface.co/IndexTeam/Index-Nailong-9B) |

The text foundation's 150-language coverage does not describe the released speech interfaces. Use the task-specific directions documented above.


## Citation

```bibtex
@techreport{indextranslate2026,
  author={Tianjiao Li and Mengran Yu and Chenyu Shi and Lusheng Zhang and
          Qisi Chen and Yanshan Zhou and Ji Qi and Jingying Liu and
          Yuang Feng and Ziang Cui and Tianxing Yan},
  title={Index-Translate: A Multilingual Translation Model Family --- Text, Speech, Controlled Dubbing, and Long-Document Translation},
  institution={Index LLM Team},
  year={2026},
  month={September}
}
```

## License and feedback

[Apache-2.0](https://github.com/bilibili/Index-Translate/blob/main/LICENSE). Questions and feedback are welcome through [GitHub Issues](https://github.com/bilibili/Index-Translate/issues).
