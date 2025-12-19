# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    """Struktur data untuk Produk."""
    id: str
    name: str
    price: float

@dataclass
class CartItem:
    """Struktur data untuk item dalam keranjang."""
    product: Product
    quantity: int

    @property
    def subtotal(self) -> float:
        """Menghitung subtotal untuk item ini."""
        return self.product.price * self.quantity