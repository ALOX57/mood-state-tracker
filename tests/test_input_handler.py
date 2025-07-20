from moodtracker.input_handler import get_tags

def test_get_tags_basic(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: " Happy, tired  ,  ")

    tags = get_tags()

    assert tags == ["happy", "tired"]