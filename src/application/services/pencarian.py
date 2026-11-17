"""Service pencarian dan perbandingan penerbangan UC03-UC05."""
from datetime import date, time
from decimal import Decimal
from src.domain.entities import MemberFrequentTraveller
from src.domain.exceptions import AksesDitolakError

class PencarianService:
    """Menyediakan pencarian bersama untuk Pengguna dan Member."""

    def __init__(self, pengguna_repository, penerbangan_repository, maskapai_repository):
        self.pengguna_repository = pengguna_repository
        self.penerbangan_repository = penerbangan_repository
        self.maskapai_repository = maskapai_repository

    def _aktor(self, aktor_id: str):
        aktor = self.pengguna_repository.get_by_id(aktor_id)
        if aktor is None:
            raise AksesDitolakError()
        return aktor

    def _format_hasil(self, penerbangan):
        maskapai = self.maskapai_repository.get_by_id(penerbangan.id_maskapai)
        return {"id_penerbangan": penerbangan.id_penerbangan,
            "lokasi_keberangkatan": penerbangan.lokasi_keberangkatan, "tujuan": penerbangan.tujuan,
            "tanggal": penerbangan.tanggal, "jam_keberangkatan": penerbangan.jam_keberangkatan,
            "harga": penerbangan.harga, "id_maskapai": penerbangan.id_maskapai,
            "nama_maskapai": maskapai.nama_maskapai if maskapai else None}

    def cari_penerbangan(self, aktor_id: str, tujuan: str, tanggal: date | None = None,
                         harga_maksimum: Decimal | None = None,
                         jam_keberangkatan: time | None = None) -> list[dict]:
        """UC03: cari berdasarkan tujuan, tanggal, harga, dan jam khusus Member."""
        aktor = self._aktor(aktor_id)
        if jam_keberangkatan is not None and not isinstance(aktor, MemberFrequentTraveller):
            raise AksesDitolakError()
        hasil = []
        for flight in self.penerbangan_repository.list_all():
            if flight.tujuan.casefold() != tujuan.casefold(): continue
            if tanggal is not None and flight.tanggal != tanggal: continue
            if harga_maksimum is not None and flight.harga > harga_maksimum: continue
            if jam_keberangkatan is not None and flight.jam_keberangkatan < jam_keberangkatan: continue
            hasil.append(self._format_hasil(flight))
        return hasil

    def cari_penerbangan_multi_destinasi(self, aktor_id: str, tanggal: date,
            lokasi_keberangkatan: str, tujuan: list[str]) -> dict:
        """UC04: cari penerbangan untuk beberapa tujuan tanpa menyediakan pemesanan."""
        self._aktor(aktor_id)
        hasil = {}
        for target in tujuan:
            flights = [f for f in self.penerbangan_repository.list_all()
                       if f.tanggal == tanggal
                       and f.lokasi_keberangkatan.casefold() == lokasi_keberangkatan.casefold()
                       and f.tujuan.casefold() == target.casefold()]
            hasil[target] = [self._format_hasil(f) for f in flights]
        return hasil

    def bandingkan_harga_penerbangan(self, aktor_id: str, hasil_pencarian: list[dict]) -> dict:
        """UC05: bandingkan harga dan jumlah penerbangan khusus Member."""
        if not isinstance(self._aktor(aktor_id), MemberFrequentTraveller):
            raise AksesDitolakError()
        harga = [item["harga"] for item in hasil_pencarian]
        return {"jumlah_penerbangan": len(hasil_pencarian), "harga": harga,
                "harga_terendah": min(harga) if harga else None,
                "harga_tertinggi": max(harga) if harga else None}
