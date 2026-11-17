"""Exception domain dan pesan error yang dipakai lintas use case."""

PESAN_PROFIL_TIDAK_LENGKAP = "data profil tidak lengkap"
PESAN_KODE_BOOKING_TIDAK_SESUAI = "kode booking reference tidak sesuai"
PESAN_AKSES_DITOLAK = "aktor tidak memiliki hak akses untuk use case ini"
PESAN_PEGAWAI_TIDAK_DITEMUKAN = "pegawai tidak ditemukan"
PESAN_PENGGUNA_TIDAK_DITEMUKAN = "pengguna tidak ditemukan"
PESAN_PENERBANGAN_TIDAK_DITEMUKAN = "penerbangan tidak ditemukan"
PESAN_PESANAN_TIDAK_DITEMUKAN = "pesanan tidak ditemukan"
PESAN_PESANAN_BUKAN_MILIK_PEMESAN = "pesanan bukan milik pengguna"
PESAN_PESANAN_SUDAH_DIBATALKAN = "pesanan sudah dibatalkan"
PESAN_KONFIRMASI_PEMBATALAN_DIBUTUHKAN = "pembatalan belum dikonfirmasi"
PESAN_DATA_PENGUNJUNG_TIDAK_DITEMUKAN = "data pengunjung tidak ditemukan"
PESAN_TIKET_TIDAK_DITEMUKAN = "tiket tidak ditemukan"


class DomainError(Exception):
    """Exception dasar untuk kegagalan aturan bisnis UC01-UC18."""


class AksesDitolakError(DomainError):
    """Aktor tidak memenuhi hak akses use case UC01-UC18."""

    def __init__(self) -> None:
        super().__init__(PESAN_AKSES_DITOLAK)


class PegawaiTidakDitemukanError(DomainError):
    """Pegawai yang dibutuhkan UC01-UC02 tidak ditemukan."""

    def __init__(self) -> None:
        super().__init__(PESAN_PEGAWAI_TIDAK_DITEMUKAN)


class PenggunaTidakDitemukanError(DomainError):
    """Pengguna yang dibutuhkan UC03-UC10 atau UC16-UC17 tidak ditemukan."""

    def __init__(self) -> None:
        super().__init__(PESAN_PENGGUNA_TIDAK_DITEMUKAN)


class PenerbanganTidakDitemukanError(DomainError):
    """Penerbangan yang dibutuhkan UC03-UC06 atau UC16-UC17 tidak ditemukan."""

    def __init__(self) -> None:
        super().__init__(PESAN_PENERBANGAN_TIDAK_DITEMUKAN)


class PesananTidakDitemukanError(DomainError):
    """Booking yang dibutuhkan UC07-UC08 atau UC14 tidak ditemukan."""

    def __init__(self) -> None:
        super().__init__(PESAN_PESANAN_TIDAK_DITEMUKAN)


class PesananBukanMilikPemesanError(DomainError):
    """Booking tidak dimiliki aktor pada UC08."""

    def __init__(self) -> None:
        super().__init__(PESAN_PESANAN_BUKAN_MILIK_PEMESAN)


class PesananSudahDibatalkanError(DomainError):
    """Booking sudah dibatalkan pada UC08."""

    def __init__(self) -> None:
        super().__init__(PESAN_PESANAN_SUDAH_DIBATALKAN)


class KonfirmasiPembatalanDibutuhkanError(DomainError):
    """Konfirmasi pembatalan belum diberikan pada UC08."""

    def __init__(self) -> None:
        super().__init__(PESAN_KONFIRMASI_PEMBATALAN_DIBUTUHKAN)


class ProfilTidakLengkapError(DomainError):
    """Profil Member tidak lengkap saat UC10 dijalankan."""

    def __init__(self) -> None:
        super().__init__(PESAN_PROFIL_TIDAK_LENGKAP)


class KodeBookingTidakSesuaiError(DomainError):
    """Kode booking reference tidak ditemukan pada UC14-UC15."""

    def __init__(self) -> None:
        super().__init__(PESAN_KODE_BOOKING_TIDAK_SESUAI)


class DataPengunjungTidakDitemukanError(DomainError):
    """Pengunjung tidak ditemukan saat UC17 dijalankan."""

    def __init__(self) -> None:
        super().__init__(PESAN_DATA_PENGUNJUNG_TIDAK_DITEMUKAN)


class TiketTidakDitemukanError(DomainError):
    """Tiket tidak ditemukan saat UC10 dijalankan."""

    def __init__(self) -> None:
        super().__init__(PESAN_TIKET_TIDAK_DITEMUKAN)
