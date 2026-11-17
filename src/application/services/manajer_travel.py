"""Service Manajer Travel UC12-UC18."""
from datetime import date
from uuid import uuid4
from src.domain.entities import ManajerTravel, Booking, Tiket
from src.domain.enums import BookingStatus
from src.domain.exceptions import (AksesDitolakError, KodeBookingTidakSesuaiError,
    DataPengunjungTidakDitemukanError, PenerbanganTidakDitemukanError)
class ManajerTravelService:
    """Menangani status booking, otorisasi, dan pemesanan pengunjung."""

    def __init__(self, pegawai_repository, booking_repository, pengguna_repository,
                 penerbangan_repository, maskapai_repository, tiket_repository, email_sender):
        self.pegawai_repository=pegawai_repository; self.booking_repository=booking_repository
        self.pengguna_repository=pengguna_repository; self.penerbangan_repository=penerbangan_repository
        self.maskapai_repository=maskapai_repository; self.tiket_repository=tiket_repository
        self.email_sender=email_sender

    def _pastikan_manajer(self, aktor_id):
        aktor=self.pegawai_repository.get_by_id(aktor_id)
        if not isinstance(aktor, ManajerTravel): raise AksesDitolakError()
        return aktor

    def lihat_status_booking(self, aktor_id: str) -> list[Booking]:
        """UC12: tampilkan seluruh booking dan statusnya."""
        self._pastikan_manajer(aktor_id)
        return list(self.booking_repository.list_all())

    def filter_status_booking(self, aktor_id: str, status: BookingStatus) -> list[Booking]:
        """UC13: filter hasil UC12 menurut status booking."""
        daftar=self.lihat_status_booking(aktor_id)
        return [b for b in daftar if b.status is status]

    def verifikasi_kode_booking_reference(self, kode: str) -> Booking:
        """UC15 internal: pastikan kode booking reference terdaftar."""
        booking=self.booking_repository.get_by_reference(kode)
        if booking is None: raise KodeBookingTidakSesuaiError()
        return booking

    def otorisasi_tiket(self, aktor_id: str, kode: str) -> Booking:
        """UC14: verifikasi kode dan tampilkan status tanpa mengubah booking."""
        self._pastikan_manajer(aktor_id)
        return self.verifikasi_kode_booking_reference(kode)

    def cari_tiket_untuk_pengunjung(self, aktor_id: str, tujuan: str) -> list[dict]:
        """UC16: cari penerbangan untuk tujuan yang diminta Manajer Travel."""
        self._pastikan_manajer(aktor_id)
        hasil=[]
        for f in self.penerbangan_repository.list_all():
            if f.tujuan.casefold()==tujuan.casefold():
                airline=self.maskapai_repository.get_by_id(f.id_maskapai)
                hasil.append({"penerbangan":f,"maskapai":airline})
        return hasil

    def kirim_e_tiket(self, email: str, tiket: Tiket) -> None:
        """UC18 internal: kirim representasi e-tiket melalui port EmailSender."""
        self.email_sender.send_email(email, "E-tiket penerbangan",
            f"Kode e-tiket: {tiket.e_tiket}; ID penerbangan: {tiket.id_penerbangan}")

    def pesan_tiket_untuk_pengunjung(self, aktor_id: str, id_pengunjung: str,
                                      id_penerbangan: str) -> dict:
        """UC17: simpan booking atas nama pengunjung dan kirim e-tiket (include UC18)."""
        manajer=self._pastikan_manajer(aktor_id)
        pengunjung=self.pengguna_repository.get_by_id(id_pengunjung)
        if pengunjung is None: raise DataPengunjungTidakDitemukanError()
        flight=self.penerbangan_repository.get_by_id(id_penerbangan)
        if flight is None: raise PenerbanganTidakDitemukanError()
        kode=f"BOOK-{uuid4().hex[:12].upper()}"
        booking=Booking(kode,date.today(),BookingStatus.BOOKED,id_pengunjung,manajer.id_pegawai)
        tiket=Tiket(f"TKT-{uuid4().hex[:10].upper()}",f"ETK-{kode}",kode,id_penerbangan)
        self.booking_repository.save(booking); self.tiket_repository.save(tiket)
        self.kirim_e_tiket(pengunjung.email,tiket)
        return {"booking":booking,"tiket":tiket,"email":pengunjung.email}
