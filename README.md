<p align="center"><img src="assets/banner.svg" alt="Llama Server Preflight — Check a llama.cpp server health endpoint and verify the expected model is exposed." width="100%"></p>

# Llama Server Preflight ✨

> Check a llama.cpp server health endpoint and verify the expected model is exposed.

[![CI](https://github.com/MofidChallenge10/llama-server-preflight/actions/workflows/ci.yml/badge.svg)](https://github.com/MofidChallenge10/llama-server-preflight/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) ![Stack](https://img.shields.io/badge/Stack-Python%20stdlib-informational)

## 🎯 Why this project?

Check a llama.cpp server health endpoint and verify the expected model is exposed. It focuses on a narrow operational problem and keeps its output inspectable, deterministic, and suitable for scripts or CI.

## 🚀 Features

- 🧭 Solves the documented use case without a hosted service.
- 🧪 Includes repeatable tests and a runnable example.
- 📄 Supports concise human-readable output; machine-readable output is available where documented.
- 🔒 Avoids changing the target system during inspection.

## ⚡ Quick Start

```bash
python -m pip install -e .
python -m llama_server_preflight --base-url http://127.0.0.1:8080 --model my-model
```

## 🖥️ Example

```text
READY  http://127.0.0.1:8080
Health: HTTP 200
Models: my-model
Expected model: available
```

## 🗺️ Roadmap

- Add optional latency thresholds for health and model-list requests.
- Add a shell completion file.
- Add a CI example that gates deployment on preflight status.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports should include the command, a minimal input fixture, and the observed output. Please do not attach credentials or private production data.

## 📜 License

MIT — see [LICENSE](LICENSE).
