"""Service booking, daftar pesanan, dan pembatalan UC06-UC08."""
from datetime import date
from uuid import uuid4
from src.domain.entities import Booking, Tiket
from src.domain.enums import BookingStatus
from src.domain.exceptions import (AksesDitolakError, KonfirmasiPembatalanDibutuhkanError,
    PenerbanganTidakDitemukanError, PesananBukanMilikPemesanError,
    PesananSudahDibatalkanError, PesananTidakDitemukanError, PenggunaTidakDitemukanError)

class PemesananService:
    """Mengelola booking milik Pengguna dan Member."""

    def __init__(self, pengguna_repository, penerbangan_repository, booking_repository, tiket_repository):
        self.pengguna_repository = pengguna_repository
        self.penerbangan_repository = penerbangan_repository
        self.booking_repository = booking_repository
        self.tiket_repository = tiket_repository

    def pesan_tiket(self, aktor_id: str, id_penerbangan: str, konfirmasi: bool = True) -> Booking | None:
        """UC06: simpan booking setelah pengguna mengonfirmasi pemesanan."""
        pengguna = self.pengguna_repository.get_by_id(aktor_id)
        if pengguna is None: raise PenggunaTidakDitemukanError()
        flight = self.penerbangan_repository.get_by_id(id_penerbangan)
        if flight is None: raise PenerbanganTidakDitemukanError()
        if not konfirmasi: return None
        kode = f"BOOK-{uuid4().hex[:12].upper()}"
        booking = Booking(kode, date.today(), BookingStatus.BOOKED, aktor_id)
        self.booking_repository.save(booking)
        self.tiket_repository.save(Tiket(f"TKT-{uuid4().hex[:10].upper()}",
            f"ETK-{kode}", kode, id_penerbangan))
        return booking

    def lihat_daftar_pesanan(self, aktor_id: str) -> list[dict]:
        """UC07: tampilkan semua booking dan tiket milik pengguna."""
        if self.pengguna_repository.get_by_id(aktor_id) is None: raise PenggunaTidakDitemukanError()
        hasil = []
        for booking in self.booking_repository.list_by_pengguna(aktor_id):
            tiket = self.tiket_repository.list_by_booking(booking.kode_booking_reference)
            hasil.append({"booking": booking, "tiket": tiket})
        return hasil

    def batalkan_pesanan(self, aktor_id: str, kode_booking_reference: str,
                         konfirmasi: bool) -> Booking:
        """UC08: tampilkan daftar (include UC07), lalu batalkan booking milik aktor."""
        daftar = self.lihat_daftar_pesanan(aktor_id)
        booking = next((x["booking"] for x in daftar
                        if x["booking"].kode_booking_reference == kode_booking_reference), None)
        if booking is None:
            if self.booking_repository.get_by_reference(kode_booking_reference):
                raise PesananBukanMilikPemesanError()
            raise PesananTidakDitemukanError()
        if booking.status is BookingStatus.CANCELLED: raise PesananSudahDibatalkanError()
        if not konfirmasi: raise KonfirmasiPembatalanDibutuhkanError()
        booking.status = BookingStatus.CANCELLED
        self.booking_repository.save(booking)
        return booking
