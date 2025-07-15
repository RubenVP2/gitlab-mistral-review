"""Port definition for the caching layer."""

from __future__ import annotations

from abc import ABC, abstractmethod


class CachePort(ABC):
    """Interface for the review cache."""

    @abstractmethod
    def is_up_to_date(self, mr_id: int, sha: str) -> bool:
        """Return ``True`` if the MR with given SHA has already been reviewed."""

        raise NotImplementedError

    @abstractmethod
    def update_reviewed(self, mr_id: int, sha: str) -> None:
        """Persist that the given MR/SHA has been reviewed."""

        raise NotImplementedError

