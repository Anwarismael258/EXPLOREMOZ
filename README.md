# Explore Moz

Catálogo turístico bilingue com páginas estáticas, pesquisa, filtros, mapa esquemático, favoritos e planeador local. O catálogo editorial está em `build.py`. As ilustrações são vectoriais.

## Executar

```sh
python3 build.py
python3 -m http.server 8080 --directory dist
```

O projecto não tem dependências externas de compilação. Importe o repositório na Vercel com o directório raiz do projecto. A configuração em `vercel.json` gera e publica `dist/`.

Os favoritos e o itinerário ficam no navegador. O catálogo não liga a um sistema de reservas, autenticação, pagamentos, avaliações ou administração. Os pontos do mapa são aproximados. A arquitectura estática permite servir o catálogo via CDN, mas a capacidade para um volume concreto requer medição com o plano e tráfego reais.

## Plataforma e Central

A migração em `supabase/migrations` é uma base de desenvolvimento. O catálogo é público e o fluxo previsto de autenticação para o turista usa confirmação por email. O pedido de suporte requer conta autenticada, sem KYC. A candidatura de parceiros começa com documentos pendentes. A aprovação é uma transição reservada ao backend e deverá preceder publicação de ofertas.

A fila de saída regista referências de suporte e início de candidatura na mesma transacção do registo original. Para activar o fluxo de produção, validar a migração no Supabase do Explore Moz, configurar autenticação por email e armazenamento privado de documentos e ligar um consumidor autenticado à Central. O consumidor deve deduplicar por ID de evento, marcar entrega após confirmação e usar acesso restrito para consultar os registos. O catálogo não apresenta formulários de envio enquanto estes serviços estiverem por ligar.

Quando PaySuite e Stripe forem integrados, a receita deve chegar à Central a partir de pagamentos confirmados no servidor, com validação dos webhooks, reconciliação e deduplicação por evento e transacção. O catálogo público continua a ser servido pela CDN e não chama os serviços de conta por visita.
