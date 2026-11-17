"""Composition root: rakit adapter, service, dan aplikasi FastAPI."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.application.services.cuti import CutiService
from src.application.services.pencarian import PencarianService
from src.application.services.pemesanan import PemesananService
from src.application.services.profil import ProfilService
from src.application.services.manajer_travel import ManajerTravelService
from src.domain.exceptions import DomainError
from src.infrastructure.email_sender import FakeEmailSender
from src.infrastructure.repositories.sqlite import (SQLiteStore, SQLitePegawaiRepository,
    SQLitePengajuanCutiRepository, SQLitePenggunaRepository, SQLiteMaskapaiRepository,
    SQLitePenerbanganRepository, SQLiteBookingRepository, SQLiteTiketRepository)
from src.infrastructure.seed_data import build_seed_data
from src.presentation.routers import router

def create_app(database_path: str = "data/sistem.db", seed: bool = True) -> FastAPI:
    """Bangun aplikasi dan seluruh dependency dari satu composition root."""
    app=FastAPI(title="Sistem Cuti dan Pemesanan Tiket", version="1.0.0",
        description="API UC01-UC18; aktor demo dipilih melalui header X-User-Id.")
    store=SQLiteStore(database_path)
    pegawai=SQLitePegawaiRepository(store); cuti=SQLitePengajuanCutiRepository(store)
    pengguna=SQLitePenggunaRepository(store); maskapai=SQLiteMaskapaiRepository(store)
    penerbangan=SQLitePenerbanganRepository(store); booking=SQLiteBookingRepository(store)
    tiket=SQLiteTiketRepository(store)
    # ASUMSI: seed hanya dimasukkan jika tabel pegawai masih kosong agar data tersimpan tidak ditimpa.
    if seed and not pegawai.list_all():
        demo=build_seed_data()
        for repo_name, table in (("pegawai","pegawai"),("pengajuan_cuti","pengajuan_cuti"),
            ("pengguna","pengguna"),("maskapai","maskapai"),("penerbangan","penerbangan"),
            ("booking","booking"),("tiket","tiket")):
            repo=getattr(demo.repositories,repo_name)
            for item in repo.list_all():
                key_attrs={"pegawai":"id_pegawai","pengajuan_cuti":"id_cuti","pengguna":"id_pengguna",
                    "maskapai":"id_maskapai","penerbangan":"id_penerbangan","booking":"kode_booking_reference","tiket":"id_tiket"}
                store.save(table,getattr(item,key_attrs[table]),item)
    email_sender=FakeEmailSender()
    app.state.cuti=CutiService(pegawai,cuti)
    app.state.pencarian=PencarianService(pengguna,penerbangan,maskapai)
    app.state.pemesanan=PemesananService(pengguna,penerbangan,booking,tiket)
    app.state.profil=ProfilService(pengguna,tiket)
    app.state.travel=ManajerTravelService(pegawai,booking,pengguna,penerbangan,maskapai,tiket,email_sender)
    app.state.email_sender=email_sender
    app.state.store=store
    app.include_router(router)
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        status=403 if "hak akses" in str(exc) else 404 if "tidak ditemukan" in str(exc) or "tidak sesuai" in str(exc) else 409
        return JSONResponse(status_code=status,content={"detail":str(exc)})
    @app.get("/", tags=["Informasi"])
    def root():
        return {"message":"Sistem Cuti dan Pemesanan Tiket API","docs":"/docs"}
    return app

app=create_app()
