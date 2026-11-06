from photography import PHOTOS, photo

# Editorial navigation for the public catalogue.
SECTIONS = [
 ("alojamento", "Onde ficar", "Where to stay", "Compare tipos de alojamento e escolha uma região para a sua base.", "Compare accommodation types and choose a region to base yourself.", [
 ("Hotéis e estadias urbanas", "Hotels and city stays", "maputo"),
 ("Lodges e estadias junto à costa", "Lodges and coastal stays", "vilankulo"),
 ("Estadias próximas da natureza", "Stays close to nature", "gorongosa")]),
 ("experiencias", "Experiências", "Things to do", "Encontre ideias para uma viagem de praia, aventura ou cultura.", "Find ideas for a beach, adventure or cultural trip.", [
 ("Passeios de barco", "Boat trips", "bazaruto"),
 ("Actividades marítimas", "Ocean activities", "ponta-do-ouro"),
 ("Passeios culturais", "Cultural walks", "ilha-de-mocambique")]),
 ("gastronomia", "Onde comer", "Where to eat", "Planeie paragens para descobrir a gastronomia local.", "Plan stops to explore local food.", [
 ("Mercados e comida da cidade", "Markets and city food", "maputo"),
 ("Sabores da baía", "Flavours from the bay", "inhambane"),
 ("Gastronomia na costa", "Coastal food", "vilankulo")]),
 ("natureza", "Natureza e aventura", "Nature and adventure", "Explore parques, ilhas e paisagens costeiras.", "Explore parks, islands and coastal landscapes.", [
 ("Parque e conservação", "Parks and conservation", "gorongosa"),
 ("Ilhas e dunas", "Islands and dunes", "bazaruto"),
 ("Praias do sul", "Southern beaches", "ponta-do-ouro")]),
 ("cultura", "Cultura e património", "Culture and heritage", "Conheça o património construído e a história de Moçambique.", "Discover Mozambique's built heritage and history.", [
 ("Passeios pela capital", "Walks in the capital", "maputo"),
 ("Património insular", "Island heritage", "ilha-de-mocambique"),
 ("Centro histórico e baía", "Old town and bay", "inhambane")]),
 ("transporte", "Transporte e como chegar", "Transport and getting there", "Organize os trajectos entre cidades, praias e ilhas.", "Plan your journeys between cities, beaches and islands.", [
 ("Chegada à capital", "Arriving in the capital", "maputo"),
 ("Percurso até à costa", "Getting to the coast", "xai-xai"),
 ("Travessia para o arquipélago", "Crossing to the archipelago", "bazaruto")]),
 ("guias", "Guias locais", "Local guides", "Escolha o destino e o tipo de visita antes de procurar um guia.", "Choose a destination and the kind of visit before looking for a guide.", [
 ("Visitas de património", "Heritage tours", "ilha-de-mocambique"),
 ("Observação da natureza", "Wildlife viewing", "gorongosa"),
 ("Passeios costeiros", "Coastal tours", "vilankulo")]),
 ("eventos", "Eventos e lazer", "Events and leisure", "Escolha a região e confirme datas directamente com os organizadores.", "Choose a region and confirm dates directly with organisers.", [
 ("Programação cultural na capital", "Cultural programmes in the capital", "maputo"),
 ("Actividades locais na baía", "Local activities by the bay", "inhambane")]),
]

def publish_sections(en, prefix, other, places, page, save, art):
    def t(pt, eng):
        return eng if en else pt

    index = {item[0]: item for item in places}
    cards = []
    for slug, pt, eng, summary, summary_en, ideas in SECTIONS:
        title = t(pt, eng)
        description = t(summary, summary_en)
        url = f"/{prefix}{slug}/"
        cards.append(f'<article class="card card-content"><h3><a href="{url}">{title} →</a></h3><p>{description}</p></article>')
        suggestions = []
        for idea, idea_en, destination in ideas:
            item = index[destination]
            photo_slug = {("alojamento", "maputo"): "polana", ("transporte", "maputo"): "katembe"}.get((slug, destination), destination)
            visual = photo(photo_slug, en) if photo_slug in PHOTOS else art(item[-1])
            suggestions.append(f'<article class="card"><div class="cover">{visual}</div><div class="card-content"><small>{item[1]}</small><h3><a href="/{prefix}destinos/{destination}/">{t(idea, idea_en)} →</a></h3><p>{t(item[5], item[6])}</p></div></article>')
        body = f"""<section class="detail" id="top"><a href="/{prefix}#discover">← {t('Explorar categorias','Explore categories')}</a><h1 class="section-heading">{title}</h1><p class="intro">{description}</p><h2>{t('Ideias para a viagem','Trip ideas')}</h2><div class="cards">{''.join(suggestions)}</div><p class="editorial-note">{t('Guias de inspiração. Confirme preços, datas e disponibilidade com o operador antes de viajar.','Ideas for your trip. Confirm prices, dates and availability with the operator before travelling.')}</p><a class="primary" href="/{prefix}#planner">{t('Planear viagem','Plan a trip')} →</a> <a href="/{prefix}#fotografias">{t('Créditos das fotografias','Photo credits')}</a></section>"""
        save(f"{prefix}{slug}", page(title, description, body, en, f"{other}{slug}/"))
    return f'<section class="section" id="discover"><small>{t("EXPLORE POR INTERESSE","EXPLORE BY INTEREST")}</small><h2>{t("Tudo começa com uma ideia","It all starts with an idea")}</h2><div class="cards">{"".join(cards)}</div></section>'
