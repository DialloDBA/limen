# Architecture de Limen

## Intuition générale

Limen n'est pas un simple orchestrateur multi-agent. Son objectif est d'introduire une **logique de seuil** entre la question et la collaboration.

Au lieu d'activer automatiquement plusieurs agents, Limen commence par estimer si le système doit :

- répondre seul ;
- consulter un pair ;
- déléguer à un expert ;
- refuser ou escalader.

## Composants principaux

### 1. `AssessorAgent`

Cet agent produit une estimation structurée de confiance, de risque et de complexité.

### 2. `CompetenceEstimator`

Ce composant transforme la sortie brute de l'agent d'évaluation en objet validé.

### 3. `DecisionEngine`

Il applique une politique explicable basée sur des seuils configurables.

### 4. `GeneratorAgent`

Il produit un premier brouillon de réponse en tenant compte de la mémoire partagée.

### 5. `CriticAgent`

Il analyse le brouillon et renvoie une critique structurée en JSON.

### 6. `SynthesizerAgent`

Il arbitre la réponse finale à partir de la question, du brouillon, de la critique et du contexte mémoire.

### 7. `SharedMemory`

Elle fournit un espace de mémoire commune de projet pour éviter que chaque agent reparte constamment de zéro.

## Propriété essentielle

Le projet est **provider-agnostic** : le protocole n'est pas lié à OpenAI, Mistral, Ollama ou tout autre fournisseur.

## Pipeline simplifié

```text
Question
   ↓
AssessorAgent
   ↓
CompetenceEstimator
   ↓
DecisionEngine
   ↓
┌──────────────┬───────────────┬────────────────────┐
│              │               │                    │
Answer Alone   Consult Peers   Delegate Expert      Escalate
│              │               │
└──────────────┴───────┬───────┘
                       ↓
                SharedMemory + Synthesizer
```
