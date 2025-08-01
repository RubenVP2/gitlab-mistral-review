"""Use case orchestrating the review of merge requests."""

from __future__ import annotations

import logging
from app.domain.services.review_engine import ReviewEngine
from app.ports.output.ai_port import AIPort
from app.ports.output.cache_port import CachePort
from app.ports.output.gitlab_port import GitLabPort
from config.settings import settings


def run_merge_request_review(
    gitlab: GitLabPort, ai: AIPort, cache: CachePort, project_id: int | None = None
) -> None:
    """Fetch opened MRs and post an automated review when possible."""
    logger = logging.getLogger("Review")
    engine = ReviewEngine(ai, settings.max_tokens)

    for mr in gitlab.get_open_merge_requests(project_id=project_id):
        if cache.is_up_to_date(mr.id, mr.sha):
            logger.debug("MR %s déjà analysée", mr.id)
            continue

        diff = gitlab.get_diff(mr.project_id, mr.id)
        review = engine.review(diff)
        if review is None:
            gitlab.post_comment(
                mr.project_id, mr.id, "Diff trop volumineux pour analyse automatique."
            )
        else:
            gitlab.post_comment(mr.project_id, mr.id, review)

        cache.update_reviewed(mr.id, mr.sha)
        logger.info("MR %s analysée", mr.id)
