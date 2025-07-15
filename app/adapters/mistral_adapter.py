"""Very small client for the Mistral API (or compatible)."""

from __future__ import annotations

import json
import logging
import urllib.request

from app.ports.output.ai_port import AIPort
from config.prompt import PROMPT_IA


class MistralAdapter(AIPort):
    """Send review requests to Mistral AI."""

    def __init__(self, api_key: str, model: str = "devstral-medium-2507") -> None:
        self.api_key = api_key
        self.model = model
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.logger = logging.getLogger(self.__class__.__name__)

    def review_diff(self, diff: str) -> str:
        prompt = PROMPT_IA.replace("{GIT_DIFF_ICI}", diff)
        payload = {
            "model": self.model,
            "prompt_mode": "reasoning",
            "messages": [{"role": "user", "content": prompt}],
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(self.url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.load(resp)
            review = (
                result.get("choices", [{}])[0].get("message", {}).get("content", "")
            )
            self.logger.debug(f"Réponse Mistral reçue : {review}")
            return review
        except Exception:
            self.logger.exception("Erreur lors de l'appel à Mistral")
            return "Erreur de communication avec Mistral."
