#!/usr/bin/env bash
#
# Gera um PDF de DEMONSTRAÇÃO para cada tipo de documento do template (e o
# subtipo corporativo 'probatorio'), reaproveitando todo o conteúdo de main.tex.
# Útil para ter uma visão completa de como o template se comporta em cada modo,
# sem afetar a compilação normal do main.tex.
#
# Uso:
#     ./gerar-exemplos.sh
#
# Saída (na raiz do repositório):
#     exemplo-academico.pdf    — modo academico (tese, ABNT completo)
#     exemplo-publicacao.pdf   — modo publicacao (série Embrapa: boletim)
#     exemplo-corporativo.pdf  — modo corporativo (análise empresarial)
#     exemplo-probatorio.pdf   — corporativo/probatorio (comprovação de período probatório)
#
# Requer: latexmk (mesma cadeia usada para compilar o main.tex).
set -euo pipefail

# Roda a partir da pasta deste script (raiz do repositório), para que os
# caminhos relativos do main.tex (lib/, elementos-*/, figuras/) resolvam.
cd "$(dirname "$0")"

exemplos=(exemplo-academico exemplo-publicacao exemplo-corporativo exemplo-probatorio)

for exemplo in "${exemplos[@]}"; do
    echo ">>> Gerando ${exemplo}.pdf"
    # -halt-on-error (paridade com a CI): faz erros graves derrubarem o build em
    # vez de o nonstopmode "se recuperar" e gerar um PDF com erro silencioso.
    latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error "${exemplo}.tex"
done

echo
echo "Concluído: ${exemplos[*]/%/.pdf}"
