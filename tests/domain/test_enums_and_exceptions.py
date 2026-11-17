"""Test enum status dan exception domain UC01-UC18."""

import pytest

from src.domain.enums import ActorRole, BookingStatus
from src.domain.exceptions import (
    KodeBookingTidakSesuaiError,
    ProfilTidakLengkapError,
)


def test_status_booking_menggunakan_nilai_yang_ditetapkan_laporan() -> None:
    """Pastikan nilai status konsisten dengan Domain Model UC12-UC14."""
    assert {status.value for status in BookingStatus} == {
        "confirmed",
        "booked",
        "waiting for the payment",
        "dibatalkan",
    }


def test_role_aktor_didefinisikan_sebagai_enum() -> None:
    """Pastikan peran aktor tidak tersebar sebagai magic string UC01-UC18."""
    assert ActorRole.HRD_MANAGER.value == "hrd_manajer"
    assert ActorRole.USER.value == "pengguna"
    assert ActorRole.MEMBER_FREQUENT_TRAVELLER.value == "member_frequent_traveller"
    assert ActorRole.TRAVEL_MANAGER.value == "manajer_travel"


def test_uc10_pesan_profil_tidak_lengkap_sesuai_laporan() -> None:
    """Pastikan pesan alternatif UC10 sama persis dengan laporan."""
    with pytest.raises(ProfilTidakLengkapError, match="^data profil tidak lengkap$"):
        raise ProfilTidakLengkapError()


def test_uc15_pesan_kode_booking_tidak_sesuai_sesuai_laporan() -> None:
    """Pastikan pesan alternatif UC15 sama persis dengan laporan."""
    with pytest.raises(
        KodeBookingTidakSesuaiError,
        match="^kode booking reference tidak sesuai$",
    ):
        raise KodeBookingTidakSesuaiError()
