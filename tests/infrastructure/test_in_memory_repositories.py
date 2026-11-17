"""Test adapter repository in-memory untuk UC01-UC18."""

from datetime import date

from src.domain.entities import Booking, Pengguna, Tiket
from src.domain.enums import BookingStatus
from src.infrastructure.email_sender import FakeEmailSender
from src.infrastructure.repositories.in_memory import (
    InMemoryBookingRepository,
    InMemoryDatabase,
    InMemoryPengajuanCutiRepository,
    InMemoryPenggunaRepository,
    InMemoryTiketRepository,
)
from src.infrastructure.seed_data import build_seed_data


def test_repository_pengajuan_cuti_mengambil_riwayat_pegawai() -> None:
    """Pastikan repository memfilter pengajuan menurut pemilik untuk UC02."""
    seed = build_seed_data()

    pengajuan = seed.repositories.pengajuan_cuti.list_by_pegawai("EMP-001")

    assert len(pengajuan) == 2
    assert all(item.id_pegawai == "EMP-001" for item in pengajuan)


def test_repository_pengguna_menyimpan_perubahan_profil() -> None:
    """Pastikan repository dapat menyimpan profil pengguna untuk UC09."""
    database = InMemoryDatabase()
    repository = InMemoryPenggunaRepository(database)
    pengguna = Pengguna("USER-1", "Dewi", "dewi@example.test")

    repository.save(pengguna)

    assert repository.get_by_id("USER-1") == pengguna


def test_repository_booking_menyimpan_dan_memfilter_booking_pengguna() -> None:
    """Pastikan repository booking mendukung simpan dan daftar pesanan UC06-UC08."""
    database = InMemoryDatabase()
    repository = InMemoryBookingRepository(database)
    booking = Booking(
        "BOOK-1", date(2026, 11, 17), BookingStatus.BOOKED, "USER-1"
    )

    repository.save(booking)

    assert repository.get_by_reference("BOOK-1") == booking
    assert repository.list_by_pengguna("USER-1") == [booking]
    assert repository.list_by_pengguna("USER-2") == []


def test_repository_booking_dapat_memperbarui_status_booking() -> None:
    """Pastikan save memperbarui booking dengan kode yang sama untuk UC08."""
    database = InMemoryDatabase()
    repository = InMemoryBookingRepository(database)
    booking = Booking(
        "BOOK-1", date(2026, 11, 17), BookingStatus.BOOKED, "USER-1"
    )
    repository.save(booking)
    booking.status = BookingStatus.CANCELLED
    repository.save(booking)

    assert repository.list_all()[0].status is BookingStatus.CANCELLED


def test_repository_tiket_menyimpan_dan_mengambil_tiket_per_booking() -> None:
    """Pastikan repository tiket mendukung UC07, UC10, dan UC17-UC18."""
    database = InMemoryDatabase()
    repository = InMemoryTiketRepository(database)
    tiket = Tiket("TICKET-1", "ETK-1", "BOOK-1", "FLIGHT-1")

    repository.save(tiket)

    assert repository.get_by_id("TICKET-1") == tiket
    assert repository.list_by_booking("BOOK-1") == [tiket]
    assert repository.list_by_booking("BOOK-2") == []


def test_repository_pengajuan_cuti_dan_booking_mengembalikan_list_kosong() -> None:
    """Pastikan repository mengembalikan list kosong jika data tidak ada UC01/UC07."""
    database = InMemoryDatabase()

    assert InMemoryPengajuanCutiRepository(database).list_all() == []
    assert InMemoryBookingRepository(database).list_all() == []


def test_fake_email_sender_menyimpan_pesan_ke_list() -> None:
    """Pastikan fake sender menyimpan email untuk pengujian UC18."""
    sender = FakeEmailSender()

    sender.send_email("pengunjung@example.test", "E-tiket", "Isi e-tiket")

    assert len(sender.sent_emails) == 1
    assert sender.sent_emails[0].recipient == "pengunjung@example.test"
    assert sender.sent_emails[0].subject == "E-tiket"
    assert sender.sent_emails[0].body == "Isi e-tiket"
