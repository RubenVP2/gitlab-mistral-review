from types import SimpleNamespace
from app.domain.entities import MergeRequest
from app.usecases import review_merge_requests as usecase

class DummyGitLab:
    def __init__(self):
        self.comments = []
    def get_open_merge_requests(self):
        return [MergeRequest(id=1, project_id=1, sha="s1")]
    def get_diff(self, project_id, mr_id):
        return "good diff"
    def post_comment(self, project_id, mr_id, text):
        self.comments.append(text)

class DummyAI:
    def __init__(self):
        self.called = None
    def review_diff(self, diff):
        self.called = diff
        return "reviewed"

class DummyCache:
    def __init__(self):
        self.data = {}
    def is_up_to_date(self, mr_id, sha):
        return self.data.get(mr_id) == sha
    def update_reviewed(self, mr_id, sha):
        self.data[mr_id] = sha


def test_run_merge_request_review(monkeypatch):
    gitlab = DummyGitLab()
    ai = DummyAI()
    cache = DummyCache()
    monkeypatch.setattr(usecase, "settings", SimpleNamespace(max_tokens=100))
    usecase.run_merge_request_review(gitlab, ai, cache)
    assert ai.called == "good diff"
    assert gitlab.comments == ["reviewed"]
    assert cache.data[1] == "s1"


def test_skip_when_diff_too_large(monkeypatch):
    gitlab = DummyGitLab()
    ai = DummyAI()
    cache = DummyCache()
    monkeypatch.setattr(usecase, "settings", SimpleNamespace(max_tokens=1))
    usecase.run_merge_request_review(gitlab, ai, cache)
    assert gitlab.comments == ["Diff trop volumineux pour analyse automatique."]
