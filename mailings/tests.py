from __future__ import annotations

import io
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from mailings.models import MailingMessage


def _make_xlsx(rows: list[list[object]]) -> Path:
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    for r in rows:
        ws.append(r)

    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp.close()
    wb.save(tmp.name)
    return Path(tmp.name)


class ImportMailingsCommandTests(TestCase):
    def test_import_creates_messages_and_skips_duplicates(self) -> None:
        xlsx = _make_xlsx(
            [
                ["external_id", "user_id", "email", "subject", "message"],
                ["ext-1", "u1", "u1@example.com", "Тема 1", "Текст 1"],
                ["ext-2", "u2", "u2@example.com", "Тема 2", "Текст 2"],
                ["ext-1", "u1", "u1@example.com", "Тема 1", "Текст 1 (дубль)"],
            ]
        )

        out = io.StringIO()
        call_command("import_mailings", str(xlsx), send_delay_ms=0, stdout=out)

        self.assertEqual(MailingMessage.objects.count(), 2)
        self.assertTrue(MailingMessage.objects.filter(external_id="ext-1").exists())
        self.assertTrue(MailingMessage.objects.filter(external_id="ext-2").exists())

        text = out.getvalue()
        self.assertIn("обработано строк: 3", text)
        self.assertIn("создано записей: 2", text)
        self.assertIn("пропущено записей: 1", text)
        self.assertIn("ошибочных строк: 0", text)

    def test_import_counts_invalid_rows(self) -> None:
        xlsx = _make_xlsx(
            [
                ["external_id", "user_id", "email", "subject", "message"],
                ["ext-1", "u1", "u1@example.com", "Тема 1", "Текст 1"],
                ["", "u2", "u2@example.com", "Тема 2", "Текст 2"],  # нет external_id
                ["ext-3", "", "u3@example.com", "Тема 3", "Текст 3"],  # нет user_id
            ]
        )

        out = io.StringIO()
        call_command("import_mailings", str(xlsx), send_delay_ms=0, stdout=out)

        self.assertEqual(MailingMessage.objects.count(), 1)
        text = out.getvalue()
        self.assertIn("обработано строк: 3", text)
        self.assertIn("создано записей: 1", text)
        self.assertIn("ошибочных строк: 2", text)

