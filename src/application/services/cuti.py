"""Service use case cuti UC01-UC02."""
from datetime import date
from src.domain.entities import HRDManajer, Pegawai
from src.domain.exceptions import AksesDitolakError, PegawaiTidakDitemukanError

class CutiService:
    """Menangani pembacaan pengajuan dan riwayat cuti."""

    def __init__(self, pegawai_repository, pengajuan_cuti_repository):
        self.pegawai_repository = pegawai_repository
        self.pengajuan_cuti_repository = pengajuan_cuti_repository

    def _pastikan_hrd(self, aktor_id: str) -> HRDManajer:
        aktor = self.pegawai_repository.get_by_id(aktor_id)
        if not isinstance(aktor, HRDManajer):
            raise AksesDitolakError()
        return aktor

    def lihat_pengajuan_cuti_per_periode(self, aktor_id: str, tanggal: date) -> list[dict]:
        """UC01: tampilkan pengajuan cuti yang beririsan dengan tanggal terpilih."""
        self._pastikan_hrd(aktor_id)
        hasil = []
        for pengajuan in self.pengajuan_cuti_repository.list_all():
            if pengajuan.tanggal_mulai <= tanggal <= pengajuan.tanggal_selesai:
                pegawai = self.pegawai_repository.get_by_id(pengajuan.id_pegawai)
                if pegawai:
                    hasil.append({"id_cuti": pengajuan.id_cuti, "id_pegawai": pegawai.id_pegawai,
                        "nama_pegawai": pegawai.nama, "tanggal_mulai": pengajuan.tanggal_mulai,
                        "tanggal_selesai": pengajuan.tanggal_selesai, "lama_cuti": pengajuan.lama_cuti})
        return hasil

    def lihat_riwayat_dan_sisa_cuti_pegawai(self, aktor_id: str, id_pegawai: str, tahun: int) -> dict:
        """UC02: tampilkan riwayat cuti dan saldo cuti tahun berjalan."""
        self._pastikan_hrd(aktor_id)
        pegawai = self.pegawai_repository.get_by_id(id_pegawai)
        if not isinstance(pegawai, Pegawai):
            raise PegawaiTidakDitemukanError()
        riwayat = [x for x in self.pengajuan_cuti_repository.list_by_pegawai(id_pegawai)
                   if x.tanggal_mulai.year == tahun or x.tanggal_selesai.year == tahun]
        return {"id_pegawai": pegawai.id_pegawai, "nama_pegawai": pegawai.nama,
                "tahun": tahun, "sisa_cuti": pegawai.sisa_cuti, "riwayat": riwayat}
