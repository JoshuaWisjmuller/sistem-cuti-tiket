"""Router HTTP: menerjemahkan request ke service UC01-UC18."""
from datetime import date
from fastapi import APIRouter, Header, Request, HTTPException
from src.domain.enums import BookingStatus
from src.domain.exceptions import DomainError
from src.presentation.schemas import (BookingRequest, CancelRequest, SearchRequest,
    MultiSearchRequest, CompareRequest, ProfileUpdateRequest, GuestBookingRequest)

router=APIRouter()

def actor(x_user_id: str | None):
    if not x_user_id: raise HTTPException(status_code=400, detail="header X-User-Id wajib diisi")
    return x_user_id

@router.get("/cuti/pengajuan")
def uc01(request: Request, tanggal: date, x_user_id: str | None=Header(default=None)):
    return request.app.state.cuti.lihat_pengajuan_cuti_per_periode(actor(x_user_id),tanggal)

@router.get("/cuti/pegawai/{id_pegawai}/riwayat")
def uc02(id_pegawai: str, tahun: int, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.cuti.lihat_riwayat_dan_sisa_cuti_pegawai(actor(x_user_id),id_pegawai,tahun)

@router.post("/penerbangan/cari")
def uc03(body: SearchRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pencarian.cari_penerbangan(actor(x_user_id),body.tujuan,body.tanggal,body.harga_maksimum,body.jam_keberangkatan)

@router.post("/penerbangan/multi-destinasi")
def uc04(body: MultiSearchRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pencarian.cari_penerbangan_multi_destinasi(actor(x_user_id),body.tanggal,body.lokasi_keberangkatan,body.tujuan)

@router.post("/penerbangan/bandingkan")
def uc05(body: CompareRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pencarian.bandingkan_harga_penerbangan(actor(x_user_id),body.hasil_pencarian)

@router.post("/booking")
def uc06(body: BookingRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pemesanan.pesan_tiket(actor(x_user_id),body.id_penerbangan,body.konfirmasi)

@router.get("/booking/saya")
def uc07(request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pemesanan.lihat_daftar_pesanan(actor(x_user_id))

@router.post("/booking/{kode_booking_reference}/batalkan")
def uc08(kode_booking_reference: str, body: CancelRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.pemesanan.batalkan_pesanan(actor(x_user_id),kode_booking_reference,body.konfirmasi)

@router.put("/profil")
def uc09(body: ProfileUpdateRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.profil.perbarui_data_profil(actor(x_user_id),body.model_dump(exclude_unset=True))

@router.post("/tiket/{id_tiket}/validasi")
def uc10(id_tiket: str, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.profil.validasi_tiket(actor(x_user_id),id_tiket)

@router.get("/travel/booking")
def uc12(request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.travel.lihat_status_booking(actor(x_user_id))

@router.get("/travel/booking/filter")
def uc13(status: BookingStatus, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.travel.filter_status_booking(actor(x_user_id),status)

@router.get("/travel/booking/{kode_booking_reference}/otorisasi")
def uc14(kode_booking_reference: str, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.travel.otorisasi_tiket(actor(x_user_id),kode_booking_reference)

@router.get("/travel/penerbangan")
def uc16(tujuan: str, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.travel.cari_tiket_untuk_pengunjung(actor(x_user_id),tujuan)

@router.post("/travel/booking")
def uc17(body: GuestBookingRequest, request: Request, x_user_id: str | None=Header(default=None)):
    return request.app.state.travel.pesan_tiket_untuk_pengunjung(actor(x_user_id),body.id_pengunjung,body.id_penerbangan)
