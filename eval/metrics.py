"""Fonctions utilitaires pour calculer quelques métriques simples."""

from __future__ import annotations


def average(values: list[float]) -> float:
    """Retourne la moyenne d'une liste de flottants."""
    if not values:
        return 0.0
    return sum(values) / len(values)
