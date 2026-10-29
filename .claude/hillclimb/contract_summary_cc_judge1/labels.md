# Etiquetas para calibrar o juiz

> **Atenção:** estas etiquetas foram atribuídas pelo Claude Opus 5.5 (a pedido do João), não por uma pessoa, e **não às cegas**: o etiquetador já tinha lido as razões do juiz nos casos reprovados. Medem concordância entre dois modelos, não calibração humana.

Para cada resumo, substitui cada `?` por `s` (cumpre) ou `n` (não cumpre). Critérios:

- **faithful**: Every factual claim in the summary is supported by the contract data or the notable points. No invented purpose, context, entity, amount, date or role; buyer and contractor are not swapped; a private individual is not named or speculated about.
- **core**: The summary states (a) what is being bought, or that the object is not described when the data only has codes, (b) the contracting entity, (c) the contractor(s), and (d) the price.
- **notable**: The summary mentions every notable point listed (or there are none). A point counts as mentioned if its meaning is conveyed, even in other words.
- **clear**: The summary is written in the requested language, in 2 to 3 sentences of plain prose (no markdown, no bullet points, no preamble), and is understandable by a non-specialist.

## L01 · caso c40 · língua en

- **Descrição:** AQUISIÇÃO DE SULPIRIDA  50 MG CÁPS E DE SULPIRIDA 200 MG COMP
- **Adjudicante:** Unidade Local de Saúde de São José, E. P. E. [508080142]
- **Adjudicatário(s):** Neuraxpharm Portugal, Unipessoal, Lda. [515471224]
- **Preço:** 97.2 € (base: None) · **Procedimento:** Ao abrigo de acordo-quadro (art.º 259.º)
- **Destaques calculados:** the contract was awarded under a framework agreement; the procedure was split into lots
- Dados completos: `cases.md`, secção c40

**Resumo:**

> Unidade Local de Saúde de São José, E. P. E. is buying sulpiride, a pharmaceutical product, in 50 mg capsules and 200 mg tablets, from Neuraxpharm Portugal, Unipessoal, Lda., for 97.2 euros. The contract was awarded under a framework agreement for various medicines that was formed through an international public tender. The procedure was split into lots, and this contract covers lot S162 (sulpiride 50 mg capsules).

faithful: s core: s notable: s clear: s

## L02 · caso c34 · língua pt

- **Descrição:** 52/AQ/AT/2026 - Aquisição de serviços de desenvolvimento aplicacional no âmbito da necessidade de implementação do projeto Adaptação do (sub)sistema de cadastro de veículos ás novas regras de liquidação do Imposto Único de Circulação (IUC)
- **Adjudicante:** Autoridade Tributária e Aduaneira [600084779]
- **Adjudicatário(s):** (particular) [-]; ACCENTURE (UK) Limited [-]; Accenture, Consultores de Gestão, SA [502309440]; Accenture Technology Solutions S.A. [502443855]
- **Preço:** 389550.0 € (base: 397500.0) · **Procedimento:** Ao abrigo de acordo-quadro (art.º 259.º)
- **Destaques calculados:** 26 bidders took part in the procedure; the contract was awarded under a framework agreement; the contract was awarded to 4 contractors; a contractor is a private individual (name removed for privacy)
- Dados completos: `cases.md`, secção c34

**Resumo:**

> A Autoridade Tributária e Aduaneira contratou serviços de desenvolvimento de software para adaptar o (sub)sistema de cadastro de veículos às novas regras de liquidação do Imposto Único de Circulação (IUC), por 389 550 euros. O contrato foi adjudicado ao abrigo de um acordo-quadro a quatro adjudicatários: um particular, a ACCENTURE (UK) Limited, a Accenture, Consultores de Gestão, SA e a Accenture Technology Solutions S.A. Participaram 26 concorrentes no procedimento.

faithful: s core: s notable: s clear: s

## L03 · caso c13 · língua pt

- **Descrição:** PRESTAÇÃO DE SERVIÇOS TÉCNICOS - PROGRAMAÇÃO SENTIR O VERÃO 2026
- **Adjudicante:** Município de Penafiel [501073663]
- **Adjudicatário(s):** Simbiose - Gestão Cultural, Unipessoal LDA [514616423]
- **Preço:** 4950.0 € (base: 48500.0) · **Procedimento:** Concurso público
- **Destaques calculados:** only one bidder took part in the procedure; the procedure was split into lots
- Dados completos: `cases.md`, secção c13

**Resumo:**

> Trata-se de uma prestação de serviços técnicos para a programação "Sentir o Verão 2026", adjudicada pelo Município de Penafiel à empresa Simbiose - Gestão Cultural, Unipessoal LDA, na sequência de um concurso público. O preço do contrato é de 4.950 euros (preço base de 48.500 euros). Notas: apenas um concorrente participou no procedimento, e este foi dividido em lotes (o contrato refere o Lote 1 - 17 de Julho).

faithful: s core: s notable: s clear: n

## L04 · caso c46 · língua pt

- **Descrição:** Aquisição de Serviços de Assistência Técnica aos equipamentos de emissão de radiação ionizante (RX Intraoral e RX Digital) e às cadeiras de estomatologia, com equipamentos de esterilização, localizados no Serviço de Estomatologia e nas Unidades de Cuidados de Saúde Primários e também aos CART localizados nos blocos operatórios do HESS e HNSA, da Unidade Local de Saúde Gaia Espinho, E.P.E. (ULSGE E.P.E.)
- **Adjudicante:** Unidade Local de Saúde de Gaia/Espinho, EPE [508142156]
- **Adjudicatário(s):** Serviço de Utilização Comum dos Hospitais [500900469]
- **Preço:** 11097.96 € (base: 11097.96) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c46

**Resumo:**

> A Unidade Local de Saúde de Gaia/Espinho, EPE contratou ao Serviço de Utilização Comum dos Hospitais serviços de assistência técnica, por 365 dias, aos equipamentos de raio-X (RX Intraoral e RX Digital), às cadeiras de estomatologia com equipamentos de esterilização do Serviço de Estomatologia e das Unidades de Cuidados de Saúde Primários, e ainda aos CART dos blocos operatórios do HESS e do HNSA. O contrato tem um preço de 11097,96 euros e foi celebrado ao abrigo do artigo 5.º, n.º 1, do Código dos Contratos Públicos, ou seja, como contratação excluída das regras de procedimento desse Código. Apenas um concorrente participou no procedimento.

faithful: s core: s notable: s clear: s

## L05 · caso c29 · língua pt

- **Descrição:** 090000042025-REAGENTES P/O SERVIÇO DE ANATOMIA PATOLOGICA
- **Adjudicante:** Unidade Local de Saúde de Coimbra, E. P. E. [510103448]
- **Adjudicatário(s):** Microgene - Produtos de Laboratório Lda. [513656677]; Bioportugal [502380543]; LEICA MICROSISTEMAS-INSTRUMENTOS DE PRECISÃO, S.U., LDA. [500301921]; Lusopalex - Produtos de Saude Unipessoal Lda [503531588]; Master-InVitro [515007897]; ENZIfarma ? Diagnostica e Farmacêutica, S.A. [503636975]; ZMWAY, Lda. [508085349]
- **Preço:** 54933.75 € (base: 62246.88) · **Procedimento:** Consulta Prévia
- **Destaques calculados:** the contract was awarded to 7 contractors
- Dados completos: `cases.md`, secção c29

**Resumo:**

> A Unidade Local de Saúde de Coimbra, E. P. E. contratou, por consulta prévia, a aquisição de reagentes para o serviço de anatomia patológica, com um preço contratual de 54 933,75 euros e execução prevista de 365 dias. O contrato foi adjudicado a sete fornecedores: Microgene - Produtos de Laboratório Lda., Bioportugal, Leica Microsistemas - Instrumentos de Precisão, S.U., Lda., Lusopalex - Produtos de Saúde Unipessoal Lda., Master-InVitro, ENZIfarma - Diagnóstica e Farmacêutica, S.A. e ZMWAY, Lda.

faithful: s core: s notable: s clear: s

## L06 · caso c29 · língua pt

- **Descrição:** 090000042025-REAGENTES P/O SERVIÇO DE ANATOMIA PATOLOGICA
- **Adjudicante:** Unidade Local de Saúde de Coimbra, E. P. E. [510103448]
- **Adjudicatário(s):** Microgene - Produtos de Laboratório Lda. [513656677]; Bioportugal [502380543]; LEICA MICROSISTEMAS-INSTRUMENTOS DE PRECISÃO, S.U., LDA. [500301921]; Lusopalex - Produtos de Saude Unipessoal Lda [503531588]; Master-InVitro [515007897]; ENZIfarma ? Diagnostica e Farmacêutica, S.A. [503636975]; ZMWAY, Lda. [508085349]
- **Preço:** 54933.75 € (base: 62246.88) · **Procedimento:** Consulta Prévia
- **Destaques calculados:** the contract was awarded to 7 contractors
- Dados completos: `cases.md`, secção c29

**Resumo:**

> Este contrato consiste na aquisição de reagentes de laboratório para o Serviço de Anatomia Patológica da Unidade Local de Saúde de Coimbra, E. P. E., tendo sido adjudicado a sete empresas: Microgene - Produtos de Laboratório Lda., Bioportugal, LEICA MICROSISTEMAS-INSTRUMENTOS DE PRECISÃO, S.U., LDA., Lusopalex - Produtos de Saude Unipessoal Lda, Master-InVitro, ENZIfarma ? Diagnostica e Farmacêutica, S.A. e ZMWAY, Lda. O preço contratual é de 54 933,75 euros, abaixo do preço base de 62 246,88 euros, e o procedimento utilizado foi uma consulta prévia, em que a entidade convida diretamente algumas empresas a apresentar propostas.

faithful: s core: s notable: s clear: s

## L07 · caso c41 · língua pt

- **Descrição:** Acordo-Quadro para prestação de serviços de Vigilância e Segurança 2
- **Adjudicante:** Comunidade Intermunicipal do Tâmega e Sousa [508889910]
- **Adjudicatário(s):** Strong Charon, Soluções de Segurança, SA [503257567]; Securitas - Serviços e Tecnologia de Segurança, SA [500243719]; 2045 - Gália - Consórcio ANCP - serviços de vigilância e segurança [502332905]; Powershield - Segurança Privada, SA [510652581]; Ronsegur, Rondas e Segurança, S.A [507011724]; Prestibel - Empresa de Segurança, S.A. [501326456]
- **Preço:** 0.0 € (base: 1500000.0) · **Procedimento:** Concurso limitado por prévia qualificação
- **Destaques calculados:** 6 bidders took part in the procedure; the registered price is 0: no fixed value was registered (usual for framework agreements); the contract was awarded to 6 contractors; the procedure was split into lots
- Dados completos: `cases.md`, secção c41

**Resumo:**

> A Comunidade Intermunicipal do Tâmega e Sousa lançou um acordo-quadro, por concurso limitado por prévia qualificação, para serviços de vigilância e segurança, dividido em três lotes: vigilância e segurança humana, ligação a central de receção e monitorização de alarmes, e serviços combinados de ambos. Participaram seis concorrentes, e o contrato foi adjudicado a seis entidades (Strong Charon, Securitas, o Consórcio 2045 - Gália, Powershield, Ronsegur e Prestibel), sem valor fixo registado, o que é habitual em acordos-quadro. O preço base indicado é de 1,5 milhões de euros, com execução prevista de 731 dias.

faithful: s core: s notable: s clear: s

## L08 · caso c05 · língua pt

- **Descrição:** SPC - SARSTEDT
- **Adjudicante:** Unidade Local de Saúde de Coimbra, E. P. E. [510103448]
- **Adjudicatário(s):** Sarstedt, Lda [503019461]
- **Preço:** 782.0 € (base: 573.5) · **Procedimento:** Ajuste Direto Regime Geral
- **Destaques calculados:** the contract price is 36.4% above the procedure's base price
- Dados completos: `cases.md`, secção c05

**Resumo:**

> Este contrato de aquisição de bens refere-se a reagentes de laboratório, segundo a classificação CPV, embora a descrição do registo («SPC - SARSTEDT») não detalhe o objeto. Foi celebrado pela Unidade Local de Saúde de Coimbra, E. P. E., com a Sarstedt, Lda, por ajuste direto, pelo preço de 782 euros e com um prazo de execução de 365 dias. O preço contratual ficou 36,4% acima do preço base do procedimento, que era de 573,5 euros.

faithful: s core: s notable: s clear: s

## L09 · caso c49 · língua pt

- **Descrição:** Deposito de pedido de patente EPO e US da tecnologia Sensing Device
- **Adjudicante:** CENTITVC - Centro de Nanotecnologia e Materiais Técnicos, Funcionais e Inteligentes [507682734]
- **Adjudicatário(s):** Patentree, Unipessoal Lda [510638490]
- **Preço:** 7003.47 € (base: 7003.47) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c49

**Resumo:**

> A entidade adjudicante é o CENTITVC - Centro de Nanotecnologia e Materiais Técnicos, Funcionais e Inteligentes, que contratou por ajuste direto (contratação excluída II) a aquisição de serviços para depósito de pedido de patente EPO e US da tecnologia "Sensing Device", à empresa Patentree, Unipessoal Lda, pelo valor de 7.003,47 euros. Trata-se de um procedimento em que apenas um concorrente participou.

faithful: n core: s notable: s clear: s

## L10 · caso c45 · língua pt

- **Descrição:** Aquisição de serviços para atualização de sistema propulsão PRAXIS para NI Mário Ruivo
- **Adjudicante:** Instituto Português do Mar e da Atmosfera, IP [510265600]
- **Adjudicatário(s):** FRANCISCO CARDAMA, S.A. [-]
- **Preço:** 48100.0 € (base: 48100.0) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c45

**Resumo:**

> O Instituto Português do Mar e da Atmosfera, IP, adjudicou à empresa FRANCISCO CARDAMA, S.A. a aquisição de serviços para atualização do sistema de propulsão PRAXIS do navio de investigação Mário Ruivo, por 48.100 euros, através de um procedimento de contratação excluída II. Foi apresentada apenas uma proposta, o que é um ponto a registar neste procedimento.

faithful: s core: s notable: s clear: s

## L11 · caso c46 · língua pt

- **Descrição:** Aquisição de Serviços de Assistência Técnica aos equipamentos de emissão de radiação ionizante (RX Intraoral e RX Digital) e às cadeiras de estomatologia, com equipamentos de esterilização, localizados no Serviço de Estomatologia e nas Unidades de Cuidados de Saúde Primários e também aos CART localizados nos blocos operatórios do HESS e HNSA, da Unidade Local de Saúde Gaia Espinho, E.P.E. (ULSGE E.P.E.)
- **Adjudicante:** Unidade Local de Saúde de Gaia/Espinho, EPE [508142156]
- **Adjudicatário(s):** Serviço de Utilização Comum dos Hospitais [500900469]
- **Preço:** 11097.96 € (base: 11097.96) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c46

**Resumo:**

> A ULS Gaia/Espinho, E.P.E. contratou a aquisição de serviços de assistência técnica aos equipamentos de radiação ionizante (RX intraoral e RX digital), às cadeiras de estomatologia com equipamentos de esterilização e aos CART dos blocos operatórios do HESS e HNSA, por 11.097,96 euros, com execução prevista de 365 dias. O contrato foi adjudicado por contratação excluída II ao Serviço de Utilização Comum dos Hospitais, que foi também o único concorrente a apresentar proposta no procedimento.

faithful: s core: s notable: s clear: s

## L12 · caso c38 · língua pt

- **Descrição:** 26Y00190 - Aquisição de voo Porto/Montpellier/Porto, para trabalhador UC de 23 a 28/11/2026, para participação no curso 32nd EASD Scientists Training Course.
- **Adjudicante:** Universidade de Coimbra [501617582]
- **Adjudicatário(s):** SMILE - VIAGENS E TURISMO UNIPESSOAL LDA [506019608]
- **Preço:** 664.01 € (base: 664.01) · **Procedimento:** Ao abrigo de acordo-quadro (art.º 259.º)
- **Destaques calculados:** the contract was awarded under a framework agreement
- Dados completos: `cases.md`, secção c38

**Resumo:**

> A Universidade de Coimbra contratou a agência de viagens SMILE - VIAGENS E TURISMO UNIPESSOAL LDA para a aquisição de um voo Porto/Montpellier/Porto para um trabalhador, entre 23 e 28 de novembro de 2026, para participar no curso 32nd EASD Scientists Training Course. O contrato, no valor de 664,01 euros, foi adjudicado ao abrigo de um acordo-quadro (artigo 259.º do Código dos Contratos Públicos), ao abrigo do Acordo Quadro de Viagens e Alojamento.

faithful: s core: s notable: s clear: s

## L13 · caso c19 · língua pt

- **Descrição:** CP 39/2026 - Fornecimento Continuado de Blusão Softshell, Casaco e Calça Impermeável, dividido em 2 lotes
- **Adjudicante:** Serviços Intermunicipalizados de Águas e Resíduos dos Municípios de Loures e Odivelas [680009671]
- **Adjudicatário(s):** Partners Steatlh, Lda [510843018]
- **Preço:** 50000.0 € (base: 100000.0) · **Procedimento:** Concurso público
- **Destaques calculados:** 14 bidders took part in the procedure; the procedure was split into lots
- Dados completos: `cases.md`, secção c19

**Resumo:**

> Os Serviços Intermunicipalizados de Águas e Resíduos dos Municípios de Loures e Odivelas contrataram o fornecimento continuado de vestuário impermeável, neste caso casaco e calças impermeáveis, à empresa Partners Steatlh, Lda, por 50 000 euros (preço base de 100 000 euros), com um prazo de execução de 1096 dias. O contrato resultou de um concurso público dividido em lotes (o procedimento incluía também um lote de blusões softshell) e contou com a participação de 14 concorrentes.

faithful: s core: s notable: s clear: s

## L14 · caso c33 · língua pt

- **Descrição:** 050104292026 - C/ BASE NO CPA 2024_899
- **Adjudicante:** Unidade Local de Saúde de Coimbra, EPE [510103448]
- **Adjudicatário(s):** GLAXOSMITHKLINE-PROD. FARMACÊUTICOS, LDA. [500139962]
- **Preço:** 1706.34 € (base: 1706.34) · **Procedimento:** Ao abrigo de acordo-quadro (art.º 258.º)
- **Destaques calculados:** only one bidder took part in the procedure; the contract was awarded under a framework agreement; the procedure was split into lots
- Dados completos: `cases.md`, secção c33

**Resumo:**

> A Unidade Local de Saúde de Coimbra, EPE, adjudicou à GlaxoSmithKline – Produtos Farmacêuticos, Lda. a aquisição de produtos farmacêuticos, com um preço contratual de 1.706,34 euros, ao abrigo de um acordo-quadro (artigo 258.º do Código dos Contratos Públicos). O procedimento foi dividido em lotes, para os medicamentos salbutamol e fluticasona, e apenas um concorrente participou.

faithful: s core: s notable: s clear: s

## L15 · caso c16 · língua en

- **Descrição:** Procedimento Por Concurso Público Internacional para a realização do Lote 01: Atividade 02  From Making to  Market  Ação 02: Interrnational Roadshow  Scaling Up Brands  Desfiles e apresentações em Official Calendars  Paris Fashion Week  Woman  Setembro  2026 e 2027; e do Lote 02: Atividade 02  From Making to  Market  Ação 02: International Roadshow  Portugal Fashion Showroom - Startup and Scaleup International Business  Showroom Coletivo Paris - Man's Fashion Week 2027  2028
- **Adjudicante:** ANJE - Associação Nacional de Jovens Empresários [501775501]
- **Adjudicatário(s):** Montenegro Reis &amp; Coelho Silva [510892060]
- **Preço:** 287409.8 € (base: 287440.0) · **Procedimento:** Concurso público
- **Destaques calculados:** only one bidder took part in the procedure; the procedure was split into lots
- Dados completos: `cases.md`, secção c16

**Resumo:**

> This international public tender by ANJE – Associação Nacional de Jovens Empresários, a Portuguese business association, covers organising fashion show appearances and showroom presentations at Paris fashion weeks and related international roadshow activities, split into two lots for the 2026–2027 and 2027–2028 seasons. The contract was awarded to Montenegro Reis & Coelho Silva for 287,409.80 euros through a public tender, and only one bidder took part in the procedure. The contract also covers two lots, and the execution period is 547 days.

faithful: n core: s notable: s clear: n

## L16 · caso c49 · língua pt

- **Descrição:** Deposito de pedido de patente EPO e US da tecnologia Sensing Device
- **Adjudicante:** CENTITVC - Centro de Nanotecnologia e Materiais Técnicos, Funcionais e Inteligentes [507682734]
- **Adjudicatário(s):** Patentree, Unipessoal Lda [510638490]
- **Preço:** 7003.47 € (base: 7003.47) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c49

**Resumo:**

> O CENTITVC - Centro de Nanotecnologia e Materiais Técnicos, Funcionais e Inteligentes contratou à Patentree, Unipessoal Lda serviços de depósito de pedidos de patente junto do EPO e nos EUA para a tecnologia "Sensing Device", enquadrados como consultoria em direitos de autor e patentes. O contrato tem um preço de 7003,47 euros e foi celebrado através de um procedimento de contratação excluída, ao abrigo do artigo 3.º, n.º 1, do Decreto-Lei n.º 60/2018. Apenas um concorrente participou no procedimento.

faithful: s core: s notable: s clear: s

## L17 · caso c50 · língua pt

- **Descrição:** Aquisição de serviços de Aluguer de materiais de orquestra e direitos de execução da versão reduzida com arranjo de Daryl Griffith
- **Adjudicante:** OPART - Organismo de Produção Artística, EPE [508180457]
- **Adjudicatário(s):** Editions Mario Bois [712687513]
- **Preço:** 6685.0 € (base: 6685.0) · **Procedimento:** Contratação excluída II
- **Destaques calculados:** only one bidder took part in the procedure
- Dados completos: `cases.md`, secção c50

**Resumo:**

> O OPART - Organismo de Produção Artística, EPE contratou à Editions Mario Bois o aluguer de materiais de orquestra e os direitos de execução da versão reduzida com arranjo de Daryl Griffith, por 6685 euros. O contrato foi celebrado ao abrigo de um regime de contratação excluída das regras normais da contratação pública (artigo 6.º-A, n.º 1, do Código dos Contratos Públicos), com um prazo de execução de 16 dias em Lisboa. Apenas um concorrente participou no procedimento.

faithful: s core: s notable: s clear: s

## L18 · caso c25 · língua pt

- **Descrição:** AQUISIÇÃO DE SERVIÇOS, EM REGIME DE TAREFA, PARA ACOMPANHAMENTO E VIGILÂNCIA NOTURNA DA RESIDÊNCIA DE ESTUDANTES DE MURÇA
- **Adjudicante:** Município de Murça [506862763]
- **Adjudicatário(s):** (particular) [-]
- **Preço:** 4800.0 € (base: 8400.0) · **Procedimento:** Consulta Prévia
- **Destaques calculados:** only one bidder took part in the procedure; the procedure was split into lots; a contractor is a private individual (name removed for privacy)
- Dados completos: `cases.md`, secção c25

**Resumo:**

> A Câmara Municipal de Murça (Município de Murça) contratou, por consulta prévia, a aquisição de serviços em regime de tarefa para acompanhamento e vigilância noturna da Residência de Estudantes de Murça, no valor de 4.800,00 euros. O contrato foi adjudicado a um particular, cujo nome não consta do registo por motivos de privacidade. Ao procedimento concorreu apenas um concorrente, o procedimento foi dividido em lotes e o contrato foi celebrado com um particular.

faithful: s core: s notable: s clear: n

## L19 · caso c01 · língua pt

- **Descrição:** ADCM 1713/26  - NE 20651926
20650126
20652526
20647426
20650326
20647726
20649226
20652926
20649126
20648326
20651826
20649926
20650926
20647926
20649426
20653026
20650226
20653126
20650626
20652726
20647626
20650426
20648726
20653926
20648526
20648626
20650526
20652626
20651026
20649326
20647526
20648926
20652326
20652826
20651626
20653426
20652026
20649526
20649026
20648826
20653726
20648226
20649826
20651426
20653226
20648026
20649626
20651126
20651526
20653326
20650026
20647826
20650826
20652126
20648126
20651326
20649726
20652426
20648426
20650726
- **Adjudicante:** Instituto Português de Oncologia do Porto Francisco Gentil, EPE [506362299]
- **Adjudicatário(s):** (particular) [-]
- **Preço:** 3024.0 € (base: 90751.91) · **Procedimento:** Ajuste Direto Regime Geral
- **Destaques calculados:** the procedure was split into lots; a contractor is a private individual (name removed for privacy)
- Dados completos: `cases.md`, secção c01

**Resumo:**

> O Instituto Português de Oncologia do Porto Francisco Gentil, EPE adquiriu material de consumo clínico, com o código CPV 33000000-0 (equipamento médico, medicamentos e produtos para cuidados pessoais), através de um ajuste direto ao abrigo do regime geral, no valor de 3.024,00 euros. O contrato foi adjudicado a um particular, cujo nome foi omitido por motivos de privacidade, e o procedimento foi dividido em lotes. A descrição do contrato contém apenas números de referência, pelo que o objeto não está detalhado no registo.

faithful: s core: s notable: s clear: s

## L20 · caso c28 · língua en

- **Descrição:** CONCESSÃO DE EXPLORAÇÃO DA MESSE E DO BAR DO COMANDO TERRITORIAL DE VILA REAL
- **Adjudicante:** Guarda Nacional Republicana [600008878]
- **Adjudicatário(s):** Sopros Anunciados Unipessoal, Lda [519336283]
- **Preço:** 1440.0 € (base: 480.0) · **Procedimento:** Consulta Prévia
- **Destaques calculados:** 2 bidders took part in the procedure; the contract price is 200.0% above the procedure's base price
- Dados completos: `cases.md`, secção c28

**Resumo:**

> The Guarda Nacional Republicana contracted Sopros Anunciados Unipessoal, Lda for the concession to operate the mess and bar of its Vila Real Territorial Command, a hospitality and catering service lasting 364 days. The contract price is 1,440 euros and it was awarded through a prior consultation, a limited procedure where selected suppliers are invited to bid. Two bidders took part, one of them a private individual, and the contract price is 200% above the procedure's base price of 480 euros.

faithful: s core: s notable: s clear: s
