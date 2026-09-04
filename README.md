# Template LaTeX para pedido de patente no INPI

Modelo para redigir e compilar as peças de um **pedido de patente** — de
invenção ou de modelo de utilidade — na forma exigida pela
**Portaria/INPI/DIRPA nº 14, de 29 de agosto de 2024**, que disciplina a forma e
o conteúdo dos pedidos de patente e certificados de adição.

O template gera **quatro PDFs**, que são exatamente os arquivos anexados no
Peticionamento Eletrônico do INPI:

| Arquivo gerado | Peça do pedido | Base legal |
| --- | --- | --- |
| `relatorio-descritivo.pdf` | Relatório descritivo | art. 3º, II |
| `reivindicacoes.pdf` | Reivindicações | art. 3º, III |
| `desenhos.pdf` | Desenhos | art. 3º, IV |
| `resumo.pdf` | Resumo | art. 3º, VI |

São quatro documentos separados porque o **art. 16** determina que cada um tenha
sequência de numeração independente, com a paginação no formato `1/3`
centralizada na margem superior. Não existe um "documento único" do pedido.

> **Este template cuida da forma, não do mérito.** Ele não diz se a sua
> invenção é nova, dotada de atividade inventiva ou suficientemente descrita
> (arts. 8º, 11, 13, 24 e 25 da LPI) — isso é exame técnico. Para um depósito
> real, procure o setor de propriedade intelectual da sua instituição ou um
> profissional habilitado.

---

## Antes de começar: sigilo

O art. 11 da LPI considera nova a invenção não compreendida no estado da
técnica, e o estado da técnica é **tudo o que foi tornado acessível ao público
antes do depósito**. Um repositório público com a descrição da sua invenção,
antes de depositar, é divulgação — você destrói a própria novidade.

O período de graça do art. 12 da LPI dá 12 meses de rede de proteção, mas é
rede, não plano: o art. 11, § 2º da Portaria 14/2024 só aceita, para esse fim,
divulgação de **documentos não-patentários**.

Daí duas regras:

1. **Um repositório por pedido**, derivado deste template. Não escreva um pedido
   real dentro do repositório do template.
2. **Esse repositório é privado** até o depósito — na prática, até a publicação
   (18 meses, art. 30 da LPI). Não há ganho em abrir antes.

O template já colabora: a guarda `github.repository` no workflow faz os passos
só-do-template serem pulados em repositórios derivados, e o `.gitignore` mantém
o material de origem fora do versionamento **por padrão**.

Esse padrão é invertível, e para um repositório privado a inversão é razoável —
veja "Versionar ou não o conteúdo" em `material-de-origem/LEIA-ME.md`. Só há uma
condição que não se negocia: **decida antes do primeiro commit**. Histórico de
git é permanente e visibilidade é um botão; material commitado e apagado depois
continua no histórico e aparece inteiro se o repositório algum dia for aberto.

Uma consequência prática: para criar o repositório do pedido, use **"Use this
template"**, não fork. O template gera repositório sem histórico; o fork carrega
o histórico e o vínculo com o original.

---

## Por onde começo

1. **Preencha `dados-do-pedido.tex`.** É o único arquivo de metadados: título,
   natureza, modalidade. O título fica em fonte única justamente porque o
   **art. 24, IV** exige que ele seja idêntico no relatório descritivo e no
   resumo.
2. **Escreva o conteúdo** nos arquivos de `pedido/`. Cada um abre com um
   comentário explicando o que a norma pede naquela seção, com o artigo
   correspondente.
3. **Compile e verifique:**

   ```sh
   make pdf          # gera as quatro peças
   make verificar    # afirma a conformidade de forma sobre os PDFs gerados
   ```

4. **Anexe os quatro PDFs** no Peticionamento Eletrônico, junto ao formulário
   de requerimento e à GRU paga.

---

## Os dois eixos de seleção

O template cobre qualquer situação prevista nos normativos por meio de dois
seletores independentes em `dados-do-pedido.tex`. Não há arquivo duplicado: os
mesmos arquivos de conteúdo servem a todas as combinações.

### `\natureza` — o que se pretende proteger

| Valor | Efeito |
| --- | --- |
| `invencao` | Reivindicações conforme os arts. 29 a 31: quantas independentes forem necessárias, uma por categoria. Desenhos opcionais. |
| `modelo-de-utilidade` | Reivindicações conforme os arts. 32 a 36: **uma única** independente (art. 33), dependentes só nas hipóteses do art. 35. Desenhos **obrigatórios** (art. 22). |

O seletor também troca o vocabulário das seções ("Campo da invenção" ↔ "Campo
do modelo de utilidade") e o efeito a destacar nos fundamentos — efeito técnico
na invenção, melhoria funcional no modelo (art. 27, IV).

### `\modalidade` — como o pedido entra

| Valor | Efeito |
| --- | --- |
| `originario` | Depósito comum. Nada é impresso após o título. |
| `adicao` | Imprime, após o título, "Certificado de adição de invenção do \_\_\_" (art. 43, II). Exige `\pedidovinculado` e só existe para `invencao` (arts. 42 e 43). |
| `divisao` | Imprime, após o título, "Dividido do \_\_\_" (art. 51, II). Exige `\pedidovinculado`. |
| `fase-nacional-pct` | Entrada na fase nacional de pedido internacional. A forma dos documentos é a mesma (art. 65 e Portaria INPI nº 39/2021, art. 9º, § 1º). |

Combinações incoerentes param a compilação com mensagem explícita — certificado
de adição em modelo de utilidade, vínculo ausente em adição ou divisão, título
vazio, valor de seletor desconhecido.

---

## Como escrever

### Parágrafos numerados

O **art. 26, II** exige que cada parágrafo do relatório descritivo tenha
numeração sequencial à esquerda do texto. Abra cada parágrafo com `\pnum`:

```latex
\pnum A presente invenção refere-se a um dispositivo de acionamento (1) que
compreende um corpo tubular (2).

\pnum Em uma concretização preferida, o corpo tubular (2) é obtido por injeção.
```

O comando não recebe argumento de propósito — assim tabelas e fórmulas podem
ser intercaladas entre parágrafos sem quebrar nenhum ambiente. O formato do
rótulo é escolhido em `dados-do-pedido.tex`: `tres-digitos` (`[001]`, como a
norma exemplifica) ou `arabico` (`[1]`, como os formulários oficiais).

O resumo e as reivindicações **não** usam `\pnum`: a numeração de parágrafos é
exigência exclusiva do relatório descritivo.

### Seções

```latex
\secaoinpi{Campo \danatureza}
```

`\danatureza` expande para "da invenção" ou "do modelo de utilidade", conforme
o seletor. Use `\nomedanatureza` quando precisar só de "invenção"/"modelo de
utilidade". Não há `\chapter`, `\section`, numeração de seção nem sumário: nada
disso existe em um pedido de patente.

### Tabelas

Permitidas no relatório descritivo e nas reivindicações, em preto e com
identificação sequencial (**art. 20**):

```latex
\begin{tabelainpi}{Energia consumida por ciclo}
    \begin{tabular}{lrr}
        \toprule
        Conjunto & Energia (J) & Pressão (kPa) \\
        \midrule
        Controle   & 216{,}0 & 0 \\
        Invenção   &   1{,}9 & 0 \\
        \bottomrule
    \end{tabular}
\end{tabelainpi}
```

A legenda sai acima, numerada ("Tabela 1 -- ..."), como nos formulários
oficiais. Toda tabela precisa ser comentada em algum parágrafo: tabela solta é
matéria que o examinador não sabe como ler.

### Fórmulas e expressões matemáticas

Use `equation`, que já numera sequencialmente conforme o art. 20:

```latex
\begin{equation}
    W = \int_{0}^{t_{p}} v(t)\, i(t)\, \mathrm{d}t
\end{equation}
```

### Reivindicações

```latex
\begin{quadroreivindicatorio}
    \reivindicacao DISPOSITIVO DE ACIONAMENTO, compreendendo um corpo tubular
    (2), caracterizado por a haste (4) apresentar um ressalto de encosto.

    \reivindicacao DISPOSITIVO DE ACIONAMENTO, de acordo com a reivindicação 1,
    caracterizado por compreender um sensor de pressão (7).
\end{quadroreivindicatorio}
```

Três regras de forma valem para toda reivindicação (**art. 28**): numeração
consecutiva em arábicos, **uma única** expressão "caracterizado por" e redação
**sem interrupção por pontos** — um único ponto final. Por causa do inciso III,
evite abreviaturas com ponto e números com ponto decimal (use vírgula).

### Figuras

Figuras existem **apenas** no documento de desenhos: o **art. 19** não as aceita
no relatório descritivo, nas reivindicações nem no resumo. Declare cada uma
**uma única vez** em `pedido/desenhos/figuras.tex`:

```latex
\figura{vista-em-corte}{a vista em corte longitudinal do dispositivo (1)}
\figura[width=0.45\linewidth]{detalhe}{o detalhe do ressalto de encosto (4)}
```

O arquivo é lido duas vezes: o relatório descritivo gera com ele a listagem
exigida pelos **arts. 26, III e 27, V** ("A Figura 1 apresenta a vista em
corte..."), e `desenhos.tex` posiciona as imagens rotuladas "Figura 1",
"Figura 2". Numeração e ordem ficam consistentes por construção — não há duas
listas para manter em sincronia.

As imagens vão em `figuras/`, referidas sem extensão. Sem o argumento opcional,
cada figura ocupa a página inteira; com uma largura menor, várias cabem na mesma
página, como permite o art. 37 — desde que nitidamente separadas. O documento de
desenhos tem geometria própria, conforme o **art. 38, I**: margem superior de
3 cm, laterais de 2 cm e inferior de 2 cm.

Exigências de conteúdo das figuras (**art. 39**): isentas de texto, admitidos
apenas termos indicativos ("corte AA", "aberto"); sinais de referência
identificando o mesmo elemento em todas as figuras; ordenadas conforme o
relatório. As figuras de exemplo em `figuras/` são desenhos vetoriais, com as
fontes em `figuras/fontes-dos-exemplos/` — substitua-as pelas do seu pedido.

### Cópia de comparação (modificações e pedido dividido)

Ao apresentar modificação depois do depósito, ou ao depositar pedido dividido, a
norma pede **dois** documentos tirados da mesma matéria:

- os documentos modificados, **sem qualquer tipo de rasura ou sinalização**
  (**art. 57, I**) — são os PDFs de `make pdf`;
- uma **cópia de comparação** indicando a localização das alterações, com
  **tachado** para remoção e **sublinhado** para inclusão ou substituição
  (**art. 57, II**; para o quadro reivindicatório do pedido dividido, o
  **art. 51, III**).

Você marca as alterações uma vez no texto, e o mesmo arquivo gera as duas
saídas:

```latex
\pnum ... pulsos de corrente de duração determinada\incluido{, inferior ao
tempo de resposta do assento de vedação de dupla face (9)}.

\pnum O limite de pressão é de \substituido{200 kPa}{240 kPa}.

\paragraforemovido{A unidade de controle (8) pode ainda ser substituída por um
temporizador mecânico.}
```

| Macro | No documento do pedido | Na cópia de comparação |
| --- | --- | --- |
| `\removido{texto}` | não imprime nada | ~~texto~~ |
| `\incluido{texto}` | texto, sem marca | <u>texto</u> |
| `\substituido{antigo}{novo}` | novo, sem marca | ~~antigo~~ <u>novo</u> |
| `\paragraforemovido{texto}` | nada, e **não consome número** | parágrafo tachado, com `[–]` no lugar do número |
| `\reivindicacaoremovida{6}{texto}` | nada, e **não consome número** | reivindicação tachada, exibindo o número que tinha |

As duas últimas não consomem número justamente para que a numeração sequencial
dos parágrafos (art. 26, II) e das reivindicações (art. 28, I) siga contínua no
documento do pedido depois da supressão.

Para gerar a cópia de comparação:

```sh
make comparacao     # produz relatorio-descritivo-comparacao.pdf etc.
```

O script injeta o modo por linha de comando e **não altera
`dados-do-pedido.tex`** — assim não há como anexar ao peticionamento a versão
marcada por descuido. Como reforço, `make verificar` recusa a verificação se
alguém deixar `\CopiaDeComparacao{sim}` no arquivo, porque nesse caso os PDFs do
pedido sairiam marcados, contra o art. 57, I.

O parágrafo único do art. 57 permite substituir a cópia de comparação por um
esclarecimento apontando página, trecho e tipo de modificação. Se preferir esse
caminho, escreva-o em prosa na petição.

### Listagem de sequências (pedidos com sequências biológicas)

Se o objeto do pedido contém **uma ou mais sequências de nucleotídeos e/ou de
aminoácidos fundamentais para a descrição da invenção**, é obrigatório
apresentar uma Listagem de sequências, que complementa o relatório descritivo e
serve à aferição da suficiência descritiva do art. 24 da LPI. Rege a matéria a
**Portaria/INPI/PR nº 48, de 20/06/2022** — é a ela que o art. 3º, V da Portaria
14/2024 remete ao dizer "conforme normativo vigente".

**O template não gera essa peça, e não deveria.** O artefato obrigatório é um
**arquivo XML único no padrão OMPI ST.26** (art. 4º), criado, editado e
verificado com a ferramenta **WIPO Sequence**, da OMPI (art. 4º, parágrafo
único). O que vale ali é passar na validação do esquema, e isso nenhum gerador
em LaTeX faz. Anexe o XML pelo Peticionamento Eletrônico; o sistema devolve um
**código de controle** automaticamente (art. 6º), que depois consta da
Carta-Patente (art. 10).

O que o template **exige de você nos documentos que ele gera**: ao citar uma
sequência no relatório descritivo, nas reivindicações ou nos desenhos, refira-a
pelo identificador precedido de **`SEQ ID NO:`** — por exemplo, "o
oligonucleotídeo SEQ ID NO: 3". É a mesma disciplina dos sinais de referência
das figuras. (Essa regra está escrita nas regras do padrão ST.25 publicadas pelo
INPI, item 2.2; o `SEQ ID NO:` é comum aos dois padrões, mas confirme nas regras
do ST.26 no site do INPI.)

Quatro pontos que custam caro se passarem batidos:

| | |
| --- | --- |
| **O que entra na listagem** | **Todas** as sequências lineares com 4 ou mais L-aminoácidos contínuos e **todas** com 10 ou mais nucleotídeos contínuos — **mesmo as não reivindicadas**, sondas de PCR incluídas (art. 3º, § 2º). Listar só o que foi reivindicado é erro comum. |
| **Prazo** | No ato do depósito (art. 7º). Se faltar, ainda cabe **até a data do requerimento de exame**, por **petição isenta de retribuição** (art. 7º, § 1º). Depois disso, o INPI formula exigência (art. 7º, § 2º). |
| **Correção posterior** | Exige novo arquivo **acompanhado do comprovante de retribuição** (art. 8º). A diferença entre os arts. 7º e 8º é dinheiro. |
| **Depósitos até 30/06/2022** | Em nova apresentação, **mantêm o padrão ST.25** (art. 5º). Não vale para pedidos novos. |

Há ainda um **PDF opcional**: o art. 9º permite apresentar a listagem
adicionalmente em PDF, como parte integrante do pedido, incluída após o
relatório descritivo, iniciada em página separada, sob o título "Listagem de
sequências", com páginas numeradas de forma sequencial e independente, em
algarismos arábicos, no centro da parte superior, entre 1 e 2 cm do limite da
página (art. 9º, §§ 1º e 2º). O template não o gera hoje: para não duplicar a
matéria, esse PDF teria de ser **convertido do XML**, não redigido à parte — do
contrário as duas versões divergem, que é justamente o risco que o template
existe para eliminar.

---

## O que **não** entra nos documentos

O **art. 21** proíbe, nas peças do pedido, "rasuras ou emendas, timbres,
logotipos, letreiros, assinaturas ou rubricas, sinais ou indicações de qualquer
natureza estranhos à matéria do pedido".

Não há, portanto, capa, folha de rosto, logotipo institucional, assinatura,
ficha catalográfica, sumário, listas de ilustrações ou de siglas, glossário,
índice, apêndices, anexos nem lista de referências ABNT. O **art. 3º** lista
exaustivamente o que compõe o pedido, e nada disso está lá.

**Depositante, inventores, procurador, prioridades e período de graça** vão no
**formulário eletrônico de requerimento**, não nos PDFs. Há um bloco comentado
no fim de `dados-do-pedido.tex` para você guardar esses dados em um lugar só,
sem risco de vazarem para o documento.

O estado da técnica é citado **em prosa**, dentro dos parágrafos numerados,
identificando o documento pelo número de publicação (`BR 10 2015 000000 0`,
`US 2018/0123456 A1`). Não existe seção de referências em um pedido de patente.

---

## Compilação

O `make` cobre o uso corrente:

```sh
make              # = make pdf
make pdf          # compila as quatro peças
make relatorio    # compila só o relatório descritivo
make verificar    # rede de conformidade normativa
make lint         # análise estática (chktex) dos arquivos de prosa
make exemplos     # showcase dos dois eixos de seleção
make comparacao   # cópia de comparação (arts. 51, III e 57, II)
make limpar       # remove artefatos
make ajuda        # lista os alvos
```

Sem o `make`, cada peça é uma raiz LaTeX independente:

```sh
latexmk -pdf -halt-on-error relatorio-descritivo.tex
```

São necessárias **duas passadas** de `pdflatex` (o `latexmk` cuida disso): a
paginação `n/N` depende do total de páginas da peça, que só é conhecido ao final
da primeira. Uma passada única entrega paginação desatualizada.

As receitas correspondentes do LaTeX Workshop já estão em
`.vscode/settings.json`. Como há quatro raízes, não existe `rootFile` fixo — a
extensão compila o arquivo aberto no editor.

### Rede de conformidade

`./verificar-conformidade.sh` compila as quatro peças e afirma, sobre os PDFs,
cada exigência de forma verificável automaticamente: paginação por peça
(art. 16), 20 a 35 linhas por página (art. 17), ausência de representação
gráfica fora dos desenhos (art. 19), título idêntico entre relatório e resumo e
com até 500 caracteres (art. 24), numeração sequencial dos parágrafos
(art. 26, II), congruência das figuras (arts. 26, III e 39, V), forma das
reivindicações (art. 28), reivindicação independente única em modelo de
utilidade (art. 33) e limite de uma página do resumo (art. 40, II).

Emite ainda um **aviso não-bloqueante** de congruência dos sinais de referência
entre o texto e as descrições das figuras. É heurística de fonte: o script não
vê o interior das imagens, então um sinal desenhado na figura mas não citado na
descrição dela aparece como aviso a conferir à mão.

`--check-only` pula a compilação e verifica os PDFs existentes — é assim que a
CI o executa, como passo bloqueante.

---

## Trabalhando com um agente de IA

O `CLAUDE.md` deste repositório carrega as regras da norma, então um agente que
abra o projeto já começa sabendo o que o INPI exige. O que falta é o **seu**
material e o **seu** enquadramento.

### Onde colocar o material

Em `material-de-origem/`: relatório do projeto, tese, notas, CAD, fotos,
resultados de ensaio. A pasta é **plana de propósito** — não classifique o
material por seção do pedido, porque ele não vem separado assim (um relatório
traz descrição, dados e menção a trabalhos anteriores no mesmo arquivo).
Nomes de arquivo descritivos valem mais que estrutura de pastas.

A única separação é `material-de-origem/anterioridades/`, e o critério não é
"que seção isso alimenta" e sim **de quem é o documento**: obra de terceiro,
sobre a qual vale uma regra distinta — nenhum trecho vai para o pedido, a
citação é em prosa pelo número de publicação (art. 27, II).

No `NOTAS-PARA-O-AGENTE.md` da pasta você **não** escreve o que é cada arquivo:
o agente lê o título e o conteúdo e conclui sozinho. Anote ali só o que nenhuma
leitura recupera — antes de tudo **o que não usar** (versão superada, rascunho,
ensaio que não se confirmou), mais o que já está decidido e o que ainda falta.

E peça o inventário **antes** da redação: uma linha por documento, o que é e o
que dele se aproveita, para você confirmar. Documento lido errado contamina tudo
o que vier depois, e corrigir na entrada custa um minuto.

O conteúdo da pasta **não é versionado por padrão** (ver "Versionar ou não o
conteúdo", no `LEIA-ME.md` dela). Em repositório privado, versionar é decisão
legítima e às vezes melhor — comente o bloco marcado no `.gitignore`, antes do
primeiro commit. `anterioridades/` fica de fora nos dois casos.

### As quatro coisas que o agente não pode fazer

| | |
| --- | --- |
| **Inventar dado técnico** | Um modelo de linguagem preenche lacuna com número plausível. Num pedido isso é matéria que não se sustenta no exame (art. 24 da LPI), num documento que você assina. A instrução mais valiosa do seu prompt é "**pare e me pergunte** em vez de preencher". |
| **Acrescentar matéria fora da origem** | O art. 32 da LPI, regulado pela Resolução INPI/PR nº 93/2013, fecha a porta para incluir matéria depois do requerimento de exame. |
| **Colar texto de anterioridade** | Citação em prosa, pelo número de publicação (art. 27, II). |
| **Copiar desenho de origem para `figuras/`** | Print de CAD vem com carimbo e logotipo: o art. 21 proíbe, e o art. 39, I exige figura isenta de texto. A figura final é redesenhada — veja `figuras/fontes-dos-exemplos/`. |

### Peça um mapa de proveniência

Ao final, peça ao agente **qual documento sustentou qual seção ou parágrafo**.
É o inventário da entrada fechando o círculo: devolve a rastreabilidade sem
obrigar você a classificar o material antes, e é o que torna a conferência
viável.

### O que continua sendo seu

`make verificar` afere **forma**. Não delegue: conferir cada afirmação técnica
contra a origem; o quadro reivindicatório, cuja decisão de escopo é estratégica
e jurídica; a busca de anterioridade efetivamente feita e lida; e, num depósito
real, a passagem pelo setor de PI antes de peticionar.

---

## Fora do escopo

- **Listagem de sequências biológicas** (art. 3º, V da Portaria 14/2024 e
  Portaria INPI/PR nº 48/2022). O artefato obrigatório é XML no padrão ST.26,
  produzido pelo WIPO Sequence. Veja a seção "Listagem de sequências" acima,
  inclusive o que ela exige dos documentos que este template gera.
- **Formulário de requerimento, GRU e procuração** (arts. 4º, 7º e 59). São atos
  no sistema de peticionamento.
- **Outros direitos de propriedade intelectual.** O escopo aqui é patente —
  invenção e modelo de utilidade. Marca, desenho industrial, programa de
  computador e cultivar têm normas e formulários próprios.

---

## Base normativa

Os textos consultados estão em `referencias-inpi/`, junto aos formulários
oficiais do e-Patentes 4.0 que serviram de referência tipográfica e de
conteúdo-guia.

| Documento | Papel |
| --- | --- |
| Portaria/INPI/DIRPA nº 14, de 29/08/2024 | Norma central deste template: forma e conteúdo do pedido |
| Resolução INPI/PR nº 124/2013 | Diretrizes de exame — conteúdo do pedido |
| Portaria INPI nº 39/2021 | Entrada na fase nacional de pedidos PCT |
| Portaria INPI nº 79/2022 | Trâmite prioritário (procedimental) |
| Portaria INPI/PR nº 48/2022 | Listagem de sequências — padrão ST.26 |

Só entram aqui normas **em vigor**. Norma revogada ou superada é removida do
repositório em vez de guardada com ressalva: material desatualizado à mão é
convite a decisão errada.

Sempre que este README, o `CLAUDE.md` ou os comentários dos arquivos citarem um
artigo sem indicar a norma, trata-se da Portaria/INPI/DIRPA nº 14/2024. "LPI" é
a Lei de Propriedade Industrial (Lei nº 9.279/1996).

---

## Mantenedor

Igor Lopes — <igor.lopes@embrapa.br>

## Licença

LaTeX Project Public License (LPPL) 1.3c. Veja o arquivo `LICENSE`.
