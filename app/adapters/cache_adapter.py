"""JSON based cache adapter implementation."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

from app.ports.output.cache_port import CachePort


class JSONCacheAdapter(CachePort):
    """Persist reviewed merge requests into a JSON file."""

    def __init__(self, cache_file: str) -> None:
        self.path = Path(cache_file)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")
        self.logger = logging.getLogger(self.__class__.__name__)

    def _load(self) -> Dict[str, str]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        return {str(k): str(v) for k, v in data.items()}

    def _save(self, data: Dict[str, str]) -> None:
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def is_up_to_date(self, mr_id: int, sha: str) -> bool:
        data = self._load()
        result = data.get(str(mr_id)) == sha
        self.logger.debug("MR %s up to date: %s", mr_id, result)
        return result

    def update_reviewed(self, mr_id: int, sha: str) -> None:
        data = self._load()
        data[str(mr_id)] = sha
        self._save(data)
        self.logger.debug("Cache mis \u00e0 jour pour MR %s", mr_id)

