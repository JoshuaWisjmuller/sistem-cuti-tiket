# Sistem Cuti Pegawai dan Pemesanan Tiket Pesawat

Backend Python 3.12 berdasarkan laporan analisis (US1–US9, Domain Model, UC01–UC18, dan Activity Diagram). Implementasi menggunakan FastAPI, Pydantic, SQLite `sqlite3`, dan pytest. Tidak ada frontend khusus; interaksi manual dilakukan melalui Swagger UI.

## 1. Persyaratan

- Python 3.12
- pip
- Terminal (PowerShell, CMD, atau bash)

## 2. Instalasi

Jalankan dari folder yang berisi `pyproject.toml`.

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

Install aplikasi dan dependency pengujian:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 3. Menjalankan aplikasi

Satu perintah untuk menjalankan server:

```bash
uvicorn src.main:app --reload
```

Buka Swagger UI:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

Database SQLite dibuat otomatis di `data/sistem.db`. Seed data dimasukkan hanya ketika tabel pegawai masih kosong. Menghapus file database akan membuat seed data dimasukkan kembali saat aplikasi dimulai.

## 4. Menjalankan seluruh test

Suite saat ini berisi **55 test otomatis** (domain, infrastructure, application, dan API); hasil verifikasi pada paket ini: seluruhnya lulus.

Satu perintah untuk semua test:

```bash
python -m pytest
```

Test service memakai repository in-memory; test API menggunakan SQLite sementara dan FastAPI TestClient. Test tidak memerlukan server berjalan.

## 5. Identitas aktor demo

Sistem belum memakai autentikasi. **ASUMSI A1 pada instruksi implementasi:** aktor ditentukan lewat header `X-User-Id`; peran diambil dari objek yang tersimpan, bukan dari nilai role yang dikirim klien.

| Aktor | Header `X-User-Id` | Kegunaan |
|---|---|---|
| HRD Manajer | `EMP-HRD-001` | UC01–UC02 |
| Manajer Travel | `EMP-TRV-001` | UC12–UC17 |
| Pengguna | `USER-001` | UC03, UC04, UC06–UC08, UC17 sebagai pengunjung |
| Member profil lengkap | `MEMBER-001` | UC03–UC11 |
| Member profil belum lengkap | `MEMBER-002` | Uji penolakan UC10 |

Masukkan header tersebut pada tombol **Authorize** di Swagger atau pada parameter header masing-masing endpoint.

## 6. Seed data penting

| Jenis | ID / nilai |
|---|---|
| Pegawai | `EMP-001`, `EMP-002` |
| Pengajuan cuti | 20–22 November 2026; 25–26 November 2026; 2–4 Desember 2026 |
| Maskapai | `AIR-001`, `AIR-002` |
| Penerbangan | `FLIGHT-001` s.d. `FLIGHT-004` |
| Tujuan | Bali, Surabaya, Yogyakarta |
| Booking | `BOOK-CONF-001`, `BOOK-NEW-001`, `BOOK-WAIT-001`, `BOOK-CANCEL-001` |
| Tiket | `TICKET-001` s.d. `TICKET-004` |

Semua nama, harga, jadwal, dan identitas pada seed merupakan data fiktif untuk demonstrasi.

## 7. Contoh mencoba API

### UC01 – Pengajuan cuti pada tanggal tertentu

`GET /cuti/pengajuan?tanggal=2026-11-20`

Header: `X-User-Id: EMP-HRD-001`

### UC02 – Riwayat dan saldo cuti

`GET /cuti/pegawai/EMP-001/riwayat?tahun=2026`

Header: `X-User-Id: EMP-HRD-001`

### UC03 – Cari penerbangan

`POST /penerbangan/cari`

Header: `X-User-Id: USER-001`

```json
{
  "tujuan": "Bali",
  "tanggal": "2026-12-01",
  "harga_maksimum": 1300000
}
```

Untuk Member, tambahkan `"jam_keberangkatan": "09:00:00"` dan gunakan `MEMBER-001`.

### UC04 – Pencarian multi-destinasi

`POST /penerbangan/multi-destinasi`

```json
{
  "tanggal": "2026-12-01",
  "lokasi_keberangkatan": "Jakarta",
  "tujuan": ["Bali", "Surabaya", "Yogyakarta"]
}
```

Header: `X-User-Id: USER-001`. UC04 hanya menghasilkan pencarian; tidak ada pemesanan dari hasil multi-destinasi (A7).

### UC05 – Bandingkan harga

`POST /penerbangan/bandingkan`

Header: `X-User-Id: MEMBER-001`

Kirim `hasil_pencarian` berupa array hasil UC03 atau UC04. Endpoint membandingkan harga dan jumlah penerbangan.

### UC06 – Pesan tiket

`POST /booking`

Header: `X-User-Id: USER-001`

```json
{
  "id_penerbangan": "FLIGHT-001",
  "konfirmasi": true
}
```

### UC07 – Daftar pesanan

`GET /booking/saya`

Header: `X-User-Id: USER-001`

### UC08 – Batalkan pesanan

`POST /booking/BOOK-CONF-001/batalkan`

Header: `X-User-Id: USER-001`

```json
{"konfirmasi": true}
```

### UC09 – Perbarui profil Member

`PUT /profil`

Header: `X-User-Id: MEMBER-002`

```json
{
  "nomor_telepon": "081234567890"
}
```

### UC10 – Validasi tiket

`POST /tiket/TICKET-002/validasi`

Header: `X-User-Id: MEMBER-001`

Untuk mencoba alur alternatif profil tidak lengkap, gunakan `MEMBER-002` dan `TICKET-003`. API mengembalikan detail persis `data profil tidak lengkap`.

### UC12 – Lihat status booking

`GET /travel/booking`

Header: `X-User-Id: EMP-TRV-001`

### UC13 – Filter status

`GET /travel/booking/filter?status=booked`

Nilai status yang diterima: `confirmed`, `booked`, `waiting for the payment`, `dibatalkan`.

### UC14 – Otorisasi tiket

`GET /travel/booking/BOOK-CONF-001/otorisasi`

Header: `X-User-Id: EMP-TRV-001`

Kode tidak valid menghasilkan detail persis `kode booking reference tidak sesuai`. Proses ini hanya membaca status booking.

### UC16 – Cari tiket untuk pengunjung

`GET /travel/penerbangan?tujuan=Bali`

Header: `X-User-Id: EMP-TRV-001`

### UC17 – Pesan tiket untuk pengunjung

`POST /travel/booking`

Header: `X-User-Id: EMP-TRV-001`

```json
{
  "id_pengunjung": "USER-001",
  "id_penerbangan": "FLIGHT-001"
}
```

Booking muncul pada `GET /booking/saya` dengan header `X-User-Id: USER-001`. Email e-tiket ditampung oleh `FakeEmailSender` dalam proses aplikasi; tidak ada email sungguhan yang dikirim.

## 8. Struktur proyek

```text
sistem_cuti_tiket/
├── src/
│   ├── domain/
│   │   ├── entities.py
│   │   ├── enums.py
│   │   ├── exceptions.py
│   │   └── profile_rules.py
│   ├── application/
│   │   ├── ports/
│   │   │   ├── repositories.py
│   │   │   └── email_sender.py
│   │   └── services/
│   │       ├── cuti.py
│   │       ├── pencarian.py
│   │       ├── pemesanan.py
│   │       ├── profil.py
│   │       └── manajer_travel.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   ├── in_memory.py
│   │   │   └── sqlite.py
│   │   ├── email_sender.py
│   │   └── seed_data.py
│   ├── presentation/
│   │   ├── routers.py
│   │   └── schemas.py
│   └── main.py
├── tests/
│   ├── domain/
│   ├── infrastructure/
│   ├── application/
│   └── presentation/
├── data/                    # dibuat otomatis
├── IMPLEMENTATION_GUIDE.md
├── README.md
└── pyproject.toml
```

## 9. Traceability UC → endpoint → service → test

UC11, UC15, dan UC18 adalah proses internal sesuai laporan, sehingga tidak mempunyai endpoint mandiri.

| UC | Endpoint | Service method | Test utama |
|---|---|---|---|
| UC01 | `GET /cuti/pengajuan` | `CutiService.lihat_pengajuan_cuti_per_periode` | `test_uc01_*` |
| UC02 | `GET /cuti/pegawai/{id}/riwayat` | `CutiService.lihat_riwayat_dan_sisa_cuti_pegawai` | `test_uc02_*` |
| UC03 | `POST /penerbangan/cari` | `PencarianService.cari_penerbangan` | `test_uc03_*` |
| UC04 | `POST /penerbangan/multi-destinasi` | `PencarianService.cari_penerbangan_multi_destinasi` | `test_uc04_*` |
| UC05 | `POST /penerbangan/bandingkan` | `PencarianService.bandingkan_harga_penerbangan` | `test_uc05_*` |
| UC06 | `POST /booking` | `PemesananService.pesan_tiket` | `test_uc06_*` |
| UC07 | `GET /booking/saya` | `PemesananService.lihat_daftar_pesanan` | `test_uc07_*` |
| UC08 | `POST /booking/{kode}/batalkan` | `PemesananService.batalkan_pesanan` (memanggil UC07) | `test_uc08_*` |
| UC09 | `PUT /profil` | `ProfilService.perbarui_data_profil` | `test_uc09_*` |
| UC10 | `POST /tiket/{id}/validasi` | `ProfilService.validasi_tiket` (memanggil UC11) | `test_uc10_*` |
| UC11 | Internal | `ProfilService.periksa_kelengkapan_data_profil` | `test_uc11_*` |
| UC12 | `GET /travel/booking` | `ManajerTravelService.lihat_status_booking` | `test_uc12_*` |
| UC13 | `GET /travel/booking/filter` | `ManajerTravelService.filter_status_booking` (memanggil UC12) | `test_uc13_*` |
| UC14 | `GET /travel/booking/{kode}/otorisasi` | `ManajerTravelService.otorisasi_tiket` (memanggil UC15) | `test_uc14_*` |
| UC15 | Internal | `ManajerTravelService.verifikasi_kode_booking_reference` | `test_uc15_*` |
| UC16 | `GET /travel/penerbangan` | `ManajerTravelService.cari_tiket_untuk_pengunjung` | `test_uc16_*` |
| UC17 | `POST /travel/booking` | `ManajerTravelService.pesan_tiket_untuk_pengunjung` (memanggil UC18) | `test_uc17_*` |
| UC18 | Internal | `ManajerTravelService.kirim_e_tiket` | `test_uc18_*` |

## 10. Asumsi dan batasan

- **A1 – identifikasi aktor:** header `X-User-Id`; role diperiksa dari data domain. Ini bukan autentikasi dan tidak aman untuk produksi.
- **A2 – pengunjung:** direpresentasikan sebagai `Pengguna` terdaftar dengan email.
- **A3 – pengajuan cuti:** pembuatan pengajuan cuti di luar cakupan; data disediakan melalui seed.
- **A4 – otorisasi:** UC14 hanya membaca status booking dan tidak mengubah data.
- **A5 – profil lengkap:** nama, nomor identitas, tanggal lahir, nomor telepon, email. Daftar satu sumber di `ATRIBUT_PROFIL_MEMBER_WAJIB`; perlu konfirmasi dosen.
- **A6 – waktu email:** e-tiket dikirim setelah booking tersimpan; pengiriman palsu hanya merekam email pada list.
- **A7 – multi-destinasi:** UC04 tidak menyediakan pemesanan.
- **A8 – pembayaran/refund:** tidak diimplementasikan. Status awal booking baru adalah `booked`; pembatalan hanya mengubah status menjadi `dibatalkan`.
- **ASUMSI tambahan:** `Tiket.sudah_divalidasi` mewakili pascakondisi UC10. Harga, jadwal, dan identitas seed bersifat fiktif.
- **Batasan penyimpanan:** SQLite menggunakan `sqlite3` standar dan menyimpan payload objek Python sebagai BLOB ter-serialisasi. Database ditujukan untuk aplikasi demo lokal, bukan format interoperabilitas data eksternal.

## 11. Panduan implementasi terperinci

Lihat [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) untuk urutan implementasi dari ZIP Langkah 1, penjelasan layer, cara menjalankan, skenario Swagger, pengujian, dan checklist peninjauan prinsip kode.
