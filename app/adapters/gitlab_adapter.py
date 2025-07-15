from __future__ import annotations

import logging
from typing import Iterable, List

import requests

from app.domain.entities import MergeRequest
from app.ports.output.gitlab_port import GitLabPort


class GitLabAdapter(GitLabPort):
    """Basic GitLab API client using the standard library."""

    def __init__(self, token: str, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.logger = logging.getLogger(self.__class__.__name__)

    def _request(self, method: str, url: str, **kwargs) -> tuple[any, dict]:
        """
        Make an HTTP request to the GitLab API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            url (str): URL to send the request to
            **kwargs: Additional keyword arguments for the request

        Returns:
            tuple[any, dict]: The response data and headers.
        """
        self.logger.debug("%s %s %s", method, url, kwargs.get("params", {}))
        headers = kwargs.setdefault("headers", {})
        headers["PRIVATE-TOKEN"] = self.token
        if "json" in kwargs:
            headers.setdefault("Content-Type", "application/json")
        resp = requests.request(method, url, **kwargs)
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            self.logger.error("HTTP error: %s", exc)
            raise
        return resp.json(), resp.headers

    def get_open_merge_requests(self) -> Iterable[MergeRequest]:
        """
        Retrieve all open merge requests from GitLab.

        Returns:
            Iterable[MergeRequest]: An iterable of MergeRequest objects representing open merge requests.
        """
        url = f"{self.base_url}/merge_requests"
        params = {"state": "opened", "per_page": 100, "page": 1}
        results: List[MergeRequest] = []
        while True:
            data, headers = self._request("GET", url, params=params)
            for mr in data:
                results.append(
                    MergeRequest(
                        id=mr["iid"],
                        project_id=mr["project_id"],
                        sha=mr["sha"],
                        title=mr.get("title"),
                    )
                )
            next_page = headers.get("X-Next-Page")
            if not next_page:
                break
            params["page"] = next_page
        self.logger.info("%d merge requests ouvertes trouvées", len(results))
        return results

    def get_diff(self, project_id: int, mr_id: int) -> str:
        """
        Retrieve the diff for a specific merge request.

        Args:
            project_id (int): _Description of the project ID_
            mr_id (int): _ID of the merge request_

        Returns:
            str: The diff as a string containing the changes made in the merge request.
        """
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_id}/changes"
        changes, _ = self._request("GET", url)
        self.logger.debug("Diff récupéré pour MR %s", mr_id)
        return "\n".join(
            c.get("new_path") + c.get("diff", "") for c in changes.get("changes", [])
        )

    def post_comment(self, project_id: int, mr_id: int, text: str) -> None:
        """
        Post a comment on a merge request.

        Args:
            project_id (int): _Description of the project ID_
            mr_id (int): _ID of the merge request_
            text (str): The text of the comment to post.
        """
        url = f"{self.base_url}/projects/{project_id}/merge_requests/{mr_id}/notes"
        payload = {"body": text}
        self._request("POST", url, json=payload)
        self.logger.debug("Commentaire posté sur MR %s", mr_id)
