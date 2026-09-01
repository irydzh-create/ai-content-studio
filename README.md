AI Content Studio MVP

AI Content Studio MVP is a Python project for generating structured content packs about artificial intelligence.

The project can work in two modes:

template - fast demo mode without a local AI model

ollama - local AI generation through Ollama

It also includes a Telegram bot interface, so the generator can be used as a real mini tool instead of only a terminal script.

Features

Generate a content pack from one topic

Create a short hook

Create a short video script

Create six carousel slide ideas

Create prompts for Gemini and Google Flow

Create a caption, hashtags and call to action

Run from the command line

Run through a Telegram bot

Support local generation with Ollama

Support fast template mode for stable demos

Project Structure

ai-content-studio-mvp/
├── app/
│   ├── database/
│   ├── generators/
│   ├── providers/
│   ├── config.py
│   ├── models.py
│   └── telegram_bot.py
├── tests/
├── main.py
├── requirements.txt
├── .env.example
└── README.md

Setup

Create and activate a virtual environment:

python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Create a local .env file based on .env.example.

Example:

AI_PROVIDER=template
AI_MODEL=llama3.2:latest
AI_BASE_URL=http://127.0.0.1:11434/v1
AI_API_KEY=ollama
DATABASE_PATH=content_studio.db
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

Do not commit .env to GitHub because it contains secrets.

Run From Terminal

Fast template mode:

python main.py generate --topic "What is AI in simple words"

Save the generated content pack:

python main.py generate --topic "What is AI in simple words" --save

Run With Ollama

Install and start Ollama, then make sure a local model is available:

ollama list

Example model:

llama3.2:latest

Update .env:

AI_PROVIDER=ollama
AI_MODEL=llama3.2:latest
AI_BASE_URL=http://127.0.0.1:11434/v1
AI_API_KEY=ollama

Then run:

python main.py generate --topic "What is AI in simple words"

Run Telegram Bot

Add your Telegram bot token to .env:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

Start the bot:

python -m app.telegram_bot

Open Telegram, send /start to the bot and then send a content topic.

Tests

Run tests:

python -m unittest discover -s tests

Portfolio Summary

AI Content Studio MVP is a local Python application with a Telegram interface for generating structured content packs about artificial intelligence. It supports a fast template mode for demos and an Ollama provider for local AI generation without external AI API keys.

Tech Stack

Python

Telegram Bot API

Ollama

SQLite

Git and GitHub

