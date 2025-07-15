[![codecov](https://codecov.io/github/RubenVP2/gitlab-mistral-review/branch/master/graph/badge.svg?token=NCZ4SSC9KU)](https://codecov.io/github/RubenVP2/gitlab-mistral-review)


# 🤖 MR Reviewer – Analyse automatique de Merge Requests avec IA

Ce projet automatise la **review de merge requests GitLab** à l’aide d’une **intelligence artificielle (ex: Mistral)**. Il s’exécute en tâche de fond, détecte les nouvelles MR ou mises à jour, génère un commentaire d’analyse, et l’envoie dans la discussion GitLab.

---

## 🚀 Fonctionnalités

- 🔁 Polling régulier des projets GitLab
- 🧠 Appel à une IA (Mistral) pour analyser le `diff`
- 📝 Post automatique de review dans la MR
- 🧮 Gestion des limites de tokens IA
- 🧠 Skip automatique des MRs trop volumineuses
- 💾 Système de cache pour éviter les doublons
- 📦 Architecture hexagonale claire et modulaire

---

## 📦 Installation

### 1. Clone

```bash
git clone https://github.com/ton-org/mr-reviewer.git
cd mr-reviewer

```
2. Créer un environnement Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```dotenv
GITLAB_TOKEN=glpat-xxxxx
GITLAB_URL=https://gitlab.com/api/v4
MISTRAL_API_KEY=sk-xxxx
CACHE_FILE=cache.json
POLLING_INTERVAL=300
MAX_TOKENS=8000
LOG_LEVEL=INFO
# Optionnel: fichier pour stocker les logs
LOG_FILE=app.log
```
Ces variables permettent de personnaliser le système de logs fourni par
le projet. Par défaut les messages sont envoyés sur la console, mais vous
pouvez spécifier `LOG_FILE` pour les écrire également dans un fichier.
### 4. Lancer l'application

```bash
python -m app.main
```

### ⚙️ Comportement de l’application
- 🔄 Le scheduler appelle review_merge_requests() à intervalle défini

- 🧠 Le diff est évalué :

    - Si le cache indique qu’il a déjà été reviewé → skip

    - Si le diff dépasse la limite de tokens → commentaire explicatif

    - Sinon → appel à Mistral, génération de review, publication GitLab

- 💾 Le SHA de la MR est persisté pour éviter les doublons

### 🧠 Architecture hexagonale
L’application suit les principes hexagonaux :

- Domain : logique métier pure

- Ports : interfaces pour les dépendances (GitLab, IA, cache)

- Adapters : implémentations concrètes

- UseCases : orchestration métier

- Infrastructure : scheduling & configuration

### 🧪 Tests
Lance les tests avec :

```bash
pytest tests/
```

### 👨‍💻 Contribution
1. Fork

2. Crée une branche feature/xxx

3. Teste ton code

4. Ouvre une MR ✨

🧱 À venir
- Support webhook GitLab

- Interface FastAPI pour supervision

- Analyse multi-projets

- Support d’autres moteurs IA