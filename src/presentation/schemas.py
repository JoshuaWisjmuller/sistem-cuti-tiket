"""Skema request API untuk UC01-UC18."""
from datetime import date, time
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProfileUpdateRequest(BaseModel):
    nama: str | None = None
    email: str | None = None
    nomor_identitas: str | None = None
    tanggal_lahir: date | None = None
    nomor_telepon: str | None = None

class BookingRequest(BaseModel):
    id_penerbangan: str
    konfirmasi: bool = True

class CancelRequest(BaseModel):
    konfirmasi: bool

class SearchRequest(BaseModel):
    tujuan: str
    tanggal: date | None = None
    harga_maksimum: Decimal | None = Field(default=None, ge=0)
    jam_keberangkatan: time | None = None

class MultiSearchRequest(BaseModel):
    tanggal: date
    lokasi_keberangkatan: str
    tujuan: list[str] = Field(min_length=1)

class CompareRequest(BaseModel):
    hasil_pencarian: list[dict]

class GuestBookingRequest(BaseModel):
    id_pengunjung: str
    id_penerbangan: str
