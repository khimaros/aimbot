---
license: other
license_name: test
license_link: LICENSE
language:
- en
- fr
- de
- es
- pt
metrics:
- accuracy
- cer
pipeline_tag: automatic-speech-recognition
homepage: https://kroko.ai/
---

# Welcome to Kroko 👋

## **Open-source speech recognition built for developers.**
>
> Our engine is fully open-source, and you choose how to deploy models: use our **CC-BY-SA licensed community models** or upgrade to **commercial models** with premium performance. We focus on building **fast, high-quality production models** and providing **examples that take the guesswork out** of integration.

## Why Kroko ASR?

- ⚡ **Fast & lightweight** – optimized Zipformer models (Whisper and parakeet style coming).
- 🧩 **Flexible licensing** – use **fully open-source CC-BY-SA community models** or integrate **commercial/OEM models** for premium accuracy.
- 🌍 **Runs anywhere** – cross-platform and with support for many programming languages.
- 📱 **Mobile & web ready** – works on Android, (iOS coming soon) in the browser via WASM, and with WebSockets for streaming.
- 🧰 **Production focus** – we prioritize real-world performance, stability, and examples.
- 🤝 **Customizable** – bring your own model, fine-tune for domain-specific vocabularies, or commission us.

> Our mission: **fast, high-quality ASR with licensing that works for both open-source and closed-source projects.**

## Demos

### ▶️ Android App
Run speech recognition **natively on your phone** using ONNX Runtime.
- [Kroko ASR Model Explorer](https://play.google.com/store/apps/details?id=com.krokoasr.demo&hl=en)

### 🌐 Browser (WASM)
Experience transcription **directly in your browser**, no server required.
- [Hugging Face Spaces Demo](https://huggingface.co/spaces/Banafo/Kroko-Streaming-ASR-Wasm)

## Models

Kroko ASR follows a **unique dual-model strategy**:

### 1. Community Models (free, open-source)

- Licensed under **CC-BY-SA**.
- Low-latency, lightweight models.
- Perfect for hobby projects, research, or free tiers.
- Faster and smaller than Whisper/Parakeet in many scenarios.

### 2. Commercial & OEM Models

- Premium accuracy and robustness.
- Licensed for professional and production products.
- Designed for SaaS, dev tools, and enterprise integration.

### 3. Bring, Train, or Commission Your Own

- **DIY:** Use our training guides to build and distribute your own models.
- **Professional services:** Work with us to create fine-tuned models for accents, jargon, or specialized domains.

> This gives you **full freedom**: start free, scale commercially, or roll your own.

## Our Community

Join the Kroko community to learn, share, and contribute:

- 💬 **[Discord](https://discord.gg/JT7wdtnK79)** – chat with developers, ask questions, and share projects.  
- 📢 **[Reddit](https://www.reddit.com/r/kroko_ai/)** – join discussions, showcase your integrations, and follow updates.
- 🤗 **[Hugging Face](https://huggingface.co/Banafo/Kroko-ASR)** – explore our models, try live demos, and contribute feedback.

## Contributing

PRs welcome! Run `ruff`, `black`, and `pytest` before submitting.

---

## License

Apache-2.0 engine. Models licensed separately (CC-BY-SA community or commercial OEM).

---

## Credits

Kroko ASR is built on top of [**Sherpa-ONNX**](https://k2-fsa.github.io/sherpa/).

⚠️ **Note:** Kroko ASR is an independent project and is **not affiliated with Sherpa-ONNX**. We build on their excellent open-source engine, but our models, demos, and packaging are developed and maintained separately.

---
