from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple
import logging

# ====================
# KONFIGURASI LOGGING
# ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)
LOGGER = logging.getLogger("RegistrationService")

# ===========
# MODEL DATA
# ===========
@dataclass
class RegistrationData:
    """
    Menyimpan data registrasi mahasiswa.

    Attributes:
        student_id (str): ID mahasiswa.
        student_name (str): Nama mahasiswa.
        sks_requested (int): Jumlah SKS yang diajukan.
        completed_courses (List[str]): Daftar mata kuliah yang telah ditempuh.
        schedule_slots (List[str]): Slot jadwal yang dipilih.
    """
    student_id: str
    student_name: str
    sks_requested: int
    completed_courses: List[str]
    schedule_slots: List[str]


# ======================
# KODE BURUK (DIBIARKAN)
# ======================
class ValidatorManager:
    """
    Contoh implementasi lama yang melanggar prinsip SOLID.
    """

    def validate(self, reg: RegistrationData) -> bool:
        if reg.sks_requested > 24:
            print("ValidatorManager: SKS melebihi batas.")
            return False
        if 'CS101' not in reg.completed_courses and 'CS102' in reg.completed_courses:
            print("ValidatorManager: Prasyarat tidak terpenuhi.")
            return False
        if len(set(reg.schedule_slots)) < len(reg.schedule_slots):
            print("ValidatorManager: Jadwal bentrok terdeteksi.")
            return False
        print("ValidatorManager: Semua validasi lulus.")
        return True


# ==================
# ABSTRAKSI VALIDASI
# ==================
class IValidationRule(ABC):
    """
    Interface untuk aturan validasi registrasi.
    """

    @abstractmethod
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        """
        Melakukan validasi terhadap data registrasi.
        Args:
            reg (RegistrationData): Data registrasi mahasiswa.
        Returns:
            Tuple[bool, str]: Status validasi dan pesan hasil.
        """
        pass


# ==================
# IMPLEMENTASI RULE
# ==================
class SksLimitRule(IValidationRule):
    """
    Aturan validasi batas maksimum SKS.
    """

    def __init__(self, max_sks: int = 24):
        self.max_sks = max_sks
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        if reg.sks_requested > self.max_sks:
            LOGGER.warning(
                f"SKS melebihi batas: {reg.sks_requested} > {self.max_sks}"
            )
            return False, "SKS melebihi batas"
        LOGGER.info("Validasi SKS berhasil")
        return True, "OK"


class PrerequisiteRule(IValidationRule):
    """
    Aturan validasi prasyarat mata kuliah.
    """

    def __init__(self, required_course: str):
        self.required_course = required_course
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        if self.required_course not in reg.completed_courses:
            LOGGER.warning(
                f"Prasyarat tidak terpenuhi: {self.required_course}"
            )
            return False, f"Missing prerequisite: {self.required_course}"
        LOGGER.info("Validasi prasyarat berhasil")
        return True, "OK"


class JadwalBentrokRule(IValidationRule):
    """
    Aturan validasi bentrokan jadwal.
    """
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        if len(set(reg.schedule_slots)) < len(reg.schedule_slots):
            LOGGER.warning("Jadwal bentrok terdeteksi")
            return False, "Jadwal bentrok"
        LOGGER.info("Validasi jadwal berhasil")
        return True, "OK"


# =====================
# REGISTRATION SERVICE
# =====================
class RegistrationService:
    """
    Service untuk mengoordinasikan proses validasi registrasi mahasiswa.
    """

    def __init__(self, rules: List[IValidationRule]):
        """
        Inisialisasi RegistrationService.
        Args:
            rules (List[IValidationRule]): Daftar aturan validasi.
        """
        self.rules = rules

    def validate(self, reg: RegistrationData) -> Tuple[bool, List[Tuple[str, str]]]:
        """
        Menjalankan seluruh aturan validasi.
        Args:
            reg (RegistrationData): Data registrasi mahasiswa.
        Returns:
            Tuple[bool, List[Tuple[str, str]]]: Status validasi dan daftar error.
        """
        LOGGER.info(f"Memulai validasi untuk mahasiswa {reg.student_name}")
        errors = []
        for rule in self.rules:
            ok, msg = rule.validate(reg)
            LOGGER.info(f"Menjalankan {rule.__class__.__name__} -> {ok}")
            if not ok:
                errors.append((rule.__class__.__name__, msg))
        if errors:
            LOGGER.warning("Validasi registrasi GAGAL")
        else:
            LOGGER.info("Validasi registrasi BERHASIL")

        return (len(errors) == 0), errors


# Program utama untuk pengujian sederhana
if __name__ == '__main__':
    # contoh pengujian sederhana
    rules = [SksLimitRule(), PrerequisiteRule('CS101'), JadwalBentrokRule()]
    service = RegistrationService(rules)

    reg = RegistrationData(
        student_id='S001',
        student_name='Ani',
        sks_requested=18,
        completed_courses=['CS101'],
        schedule_slots=['Mon-9', 'Tue-10']
    )

    service.validate(reg)
