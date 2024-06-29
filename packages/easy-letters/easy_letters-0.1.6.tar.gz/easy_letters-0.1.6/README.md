# Easy Letters

[![Tests](https://github.com/habedi/easy-letters/actions/workflows/tests.yml/badge.svg)](https://github.com/habedi/easy-letters/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/easy-letters.svg)](https://badge.fury.io/py/easy-letters)
[![Downloads](https://pepy.tech/badge/easy-letters)](https://pepy.tech/project/easy-letters)

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

At the moment, Easy Letters gets the API key for supported services from the environment variables.
So you need to set the following environment variables to be able to use Easy Letters:

- `OPENAI_API_KEY`: The OpenAI API key (required)

### Sample Notebooks

You can find Jupyter notebooks with example code in the `notebooks` directory.
The notebooks demonstrate how to use Easy Letters to generate application letter drafts.

### Supported Models

Easy Letters currently supports the following models:

| Model                            | Type            |
|----------------------------------|-----------------|
| GPT-3.5 Turbo                    | Text Generation |
| GPT-4o                           | Text Generation |
| Text Embedding 3 (Small Variant) | Text Embedding  |
| Text Embedding 3 (Large Variant) | Text Embedding  |

## TODO

- [ ] Add support for Anthropic models and API
- [ ] Add support for locally served models via Ollama
