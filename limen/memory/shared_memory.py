"""Mémoire partagée persistante de Limen.

Cette mémoire est volontairement simple dans cette version :
elle s'appuie sur un fichier JSON local afin d'offrir un point de départ
clair, testable et facilement remplaçable.
"""

from __future__ import annotations

import json
from pathlib import Path

from limen.core.schemas import MemoryRecord


class SharedMemory:
    """Stockage clé-valeur minimal pour partager le contexte entre agents."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._write_records([])

    def _read_records(self) -> list[dict]:
        """Lit l'ensemble des enregistrements stockés."""
        return json.loads(self.storage_path.read_text(encoding="utf-8"))

    def _write_records(self, records: list[dict]) -> None:
        """Écrit la liste complète des enregistrements en JSON."""
        self.storage_path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def append(self, record: MemoryRecord) -> None:
        """Ajoute un nouvel enregistrement en mémoire partagée."""
        records = self._read_records()
        records.append(record.model_dump())
        self._write_records(records)

    def fetch_context(self, limit: int = 10) -> str:
        """Construit un contexte textuel compact à partir des dernières entrées."""
        records = self._read_records()[-limit:]
        lines: list[str] = []
        for item in records:
            lines.append(f"- key={item['key']} | source={item['source']} | value={item['value']}")
        return "\n".join(lines)
