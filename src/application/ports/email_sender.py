"""Port pengiriman e-tiket yang dipakai oleh UC17-UC18."""

from typing import Protocol


class EmailSender(Protocol):
    """Kontrak pengiriman email agar application tidak terikat layanan email."""

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        """Kirim e-tiket ke email terdaftar pengunjung untuk UC18."""
