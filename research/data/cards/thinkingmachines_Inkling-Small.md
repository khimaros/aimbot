---
license: apache-2.0
license_link: https://www.apache.org/licenses/LICENSE-2.0
pipeline_tag: image-text-to-text
tags:
- conversational
- image-text-to-text
- audio-text-to-text
- moe
library_name: transformers
---

# Inkling

<img src="https://cdn-uploads.huggingface.co/production/uploads/630e8f0bf6f6d700f50ebd2e/AvmDwmrWRMnKjOWvmLieg.png" style="display: block;margin-left: auto;margin-right: auto;width: 30%;">

<p align="center">
  <a href="https://huggingface.co/thinkingmachines/Inkling-Small">BF16</a> |
  <a href="https://huggingface.co/thinkingmachines/Inkling-Small-NVFP4">NVFP4</a> |
  <a href="https://tinker.thinkingmachines.ai/playground">Playground</a> |
  <a href="https://github.com/thinking-machines-lab/tinker-cookbook">Tinker Cookbook</a> |
  <a href="https://thinkingmachines.ai/model-acceptable-use-policy">Acceptable Use</a>
</p>

## 1. General Information

Inkling-Small is a general-purpose multimodal model that accepts text, image and audio inputs and generates text outputs. It is intended for use in English and other languages, and across multiple coding languages. The model is designed to be used by developers building AI-powered applications, including agentic and tool-use systems, coding assistants, chatbots, and retrieval-augmented generation systems, and is suitable for general-purpose conversational use, instruction-following, and other natural language and multimodal tasks. It is released with open weights to support research, fine-tuning and integration into third-party products by downstream developers.

**Languages:** English, with general multilingual capabilities across other languages.

## 2. Getting Started

Try Inkling-Small on the [Tinker Playground](https://tinker.thinkingmachines.ai/playground) or access via API using the [Tinker Cookbook](https://github.com/thinking-machines-lab/tinker-cookbook).

Inkling-Small supports local deployment using the following open-source libraries:

* SGLang ([recipe](https://docs.sglang.io/cookbook/autoregressive/ThinkingMachines/Inkling-Small))
* vLLM ([recipe](https://recipes.vllm.ai/thinkingmachines/Inkling-Small))
* TokenSpeed ([recipe](https://lightseek.org/tokenspeed/recipes/models#Inkling))
* Unsloth ([recipe](https://unsloth.ai/docs/models/inkling))
* Huggingface ([recipe](https://hf.co/blog/thinkingmachines-inkling))

API access is also available through third party inference providers.

## 3. Model Properties

### Model type

Multimodal autoregressive transformer

### Architecture type

A 42-layer decoder-only transformer with a sparse Mixture-of-Experts (MoE) feed-forward backbone: each token is routed to 6 of 256 experts, plus 2 shared experts active on every token. Attention is a hybrid of local and global layers. The model is natively multimodal — images are encoded via a hierarchical patch encoder, and audio via discrete token encoding — with all modalities projected into a shared hidden space and processed jointly by the decoder.

### Parameters

276B total, 12B active

### Numerics support

BF16 and NVFP4

### Input modalities

Inkling-Small accepts text, image, and audio inputs:

- Text: UTF-8 encoded text
- Image: Any pixel-based image input. For optimal performance, each image dimension should be between 40px to 4096px.
- Audio: WAV format, sampled at 16kHz. For optimal performance, audio length should ideally be under 2 mins.

### Output modalities

Inkling-Small generates output as UTF-8 encoded text.

## 4. Training

Training data includes a broad variety of content types, including text, images, audio, video. 

Training data for the model was drawn from publicly available sources, acquired from third-parties, or synthetically generated or augmented.  Publicly available data includes content from the public internet and publicly accessible repositories.

The training data curation process includes cleaning, processing, and modifying datasets. These processing steps, which vary by data type, may include deduplication and filtering to remove junk or other low-quality data, or to advance safety or other objectives.

## 5. Evaluations

<table class="benchmark-results-table benchmark-results-categorized">
    <colgroup>
      <col class="benchmark-name-column">
      <col class="benchmark-model-column" span="10">
    </colgroup>
    <thead>
      <tr class="benchmark-model-group-row">
        <td class="benchmark-heading-spacer" aria-hidden="true"></td>
        <th class="benchmark-model-group" colspan="7" scope="colgroup">
          <span class="benchmark-model-group-anchor"><span class="benchmark-model-group-label">Open weights</span></span>
        </th>
        <th class="benchmark-model-group" colspan="3" scope="colgroup">
          <span class="benchmark-model-group-anchor"><span class="benchmark-model-group-label">Closed weights</span></span>
        </th>
      </tr>
      <tr class="benchmark-model-header-row">
        <td class="benchmark-heading-spacer" aria-hidden="true"></td>
        <th class="benchmark-model benchmark-instant-start"><span class="benchmark-lock-content"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Inkling-Small</span></span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Qwen3.5</span> <span class="benchmark-model-name-line">397B-A17B</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">MiMo V2.5</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Minimax M2.7</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">DeepSeek V4</span> <span class="benchmark-model-name-line">Flash</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Nemotron 3</span> <span class="benchmark-model-name-line">Ultra</span></span></th>
        <th class="benchmark-model benchmark-instant-start"><span class="benchmark-lock-content"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Inkling</span></span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Claude 4.5</span> <span class="benchmark-model-name-line">Haiku</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">Gemini 3.5</span> <span class="benchmark-model-name-line">Flash-Lite</span></span></th>
        <th class="benchmark-model"><span class="benchmark-model-name">
            <span class="benchmark-model-name-line">GPT 5.6</span> <span class="benchmark-model-name-line">Luna</span></span></th>
      </tr>
    </thead>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Model Info</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">AA Index</span> <span class="benchmark-subtitle">(v4.1)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">40.0%</span></td>
        <td class="benchmark-value">34.0%</td>
        <td class="benchmark-value">37.0%</td>
        <td class="benchmark-value">38.0%</td>
        <td class="benchmark-value">40.0%</td>
        <td class="benchmark-value">38.0%</td>
        <td class="benchmark-value">41.0%</td>
        <td class="benchmark-value">30.0%</td>
        <td class="benchmark-value">36.0%</td>
        <td class="benchmark-value">49.0%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Params (B)</span> <span class="benchmark-subtitle">(activated / total)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">12 / 276</span></td>
        <td class="benchmark-value">17 / 397</td>
        <td class="benchmark-value">15 / 310</td>
        <td class="benchmark-value">10 / 230</td>
        <td class="benchmark-value">13 / 284</td>
        <td class="benchmark-value">55 / 550</td>
        <td class="benchmark-value">41 / 975</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Agentic (coding)</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">SWEBench Verified</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">80.2%</span></td>
        <td class="benchmark-value">76.4%</td>
        <td class="benchmark-value">71.0%</td>
        <td class="benchmark-value">79.9%</td>
        <td class="benchmark-value">79.0%</td>
        <td class="benchmark-value">70.7%</td>
        <td class="benchmark-value">77.6%</td>
        <td class="benchmark-value">73.3%</td>
        <td class="benchmark-value">75.0%</td>
        <td class="benchmark-value">93.0%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">SWEBench Pro</span> <span class="benchmark-subtitle">(public)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">55.9%</span></td>
        <td class="benchmark-value">50.9%</td>
        <td class="benchmark-value">56.1%</td>
        <td class="benchmark-value">56.2%</td>
        <td class="benchmark-value">52.6%</td>
        <td class="benchmark-value">46.4%</td>
        <td class="benchmark-value">54.3%</td>
        <td class="benchmark-value">39.5%</td>
        <td class="benchmark-value">54.2%</td>
        <td class="benchmark-value">62.7%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Terminal Bench 2.1</span> <span class="benchmark-subtitle">(best harness)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">64.7%</span></td>
        <td class="benchmark-value">51.3%</td>
        <td class="benchmark-value">63.7%</td>
        <td class="benchmark-value">55.4%</td>
        <td class="benchmark-value">61.8%</td>
        <td class="benchmark-value">56.4%</td>
        <td class="benchmark-value">63.8%</td>
        <td class="benchmark-value">44.2%</td>
        <td class="benchmark-value">54.0%</td>
        <td class="benchmark-value">82.5%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">SciCode</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">48.7%</span></td>
        <td class="benchmark-value">42.0%</td>
        <td class="benchmark-value">43.1%</td>
        <td class="benchmark-value">47.0%</td>
        <td class="benchmark-value">44.9%</td>
        <td class="benchmark-value">39.9%</td>
        <td class="benchmark-value">46.1%</td>
        <td class="benchmark-value">43.3%</td>
        <td class="benchmark-value">40.9%</td>
        <td class="benchmark-value">50.0%</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Agentic (general)</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">GDPval-AA v2</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">1269</span></td>
        <td class="benchmark-value">962</td>
        <td class="benchmark-value">1145</td>
        <td class="benchmark-value">1159</td>
        <td class="benchmark-value">1189</td>
        <td class="benchmark-value">1164</td>
        <td class="benchmark-value">1238</td>
        <td class="benchmark-value">911</td>
        <td class="benchmark-value">1139</td>
        <td class="benchmark-value">1530</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">MCP Atlas</span> <span class="benchmark-subtitle">(public / all)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">79.6/79.2%</span></td>
        <td class="benchmark-value">74.2%/–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">49.4%/–</td>
        <td class="benchmark-value">69.0%/–</td>
        <td class="benchmark-value">47.4/44.7%</td>
        <td class="benchmark-value">78.8/76.0%</td>
        <td class="benchmark-value">41.2/40.2%</td>
        <td class="benchmark-value">79.8/76.8%</td>
        <td class="benchmark-value">77.0/75.0%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Tau 3 Banking</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">15.5%</span></td>
        <td class="benchmark-value">13.4%</td>
        <td class="benchmark-value">6.6%</td>
        <td class="benchmark-value">8.9%</td>
        <td class="benchmark-value">22.9%</td>
        <td class="benchmark-value">13.8%</td>
        <td class="benchmark-value">23.7%</td>
        <td class="benchmark-value">9.1%</td>
        <td class="benchmark-value">16.5%</td>
        <td class="benchmark-value">24.3%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">BrowseComp</span> <span class="benchmark-subtitle">(with context management)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">77.4%</span></td>
        <td class="benchmark-value">78.6%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">76.3%</td>
        <td class="benchmark-value">73.2%</td>
        <td class="benchmark-value">63.0%</td>
        <td class="benchmark-value">77.1%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">84.0%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Toolathlon Verified</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">54.4%</span></td>
        <td class="benchmark-value">40.7%</td>
        <td class="benchmark-value">49.1%</td>
        <td class="benchmark-value">47.5%</td>
        <td class="benchmark-value">50.9%</td>
        <td class="benchmark-value">34.3%</td>
        <td class="benchmark-value">45.5%</td>
        <td class="benchmark-value">26.9%</td>
        <td class="benchmark-value">57.1%</td>
        <td class="benchmark-value">67.9%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">AA-Briefcase</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">917</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">833</td>
        <td class="benchmark-value">870</td>
        <td class="benchmark-value">839</td>
        <td class="benchmark-value">612</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Reasoning (general)</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">GPQA Diamond</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">89.5%</span></td>
        <td class="benchmark-value">89.3%</td>
        <td class="benchmark-value">84.9%</td>
        <td class="benchmark-value">87.4%</td>
        <td class="benchmark-value">89.4%</td>
        <td class="benchmark-value">86.7%</td>
        <td class="benchmark-value">87.2%</td>
        <td class="benchmark-value">67.2%</td>
        <td class="benchmark-value">83.8%</td>
        <td class="benchmark-value">89.5%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">HLE</span> <span class="benchmark-subtitle">(text only)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">31.6%</span></td>
        <td class="benchmark-value">27.3%</td>
        <td class="benchmark-value">25.2%</td>
        <td class="benchmark-value">28.1%</td>
        <td class="benchmark-value">32.1%</td>
        <td class="benchmark-value">26.6%</td>
        <td class="benchmark-value">29.7%</td>
        <td class="benchmark-value">9.7%</td>
        <td class="benchmark-value">17.5%</td>
        <td class="benchmark-value">35.6%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">HLE</span> <span class="benchmark-subtitle">(with tools)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">47.8%</span></td>
        <td class="benchmark-value">48.3%</td>
        <td class="benchmark-value">40.0%</td>
        <td class="benchmark-value">40.3%</td>
        <td class="benchmark-value">45.1%</td>
        <td class="benchmark-value">37.4%</td>
        <td class="benchmark-value">46.0%</td>
        <td class="benchmark-value">17.8%</td>
        <td class="benchmark-value">42.5%</td>
        <td class="benchmark-value">48.9%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">AIME 2026</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">95.5%</span></td>
        <td class="benchmark-value">93.3%</td>
        <td class="benchmark-value">93.6%</td>
        <td class="benchmark-value">87.7%</td>
        <td class="benchmark-value">95.8%</td>
        <td class="benchmark-value">94.2%</td>
        <td class="benchmark-value">97.1%</td>
        <td class="benchmark-value">85.1%</td>
        <td class="benchmark-value">82.2%</td>
        <td class="benchmark-value">97.6%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">HMMT Feb 2026</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">90.2%</span></td>
        <td class="benchmark-value">87.9%</td>
        <td class="benchmark-value">82.6%</td>
        <td class="benchmark-value">71.2%</td>
        <td class="benchmark-value">93.9%</td>
        <td class="benchmark-value">78.8%</td>
        <td class="benchmark-value">86.3%</td>
        <td class="benchmark-value">66.7%</td>
        <td class="benchmark-value">63.6%</td>
        <td class="benchmark-value">98.5%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">CritPt</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">8.3%</span></td>
        <td class="benchmark-value">1.7%</td>
        <td class="benchmark-value">3.7%</td>
        <td class="benchmark-value">0.6%</td>
        <td class="benchmark-value">7.1%</td>
        <td class="benchmark-value">3.1%</td>
        <td class="benchmark-value">5.4%</td>
        <td class="benchmark-value">0.0%</td>
        <td class="benchmark-value">0.0%</td>
        <td class="benchmark-value">20.6%</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Reasoning (abstract)</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">ARC-AGI-1</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">84.0%</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">79.5%</td>
        <td class="benchmark-value">47.7%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">87.7%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">ARC-AGI-2</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">40.1%</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">36.5%</td>
        <td class="benchmark-value">4.0%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">47.6%</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Factuality</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">SimpleQA Verified</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">20.6%</span></td>
        <td class="benchmark-value">26.0%</td>
        <td class="benchmark-value">16.1%</td>
        <td class="benchmark-value">13.5%</td>
        <td class="benchmark-value">34.1%</td>
        <td class="benchmark-value">32.4%</td>
        <td class="benchmark-value">43.9%</td>
        <td class="benchmark-value">5.9%</td>
        <td class="benchmark-value">44.1%</td>
        <td class="benchmark-value">41.7%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">AA Omniscience</span> <span class="benchmark-subtitle">(index)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">-9.0</span></td>
        <td class="benchmark-value">-29.8</td>
        <td class="benchmark-value">-9.3</td>
        <td class="benchmark-value">0.7</td>
        <td class="benchmark-value">-22.9</td>
        <td class="benchmark-value">-1.0</td>
        <td class="benchmark-value">2.1</td>
        <td class="benchmark-value">-4.2</td>
        <td class="benchmark-value">6.9</td>
        <td class="benchmark-value">-11.6</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Chat</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">IFBench</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">82.2%</span></td>
        <td class="benchmark-value">78.8%</td>
        <td class="benchmark-value">67.1%</td>
        <td class="benchmark-value">75.7%</td>
        <td class="benchmark-value">79.2%</td>
        <td class="benchmark-value">81.4%</td>
        <td class="benchmark-value">79.8%</td>
        <td class="benchmark-value">54.3%</td>
        <td class="benchmark-value">78.6%</td>
        <td class="benchmark-value">67.3%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Global-MMLU-Lite</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">86.7%</span></td>
        <td class="benchmark-value">90.0%</td>
        <td class="benchmark-value">83.5%</td>
        <td class="benchmark-value">83.9%</td>
        <td class="benchmark-value">88.4%</td>
        <td class="benchmark-value">85.6%</td>
        <td class="benchmark-value">88.7%</td>
        <td class="benchmark-value">83.4%</td>
        <td class="benchmark-value">89.4%</td>
        <td class="benchmark-value">88.7%</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Safety</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">StrongREJECT</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">98.4%</span></td>
        <td class="benchmark-value">99.4%</td>
        <td class="benchmark-value">99.3%</td>
        <td class="benchmark-value">99.4%</td>
        <td class="benchmark-value">97.4%</td>
        <td class="benchmark-value">98.7%</td>
        <td class="benchmark-value">98.6%</td>
        <td class="benchmark-value">98.6%</td>
        <td class="benchmark-value">97.6%</td>
        <td class="benchmark-value">98.7%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">FORTRESS</span> <span class="benchmark-subtitle">(adversarial)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">71.6%</span></td>
        <td class="benchmark-value">77.3%</td>
        <td class="benchmark-value">64.8%</td>
        <td class="benchmark-value">86.3%</td>
        <td class="benchmark-value">32.0%</td>
        <td class="benchmark-value">77.6%</td>
        <td class="benchmark-value">78.0%</td>
        <td class="benchmark-value">91.3%</td>
        <td class="benchmark-value">70.7%</td>
        <td class="benchmark-value">83.8%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">FORTRESS</span> <span class="benchmark-subtitle">(benign)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">96.9%</span></td>
        <td class="benchmark-value">95.4%</td>
        <td class="benchmark-value">94.6%</td>
        <td class="benchmark-value">90.1%</td>
        <td class="benchmark-value">99.2%</td>
        <td class="benchmark-value">90.6%</td>
        <td class="benchmark-value">95.9%</td>
        <td class="benchmark-value">94.1%</td>
        <td class="benchmark-value">95.5%</td>
        <td class="benchmark-value">97.8%</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Vision</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">MMMU Pro</span> <span class="benchmark-subtitle">(Standard 10)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">74.0%</span></td>
        <td class="benchmark-value">77.3%</td>
        <td class="benchmark-value">75.4%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">73.5%</td>
        <td class="benchmark-value">58.6%</td>
        <td class="benchmark-value">79.0%</td>
        <td class="benchmark-value">78.6%</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Charxiv RQ</span> <span class="benchmark-subtitle">(original / with python)</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">77.4/81.3%</span></td>
        <td class="benchmark-value">80.8%/–</td>
        <td class="benchmark-value">81.0%/–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">78.1/82.0%</td>
        <td class="benchmark-value">57.4%/–</td>
        <td class="benchmark-value">70.0%/–</td>
        <td class="benchmark-value">81.4%/–</td>
      </tr>
    </tbody>
    <tbody class="benchmark-category-group">
      <tr class="benchmark-category-row">
        <th class="benchmark-category-label" scope="rowgroup"><span class="benchmark-category-label-text">Audio</span></th>
        <td class="benchmark-category-cell benchmark-value benchmark-instant-start" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
        <td class="benchmark-category-cell" aria-hidden="true"></td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">Audio MC</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">54.9%</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">30.4%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">56.6%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">33.6%</td>
        <td class="benchmark-value">–</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">MMAU</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">77.0%</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">73.6%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">77.2%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">75.2%</td>
        <td class="benchmark-value">–</td>
      </tr>
      <tr>
        <td class="benchmark-name">
          <span class="benchmark-title">VoiceBench</span>
        </td>
        <td class="benchmark-value benchmark-instant-start"><span class="benchmark-lock-content">90.1%</span></td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">86.4%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">91.4%</td>
        <td class="benchmark-value">–</td>
        <td class="benchmark-value">85.9%</td>
        <td class="benchmark-value">–</td>
      </tr>
    </tbody>
  </table>

- <small>Inkling-Small against open-and closed-weights models across the full eval suite. Activated and total parameters are given for scale; a dash means the score was not available at the time of writing.</small>
- <small>SWEBench Verified: Inkling and Inkling-Small’s numbers are reported using a bash-only harness. We use self-reported numbers for external models.</small>
- <small>Terminal Bench 2.1: Inkling and Inkling-Small’s numbers are reported using an internal coding harness. A small number of solutions were found to be contaminated from web search and were assigned a score of 0. We use self-reported numbers for external models where available. Otherwise, we report performance using our internal harness.</small>
- <small>Audio MC: Other models were evaluated internally since they are not on the official leaderboard.</small>
- <small>VoiceBench: VoiceBench uses rule-based, hard-coded string matching for grading, making the evaluation sensitive to output-formatting differences. We therefore added a system message instructing models to follow the expected answer format.</small>
- <small>HLE with tools: We benchmarked Minimax M2.7, Claude 4.5 Haiku, Gemini 3.5 Flash-Lite, and GPT 5.6 Luna using our internal harness.</small>

## 6. Safety

We conducted safety evaluations ahead of release, spanning both everyday human-AI interaction and dangerous-capability testing. Because Inkling-Small is multimodal, we paid attention to whether safety behavior held consistently across text, audio, and image inputs. We applied mitigations to reduce risks before release.

For everyday interaction, we evaluated sycophancy, harmful manipulation, and psychological-harm patterns like parasocial dependency and validation of delusional reasoning, including through multi-turn, open-ended external red-teaming designed to surface issues that only emerge over longer conversations. We also assessed whether the model refuses genuinely harmful requests without over-refusing benign ones. For CBRN and cyber, we assessed knowledge and procedural uplift through internal evaluations, external testing, and refusal-suppressed variants intended to estimate latent capability with safeguards removed. For loss of control, we evaluated agentic capability, strategic deception, and sabotage potential, benchmarked against public frontier models, and found the model materially below frontier capabilities.

Across all areas, we concluded that Inkling-Small did not present risk of material uplift beyond what's already available in the open-weight ecosystem.

The residual risks identified in our evaluations — specifically, Inkling-Small’s occasional tendency to comply with role-play and indirectly framed prompts concerning harmful topics — are consistent with what you would see from any open-weight model, and are best addressed with defense-in-depth rather than relying on the model's refusals alone. Common downstream moderation tools, such as Llama Guard, are compatible with Inkling-Small and can be layered around the model to catch jailbreak attempts, filter unsafe outputs, and enforce use-case-specific policies. We would encourage treating this kind of input/output classification as a part of your deployment stack, especially for consumer-facing or high-traffic applications where adversarial prompting is more likely.

## 7. Bias, risks and limitations

Inkling-Small may exhibit general limitations common to foundation models, including hallucination (generating plausible but factually incorrect or unsupported content), occasional failures to follow instructions precisely, and degraded performance in long multi-turn conversations. As with other large-scale models trained on web-derived and synthetic data, Inkling-Small may reflect biases present in its training data, including demographic, cultural, or linguistic biases, and may perform unevenly across languages, dialects, or subject domains that were less represented during training.

Inkling-Small's knowledge is limited to information available as of its training cutoff, and it may not reflect events, developments, or changes that occurred afterward.

We recommend that downstream developers and deployers apply appropriate human oversight and review for outputs used in high-stakes or safety-critical contexts, rather than relying on Inkling-Small's outputs without verification.

- Conduct their own evaluation of Inkling-Small's performance, safety, and fairness for their specific use case, language, and population prior to deployment, particularly for applications involving vulnerable groups.
- Implement additional safeguards – such as content filtering, rate limiting, and monitoring – at the application layer, especially for open deployment contexts where Inkling-Small's built-in mitigations may not be sufficient on their own.
- Avoid deploying Inkling-Small in domains such as medical, legal, or safety-critical decision-making without additional fine-tuning, domain-specific validation, and human oversight

## 8. Legal

[Training Data Documentation](https://thinkingmachines.ai/training-data-documentation/)