from pathlib import Path

from limen.core.factory import build_limen


def test_orchestrator_runs_with_mock_config():
    orchestrator = build_limen(Path("config/limen.yaml"))
    result = orchestrator.run("Explique brièvement ce qu'est un test unitaire.")

    assert result.question
    assert result.final_answer
    assert result.assessment.confidence >= 0.0
