"""Seed data demo untuk mencoba alur UC01-UC18 pada tahap pengembangan."""

from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal

from src.domain.entities import (
    Booking,
    HRDManajer,
    ManajerTravel,
    Maskapai,
    MemberFrequentTraveller,
    Pegawai,
    PengajuanCuti,
    Penerbangan,
    Pengguna,
    Tiket,
)
from src.domain.enums import BookingStatus
from src.infrastructure.email_sender import FakeEmailSender
from src.infrastructure.repositories.in_memory import (
    InMemoryBookingRepository,
    InMemoryDatabase,
    InMemoryMaskapaiRepository,
    InMemoryPegawaiRepository,
    InMemoryPengajuanCutiRepository,
    InMemoryPenerbanganRepository,
    InMemoryPenggunaRepository,
    InMemoryTiketRepository,
)


@dataclass(slots=True)
class RepositorySet:
    """Kumpulan adapter in-memory yang berbagi satu database untuk UC01-UC18."""

    pegawai: InMemoryPegawaiRepository
    pengajuan_cuti: InMemoryPengajuanCutiRepository
    pengguna: InMemoryPenggunaRepository
    maskapai: InMemoryMaskapaiRepository
    penerbangan: InMemoryPenerbanganRepository
    booking: InMemoryBookingRepository
    tiket: InMemoryTiketRepository


@dataclass(slots=True)
class SeedData:
    """Seluruh dependency demo yang disiapkan untuk pengujian UC01-UC18."""

    database: InMemoryDatabase
    repositories: RepositorySet
    email_sender: FakeEmailSender


def build_seed_data() -> SeedData:
    """Bangun dataset demo dan repository in-memory untuk UC01-UC18."""
    pegawai: dict[str, Pegawai] = {
        "EMP-HRD-001": HRDManajer("EMP-HRD-001", "Rina HRD", 12),
        "EMP-TRV-001": ManajerTravel("EMP-TRV-001", "Bima Travel", 12),
        "EMP-001": Pegawai("EMP-001", "Andi Pratama", 8),
        "EMP-002": Pegawai("EMP-002", "Siti Rahma", 10),
    }

    pengajuan_cuti = {
        "CUTI-001": PengajuanCuti(
            "CUTI-001", date(2026, 11, 20), date(2026, 11, 22), 3, "EMP-001"
        ),
        "CUTI-002": PengajuanCuti(
            "CUTI-002", date(2026, 11, 25), date(2026, 11, 26), 2, "EMP-002"
        ),
        "CUTI-003": PengajuanCuti(
            "CUTI-003", date(2026, 12, 2), date(2026, 12, 4), 3, "EMP-001"
        ),
    }

    pengguna: dict[str, Pengguna] = {
        "USER-001": Pengguna("USER-001", "Dewi Lestari", "dewi@example.test"),
        "MEMBER-001": MemberFrequentTraveller(
            id_pengguna="MEMBER-001",
            nama="Maya Pratama",
            email="maya@example.test",
            nomor_identitas="3174000000000001",
            tanggal_lahir=date(2003, 5, 17),
            nomor_telepon="081234567890",
        ),
        "MEMBER-002": MemberFrequentTraveller(
            id_pengguna="MEMBER-002",
            nama="Rafi Nugraha",
            email="rafi@example.test",
            nomor_identitas="3174000000000002",
            tanggal_lahir=date(2002, 8, 9),
            nomor_telepon=None,
        ),
    }

    maskapai = {
        "AIR-001": Maskapai("AIR-001", "Aero Nusantara"),
        "AIR-002": Maskapai("AIR-002", "Langit Express"),
    }

    penerbangan = {
        "FLIGHT-001": Penerbangan(
            "FLIGHT-001",
            "Jakarta",
            "Bali",
            date(2026, 12, 1),
            time(8, 30),
            Decimal("1250000"),
            "AIR-001",
        ),
        "FLIGHT-002": Penerbangan(
            "FLIGHT-002",
            "Jakarta",
            "Bali",
            date(2026, 12, 1),
            time(13, 15),
            Decimal("980000"),
            "AIR-002",
        ),
        "FLIGHT-003": Penerbangan(
            "FLIGHT-003",
            "Jakarta",
            "Surabaya",
            date(2026, 12, 1),
            time(10, 0),
            Decimal("750000"),
            "AIR-001",
        ),
        "FLIGHT-004": Penerbangan(
            "FLIGHT-004",
            "Bali",
            "Yogyakarta",
            date(2026, 12, 2),
            time(9, 45),
            Decimal("890000"),
            "AIR-002",
        ),
    }

    booking = {
        "BOOK-CONF-001": Booking(
            "BOOK-CONF-001",
            date(2026, 11, 10),
            BookingStatus.CONFIRMED,
            "USER-001",
        ),
        "BOOK-NEW-001": Booking(
            "BOOK-NEW-001",
            date(2026, 11, 12),
            BookingStatus.BOOKED,
            "MEMBER-001",
        ),
        "BOOK-WAIT-001": Booking(
            "BOOK-WAIT-001",
            date(2026, 11, 13),
            BookingStatus.WAITING_FOR_PAYMENT,
            "MEMBER-002",
        ),
        "BOOK-CANCEL-001": Booking(
            "BOOK-CANCEL-001",
            date(2026, 11, 14),
            BookingStatus.CANCELLED,
            "USER-001",
        ),
    }

    tiket = {
        "TICKET-001": Tiket(
            "TICKET-001", "ETK-BOOK-CONF-001", "BOOK-CONF-001", "FLIGHT-001"
        ),
        "TICKET-002": Tiket(
            "TICKET-002", "ETK-BOOK-NEW-001", "BOOK-NEW-001", "FLIGHT-002"
        ),
        "TICKET-003": Tiket(
            "TICKET-003", "ETK-BOOK-WAIT-001", "BOOK-WAIT-001", "FLIGHT-003"
        ),
        "TICKET-004": Tiket(
            "TICKET-004", "ETK-BOOK-CANCEL-001", "BOOK-CANCEL-001", "FLIGHT-004"
        ),
    }

    database = InMemoryDatabase(
        pegawai=pegawai,
        pengajuan_cuti=pengajuan_cuti,
        pengguna=pengguna,
        maskapai=maskapai,
        penerbangan=penerbangan,
        booking=booking,
        tiket=tiket,
    )
    repositories = RepositorySet(
        pegawai=InMemoryPegawaiRepository(database),
        pengajuan_cuti=InMemoryPengajuanCutiRepository(database),
        pengguna=InMemoryPenggunaRepository(database),
        maskapai=InMemoryMaskapaiRepository(database),
        penerbangan=InMemoryPenerbanganRepository(database),
        booking=InMemoryBookingRepository(database),
        tiket=InMemoryTiketRepository(database),
    )
    return SeedData(database, repositories, FakeEmailSender())
