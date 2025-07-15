import requests
from app.adapters.mistral_adapter import MistralAdapter

class DummyResponse:
    def __init__(self, data, status=200):
        self._json = data
        self.status_code = status
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("bad")


def test_review_diff_success(monkeypatch):
    def fake_post(url, json=None, headers=None):
        assert headers["Authorization"] == "Bearer k"
        return DummyResponse({"choices": [{"message": {"content": "ok"}}]})
    monkeypatch.setattr(requests, "post", fake_post)
    adapter = MistralAdapter(api_key="k", model="m")
    result = adapter.review_diff("diff")
    assert result == "ok"


def test_review_diff_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.RequestException()
    monkeypatch.setattr(requests, "post", fake_post)
    adapter = MistralAdapter(api_key="k")
    assert "Erreur" in adapter.review_diff("x")
