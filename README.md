# AI Content Studio for LLM Creators

Python MVP for planning and generating Instagram/TikTok content about AI, LLMs,
Python, and beginner-friendly IT learning.

The project is designed as a portfolio-ready AI tool, not just a one-off prompt.
It can start in a free template mode and later switch to Ollama or OpenAI-style
LLM APIs.

## Features

- Generate one complete content package from a topic.
- Produce a hook, short video script, carousel outline, video prompts, caption,
  hashtags, CTA, and quality notes.
- Save generated content to SQLite.
- Run locally without paid APIs.
- Keep the architecture ready for Ollama, OpenAI-compatible APIs, and a future
  Custom GPT action.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py generate --topic "LLM для новачків" --save
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py generate --topic "LLM для новачків" --save
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Generation Modes

Default free mode:

```env
AI_PROVIDER=template
```

Local Ollama mode:

```env
AI_PROVIDER=ollama
AI_MODEL=llama3.1:8b
AI_BASE_URL=http://127.0.0.1:11434/v1
AI_API_KEY=ollama
```

Future OpenAI-compatible mode:

```env
AI_PROVIDER=openai
AI_MODEL=gpt-4.1-mini
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=your_key_here
```

Do not commit `.env` or `.env.local` to GitHub.

## Example

```bash
python main.py generate \
  --topic "Що таке RAG у простих словах" \
  --audience "початківці, які хочуть перейти в IT" \
  --platform "instagram,tiktok" \
  --save
```

## Tests

Run the dependency-free smoke test:

```bash
python -m unittest discover -s tests
```

## Roadmap

- Add a FastAPI backend.
- Add a weekly content calendar.
- Add trend input from RSS or manual sources.
- Add carousel export to Markdown/Canva-ready text.
- Add quality scoring.
- Add Custom GPT action schema.
- Add official publishing integrations only after platform approvals.

## Portfolio Value

This project demonstrates Python, LLM integration, API-ready architecture,
SQLite persistence, content automation, prompt engineering, and product thinking.
