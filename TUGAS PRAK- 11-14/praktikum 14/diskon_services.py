# diskon_services.py

class DiskonCalculator:
    """Menghitung harga akhir setelah diberi diskon."""

    def hitung_diskon(self, harga_awal: float, persentase_diskon: int) -> float:
        # Validasi harga awal
        if harga_awal <= 0:
            return 0.0

        # Validasi persentase diskon
        if persentase_diskon < 0:
            persentase_diskon = 0
        elif persentase_diskon > 100:
            persentase_diskon = 100

        # PERBAIKAN BUG: diskon dibagi 100
        jumlah_diskon = harga_awal * (persentase_diskon / 100)

        harga_akhir = harga_awal - jumlah_diskon

        # Pastikan tidak negatif
        if harga_akhir < 0:
            harga_akhir = 0.0

        return round(harga_akhir, 2)
