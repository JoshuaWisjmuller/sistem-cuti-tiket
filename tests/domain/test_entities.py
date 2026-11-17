"""Test dasar entitas domain untuk UC01-UC18."""

from datetime import date

from src.domain.entities import (
    HRDManajer,
    ManajerTravel,
    MemberFrequentTraveller,
    Pegawai,
    Pengguna,
)


def test_pegawai_dapat_diturunkan_menjadi_aktor_hrd_dan_travel() -> None:
    """Pastikan spesialisasi pegawai sesuai Domain Model UC01 dan UC12-UC18."""
    hrd = HRDManajer("HRD-1", "Rina", 12)
    manajer = ManajerTravel("TRV-1", "Bima", 12)

    assert isinstance(hrd, Pegawai)
    assert isinstance(manajer, Pegawai)
    assert hrd.id_pegawai == "HRD-1"
    assert manajer.nama == "Bima"


def test_member_frequent_traveller_mewarisi_pengguna() -> None:
    """Pastikan Member mewarisi atribut Pengguna sesuai UC03-UC11."""
    member = MemberFrequentTraveller(
        "MEM-1", "Maya", "maya@example.test", "12345", date(2003, 5, 17), "08123"
    )

    assert isinstance(member, Pengguna)
    assert member.id_pengguna == "MEM-1"


def test_status_profil_member_lengkap_dihitung_dari_atributnya() -> None:
    """Pastikan status profil dihitung dari data A5 untuk UC10-UC11."""
    member = MemberFrequentTraveller(
        "MEM-1", "Maya", "maya@example.test", "12345", date(2003, 5, 17), "08123"
    )

    assert member.status_profil_lengkap is True


def test_status_profil_member_tidak_lengkap_jika_ada_atribut_kosong() -> None:
    """Pastikan profil yang belum lengkap dikenali untuk UC10-UC11."""
    member = MemberFrequentTraveller(
        "MEM-2", "Rafi", "rafi@example.test", "67890", date(2002, 8, 9), None
    )

    assert member.status_profil_lengkap is False
