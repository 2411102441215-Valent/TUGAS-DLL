
# refactor_registration.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

# =============================
# KODE BURUK (Sebelum refactor)
# =============================
@dataclass
class RegistrationData:
    student_id: str
    student_name: str
    sks_requested: int
    completed_courses: List[str]
    schedule_slots: List[str]  # e.g., ['Mon-9', 'Tue-14']


class ValidatorManager:
    """Satu class yang meng-handle semua validasi dengan if/else.
    Melanggar SRP, OCP, DIP."""
    def validate(self, reg: RegistrationData) -> bool:
        # Validasi SKS
        if reg.sks_requested > 24:
            print("ValidatorManager: SKS melebihi batas.")
            return False
        # Validasi Prasyarat (hardcoded)
        if 'CS101' not in reg.completed_courses and 'CS102' in reg.completed_courses:
            print("ValidatorManager: Prasyarat tidak terpenuhi.")
            return False
        # (tambahan) Validasi jadwal bentrok
        if len(set(reg.schedule_slots)) < len(reg.schedule_slots):
            print("ValidatorManager: Jadwal bentrok terdeteksi.")
            return False
        print("ValidatorManager: Semua validasi lulus.")
        return True


# =======================================
# REFACTOR: Abstraksi + Implementasi SRP/OCP/DIP
# =======================================
class IValidationRule(ABC):
    """Kontrak: semua aturan harus implement method validate(reg) -> (bool, message)"""
    @abstractmethod
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        pass


class SksLimitRule(IValidationRule):
    def __init__(self, max_sks=24):
        self.max_sks = max_sks

    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        if reg.sks_requested > self.max_sks:
            return False, f"SKS requested ({reg.sks_requested}) > max ({self.max_sks})"
        return True, "OK"


class PrerequisiteRule(IValidationRule):
    def __init__(self, required_course):
        self.required_course = required_course

    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        if self.required_course not in reg.completed_courses:
            return False, f"Missing prerequisite: {self.required_course}"
        return True, "OK"


# RegistrationService: koordinator yang menerima list of IValidationRule via DI
class RegistrationService:
    def __init__(self, rules: List[IValidationRule]):
        self.rules = rules

    def validate(self, reg: RegistrationData) -> Tuple[bool, List[Tuple[str, str]]]:
        errors = []
        for rule in self.rules:
            ok, msg = rule.validate(reg)
            # tampilkan nama rule agar mudah dilihat di terminal
            print(f"Running rule: {rule.__class__.__name__} -> {ok} : {msg}")
            if not ok:
                errors.append((rule.__class__.__name__, msg))
        return (len(errors) == 0), errors


# Challenge: Tambah JadwalBentrokRule tanpa mengubah RegistrationService
class JadwalBentrokRule(IValidationRule):
    def validate(self, reg: RegistrationData) -> Tuple[bool, str]:
        # sederhana: bentrok jika ada duplicate slot
        if len(set(reg.schedule_slots)) < len(reg.schedule_slots):
            return False, "Jadwal bentrok: ada slot yang sama."
        return True, "OK"


# ============ Demo / Program Utama ============
def demo():
    print("=== Demo: Sebelum refactor (ValidatorManager) ===")
    reg1 = RegistrationData(student_id='S001', student_name='Ani', sks_requested=26,
                            completed_courses=['CS101'], schedule_slots=['Mon-9','Tue-10'])
    vm = ValidatorManager()
    vm.validate(reg1)

    print("\n=== Demo: Sesudah refactor (RegistrationService) ===")
    # buat rules: SKS + Prasyarat CS101
    rules = [SksLimitRule(max_sks=24), PrerequisiteRule('CS101')]
    service = RegistrationService(rules)

    reg2 = RegistrationData(student_id='S002', student_name='Budi', sks_requested=20,
                            completed_courses=['CS102'], schedule_slots=['Mon-9','Tue-10'])
    ok, errors = service.validate(reg2)
    print(f"Validation result: {ok}, errors: {errors}")

    print("\n=== Demo: Challenge - Inject JadwalBentrokRule tanpa mengubah RegistrationService ===")
    # tambahkan rule bentrok dan tes
    rules_with_bentrok = [SksLimitRule(), PrerequisiteRule('CS101'), JadwalBentrokRule()]
    service2 = RegistrationService(rules_with_bentrok)
    reg3 = RegistrationData(student_id='S003', student_name='Citra', sks_requested=18,
                            completed_courses=['CS101'], schedule_slots=['Mon-9','Mon-9'])  # duplicate slot -> bentrok
    ok3, errors3 = service2.validate(reg3)
    print(f"Validation result (with JadwalBentrokRule): {ok3}, errors: {errors3}")

if __name__ == '__main__':
    demo()
