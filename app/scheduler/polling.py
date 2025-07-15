"""Very small polling scheduler."""

from __future__ import annotations

import logging
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler


_scheduler: BackgroundScheduler | None = None


def start_scheduler(task: Callable[[], None], interval: int) -> None:
    """Run ``task`` every ``interval`` seconds using APScheduler."""
    global _scheduler
    logger = logging.getLogger("Scheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, "interval", seconds=interval)
    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler démarré (intervalle=%ss)", interval)


def stop_scheduler() -> None:
    """Stop the running scheduler if any."""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None

