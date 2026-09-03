# Plano de refatoração — de EmbrapaTex (ABNT) para template de pedido de patente (INPI)

Documento de planejamento. Descreve o que apagar, o que criar e o que reescrever
para que este repositório pare de gerar publicações da Embrapa em formato ABNT e
passe a gerar as peças do pedido de patente exigidas pelo INPI.

Base normativa lida integralmente em `Documentação do INPI/`:

| Documento | Situação | Papel no plano |
| --- | --- | --- |
| **Portaria/INPI/DIRPA nº 14, de 29/08/2024** | **vigente** | Norma central: forma e conteúdo do pedido. É a fonte de praticamente todas as regras deste plano. |
| Resolução INPI/PR nº 124/2013 (diretrizes de exame) | vigente | Orienta o *conteúdo* (suficiência descritiva, redação de reivindicações). Alimenta os comentários-guia dos arquivos. |
| Portaria INPI nº 39/2021 (fase nacional PCT) | vigente | Mesma forma documental da Portaria 14 (art. 65). Só acrescenta peças de requerimento. |
| Portaria INPI nº 79/2022 (trâmite prioritário) | vigente | Procedimental. **Não afeta** a forma dos documentos. |
| IN/INPI/PR nº 30/2013 e nº 31/2013 | **revogadas** (art. 66 da Portaria 14/2024) | Referência histórica. Não devem guiar o template. |
| Formulários oficiais e-Patentes 4.0 (8 `.docx`, PI e MU) | modelos oficiais | Fonte do texto-guia, da estrutura de seções e da tipografia de referência. |

---

## 1. Veredito

Não é um trabalho de renomeação. **A peça central do repositório atual — a
maquinaria ABNT/abnTeX2 — é incompatível com o pedido de patente, e em vários
pontos é expressamente proibida por norma.** O que sobrevive do EmbrapaTex é a
*engenharia* do repositório (Makefile, `.latexmkrc`, CI, `.gitignore`, o hábito
de separar orquestração / estilo / conteúdo e a rede de regressão), não o seu
conteúdo LaTeX.

Três incompatibilidades estruturais decidem o desenho novo:

1. **O pedido não é um documento — são quatro.** O art. 16 da Portaria 14/2024
   determina que relatório descritivo, reivindicações, desenhos e resumo sejam
   *documentos separados*, cada um com sequência de numeração independente e
   paginação no formato `1/3` centralizada na margem superior. No peticionamento
   eletrônico eles são anexados como arquivos distintos. Um `main.tex` que gera
   um `main.pdf` único **não serve** — o template tem de gerar quatro PDFs.
2. **Logotipo, capa e assinatura são proibidos.** O art. 21 veda "timbres,
   logotipos, letreiros, assinaturas ou rubricas, sinais ou indicações de
   qualquer natureza estranhos à matéria do pedido". Isso elimina de uma vez a
   capa com o logo da Embrapa, a folha de rosto, a folha de aprovação (assinada
   ou tipografada), a ficha catalográfica e o bloco de assinaturas do subtipo
   `probatorio`.
3. **Figura no texto é proibida.** O art. 19 não aceita representações gráficas
   no relatório descritivo, nas reivindicações ou no resumo — figuras existem
   *apenas* no documento de desenhos. Isso inverte a lógica do `\EMBRAPAfig`,
   que hoje espalha figuras pelo corpo do texto. Tabelas, fórmulas químicas e
   expressões matemáticas continuam permitidas no relatório e nas reivindicações
   (art. 20), em preto e com identificação sequencial.

Além disso, o pedido não tem sumário, lista de ilustrações, lista de tabelas,
lista de siglas, lista de símbolos, glossário, índice remissivo, errata,
dedicatória, agradecimentos, epígrafe, apêndices, anexos nem seção de
referências normalizada pela ABNT. O art. 3º lista exaustivamente o que compõe o
pedido: requerimento (formulário eletrônico), relatório descritivo,
reivindicações, desenhos (se houver), listagem de sequências (se houver), resumo
e comprovante de pagamento. Nada mais entra nos arquivos que anexamos.

---

## 2. O que a norma exige, item por item

Estas são as regras que o novo `lib/inpitex.sty` precisa implementar — cada uma
com o artigo que a impõe, para que a revisão do código seja verificável.

### 2.1 Comuns aos quatro documentos

| Regra | Artigo |
| --- | --- |
| Documentos separados, cada um com numeração independente | 16, I |
| Paginação `n/N` (página / total daquela parte), algarismos arábicos, **centralizada na margem superior** | 16, II |
| Corpo 12 (mín. 2,1 mm de altura), **entrelinha 1½**, justificado ou alinhado à esquerda, **entre 20 e 35 linhas por página**, em preto | 17 |
| Sem rasuras, emendas, timbres, logotipos, letreiros, assinaturas, rubricas ou indicações estranhas | 21 |
| Sem representações gráficas no relatório, nas reivindicações e no resumo | 19 |
| Tabelas, fórmulas químicas e expressões matemáticas em preto e identificadas sequencialmente | 20 |
| Unidades no SI; terminologia e símbolos uniformes em todo o pedido | 23 |
| Idioma português | 3º |

### 2.2 Título

Conciso, claro e específico; até 500 caracteres; sem denominação de fantasia; sem
fórmula química ou matemática; **idêntico no relatório descritivo e no resumo**
(art. 24). Deve representar as categorias de reivindicação (art. 25).

> Consequência de projeto: o título tem de ter **fonte única**, compartilhada
> pelos dois documentos. Duas cópias em arquivos diferentes é um defeito formal
> esperando para acontecer.

### 2.3 Relatório descritivo

Forma (art. 26):

- título **apenas na página inicial**, centralizado, separado do texto;
- **cada parágrafo numerado sequencialmente** em algarismos arábicos à esquerda
  do texto — a norma exemplifica `[003]`, `[015]`;
- listagem de todas as figuras do documento de desenhos.

Conteúdo, na ordem do art. 27 (I a IX) — que é exatamente a estrutura dos
formulários oficiais:

| Seção do formulário oficial (PI / MU) | Art. 27 |
| --- | --- |
| Campo da invenção / Campo do modelo de utilidade | I |
| Fundamentos da invenção / do modelo de utilidade | II, III, IV |
| Breve descrição dos desenhos | V (e 26, III) |
| Descrição da invenção / do modelo de utilidade | VI, VII |
| Exemplos de concretizações | VI |
| Aplicação industrial (quando não evidente) | VIII |

### 2.4 Reivindicações

Forma (arts. 18 e 28): cabeçalho "Reivindicações" centralizado no topo da
primeira página; cada reivindicação numerada consecutivamente em arábicos, com
**uma única** expressão "caracterizado por" e **sem interrupção por pontos**
(um único ponto final).

Conteúdo, e aqui **PI e MU divergem**:

- **Invenção** (arts. 29–31): quantas independentes forem necessárias, uma por
  categoria; dependentes agrupadas; estrutura *preâmbulo + "caracterizado por" +
  matéria pleiteada*.
- **Modelo de utilidade** (arts. 32–36): **uma única reivindicação
  independente** (art. 33), preferencialmente iniciada pelo título; dependentes
  só nas três hipóteses do art. 35; sinais de referência das figuras
  obrigatórios entre parênteses (art. 32, III).

### 2.5 Desenhos

- Documento composto **apenas por figuras**, várias por página, nitidamente
  separadas (art. 37).
- Margens da página: **superior entre 2,5 cm e 4 cm; esquerda e direita entre
  1,5 cm e 2,5 cm; inferior de pelo menos 1 cm** (art. 38, I).
- Figuras numeradas consecutivamente (art. 38, III).
- Figuras isentas de texto, admitidos apenas termos indicativos ("corte AA",
  "vapor d'água") e sinais de referência uniformes entre figuras (art. 39).
- **Obrigatório em modelo de utilidade** (art. 22).

### 2.6 Resumo

Cabeçalho "Resumo" centralizado no topo (art. 18); título do pedido
centralizado, separado do texto (art. 40, I); **50 a 200 palavras, não
excedendo uma página** (art. 40, II); um único parágrafo, sem menção ao mérito
da invenção (art. 41, IV).

### 2.7 Variantes do pedido

| Variante | Exigência de forma |
| --- | --- |
| Certificado de adição de invenção | No relatório, **após o título**: "certificado de adição de invenção do \_\_\_" (art. 43, II) |
| Pedido dividido | No relatório, **após o título**: "Dividido do \_\_\_" (art. 51, II) |
| Modificação após o depósito | Documento modificado sem sinalização + cópia de comparação com tachado/sublinhado (art. 57) |
| Folha de substituição com rearranjo | Numeração híbrida `4`, `4a`, `4b` com nota de rodapé "segue-se folha 4a" (art. 58) |
| Fase nacional PCT | Mesma forma documental (Portaria 39/2021, art. 9º, §1º, e art. 65 da Portaria 14) |

---

## 3. Decisões de arquitetura

Cinco decisões definem o trabalho. Em cada uma, a recomendação está marcada.

### D1. Quatro raízes LaTeX, quatro PDFs — **recomendado**

Cada parte é um arquivo raiz próprio na raiz do repositório
(`relatorio-descritivo.tex`, `reivindicacoes.tex`, `desenhos.tex`,
`resumo.tex`), compilado independentemente, cada um produzindo o PDF que será
anexado ao peticionamento. É o único desenho que satisfaz o art. 16 e o único
que espelha o que o INPI recebe.

Alternativa descartada: PDF único com quebras internas — não é anexável e viola
a numeração independente por parte.

### D2. Abandonar `abntex2` e o `embrapatex.sty`; novo `lib/inpitex.sty` sobre `article` — **recomendado**

O `abntex2` (sobre `memoir`) carrega capa, folha de rosto, `\textual`,
pré/pós-textuais, numeração romana, `\chapter` em caixa-alta, `\IBGEtab` —
tudo inútil ou proibido aqui, e cada um deles é uma fonte de atrito (vide a
armadilha do `\savebox` do `\IBGEtab` documentada no `CLAUDE.md`). O pedido de
patente é tipograficamente **simples**: uma coluna, sem capítulos, sem sumário.

Base enxuta proposta:

```latex
\documentclass[a4paper,12pt]{article}
\usepackage[T1]{fontenc} \usepackage[utf8]{inputenc}
\usepackage[brazilian]{babel}
\usepackage{geometry}   % margens + travamento do nº de linhas por página
\usepackage{setspace}   % entrelinha 1,5
\usepackage{fancyhdr}   % paginação n/N centralizada no topo
\usepackage{lastpage}   % total de páginas da parte
\usepackage{graphicx}   % só no documento de desenhos
\usepackage{amsmath}    % expressões matemáticas (art. 20)
\usepackage{booktabs,longtable} % tabelas (art. 20)
```

Fonte: os formulários oficiais usam **Arial 12 pt** no corpo, 14 pt nos títulos
de seção e 16 pt no título do pedido, entrelinha 1,5. O `mathptmx` (Times) do
template atual deve sair; a norma só exige altura mínima de caractere, então
adotar uma sans-serif próxima do oficial (`helvet` com `\renewcommand
{\familydefault}{\sfdefault}`) alinha o resultado ao formulário do INPI.

### D3. Metadados em fonte única, e o que **não** se imprime — **recomendado**

Um `dados-do-pedido.tex` na raiz, lido pelas quatro raízes, com:

- `\titulodopedido{...}` — usado pelo relatório e pelo resumo (art. 24, IV);
- `\natureza{invencao|modelo-de-utilidade}` — chaveia títulos de seção e
  esqueleto de reivindicações;
- `\vinculo{adicao|divisao}{<número do pedido>}` — imprime a menção pós-título
  dos arts. 43, II e 51, II; vazio para pedido comum.

E um bloco explicitamente **não impresso** com depositante, inventores,
procurador, prioridades e código de serviço da GRU. Esses dados vão no
*formulário eletrônico de requerimento*, não nos arquivos anexados — imprimi-los
violaria o art. 21. Mantê-los ali, comentados e rotulados, dá ao redator um
lugar único para os dados do depósito sem risco de vazarem para o PDF.

### D4. PI e MU no mesmo template, via `\natureza` — **recomendado**

As duas naturezas compartilham a forma (arts. 16 a 28) e divergem no conteúdo
das reivindicações (arts. 29–31 vs. 32–36), no vocabulário das seções
("invenção" vs. "modelo de utilidade") e na obrigatoriedade dos desenhos
(art. 22). Um seletor cobre isso sem duplicar o repositório — mesmo padrão que o
`\tipodocumento` cumpre hoje, aplicado a um eixo real da norma.

### D5. Declaração única das figuras — **recomendado**

O art. 26, III exige que o relatório liste todas as figuras, e o art. 39, V pede
que a ordem das figuras siga o relatório. Manter as duas listas à mão é convite
a divergência. Proposta: um `pedido/desenhos/figuras.tex` com uma entrada por
figura —

```latex
\figura{esquema-do-conjunto}{a vista frontal do conjunto montado}
\figura{corte-aa}{o corte AA do elemento de fixação (12)}
```

— consumido **duas vezes**: no relatório descritivo, para gerar a seção "Breve
descrição dos desenhos" ("A Figura 1 apresenta a vista frontal…"), e em
`desenhos.tex`, para posicionar as imagens rotuladas "Figura 1", "Figura 2".
Numeração e ordem passam a ser consistentes por construção.

---

## 4. Estrutura proposta do repositório

```
.
├── dados-do-pedido.tex              # metadados únicos (título, natureza, vínculo)
├── relatorio-descritivo.tex         # raiz → relatorio-descritivo.pdf
├── reivindicacoes.tex               # raiz → reivindicacoes.pdf
├── desenhos.tex                     # raiz → desenhos.pdf
├── resumo.tex                       # raiz → resumo.pdf
├── lib/
│   └── inpitex.sty                  # todo o estilo e as macros do pedido
├── pedido/
│   ├── relatorio-descritivo/
│   │   ├── 1-campo-tecnico.tex
│   │   ├── 2-fundamentos.tex
│   │   ├── 3-descricao.tex
│   │   ├── 4-concretizacoes.tex
│   │   └── 5-aplicacao-industrial.tex
│   ├── reivindicacoes/
│   │   └── reivindicacoes.tex
│   ├── desenhos/
│   │   └── figuras.tex              # declaração única (D5)
│   └── resumo/
│       └── resumo.tex
├── figuras/                         # imagens, consumidas só por desenhos.tex
├── referencias-inpi/                # ex-"Documentação do INPI" (só leitura)
│   ├── formularios-oficiais/{invencao,modelo-de-utilidade}/
│   └── normas/                      # com IN30/IN31 marcadas como revogadas
├── verificar-conformidade.sh        # rede de regressão normativa
├── gerar-exemplo-mu.sh              # showcase da natureza modelo de utilidade
├── Makefile · .latexmkrc · .gitignore · .vscode/settings.json
├── .github/workflows/compilar-latex.yml
├── CLAUDE.md · README.md · LICENSE
```

A seção "Breve descrição dos desenhos" não tem arquivo próprio: é gerada da
declaração de figuras (D5), inserida pela macro na posição do art. 27, V.

Renomear `Documentação do INPI/` → `referencias-inpi/` remove espaços e acentos
do caminho (hoje há até divergência entre `Formularios` e `Formulários`) e segue
o kebab-case que o repositório já adota para arquivos.

---

## 5. Mapa de ações

### 5.1 Apagar

| Caminho | Motivo |
| --- | --- |
| `main.tex` | Substituído por quatro raízes (D1) |
| `lib/embrapatex.sty` | 1.818 linhas de maquinaria ABNT; nada aproveitável estruturalmente |
| `lib/preambulo.tex` | Preâmbulo `abntex2` + biblatex + glossaries + algorithm2e; substituído pelo `inpitex.sty` |
| `lib/logo-embrapa-*.png` (3 arquivos) | Logotipo proibido no pedido (art. 21) |
| `elementos-pre-textuais/` (todo) | Capa, ficha, errata, dedicatória, agradecimentos, epígrafe, resumo/abstract ABNT, sumário executivo, listas de siglas e símbolos, `folha-aprovacao.pdf` — nenhum existe no pedido (arts. 3º e 21) |
| `elementos-textuais/` (todo) | Capítulos ABNT (introdução, revisão de literatura, metodologia…); o relatório descritivo tem outra estrutura, fixada pelo art. 27 |
| `elementos-pos-textuais/` (todo) | Referências, glossário, apêndices, anexos — não integram o pedido |
| `exemplo-academico.tex`, `exemplo-publicacao.tex`, `exemplo-corporativo.tex`, `exemplo-probatorio.tex` | Showcase dos tipos Embrapa |
| `gerar-exemplos.sh` | Idem; substituído por `gerar-exemplo-mu.sh` |
| `verificar-ocultamento.sh` | Testa a "exibição automática de elementos opcionais", conceito que morre com os pré-textuais |
| `figuras/exemplo_imagem.jpg` | Substituída por uma figura-exemplo condizente com um desenho de patente |

Some com isso todo o vocabulário `\EMBRAPAfig` / `\EMBRAPAtab` / `\EMBRAPAqua` /
`\EMBRAPAtablonga`, o ambiente `quadro`, os `alineas`/`subalineas`, os teoremas,
os algoritmos (`algorithm2e`), os `lstlisting`, as citações `\cite`/`\citeonline`
e o `biblatex-abnt`. O estado da técnica em um pedido de patente é citado em
prosa numerada, dentro dos parágrafos `[00N]` (art. 27, II; R124/2013, itens
2.03–2.05 e 2.40–2.46) — não há lista de referências ABNT no pedido.

### 5.2 Criar

| Caminho | Conteúdo |
| --- | --- |
| `lib/inpitex.sty` | Todo o estilo e as macros (§6) |
| `dados-do-pedido.tex` | Metadados únicos + bloco não impresso (D3) |
| `relatorio-descritivo.tex` | Orquestra título, menção de vínculo, seções do art. 27 e a lista de figuras |
| `reivindicacoes.tex` | Cabeçalho "Reivindicações" + `\input` do quadro |
| `desenhos.tex` | Geometria do art. 38 + varredura da declaração de figuras |
| `resumo.tex` | Cabeçalho "Resumo" + título + parágrafo único |
| `pedido/**` | Arquivos de conteúdo com o texto-guia dos formulários oficiais em comentários PT-BR |
| `verificar-conformidade.sh` | Rede de regressão normativa (§7) |
| `gerar-exemplo-mu.sh` | Gera os quatro PDFs na natureza MU, para validar o seletor `\natureza` |

### 5.3 Reescrever

| Caminho | Mudança |
| --- | --- |
| `README.md` | Reescrita completa: como preencher cada uma das quatro peças, o que a norma exige, como anexar no peticionamento. Sai todo o "como inserir quadro/algoritmo/alínea/ficha catalográfica" |
| `CLAUDE.md` | Reescrita completa. As 27 KB atuais descrevem tipos de documento, exibição automática de elementos, ficha catalográfica e verificação da lista de símbolos — tudo inexistente no template novo, e ativamente enganoso se ficar |
| `Makefile` | Alvos `pdf` (os quatro), `relatorio`/`reivindicacoes`/`desenhos`/`resumo` (individuais), `verificar`, `lint`, `limpar`, `exemplo-mu` |
| `.latexmkrc` | Remover as dependências `.glo→.gls` e `.acn→.acr` (não há mais glossário); manter só o que as quatro raízes precisam |
| `.gitignore` | Trocar `/main.pdf` e `/exemplo-*.pdf` pelos quatro PDFs gerados; remover as extensões de glossário, índice, biblatex e listas |
| `.vscode/settings.json` | Remover `rootFile` fixo e as ferramentas `biber`/`makeglossaries`/`makeindex`; recipes para as quatro raízes |
| `.github/workflows/compilar-latex.yml` | Compilar as quatro raízes, publicar os quatro PDFs como um artefato, rodar `verificar-conformidade.sh` como passo bloqueante, atualizar a guarda `github.repository` para o nome novo do repositório (hoje aponta para `embrapa-template-documentos-latex-abnt`) |
| Cabeçalhos LPPL dos arquivos novos | Trocar a atribuição "Customizações do abnTeX2 … para a Embrapa" pela identificação do template INPI; manter a LPPL e o mantenedor |

### 5.4 Manter como está

`LICENSE` (LPPL 1.3c), o diretório `figuras/` (esvaziado) e os arquivos de
referência do INPI, apenas movidos e renomeados.

---

## 6. Especificação do `lib/inpitex.sty`

Cada macro abaixo existe para cumprir um artigo. É a lista de verificação da
revisão de código.

**Layout e paginação**

- Geometria A4 com margens de 2,5 cm e `lines=30` no `geometry`, travando a
  caixa de texto em 30 linhas por página — dentro da faixa de 20 a 35 do
  art. 17, com folga nas duas pontas.
- `\onehalfspacing` (entrelinha 1½, art. 17) e corpo 12 pt.
- `\fancyhead[C]{\thepage/\pageref{LastPage}}`, cabeçalho sem filete, para a
  paginação `n/N` centralizada na margem superior (art. 16, II). Como cada parte
  é um PDF próprio, o `lastpage` dá o total daquela parte, e a numeração
  recomeça em 1 naturalmente (art. 16, I).
- `\pagestyle` sem rodapé, sem qualquer marca — art. 21.

**Metadados**

- `\titulodopedido{}`, `\natureza{}`, `\vinculo{}{}` — fonte única (D3).
- `\natureza` define o booleano interno consumido pelas macros de seção e pelo
  esqueleto de reivindicações (D4), e emite `\PackageError` para valor
  desconhecido — mesma ruptura limpa que o `\tipodocumento` adotou.

**Relatório descritivo**

- `\imprimirtitulodopedido` — título centralizado, separado do texto, **apenas
  na página inicial** (art. 26, I), seguido da menção de vínculo quando houver
  (arts. 43, II e 51, II).
- `\pnum` — abre parágrafo numerado. Incrementa o contador, imprime o rótulo
  `[001]` à esquerda com recuo pendente de 0,63 cm (o `w:hanging="357"` dos
  formulários oficiais) e segue com o texto (art. 26, II). Sem argumento: o
  redator escreve `\pnum` e o parágrafo em seguida, de modo que tabelas e
  fórmulas possam ser intercaladas sem quebrar ambiente de lista.
- `\formatorotuloparagrafo` — padrão em três dígitos (`[003]`, como a norma
  exemplifica), trocável para arábico simples.
- `\secaoINPI{...}` — título de seção do art. 27 em negrito, 14 pt, sem
  numeração de capítulo (não existe `\chapter` aqui).
- `\INPItab{<legenda>}{<tabular>}` — tabela com legenda **acima**, rotulada
  "Tabela N - …", numeração sequencial, tudo em preto (art. 20); segue o
  formulário oficial. Sem linha "Fonte:" (elemento ABNT, dispensável aqui).
- `\imprimirdescricaodosdesenhos` — gera a seção "Breve descrição dos
  desenhos" a partir da declaração de figuras (D5), cumprindo os arts. 26, III
  e 27, V.

**Reivindicações**

- `\imprimircabecalhoreivindicacoes` — "Reivindicações" centralizado no topo da
  primeira página (art. 18).
- Ambiente `reivindicacoes` com `\reivindicacao` — numeração consecutiva em
  arábicos (art. 28, I) e recuo pendente coerente com o formulário.
- Comentários-guia distintos por natureza: para MU, o alerta de reivindicação
  independente **única** (art. 33) e das três hipóteses de dependente (art. 35);
  para PI, o agrupamento por categoria (art. 30, VII).

**Desenhos**

- Geometria própria: superior 3 cm, esquerda/direita 2 cm, inferior 2 cm — dentro
  das faixas do art. 38, I.
- `\imprimirdesenhos` — percorre a declaração de figuras, uma ou mais por
  página, centralizadas, cada uma com o rótulo "Figura N" centralizado abaixo,
  numeração consecutiva (art. 38, III), nitidamente separadas (art. 37).

**Resumo**

- `\imprimirresumo` — "Resumo" centralizado no topo (art. 18), título do pedido
  centralizado e separado (art. 40, I), parágrafo único.
- Aviso na compilação se a contagem de palavras sair da faixa de 50 a 200
  (art. 40, II) — a checagem dura fica no script (§7).

---

## 7. Rede de conformidade (`verificar-conformidade.sh`)

O `verificar-ocultamento.sh` atual afirma que elementos opcionais aparecem ou
somem conforme o esperado. O conceito continua valendo — trocar o objeto de
verificação. O script novo compila as quatro raízes com `-halt-on-error` e
**afirma conformidade normativa** sobre os PDFs gerados, com `pdftotext` e
`pdfimages` (o `poppler-utils` já é instalado pela CI):

| Afirmação | Artigo |
| --- | --- |
| Cada PDF traz `n/N` no topo de cada página, com `N` igual ao total daquele PDF, recomeçando em 1 | 16 |
| Nenhuma página passa de 35 linhas nem fica abaixo de 20 | 17 |
| `pdfimages -list` retorna zero imagens no relatório, nas reivindicações e no resumo | 19 e 21 |
| O título extraído do relatório é idêntico ao extraído do resumo | 24, IV |
| Título com até 500 caracteres, sem `$`, `\ce` ou dígito de fórmula | 24, I e III |
| Parágrafos do relatório numerados de `[001]` em diante, sem lacuna nem repetição | 26, II |
| Toda figura declarada aparece na listagem do relatório **e** no documento de desenhos | 26, III e 39, V |
| Cada reivindicação tem exatamente uma expressão "caracterizado(a) por" e um único ponto final | 28, II e III |
| Em MU, exatamente uma reivindicação independente | 33 |
| Em MU, o documento de desenhos existe e não está vazio | 22 |
| Resumo com 50 a 200 palavras e uma única página | 40, II |

`--check-only` (usado pela CI) mantém o comportamento atual de pular a
compilação e checar os artefatos existentes.

Vale acrescentar o inverso do aviso que hoje existe para a lista de símbolos:
**sinal de referência citado no relatório ou nas reivindicações que não apareça
em nenhuma figura declarada** — e vice-versa (arts. 29, VIII, 32, III; R124/2013,
itens 4.01 e 2.27–2.29). É o mesmo tipo de congruência bidirecional que o
`CLAUDE.md` já pede hoje para os símbolos, aplicada ao que a norma cobra.

---

## 8. Ordem de execução

Sete commits, cada um deixando o repositório em estado compilável ao final:

1. **Fundação** — `lib/inpitex.sty` (layout, paginação `n/N`, metadados,
   `\pnum`) e `dados-do-pedido.tex`. Nada ainda foi apagado.
2. **As quatro raízes** — `relatorio-descritivo.tex`, `reivindicacoes.tex`,
   `desenhos.tex`, `resumo.tex` e a árvore `pedido/`, preenchidos com o
   texto-guia dos formulários oficiais (natureza `invencao`). Neste ponto o
   repositório já gera os quatro PDFs válidos.
3. **Natureza MU** — seletor `\natureza`, variação de vocabulário e do esqueleto
   de reivindicações, `gerar-exemplo-mu.sh`.
4. **Remoção** — apagar tudo do §5.1 de uma vez. É aqui que o `abntex2` sai.
5. **Infraestrutura** — Makefile, `.latexmkrc`, `.gitignore`, `.vscode`, CI (com
   a guarda `github.repository` corrigida).
6. **Conformidade** — `verificar-conformidade.sh` e sua entrada na CI como passo
   bloqueante.
7. **Documentação** — `README.md` e `CLAUDE.md` reescritos; mover e renomear
   `Documentação do INPI/` → `referencias-inpi/`, marcando IN30/IN31 como
   revogadas.

Colocar a remoção depois da construção (4 depois de 2 e 3) permite comparar o
resultado novo com o antigo enquanto se trabalha, e evita um intervalo em que o
repositório não compila.

---

## 9. Fora de escopo

- **Listagem de sequências biológicas** (art. 3º, V; R124/2013, item 2.19). Segue
  norma própria e o padrão WIPO ST.26, gerado por ferramenta específica
  (WIPO Sequence), não por LaTeX. O template deve apenas mencionar onde ela
  entra.
- **Formulário eletrônico de requerimento, GRU e procuração** (arts. 4º, 7º e
  59). São atos no sistema de peticionamento, não documentos que o template
  produza.
- **Cópia de comparação com tachado/sublinhado** (arts. 51, III e 57, II). Útil
  para petições de modificação; proponho deixar para uma fase posterior, com um
  `\usepackage{ulem}` e macros `\incluido`/`\removido`, depois que o núcleo
  estiver estável.
- **Outros direitos de propriedade intelectual.** A pasta fornecida cobre
  exclusivamente patentes (invenção e modelo de utilidade). Marca, desenho
  industrial, programa de computador e cultivar têm formulários e normas
  próprias e ficam de fora — vale registrar isso no README, já que o nome do
  repositório ("propriedade intelectual") é mais amplo do que o escopo real.

---

## 10. Pontos que precisam da sua confirmação

1. **Idioma do código.** Sua preferência geral é escrever código e comentários
   em inglês; o `CLAUDE.md` deste repositório determina PT-BR para todo texto,
   comentário e argumento de comando, e as 1.800 linhas atuais seguem isso.
   O plano assume **PT-BR** (`\pnum`, `\titulodopedido`, `\reivindicacao`), por
   coerência com o domínio — o documento gerado é uma peça jurídica em português
   e os nomes das macros espelham a norma. Diga se prefere que eu inverta para
   inglês na reescrita.
2. **Fonte.** Adotar sans-serif (Arial/Helvetica), como os formulários oficiais
   do e-Patentes, ou manter serif? A norma só exige altura mínima de caractere;
   a semelhança com o formulário oficial é o argumento a favor da sans.
3. **Escopo de natureza.** Cobrir PI **e** MU desde já (D4), ou começar só por
   PI, que é o seu caso mais frequente, e acrescentar MU depois?
4. **Histórico do repositório.** O repositório tem dois commits ("Initial
   commit" e "adicionar documentação do inpi"), então não há paridade com o
   Overleaf a preservar — a diretriz do `CLAUDE.md` de "preferir mudanças
   aditivas a mover arquivos" perde a razão de ser e o plano a descarta. Confirme
   se concorda.
