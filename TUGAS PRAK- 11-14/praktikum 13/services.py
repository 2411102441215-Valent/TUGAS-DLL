# services.py
from abc import ABC, abstractmethod
import logging
from models import Product, CartItem 
from typing import List

LOGGER = logging.getLogger('SERVICES')

# --- INTERFACE PEMBAYARAN (Diperlukan untuk DIP/OCP) ---
class IPaymentProcessor(ABC):
    """Kontrak untuk semua metode pembayaran."""
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

# --- IMPLEMENTASI PEMBAYARAN TUNAI ---
class CashPayment(IPaymentProcessor):
    """Logika pembayaran tunai."""
    def process(self, amount: float) -> bool:
        LOGGER.info(f"Menerima TUNAI sejumlah: Rp{amount:,.0f}")
        return True

# --- IMPLEMENTASI PEMBAYARAN DEBIT BARU (Pembuktian OCP) ---
class DebitCardPayment(IPaymentProcessor):
    """Implementasi pembayaran menggunakan kartu debit."""
    def process(self, amount: float) -> bool:
        LOGGER.info(f"Memproses pembayaran DEBIT sejumlah: Rp{amount:,.0f}")
        # Simulasi berhasil
        return True   


# --- SERVICE KERANJANG BELANJA (Logika Inti Bisnis & SRP) ---
class ShoppingCart:
    """Mengelola item, kuantitas, dan total harga pesanan (SRP)."""
    def __init__(self):
        self._items: dict[str, CartItem] = {}

    def add_item(self, product: Product, quantity: int = 1):
        if product.id in self._items:
            self._items[product.id].quantity += quantity
        else:
            self._items[product.id] = CartItem(product=product, quantity=quantity)
            LOGGER.info(f"Added {quantity}x {product.name} to cart.")

    def get_items(self) -> list[CartItem]:
        """Mengembalikan daftar item di keranjang."""
        return list(self._items.values())

    @property
    def total_price(self) -> float:
        """Menghitung total harga seluruh item di keranjang."""
        return sum(item.subtotal for item in self._items.values())
    
class EWalletPayment(IPaymentProcessor):
    """
    Implementasi pembayaran menggunakan E-Wallet.
    Digunakan sebagai inovasi metode pembayaran pada Praktikum 13.
    """
    def process(self, amount: float) -> bool:
        print("Payment: Memproses pembayaran via E-Wallet.")

        # Simulasi saldo e-wallet
        wallet_balance = 1_000_000

        if wallet_balance >= amount:
            print("Payment: Saldo E-Wallet mencukupi.")
            return True
        else:
            print("Payment: Saldo E-Wallet tidak mencukupi.")
            return False
