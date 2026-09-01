from __future__ import annotations

import json
import urllib.error
import urllib.request

from app.providers.base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout: int = 120,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": 0.2,
            "max_tokens": 800,
            "stream": False,
        }
        request = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                response_body = response.read().decode("utf-8")
                data = json.loads(response_body)

        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")

            raise RuntimeError(
                f"сервер Ollama вернул HTTP {error.code}: {details}"
            ) from error

        except urllib.error.URLError as error:
            raise RuntimeError(
                f"не удалось подключиться к Ollama: {error.reason}"
            ) from error

        except TimeoutError as error:
            raise RuntimeError(
                "Ollama не ответил за установленное время"
            ) from error

        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Ollama вернул некорректный JSON"
            ) from error

        try:
            return data["choices"][0]["message"]["content"]

        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(
                "ответ Ollama не содержит сгенерированный текст"
            ) from error