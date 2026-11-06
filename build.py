"""Generate the Explore Moz static catalogue."""
from html import escape
from pathlib import Path
import shutil
from sections import publish_sections
from photography import PHOTOS, gallery, photo

places = [
 ("maputo","Maputo","Cidade de Maputo","Cultura","Culture","Arquitectura, mercados e sabores à beira da baía.","Architecture, markets and flavours by the bay.",-25.97,32.57,"Explore a Baixa, a estação ferroviária e os espaços culturais da cidade.","Explore downtown, the railway station and the city's cultural spaces.","city"),
 ("matola","Matola","Maputo","Cultura","Culture","Uma perspectiva local sobre a área metropolitana.","A local perspective on the metropolitan area.",-25.96,32.46,"Combine uma visita cultural com uma paragem gastronómica.","Combine a cultural visit with a stop for local food.","city"),
 ("ponta-do-ouro","Ponta do Ouro","Maputo","Praia","Beach","Dunas, praia e experiências no Índico.","Dunes, beaches and Indian Ocean experiences.",-26.84,32.89,"Explore a costa e consulte operadores locais para actividades marítimas.","Explore the coast and ask local operators about ocean activities.","sea"),
 ("xai-xai","Xai-Xai","Gaza","Praia","Beach","Uma escapadinha entre a cidade e a costa.","A getaway between town and coast.",-25.05,33.64,"Reserve tempo para conhecer a cidade e a Praia de Xai-Xai.","Set aside time to explore town and Xai-Xai Beach.","sea"),
 ("inhambane","Inhambane","Inhambane","Cultura","Culture","Património urbano e paisagens da baía.","Urban heritage and bay landscapes.",-23.86,35.38,"Passeie pelo centro e combine a visita com uma extensão à costa.","Walk through the centre and consider extending your trip to the coast.","city"),
 ("vilankulo","Vilankulo","Inhambane","Praia","Beach","Um ponto de partida para explorar o arquipélago de Bazaruto.","A gateway to the Bazaruto Archipelago.",-22,35.32,"Descubra a costa e consulte operadores locais para passeios de barco.","Discover the coast and ask local operators about boat trips.","sea"),
 ("bazaruto","Bazaruto","Inhambane","Natureza","Nature","Dunas e ilhas num arquipélago do Índico.","Dunes and islands in an Indian Ocean archipelago.",-21.65,35.47,"Planeie a travessia com um operador e confirme as condições marítimas.","Plan the crossing with an operator and confirm sea conditions.","sea"),
 ("gorongosa","Gorongosa","Sofala","Natureza","Nature","Paisagens de conservação no centro de Moçambique.","Conservation landscapes in central Mozambique.",-18.76,34.49,"Consulte o parque para conhecer as modalidades de visita e os horários.","Check with the park for visiting options and opening hours.","land"),
 ("ilha-de-mocambique","Ilha de Moçambique","Nampula","Cultura","Culture","Património, arquitectura e histórias do Índico.","Heritage, architecture and stories of the Indian Ocean.",-15.03,40.74,"Explore a ilha a pé e procure um guia local para contextualizar o património.","Explore on foot and consider a local guide to understand the island's heritage.","city"),
]

def page(title, description, body, en=False, switch="/", extra=""):
    return f"""<!doctype html><html lang="{'en' if en else 'pt-MZ'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · Explore Moz</title><meta name="description" content="{escape(description,quote=True)}"><meta property="og:title" content="{escape(title,quote=True)} · Explore Moz"><meta property="og:description" content="{escape(description,quote=True)}"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{extra}<script src="/app.js" defer></script></head><body><header><a class="brand" href="{'/en/' if en else '/'}"><img src="/icon.svg" alt="" width="36" height="36">Explore<b>Moz</b></a><nav aria-label="{'Navigation' if en else 'Navegação'}"><a href="{'/en/' if en else '/'}#catalog">{'Destinations' if en else 'Destinos'}</a><a href="{'/en/' if en else '/'}#planner">{'My trip' if en else 'Minha viagem'}</a><a class="language" href="{switch}" hreflang="{'pt-MZ' if en else 'en'}">{'PT' if en else 'EN'}</a></nav></header><main>{body}</main><footer><strong>Explore Moz</strong><span>{'A DeliGo Triunfal initiative' if en else 'Uma iniciativa da DeliGo Triunfal'}</span><a href="#top">{'Back to top ↑' if en else 'Voltar ao topo ↑'}</a></footer></body></html>"""

def art(kind):
    palettes={"sea":("#84d9ce","#187d79","#ecd39a"),"city":("#f0c581","#a75c41","#efd7ab"),"land":("#adbf87","#526b40","#dfb96e")}
    sky,deep,sand=palettes[kind]
    shape={
        "sea":f'<path fill="{deep}" d="M0 108Q110 52 223 107T480 90V300H0Z"/><path fill="{sand}" d="M0 266Q130 152 480 176V300H0Z"/><path fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="4" d="M0 250Q155 142 480 165"/>',
        "city":f'<path fill="{deep}" d="M0 160h48v-29h56v29h26v-56h85v56h32v-31h74v31h39v-73h74v73h46v140H0Z"/><path fill="{sand}" d="M0 226h480v74H0Z"/><path stroke="{sand}" stroke-width="8" stroke-dasharray="12 19" d="M22 191h440"/>',
        "land":f'<path fill="{deep}" d="M0 163 113 58l110 122 118-100 139 70v150H0Z"/><path fill="{sand}" d="M0 241Q164 121 480 217v83H0Z"/>'
    }[kind]
    return f'<svg viewBox="0 0 480 300" aria-hidden="true" preserveAspectRatio="xMidYMid slice"><rect width="480" height="300" fill="{sky}"/><circle cx="361" cy="61" r="30" fill="#fff0bd"/>{shape}</svg>'

out = Path("dist")
out.mkdir(exist_ok=True)
for file in ("style.css","app.js","icon.svg"):
    shutil.copyfile(file,out/file)
shutil.copytree("media", out / "media", dirs_exist_ok=True)

def save(path, html):
    target=out/path/"index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html,encoding="utf-8")

for en in (False,True):
    def t(pt, english): return english if en else pt
    prefix=t("","en/")
    other=t("/en/","/")
    cards=[]
    pins=[]
    options=[]
    for slug,name,province,cat,eng,desc,translation,lat,lon,guide,guide_en,kind in places:
        category=t(cat,eng)
        summary=t(desc,translation)
        href=f"/{prefix}destinos/{slug}/"
        options.append(f'<option value="{slug}">{name}</option>')
        pins.append(f'<a href="{href}" data-pin="{slug}" style="--x:{(lon-30)*7.3:.2f}%;--y:{(-lat-10)*5.25:.2f}%" title="{name}" aria-label="{name}"><span></span></a>')
        cover = photo(slug, en) if slug in PHOTOS else art(kind)
        cards.append(f'<article class="card" data-id="{slug}" data-category="{category}" data-province="{province}"><a href="{href}" class="cover" tabindex="-1" aria-hidden="true">{cover}</a><div class="card-content"><small>{province} · {category}</small><h3><a href="{href}">{name}</a></h3><p>{summary}</p><button class="save" type="button" data-save="{slug}" aria-pressed="false" aria-label="{t("Guardar","Save")} {name}">♡</button></div></article>')
        body=f"""<section class="detail" id="top"><a href="/{prefix}#catalog">← {t('Todos os destinos','All destinations')}</a><div class="detail-grid"><div><small>{province} · {category}</small><h1>{name}</h1><p class="intro">{summary}</p><button class="primary" data-save="{slug}" aria-pressed="false">{t('Guardar nos favoritos','Save to favourites')}</button></div><div class="detail-art">{cover}</div></div></section><section class="guide"><h2>{t('O que explorar','What to explore')}</h2><p>{t(guide,guide_en)}</p>{f'<p><a href="/{prefix}#fotografias">{t("Créditos da fotografia","Photo credits")}</a></p>' if slug in PHOTOS else ''}<h2>{t('Localização','Location')}</h2><a href="https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lon}#map=10/{lat}/{lon}">{t('Ver no OpenStreetMap ↗','View on OpenStreetMap ↗')}</a><p><a href="/{prefix}#planner">{t('Abrir planeador de viagem →','Open trip planner →')}</a></p></section>"""
        save(Path(prefix)/"destinos"/slug,page(name,summary,body,en,f"{other}destinos/{slug}/"))
    provinces="".join(f"<option>{p}</option>" for p in dict.fromkeys(row[2] for row in places))
    categories="".join(f'<button data-category-filter="{label}" aria-pressed="false" type="button">{label}</button>' for label in [t("Praia","Beach"),t("Natureza","Nature"),t("Cultura","Culture")])
    title=t("Moçambique começa aqui.","Mozambique starts here.")
    desc=t("Descubra destinos, inspire-se com novas experiências e planeie a sua próxima viagem por Moçambique.","Discover destinations, find inspiration and plan your next trip across Mozambique.")
    discovery = publish_sections(en, prefix, other, places, page, save, art)
    photography = gallery(en, prefix)
    body=f"""<section class="hero" id="top"><div class="scene hero-film" aria-hidden="true"><img src="/media/poster.webp" alt="" fetchpriority="high"><video id="hero-video" data-src="/media/mozambique.mp4" poster="/media/poster.webp" muted loop playsinline preload="none" tabindex="-1"></video></div><button type="button" id="hero-video-toggle" class="video-toggle" hidden data-play="{t('Reproduzir vídeo','Play video')}" data-pause="{t('Pausar vídeo','Pause video')}">{t('Reproduzir vídeo','Play video')}</button><div class="hero-copy"><small>{t("GUIA DE VIAGEM · MOÇAMBIQUE","TRAVEL GUIDE · MOZAMBIQUE")}</small><h1>{title}</h1><p>{desc}</p><a class="primary" href="#catalog">{t("Explorar destinos","Explore destinations")} ↘</a></div></section>
{photography}
{discovery}
<section class="section" id="catalog"><div class="section-title"><div><small>{t("ESCOLHA O SEU PRÓXIMO DESTINO","FIND YOUR NEXT DESTINATION")}</small><h2>{t("O que gostaria de explorar?","What would you like to explore?")}</h2></div><a href="#map">{t("Ver mapa","View map")} ↗</a></div><div class="filters"><label>{t("Pesquisar destinos","Search destinations")}<input id="search" type="search" placeholder="{t('Ex. Vilankulo','E.g. Vilankulo')}"></label><label>{t("Província","Province")}<select id="province"><option value="">{t("Todas","All")}</option>{provinces}</select></label></div><div class="chips"><button data-category-filter="" aria-pressed="true" type="button">{t("Todos","All")}</button>{categories}<button id="favorites" aria-pressed="false" type="button">♡ {t("Favoritos","Favourites")}</button></div><p id="results" role="status"></p><div class="cards">{''.join(cards)}</div></section>
<section id="map" class="section map-section"><div><small>{t("DO LITORAL AO INTERIOR","FROM COAST TO INLAND")}</small><h2>{t("Explore pelo mapa","Explore on the map")}</h2><p>{t("Seleccione um ponto para abrir o guia do destino. O esquema acompanha os filtros do catálogo.","Select a marker to open its destination guide. The schematic follows the catalogue filters.")}</p><p><small>{t("Mapa esquemático · Localizações aproximadas","Schematic map · Approximate locations")}</small></p></div><div class="map"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M59 9 90 6 87 29 75 40 60 43 46 53 42 67 26 78 23 92 15 92 13 79 21 68 18 53 27 43 3 31 11 27 40 34 49 23 50 13Z" fill="#abc6a2" stroke="#305f52" stroke-width=".5"/></svg>{''.join(pins)}</div></section>
<section class="section planner" id="planner"><div><small>{t("MINHA VIAGEM","MY TRIP")}</small><h2>{t("Da inspiração ao itinerário","From inspiration to itinerary")}</h2><p>{t("Guarde um plano neste dispositivo e leve uma cópia consigo.","Save a plan on this device and take a copy with you.")}</p></div><form id="trip"><label>{t("Origem","Starting point")}<input name="origin" required maxlength="100"></label><label>{t("Destino","Destination")}<select name="destination">{''.join(options)}</select></label><label>{t("Chegada","Arrival")}<input name="arrival" type="date" required></label><label>{t("Partida","Departure")}<input name="departure" type="date" required></label><label>{t("Pessoas","Travellers")}<input name="people" type="number" min="1" max="100" value="2" required></label><button class="primary" type="submit">{t("Guardar itinerário","Save itinerary")}</button></form><div id="trip-result" role="status"></div><button id="download" type="button" hidden>{t("Descarregar itinerário","Download itinerary")}</button></section>"""
    save(Path(prefix),page(title,desc,body,en,other))

from xml.sax.saxutils import escape as xml_escape
base_url = "https://exploremoz.vercel.app"
urls = sorted(base_url + "/" + path.relative_to(out).as_posix().removesuffix("index.html") for path in out.rglob("index.html"))
entries = "".join("<url><loc>" + xml_escape(url.rstrip("/") + "/") + "</loc></url>" for url in urls)
(out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + entries + "</urlset>", encoding="utf-8")
(out / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + base_url + "/sitemap.xml\n", encoding="utf-8")
