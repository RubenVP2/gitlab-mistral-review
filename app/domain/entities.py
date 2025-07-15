"""Domain entities used across the application."""

from dataclasses import dataclass


@dataclass
class MergeRequest:
    """Simple representation of a GitLab merge request."""

    id: int
    project_id: int
    sha: str
    title: str | None = None


@dataclass
class ReviewResult:
    """Result returned by the review engine."""

    text: str
