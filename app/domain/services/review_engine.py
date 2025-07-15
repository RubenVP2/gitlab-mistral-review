"""Business logic used to generate merge request reviews."""

from __future__ import annotations

from typing import Optional

import logging
from app.ports.output.ai_port import AIPort


class ReviewEngine:
    """Generate reviews while taking token limits into account."""

    def __init__(self, ai: AIPort, max_tokens: int) -> None:
        self.ai = ai
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(self.__class__.__name__)

    def _estimate_tokens(self, text: str) -> int:
        """Naive token estimation based on word count."""

        return len(text.split())

    def review(self, diff: str) -> Optional[str]:
        """Return a review text or ``None`` if the diff is too large."""

        if self._estimate_tokens(diff) > self.max_tokens:
            self.logger.info("Diff trop volumineux pour analyse")
            return None
        self.logger.debug("Analyse du diff (%d tokens)" % self._estimate_tokens(diff))
        return self.ai.review_diff(diff)

