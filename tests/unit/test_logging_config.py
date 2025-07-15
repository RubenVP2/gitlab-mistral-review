from types import SimpleNamespace
import logging.config

import config.logging as log_config


def test_configure_logging_with_and_without_file(monkeypatch):
    recorded = {}
    monkeypatch.setattr(log_config, "dictConfig", lambda cfg: recorded.update(cfg))

    monkeypatch.setattr(log_config, "settings", SimpleNamespace(log_level="INFO", log_file=None))
    log_config.configure_logging()
    assert "file" not in recorded["handlers"]

    monkeypatch.setattr(log_config, "settings", SimpleNamespace(log_level="DEBUG", log_file="x.log"))
    log_config.configure_logging()
    assert recorded["handlers"]["file"]["filename"] == "x.log"
