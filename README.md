# ![logo](./three_one_logo.svg)

Un agent conversationnel interactif en ligne de commande propulsé par les modèles **Google Gemini** (via le SDK `google-genai`), doté d'une mémoire persistante par utilisateur et d'un accès au web en temps réel.

---

## Fonctionnalités

- **Moteur Gemini moderne** : Utilise la nouvelle API avec état _Interactions_ (`client.interactions`) de Google GenAI avec gestion native des appels d'outils (_function calling_).
- **Mémoire persistante multi-utilisateurs** :
  - `remember` : Retient des faits ou préférences par identifiant utilisateur (`user_id`).
  - `recall` : Restitue les informations mémorisées.
  - Stockage dans un fichier JSON dédié configurable.
- **Recherche Web en temps réel** :
  - `web_search` : Recherche en ligne via l'API **Tavily** avec synthèse et citations des URLs sources.
- **Gestion de configuration robuste** : Validation des variables d'environnement via `pydantic-settings`.
- **Interface interactive (CLI)** : Boucle de discussion interactive avec sélection d'identifiant (`guest` par défaut).

---

## Structure du Projet

```text
three-one-agent/
├── main.py                     # Point d'entrée de l'application (boucle interactive)
├── pyproject.toml              # Dépendances et configuration des outils (Ruff)
├── uv.lock                     # Fichier de verrouillage des dépendances
├── .env.sample                 # Exemple de variables d'environnement
├── README.md                   # Documentation du projet
├── AGENT.md                    # Guide pour agents IA sur le projet
└── src/
    ├── client/
    │   └── index.py            # Client Google AI et boucle d'exécution des outils
    ├── config/
    │   └── env.py              # Chargement et validation des variables d'environnement
    ├── memory/                 # Dossier de persistance locale de la mémoire JSON
    └── tools/
        ├── functions_def.py    # Implémentation des outils (mémoire, recherche web, etc.)
        └── functions_list.py   # Déclarations des schémas d'outils pour Gemini
```

---

## Prérequis

- **Python** `>= 3.13`
- Gestionnaire de paquets [**uv**](https://docs.astral.sh/uv/) (recommandé)
- Une clé API [Google AI Studio](https://aistudio.google.com/)
- Une clé API [Tavily](https://tavily.com/)

---

## Installation et Configuration

1. **Cloner le dépôt** :

   ```bash
   git clone <url-du-depot>
   cd three-one-agent
   ```

2. **Installer les dépendances** :

   ```bash
   uv sync
   ```

3. **Configurer les variables d'environnement** :
   Copiez `.env.sample` vers `.env` et renseignez vos clés :

   ```bash
   cp .env.sample .env
   ```

   Éditez `.env` :

   ```env
   GOOGLE_API_KEY=votre_cle_google_ai
   TAVILY_API_KEY=votre_cle_tavily
   MEMORY_PATH=src/memory/user_memory.json
   ```

---

## Utilisation

Lancez l'agent avec `poe`:

```bash
poe main
```

Exemple d'échange dans la console :

```text
Identifiant (Entree = guest) > alice
Agent pret pour 'alice'. Tapez 'quit' pour sortir.
Vous > Je m'appelle Alice et j'aime le thé vert.
Agent > C'est bien noté, Alice ! Je me souviendrai que vous aimez le thé vert.
Vous > Quelles sont les dernières actualités sur Python 3.13 ?
	Called web_search({'query': 'Python 3.13 latest news'}) → ...
Agent > Voici les dernières nouveautés concernant Python 3.13 : ...
Vous > De quoi est-ce que je t'ai parlé tout à l'heure ?
	Called recall({'key': 'preferences'}) → ...
Agent > Vous m'avez dit que vous vous appelez Alice et que vous aimez le thé vert.
Vous > quit
```

---

## Développement et Qualité de Code

Le projet utilise [Ruff](https://docs.astral.sh/ruff/) pour le linting et le formatage :

- **Vérifier le code** :
  ```bash
  uv run ruff check .
  ```
- **Formater le code** :
  ```bash
  uv run ruff format .
  ```
