import time

from app.adapters.gitlab_adapter import GitLabAdapter
from app.adapters.mistral_adapter import MistralAdapter
from app.adapters.cache_adapter import JSONCacheAdapter
from app.usecases.review_merge_requests import run_merge_request_review
from app.scheduler.polling import start_scheduler, stop_scheduler
from config.settings import settings
from config.logging import configure_logging


def main():
    """Main entry point for the application."""
    configure_logging()
    gitlab = GitLabAdapter(token=settings.gitlab_token, base_url=settings.gitlab_url)
    ai = MistralAdapter(api_key=settings.mistral_api_key, model=settings.mistral_model)
    cache = JSONCacheAdapter(cache_file=settings.cache_file)

    start_scheduler(
        lambda: run_merge_request_review(gitlab, ai, cache, project_id=settings.project_id),
        settings.polling_interval,
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_scheduler()


if __name__ == "__main__":
    main()
