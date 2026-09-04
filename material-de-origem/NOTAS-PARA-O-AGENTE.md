# Notas para o agente

> Modelo. Preencha antes de pedir a um agente de IA que redija as peças, e
> apague o que não se aplicar. Como o material desta pasta não é classificado
> por seção, este arquivo é o mapa — é por ele que o agente começa.

## 1. O que é cada documento

| Arquivo | O que é | O que aproveitar |
| --- | --- | --- |
| `relatorio-final-projeto-XXX.pdf` | Relatório final do projeto | Descrição do objeto (cap. 3) e ensaios (cap. 5) |
| `anterioridades/BR-10-2015-XXXXXX.pdf` | Patente encontrada na busca | Só para citar em prosa, pelo número |
| | | |

Diga também o que **não** aproveitar: versão superada, rascunho, dado de ensaio
que não se confirmou. O agente não tem como adivinhar.

## 2. Decisões já tomadas

- **Natureza**: invenção | modelo de utilidade
- **Modalidade**: originário | adição | divisão | fase nacional PCT
- **Título pretendido**: ...
- **Categorias a reivindicar**: produto? processo? uso? (define o título — art. 25)
- **Há sequências biológicas?**: sim | não (se sim, veja a seção correspondente
  do `README.md`)

## 3. O que ainda está em aberto

Liste o que você sabe que falta. É mais barato o agente perguntar do que
inventar.

- ...

## 4. Regras para esta redação

Copie estas no seu prompt, ou aponte o agente para cá:

- **Não invente nenhum dado técnico.** Se faltar informação para uma seção,
  **pare e pergunte** em vez de preencher com valor plausível. Um número
  inventado num pedido de patente é matéria que não se sustenta no exame
  (art. 24 da LPI) e num documento que o depositante assina.
- **Não acrescente matéria que não esteja no material de origem.** O art. 32 da
  LPI, regulado pela Resolução INPI/PR nº 93/2013, fecha a porta para incluir
  matéria depois do requerimento de exame.
- **Anterioridade se cita em prosa, pelo número de publicação.** Nada de colar
  trecho de documento de `anterioridades/`.
- **Não copie desenho de origem para `figuras/`.** Print de CAD vem com carimbo,
  logotipo e legenda — o art. 21 proíbe, e o art. 39, I exige figura isenta de
  texto, com apenas termos indicativos e sinais de referência. Proponha o que
  cada figura precisa mostrar; a figura final é redesenhada.
- **Ao terminar, entregue um mapa de proveniência**: qual documento desta pasta
  sustentou qual seção ou parágrafo do relatório. É o que me permite conferir
  sem reler tudo.
- **Rode `make verificar` e relate os avisos.**
