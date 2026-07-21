# Soma Website AI

The official AI website guide for Soma Education Technologies.

This API uses a Groq-hosted Llama model to explain Soma, answer questions in English or Shona, and help Zimbabwean schools understand the platform.

## Endpoints

- `GET /` — service information
- `GET /health` — service health check
- `POST /api/chat` — talk to Soma Guide

## Required environment variable

`GROQ_API_KEY`

## Render commands

Build:

```text
pip install -r requirements.txt
vicorn main:app --host 0.0.0.0 --port $PORT

3. Click **Commit changes…**
4. Use:

```text
docs: update project README
