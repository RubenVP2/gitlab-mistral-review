import json
from app.adapters.cache_adapter import JSONCacheAdapter


def test_update_and_check(tmp_path):
    cache_file = tmp_path / "cache.json"
    cache = JSONCacheAdapter(str(cache_file))
    assert not cache.is_up_to_date(1, "a1")
    cache.update_reviewed(1, "a1")
    assert cache.is_up_to_date(1, "a1")
    assert not cache.is_up_to_date(1, "b2")


def test_load_invalid_file(tmp_path):
    cache_file = tmp_path / "cache.json"
    cache_file.write_text("[]")
    cache = JSONCacheAdapter(str(cache_file))
    assert cache.is_up_to_date(2, "x") is False
    cache.update_reviewed(2, "x")
    data = json.loads(cache_file.read_text())
    assert data == {"2": "x"}
