# -*- coding: utf-8 -*-
"""
Generateur du site public MG Apps.
--------------------------------------------------------------------------
Source unique : _data/site.json
Lancer :        py -3 generer.py
Produit :       index.html + une page par produit (vigo.html, trajo.html...)
                + robots.txt + sitemap.xml + llms.txt

Pour AJOUTER un produit : ajouter un bloc dans _data/site.json, relancer.
Pour MODIFIER un texte / un prix : editer _data/site.json, relancer.
Le texte est ecrit EN DUR dans les pages (lisible par Google et par les IA),
et double par des donnees structurees schema.org + une FAQ par produit.
"""

import io, os, json, html, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.abspath(__file__))

with io.open(os.path.join(BASE, "_data", "site.json"), encoding="utf-8") as f:
    DATA = json.load(f)

STE = DATA["societe"]
PRODUITS = [p for p in DATA["produits"] if p.get("actif")]
DOMAINE = STE["domaine"].rstrip("/")

def e(s):
    return html.escape(str(s), quote=True)

try:
    from PIL import Image
    def orientation(rel):
        chemin = os.path.join(BASE, rel)
        if not os.path.exists(chemin):
            return None
        with Image.open(chemin) as im:
            return "portrait" if im.height > im.width else "paysage"
except Exception:
    def orientation(rel):
        return None

FB_SVG = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
          '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24'
          'v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97'
          'h-1.51c-1.49 0-1.95.93-1.95 1.88v2.26h3.32l-.53 3.49h-2.79V24C19.61 23.1 24 18.1 24 12.07"/></svg>')

def bouton_fb():
    if not STE.get("facebook"):
        return ""
    return ('<a class="btn-fb" href="%s" target="_blank" rel="noopener">%s Suivez-nous sur Facebook</a>'
            % (e(STE["facebook"]), FB_SVG))

# ---------------------------------------------------------------- styles
CSS = """
:root{--nuit:#101BA8;--or:#FEBF1A;--encre:#0d1b4c;--gris:#5b6b8c;--fond:#f4f6fc;
--carte:#fff;--trait:#e2e8f6;--accent:#101BA8}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--encre);
background:var(--fond);line-height:1.62}
img{max-width:100%;display:block}a{color:inherit;text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
header.top{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.94);
backdrop-filter:blur(8px);border-bottom:1px solid var(--trait)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.brand{display:flex;align-items:center;gap:11px;font-weight:800;font-size:20px;color:var(--nuit)}
.brand img{height:36px;width:auto}
.top nav{display:flex;gap:26px;font-weight:600;font-size:15px}
.top nav a{color:var(--gris)}.top nav a:hover{color:var(--nuit)}
@media(max-width:640px){.top nav{display:none}}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:16px;
padding:13px 24px;border-radius:12px;border:2px solid transparent;cursor:pointer;transition:.15s}
.btn-or{background:var(--or);color:#3a2c00}.btn-or:hover{filter:brightness(1.06)}
.btn-pri{background:var(--accent);color:#fff}.btn-pri:hover{filter:brightness(1.1)}
.btn-clair{background:transparent;border-color:rgba(255,255,255,.5);color:#fff}
.btn-clair:hover{background:rgba(255,255,255,.12)}
.btn-sec{background:#fff;border-color:var(--trait);color:var(--nuit)}.btn-sec:hover{border-color:var(--accent)}
/* hero accueil */
.hero{position:relative;color:#fff;padding:96px 0 104px;overflow:hidden;
background:linear-gradient(160deg,#0a1270 0%,#1a1f9e 55%,#101BA8 100%)}
.hero .bg{position:absolute;inset:0;object-fit:cover;width:100%;height:100%;opacity:.16;z-index:0}
.hero .wrap{position:relative;z-index:1}
.hero .r{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
color:#fff;font-weight:700;font-size:13px;padding:6px 14px;border-radius:20px;margin-bottom:22px}
.hero h1{font-size:46px;line-height:1.1;font-weight:900;letter-spacing:-.5px;max-width:17ch}
.hero p{font-size:19px;color:#dfe3ff;margin-top:18px;max-width:60ch}
.hero .cta{margin-top:30px;display:flex;gap:14px;flex-wrap:wrap}
@media(max-width:640px){.hero h1{font-size:33px}}
.sec{padding:70px 0}
.sec>.wrap>h2{font-size:30px;font-weight:900;color:var(--nuit);text-align:center}
.sec .sous{text-align:center;color:var(--gris);font-size:17px;margin-top:8px;margin-bottom:40px}
.cartes{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
.carte{background:var(--carte);border:1px solid var(--trait);border-radius:18px;padding:30px;
display:flex;flex-direction:column;transition:.18s;box-shadow:0 4px 20px rgba(16,27,168,.05)}
.carte:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(16,27,168,.13);border-color:#c9d3f2}
.carte .logo{height:50px;margin-bottom:16px}.carte .logo img{height:100%;width:auto}
.carte h3{font-size:24px;color:var(--nuit);font-weight:800}
.carte .acc{color:var(--gris);margin-top:6px;min-height:46px}
.carte .desc{margin-top:14px;font-size:15px;flex:1 1 auto}
.carte .pied{margin-top:22px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.tag{font-weight:800;color:var(--nuit);font-size:16px}
.tag small{display:block;font-weight:600;color:var(--gris);font-size:12px}
.fleche{background:var(--nuit);color:#fff;font-weight:700;font-size:15px;padding:10px 18px;border-radius:10px}
.pourquoi{background:#fff;border-top:1px solid var(--trait);border-bottom:1px solid var(--trait)}
.pourquoi .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:30px}
.pourquoi h4{color:var(--nuit);font-size:18px;margin-bottom:6px}
.pourquoi p{color:var(--gris);font-size:15px}.pourquoi .ic{font-size:26px;margin-bottom:10px}
.contact .box{background:linear-gradient(160deg,var(--nuit),#2a2496);color:#fff;
border-radius:20px;padding:48px 30px;text-align:center}
.contact h2{color:#fff}.contact p{color:#dfe3ff;margin:12px auto 26px;max-width:52ch}
.contact .liens{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
.btn-fb{display:inline-flex;align-items:center;gap:9px;background:#1877F2;color:#fff;font-weight:700;
font-size:16px;padding:13px 22px;border-radius:12px;border:2px solid transparent;transition:.15s}
.btn-fb:hover{filter:brightness(1.08)}.btn-fb svg{flex:0 0 auto}
footer.bas{padding:34px 0;color:var(--gris);font-size:14px;text-align:center;border-top:1px solid var(--trait)}
footer.bas b{color:var(--nuit)}footer.bas a{color:var(--nuit)}
/* page produit */
.tete{padding:56px 0 40px}
.tete .wrap{display:grid;grid-template-columns:1.05fr 1fr;gap:44px;align-items:center}
@media(max-width:820px){.tete .wrap{grid-template-columns:1fr;gap:26px}}
.tete .logo{height:58px;margin-bottom:16px}.tete .logo img{height:100%;width:auto}
.tete h1{font-size:38px;font-weight:900;color:var(--accent);letter-spacing:-.5px}
.tete .acc{font-size:20px;color:var(--gris);margin-top:10px}
.tete .pour{display:inline-block;margin-top:16px;background:#eef1fc;color:var(--nuit);
font-weight:700;font-size:14px;padding:6px 14px;border-radius:20px}
.statut{display:inline-block;background:var(--or);color:#3a2c00;font-weight:800;font-size:12px;
padding:4px 12px;border-radius:20px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:12px}
.carte .statut{margin:0 0 10px}
.tete .desc{margin-top:18px;font-size:17px;max-width:54ch}
.tete .aussi{margin-top:12px;font-size:14px;color:var(--gris);font-style:italic;max-width:56ch}
.tete .cta{margin-top:26px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.prix{font-weight:800;color:var(--accent);font-size:18px}.prix small{font-weight:600;color:var(--gris)}
.carrousel{position:relative;background:#fff;border:1px solid var(--trait);border-radius:20px;
overflow:hidden;box-shadow:0 10px 30px rgba(16,27,168,.08)}
.carrousel.portrait{max-width:320px;margin-left:auto;margin-right:auto}
.piste{display:flex;transition:transform .4s ease}
.slide{min-width:100%;position:relative;background:#eef1fc}
.carrousel.paysage .slide{aspect-ratio:16/9}
.carrousel.portrait .slide{aspect-ratio:9/20}
.slide img{width:100%;height:100%;object-fit:contain}
.slide .vide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
flex-direction:column;color:var(--gris);font-size:15px;text-align:center;padding:20px}
.slide .vide b{color:var(--nuit);font-size:17px;margin-bottom:4px}
.nav{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;
background:rgba(255,255,255,.92);border:1px solid var(--trait);cursor:pointer;font-size:20px;color:var(--nuit);
display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.1)}
.nav:hover{background:#fff}.nav.g{left:12px}.nav.d{right:12px}
.puces{position:absolute;bottom:14px;left:0;right:0;display:flex;gap:8px;justify-content:center}
.puce{width:9px;height:9px;border-radius:50%;background:rgba(16,27,168,.25);cursor:pointer;transition:.2s}
.puce.on{background:var(--accent);width:24px;border-radius:5px}
.forts{padding:16px 0 60px}.forts h2{font-size:26px;color:var(--accent);font-weight:800;
margin-bottom:24px;text-align:center}
.liste{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;max-width:860px;margin:0 auto}
.pt{background:#fff;border:1px solid var(--trait);border-radius:14px;padding:16px 20px;display:flex;gap:12px}
.pt .ck{color:var(--or);font-weight:900;font-size:18px}
.faq{background:#fff;border-top:1px solid var(--trait);padding:60px 0}
.faq h2{font-size:26px;color:var(--accent);font-weight:800;text-align:center;margin-bottom:30px}
.qa{max-width:800px;margin:0 auto}
.qa details{border:1px solid var(--trait);border-radius:12px;margin-bottom:12px;overflow:hidden;background:#fff}
.qa summary{padding:16px 20px;font-weight:700;color:var(--nuit);cursor:pointer;list-style:none;
display:flex;justify-content:space-between;align-items:center}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";color:var(--or);font-size:22px;font-weight:900}
.qa details[open] summary::after{content:"-"}
.qa .rep{padding:0 20px 18px;color:var(--encre)}
.final{padding:20px 0 76px}.final .box{background:linear-gradient(160deg,var(--accent),#2a2496);
color:#fff;border-radius:20px;padding:44px 30px;text-align:center}
.final h2{color:#fff;font-size:26px}.final p{color:#dfe3ff;margin:12px auto 24px;max-width:48ch}
""".strip()

def shell(titre, desc, canon, jsonld, corps, og_image, keywords=""):
    kwmeta = ('<meta name="keywords" content="%s">' % e(keywords)) if keywords else ""
    blocs = "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(j, ensure_ascii=False)
        for j in jsonld
    )
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{desc}">
{kwmeta}
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MG Apps">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#101BA8">
<style>{css}</style>
{blocs}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="index.html"><img src="img/mgapps-logo-officiel.png" alt="MG Apps" onerror="this.style.display='none'">MG Apps</a>
  <nav><a href="index.html#produits">Produits</a><a href="index.html#pourquoi">Pourquoi MG Apps</a><a href="index.html#contact">Contact</a></nav>
</div></header>
{corps}
<footer class="bas"><div class="wrap">
  <b>MG Apps</b> - Editeur de logiciels - {adr}<br>
  <a href="mailto:{email}">{email}</a> - SIRET {siret}{fb}
</div></footer>
</body>
</html>""".format(
        titre=e(titre), desc=e(desc), canon=e(canon), og=e(og_image), kwmeta=kwmeta,
        css=CSS, blocs=blocs, corps=corps,
        adr=e(STE["adresse"]), email=e(STE["email"]), siret=e(STE["siret"]),
        fb=(' - <a href="%s" target="_blank" rel="noopener">Facebook</a>' % e(STE["facebook"]))
           if STE.get("facebook") else "",
    )

# ---------------------------------------------------------------- JSON-LD communs
ORG = {
    "@context": "https://schema.org", "@type": "Organization",
    "name": STE["nom"], "url": DOMAINE + "/",
    "logo": DOMAINE + "/img/mgapps-logo-officiel.png",
    "email": STE["email"], "telephone": STE["telephone"],
    "founder": {"@type": "Person", "name": STE["fondateur"]},
    "address": {"@type": "PostalAddress", "streetAddress": "44 avenue Edouard Herriot",
                "postalCode": "21400", "addressLocality": "Chatillon-sur-Seine", "addressCountry": "FR"},
    "description": STE["pitch"],
}
if STE.get("facebook"):
    ORG["sameAs"] = [STE["facebook"]]

# ---------------------------------------------------------------- page produit
def page_produit(p):
    url = DOMAINE + "/" + p["id"]
    orient = "paysage"
    for c in p["captures"]:
        o = orientation(c)
        if o:
            orient = o
            break
    # carrousel : images en dur, repli "capture a venir" si absente
    slides = ""
    for i, src in enumerate(p["captures"], 1):
        slides += ('<div class="slide"><img src="%s" alt="%s, écran %d" loading="lazy" '
                   'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">'
                   '<div class="vide" style="display:none"><b>Capture à venir</b>Écran %d de %s</div></div>'
                   ) % (e(src), e(p["nom"]), i, i, e(p["nom"]))
    multi = len(p["captures"]) > 1
    puces = "".join('<span class="puce%s" data-i="%d"></span>' % (" on" if i == 0 else "", i)
                    for i in range(len(p["captures"]))) if multi else ""
    navs = ('<button class="nav g" aria-label="Précédent">&#8249;</button>'
            '<button class="nav d" aria-label="Suivant">&#8250;</button>'
            '<div class="puces">%s</div>') % puces if multi else ""

    pts = "".join('<div class="pt"><span class="ck">&#10003;</span><span>%s</span></div>' % e(t)
                  for t in p["points"])
    if p.get("lienAppli"):
        bouton = '<a class="btn btn-pri" href="%s" target="_blank" rel="noopener">%s &rarr;</a>' % (
            e(p["lienAppli"]), e(p["texteBouton"]))
    else:
        bouton = '<a class="btn btn-pri" href="mailto:%s?subject=Demande%%20-%%20%s">Demander une démonstration &rarr;</a>' % (
            e(STE["email"]), e(p["nom"]))
    prix = '<span class="prix">%s</span>' % e(p["tarif"]) if p.get("tarif") else \
           '<span class="prix">Sur devis <small>selon vos besoins</small></span>'
    qa = "".join('<details><summary>%s</summary><div class="rep">%s</div></details>' % (e(f["q"]), e(f["a"]))
                 for f in p["faq"])

    corps = """
<main>
<section class="tete"><div class="wrap">
  <div>
    <div class="logo"><img src="{logo}" alt="{nom}" onerror="this.parentNode.style.display='none'"></div>
    {statut}<h1>{nom}</h1>
    <p class="acc">{acc}</p>
    <p class="pour">{pour}</p>
    <p class="desc">{desc}</p>
    {aussi}
    <div class="cta">{bouton}{prix}</div>
  </div>
  <div class="carrousel {orient}"><div class="piste">{slides}</div>{navs}</div>
</div></section>

<section class="forts"><div class="wrap">
  <h2>Ce que fait {nom}</h2><div class="liste">{pts}</div>
</div></section>

<section class="faq"><div class="wrap">
  <h2>Questions fréquentes sur {nom}</h2><div class="qa">{qa}</div>
</div></section>

<section class="final"><div class="wrap"><div class="box">
  <h2>Envie d'en savoir plus sur {nom} ?</h2>
  <p>Une démonstration, un devis, une question : on vous répond vite et sans jargon.</p>
  <a class="btn btn-or" href="mailto:{email}?subject=Demande%20-%20{nom}">{email}</a>
</div></div></section>
</main>
""".format(logo=e(p["logo"]), nom=e(p["nom"]), acc=e(p["accroche"]), pour=e(p["pour"]),
           desc=e(p["description"]), bouton=bouton, prix=prix, slides=slides, navs=navs,
           pts=pts, qa=qa, email=e(STE["email"]),
           statut=('<div class="statut">%s</div>' % e(p["statut"])) if p.get("statut") else "",
           aussi=('<p class="aussi">%s</p>' % e(p["aussiPour"])) if p.get("aussiPour") else "",
           orient=orient)

    if multi:
        corps += """<script>
(function(){var pi=document.querySelector('.piste'),ps=document.querySelectorAll('.puce'),
n=%d,pos=0;function m(i){pos=(i+n)%%n;pi.style.transform='translateX(-'+(pos*100)+'%%)';
ps.forEach(function(x,k){x.classList.toggle('on',k===pos)})}
document.querySelector('.nav.g').onclick=function(){m(pos-1)};
document.querySelector('.nav.d').onclick=function(){m(pos+1)};
ps.forEach(function(x){x.onclick=function(){m(+x.dataset.i)}});
setInterval(function(){m(pos+1)},6000);})();
</script>""" % len(p["captures"])

    appli = {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": p["nom"], "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web, iOS, Android", "url": url,
        "description": p["description"],
        "offers": {"@type": "Offer", "price": p.get("prixValeur", ""), "priceCurrency": "EUR",
                   "availability": "https://schema.org/PreOrder" if p.get("statut")
                   else "https://schema.org/InStock"},
        "publisher": {"@type": "Organization", "name": STE["nom"]},
        "audience": {"@type": "Audience", "audienceType": p["pour"]},
    }
    if p.get("motsCles"):
        appli["keywords"] = ", ".join(p["motsCles"])
    faqld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]],
    }
    fil = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOMAINE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["nom"], "item": url},
        ],
    }
    og = DOMAINE + "/" + (p["captures"][0] if p["captures"] else p["logo"])
    return shell(p["seoTitle"], p["seoDesc"], url, [ORG, appli, faqld, fil], corps, og,
                 keywords=", ".join(p.get("motsCles", [])))

# ---------------------------------------------------------------- accueil
def page_accueil():
    cartes = ""
    for p in PRODUITS:
        cartes += """<a class="carte" href="{id}.html">
  <div class="logo"><img src="{logo}" alt="{nom}" onerror="this.parentNode.innerHTML='<h3>{nom}</h3>'"></div>
  {statut}<h3>{nom}</h3><div class="acc">{acc}</div><div class="desc">{desc}</div>
  <div class="pied"><div class="tag">{tarif}<small>{pour}</small></div><span class="fleche">Découvrir &rarr;</span></div>
</a>""".format(id=e(p["id"]), logo=e(p["logo"]), nom=e(p["nom"]), acc=e(p["accroche"]),
               desc=e(p["description"]), tarif=e(p.get("tarif") or "Sur devis"), pour=e(p["pour"]),
               statut=('<div class="statut">%s</div>' % e(p["statut"])) if p.get("statut") else "")

    corps = """
<main>
<section class="hero">
  <img class="bg" src="img/mgapps-banniere.png" alt="" aria-hidden="true" onerror="this.style.display='none'">
  <div class="wrap">
    <span class="r">Créé par un artisan, pour les pros du terrain</span>
    <h1>Des logiciels qui parlent le langage de votre métier.</h1>
    <p>{pitch}</p>
    <div class="cta"><a class="btn btn-or" href="#produits">Voir les produits</a>
    <a class="btn btn-clair" href="#contact">Nous contacter</a></div>
  </div>
</section>

<section class="sec" id="produits"><div class="wrap">
  <h2>Nos produits</h2><div class="sous">Chaque application résout un vrai problème de terrain.</div>
  <div class="cartes">{cartes}</div>
</div></section>

<section class="sec pourquoi" id="pourquoi"><div class="wrap">
  <h2 style="text-align:center;margin-bottom:36px">Pourquoi MG Apps</h2>
  <div class="grid">
    <div><div class="ic">&#128296;</div><h4>Né du terrain</h4><p>Nos outils sont nés dans une vraie entreprise, sur de vrais chantiers. Ils répondent à des besoins réels, pas à une idée de logiciel.</p></div>
    <div><div class="ic">&#128241;</div><h4>Simple, partout</h4><p>Ordinateur, tablette, téléphone. Rien à installer, tout se fait depuis le navigateur, et ça marche même sans réseau.</p></div>
    <div><div class="ic">&#128274;</div><h4>Vos données restent à vous</h4><p>Une base isolée par entreprise, hébergée en Europe. Vos données ne sont ni vendues, ni mélangées avec celles d'un autre.</p></div>
  </div>
</div></section>

<section class="sec contact" id="contact"><div class="wrap"><div class="box">
  <h2>Une question, une démonstration ?</h2>
  <p>Écrivez-nous, on répond vite et sans jargon. Suivez aussi nos actualités sur Facebook.</p>
  <div class="liens"><a class="btn btn-or" href="mailto:{email}">{email}</a>{fb}</div>
</div></div></section>
</main>
""".format(pitch=e(STE["pitch"]), cartes=cartes, email=e(STE["email"]), fb=bouton_fb())

    website = {"@context": "https://schema.org", "@type": "WebSite",
               "name": STE["nom"], "url": DOMAINE + "/", "inLanguage": "fr-FR"}
    liste = {"@context": "https://schema.org", "@type": "ItemList",
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["nom"],
                                  "url": DOMAINE + "/" + p["id"]} for i, p in enumerate(PRODUITS)]}
    kws = ["logiciel de gestion", "logiciel métier", "logiciel bâtiment", "profession libérale"]
    for p in PRODUITS:
        kws += p.get("motsCles", [])
    return shell(
        "MG Apps - Logiciels de gestion et de pilotage pour les pros du terrain",
        STE["pitch"], DOMAINE + "/", [ORG, website, liste], corps,
        DOMAINE + "/img/mgapps-banniere.png",
        keywords=", ".join(dict.fromkeys(kws)))

# ---------------------------------------------------------------- annexes SEO / IA
def robots():
    lignes = ["# MG Apps - robots.txt", "# Les robots d'IA sont les bienvenus.", "",
              "User-agent: *", "Allow: /", ""]
    for bot in STE["botsIA"]:
        lignes += ["User-agent: %s" % bot, "Allow: /", ""]
    lignes += ["Sitemap: %s/sitemap.xml" % DOMAINE, ""]
    return "\n".join(lignes)

def sitemap():
    urls = [DOMAINE + "/"] + [DOMAINE + "/" + p["id"] for p in PRODUITS]
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        x += ["  <url><loc>%s</loc><changefreq>monthly</changefreq></url>" % u]
    x += ["</urlset>"]
    return "\n".join(x)

def llms():
    t = ["# MG Apps", "",
         "> %s" % STE["pitch"], "",
         "MG Apps est un éditeur de logiciels français basé à Chatillon-sur-Seine, "
         "fondé par %s. Contact : %s." % (STE["fondateur"], STE["email"]), "",
         "## Produits", ""]
    for p in PRODUITS:
        t += ["### %s" % p["nom"],
              "- Pour : %s" % p["pour"],
              "- Ce que c'est : %s" % p["accroche"],
              "- Prix : %s" % (p.get("tarif") or "sur devis"),
              "- Page : %s/%s" % (DOMAINE, p["id"]),
              "- %s" % p["description"], ""]
        if p.get("aussiPour"):
            t += ["- Concerne aussi : %s" % p["aussiPour"]]
        if p.get("motsCles"):
            t += ["- Mots-clés : %s" % ", ".join(p["motsCles"])]
        t += ["", "Questions fréquentes :"]
        for f in p["faq"]:
            t += ["- %s %s" % (f["q"], f["a"])]
        t += [""]
    return "\n".join(t)

# ---------------------------------------------------------------- ecriture
def ecrire(nom, contenu):
    with io.open(os.path.join(BASE, nom), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenu)
    print("  ecrit : %s (%d o)" % (nom, len(contenu.encode("utf-8"))))

print("Generation du site MG Apps")
ecrire("index.html", page_accueil())
for p in PRODUITS:
    ecrire(p["id"] + ".html", page_produit(p))
ecrire("robots.txt", robots())
ecrire("sitemap.xml", sitemap())
ecrire("llms.txt", llms())
print("Termine : %d produits, %d pages + robots.txt + sitemap.xml + llms.txt"
      % (len(PRODUITS), 1 + len(PRODUITS)))
