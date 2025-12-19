from abc import ABC, abstractmethod
from dataclasses import dataclass

#  MODEL SEDERHANA
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

#  KODE BURUK (SEBELUM REFACTOR) – Melanggar SOLID
class OrderManager:
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")

        # LOGIKA PEMBAYARAN (Hardcoded)
        if payment_method == "credit_card":
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False

        # LOGIKA NOTIFIKASI (Hardcoded)
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"

        return True


#  REFACTOR: SOLID (SRP, OCP, DIP)

# --- ABSTRAKSI / KONTRAK (OCP & DIP) ---
class IPaymentProcessor(ABC):
    """Kontrak: Semua metode pembayaran wajib punya method process()."""
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    """Kontrak: Semua layanan notifikasi wajib punya method send()."""
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT (Plug-in) ---
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KOORDINATOR (SRP + DIP) ---
class CheckoutService:
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            print("Checkout Sukses.")
            return True

        return False


#  PROGRAM UTAMA (Pembuktian OCP)

# Setup awal
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 1. Implementasi 1 — Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)

print("\n--- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)


# 2. Pembuktian OCP — Tambah QRIS tanpa mengubah kode lain
class QrisProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS.")
        return True


budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# inject implmentasi QRIS yang baru dibuat
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)
