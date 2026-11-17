"""Port repository yang diimplementasikan infrastructure, bukan application."""

from collections.abc import Sequence
from datetime import date
from typing import Protocol

from src.domain.entities import (
    Booking,
    Maskapai,
    Pegawai,
    PengajuanCuti,
    Penerbangan,
    Pengguna,
    Tiket,
)


class PegawaiRepository(Protocol):
    """Port akses data pegawai untuk UC01-UC02 dan UC12-UC18."""

    def get_by_id(self, id_pegawai: str) -> Pegawai | None:
        """Ambil pegawai berdasarkan ID untuk UC01-UC02 dan UC12-UC18."""

    def list_all(self) -> Sequence[Pegawai]:
        """Ambil seluruh pegawai untuk UC01-UC02 dan UC12-UC18."""


class PengajuanCutiRepository(Protocol):
    """Port akses data pengajuan cuti untuk UC01-UC02."""

    def get_by_id(self, id_cuti: str) -> PengajuanCuti | None:
        """Ambil pengajuan cuti berdasarkan ID untuk UC01-UC02."""

    def list_all(self) -> Sequence[PengajuanCuti]:
        """Ambil seluruh pengajuan cuti untuk UC01-UC02."""

    def list_by_pegawai(self, id_pegawai: str) -> Sequence[PengajuanCuti]:
        """Ambil riwayat cuti pegawai untuk UC02."""


class PenggunaRepository(Protocol):
    """Port akses Pengguna dan Member untuk UC03-UC10 serta UC16-UC17."""

    def get_by_id(self, id_pengguna: str) -> Pengguna | None:
        """Ambil pengguna berdasarkan ID untuk UC03-UC10 dan UC16-UC17."""

    def list_all(self) -> Sequence[Pengguna]:
        """Ambil seluruh pengguna untuk UC03-UC10 dan UC16-UC17."""

    def save(self, pengguna: Pengguna) -> None:
        """Simpan pengguna atau profil yang diperbarui untuk UC09."""


class MaskapaiRepository(Protocol):
    """Port akses data maskapai untuk UC03-UC05 dan UC16."""

    def get_by_id(self, id_maskapai: str) -> Maskapai | None:
        """Ambil maskapai berdasarkan ID untuk UC03-UC05 dan UC16."""

    def list_all(self) -> Sequence[Maskapai]:
        """Ambil seluruh maskapai untuk UC03-UC05 dan UC16."""


class PenerbanganRepository(Protocol):
    """Port akses jadwal penerbangan untuk UC03-UC06 dan UC16-UC17."""

    def get_by_id(self, id_penerbangan: str) -> Penerbangan | None:
        """Ambil penerbangan berdasarkan ID untuk UC03-UC06 dan UC16-UC17."""

    def list_all(self) -> Sequence[Penerbangan]:
        """Ambil seluruh penerbangan untuk UC03-UC06 dan UC16-UC17."""


class BookingRepository(Protocol):
    """Port akses booking untuk UC06-UC08 dan UC12-UC17."""

    def get_by_reference(self, kode_booking_reference: str) -> Booking | None:
        """Ambil booking berdasarkan kode untuk UC14-UC15."""

    def list_all(self) -> Sequence[Booking]:
        """Ambil seluruh booking untuk UC12-UC14."""

    def list_by_pengguna(self, id_pengguna: str) -> Sequence[Booking]:
        """Ambil booking milik pengguna untuk UC07-UC08."""

    def save(self, booking: Booking) -> None:
        """Simpan booking baru atau perubahan status untuk UC06-UC08 dan UC17."""


class TiketRepository(Protocol):
    """Port akses tiket untuk UC06-UC10 dan UC17-UC18."""

    def get_by_id(self, id_tiket: str) -> Tiket | None:
        """Ambil tiket berdasarkan ID untuk UC10."""

    def list_by_booking(self, kode_booking_reference: str) -> Sequence[Tiket]:
        """Ambil tiket dari booking untuk UC07 dan UC17-UC18."""

    def save(self, tiket: Tiket) -> None:
        """Simpan tiket untuk UC06 dan UC17."""
