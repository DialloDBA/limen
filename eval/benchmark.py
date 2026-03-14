"""Benchmark minimal pour comparer un flux direct et le flux Limen.

Ce script n'a pas vocation à fournir des métriques académiques définitives.
Il sert de base de travail pour instrumenter le coût, la latence et la qualité.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from limen.core.factory import build_limen


def run_benchmark(config_path: str = "config/limen.yaml", tasks_path: str = "data/tasks.json") -> list[dict]:
    orchestrator = build_limen(Path(config_path))
    tasks = json.loads(Path(tasks_path).read_text(encoding="utf-8"))

    results: list[dict] = []
    for task in tasks:
        started_at = time.perf_counter()
        result = orchestrator.run(task["question"])
        elapsed = time.perf_counter() - started_at

        results.append(
            {
                "id": task["id"],
                "decision": result.decision.value,
                "latency_seconds": round(elapsed, 4),
                "confidence": result.assessment.confidence,
                "risk": result.assessment.risk,
                "final_answer": result.final_answer,
            }
        )

    return results


if __name__ == "__main__":
    benchmark_results = run_benchmark()
    print(json.dumps(benchmark_results, indent=2, ensure_ascii=False))
