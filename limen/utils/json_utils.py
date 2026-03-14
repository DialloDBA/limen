"""Utilitaires JSON robustes pour parser les réponses d'agents."""

from __future__ import annotations

import json
import re
from typing import Any


_JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)


def extract_json_object(text: str) -> dict[str, Any]:
    """Extrait le premier objet JSON détecté dans un texte.

    Cette approche est utile lorsqu'un modèle renvoie du texte parasite
    autour d'une structure JSON attendue.
    """
    candidate = text.strip()
    if candidate.startswith("{") and candidate.endswith("}"):
        return json.loads(candidate)

    match = _JSON_BLOCK_PATTERN.search(candidate)
    if not match:
        raise ValueError("No JSON object found in agent output.")

    return json.loads(match.group(0))
