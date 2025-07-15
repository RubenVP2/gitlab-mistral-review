from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict

from filelock import FileLock

from app.ports.output.cache_port import CachePort


class JSONCacheAdapter(CachePort):
    """Persist reviewed merge requests into a JSON file."""

    def __init__(self, cache_file: str) -> None:
        self.path = Path(cache_file)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")
        self.lock = FileLock(str(self.path) + ".lock")
        self.logger = logging.getLogger(self.__class__.__name__)

    def _load(self) -> Dict[str, str]:
        """
        Load the cache from the JSON file.

        Returns:
            Dict[str, str]: A dictionary mapping merge request IDs to their SHA values.
        """
        with self.lock:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        return {str(k): str(v) for k, v in data.items()}

    def _save(self, data: Dict[str, str]) -> None:
        """
        Save the cache to the JSON file.

        Args:
            data (Dict[str, str]): A dictionary mapping merge request IDs to their SHA values.
        """
        with self.lock:
            self.path.write_text(json.dumps(data), encoding="utf-8")

    def is_up_to_date(self, mr_id: int, sha: str) -> bool:
        """
        Check if the merge request is up to date in the cache.

        Args:
            mr_id (int): The ID of the merge request.
            sha (str): The SHA of the merge request.

        Returns:
            bool: True if the merge request is up to date, False otherwise.
        """
        data = self._load()
        result = data.get(str(mr_id)) == sha
        self.logger.debug("MR %s up to date: %s", mr_id, result)
        return result

    def update_reviewed(self, mr_id: int, sha: str) -> None:
        """
        Update the cache with the reviewed merge request.

        Args:
            mr_id (int): The ID of the merge request.
            sha (str): The SHA of the merge request.
        """
        data = self._load()
        data[str(mr_id)] = sha
        self._save(data)
        self.logger.debug("Cache mis à jour pour MR %s", mr_id)
