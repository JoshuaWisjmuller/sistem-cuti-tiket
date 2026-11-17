"""Pengujian service untuk UC01-UC18."""
from datetime import date, time
from decimal import Decimal
import pytest
from src.infrastructure.seed_data import build_seed_data
from src.application.services.cuti import CutiService
from src.application.services.pencarian import PencarianService
from src.application.services.pemesanan import PemesananService
from src.application.services.profil import ProfilService
from src.application.services.manajer_travel import ManajerTravelService
from src.domain.enums import BookingStatus
from src.domain.exceptions import *

@pytest.fixture
def services():
    seed=build_seed_data(); r=seed.repositories
    return seed, CutiService(r.pegawai,r.pengajuan_cuti), PencarianService(r.pengguna,r.penerbangan,r.maskapai), PemesananService(r.pengguna,r.penerbangan,r.booking,r.tiket), ProfilService(r.pengguna,r.tiket), ManajerTravelService(r.pegawai,r.booking,r.pengguna,r.penerbangan,r.maskapai,r.tiket,seed.email_sender)

def test_uc01_hrd_melihat_pengajuan_per_tanggal(services):
    _,cuti,*_=services
    result=cuti.lihat_pengajuan_cuti_per_periode("EMP-HRD-001",date(2026,11,20))
    assert len(result)==1 and result[0]["nama_pegawai"]=="Andi Pratama"

def test_uc01_periode_kosong_mengembalikan_list_kosong(services):
    _,cuti,*_=services
    assert cuti.lihat_pengajuan_cuti_per_periode("EMP-HRD-001",date(2026,1,1))==[]

def test_uc02_hrd_melihat_riwayat_dan_sisa_cuti(services):
    _,cuti,*_=services
    result=cuti.lihat_riwayat_dan_sisa_cuti_pegawai("EMP-HRD-001","EMP-001",2026)
    assert result["sisa_cuti"]==8 and len(result["riwayat"])==2

def test_uc03_pengguna_mencari_penerbangan(services):
    _,_,search,*_=services
    assert len(search.cari_penerbangan("USER-001","Bali",date(2026,12,1)))==2

def test_uc03_penerbangan_tidak_ditemukan_mengembalikan_list_kosong(services):
    _,_,search,*_=services
    assert search.cari_penerbangan("USER-001","Tokyo")==[]

def test_uc03_member_dapat_memfilter_jam_keberangkatan(services):
    _,_,search,*_=services
    result=search.cari_penerbangan("MEMBER-001","Bali",jam_keberangkatan=time(9,0))
    assert len(result)==1

def test_uc04_multi_destinasi_menampilkan_tiap_tujuan(services):
    _,_,search,*_=services
    result=search.cari_penerbangan_multi_destinasi("USER-001",date(2026,12,1),"Jakarta",["Bali","Surabaya","Tokyo"])
    assert len(result["Bali"])==2 and result["Tokyo"]==[]

def test_uc05_member_membandingkan_harga(services):
    _,_,search,*_=services
    flights=search.cari_penerbangan("MEMBER-001","Bali")
    result=search.bandingkan_harga_penerbangan("MEMBER-001",flights)
    assert result["jumlah_penerbangan"]==2 and result["harga_terendah"]==Decimal("980000")

def test_uc06_pengguna_membuat_booking_dan_tiket(services):
    _,_,_,orders,*_=services
    booking=orders.pesan_tiket("USER-001","FLIGHT-001")
    assert booking.status is BookingStatus.BOOKED and len(orders.lihat_daftar_pesanan("USER-001"))==3

def test_uc06_pemesanan_tidak_dikonfirmasi_tidak_menyimpan_booking(services):
    _,_,_,orders,*_=services
    before=len(orders.booking_repository.list_all())
    assert orders.pesan_tiket("USER-001","FLIGHT-001",False) is None
    assert len(orders.booking_repository.list_all())==before

def test_uc07_daftar_pesanan_pengguna(services):
    _,_,_,orders,*_=services
    assert len(orders.lihat_daftar_pesanan("USER-001"))==2

def test_uc08_pengguna_membatalkan_pesanan_miliknya(services):
    _,_,_,orders,*_=services
    result=orders.batalkan_pesanan("USER-001","BOOK-CONF-001",True)
    assert result.status is BookingStatus.CANCELLED

def test_uc08_pembatalan_ditolak_jika_bukan_milik_pemesan(services):
    _,_,_,orders,*_=services
    with pytest.raises(PesananBukanMilikPemesanError):
        orders.batalkan_pesanan("MEMBER-001","BOOK-CONF-001",True)

def test_uc08_pembatalan_ditolak_jika_sudah_dibatalkan(services):
    _,_,_,orders,*_=services
    with pytest.raises(PesananSudahDibatalkanError):
        orders.batalkan_pesanan("USER-001","BOOK-CANCEL-001",True)

def test_uc08_pembatalan_membutuhkan_konfirmasi(services):
    _,_,_,orders,*_=services
    with pytest.raises(KonfirmasiPembatalanDibutuhkanError):
        orders.batalkan_pesanan("USER-001","BOOK-CONF-001",False)

def test_uc09_member_memperbarui_profil(services):
    _,_,_,_,profile,*_=services
    result=profile.perbarui_data_profil("MEMBER-002",{"nomor_telepon":"081234"})
    assert result.nomor_telepon=="081234"

def test_uc10_validasi_tiket_ditolak_jika_profil_tidak_lengkap(services):
    _,_,_,_,profile,*_=services
    with pytest.raises(ProfilTidakLengkapError,match="^data profil tidak lengkap$"):
        profile.validasi_tiket("MEMBER-002","TICKET-003")

def test_uc10_member_dengan_profil_lengkap_memvalidasi_tiket(services):
    _,_,_,_,profile,*_=services
    assert profile.validasi_tiket("MEMBER-001","TICKET-002").sudah_divalidasi

def test_uc11_periksa_profil_lengkap(services):
    _,_,_,_,profile,*_=services
    member=profile.pengguna_repository.get_by_id("MEMBER-001")
    assert profile.periksa_kelengkapan_data_profil(member)

def test_uc12_manajer_melihat_semua_status_booking(services):
    _,_,_,_,_,travel=services
    assert len(travel.lihat_status_booking("EMP-TRV-001"))==4

def test_uc13_manajer_memfilter_status_booking(services):
    _,_,_,_,_,travel=services
    assert len(travel.filter_status_booking("EMP-TRV-001",BookingStatus.BOOKED))==1

def test_uc14_otorisasi_membaca_status_tanpa_mengubah_booking(services):
    _,_,_,_,_,travel=services
    before=travel.booking_repository.get_by_reference("BOOK-CONF-001").status
    result=travel.otorisasi_tiket("EMP-TRV-001","BOOK-CONF-001")
    assert result.status is before

def test_uc15_kode_booking_salah_menghasilkan_pesan_persis(services):
    _,_,_,_,_,travel=services
    with pytest.raises(KodeBookingTidakSesuaiError,match="^kode booking reference tidak sesuai$"):
        travel.otorisasi_tiket("EMP-TRV-001","SALAH")

def test_uc16_manajer_mencari_tiket_berdasarkan_tujuan(services):
    _,_,_,_,_,travel=services
    assert len(travel.cari_tiket_untuk_pengunjung("EMP-TRV-001","Bali"))==2

def test_uc17_manajer_memesan_untuk_pengunjung_dan_kirim_email(services):
    seed,_,_,_,_,travel=services
    result=travel.pesan_tiket_untuk_pengunjung("EMP-TRV-001","USER-001","FLIGHT-001")
    assert result["booking"].id_pengguna=="USER-001"
    assert seed.email_sender.sent_emails[-1].recipient=="dewi@example.test"

def test_uc17_data_pengunjung_tidak_ditemukan_tidak_menyimpan(services):
    _,_,_,_,_,travel=services
    before=len(travel.booking_repository.list_all())
    with pytest.raises(DataPengunjungTidakDitemukanError):
        travel.pesan_tiket_untuk_pengunjung("EMP-TRV-001","GUEST-X","FLIGHT-001")
    assert len(travel.booking_repository.list_all())==before

def test_uc18_email_dikirim_melalui_fake_sender(services):
    seed,_,_,_,_,travel=services
    travel.pesan_tiket_untuk_pengunjung("EMP-TRV-001","USER-001","FLIGHT-001")
    assert len(seed.email_sender.sent_emails)==1
