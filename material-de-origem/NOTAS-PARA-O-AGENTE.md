# Notas para o agente

> Modelo. Preencha o que se aplicar, apague o resto, deixe o arquivo aqui.
>
> **Não escreva aqui o inventário do material.** Quem lê os arquivos e conclui
> o que cada um é, pelo título e pelo conteúdo, é o agente — e ele faz isso
> melhor do que você faria à mão. Este arquivo guarda só o que **nenhuma
> leitura recupera**.

## 1. O que NÃO usar

A parte mais importante daqui, e a única que o agente não tem como descobrir
sozinho. Documento superado continua parecendo válido para quem o lê pela
primeira vez: nada dentro do `relatorio.pdf` diz que o `relatorio-v2.pdf` o
substituiu, e nada no capítulo de ensaios avisa que aquela série não se
confirmou depois. Dado invalidado dentro de um pedido é exatamente a matéria
que não se sustenta no exame (art. 24 da LPI).

Liste o que está na pasta mas está fora:

- `<arquivo>` — superado por `<arquivo>`; use só o segundo.
- `<arquivo>` — rascunho, nunca revisado; ignore.
- `<seção, tabela ou ensaio>` de `<arquivo>` — resultado não se confirmou.
- ...

Se não houver nada nessa condição, escreva "nada" — também é informação útil.

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

- **Comece inventariando a pasta.** Leia todos os arquivos, `anterioridades/`
  inclusive, e devolva uma linha por documento: o que ele é e o que dele se
  aproveita. Confira contra a seção 1 acima e **espere minha confirmação**
  antes de começar a redigir. Documento lido errado contamina tudo o que vier
  depois; corrigir o inventário custa um minuto.
- **Não invente nenhum dado técnico.** Se faltar informação para uma seção,
  **pare e pergunte** em vez de preencher com valor plausível. Um número
  inventado num pedido de patente é matéria que não se sustenta no exame
  (art. 24 da LPI) e num documento que o depositante assina.
- **Não acrescente matéria que não esteja no material de origem.** O art. 32 da
  LPI, regulado pela Resolução INPI/PR nº 93/2013, fecha a porta para incluir
  matéria depois do requerimento de exame.
- **Anterioridade se cita em prosa, pelo número de publicação.** Nada de colar
  trecho de documento de `anterioridades/`.
- **Nunca crie, gere ou redesenhe uma imagem para `figuras/`** — nem copiando
  desenho de origem, nem com TikZ, nem por qualquer outro meio. Print de CAD
  vem com carimbo, logotipo e legenda — o art. 21 proíbe, e o art. 39, I exige
  figura isenta de texto, com apenas termos indicativos e sinais de
  referência. Falta o desenho de uma figura necessária? Diga o que ela
  precisa mostrar e peça que eu a traga — veja `figuras/LEIA-ME.md`.
- **Prefira faixa a valor fechado em grandeza numérica.** Medida, proporção,
  temperatura, tempo: valor fechado protege só aquele número exato, faixa
  protege toda a amplitude. Só vale quando o material sustentar a variação —
  se houver só um valor pontual, pergunte antes de arbitrar os extremos.
- **Ao terminar, entregue um mapa de proveniência**: qual documento desta pasta
  sustentou qual seção ou parágrafo do relatório. É o inventário da primeira
  regra fechando o círculo, e é o que me permite conferir sem reler tudo.
- **Rode `make verificar` e relate os avisos.**
