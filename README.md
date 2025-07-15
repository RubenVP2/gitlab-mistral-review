# MR Reviewer - Analyse de Merge Requests avec IA

[![codecov](https://codecov.io/github/RubenVP2/gitlab-mistral-review/branch/master/graph/badge.svg?token=NCZ4SSC9KU)](https://codecov.io/github/RubenVP2/gitlab-mistral-review)


MR Reviewer automatise la revue de code sur GitLab en s'appuyant sur un moteur d'intelligence artificielle (par exemple Mistral). L'application interroge régulièrement vos projets pour détecter les nouvelles demandes de fusion ou les mises à jour, génère un commentaire d'analyse et le publie directement dans la discussion de la MR.

## Fonctionnalités principales

- Interrogation périodique de GitLab pour récupérer les MRs ouvertes
- Analyse du diff via Mistral et publication automatisée des commentaires
- Gestion du nombre maximal de tokens et filtrage des MRs trop volumineuses
- Système de cache pour éviter les doublons
- Architecture hexagonale claire et modulaire

## Installation rapide

1. Clonez le dépôt puis créez un environnement Python :

```bash
git clone https://github.com/ton-org/mr-reviewer.git
cd mr-reviewer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configurez l'application à l'aide d'un fichier `.env` :

```dotenv
GITLAB_TOKEN=glpat-xxxxx
GITLAB_URL=https://gitlab.com/api/v4
MISTRAL_API_KEY=sk-xxxx
CACHE_FILE=cache.json
POLLING_INTERVAL=300
MAX_TOKENS=8000
LOG_LEVEL=INFO
# Optionnel : fichier où enregistrer les logs
LOG_FILE=app.log
```

3. Lancez l'application :

```bash
python -m app.main
```

## Comportement général

- Le scheduler déclenche immédiatement `review_merge_requests()` puis à l'intervalle défini
- Pour chaque MR détectée :
  - si elle a déjà été traitée, elle est ignorée
  - si le diff dépasse la limite autorisée, un message explicatif est envoyé
  - sinon la revue est générée via Mistral puis publiée
- Les identifiants de MR sont conservés dans le cache afin d'éviter les doublons

## Tests

Exécutez la suite de tests avec :

```bash
pytest tests/
```

## Contribution

1. Forkez le dépôt
2. Créez une branche dédiée pour vos changements
3. Vérifiez votre code via la suite de tests
4. Ouvrez une merge request

## Feuille de route

- Support des webhooks GitLab
- Interface FastAPI de supervision
- Analyse multi-projets
- Compatibilité avec d'autres moteurs IA
