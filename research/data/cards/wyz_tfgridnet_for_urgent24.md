---
tags:
- audio
- audio-to-audio
language: en
datasets:
- urgent24
license: cc-by-4.0
library_name: espnet
---

## ESPnet2 ENH model

### `wyz/tfgridnet_for_urgent24`

This model was trained by Wangyou Zhang using the [urgent24](https://github.com/espnet/espnet/blob/master/egs2/urgent24/enh1) recipe in [espnet](https://github.com/espnet/espnet/).

This model is provided as a pre-trained baseline model for the [URGENT 2024 Challenge](https://urgent-challenge.github.io/urgent2024).

### Demo: How to use in ESPnet2

Follow the [ESPnet installation instructions](https://espnet.github.io/espnet/installation.html)
if you haven't done that already.

```bash
cd espnet

pip install -e .
cd egs2/urgent24/enh1
./run.sh --skip_data_prep false --skip_train true --is_tse_task true --download_model wyz/tfgridnet_for_urgent24
```

To use the model in the Python interface, you could use the following code:
> Please make sure you are using the latest ESPnet by installing from the source:
> ```
> python -m pip install git+https://github.com/espnet/espnet
> ```

```python
import soundfile as sf
from espnet2.bin.enh_inference import SeparateSpeech

# For model downloading + loading
model = SeparateSpeech.from_pretrained(
    model_tag="wyz/tfgridnet_for_urgent24",
    normalize_output_wav=True,
    device="cuda",
)
# For loading a downloaded model
# model = SeparateSpeech(
#     train_config="exp/xxx/config.yaml",
#     model_file="exp/xx/valid.loss.best.pth",
#     normalize_output_wav=True,
#     device="cuda",
# )

audio, fs = sf.read("/path/to/noisy/utt1.flac")
enhanced = model(audio[None, :], fs=fs)[0]
```

## ENH config

<details><summary>expand</summary>

```
config: conf/tuning/train_enh_tfgridnet.yaml
print_config: false
log_level: INFO
drop_last_iter: false
dry_run: false
iterator_type: chunk
valid_iterator_type: null
output_dir: exp/enh_train_enh_tfgridnet_raw
ngpu: 1
seed: 0
num_workers: 4
num_att_plot: 3
dist_backend: nccl
dist_init_method: env://
dist_world_size: 4
dist_rank: 0
local_rank: 0
dist_master_addr: localhost
dist_master_port: 54825
dist_launcher: null
multiprocessing_distributed: true
unused_parameters: true
sharded_ddp: false
cudnn_enabled: true
cudnn_benchmark: false
cudnn_deterministic: true
collect_stats: false
write_collected_feats: false
max_epoch: 100
patience: 40
val_scheduler_criterion:
- valid
- loss
early_stopping_criterion:
- valid
- loss
- min
best_model_criterion:
-   - valid
    - loss
    - min
keep_nbest_models: 1
nbest_averaging_interval: 0
grad_clip: 1.0
grad_clip_type: 2.0
grad_noise: false
accum_grad: 1
no_forward_run: false
resume: true
train_dtype: float32
use_amp: false
log_interval: null
use_matplotlib: true
use_tensorboard: true
create_graph_in_tensorboard: false
use_wandb: false
wandb_project: null
wandb_id: null
wandb_entity: null
wandb_name: null
wandb_model_log_interval: -1
detect_anomaly: false
use_adapter: false
adapter: lora
save_strategy: all
adapter_conf: {}
pretrain_path: null
init_param: []
ignore_init_mismatch: false
freeze_param: []
num_iters_per_epoch: 8000
batch_size: 4
valid_batch_size: null
batch_bins: 1000000
valid_batch_bins: null
train_shape_file:
- exp/enh_stats_16k/train/speech_mix_shape
- exp/enh_stats_16k/train/speech_ref1_shape
valid_shape_file:
- exp/enh_stats_16k/valid/speech_mix_shape
- exp/enh_stats_16k/valid/speech_ref1_shape
batch_type: folded
valid_batch_type: null
fold_length:
- 80000
- 80000
sort_in_batch: descending
shuffle_within_batch: false
sort_batch: descending
multiple_iterator: false
chunk_length: 200
chunk_shift_ratio: 0.5
num_cache_chunks: 1024
chunk_excluded_key_prefixes: []
chunk_default_fs: 50
chunk_max_abs_length: 100000
chunk_discard_short_samples: true
train_data_path_and_name_and_type:
-   - dump/raw/train/wav.scp
    - speech_mix
    - sound
-   - dump/raw/train/spk1.scp
    - speech_ref1
    - sound
-   - dump/raw/train/utt2category
    - category
    - text
-   - dump/raw/train/utt2fs
    - fs
    - text_int
valid_data_path_and_name_and_type:
-   - dump/raw/validation/wav.scp
    - speech_mix
    - sound
-   - dump/raw/validation/spk1.scp
    - speech_ref1
    - sound
-   - dump/raw/validation/utt2category
    - category
    - text
-   - dump/raw/validation/utt2fs
    - fs
    - text_int
allow_variable_data_keys: false
max_cache_size: 0.0
max_cache_fd: 32
allow_multi_rates: true
valid_max_cache_size: null
exclude_weight_decay: false
exclude_weight_decay_conf: {}
optim: adam
optim_conf:
    lr: 0.001
    eps: 1.0e-08
    weight_decay: 1.0e-05
scheduler: steplr
scheduler_conf:
    step_size: 2
    gamma: 0.99
init: null
model_conf:
    normalize_variance_per_ch: true
    categories:
    - 1ch_8000Hz
    - 1ch_16000Hz
    - 1ch_22050Hz
    - 1ch_24000Hz
    - 1ch_32000Hz
    - 1ch_44100Hz
    - 1ch_48000Hz
criterions:
-   name: mr_l1_tfd
    conf:
        window_sz:
        - 256
        - 512
        - 768
        - 1024
        hop_sz: null
        eps: 1.0e-08
        time_domain_weight: 0.5
        normalize_variance: true
    wrapper: fixed_order
    wrapper_conf:
        weight: 1.0
-   name: si_snr
    conf:
        eps: 1.0e-07
    wrapper: fixed_order
    wrapper_conf:
        weight: 0.0
speech_volume_normalize: null
rir_scp: null
rir_apply_prob: 1.0
noise_scp: null
noise_apply_prob: 1.0
noise_db_range: '13_15'
short_noise_thres: 0.5
use_reverberant_ref: false
num_spk: 1
num_noise_type: 1
sample_rate: 8000
force_single_channel: true
channel_reordering: true
categories:
- 1ch_8000Hz
- 1ch_16000Hz
- 1ch_22050Hz
- 1ch_24000Hz
- 1ch_32000Hz
- 1ch_44100Hz
- 1ch_48000Hz
speech_segment: null
avoid_allzero_segment: true
flexible_numspk: false
dynamic_mixing: false
utt2spk: null
dynamic_mixing_gain_db: 0.0
encoder: stft
encoder_conf:
    n_fft: 256
    hop_length: 128
    use_builtin_complex: true
    default_fs: 8000
separator: tfgridnetv3
separator_conf:
    n_srcs: 1
    n_imics: 1
    n_layers: 6
    lstm_hidden_units: 200
    attn_n_head: 4
    attn_qk_output_channel: 2
    emb_dim: 48
    emb_ks: 4
    emb_hs: 1
    activation: prelu
    eps: 1.0e-05
decoder: stft
decoder_conf:
    n_fft: 256
    hop_length: 128
    default_fs: 8000
mask_module: multi_mask
mask_module_conf: {}
preprocessor: enh
preprocessor_conf: {}
diffusion_model: null
diffusion_model_conf: {}
required:
- output_dir
version: '202402'
distributed: true
```

</details>



### Citing ESPnet

```BibTex
@inproceedings{watanabe2018espnet,
  author={Shinji Watanabe and Takaaki Hori and Shigeki Karita and Tomoki Hayashi and Jiro Nishitoba and Yuya Unno and Nelson Yalta and Jahn Heymann and Matthew Wiesner and Nanxin Chen and Adithya Renduchintala and Tsubasa Ochiai},
  title={{ESPnet}: End-to-End Speech Processing Toolkit},
  year={2018},
  booktitle={Proceedings of Interspeech},
  pages={2207--2211},
  doi={10.21437/Interspeech.2018-1456},
  url={http://dx.doi.org/10.21437/Interspeech.2018-1456}
}


@inproceedings{ESPnet-SE,
  author = {Chenda Li and Jing Shi and Wangyou Zhang and Aswin Shanmugam Subramanian and Xuankai Chang and
  Naoyuki Kamo and Moto Hira and Tomoki Hayashi and Christoph B{"{o}}ddeker and Zhuo Chen and Shinji Watanabe},
  title = {ESPnet-SE: End-To-End Speech Enhancement and Separation Toolkit Designed for {ASR} Integration},
  booktitle = {{IEEE} Spoken Language Technology Workshop, {SLT} 2021, Shenzhen, China, January 19-22, 2021},
  pages = {785--792},
  publisher = {{IEEE}},
  year = {2021},
  url = {https://doi.org/10.1109/SLT48900.2021.9383615},
  doi = {10.1109/SLT48900.2021.9383615},
  timestamp = {Mon, 12 Apr 2021 17:08:59 +0200},
  biburl = {https://dblp.org/rec/conf/slt/Li0ZSCKHHBC021.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}


```

or arXiv:

```bibtex
@misc{watanabe2018espnet,
  title={ESPnet: End-to-End Speech Processing Toolkit},
  author={Shinji Watanabe and Takaaki Hori and Shigeki Karita and Tomoki Hayashi and Jiro Nishitoba and Yuya Unno and Nelson Yalta and Jahn Heymann and Matthew Wiesner and Nanxin Chen and Adithya Renduchintala and Tsubasa Ochiai},
  year={2018},
  eprint={1804.00015},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```