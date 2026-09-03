# Makefile — atalhos para compilar e verificar o template de pedido de patente.
# Requer latexmk (compilação) e, para `make lint`, chktex — ambos vêm no
# TeX Live. Rode `make` (ou `make ajuda`) para ver os alvos.

.PHONY: all pdf relatorio reivindicacoes desenhos resumo exemplos verificar lint limpar ajuda

# As quatro peças do pedido (art. 16 da Portaria/INPI/DIRPA nº 14/2024): cada
# uma é uma raiz LaTeX própria e gera o PDF que se anexa ao peticionamento.
PECAS := relatorio-descritivo reivindicacoes desenhos resumo
PDFS  := $(addsuffix .pdf,$(PECAS))

# Arquivos de prosa para o lint.
FONTES_PROSA := pedido/*/*.tex dados-do-pedido.tex
# Avisos do chktex silenciados (ruído de macros/comentários neste template):
#  1 espaço após comando · 8 traços · 12/36 espaçamento · 24 espaço após \label
#  44 nudge de booktabs
CHKTEX_SILENCIA := -n1 -n8 -n12 -n24 -n36 -n44

# -halt-on-error: erro grave derruba o build em vez de o nonstopmode "se
# recuperar" e entregar um PDF com erro silencioso.
LATEXMK := latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error

all: pdf

## pdf       Compila as quatro peças do pedido
pdf: $(PDFS)

%.pdf: %.tex dados-do-pedido.tex lib/inpitex.sty
	$(LATEXMK) $<

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

## verificar Roda a rede de conformidade normativa sobre os PDFs gerados
verificar:
	bash verificar-conformidade.sh

## lint      Análise estática (chktex) dos arquivos de prosa
lint:
	chktex -q $(CHKTEX_SILENCIA) $(FONTES_PROSA)

## limpar    Remove artefatos de compilação (inclui os PDFs do showcase)
limpar:
	latexmk -C $(addsuffix .tex,$(PECAS)) || true
	rm -f $(PDFS) exemplo-*.pdf
	rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.synctex.gz
	rm -f exemplo-*.aux exemplo-*.log exemplo-*.out exemplo-*.fls exemplo-*.fdb_latexmk

## ajuda     Mostra esta lista de alvos
ajuda:
	@echo "Alvos disponíveis (use: make <alvo>):"
	@grep -E '^## ' $(firstword $(MAKEFILE_LIST)) | sed -e 's/^## /  /'
