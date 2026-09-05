# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

## Projeto

Template LaTeX para redigir as peças de um **pedido de patente** junto ao **INPI** (Instituto Nacional da Propriedade Industrial), na forma exigida pela **Portaria/INPI/DIRPA nº 14, de 29 de agosto de 2024**. Todo o conteúdo é em **português (PT-BR)** — inclusive nomes de macro, comentários e mensagens de erro: o documento gerado é peça jurídica em português e as macros espelham o vocabulário da norma.

**Convenção de citação:** quando este arquivo, o `README.md` ou um comentário de código citam um artigo sem indicar a norma, trata-se da Portaria/INPI/DIRPA nº 14/2024. "LPI" é a Lei nº 9.279/1996. As normas estão em `referencias-inpi/normas/`, e **só há norma em vigor ali**: quando uma norma é revogada ou superada, ela sai do repositório em vez de ficar guardada com ressalva. Se você encontrar orientação que se apoie em norma que não está nessa pasta, desconfie e confira contra a Portaria 14/2024 antes de aplicar.

**O repositório gera QUATRO PDFs, não um.** O art. 16 exige que relatório descritivo, reivindicações, desenhos e resumo sejam documentos separados, cada um com numeração de páginas independente e paginação `n/N` centralizada na margem superior. São, portanto, quatro raízes LaTeX independentes na raiz do repositório, e são exatamente os arquivos anexados no Peticionamento Eletrônico. Não existe `main.tex`.

O template **verifica forma, não mérito**. Nada aqui avalia novidade, atividade inventiva ou suficiência descritiva (arts. 8º, 11, 13, 24 e 25 da LPI).

## Origem: o que este repositório NÃO é mais

Este repositório é uma cópia do `embrapa-template-documentos-latex-abnt` (template ABNT/abnTeX2 para publicações da Embrapa), refatorado para o INPI. **Nada da maquinaria ABNT sobreviveu**, e é importante não reintroduzi-la: em vários pontos ela é expressamente proibida pela norma.

- **Art. 21** veda "timbres, logotipos, letreiros, assinaturas ou rubricas, sinais ou indicações de qualquer natureza estranhos à matéria do pedido" → não há capa, folha de rosto, folha de aprovação, logotipo, assinatura nem ficha catalográfica.
- **Art. 19** não aceita representações gráficas no relatório descritivo, nas reivindicações ou no resumo → figuras existem **apenas** no documento de desenhos. É o inverso do antigo `\EMBRAPAfig`.
- **Art. 3º** lista exaustivamente o que compõe o pedido → não há sumário, listas de ilustrações/tabelas/quadros/algoritmos/códigos, lista de siglas, lista de símbolos, glossário, índice remissivo, errata, dedicatória, agradecimentos, epígrafe, apêndices, anexos nem seção de referências ABNT.

Foram-se com isso: `abntex2`, `biblatex-abnt`/`biber`, `glossaries`, `makeindex`, `algorithm2e`, `listings`, `pdfpages`, os encapsuladores `\EMBRAPAfig`/`\EMBRAPAtab`/`\EMBRAPAqua`/`\EMBRAPAtablonga`, o ambiente `quadro`, os `alineas`/`subalineas`, os teoremas, as citações `\cite`/`\citeonline`, a macro `\textual` e todo o mecanismo de "exibição automática de elementos opcionais". **Não use nem cite nada disso.** O estado da técnica é citado em prosa, dentro dos parágrafos numerados (art. 27, II), pelo número de publicação do documento.

## Compilação

Cada peça é uma raiz independente. São necessárias **duas passadas** de `pdflatex` — a paginação `n/N` depende do `\pageref{LastPage}` do pacote `lastpage`, que só estabiliza na segunda:

```sh
# Recomendado — compila as quatro peças:
make pdf

# Uma peça só:
latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error relatorio-descritivo.tex

# Sem latexmk (duas passadas obrigatórias):
pdflatex relatorio-descritivo.tex
pdflatex relatorio-descritivo.tex
```

Sempre use **`-halt-on-error`**. Sob `nonstopmode` sem ele, um erro grave é **silencioso**: o LaTeX "se recupera" e ainda entrega um PDF. Todos os alvos do `Makefile`, o `gerar-exemplos.sh` e o `verificar-conformidade.sh` já o passam.

**Atalhos (`Makefile`)** — `make` (= `make pdf`) compila as quatro peças; `make relatorio`/`reivindicacoes`/`desenhos`/`resumo` compilam uma só; `make verificar` roda a rede de conformidade; `make lint` roda o chktex; `make exemplos` roda o showcase; `make comparacao` gera a cópia de comparação; `make limpar` remove artefatos; `make ajuda` lista os alvos.

Os alvos de PDF dependem de `FORCE` de propósito: **quem decide se recompila é o `latexmk`, não o `make`**. Não substitua isso por uma lista de dependências escrita à mão. O texto do pedido mora em `pedido/**` e as imagens em `figuras/**`, e uma lista assim esquece os dois — foi o que fazia `make pdf` responder "Nothing to be done" depois de editar o relatório, deixando anexar ao peticionamento o PDF da versão anterior. O `latexmk` rastreia dependência pelo `.fls`, que enxerga todo `\input` e todo `\includegraphics`, inclusive os que aparecerem depois.

**Showcase** — `./gerar-exemplos.sh` gera as quatro peças para cada combinação relevante dos dois eixos de seleção (`exemplo-invencao-*`, `exemplo-mu-*`, `exemplo-divisao-*`), injetando os valores por `-pretex` sobre os `\providecommand` de `dados-do-pedido.tex`. **Nenhum arquivo de conteúdo é duplicado.** Existe para provar que os seletores realmente chaveiam o que deveriam; é comando de mantenedor do template, não do fluxo de escrita de um pedido.

**Cópia de comparação** — `./gerar-copia-de-comparacao.sh` (ou `make comparacao`) gera os `*-comparacao.pdf` dos arts. 51, III e 57, II. O ponto de projeto é que **a mesma fonte gera as duas saídas** exigidas pelo art. 57: `\removido` some por completo no documento do pedido e sai tachado na cópia; `\incluido` sai limpo lá e sublinhado aqui. `\paragraforemovido` e `\reivindicacaoremovida` **não incrementam contador** no documento do pedido, para que a numeração dos arts. 26, II e 28, I siga contínua depois da supressão. Na cópia de comparação o rótulo delas sai **entre colchetes** (`[–]`, `[6]`), e isso é necessário: impresso como `6.`, o número antigo se confunde com a numeração viva do quadro, e suprimir a reivindicação 2 de um quadro de quatro produzia dois itens numerados "2.". O modo é injetado por linha de comando, e o `verificar-conformidade.sh` **aborta** se `\CopiaDeComparacao{sim}` ficar em `dados-do-pedido.tex` — seria o erro mais caro que o template permitiria, porque os PDFs do pedido sairiam marcados contra o art. 57, I sem nada parecer errado.

**Rede de conformidade** — `./verificar-conformidade.sh` compila as quatro peças e **afirma** sobre os PDFs cada exigência de forma verificável automaticamente (arts. 16, 17, 19, 21, 22, 24, 26, 28, 33, 38, 39, 40 e 57), citando o artigo em cada afirmação. `--check-only` pula a compilação e verifica os PDFs atuais (é assim que a CI o roda). Emite ainda **avisos não-bloqueantes** sobre os sinais de referência, cruzando o texto, a frase de cada figura e o glossário `figuras/sinais-de-referencia.md` — o script não vê o interior das imagens, e quem sabe em que figura cada sinal está desenhado é o glossário.

Ele também lê os `.log` e **falha** em transbordamento de caixa. Isso não é preciosismo tipográfico: o LaTeX trata transbordamento como aviso, o `-halt-on-error` não pega e o build "termina com sucesso", mas um `Overfull \vbox` significa matéria empurrada para fora da página — uma tabela alta demais perde as linhas excedentes, que deixam de existir no PDF anexado ao peticionamento. `Overfull \hbox` acima de 2 pt é tinta impressa por cima da margem, e também falha.

Quatro detalhes de implementação do script que **não devem ser desfeitos**:

- ele gera **dois arquivos de texto por peça**: a extração fiel do `pdftotext` (para contar linhas e conferir a paginação) e uma versão **des-hifenizada** (para as buscas textuais). O `pdftotext` preserva a hifenização de fim de linha do LaTeX (`compre- endendo`), o que fura qualquer busca por expressão — era o que fazia a contagem de "caracterizado por" passar batida. Des-hifenizar junta linhas, então um arquivo só não serve para as duas coisas;
- a checagem do art. 19 procura o comando gráfico **na fonte**, não só no PDF. O `pdfimages` lista apenas imagens rasterizadas e **não vê desenho vetorial** — justamente o formato das figuras deste template. A checagem de PDF ficou como complemento;
- o limite de 500 caracteres do título (art. 24, I) é contado **na fonte**, em `dados-do-pedido.tex`, e não no texto extraído do PDF. A comparação de identidade do art. 24, IV precisa remover todos os espaços (o `pdftotext` inventa espaço de kerning: "VÁL VULA"), e essa mesma string não serve para contar — um título de 505 caracteres passava como 439. Some-se que `wc -m` sem locale UTF-8 conta bytes, e cada acento valeria dois;
- comparação de conjunto de sinais se faz em Python, com `set()`, **nunca** com `sort -un` alimentando `comm`. O `sort -un` ordena por valor (2, 9, 10) e o `comm` compara por texto (10 < 2): basta um sinal de dois dígitos, que é o caso normal num pedido real, para o `comm` desalinhar, reportar como ausente um sinal presente nos dois lados e despejar "comm: input is not in sorted order" no meio do relatório.

**Rigor calibrado à norma:** a faixa de 50 a 200 palavras do resumo é **aviso**, não falha, porque o art. 40, II diz "conter *preferencialmente* entre 50 e 200 palavras, e não exceder uma página" — só o limite de página é imperativo. Ao acrescentar checagens, distinga o que a norma impõe do que ela prefere.

Há **CI** (GitHub Actions): o workflow `.github/workflows/compilar-latex.yml`, a cada Pull Request e push na `main`, (a) roda o chktex como **lint advisory** (não bloqueia), (b) compila as quatro raízes numa imagem TeX Live completa e publica os PDFs no artefato `pedido-de-patente-pdf`, (c) roda `verificar-conformidade.sh --check-only` como passo **bloqueante** e (d) gera o showcase, publicando-o como artefato `exemplos-pdf`. O passo (d) é **só-do-template** (guarda `if: github.repository == '<repo do template>'`) e é pulado em pedidos derivados. O passo (c) **não** é só-do-template: verifica a norma, não o conteúdo-exemplo, e por isso vale também para pedidos reais. O `.gitignore` cobre os artefatos de compilação e os quatro PDFs gerados; as figuras em PDF de `figuras/` são fonte e continuam versionadas.

## Arquitetura

```
dados-do-pedido.tex          metadados únicos (título, natureza, modalidade)
relatorio-descritivo.tex     ─┐
reivindicacoes.tex            │ as quatro raízes: só orquestração
desenhos.tex                  │
resumo.tex                   ─┘
lib/inpitex.sty              todo o estilo e as macros
pedido/                      o conteúdo redigido
figuras/                     imagens prontas, consumidas só por desenhos.tex
material-de-origem/          material do inventor (não versionado)
referencias-inpi/            normas e formulários oficiais (só leitura)
```

- **As quatro raízes** — apenas orquestração: `\documentclass`, `\usepackage{lib/inpitex}`, `\input{dados-do-pedido}` e as chamadas de montagem. **Nunca coloque texto corrido nelas.** No `relatorio-descritivo.tex`, a ordem dos `\input` segue os incisos I a VIII do art. 27 — mexer nessa ordem muda a estrutura que a norma fixa (o inciso IX permite outra ordem só quando ela favorecer a compreensão).
- **`dados-do-pedido.tex`** — fonte única dos metadados. O título fica aqui justamente porque o art. 24, IV exige que seja idêntico no relatório e no resumo; duas cópias em arquivos diferentes seria um defeito formal esperando para acontecer. Os valores usam `\providecommand` para que o showcase os injete por linha de comando. O bloco final, comentado, guarda depositante/inventores/prioridades — dados que vão no **formulário eletrônico** e que o art. 21 proíbe nos documentos.
- **`lib/inpitex.sty`** — o pacote de estilo. Sobre `article`, com `geometry`, `setspace`, `fancyhdr`, `lastpage`, `enumitem`, `graphicx`, `amsmath`, `booktabs`/`longtable` e `etoolbox`. **Cada bloco cita o artigo que o justifica** — mantenha essa convenção ao editar. Adicione `\RequirePackage` aqui, não nas raízes.
- **`pedido/`** — o conteúdo redigido, em `relatorio-descritivo/` (cinco arquivos na ordem do art. 27), `reivindicacoes/`, `desenhos/` (a declaração de figuras) e `resumo/`. Cada arquivo abre com um comentário do que a norma pede naquela seção.

### Pontos de projeto que exigem cuidado

**Paginação `n/N` (art. 16).** `\fancyhead[C]{\thepage/\pageref{LastPage}}`, com `includehead=false` no `geometry` para que o cabeçalho fique **dentro da margem superior**, acima da caixa de texto. Como cada peça é um PDF próprio, o `lastpage` devolve o total daquela peça e a contagem recomeça em 1 sozinha. O estilo `plain` foi igualado ao `inpi` para que nenhuma página escape da paginação.

**Travamento de linhas por página (art. 17).** A altura da caixa de texto é fixada em 31 linhas via `lines=31` do `geometry`, de modo que nenhuma página possa estourar o teto de 35. **O `\normalsize` imediatamente antes do `\geometry` não é decorativo:** a chave `lines` calcula a altura a partir do `\baselineskip` vigente, e o `\onehalfspacing` só altera o `\baselineskip` na próxima seleção de fonte. Sem ele o cálculo usaria entrelinha simples e caberiam ~46 linhas.

**Expansão dos metadados.** `\titulodopedido`, `\natureza`, `\modalidade`, `\pedidovinculado` e `\formatorotuloparagrafo` guardam o argumento com **`\protected@edef`**, não `\def`. Os valores chegam como macros (`\NaturezaDoPedido` etc.) por causa do padrão `\providecommand`; com `\def`, tanto o `\ifdefstring` quanto o `\ifdefempty` compararariam contra o *nome* da macro em vez do valor, e todos os seletores e guardas falhariam. O `\protected@edef` expande antes de guardar e preserva os caracteres acentuados.

**Opções do `\includegraphics`.** Em `\inpi@figuradesenho` a chamada é `\expandafter\includegraphics\expandafter[\inpi@opcoesdafigura]{...}`. O `keyval` varre a lista de opções procurando vírgulas **sem expandir macros**: passar uma macro direto viraria uma única chave gigante e o `keyval` erraria ao montar `\csname KV@Gin@...\endcsname`. O par de `\expandafter` resolve a macro numa lista literal antes, e é inofensivo quando o argumento já vem literal.

**Argumento opcional vazio em `\inpi@figuradesenho`.** O padrão do argumento opcional é **vazio**, e não `\inpi@opcoesfigura`. É o que distingue "o autor não pediu largura nenhuma" de "o autor pediu uma largura menor porque a figura divide a página" — com o valor padrão embutido, as duas situações chegam indistinguíveis e a conferência de margem do art. 38 dispararia na segunda, que é legítima.

**Margem lateral das figuras (art. 38, I).** A `\newgeometry` de `\abrirdesenhos` fixa a **caixa de texto** em 2 cm de cada lado, mas o art. 38, I mede a **figura**, e as duas coisas só coincidem quando a figura preenche a largura da caixa. Com `keepaspectratio`, qualquer imagem mais alta que ~1,3:1 passa a ser limitada pela altura e encolhe na horizontal — uma figura 3:16 sai com mais de 8 cm de margem de cada lado. Por isso `\inpi@figuradesenho` compõe a figura numa caixa, mede `\wd` e compara com a faixa da norma. **Não troque isso por uma conferência da geometria**: a geometria está certa e não é ela que a norma mede.

**Tabelas e `center` (art. 20).** O ambiente `tabelainpi` usa `\centering`, **não** o ambiente `center`. O `center` é um `trivlist`, e `longtable` dentro de lista não quebra de página: transborda, o LaTeX emite só um `Overfull \vbox` (aviso, invisível ao `-halt-on-error`) e as linhas excedentes **somem do PDF**. A legenda é presa ao corpo por `\penalty\@M` dos dois lados da cola e por `\interlinepenalty\@M` dentro dela — sem os dois, a legenda fica órfã no pé da página ou se parte no meio, e a identificação sequencial que o art. 20 exige acaba longe da tabela que identifica. Para tabela que não caiba na largura, use os tipos de coluna `L`/`R`/`C` com frações de `\linewidth`.

**Menção de vínculo só no relatório descritivo.** Os arts. 43, II e 51, II dizem em que documento entra o "Certificado de adição de invenção do ___" / "Dividido do ___", e dizem só um: o relatório descritivo. Por isso `\inpi@mencaodevinculo` é passada como argumento opcional de `\inpi@imprimirtitulo` a partir de `\abrirrelatoriodescritivo`, e não embutida na macro — que o resumo também usa. No resumo a menção não é exigida por nada (o art. 40, I pede ali o título e mais nada) e é indicação processual, do tipo que o art. 21 chama de estranho à matéria do pedido.

**Vocabulário de "concretização" (art. 27, VII).** Em modelo de utilidade a norma veda "trechos do tipo *concretização preferida*, *a título exemplificativo* etc.", porque o modelo protege forma determinada e não princípio com concretizações alternativas. `\secaodasconcretizacoes` e `\nomedaconcretizacao` trocam junto com a natureza. Ao escrever conteúdo, use as macros em vez de texto fixo.

**Declaração única das figuras.** `pedido/desenhos/figuras.tex` é lido **duas vezes**, e `\figura` se comporta de um jeito em cada leitura: `\imprimirdescricaodosdesenhos` (no relatório) gera a listagem dos arts. 26, III e 27, V; `\imprimirdesenhos` (em `desenhos.tex`) posiciona as imagens. A troca é feita com `\let\figura\inpi@figuralistagem` / `\let\figura\inpi@figuradesenho`. **Não crie uma segunda lista de figuras** — a congruência de numeração e ordem é garantida por essa fonte única, e o `verificar-conformidade.sh` a confere.

**Guardas de coerência.** Cinco `\PackageError` em `\AtBeginDocument` (para valer em qualquer ordem de preenchimento): natureza inválida, modalidade inválida, certificado de adição em modelo de utilidade (arts. 42 e 43), vínculo ausente em `adicao`/`divisao` (arts. 43, II e 51, II) e título vazio (art. 24). Ao acrescentar campo obrigatório, acrescente a guarda — errar isso silenciosamente custa uma exigência formal do INPI.

## Redigindo um pedido real a partir do material de origem

Em um repositório **derivado** deste template, o material do inventor fica em `material-de-origem/` — pasta **plana** (o material não vem separado por seção do pedido) com uma única subpasta, `anterioridades/`, cujo critério é a origem do documento, não a seção que ele alimenta. Comece **lendo a pasta inteira** e monte você mesmo o inventário — o que é cada documento, pelo título e pelo conteúdo, e o que dele se aproveita; apresente esse inventário ao depositante e espere a confirmação antes de redigir. O `NOTAS-PARA-O-AGENTE.md` da pasta **não** é o índice do material: ele carrega o que nenhuma leitura recupera — sobretudo **o que não usar** (versão superada, rascunho, ensaio que não se confirmou), mais as decisões já tomadas e o que está em aberto. Leia-o antes de inventariar e cruze as duas coisas. O conteúdo da pasta não é versionado **por padrão** (sigilo — art. 11 da LPI), mas em repositório privado a inversão é decisão legítima do depositante, feita comentando o bloco marcado no `.gitignore` antes do primeiro commit; `anterioridades/` fica fora nos dois casos, por direito de terceiro. **Não altere esse `.gitignore` por conta própria** — é decisão de sigilo do depositante, não de organização de repositório.

Quatro limites que valem mais que qualquer regra de forma deste arquivo:

1. **Não invente dado técnico.** Faltou informação para uma seção? **Pare e pergunte.** Número plausível preenchido por conta própria é matéria que não se sustenta no exame do art. 24 da LPI, em documento que o depositante assina. Este é o erro mais grave que um agente pode cometer aqui.
2. **Não acrescente matéria fora do material de origem** (art. 32 da LPI e Resolução INPI/PR nº 93/2013).
3. **Não transporte texto de `anterioridades/` para o pedido.** Anterioridade se cita em prosa, pelo número de publicação (art. 27, II).
4. **Nunca crie, gere ou redesenhe uma imagem para `figuras/`** — nem copiando desenho de origem, nem com TikZ, nem por qualquer outro meio. Carimbo e logotipo de um print de CAD violam o art. 21; o art. 39, I exige figura isenta de texto. A imagem final só entra em `figuras/` trazida por quem redige o pedido — veja `figuras/LEIA-ME.md`. Falta o desenho de uma figura necessária? Pare e peça ao depositante, como faltaria qualquer outro dado técnico (limite 1).

Ao concluir, entregue um **mapa de proveniência** (qual documento sustentou qual seção ou parágrafo, fechando o círculo aberto pelo inventário) e rode `make verificar`, relatando os avisos.

## Convenções de escrita

- **Idioma**: todo o texto, comentários, nomes de macro e argumentos de comando em PT-BR. O art. 3º exige o pedido "sempre em idioma português". Não há resumo em língua estrangeira (aquilo era exigência da ABNT).
- **Estrangeirismos**: evite palavra estrangeira quando houver termo em português. Prefira o termo técnico consagrado no setor (Resolução INPI/PR nº 124/2013, itens 2.30 a 2.32, exige terminologia clara e uniforme).
- **Terminologia uniforme** (art. 23, IV): o mesmo elemento com o mesmo nome e o mesmo sinal de referência em **todo** o pedido — relatório, reivindicações, desenhos e resumo. Divergência aqui gera exigência.
- **Sinais de referência**: sempre entre parênteses e sempre os mesmos para o mesmo elemento em todas as figuras (art. 39, IV). Ao citar elemento do desenho no texto, cite o sinal: "a haste de acionamento (4) desloca o assento (9)".
- **Sequências biológicas**: ao citar uma sequência no relatório, nas reivindicações ou nos desenhos, refira-a pelo identificador precedido de `SEQ ID NO:` ("o oligonucleotídeo SEQ ID NO: 3"). A Listagem de sequências em si **não é gerada aqui**: é um XML no padrão OMPI ST.26 produzido pelo WIPO Sequence (Portaria INPI/PR nº 48/2022, art. 4º). Veja a seção correspondente do `README.md` antes de mexer em qualquer coisa relacionada.
- **Unidades**: Sistema Internacional (art. 23, I), salvo termo consagrado em área técnica específica (Btu, mesh, barril, polegada).
- **Ênfase**: em texto corrido **não use negrito nem itálico** — o art. 21 desestimula sinais estranhos à matéria e a norma não prevê destaque tipográfico no corpo. O negrito fica restrito ao que o próprio template aplica: título do pedido, títulos de seção e cabeçalhos de tabela.
- **Travessões**: evite travessão (—) e meia-risca (–) no corpo do pedido; use vírgulas ou parênteses. Em reivindicação eles são especialmente indesejáveis, pela regra de redação sem interrupção do art. 28, III.
- **Nomes de arquivo**: kebab-case em PT-BR (`1-campo-tecnico.tex`, não `technicalField.tex`).
- **Rótulos (`\label`)**: praticamente não são usados. O pedido não tem referência cruzada numerada — a norma pede remissão pelos **sinais de referência** e pelo número da reivindicação, escritos literalmente. O art. 29, VII proíbe reivindicação que remeta ao relatório ou aos desenhos ("como descrito na parte ... do relatório").
- **Sem referências cruzadas de leitura**: escreva de forma unidirecional. O art. 29, VII e o art. 32, V vedam esse tipo de remissão nas reivindicações, e no relatório ela só atrapalha o examinador.

## Diretrizes para agentes de IA (Claude Code)

**Verificação bidirecional dos sinais de referência.** O aviso do `verificar-conformidade.sh` é heurístico e não-bloqueante, e **não vê o interior das imagens**. O que ele consegue conferir é o triângulo entre o texto, a frase de cada figura em `pedido/desenhos/figuras.tex` e o glossário `figuras/sinais-de-referencia.md` — que é a única fonte do repositório a dizer em que figura cada sinal está desenhado, e por isso declara isso explicitamente (`- (4) haste de acionamento — Figuras 1, 2`).

Esse `— Figuras N` só vale se quem escreveu **abriu a imagem e conferiu**. É trabalho seu, não do script. Garanta que: (a) todo sinal citado no texto exista em alguma figura; (b) todo sinal desenhado nas figuras seja citado no texto; e (c) o mesmo sinal designe sempre o mesmo elemento (art. 23, IV; art. 39, IV). Faça isso sempre que mexer em desenhos, em sinais de referência ou ao concluir um trabalho, e mantenha o glossário fiel ao que está desenhado — declarar figura onde o sinal não aparece é pior que não declarar, porque desliga a checagem sem avisar.

**Fundamentação das reivindicações.** Ao editar o quadro reivindicatório ou o relatório, confira que **toda** característica pleiteada está descrita e concretizada no relatório descritivo (arts. 24 e 25 da LPI; art. 29, VI). É a causa mais comum de indeferimento, e vale mesmo quando o objeto é realmente novo e inventivo. Confira também o inverso: matéria no quadro que não aparece no relatório (Resolução INPI/PR nº 124/2013, itens 3.96 e 3.97).

**Grandezas numéricas em faixa, não em valor fechado.** Ao descrever medida, proporção, temperatura, tempo ou qualquer outra grandeza no relatório descritivo ou no quadro reivindicatório, prefira expressá-la como faixa ou amplitude ("entre X e Y") a um valor fechado, sempre que o material de origem sustentar a variação: valor fechado protege só aquele número exato, e faixa protege toda a amplitude reivindicada. Isso não é exceção ao limite de não inventar dado técnico — se o material só traz um valor pontual e não há como saber se ele admite variação, pergunte ao depositante em vez de arbitrar os extremos da faixa.

**Título e categorias.** Ao mudar as categorias de reivindicação, ajuste o título (art. 25 e Resolução 124/2013, item 1.02). Se o quadro deixa de ter reivindicação de processo, "E PROCESSO DE ..." tem de sair do título — e ele muda em **um só lugar**, `dados-do-pedido.tex`.

**Ao rodar `make verificar`, leia os AVISOS.** Eles não quebram a CI de propósito, mas apontam exatamente o tipo de incongruência que gera exigência formal no INPI.

**Não reintroduza elemento ABNT.** Se uma tarefa parecer pedir sumário, referências, glossário, apêndice, capa ou figura no meio do texto, o pedido está mal formulado à luz dos arts. 3º, 19 e 21 — diga isso em vez de implementar.

## Revisão final

Ao terminar de redigir ou fazer uma edição longa (mais de 30% do texto), verifique que:

1. nenhuma tabela ou fórmula ficou sem parágrafo que a comente e contextualize (elemento solto é matéria que o examinador não sabe como ler);
2. nenhuma figura declarada ficou sem citação no corpo do relatório, e nenhuma figura citada ficou sem declaração;
3. a numeração dos parágrafos está contínua — use `\pnum` em todo parágrafo **que você escrever** no relatório, sob pena de violar o art. 26, II. A exceção é a listagem de figuras dos arts. 26, III e 27, V: o parágrafo de abertura e as linhas "A Figura N apresenta ..." saem sem rótulo, porque o próprio formulário oficial do e-Patentes as estiliza como títulos (`AppBody-Heading`, sem numeração), e não como parágrafos do corpo (`AppBody-Description`, que é o estilo numerado `[1]`). Isso é decisão do template, tomada contra o formulário oficial, e não descuido — **não "conserte"**;
4. `make verificar` termina com `Conformidade de forma: OK`, e os avisos foram lidos e resolvidos.
