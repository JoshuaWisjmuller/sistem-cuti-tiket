"""Test konsistensi seed data demo untuk UC01-UC18."""

from src.domain.entities import HRDManajer, ManajerTravel, MemberFrequentTraveller
from src.domain.enums import BookingStatus
from src.infrastructure.seed_data import build_seed_data


def test_seed_data_menyediakan_aktor_dan_profil_member_lengkap_tidak_lengkap() -> None:
    """Pastikan data demo memuat aktor utama dan dua kondisi profil UC01-UC18."""
    seed = build_seed_data()
    pegawai = seed.repositories.pegawai
    pengguna = seed.repositories.pengguna

    assert isinstance(pegawai.get_by_id("EMP-HRD-001"), HRDManajer)
    assert isinstance(pegawai.get_by_id("EMP-TRV-001"), ManajerTravel)
    member_lengkap = pengguna.get_by_id("MEMBER-001")
    member_tidak_lengkap = pengguna.get_by_id("MEMBER-002")
    assert isinstance(member_lengkap, MemberFrequentTraveller)
    assert isinstance(member_tidak_lengkap, MemberFrequentTraveller)
    assert member_lengkap.status_profil_lengkap is True
    assert member_tidak_lengkap.status_profil_lengkap is False


def test_seed_data_menyediakan_booking_dengan_setiap_status() -> None:
    """Pastikan semua status booking laporan tersedia untuk UC12-UC14."""
    seed = build_seed_data()

    status_seed = {booking.status for booking in seed.repositories.booking.list_all()}

    assert status_seed == set(BookingStatus)


def test_seed_data_memiliki_penerbangan_multi_tujuan_dan_relasi_maskapai() -> None:
    """Pastikan data demo mendukung pencarian multi-destinasi UC03-UC05 dan UC16."""
    seed = build_seed_data()
    penerbangan = seed.repositories.penerbangan.list_all()
    tujuan = {flight.tujuan for flight in penerbangan}

    assert {"Bali", "Surabaya", "Yogyakarta"}.issubset(tujuan)
    assert all(seed.repositories.maskapai.get_by_id(flight.id_maskapai) for flight in penerbangan)


def test_fake_email_sender_dimulai_dengan_list_kosong() -> None:
    """Pastikan fake sender siap menyimpan pengiriman e-tiket pada UC18."""
    seed = build_seed_data()

    assert seed.email_sender.sent_emails == []
