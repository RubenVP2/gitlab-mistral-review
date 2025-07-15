"""Very small polling scheduler."""

from __future__ import annotations

import threading
import time
from typing import Callable


def start_scheduler(task: Callable[[], None], interval: int) -> None:
    """Run ``task`` every ``interval`` seconds in a background thread."""

    def loop() -> None:
        while True:
            task()
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    # Keep the main thread alive
    thread.join()

