#!/usr/bin/env bash
#
# Gera um conjunto de PDFs de DEMONSTRAÇÃO para cada combinação relevante dos
# dois eixos de seleção do template, reaproveitando o MESMO conteúdo de pedido/.
# Serve para ver como o template se comporta em cada caso e, principalmente,
# para provar que os dois seletores de dados-do-pedido.tex realmente chaveiam o
# que deveriam — é a razão de este script rodar na CI.
#
# Uso:
#     ./gerar-exemplos.sh
#
# Saída (na raiz do repositório), quatro PDFs por exemplo:
#     exemplo-invencao-*.pdf   natureza=invencao,            modalidade=originario
#     exemplo-mu-*.pdf         natureza=modelo-de-utilidade, modalidade=originario
#     exemplo-divisao-*.pdf    natureza=invencao,            modalidade=divisao
#
# O terceiro exemplo existe para exercitar a menção pós-título exigida pelo
# art. 51, II da Portaria/INPI/DIRPA nº 14/2024 ("Dividido do ___"); a menção do
# art. 43, II (certificado de adição) usa o mesmo caminho de código.
#
# Nenhum arquivo é duplicado: os valores dos seletores são injetados por linha
# de comando, aproveitando os \providecommand de dados-do-pedido.tex.
#
# Requer: latexmk (a mesma cadeia usada para compilar o pedido).
set -euo pipefail

cd "$(dirname "$0")"

PECAS=(relatorio-descritivo reivindicacoes desenhos resumo)

# Cada exemplo é "prefixo|definições TeX injetadas antes do \documentclass".
EXEMPLOS=(
    "exemplo-invencao|\\def\\NaturezaDoPedido{invencao}\\def\\ModalidadeDoPedido{originario}"
    "exemplo-mu|\\def\\NaturezaDoPedido{modelo-de-utilidade}\\def\\ModalidadeDoPedido{originario}\\def\\TituloDoPedido{DISPOSITIVO DE ACIONAMENTO PARA VÁLVULA DE IRRIGAÇÃO}"
    "exemplo-divisao|\\def\\NaturezaDoPedido{invencao}\\def\\ModalidadeDoPedido{divisao}\\def\\PedidoVinculado{BR 10 2024 000000 0}"
)

for exemplo in "${EXEMPLOS[@]}"; do
    prefixo="${exemplo%%|*}"
    injecao="${exemplo#*|}"
    echo ">>> Gerando ${prefixo}-*.pdf"
    for peca in "${PECAS[@]}"; do
        # -halt-on-error (paridade com a CI): erro grave derruba o build em vez
        # de o nonstopmode "se recuperar" e gerar um PDF com erro silencioso.
        latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error \
            -jobname="${prefixo}-${peca}" \
            -pretex="${injecao}" -usepretex \
            "${peca}.tex" > /dev/null
    done
done

echo
echo "Concluído. PDFs gerados:"
ls -1 exemplo-*.pdf
