"""Test pure function aturan profil Member untuk UC10-UC11."""

from datetime import date

from src.domain.profile_rules import (
    ATRIBUT_PROFIL_MEMBER_WAJIB,
    periksa_kelengkapan_profil_member,
)


def test_uc11_profil_lengkap_jika_seluruh_atribut_wajib_terisi() -> None:
    """Profil lengkap harus menghasilkan True pada pemeriksaan UC11."""
    data_profil = {
        "nama": "Maya",
        "nomor_identitas": "12345",
        "tanggal_lahir": date(2003, 5, 17),
        "nomor_telepon": "08123",
        "email": "maya@example.test",
    }

    assert periksa_kelengkapan_profil_member(data_profil) is True


def test_uc11_profil_tidak_lengkap_jika_atribut_wajib_tidak_ada() -> None:
    """Atribut wajib yang tidak tersedia harus menghasilkan False pada UC11."""
    data_profil = {
        "nama": "Maya",
        "nomor_identitas": "12345",
        "tanggal_lahir": date(2003, 5, 17),
        "email": "maya@example.test",
    }

    assert periksa_kelengkapan_profil_member(data_profil) is False


def test_uc11_profil_tidak_lengkap_jika_string_hanya_berisi_spasi() -> None:
    """String kosong atau spasi dianggap belum lengkap pada UC11."""
    data_profil = {
        "nama": "Maya",
        "nomor_identitas": "12345",
        "tanggal_lahir": date(2003, 5, 17),
        "nomor_telepon": "   ",
        "email": "maya@example.test",
    }

    assert periksa_kelengkapan_profil_member(data_profil) is False


def test_atribut_profil_wajib_didefinisikan_satu_kali() -> None:
    """Pastikan daftar atribut A5 terpusat dan eksplisit untuk UC11."""
    assert ATRIBUT_PROFIL_MEMBER_WAJIB == (
        "nama",
        "nomor_identitas",
        "tanggal_lahir",
        "nomor_telepon",
        "email",
    )
