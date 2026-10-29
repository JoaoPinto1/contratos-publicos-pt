# Notas para agentes

- Não faças pedidos repetidos ao `www.base.gov.pt`: a firewall bloqueia ao fim de ~10 pedidos (HTTP 999). Para explorar os dados, usa os dumps (ver `docs/fontes-de-dados.md`).
- Os dumps vão para `data/` (está no gitignore). Nunca os faças commit.
- Os adjudicatários com NIF `-` são muitas vezes pessoas singulares e o nome vem lá: trata-os como dados pessoais (RGPD). A regra está em `docs/esquema-de-saida.md`.
- Commits no formato `tipo: descrição`, em português.
