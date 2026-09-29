# Makefile — atalhos para compilar e verificar o template de pedido de patente
# no Linux e no macOS. No Windows, o make.bat faz o mesmo papel. Rode `make`
# (ou `make ajuda`) para ver os alvos.
#
# NÃO ESCREVA RECEITA AQUI. Toda a lógica está em tarefas.py, em Python com só
# a biblioteca padrão, para funcionar igual no Linux e no Windows; este arquivo
# só repassa o alvo. Uma receita escrita aqui não existiria para quem usa o
# make.bat, e as duas maneiras de compilar passariam a divergir em silêncio.
#
# Todos os alvos são .PHONY e sempre chamam o tarefas.py, que sempre chama o
# latexmk: quem decide se recompila é o latexmk, pelo .fls, e nunca uma lista
# de dependências escrita à mão — ela esqueceria pedido/** e figuras/**, e
# `make pdf` responderia "Nothing to be done" depois de você editar o
# relatório. O porquê completo está em tarefas.py.

# No Windows (GNU make do Git Bash, do MSYS2 ou do Chocolatey) o Python
# costuma se chamar python, e o python3 pode ser só o atalho da Microsoft
# Store. Para outro nome: make PYTHON="py -3" pdf
ifeq ($(OS),Windows_NT)
PYTHON ?= python
else
PYTHON ?= python3
endif

ALVOS := pdf relatorio reivindicacoes desenhos resumo exemplos comparacao \
         verificar lint limpar ajuda

.PHONY: all $(ALVOS)

all: pdf

$(ALVOS):
	@$(PYTHON) tarefas.py $@
