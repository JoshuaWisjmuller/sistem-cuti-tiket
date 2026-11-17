"""API integration test FastAPI untuk UC utama."""
from fastapi.testclient import TestClient
from src.main import create_app

def test_api_uc01_pengajuan_cuti():
    client=TestClient(create_app("/tmp/test-cuti-api.db"))
    response=client.get("/cuti/pengajuan",params={"tanggal":"2026-11-20"},headers={"X-User-Id":"EMP-HRD-001"})
    assert response.status_code==200 and len(response.json())==1

def test_api_uc03_pencarian_penerbangan():
    client=TestClient(create_app("/tmp/test-flight-api.db"))
    response=client.post("/penerbangan/cari",json={"tujuan":"Bali","tanggal":"2026-12-01"},headers={"X-User-Id":"USER-001"})
    assert response.status_code==200 and len(response.json())==2

def test_api_uc14_otorisasi_kode_booking():
    client=TestClient(create_app("/tmp/test-travel-api.db"))
    response=client.get("/travel/booking/BOOK-CONF-001/otorisasi",headers={"X-User-Id":"EMP-TRV-001"})
    assert response.status_code==200 and response.json()["status"]=="confirmed"

def test_api_uc10_profil_tidak_lengkap_mendapat_error_persis():
    client=TestClient(create_app("/tmp/test-profile-api.db"))
    response=client.post("/tiket/TICKET-003/validasi",headers={"X-User-Id":"MEMBER-002"})
    assert response.status_code==409 and response.json()["detail"]=="data profil tidak lengkap"

def test_api_swagger_tersedia():
    client=TestClient(create_app("/tmp/test-docs-api.db"))
    assert client.get("/docs").status_code==200
