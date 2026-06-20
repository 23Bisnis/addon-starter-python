"""Catalog + product-mapping interface. A real addon pulls an upstream catalog
('tarik produk') and stores product mappings here. Empty in the starter."""


def list_catalog(install_id: int) -> list[dict]:
    return []


def resolve_sku(install_id: int, sku: str) -> dict | None:
    """Translate the per-supplier sku into upstream identifiers. None = unmapped."""
    return None
