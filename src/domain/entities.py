"""Entitas domain sistem cuti dan pemesanan tiket untuk UC01-UC18."""

from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal

from src.domain.enums import BookingStatus
from src.domain.profile_rules import periksa_kelengkapan_profil_member


@dataclass(slots=True)
class Pegawai:
    """Pegawai pemilik pengajuan cuti pada UC01-UC02."""

    id_pegawai: str
    nama: str
    sisa_cuti: int


@dataclass(slots=True)
class HRDManajer(Pegawai):
    """Aktor HRD Manajer yang mewarisi Pegawai pada UC01-UC02."""


@dataclass(slots=True)
class ManajerTravel(Pegawai):
    """Aktor Manajer Travel yang mewarisi Pegawai pada UC12-UC18."""


@dataclass(slots=True)
class PengajuanCuti:
    """Pengajuan cuti milik satu pegawai untuk UC01-UC02."""

    id_cuti: str
    tanggal_mulai: date
    tanggal_selesai: date
    lama_cuti: int
    id_pegawai: str


@dataclass(slots=True)
class Pengguna:
    """Pengguna terdaftar yang dapat memiliki booking pada UC03-UC08."""

    id_pengguna: str
    nama: str
    email: str


@dataclass(slots=True)
class MemberFrequentTraveller(Pengguna):
    """Spesialisasi Pengguna dengan atribut profil untuk UC04-UC11."""

    nomor_identitas: str | None = None
    tanggal_lahir: date | None = None
    nomor_telepon: str | None = None

    @property
    def status_profil_lengkap(self) -> bool:
        """Hitung status kelengkapan profil Member untuk UC10-UC11."""
        return periksa_kelengkapan_profil_member(
            {
                "nama": self.nama,
                "nomor_identitas": self.nomor_identitas,
                "tanggal_lahir": self.tanggal_lahir,
                "nomor_telepon": self.nomor_telepon,
                "email": self.email,
            }
        )


@dataclass(slots=True)
class Maskapai:
    """Maskapai yang ditampilkan pada hasil pencarian UC03-UC05 dan UC16."""

    id_maskapai: str
    nama_maskapai: str


@dataclass(slots=True)
class Penerbangan:
    """Jadwal penerbangan sebagai dasar UC03-UC06 dan UC16-UC17."""

    id_penerbangan: str
    lokasi_keberangkatan: str
    tujuan: str
    tanggal: date
    jam_keberangkatan: time
    harga: Decimal
    id_maskapai: str


@dataclass(slots=True)
class Booking:
    """Booking milik Pengguna dan dapat dibuat Manajer Travel pada UC06-UC08/UC17."""

    kode_booking_reference: str
    tanggal_booking: date
    status: BookingStatus
    id_pengguna: str
    id_manajer_travel: str | None = None


@dataclass(slots=True)
class Tiket:
    """Tiket untuk satu penerbangan yang dihasilkan dari booking pada UC06-UC10/UC17."""

    id_tiket: str
    e_tiket: str
    id_booking: str
    id_penerbangan: str
    # ASUMSI UC10: status boolean ini merepresentasikan pascakondisi "tiket tervalidasi".
    sudah_divalidasi: bool = False
