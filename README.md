# EmbrapaTex - Template LaTeX para Publicações da Embrapa

O **EmbrapaTex** é um template LaTeX baseado no [abnTeX2](http://www.abntex2.net.br/) desenvolvido para auxiliar pesquisadores e analistas da **Empresa Brasileira de Pesquisa Agropecuária (Embrapa)** na elaboração padronizada de seus trabalhos, relatórios e publicações técnicas. O template implementa as normas da ABNT, permitindo que o autor se concentre no conteúdo sem se preocupar com formatação.

### Tipos de Documento Disponíveis

Há **três tipos fundamentais**, escolhidos por `\tipodocumento{...}`. Cada tipo tem seu **próprio seletor de subtipo**:

- **`academico`** — trabalhos de graduação/pós (TCC, dissertação, tese…), em formato ABNT completo, com orientador, **banca**, campos de pesquisa e **instituição de ensino**. Subtipo via `\nivel{...}`:
  - `tcc` — Trabalho de Conclusão de Curso
  - `monografia` — Monografia (especialização)
  - `dissertacao` — Dissertação (mestrado)
  - `tese` — Tese (doutorado)
  - `relatorio` — Relatório acadêmico avaliado (ex.: probatório)
- **`publicacao`** (padrão) — publicações técnico-científicas da Embrapa (séries). Subtipo via `\serie{...}`; o `\numerodocumento` é impresso na capa:
  - `relatorio` — Relatório Técnico
  - `boletim` — Boletim de Pesquisa e Desenvolvimento
  - `comunicado` — Comunicado Técnico
  - `documento` — Documento genérico
- **`corporativo`** — relatórios e análises empresariais (ex.: análise exploratória de dados de uma commodity). Subtipo via `\categoria{relatorio|analise|probatorio}`. Usa um **Sumário executivo** no lugar de resumo/abstract e dispensa banca/ficha. O subtipo `probatorio` é um **Relatório de Comprovação de Período Probatório** (identificação do servidor + assinaturas) — veja [Modo corporativo](#modo-corporativo).

> Cada seletor afeta apenas o rótulo da capa e a frase do preâmbulo; por baixo, só preenche dois campos. Para um caso não previsto, defina-os direto no `main.tex`:
>
> ```tex
> \subtitulodacapa{Circular Técnica}
> \naturezadapublicacao{Circular Técnica da \imprimirunidade\ (\imprimirunidadesigla).}
> ```

### Estrutura do Projeto

```
├── main.tex                          # Arquivo principal
├── lib/
│   ├── preambulo.tex                 # Configurações de pacotes
│   ├── embrapatex.sty                # Pacote de estilos EmbrapaTex
│   └── logo-embrapa-*.png            # Logos da Embrapa
├── elementos-pre-textuais/           # Resumo, abstract, sumário executivo, etc.
├── elementos-textuais/               # Capítulos do documento
│   ├── introducao.tex
│   ├── revisao-de-literatura.tex
│   ├── estado-da-arte.tex
│   ├── material-e-metodos.tex
│   ├── resultados-e-discussao.tex
│   └── consideracoes-finais.tex
├── elementos-pos-textuais/           # Referências, glossário, apêndices, anexos
└── figuras/                          # Diretório para figuras
```

# Por onde começo?

1. Abra o arquivo `main.tex` e configure os dados do seu documento:
   - Tipo de documento (`\tipodocumento{publicacao}` é o padrão) e o subtipo do seu tipo: `\nivel{...}` (academico), `\serie{...}` (publicacao) ou `\categoria{...}` (corporativo)
   - Unidade Embrapa (`\unidade{...}`)
   - Autor, título, data e local
   - Orientador/supervisor (se aplicável)
2. Edite os arquivos nos diretórios `elementos-pre-textuais/`, `elementos-textuais/` e `elementos-pos-textuais/`
3. Adicione suas figuras ao diretório `figuras/`
4. Compile o projeto. O modo recomendado é `latexmk -pdf main.tex` (executa todas as passadas e o `makeglossaries` automaticamente). Alternativamente, rode manualmente: `pdflatex` → `biber` → `makeglossaries` → `makeindex` → `pdflatex` (2×)

> **Começar do zero?** O `main.tex` já vem preenchido com um **exemplo fictício** (publicação — Relatório Técnico), de propósito: assim ele compila e mostra uma amostra logo de cara. Para o seu documento, **substitua os valores pelos seus** e **esvazie (`{}`) os campos que não usar** — campos vazios somem do PDF automaticamente (exibição automática de elementos). Para se localizar, tudo que você edita no `main.tex` fica entre os marcadores **`SEUS DADOS (início)`** e **`SEUS DADOS (fim)`**, e a lista de capítulos está sob **`SEUS CAPÍTULOS`**. Os `exemplo-*.tex` ficam como referência de "como fica preenchido" em cada modo.

> **Quer ver todos os tipos de uma vez?** Rode `./gerar-exemplos.sh` para gerar `exemplo-academico.pdf` (tese), `exemplo-publicacao.pdf` (boletim), `exemplo-corporativo.pdf` (análise) e `exemplo-probatorio.pdf` (comprovação de período probatório) — uma amostra de cada modo. (A CI também publica esses PDFs como artefato `exemplos-pdf` em cada Pull Request.)

> **Atalhos:** há um `Makefile` com `make` (compila), `make exemplos`, `make lint` (chktex), `make verificar` (rede de regressão) e `make limpar`. Rode `make ajuda` para a lista.

> **Usando o template num documento real (CI sem atrito):** `make verificar` (rede de regressão) e `make exemplos` (showcase) — e os passos correspondentes da CI — são **testes do próprio template**, calibrados para o conteúdo-exemplo padrão. Num repositório **derivado** do template (o seu documento), a CI **pula esses passos automaticamente**: você só vê o lint + a compilação do seu `main.tex` + o PDF publicado, sem falsos vermelhos. Não precisa rodar `make verificar` para o seu documento. (Criou o seu repositório a partir de uma cópia **antiga** do template? Basta copiar o `.github/workflows/compilar-latex.yml` atualizado — a guarda `if:` já pula os passos só-do-template no seu repo.)

# Dicas de Formatação

Veja a seguir como inserir alguns elementos no seu texto.

### Como inserir uma Tabela
```tex
\begin{table}[h!]	
	\centering
	\Caption{\label{tab:label_da_tabela} Legenda da Tabela}
	\EMBRAPAtab{}{
		\begin{tabular}{ccll}
			\toprule
		    	Coluna 1 & Coluna 2 & Coluna 3 & Coluna 4 \\
			\midrule \midrule
				Dado 1 & Dado 2 & Dado 3 & Dado 4 \\
			\bottomrule
		\end{tabular}
	}{
		\Fonte{Elaborado pelo autor}
    }
\end{table}
```

> **Espaçamento das linhas — use comandos, não ambientes.** Dentro de `\EMBRAPAtab`/`\EMBRAPAqua`/`\EMBRAPAfig`, ajuste o espaçamento com **comandos** — `\renewcommand{\arraystretch}{0.9}` (antes do `tabular`) ou `\linespread{1}\selectfont` — e **nunca** com ambientes de espaçamento (`SingleSpace`, `spacing`, `Spacing`…). Esses encapsuladores medem o conteúdo num `\hbox` (modo restrito), onde os comandos verticais desses ambientes causam **erro fatal** (`Missing \endgroup`). Para tabelas que passam de uma página, use a **Tabela longa** abaixo (e não um ambiente de espaçamento para "encolher" a tabela).

### Como inserir um Quadro
```tex
\begin{quadro}[h!]	
	\centering
	\Caption{\label{qua:label_do_quadro} Legenda do Quadro}
	\EMBRAPAqua{}{
		\begin{tabular}{|c|c|}
			\hline
			Coluna 1 & Coluna 2 \\
			\hline
			Dado 1 & Dado 2 \\
			\hline
		\end{tabular}
	}{
		\Fonte{Elaborado pelo autor}
	}
\end{quadro}
```

### Como inserir uma Figura
```tex
\begin{figure}[h!]
	\centering
	\EMBRAPAfig{
	    \Caption{\label{fig:label_da_figura} Legenda da Figura}	
	}{
	    \includegraphics[width=8cm]{figuras/nome-da-figura}
	}{
	    \Fonte{Elaborado pelo autor}
	}	
\end{figure}
```

### Como inserir uma Tabela longa (multipágina)

`\EMBRAPAtab` é um *float* e **não quebra entre páginas**. Para tabelas mais longas que uma página, use o ambiente `EMBRAPAtablonga` (baseado em `longtable`): ele quebra entre páginas e **repete o cabeçalho** automaticamente. Diferente de `\EMBRAPAtab`, ele **não** vai dentro de um `table`:

```tex
\begin{EMBRAPAtablonga}{lrr}{\label{tab:longa} Legenda da Tabela longa}{Coluna 1 & Coluna 2 & Coluna 3}{Elaborado pelo autor}
	Dado 1 & Dado 2 & Dado 3 \\
	Dado 4 & Dado 5 & Dado 6 \\
	% ... demais linhas ...
\end{EMBRAPAtablonga}
```

Os quatro argumentos do `\begin`, na ordem, são: **(1)** as colunas do `tabular` (ex.: `lrr`, `p{6cm}r`); **(2)** a legenda, **com o `\label`** — sai como "Tabela N — …" acima, na 1ª página, e entra na Lista de Tabelas; **(3)** a linha de cabeçalho (com `&` entre as colunas), repetida no topo de cada página; **(4)** o texto da fonte — sai como "Fonte: …" abaixo, na última página. A numeração segue o mesmo contador de `\EMBRAPAtab`. Há um exemplo real em `elementos-pos-textuais/apendices/exemplo-de-apendice.tex`.

### Como inserir uma Alínea
```tex
\begin{alineas}
	\item Lorem ipsum dolor sit amet;
    \item Praesent vitae nulla varius;
	\item Praesent quis erat eleifend;
	\item Mauris facilisis odio eu:
	\begin{subalineas}
		\item Integer non lacinia magna;
		\item Proin mattis placerat risus.
	\end{subalineas}
\end{alineas}
```

### Como criar Capítulos e Seções
```tex
\chapter{Nome do Capítulo}
\label{cap:nome-do-capitulo}

% Seções Secundárias
\section{Nome da Seção}
\label{sec:nome-da-secao}

% Seções Terciárias
\subsection{Nome da Subseção}
\label{sec:nome-da-subsecao}

% Seções Quaternárias
\subsubsection{Nome da Sub-subseção}
\label{sec:nome-da-sub-subsecao}
```

### Como inserir um Algoritmo
```tex
\begin{algorithm}[h!]
	\SetSpacedAlgorithm
	\caption{\label{alg:exemplo}Descrição do Algoritmo}
	\Entrada{Entrada do Algoritmo}
	\Saida{Saída do Algoritmo}
	\Inicio{
		Passo 1\;
		Passo 2\;
	}
\end{algorithm}
```

### Como preencher a Ficha Catalográfica

A ficha catalográfica é gerada automaticamente em LaTeX a partir dos campos definidos no `main.tex` — **não é mais necessário anexar um PDF externo**. Preencha os campos no bloco *Informação da Ficha Catalográfica*:

```tex
\autorinvertido{Sobrenome, Nome}   % entrada principal; se vazio, usa o \autor
\numeropaginas{85}                 % número de páginas
\ilustracao{il.}                   % il. / il. color. (opcional)
\descritores{1. Assunto um. 2. Assunto dois. I. Título.}
\cdd{630}                          % classificação CDD
\bibliotecario{Nome do Bibliotecário}
\crb{CRB-1/1234}                   % registro profissional
```

Os dados de classificação (CDD/CDU), os descritores de assunto e o registro CRB devem ser fornecidos por um(a) **bibliotecário(a)**. Os campos `\autor`, `\titulo`, `\local` e `\data` já configurados no documento são reaproveitados automaticamente, e qualquer campo deixado em branco é omitido.

# Modo corporativo

Para relatórios empresariais/não acadêmicos (por exemplo, uma análise exploratória de dados comerciais de uma commodity), defina o tipo de documento como `corporativo` no `main.tex`:

```tex
\tipodocumento{corporativo}
```

Nesse modo, o template:

- coloca na capa um subtítulo conforme `\categoria{relatorio|analise|probatorio}` (**RELATÓRIO**, **ANÁLISE** ou **RELATÓRIO DE COMPROVAÇÃO DE PERÍODO PROBATÓRIO**) e usa uma folha de rosto com texto próprio;
- substitui o par **Resumo/Abstract** (acadêmico) por um **Sumário executivo**, escrito em `elementos-pre-textuais/sumario-executivo.tex`;
- **omite** os elementos de trabalho acadêmico: banca, folha de aprovação e ficha catalográfica.

Os metadados acadêmicos (orientador, banca, campos da ficha) podem continuar preenchidos no `main.tex` — eles são simplesmente ignorados enquanto o tipo for `corporativo`. Para voltar ao formato ABNT, troque o tipo para `\tipodocumento{academico}` ou `\tipodocumento{publicacao}` (e escolha o subtipo com `\nivel{...}` ou `\serie{...}`).

## Subtipo `probatorio` — Relatório de Comprovação de Período Probatório

O subtipo `probatorio` adapta o modo corporativo para o **relatório final de período probatório** de um(a) analista. Além do sumário executivo, ele gera automaticamente a **identificação do servidor** (Seção 1) e um **bloco de assinatura** ("De acordo" da chefia) ao final, tudo a partir de campos de metadados:

```tex
\tipodocumento{corporativo}
\categoria{probatorio}
```

Preencha no `main.tex` os dados do servidor (o **nome** é o próprio `\autor`):

```tex
\autor{Seu Nome Completo}            % nome do servidor
\matriculasiape{0000000}
\cargo{Analista A --- Prospecção de Negócios}
\lotacao{Núcleo de Inovação e Negócios (NIN) --- Embrapa Acre}
\periodoprobatorio{01/06/2023 a 31/05/2026}
\chefia{Nome da Chefia Imediata}     % assina o "De acordo"
\chefiacargo{Supervisor do NIN --- Embrapa Acre}
\local{Rio Branco --- AC}            % local da assinatura
\dataaprovacao{26 de maio de 2026}   % data de fechamento (no bloco de assinatura)
```

Qualquer campo deixado em branco (`{}`) é omitido da identificação. Com `corporativo` + `probatorio`, o `main.tex` chama `\imprimiridentificacao` (abre o capítulo "Identificação" com a subseção "Servidor") e, ao final do corpo, `\imprimirassinaturas`. **O conteúdo das demais seções é seu**: escreva-o em arquivos de `elementos-textuais/` e inclua-os com `\input` no ramo `\ifprobatorio` do `main.tex` (há um esqueleto comentado lá indicando exatamente onde).

> Veja o resultado renderizado em `exemplo-probatorio.pdf` (gere com `./gerar-exemplos.sh`).

# Elementos que aparecem só quando preenchidos

Os elementos abaixo ficam sempre disponíveis no `main.tex`, mas só aparecem no PDF quando há conteúdo correspondente — caso contrário são omitidos automaticamente, sem deixar um título em página vazia:

| Elemento | Aparece quando… |
|---|---|
| **Referências** | há `\cite`/`\citeonline` (ou `\nocite`) no texto |
| **Glossário** | algum termo do glossário principal é usado com `\gls`/`\Gls` |
| **Lista de Abreviaturas e Siglas** | alguma sigla do tipo `acronym` é referenciada no texto |
| **Lista de Ilustrações** | há ao menos uma figura com legenda |
| **Lista de Tabelas** | há ao menos uma tabela com legenda |
| **Lista de Quadros** | há ao menos um quadro com legenda |
| **Lista de Algoritmos** | há ao menos um algoritmo com legenda |
| **Lista de Códigos-Fonte** | há ao menos uma listagem `lstlisting` com legenda |
| **Lista de Símbolos** | o arquivo `lista-de-simbolos.tex` tem ao menos um `\item` (lista **manual** — ver nota abaixo) |
| **Errata** | o arquivo `errata.tex` tem conteúdo (fora comentários) |
| **Dedicatória** / **Agradecimentos** / **Epígrafe** | o respectivo arquivo tem conteúdo (fora comentários) |
| **Apêndices** / **Anexos** | o argumento de `\imprimirapendices{...}` / `\imprimiranexos{...}` não está vazio |
| **Índice remissivo** | há entradas `\index{}` no texto |

Apêndices e anexos recebem o conteúdo **entre chaves** no `main.tex`; deixe as chaves vazias para omitir a seção:

```tex
% Com apêndices:
\imprimirapendices{%
    \input{elementos-pos-textuais/apendices/exemplo-de-apendice}%
}

% Sem apêndices (seção omitida):
\imprimirapendices{}
```

> As listas pré-textuais (abreviaturas/siglas, ilustrações, tabelas, quadros, algoritmos, códigos-fonte) têm sua exibição decidida com base na compilação anterior. Ao usar o `latexmk` (recomendado), a recompilação acontece automaticamente até estabilizar — não é preciso rodar à mão.

> **Lista de Símbolos é manual.** Diferente do glossário e da lista de siglas — em que o pacote `glossaries` só imprime as entradas efetivamente citadas com `\gls` —, a Lista de Símbolos vem de um arquivo digitado à mão (`lista-de-simbolos.tex`) e é exibida por inteiro sempre que tiver ao menos um `\item`. O template **não** confere, ao compilar, se cada símbolo é de fato usado no texto, então mantenha a lista em dia: inclua apenas símbolos que realmente aparecem no documento. A rede de regressão `verificar-ocultamento.sh` ajuda nesse controle emitindo um **aviso não-bloqueante** quando um símbolo listado não é encontrado no corpo.

# Mantenedor

**Igor Lopes** — igor.lopes@embrapa.br

# Licença

O EmbrapaTex é fornecido gratuitamente sob a [LaTeX Project Public License (LPPL)](http://www.latex-project.org/lppl.txt) e pode ser redistribuído livremente para fins de pesquisa e publicação.
