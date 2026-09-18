# MG Apps - Site public (www.mgapps.fr)

Site vitrine statique **genere** par un script Python. Deploiement Cloudflare Pages
sur push `main`.

## Regle numero un

`index.html`, `vigo.html`, `trajo.html`, `robots.txt`, `sitemap.xml` et `llms.txt`
sont **GENERES**. Ne jamais les editer a la main : la modification serait ecrasee a
la prochaine generation.

```
_data/site.json   <-- la seule chose qu'on edite pour le contenu
generer.py        <-- le gabarit (CSS, structure HTML, schema.org, FAQ)
```

Changer un texte, un prix, un mot-cle, ajouter un produit :
1. editer `_data/site.json`
2. `pip install Pillow` si besoin (voir ci-dessous), puis `python3 generer.py`
3. commiter **et le JSON et les fichiers regeneres**

## Pillow est obligatoire pour generer

`generer.py` lit la taille des captures avec Pillow pour poser la classe
`portrait` ou `paysage` sur le carrousel. **Sans Pillow, le script ne plante pas** :
il se rabat silencieusement sur `paysage` et casse l'affichage des captures verticales.

```bash
python3 -c "import PIL" || pip install Pillow
```
Si Pillow ne peut pas etre installe, ne pas commiter les pages regenerees : verifier
`git diff` et annuler toute bascule `portrait` -> `paysage` non voulue.

Changer la mise en page, le CSS ou la structure : editer `generer.py`, puis regenerer.

## Structure de `_data/site.json`

- `societe` : identite, coordonnees, pitch, `botsIA` (liste des robots d'IA autorises,
  utilisee pour produire `robots.txt` et `llms.txt`)
- `produits` : un bloc par produit, `actif: true/false` decide de sa publication.
  Un produit inactif ne genere pas de page et disparait du sitemap.

## Conventions

- Charte : bleu nuit `#101BA8`, or `#FEBF1A` (variables CSS `--nuit` / `--or` dans
  `generer.py`).
- Le texte doit rester **en dur dans le HTML genere**, lisible par Google et par les
  IA. Ne pas deplacer du contenu vers du JavaScript.
- Chaque produit porte ses donnees structurees schema.org + une FAQ : en ajouter un
  sans ces blocs degraderait le referencement.
- `generer.py` est en Python 3, sans dependance obligatoire (Pillow est optionnel,
  seulement pour detecter l'orientation des images).
- Redaction en francais, ton sobre. Pas de em-dash.

## Verification apres generation
```bash
python3 generer.py && git diff --stat
```
Le diff ne doit toucher que les fichiers generes attendus. Un fichier inattendu qui
bouge = un fichier edite a la main quelque part.
