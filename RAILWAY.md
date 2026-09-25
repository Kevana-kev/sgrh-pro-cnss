# Déploiement Railway — SGRH Pro

Repo : https://github.com/Kevana-kev/sgrh-pro-cnss

## Réponse courte

**Oui, le dépôt est maintenant prêt pour Railway**, à condition de :

1. Mettre le **Root Directory** sur `RH_CNSS/sgrh-pro`
2. Ajouter un **MySQL**
3. Renseigner les **variables d’environnement** (surtout `APP_KEY` et DB_*)

Voir le guide détaillé : `RH_CNSS/sgrh-pro/README.md` (section Railway.com).

## Ce qui marche sur Railway

- Application web Laravel (login, employés, congés, dashboard, rapports…)
- Base MySQL + migrations + seed (optionnel)

## Ce qui ne marche PAS sur Railway

- Lecteur **ZK-9500** + bridge C# Windows (USB local uniquement)
