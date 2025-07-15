from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from app.domain.entities import MergeRequest


class GitLabPort(ABC):
    """Interface used to interact with GitLab."""

    @abstractmethod
    def get_open_merge_requests(self, project_id: int | None = None) -> Iterable[MergeRequest]:
        """Return currently opened merge requests.

        Args:
            project_id: restrict search to this project when provided.
        """

        raise NotImplementedError

    @abstractmethod
    def get_diff(self, project_id: int, mr_id: int) -> str:
        """Return the diff of the merge request."""

        raise NotImplementedError

    @abstractmethod
    def post_comment(self, project_id: int, mr_id: int, text: str) -> None:
        """Post a comment on the merge request."""

        raise NotImplementedError
