# Recherche d'items CS2 sur CSFloat

Ce repo contient un exemple minimal en Python pour interroger les listings CSFloat via HTTP.

## Prérequis

- Python 3.10+

## Utilisation rapide

```bash
python csfloat_search.py --query "AK-47 | Redline (Field-Tested)" --limit 5
```

## Authentification (optionnelle selon endpoint/quotas)

Tu peux définir une clé API CSFloat dans une variable d'environnement :

```bash
export CSFLOAT_API_KEY="ton_token"
```

Le script enverra automatiquement cet en-tête : `Authorization: <token>`.

## Exemples

Filtrer par prix (en cents) et float :

```bash
python csfloat_search.py \
  --query "AWP | Asiimov (Battle-Scarred)" \
  --min-price 5000 \
  --max-price 30000 \
  --min-float 0.45 \
  --max-float 0.99 \
  --sort-by lowest_price \
  --order asc
```

## Notes importantes

- Vérifie toujours la documentation CSFloat pour les endpoints et paramètres à jour.
- Évite le scraping HTML : préfère l'API officielle (plus stable et conforme aux conditions d'utilisation).
