"""Business logic used to generate merge request reviews."""

from __future__ import annotations

from typing import Optional

from app.ports.output.ai_port import AIPort


class ReviewEngine:
    """Generate reviews while taking token limits into account."""

    def __init__(self, ai: AIPort, max_tokens: int) -> None:
        self.ai = ai
        self.max_tokens = max_tokens

    def _estimate_tokens(self, text: str) -> int:
        """Naive token estimation based on word count."""

        return len(text.split())

    def review(self, diff: str) -> Optional[str]:
        """Return a review text or ``None`` if the diff is too large."""

        if self._estimate_tokens(diff) > self.max_tokens:
            return None
        return self.ai.review_diff(diff)

