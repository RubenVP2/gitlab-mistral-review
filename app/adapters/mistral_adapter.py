"""Very small client for the Mistral API (or compatible)."""

from __future__ import annotations

import json
import urllib.request

from app.ports.output.ai_port import AIPort


class MistralAdapter(AIPort):
    """Send review requests to Mistral AI."""

    def __init__(self, api_key: str, model: str = "mistral-7b") -> None:
        self.api_key = api_key
        self.model = model
        self.url = "https://api.mistral.ai/v1/chat/completions"

    def review_diff(self, diff: str) -> str:
        prompt = (
            "Please review the following Git diff and provide suggestions:\n" + diff
        )
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(self.url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.load(resp)
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception:
            # Fallback in case of network issues
            return "AI review could not be generated." 

