# Eval dos resumos por LLM

Estado a 29 out 2026. O código está em `evals/contract_summary/` e o resumidor em `src/summarize.py`.

## Desenho
- **Casos:** 50 contratos reais publicados desde jul/2026, estratificados por tipo de procedimento
  (`build_cases.py`, seed fixa; revistos e aprovados em `cases.md`). 38 casos são em PT e 12 em EN.
  Incluem casos difíceis: descrições só com códigos, preço 0 em acordo-quadro, consórcios, particulares e preços acima do base.
- **Graders:**
  - factos verificados em código (valores em euros e NIFs, tolerância de 1%);
  - um juiz Claude Sonnet 5.5 com 4 critérios sim/não: fiel, essencial, destaques, claro.
  
  **Pass = factos + fiel + essencial.**
- **Backends:**
  - API (números reais de custo);
  - `claude -p` com a subscrição (grátis, números indicativos). Os resultados de cada um ficam em pastas separadas.

## Resultados: juiz v1, via subscrição (`.claude/hillclimb/contract_summary_cc_judge1/`)

| | Haiku 5.5 (prompt v1) | Opus 5.5 (prompt v1) |
|---|---|---|
| Pass | 84% (±10 pp) | 96% (±5 pp) |
| Factos / Essencial / Destaques | 100% / 100% / 100% | 100% / 100% / 100% |
| Claro | 86% | 96% |
| Custo estimado por resumo (preços API) | **$0,0003** | **$0,013** |
| Latência mediana | 6,7 s | 6,9 s |

- O custo é uma estimativa a partir dos tokens medidos no `claude -p`. Antes de fixar o preço do evento `summary`, convém confirmá-lo com uma corrida na API.
- O Opus custa mais do que os $0,01 previstos por resumo, por isso só o Haiku é viável a esse preço.
- **Erros reais do Haiku com o prompt v1:**
  - chama "ajuste direto" a contratações excluídas e a contratos ao abrigo de acordo-quadro (c39, c42, c49);
  - escreve meta-texto sobre os destaques ("No notable points were flagged", "Notas:");
  - inventa períodos (c16).
- **Calibração do juiz v1:** as 20 etiquetas em `labels.md` foram atribuídas pelo **Claude Opus 5.5, não às cegas, não por uma pessoa**.
  - A concordância foi de 80% em *fiel* e 85% em *claro*; nos outros critérios foi de 100%.
  - As 7 discordâncias eram todas do juiz a ser mais estrito, quase sempre por não conhecer as regras do resumidor.
  - Para uma validação humana a sério, alguém tem de rever essas 7 discordâncias.

## Feito, mas ainda não medido
- **Juiz v2:** a rubrica passa a conhecer as regras do resumidor. O self-test passou: reprova os 3 resumos maus.
- **Prompt v2 do Haiku:** 5 regras novas, uma por cada categoria de erro acima. Atenção: as regras foram desenhadas a partir dos mesmos 50 casos, sem nenhum conjunto separado para validação. O ideal é confirmar com casos novos (`build_cases.py` com outra seed).

## Próximos passos (comandos)
São ~200 chamadas à subscrição. Convém corrê-los numa sessão com limite livre.

1. Reavaliar com o juiz v2 os resumos que já existem:
```bash
.venv/Scripts/python -m evals.contract_summary.run --backend claude-code --variant baseline --model claude-haiku-5-5 --reuse-from .claude/hillclimb/contract_summary_cc_judge1/baseline --concurrency 2
```
```bash
.venv/Scripts/python -m evals.contract_summary.run --backend claude-code --variant v1 --model claude-opus-5-5 --reuse-from .claude/hillclimb/contract_summary_cc_judge1/v1 --concurrency 2
```
2. Correr o prompt v2 do Haiku:
```bash
.venv/Scripts/python -m evals.contract_summary.run --backend claude-code --variant v2 --model claude-haiku-5-5 --concurrency 2
```
3. Gerar o relatório: `node <skill>/shared/evals/report/build-report-lite.mjs .claude/hillclimb/contract_summary_cc/`
4. Se o Haiku v2 se aproximar dos 96%, ligar os resumos no actor: um input `summaries`, o evento `summary` a $0,01, e uma corrida de confirmação na API para medir o custo real.
