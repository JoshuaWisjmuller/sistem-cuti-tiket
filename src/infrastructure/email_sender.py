"""Fake EmailSender untuk pengujian UC17-UC18 tanpa layanan email eksternal."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SentEmail:
    """Representasi email yang ditampung oleh fake sender untuk UC18."""

    recipient: str
    subject: str
    body: str


class FakeEmailSender:
    """Adapter EmailSender yang menyimpan pesan terkirim di dalam list untuk UC18."""

    def __init__(self) -> None:
        """Siapkan list email palsu untuk UC18."""
        self.sent_emails: list[SentEmail] = []

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        """Simpan email ke list lokal sebagai pengganti pengiriman pada UC18."""
        self.sent_emails.append(SentEmail(recipient, subject, body))
