"""Interaction with the GitLab REST API."""

from __future__ import annotations

import json
import logging
import urllib.request
from typing import Iterable, List

from app.domain.entities import MergeRequest
from app.ports.output.gitlab_port import GitLabPort


class GitLabAdapter(GitLabPort):
    """Basic GitLab API client using the standard library."""

    def __init__(self, token: str, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.logger = logging.getLogger(self.__class__.__name__)

    # internal helper
    def _request(self, method: str, url: str, data: bytes | None = None) -> any:
        self.logger.debug("%s %s", method, url)
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("PRIVATE-TOKEN", self.token)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)

    def get_open_merge_requests(self) -> Iterable[MergeRequest]:
        url = f"{self.base_url}/merge_requests?state=opened"
        mrs = self._request("GET", url)
        results: List[MergeRequest] = []
        for mr in mrs:
            results.append(
                MergeRequest(
                    id=mr["iid"],
                    project_id=mr["project_id"],
                    sha=mr["sha"],
                    title=mr.get("title"),
                )
            )
        self.logger.info("%d merge requests ouvertes trouvées", len(results))
        return results

    def get_diff(self, project_id: int, mr_id: int) -> str:
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_id}/changes"
        changes = self._request("GET", url)
        self.logger.debug("Diff récupéré pour MR %s", mr_id)
        return "\n".join(
            c.get("new_path") + c.get("diff", "") for c in changes.get("changes", [])
        )

    def post_comment(self, project_id: int, mr_id: int, text: str) -> None:
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_id}/notes"
        payload = json.dumps({"body": text}).encode()
        self._request("POST", url, data=payload)
        self.logger.debug("Commentaire post\u00e9 sur MR %s", mr_id)
