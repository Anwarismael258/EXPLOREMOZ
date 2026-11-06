from urllib.parse import quote

PHOTOS = {
    "bazaruto": ("Bazaruto visto do ar", "Bazaruto from the air", "Bazaruto Island Mozambique from air.jpg", "Tom Corser", "by-sa/3.0"),
    "maputo": ("Estação ferroviária de Maputo", "Maputo railway station", "Caminhos de Ferro de Mocambique, Railway Station in Maputo, Mozambique.jpg", "Justin K G Dumpleton", None),
    "katembe": ("Praia da Katembe e ponte sobre a baía", "Katembe beach and bridge across the bay", "Katembe beach with bridge.jpg", "Jcornelius", "by-sa/4.0"),
    "gorongosa": ("Monte Gorongosa", "Mount Gorongosa", "Mount Gorongosa, Gorongosa National Park, Mozambique (46316615492).jpg", "Judy Gallagher", "by/2.0"),
    "polana": ("Hotel Polana, Maputo", "Polana Hotel, Maputo", "Hotel Polana.jpg", "F Mira", "by-sa/2.0"),
}

def photo(slug, en):
    pt, english, *_ = PHOTOS[slug]
    return f'<img src="/media/{slug}.webp" alt="{english if en else pt}" loading="lazy" decoding="async">'

def gallery(en, prefix):
    tiles = []
    for slug, (pt, english, filename, author, license_id) in PHOTOS.items():
        source = "https://commons.wikimedia.org/wiki/File:" + quote(filename.replace(" ", "_"))
        license_label = ('Public domain' if en else 'Domínio público') if not license_id else f'CC {license_id.replace("/", " ").upper()}'
        license_markup = f'<a href="https://creativecommons.org/licenses/{license_id}/">{license_label}</a>' if license_id else license_label
        title = english if en else pt
        tiles.append(f'<figure><a class="photo-frame" href="{source}">{photo(slug, en)}</a><figcaption><strong>{title}</strong><small>{author} · {license_markup} · <a href="{source}">Wikimedia Commons</a> · {"resized" if en else "redimensionada"}</small></figcaption></figure>')
    return f'<section class="section photo-section" id="fotografias"><small>{"MOZAMBIQUE IN PHOTOGRAPHS" if en else "MOÇAMBIQUE EM FOTOGRAFIAS"}</small><h2>{"From the Indian Ocean to the mountains" if en else "Do Índico à serra"}</h2><div class="photo-grid">{"".join(tiles)}</div></section>'
