"""Adapter SQLite standar-library untuk repository aplikasi."""
import pickle
import sqlite3
from pathlib import Path

class SQLiteStore:
    """Penyimpanan objek domain dalam tabel SQLite terpisah."""

    def __init__(self, database_path: str = "data/app.db"):
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            for table in ("pegawai","pengajuan_cuti","pengguna","maskapai","penerbangan","booking","tiket"):
                connection.execute(f"CREATE TABLE IF NOT EXISTS {table} (item_key TEXT PRIMARY KEY, payload BLOB NOT NULL)")

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def save(self, table: str, key: str, value) -> None:
        payload=sqlite3.Binary(pickle.dumps(value))
        with self._connect() as connection:
            connection.execute(f"INSERT INTO {table}(item_key,payload) VALUES(?,?) ON CONFLICT(item_key) DO UPDATE SET payload=excluded.payload",(key,payload))

    def get(self, table: str, key: str):
        with self._connect() as connection:
            row=connection.execute(f"SELECT payload FROM {table} WHERE item_key=?",(key,)).fetchone()
        return pickle.loads(row[0]) if row else None

    def all(self, table: str):
        with self._connect() as connection:
            rows=connection.execute(f"SELECT payload FROM {table} ORDER BY item_key").fetchall()
        return [pickle.loads(row[0]) for row in rows]

class SQLiteRepository:
    """Repository generik internal yang membatasi operasi pada nama tabel tetap."""
    def __init__(self, store: SQLiteStore, table: str, key_attribute: str):
        self.store=store; self.table=table; self.key_attribute=key_attribute
    def get_by_id(self, key: str): return self.store.get(self.table,key)
    def list_all(self): return self.store.all(self.table)
    def save(self, value): self.store.save(self.table,getattr(value,self.key_attribute),value)

class SQLitePegawaiRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"pegawai","id_pegawai")
class SQLitePengajuanCutiRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"pengajuan_cuti","id_cuti")
    def list_by_pegawai(self,id_pegawai): return [x for x in self.list_all() if x.id_pegawai==id_pegawai]
class SQLitePenggunaRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"pengguna","id_pengguna")
class SQLiteMaskapaiRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"maskapai","id_maskapai")
class SQLitePenerbanganRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"penerbangan","id_penerbangan")
class SQLiteBookingRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"booking","kode_booking_reference")
    def get_by_reference(self,kode): return self.store.get("booking",kode)
    def list_by_pengguna(self,id_pengguna): return [x for x in self.list_all() if x.id_pengguna==id_pengguna]
class SQLiteTiketRepository(SQLiteRepository):
    def __init__(self,s): super().__init__(s,"tiket","id_tiket")
    def list_by_booking(self,kode): return [x for x in self.list_all() if x.id_booking==kode]
