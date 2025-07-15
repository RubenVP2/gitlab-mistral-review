import requests
from app.adapters.gitlab_adapter import GitLabAdapter


class DummyResponse:
    def __init__(self, data, status=200, headers=None):
        self._json = data
        self.status_code = status
        self.headers = headers or {}

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("boom")


def test_get_open_merge_requests_pagination(monkeypatch):
    pages = [
        DummyResponse(
            [{"iid": 1, "project_id": 1, "sha": "a"}], headers={"X-Next-Page": "2"}
        ),
        DummyResponse([], headers={}),
    ]
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        return pages.pop(0)

    monkeypatch.setattr(requests, "request", fake_request)
    adapter = GitLabAdapter(token="t", base_url="http://x")
    mrs = list(adapter.get_open_merge_requests())
    assert len(mrs) == 1 and mrs[0].id == 1
    assert calls[0][2]["headers"]["PRIVATE-TOKEN"] == "t"
    assert calls[-1][2]["params"]["page"] == "2"


def test_get_diff_and_post_comment(monkeypatch):
    def fake_request(method, url, **kwargs):
        if method == "GET":
            return DummyResponse(
                {
                    "changes": [
                        {"new_path": "main.py", "diff": "a"},
                        {"new_path": "app.py", "diff": "b"},
                    ]
                }
            )
        assert method == "POST"
        assert kwargs["json"] == {"body": "hi"}
        return DummyResponse({}, status=201)

    monkeypatch.setattr(requests, "request", fake_request)
    adapter = GitLabAdapter(token="t", base_url="http://x")
    diff = adapter.get_diff(1, 2)
    assert diff == "main.pya\napp.pyb"
    adapter.post_comment(1, 2, "hi")
