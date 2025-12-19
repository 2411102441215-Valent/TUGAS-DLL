from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# ====================
# KONFIGURASI LOGGING
# ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)
LOGGER = logging.getLogger("CheckoutService")


# ============
# MODEL DATA
# ============
@dataclass
class Order:
    """
    Merepresentasikan data pesanan pelanggan.

    Attributes:
        customer_name (str): Nama pelanggan.
        total_price (float): Total harga pesanan.
        status (str): Status pesanan.
    """
    customer_name: str
    total_price: float
    status: str = "open"


# =============================
# KODE BURUK (SEBELUM REFACTOR)
# =============================
class OrderManager:
    """
    Class lama yang menangani checkout secara langsung
    dan melanggar prinsip SRP, OCP, dan DIP.
    """

    def process_checkout(self, order: Order, payment_method: str) -> bool:
        """
        Memproses checkout menggunakan metode pembayaran tertentu.

        Args:
            order (Order): Data pesanan.
            payment_method (str): Metode pembayaran.

        Returns:
            bool: True jika berhasil, False jika gagal.
        """
        print(f"Memulai checkout untuk {order.customer_name}...")
        print("Metode pembayaran diproses secara hardcoded.")
        order.status = "paid"
        return True


# ====================
# ABSTRAKSI / KONTRAK
# ====================
class IPaymentProcessor(ABC):
    """
    Interface untuk memproses pembayaran.
    """

    @abstractmethod
    def process(self, order: Order) -> bool:
        """
        Memproses pembayaran pesanan.

        Args:
            order (Order): Data pesanan.

        Returns:
            bool: True jika pembayaran berhasil.
        """
        pass


class INotificationService(ABC):
    """
    Interface untuk layanan notifikasi.
    """

    @abstractmethod
    def send(self, order: Order) -> None:
        """
        Mengirim notifikasi kepada pelanggan.

        Args:
            order (Order): Data pesanan.
        """
        pass


# =====================
# IMPLEMENTASI KONKRIT
# =====================
class CreditCardProcessor(IPaymentProcessor):
    """
    Implementasi pembayaran menggunakan kartu kredit.
    """

    def process(self, order: Order) -> bool:
        """
        Memproses pembayaran dengan kartu kredit.

        Args:
            order (Order): Data pesanan.

        Returns:
            bool: True jika berhasil.
        """
        LOGGER.info("Memproses pembayaran menggunakan kartu kredit")
        return True


class EmailNotifier(INotificationService):
    """
    Implementasi notifikasi melalui email.
    """

    def send(self, order: Order) -> None:
        """
        Mengirim email konfirmasi pembayaran.

        Args:
            order (Order): Data pesanan.
        """
        LOGGER.info(f"Mengirim email ke {order.customer_name}")


# ========================
# KOORDINATOR (SRP + DIP)
# ========================
class CheckoutService:
    """
    Service untuk mengoordinasikan proses checkout.

    Class ini mengatur alur pembayaran dan notifikasi
    dengan menerapkan Dependency Injection.
    """

    def __init__(
        self,
        payment_processor: IPaymentProcessor,
        notifier: INotificationService
    ):
        """
        Inisialisasi CheckoutService.

        Args:
            payment_processor (IPaymentProcessor): Metode pembayaran.
            notifier (INotificationService): Layanan notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """
        Menjalankan proses checkout pesanan.

        Args:
            order (Order): Data pesanan.

        Returns:
            bool: True jika checkout berhasil, False jika gagal.
        """
        LOGGER.info(
            f"Memulai checkout untuk {order.customer_name} "
            f"dengan total {order.total_price}")

        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            LOGGER.info("Checkout berhasil, status PAID")
            return True
        else :
            LOGGER.warning("Checkout gagal, pembayaran tidak berhasil")
            return False


# ==============
# PROGRAM UTAMA
# ==============
if __name__ == "__main__":
    order = Order("Andi", 500000)
    payment = CreditCardProcessor()
    notifier = EmailNotifier()

    service = CheckoutService(payment, notifier)
    service.run_checkout(order)
