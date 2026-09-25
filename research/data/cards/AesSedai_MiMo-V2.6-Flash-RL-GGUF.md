---
base_model:
- XiaomiMiMo/MiMo-V2.6-Flash-RL
---

## Updates
- 09/22/26: Added 3.5, 2.5, and 2.0 BPW quants using [ed's bpw-size PR](https://github.com/ggml-org/llama.cpp/pull/15550). The FFNs are the primarily quantized feature, rest of the model remains in Q8_0 / Q6_K

This repo contains specialized MoE-quants for XiaomiMiMo/MiMo-V2.6-Flash-RL. The idea being that given the huge size of the FFN tensors compared to the rest of the tensors in the model, it should be possible to achieve a better quality while keeping the overall size of the entire model smaller compared to a similar naive quantization. To that end, the quantization type default is kept in high quality and the FFN UP + FFN GATE tensors are quanted down along with the FFN DOWN tensors.

The MXFP4 quant is the "full quality" version, as the model has MXFP4 experts.

| Quant  | Size                  | Mixture                               | PPL                 | 1-(Mean PPL(Q)/PPL(base)) | KLD                  |
| :----- | :-------------------- | :------------------------------------ | :------------------ | :------------------------ | :------------------- |
| MXFP4  | 162.89 GiB (4.52 BPW) | BF16 / MXFP4  | 5.149210 ± 0.030596 | +0.0715%                  | -0.000000 ± 0.000000 |
| Q3_K   | 137.75 GiB (3.82 BPW) | Q8_0 / Q3_K / Q3_K / MXFP4            | 5.177623 ± 0.030900 | +0.6237%                  | 0.123607 ± 0.000648  |
| BPW3.5 | 126.19 GiB (3.50 BPW) | Q8_0 / varies | 5.232510 ± 0.031063 | +1.6904%                  | 0.138808 ± 0.000718  |
| IQ2_S  | 106.31 GiB (2.95 BPW) | Q6_K / IQ2_S / IQ2_S / Q3_K           | 5.404774 ± 0.032158 | +5.0382%                  | 0.178092 ± 0.000878  |
| BPW2.5 | 90.14 GiB (2.50 BPW)  | Q8_0 / varies | 5.739578 ± 0.034587 | +11.5449%                 | 0.243713 ± 0.001158  |
| BPW2.0 | 66.99 GiB (1.86 BPW)  | Q6_K / varies | 7.290888 ± 0.046722 | +41.6936%                 | 0.477636 ± 0.002111  |


![kld_graph](kld_data/01_kld_vs_filesize.png "Chart showing Pareto KLD analysis of quants")
![ppl_graph](kld_data/02_ppl_vs_filesize.png "Chart showing Pareto PPL analysis of quants")