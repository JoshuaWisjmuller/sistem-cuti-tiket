"""Repository in-memory untuk unit test dan seed data UC01-UC18."""

from dataclasses import dataclass, field

from src.domain.entities import (
    Booking,
    Maskapai,
    Pegawai,
    PengajuanCuti,
    Penerbangan,
    Pengguna,
    Tiket,
)


@dataclass(slots=True)
class InMemoryDatabase:
    """Penyimpanan dictionary bersama untuk repository in-memory UC01-UC18."""

    pegawai: dict[str, Pegawai] = field(default_factory=dict)
    pengajuan_cuti: dict[str, PengajuanCuti] = field(default_factory=dict)
    pengguna: dict[str, Pengguna] = field(default_factory=dict)
    maskapai: dict[str, Maskapai] = field(default_factory=dict)
    penerbangan: dict[str, Penerbangan] = field(default_factory=dict)
    booking: dict[str, Booking] = field(default_factory=dict)
    tiket: dict[str, Tiket] = field(default_factory=dict)


class InMemoryPegawaiRepository:
    """Adapter repository pegawai untuk UC01-UC02 dan UC12-UC18."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC01-UC02 dan UC12-UC18."""
        self._database = database

    def get_by_id(self, id_pegawai: str) -> Pegawai | None:
        """Ambil pegawai berdasarkan ID untuk UC01-UC02 dan UC12-UC18."""
        return self._database.pegawai.get(id_pegawai)

    def list_all(self) -> list[Pegawai]:
        """Ambil seluruh pegawai untuk UC01-UC02 dan UC12-UC18."""
        return list(self._database.pegawai.values())


class InMemoryPengajuanCutiRepository:
    """Adapter repository pengajuan cuti untuk UC01-UC02."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC01-UC02."""
        self._database = database

    def get_by_id(self, id_cuti: str) -> PengajuanCuti | None:
        """Ambil pengajuan cuti berdasarkan ID untuk UC01-UC02."""
        return self._database.pengajuan_cuti.get(id_cuti)

    def list_all(self) -> list[PengajuanCuti]:
        """Ambil seluruh pengajuan cuti untuk UC01-UC02."""
        return list(self._database.pengajuan_cuti.values())

    def list_by_pegawai(self, id_pegawai: str) -> list[PengajuanCuti]:
        """Ambil riwayat cuti pegawai untuk UC02."""
        return [
            pengajuan
            for pengajuan in self._database.pengajuan_cuti.values()
            if pengajuan.id_pegawai == id_pegawai
        ]


class InMemoryPenggunaRepository:
    """Adapter repository Pengguna dan Member untuk UC03-UC10 serta UC16-UC17."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC03-UC10 dan UC16-UC17."""
        self._database = database

    def get_by_id(self, id_pengguna: str) -> Pengguna | None:
        """Ambil pengguna berdasarkan ID untuk UC03-UC10 dan UC16-UC17."""
        return self._database.pengguna.get(id_pengguna)

    def list_all(self) -> list[Pengguna]:
        """Ambil seluruh pengguna untuk UC03-UC10 dan UC16-UC17."""
        return list(self._database.pengguna.values())

    def save(self, pengguna: Pengguna) -> None:
        """Simpan pengguna atau profil yang diperbarui untuk UC09."""
        self._database.pengguna[pengguna.id_pengguna] = pengguna


class InMemoryMaskapaiRepository:
    """Adapter repository maskapai untuk UC03-UC05 dan UC16."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC03-UC05 dan UC16."""
        self._database = database

    def get_by_id(self, id_maskapai: str) -> Maskapai | None:
        """Ambil maskapai berdasarkan ID untuk UC03-UC05 dan UC16."""
        return self._database.maskapai.get(id_maskapai)

    def list_all(self) -> list[Maskapai]:
        """Ambil seluruh maskapai untuk UC03-UC05 dan UC16."""
        return list(self._database.maskapai.values())


class InMemoryPenerbanganRepository:
    """Adapter repository penerbangan untuk UC03-UC06 dan UC16-UC17."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC03-UC06 dan UC16-UC17."""
        self._database = database

    def get_by_id(self, id_penerbangan: str) -> Penerbangan | None:
        """Ambil penerbangan berdasarkan ID untuk UC03-UC06 dan UC16-UC17."""
        return self._database.penerbangan.get(id_penerbangan)

    def list_all(self) -> list[Penerbangan]:
        """Ambil seluruh penerbangan untuk UC03-UC06 dan UC16-UC17."""
        return list(self._database.penerbangan.values())


class InMemoryBookingRepository:
    """Adapter repository booking untuk UC06-UC08 dan UC12-UC17."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC06-UC08 dan UC12-UC17."""
        self._database = database

    def get_by_reference(self, kode_booking_reference: str) -> Booking | None:
        """Ambil booking berdasarkan kode untuk UC14-UC15."""
        return self._database.booking.get(kode_booking_reference)

    def list_all(self) -> list[Booking]:
        """Ambil seluruh booking untuk UC12-UC14."""
        return list(self._database.booking.values())

    def list_by_pengguna(self, id_pengguna: str) -> list[Booking]:
        """Ambil booking milik pengguna untuk UC07-UC08."""
        return [
            booking
            for booking in self._database.booking.values()
            if booking.id_pengguna == id_pengguna
        ]

    def save(self, booking: Booking) -> None:
        """Simpan booking baru atau perubahan status untuk UC06-UC08 dan UC17."""
        self._database.booking[booking.kode_booking_reference] = booking


class InMemoryTiketRepository:
    """Adapter repository tiket untuk UC06-UC10 dan UC17-UC18."""

    def __init__(self, database: InMemoryDatabase) -> None:
        """Suntikkan penyimpanan in-memory untuk UC06-UC10 dan UC17-UC18."""
        self._database = database

    def get_by_id(self, id_tiket: str) -> Tiket | None:
        """Ambil tiket berdasarkan ID untuk UC10."""
        return self._database.tiket.get(id_tiket)

    def list_by_booking(self, kode_booking_reference: str) -> list[Tiket]:
        """Ambil tiket dari booking untuk UC07 dan UC17-UC18."""
        return [
            tiket
            for tiket in self._database.tiket.values()
            if tiket.id_booking == kode_booking_reference
        ]

    def list_all(self) -> list[Tiket]:
        """Ambil seluruh tiket untuk seed data dan UC06-UC10/UC17-UC18."""
        return list(self._database.tiket.values())

    def save(self, tiket: Tiket) -> None:
        """Simpan tiket untuk UC06 dan UC17."""
        self._database.tiket[tiket.id_tiket] = tiket
