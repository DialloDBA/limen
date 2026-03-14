"""Fabrique principale du projet.

Ce module lit la configuration externe, construit les providers,
instancie les agents et assemble l'orchestrateur final.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from limen.agents.assessor import AssessorAgent
from limen.agents.base_agent import AgentConfig
from limen.agents.critic import CriticAgent
from limen.agents.generator import GeneratorAgent
from limen.agents.synthesizer import SynthesizerAgent
from limen.core.competence_estimator import CompetenceEstimator
from limen.core.decision_engine import DecisionEngine, DecisionThresholds
from limen.core.orchestrator import LimenOrchestrator
from limen.core.prompts import (
    ASSESSOR_SYSTEM_PROMPT,
    CRITIC_SYSTEM_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
    SYNTHESIZER_SYSTEM_PROMPT,
)
from limen.memory.shared_memory import SharedMemory
from limen.providers.mock_provider import MockProvider
from limen.providers.ollama_provider import OllamaProvider
from limen.providers.openai_provider import OpenAIProvider


PROMPT_REGISTRY: dict[str, str] = {
    "generator": GENERATOR_SYSTEM_PROMPT,
    "critic": CRITIC_SYSTEM_PROMPT,
    "synthesizer": SYNTHESIZER_SYSTEM_PROMPT,
    "assessor": ASSESSOR_SYSTEM_PROMPT,
}


def load_config(config_path: Path) -> dict[str, Any]:
    """Charge la configuration YAML du projet."""
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_provider(provider_cfg: dict[str, Any]):
    """Construit dynamiquement le provider demandé par la configuration."""
    provider_type = provider_cfg["type"].lower()

    if provider_type == "openai":
        return OpenAIProvider(
            model=provider_cfg["model"],
            api_key=provider_cfg.get("api_key"),
            base_url=provider_cfg.get("base_url"),
        )

    if provider_type == "ollama":
        return OllamaProvider(
            model=provider_cfg["model"],
            endpoint=provider_cfg.get("endpoint", "http://localhost:11434/api/chat"),
        )

    if provider_type == "mock":
        return MockProvider(name=provider_cfg.get("name", "mock"))

    raise ValueError(f"Unsupported provider type: {provider_type}")


def build_agent(agent_name: str, agent_cfg: dict[str, Any], providers: dict[str, Any]):
    """Construit un agent à partir de sa configuration externe."""
    provider = providers[agent_cfg["provider_ref"]]
    config = AgentConfig(
        name=agent_name,
        system_prompt=PROMPT_REGISTRY[agent_cfg["prompt_ref"]],
        temperature=agent_cfg.get("temperature", 0.2),
        max_tokens=agent_cfg.get("max_tokens"),
        response_format=agent_cfg.get("response_format"),
    )

    if agent_name == "generator":
        return GeneratorAgent(provider=provider, config=config)
    if agent_name == "critic":
        return CriticAgent(provider=provider, config=config)
    if agent_name == "synthesizer":
        return SynthesizerAgent(provider=provider, config=config)
    if agent_name == "assessor":
        return AssessorAgent(provider=provider, config=config)

    raise ValueError(f"Unsupported agent name: {agent_name}")


def build_limen(config_path: Path) -> LimenOrchestrator:
    """Assemble l'ensemble du système Limen à partir du YAML fourni."""
    cfg = load_config(config_path)

    providers = {
        name: build_provider(provider_cfg)
        for name, provider_cfg in cfg["providers"].items()
    }

    assessor = build_agent("assessor", cfg["agents"]["assessor"], providers)
    generator = build_agent("generator", cfg["agents"]["generator"], providers)
    critic = build_agent("critic", cfg["agents"]["critic"], providers)
    synthesizer = build_agent("synthesizer", cfg["agents"]["synthesizer"], providers)

    estimator = CompetenceEstimator(assessor=assessor)
    thresholds = DecisionThresholds(**cfg["workflow"]["thresholds"])
    decision_engine = DecisionEngine(thresholds=thresholds)
    shared_memory = SharedMemory(Path(cfg["memory"]["storage_path"]))

    return LimenOrchestrator(
        estimator=estimator,
        decision_engine=decision_engine,
        generator=generator,
        critic=critic,
        synthesizer=synthesizer,
        shared_memory=shared_memory,
        revision_threshold=cfg["workflow"].get("revision_threshold", 7),
    )
