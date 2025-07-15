from __future__ import annotations

import logging
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler


_scheduler: BackgroundScheduler | None = None
logger = logging.getLogger("Scheduler")


def start_scheduler(task: Callable[[], None], interval: int) -> None:
    """
    Start the background scheduler with the given task and interval.

    Args:
        task (Callable[[], None]): The task to run periodically.
        interval (int): The interval in seconds at which to run the task.
    """
    global _scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, "interval", seconds=interval)
    task()
    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler démarré (intervalle=%ss)", interval)


def stop_scheduler() -> None:
    """Stop the background scheduler if it is running."""
    global _scheduler
    if _scheduler:
        _scheduler.shutdown()
        _scheduler = None
        logger.info("Scheduler arrêté")
    else:
        logger.warning("Aucun scheduler en cours d'exécution à arrêter")
