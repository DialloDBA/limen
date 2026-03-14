"""Orchestrateur principal de Limen.

Il coordonne l'évaluation de compétence, la prise de décision,
la consultation éventuelle d'agents, et les mises à jour de mémoire.
"""

from __future__ import annotations

from limen.agents.critic import CriticAgent
from limen.agents.generator import GeneratorAgent
from limen.agents.synthesizer import SynthesizerAgent
from limen.core.competence_estimator import CompetenceEstimator
from limen.core.decision_engine import DecisionEngine
from limen.core.schemas import CritiquePayload, DecisionType, LimenResult, MemoryRecord
from limen.memory.shared_memory import SharedMemory
from limen.utils.json_utils import extract_json_object


class LimenOrchestrator:
    """Pipeline exécutable du framework Limen."""

    def __init__(
        self,
        estimator: CompetenceEstimator,
        decision_engine: DecisionEngine,
        generator: GeneratorAgent,
        critic: CriticAgent,
        synthesizer: SynthesizerAgent,
        shared_memory: SharedMemory,
        revision_threshold: int = 7,
    ):
        self.estimator = estimator
        self.decision_engine = decision_engine
        self.generator = generator
        self.critic = critic
        self.synthesizer = synthesizer
        self.shared_memory = shared_memory
        self.revision_threshold = revision_threshold

    def run(self, question: str) -> LimenResult:
        """Exécute le cycle complet sur une question utilisateur."""
        memory_context = self.shared_memory.fetch_context()
        assessment = self.estimator.assess(question, memory_context)
        decision = self.decision_engine.decide(assessment)

        draft: str | None = None
        critique_payload: CritiquePayload | None = None
        final_answer: str
        memory_updates: list[str] = []

        if decision is DecisionType.ANSWER_ALONE:
            draft = self.generator.generate(question, memory_context)
            final_answer = self.synthesizer.finalize(question, draft, None, memory_context)

        elif decision is DecisionType.CONSULT_PEERS:
            draft = self.generator.generate(question, memory_context)
            critique_raw = self.critic.review(question, draft, memory_context)
            critique_payload = CritiquePayload(**extract_json_object(critique_raw))

            working_draft = draft
            if critique_payload.revision_useful and critique_payload.severity_score >= self.revision_threshold:
                working_draft = self.generator.revise(question, draft, critique_raw, memory_context)

            final_answer = self.synthesizer.finalize(
                question=question,
                draft=working_draft,
                critique_json=critique_raw,
                memory_context=memory_context,
            )

        elif decision is DecisionType.DELEGATE_EXPERT:
            draft = "Delegation placeholder: route to a specialized expert agent."
            final_answer = (
                "Le système estime que la question dépasse sa compétence directe. "
                "Une délégation vers un expert spécialisé est recommandée."
            )

        else:
            final_answer = (
                "Le niveau de risque est trop élevé pour répondre de manière fiable dans l'état actuel. "
                "Une validation humaine ou une escalade contrôlée est recommandée."
            )

        self.shared_memory.append(
            MemoryRecord(
                key="last_question",
                value=question,
                source="orchestrator",
                tags=["question"],
            )
        )
        memory_updates.append("last_question")

        self.shared_memory.append(
            MemoryRecord(
                key="last_decision",
                value=decision.value,
                source="decision_engine",
                tags=["decision"],
            )
        )
        memory_updates.append("last_decision")

        return LimenResult(
            question=question,
            assessment=assessment,
            decision=decision,
            draft=draft,
            critique=critique_payload,
            final_answer=final_answer,
            memory_updates=memory_updates,
        )
