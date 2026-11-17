"""Service profil dan validasi tiket UC09-UC11."""
from src.domain.entities import MemberFrequentTraveller
from src.domain.exceptions import (AksesDitolakError, ProfilTidakLengkapError,
    TiketTidakDitemukanError, PenggunaTidakDitemukanError)
from src.domain.profile_rules import periksa_kelengkapan_profil_member

class ProfilService:
    """Mengelola profil Member dan validasi tiket."""

    def __init__(self, pengguna_repository, tiket_repository):
        self.pengguna_repository = pengguna_repository
        self.tiket_repository = tiket_repository

    def perbarui_data_profil(self, aktor_id: str, data: dict) -> MemberFrequentTraveller:
        """UC09: perbarui atribut profil Member."""
        member = self.pengguna_repository.get_by_id(aktor_id)
        if not isinstance(member, MemberFrequentTraveller): raise AksesDitolakError()
        for field in ("nama", "email", "nomor_identitas", "tanggal_lahir", "nomor_telepon"):
            if field in data: setattr(member, field, data[field])
        self.pengguna_repository.save(member)
        return member

    def periksa_kelengkapan_data_profil(self, member: MemberFrequentTraveller) -> bool:
        """UC11 internal: periksa atribut wajib profil Member."""
        return periksa_kelengkapan_profil_member({"nama": member.nama,
            "nomor_identitas": member.nomor_identitas, "tanggal_lahir": member.tanggal_lahir,
            "nomor_telepon": member.nomor_telepon, "email": member.email})

    def validasi_tiket(self, aktor_id: str, id_tiket: str):
        """UC10: validasi tiket hanya jika profil Member lengkap."""
        member = self.pengguna_repository.get_by_id(aktor_id)
        if not isinstance(member, MemberFrequentTraveller): raise AksesDitolakError()
        if not self.periksa_kelengkapan_data_profil(member): raise ProfilTidakLengkapError()
        tiket = self.tiket_repository.get_by_id(id_tiket)
        if tiket is None: raise TiketTidakDitemukanError()
        tiket.sudah_divalidasi = True
        self.tiket_repository.save(tiket)
        return tiket
