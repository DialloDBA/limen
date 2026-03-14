"""Point d'entrée simple pour exécuter Limen en ligne de commande."""

from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from limen.core.factory import build_limen


def build_parser() -> argparse.ArgumentParser:
    """Construit le parseur CLI principal."""
    parser = argparse.ArgumentParser(description="Exécuter Limen sur une question donnée.")
    parser.add_argument(
        "--config",
        default="config/limen.yaml",
        help="Chemin du fichier de configuration YAML.",
    )
    parser.add_argument(
        "--question",
        required=True,
        help="Question à traiter par le système Limen.",
    )
    return parser


def main() -> None:
    """Charge la configuration puis exécute le pipeline principal."""
    load_dotenv()
    args = build_parser().parse_args()

    limen = build_limen(Path(args.config))
    result = limen.run(args.question)

    print("\n=== LIMEN RESULT ===")
    print(result.model_dump_json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
