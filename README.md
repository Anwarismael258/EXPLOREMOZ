# Explore Moz

Catálogo turístico bilingue com páginas estáticas, pesquisa, filtros, mapa esquemático, favoritos e planeador local. O catálogo editorial está em `build.py`. As ilustrações são vectoriais.

## Executar

```sh
python3 build.py
python3 -m http.server 8080 --directory dist
```

O projecto não tem dependências externas de compilação. Importe o repositório na Vercel com o directório raiz do projecto. A configuração em `vercel.json` gera e publica `dist/`.

Os favoritos e o itinerário ficam no navegador. O catálogo não liga a um sistema de reservas, autenticação, pagamentos, avaliações ou administração. Os pontos do mapa são aproximados. A arquitectura estática permite servir o catálogo via CDN, mas a capacidade para um volume concreto requer medição com o plano e tráfego reais.
