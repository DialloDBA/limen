from limen.core.decision_engine import DecisionEngine, DecisionThresholds
from limen.core.schemas import CompetenceAssessment, DecisionType


def test_decision_answer_alone():
    engine = DecisionEngine(DecisionThresholds())
    assessment = CompetenceAssessment(
        confidence=0.9,
        risk=0.1,
        domain="general",
        complexity="low",
        rationale="high confidence",
    )
    assert engine.decide(assessment) == DecisionType.ANSWER_ALONE


def test_decision_consult_peers():
    engine = DecisionEngine(DecisionThresholds())
    assessment = CompetenceAssessment(
        confidence=0.5,
        risk=0.5,
        domain="general",
        complexity="medium",
        rationale="consultation useful",
    )
    assert engine.decide(assessment) == DecisionType.CONSULT_PEERS
