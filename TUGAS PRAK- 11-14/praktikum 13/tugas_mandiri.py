# main_app.py
import logging
from repositories import ProductRepository
from services import IPaymentProcessor, ShoppingCart, CashPayment, DebitCardPayment, EWalletPayment
from models import Product

LOGGER = logging.getLogger('MAIN_APP')

class PosApp:
    """Kelas Orchestrator (Aplikasi Utama). Hanya mengkoordinasi flow dan menerapkan DI."""
    def __init__(self, repository: ProductRepository, payment_processor: IPaymentProcessor):
        # Dependency Injection (DI)
        self.repository = repository
        self.payment_processor = payment_processor
        self.cart = ShoppingCart()
        LOGGER.info("PosApp Application Initialized.")

    def _display_menu(self):
        """Menampilkan daftar produk."""
        LOGGER.info("\n--- DAFTAR PRODUK ---")
        for p in self.repository.get_all():
            LOGGER.info(f"[{p.id}] {p.name} - Rp{p.price:,.0f}")

    def _handle_add_item(self):
        """Menangani input untuk menambahkan item ke keranjang."""
        product_id = input("Masukkan ID Produk: ").strip().upper()
        product = self.repository.get_by_id(product_id)

        if not product:
            LOGGER.warning(f"Produk ID '{product_id}' tidak ditemukan.")
            return

        try:
            quantity_input = input("Jumlah (default 1): ")
            quantity = int(quantity_input) if quantity_input else 1
            if quantity <= 0:
                raise ValueError
            
            self.cart.add_item(product, quantity)

        except ValueError:
            LOGGER.error("Jumlah tidak valid. Hanya angka positif yang diterima.")
        except Exception as e:
            LOGGER.error(f"Error saat menambahkan item: {e}")

    def _handle_checkout(self):
        """Menangani proses checkout."""
        total = self.cart.total_price
        
        if total == 0:
            LOGGER.warning("Keranjang kosong. Tidak bisa checkout.")
            return

        LOGGER.info(f"\nTotal Belanja: Rp{total:,.0f}")
        
        # Delegasi ke Payment Processor yang di-inject
        success = self.payment_processor.process(total) 

        if success:
            LOGGER.info("TRANSAKSI BERHASIL.")
            self._print_receipt()
            self.cart = ShoppingCart()  # Reset cart
        else:
            LOGGER.error("TRANSAKSI GAGAL.")

    def _print_receipt(self):
        """Mencetak struk pembelian sederhana."""
        LOGGER.info("\n--- STRUK PEMBELIAN ---")
        for item in self.cart.get_items():
            LOGGER.info(f" {item.product.name} x{item.quantity} = Rp{item.subtotal:,.0f}")
        LOGGER.info("---------------------------")
        LOGGER.info(f"TOTAL AKHIR: Rp{self.cart.total_price:,.0f}")
        LOGGER.info("---------------------------")


# --- TITIK MASUK UTAMA (Orchestration) ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    # 1. Lapisan Data
    repo = ProductRepository()

    # 2. Ins- Service (Implementasi Konkret)
    # Inovasi Praktikum 13: menggunakan E-Wallet Payment
    payment_method = EWalletPayment()

    # 3. Inject Dependencies ke Aplikasi Utama
    app = PosApp(repository=repo, payment_processor=payment_method)

    # Loop CLI
    while True:
        print("\nMenu:")
        print("1. Tampilkan Produk")
        print("2. Tambah ke Keranjang")
        print("3. Checkout")
        print("4. Keluar")
        
        choice = input("Pilih opsi (1-4): ")

        if choice == "1":
            app._display_menu()
        elif choice == "2":
            app._handle_add_item()
        elif choice == "3":
            app._handle_checkout()
        elif choice == "4":
            LOGGER.info("Aplikasi dihentikan.")
            break
        else:
            LOGGER.warning("Pilihan tidak valid.")
