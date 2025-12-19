# test_diskon.py
import unittest
from diskon_services import DiskonCalculator

class TestDiskonCalculator(unittest.TestCase):
    def setUp(self):
        """Menyiapkan instance Calculator."""
        self.calc = DiskonCalculator()

    def test_diskon_standar_10_persen(self):
        """Tes 1: Diskon 10% dari 1000."""
        hasil = self.calc.hitung_diskon(1000, 10)
        self.assertEqual(hasil, 900.0)

    def test_diskon_nol(self):
        """Tes 2: Diskon 0%."""
        hasil = self.calc.hitung_diskon(500, 0)
        self.assertEqual(hasil, 500.0)

    def test_diskon_batas_atas(self):
        """Tes 3: Diskon 100%."""
        hasil = self.calc.hitung_diskon(750, 100)
        self.assertEqual(hasil, 0.0)

    def test_input_negatif(self):
        """Tes 4: Diskon negatif tidak menurunkan harga."""
        hasil = self.calc.hitung_diskon(500, -5)
        self.assertGreaterEqual(hasil, 500.0)


class TestDiskonLanjut(unittest.TestCase):
    def setUp(self):
        self.calc = DiskonCalculator()

    def test_diskon_float(self):
        """Tes 5: Diskon float (33% dari 999)."""
        hasil = self.calc.hitung_diskon(999, 33)
        self.assertAlmostEqual(hasil, 669.33, places=2)

    def test_edge_case_harga_nol(self):
        """Tes 6: Harga awal 0."""
        hasil = self.calc.hitung_diskon(0, 50)
        self.assertEqual(hasil, 0.0)

    def test_diskon_lebih_dari_100(self):
        """Tes 7: Diskon > 100% tidak menghasilkan harga negatif."""
        hasil = self.calc.hitung_diskon(400, 150)
        self.assertGreaterEqual(hasil, 0.0)

    def test_ppn_ganda_setelah_bug_fix(self):
        """Tes 8: Memastikan bug PPN ganda sudah diperbaiki."""
        hasil = self.calc.hitung_diskon(1000, 10)
        self.assertEqual(hasil, 900.0)


if __name__ == '__main__':
    unittest.main()
