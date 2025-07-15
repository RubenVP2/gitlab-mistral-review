import sys
from pathlib import Path
from types import SimpleNamespace

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Stub modules when missing
if 'requests' not in sys.modules:
    sys.modules['requests'] = SimpleNamespace(
        request=lambda *a, **k: (_ for _ in ()).throw(ImportError("requests")),
        post=lambda *a, **k: (_ for _ in ()).throw(ImportError("requests")),
        HTTPError=Exception,
        RequestException=Exception,
    )

if 'filelock' not in sys.modules:
    class FileLock:
        def __init__(self, *a, **k):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            pass
    sys.modules['filelock'] = SimpleNamespace(FileLock=FileLock)

if 'pydantic_settings' not in sys.modules:
    class BaseSettings:
        def __init__(self, **values):
            for k, v in values.items():
                setattr(self, k, v)
    sys.modules['pydantic_settings'] = SimpleNamespace(BaseSettings=BaseSettings)

if 'apscheduler.schedulers.background' not in sys.modules:
    class BackgroundScheduler:
        def __init__(self):
            pass
        def add_job(self, *a, **k):
            pass
        def start(self):
            pass
        def shutdown(self):
            pass
    sys.modules['apscheduler.schedulers.background'] = SimpleNamespace(BackgroundScheduler=BackgroundScheduler)

if 'pydantic' not in sys.modules:
    def Field(default=None, env=None):
        return default
    sys.modules['pydantic'] = SimpleNamespace(Field=Field)
