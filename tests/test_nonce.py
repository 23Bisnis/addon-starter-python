from app.nonce import get_nonce_store


def test_nonce_first_seen_then_replay():
    store = get_nonce_store()
    assert store.remember("abc", 600) is True   # fresh
    assert store.remember("abc", 600) is False  # replay
