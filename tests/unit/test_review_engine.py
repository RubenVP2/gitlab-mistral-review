import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))
from app.domain.services.review_engine import ReviewEngine


class DummyAI:
    def __init__(self, reply: str):
        self.reply = reply
        self.called_with = None

    def review_diff(self, diff: str) -> str:
        self.called_with = diff
        return self.reply

def test_returns_none_when_diff_too_large():
    ai = DummyAI("ok")
    engine = ReviewEngine(ai, max_tokens=1)
    assert engine.review("word1 word2") is None
    assert ai.called_with is None

def test_returns_ai_response_when_within_limit():
    ai = DummyAI("review")
    engine = ReviewEngine(ai, max_tokens=10)
    diff = "a b c"
    assert engine.review(diff) == "review"
    assert ai.called_with == diff
