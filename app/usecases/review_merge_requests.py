"""Use case orchestrating the review of merge requests."""

from __future__ import annotations

from app.domain.services.review_engine import ReviewEngine
from app.ports.output.ai_port import AIPort
from app.ports.output.cache_port import CachePort
from app.ports.output.gitlab_port import GitLabPort
from config.settings import settings


def run_merge_request_review(gitlab: GitLabPort, ai: AIPort, cache: CachePort) -> None:
    """Fetch opened MRs and post an automated review when possible."""

    engine = ReviewEngine(ai, settings.max_tokens)

    for mr in gitlab.get_open_merge_requests():
        if cache.is_up_to_date(mr.id, mr.sha):
            continue

        diff = gitlab.get_diff(mr.id)
        review = engine.review(diff)
        if review is None:
            gitlab.post_comment(mr.id, "Diff trop volumineux pour analyse automatique.")
        else:
            gitlab.post_comment(mr.id, review)

        cache.update_reviewed(mr.id, mr.sha)

