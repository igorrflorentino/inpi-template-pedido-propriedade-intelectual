# Makefile — atalhos para compilar e verificar o template de pedido de patente.
# Requer latexmk (compilação) e, para `make lint`, chktex — ambos vêm no
# TeX Live. Rode `make` (ou `make ajuda`) para ver os alvos.

.PHONY: all pdf relatorio reivindicacoes desenhos resumo exemplos comparacao verificar lint limpar ajuda FORCE

# As quatro peças do pedido (art. 16 da Portaria/INPI/DIRPA nº 14/2024): cada
# uma é uma raiz LaTeX própria e gera o PDF que se anexa ao peticionamento.
PECAS := relatorio-descritivo reivindicacoes desenhos resumo
PDFS  := $(addsuffix .pdf,$(PECAS))

# Arquivos de prosa para o lint. As quatro raízes e o pacote de estilo entram
# junto: erro de sintaxe ali derruba as quatro peças de uma vez.
FONTES_PROSA := pedido/*/*.tex dados-do-pedido.tex $(addsuffix .tex,$(PECAS))
# Avisos do chktex silenciados (ruído de macros/comentários neste template):
#  1 espaço após comando · 8 traços · 12/36 espaçamento · 24 espaço após \label
#  44 nudge de booktabs
# -I0 impede o chktex de seguir \input/\usepackage: cada arquivo já é
# passado explicitamente, e sem isso ele tenta abrir \input{\macro} e
# despeja avisos que não são do código.
CHKTEX_SILENCIA := -I0 -n1 -n8 -n12 -n24 -n36 -n44

# -halt-on-error: erro grave derruba o build em vez de o nonstopmode "se
# recuperar" e entregar um PDF com erro silencioso.
LATEXMK := latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error

all: pdf

## pdf       Compila as quatro peças do pedido
pdf: $(PDFS)

# QUEM DECIDE SE RECOMPILA É O LATEXMK, NÃO O MAKE.
#
# A tentação é escrever `%.pdf: %.tex dados-do-pedido.tex lib/inpitex.sty`. Não
# faça isso: o texto do pedido mora em pedido/**, as imagens em figuras/**, e
# nenhum dos dois estaria na lista. O resultado é `make pdf` responder "Nothing
# to be done" depois de você editar o relatório, e o PDF que você anexa ao
# peticionamento continuar sendo o da versão anterior — em silêncio, que é o
# pior jeito de errar aqui.
#
# Listar tudo à mão só empurra o problema (a lista envelhece a cada arquivo
# novo). O latexmk já rastreia dependência de verdade, pelo .fls que o pdflatex
# emite: ele enxerga todo \input e todo \includegraphics, inclusive os que
# aparecerem depois. Então o alvo é sempre "fora de data" para o make, e é o
# latexmk que decide não fazer nada quando nada mudou — o custo de uma chamada
# ociosa é uma fração de segundo.
%.pdf: %.tex FORCE
	$(LATEXMK) $<

FORCE:

## relatorio Compila só o relatório descritivo
relatorio: relatorio-descritivo.pdf

## reivindicacoes Compila só as reivindicações
reivindicacoes: reivindicacoes.pdf

## desenhos  Compila só o documento de desenhos
desenhos: desenhos.pdf

## resumo    Compila só o resumo
resumo: resumo.pdf

## exemplos  Gera o showcase dos dois eixos de seleção (invenção, MU, divisão)
exemplos:
	bash gerar-exemplos.sh

## comparacao Gera a cópia de comparação das peças (arts. 51, III e 57, II)
comparacao:
	bash gerar-copia-de-comparacao.sh

## verificar Roda a rede de conformidade normativa sobre os PDFs gerados
verificar:
	bash verificar-conformidade.sh

## lint      Análise estática (chktex) da prosa, das raízes e do pacote de estilo
lint:
	chktex -q $(CHKTEX_SILENCIA) $(FONTES_PROSA)
	@# O .sty vai à parte, com supressões próprias: ali o chktex não resolve
	@# \input{\macro} (27), lê os "..." das mensagens de erro como reticências
	@# (11) e trata os artigos citados nas mensagens ("art. 38, I:") como fim de
	@# frase (13). Nenhum dos três é problema em código de pacote.
	@chktex -q $(CHKTEX_SILENCIA) -n11 -n13 -n27 lib/inpitex.sty

## limpar    Remove artefatos de compilação (inclui os PDFs do showcase)
limpar:
	latexmk -C $(addsuffix .tex,$(PECAS)) || true
	rm -f $(PDFS) exemplo-*.pdf ./*-comparacao.pdf
	rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz
	rm -f exemplo-*.aux exemplo-*.log exemplo-*.out exemplo-*.fls exemplo-*.fdb_latexmk
	rm -f ./*-comparacao.aux ./*-comparacao.log ./*-comparacao.out ./*-comparacao.fls ./*-comparacao.fdb_latexmk
	rm -f figuras/fontes-dos-exemplos/*.aux figuras/fontes-dos-exemplos/*.log figuras/fontes-dos-exemplos/*.pdf

## ajuda     Mostra esta lista de alvos
ajuda:
	@echo "Alvos disponíveis (use: make <alvo>):"
	@grep -E '^## ' $(firstword $(MAKEFILE_LIST)) | sed -e 's/^## /  /'
