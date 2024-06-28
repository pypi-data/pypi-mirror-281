# Easy Letters

[![PyPI version](https://badge.fury.io/py/easy-letters.svg)](https://badge.fury.io/py/easy-letters)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/easy-letters)](https://pepy.tech/project/easy-letters)
[![Tests](https://github.com/habedi/easy-letters/actions/workflows/tests.yml/badge.svg)](https://github.com/habedi/easy-letters/actions/workflows/tests.yml)
[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red.svg)](https://github.com/habedi/easy-letters)

Easy Letters is a Python package to help job seekers writing application letters. It uses a simple retrieval
augmented generation (RAG) pipeline to generate the letters. The user can then edit the draft letter to suit their
needs.

## Installation

You can install Easy Letters using pip:

```bash
pip install easy-letters
```

## Getting Started

### API Key Setup

At the moment, Easy Letters retrieves the API keys from the environment variables.
You need to set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Sample Notebooks

You can find Jupyter notebooks with example code in the [`notebook`](notebooks) directory.
The notebooks demonstrate how to use Easy Letters to generate application letter drafts.

## TODO

- [ ] Add support for Anthropic models and API
- [ ] Add support for locally served models via Ollama
