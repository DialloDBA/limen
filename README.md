# Limen
### Un framework de détection de seuil de compétence pour l'orchestration intelligente des LLM

**Limen** est un framework expérimental de raisonnement adaptatif pour systèmes IA. 
Son idée centrale est simple : une IA ne devrait pas collaborer *tout le temps*, mais seulement lorsqu'elle détecte qu'elle approche ou franchit le **seuil de sa propre compétence**.

> *"Un humain compétent ne résout pas tout seul. Il sait estimer ses limites, consulter les bonnes personnes au bon moment, et construire sur une mémoire collective. Les IA actuelles ne savent pas encore faire ça."*

---

## Table des matières

1. [Motivation & Problème](#motivation--problème)
2. [Idée centrale](#idée-centrale)
3. [Les trois piliers de Limen](#les-trois-piliers-de-limen)
4. [Architecture](#architecture)
5. [Structure du dépôt](#structure-du-dépôt)
6. [Principes d'ingénierie](#principes-dingénierie)
7. [Installation & Installation](#installation--utilisation)
8. [Configuration](#configuration)
9. [Différenciation](#différenciation)
10. [Évaluation](#évaluation)
11. [État du projet & Travaux futurs](#état-du-projet--travaux-futurs)
12. [Auteur & Licence](#auteur--licence)

---

## Motivation & Problème

Ce projet est né d'une observation terrain lors du développement de **Dymmo**, une infrastructure financière pilotée par des agents IA. En travaillant simultanément avec plusieurs modèles (Claude, Gemini, GPT) sur un même projet, nous avons constaté que malgré la présence de contextes riches et d'historiques, les agents ne partageaient aucune mémoire commune. Chacun retraitait les mêmes informations, reconsommait les mêmes tokens, reconstruisait le même contexte — comme si l'autre n'existait pas.

Le problème n'est pas le nombre de modèles, c'est l'architecture. De plus, ces agents ne savaient pas quand ils auraient dû demander de l'aide : ils répondaient toujours avec la même confiance, même quand ils ne savaient pas.

### Les deux faiblesses structurelles identifiées :
1. **Surconfiance algorithmique :** Un LLM ne raisonne pas sur sa propre compétence. Il n'a aucun mécanisme interne pour dire : *"Je ne suis pas sûr. Je devrais demander de l'aide."* Résultat : hallucinations et erreurs logiques présentées avec assurance.
2. **Absence de mémoire partagée :** Quand plusieurs agents travaillent en parallèle, chacun repart de son propre contexte. Il n'existe pas d'espace cognitif commun, ce qui rend la collaboration réelle impossible et entraîne un retraitement inutile de l'information.


**Question de recherche centrale :**
> *Comment un système d'IA peut-il détecter le seuil de sa propre compétence, décider intelligemment quand collaborer, et partager une mémoire commune avec d'autres agents ?*

---

## Idée centrale

La plupart des systèmes multi-agents actuels fonctionnent par "brute force" (débat systématique). Limen propose une **couche métacognitive** inspirée du comportement humain :

```text
Question
    ↓
Estimation de compétence
    ↓
┌──────────────────────────────────┐
│  Compétence élevée → Répond seul │
│  Incertitude      → Consulte     │
│  Hors domaine     → Délègue      │
└──────────────────────────────────┘
    ↓
Mémoire partagée mise à jour
```

La collaboration n'est pas déclenchée systématiquement. Elle est déclenchée **au seuil** — au moment exact où elle devient nécessaire.

---

## Les trois piliers de Limen

### Pilier 1 — Le Seuil *(Limen Score)*
Limen observe des signaux externes pour estimer l'incertitude : variance sémantique (stabilité de la réponse), auto-sondage (auto-vérification logique), détection de domaine et score de confiance.

### Pilier 2 — La Décision *(Moteur de décision)*
Le moteur traduit le Limen Score en action conditionnelle : `answer_alone`, `consult_peers`, ou `delegate_expert`. Ce n'est pas un pipeline fixe, mais une décision dynamique.

### Pilier 3 — La Mémoire Partagée *(Shared Context Layer)*
Un espace cognitif commun attaché au **projet**, pas à l'agent. Chaque agent lit la mémoire avant d'intervenir et la met à jour après, évitant les hallucinations et les répétitions.

---

## Architecture

```text
Utilisateur
     │
     ▼
┌────────────────────────────────────────┐
│           LIMEN GATEWAY                │
│                                        │
│  ┌─────────────────────────────────┐   │
│  │     Competence Estimator        │   │
│  │  (variance + domaine + confiance)│  │
│  └──────────────┬──────────────────┘   │
│                 │ Limen Score           │
│  ┌──────────────▼──────────────────┐   │
│  │       Decision Engine           │   │
│  └────────┬──────────┬─────────────┘   │
│           │          │         │       │
│      Autonome    Consultation  Délégation
│           │          │         │       │
│           │    ┌─────▼──────┐  │       │
│           │    │  Générateur│  │       │
│           │    │  Critique  │  │       │
│           │    │ Synthétiseur│ │       │
│           │    └─────┬──────┘  │       │
│           └──────────┼─────────┘       │
│                      │                 │
│  ┌───────────────────▼─────────────┐   │
│  │       Shared Context Layer      │   │
│  │    (mémoire commune du projet)  │   │
│  └─────────────────────────────────┘   │
└────────────────────────────────────────┘
     │
     ▼
 Réponse finale
```

---

## Structure du dépôt

```text
limen/
├── agents/          # Interfaces des agents (Générateur, Critique, Synthétiseur)
├── core/            # Cœur logique (Estimator, Decision, Orchestrator)
├── memory/          # Gestion de la mémoire partagée et schémas Pydantic
├── providers/       # Abstraction multi-fournisseurs (OpenAI, Ollama, Mistral, Anthropic)
├── config/          # Configuration externe YAML
├── data/            # Datasets pour le benchmark
├── eval/            # Métriques d'évaluation et scripts de benchmark
├── tests/           # Tests unitaires et d'intégration
├── main.py          # Point d'entrée CLI
└── requirements.txt
```

---

## Principes d'ingénierie

- **Commentaires et documentation en français** (pour la clarté pédagogique).
- **Code (variables, classes, API) en anglais** (standard industriel).
- **Agnostique aux fournisseurs :** Aucun hardcoding, support natif de LiteLLM, Ollama, etc.
- **Configuration externe :** Piloté par YAML via `config/limen.yaml`.
- **Sorties structurées :** Utilisation intensive de JSON et Pydantic.

---

## Installation & Utilisation

### 1. Installation
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
cp .env.example .env       # Configurez vos clés API
```

### 2. Lancement
```bash
python main.py --question "Explique le protocole BGP hijacking."
```

---

## Configuration

Exemple de `config/limen.yaml` :
```yaml
seuils:
  limen_score_consultation: 0.45   # En dessous → réponse autonome
  limen_score_delegation: 0.75     # Au dessus → délégation expert

providers:
  principal: { type: ollama, model: mistral }
  critique: { type: openai, model: gpt-4o-mini }

agents:
  generateur: { provider_ref: principal, temperature: 0.3 }
  critique: { provider_ref: critique, temperature: 0.1 }
```

---

## Différenciation

| Système | Ce qu'il fait | Différence Limen |
|---|---|---|
| **AutoGen / CrewAI** | Agents discutent librement | Décision conditionnelle *avant* collaboration |
| **LangGraph** | Workflows cycliques | Couche de métacognition en amont du workflow |
| **Multi-Agent Debate** | Débat systématique | Ne débat que si le seuil le justifie |

---

## Évaluation

Limen est évalué sur des tâches de raisonnement complexe avec les métriques suivantes :
- **Taux d'erreur** vs vérité terrain.
- **Réduction d'erreur** relative au modèle seul.
- **Taux de consultation** (efficience du seuil).
- **Coût et Latence**.

---

## État du projet & Travaux futurs

### État actuel
- Architecture modulaire et interfaces providers fonctionnelles.
- Mémoire partagée basée sur fichiers.
- Stratégie de décision par seuil heuristique.

### Travaux futurs
- **Calibration dynamique :** Ajustement des seuils par apprentissage.
- **Mémoire vectorielle :** Passage de fichiers à une base vectorielle (RAG partagé).
- **Protocoles de conflit :** Résolution des contradictions entre agents en mémoire.

---

## Auteur & Licence

**Abdourahamane** - Étudiant à l'Université de Montréal (UdeM).
Projet de recherche indépendant né du développement de Dymmo.

Licence : **MIT**
