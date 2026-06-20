from addon_sdk_23bisnis import InMemoryNonceStore, NonceStore

# Single process-wide store. In production, swap for a Redis-backed NonceStore
# (implement the .remember(nonce, ttl_seconds) -> bool protocol).
_store: NonceStore = InMemoryNonceStore()


def get_nonce_store() -> NonceStore:
    return _store
