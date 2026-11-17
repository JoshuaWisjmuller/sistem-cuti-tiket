"""Aturan murni untuk memeriksa kelengkapan profil Member pada UC10-UC11."""

from collections.abc import Mapping

# ASUMSI A5: daftar atribut ini perlu dikonfirmasi kepada dosen.
ATRIBUT_PROFIL_MEMBER_WAJIB = (
    "nama",
    "nomor_identitas",
    "tanggal_lahir",
    "nomor_telepon",
    "email",
)


def periksa_kelengkapan_profil_member(
    data_profil: Mapping[str, object | None],
) -> bool:
    """Periksa atribut wajib profil Member untuk UC10-UC11 tanpa efek samping."""
    for nama_atribut in ATRIBUT_PROFIL_MEMBER_WAJIB:
        nilai = data_profil.get(nama_atribut)
        if nilai is None:
            return False
        if isinstance(nilai, str) and not nilai.strip():
            return False
    return True
