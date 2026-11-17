"""Enum domain untuk status booking dan peran aktor."""

from enum import StrEnum


class BookingStatus(StrEnum):
    """Status booking yang digunakan pada UC06-UC08 dan UC12-UC14."""

    CONFIRMED = "confirmed"
    BOOKED = "booked"
    WAITING_FOR_PAYMENT = "waiting for the payment"
    CANCELLED = "dibatalkan"


class ActorRole(StrEnum):
    """Peran aktor yang digunakan untuk pemeriksaan hak akses UC01-UC18."""

    HRD_MANAGER = "hrd_manajer"
    USER = "pengguna"
    MEMBER_FREQUENT_TRAVELLER = "member_frequent_traveller"
    TRAVEL_MANAGER = "manajer_travel"
