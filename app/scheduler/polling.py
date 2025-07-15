"""Very small polling scheduler."""

from __future__ import annotations

import logging
import threading
import time
from typing import Callable


def start_scheduler(task: Callable[[], None], interval: int) -> None:
    """Run ``task`` every ``interval`` seconds in a background thread."""
    logger = logging.getLogger("Scheduler")

    def loop() -> None:
        while True:
            logger.debug("Exécution planifiée")
            task()
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    logger.info("Scheduler démarré (intervalle=%ss)", interval)
    thread.start()
    # Keep the main thread alive
    thread.join()

