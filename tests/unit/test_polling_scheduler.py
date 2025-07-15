from types import SimpleNamespace
import builtins

import app.scheduler.polling as polling


class DummyScheduler:
    def __init__(self):
        self.started = False
        self.jobs = []
        self.shutdown_called = False

    def add_job(self, func, trigger, seconds):
        self.jobs.append((func, trigger, seconds))

    def start(self):
        self.started = True

    def shutdown(self):
        self.shutdown_called = True


def test_start_and_stop_scheduler(monkeypatch):
    dummy = DummyScheduler()
    monkeypatch.setattr(polling, "BackgroundScheduler", lambda: dummy)

    called = []

    def task():
        called.append(True)

    polling.start_scheduler(task, interval=5)
    assert dummy.started
    assert dummy.jobs[0][1] == "interval" and dummy.jobs[0][2] == 5
    assert polling._scheduler is dummy

    polling.stop_scheduler()
    assert dummy.shutdown_called
    assert polling._scheduler is None
