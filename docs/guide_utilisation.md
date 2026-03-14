# Guide d'utilisation

## 1. Préparer l'environnement

Créer un environnement virtuel puis installer les dépendances.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Utiliser la configuration mock

La configuration par défaut utilise des providers `mock` afin que le projet puisse être exécuté immédiatement.

```bash
python main.py --question "Explique le rôle d'un routeur BGP."
```

## 3. Brancher un vrai provider

Modifier `config/limen.yaml` :

- remplacer un provider `mock` par `openai` ou `ollama` ;
- renseigner le modèle souhaité ;
- ajouter les clés nécessaires dans `.env`.

## 4. Ajouter des tâches de benchmark

Compléter `data/tasks.json` avec des questions supplémentaires.

## 5. Lancer les tests

```bash
pytest -q
```
