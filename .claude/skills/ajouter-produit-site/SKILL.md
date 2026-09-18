---
name: ajouter-produit-site
description: Ajouter ou modifier un produit sur le site public mgapps.fr (nouveau logiciel, changement de tarif, de texte, de FAQ ou de captures). A utiliser des qu'il faut toucher au contenu du site vitrine, y compris pour corriger une simple phrase ou un prix.
---

# Ajouter ou modifier un produit sur mgapps.fr

Le site est genere. **On n'edite jamais les `.html`** : on edite `_data/site.json`
puis on relance `generer.py`.

## Modifier un contenu existant
```bash
# 1. editer le bloc du produit dans _data/site.json
# 2. regenerer
python3 generer.py
# 3. verifier que seuls les fichiers generes ont bouge
git diff --stat
```

## Ajouter un produit

Dupliquer un bloc existant de `produits` dans `_data/site.json` et renseigner :

| Cle | Contenu |
|---|---|
| `id` | identifiant court en minuscules. **Il donne le nom de page** : `id: "vigo"` -> `vigo.html` |
| `nom` | nom affiche |
| `actif` | `true` publie le produit, `false` le retire du site et du sitemap |
| `logo` | chemin relatif dans `img/` |
| `accroche` | une phrase, sous le nom |
| `categorie` | categorie schema.org du logiciel |
| `pour` / `aussiPour` | cible principale / elargissement du referencement |
| `motsCles` | liste de mots-cles pour le referencement |
| `tarif` / `prixValeur` | libelle affiche (`"A partir de 129 € par mois"`) et valeur numerique seule (`"129"`) pour schema.org |
| `statut` | optionnel, ex. `"Lancement prochain"` |
| `lienAppli` / `texteBouton` | lien vers l'application, vide si pas encore ouverte |
| `seoTitle` / `seoDesc` | balise title et meta description |
| `description` | paragraphes de presentation |
| `points` | arguments cles |
| `faq` | questions/reponses, reprises en donnees structurees |
| `captures` | images, a deposer dans `img/` avant de generer |

Puis :
```bash
python3 generer.py
git add _data/site.json img/ *.html robots.txt sitemap.xml llms.txt
```

## Points de vigilance

- **Pillow doit etre installe** (`python3 -c "import PIL" || pip install Pillow`).
  Sans lui `generer.py` ne plante pas : il classe toutes les captures en `paysage`,
  ce qui casse l'affichage des captures verticales. Toujours relire `git diff` a la
  recherche d'une bascule `carrousel portrait` -> `carrousel paysage` non demandee.
- **Deposer les images dans `img/` AVANT de generer** : `generer.py` lit leur
  dimension pour decider portrait ou paysage.
- `seoTitle` et `seoDesc` ne sont pas facultatifs : sans eux la page sort avec un
  referencement degrade.
- Ne jamais retirer la FAQ ni les donnees structurees d'un produit.
- Ne pas mettre un prix dans un texte libre ailleurs que `tarif` / `prixValeur` : le
  prix se retrouverait a deux endroits et divergerait.
- La liste `societe.botsIA` autorise explicitement les robots d'IA dans `robots.txt` et
  `llms.txt`. Ne pas la reduire sans demande explicite : elle sert la visibilite du
  site dans les reponses des IA.
