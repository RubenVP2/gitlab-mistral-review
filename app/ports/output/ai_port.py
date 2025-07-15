"""Port definition for AI engines."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIPort(ABC):
    """Interface for AI providers used by the review engine."""

    @abstractmethod
    def review_diff(self, diff: str) -> str:
        """Return a textual review for the given diff."""

        raise NotImplementedError

