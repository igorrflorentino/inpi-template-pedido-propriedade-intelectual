#!/usr/bin/env bash
#
# Gera a CÓPIA DE COMPARAÇÃO das peças do pedido, exigida pelo art. 57, II da
# Portaria/INPI/DIRPA nº 14/2024 (e, para o quadro reivindicatório do pedido
# dividido, pelo art. 51, III): o mesmo texto do pedido, com marcação de
# TACHADO indicando remoção e SUBLINHADO indicando inclusão ou substituição.
#
# Uso:
#     ./gerar-copia-de-comparacao.sh
#
# Saída (na raiz do repositório):
#     relatorio-descritivo-comparacao.pdf
#     reivindicacoes-comparacao.pdf
#     desenhos-comparacao.pdf
#     resumo-comparacao.pdf
#
# Estes PDFs acompanham a petição; NÃO são os documentos do pedido. Os
# documentos do pedido são os gerados por `make pdf`, que saem sem sinalização
# alguma, como exige o art. 57, I. Os dois vêm da mesma fonte: as macros
# \removido, \incluido e \substituido imprimem a marca aqui e nada (ou texto
# limpo) lá.
#
# O modo é injetado por linha de comando, sobre o \providecommand de
# dados-do-pedido.tex — assim o arquivo não precisa ser editado, e não há risco
# de anexar ao peticionamento a versão marcada.
#
# Requer: latexmk (a mesma cadeia usada para compilar o pedido).
set -euo pipefail

cd "$(dirname "$0")"

PECAS=(relatorio-descritivo reivindicacoes desenhos resumo)

for peca in "${PECAS[@]}"; do
    echo ">>> Gerando ${peca}-comparacao.pdf"
    latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error \
        -jobname="${peca}-comparacao" \
        -pretex="\\def\\CopiaDeComparacao{sim}" -usepretex \
        "${peca}.tex" > /dev/null
done

# A cópia de comparação também é peça que acompanha a petição, então também não
# pode sair com texto por cima da margem. E ela é mais suscetível que o
# documento do pedido: o ulem não hifeniza o que está dentro de \sout e \uline,
# de modo que um trecho marcado no fim da linha pode não ter onde quebrar. O
# lib/inpitex já afrouxa o espacejamento no modo comparação para evitar isso;
# esta conferência existe para o caso em que a folga não bastar.
#
# O verificar-conformidade.sh cuida das quatro peças do pedido; estes PDFs são
# gerados aqui e é aqui que se conferem.
TRANSBORDOU=0
for peca in "${PECAS[@]}"; do
    log="${peca}-comparacao.log"
    [ -f "$log" ] || continue
    while IFS= read -r linha; do
        printf 'AVISO: %s-comparacao: %s\n' "$peca" "$linha" >&2
        TRANSBORDOU=1
    done < <(grep -o 'Overfull \\[hv]box ([0-9.]*pt too [a-z]*)' "$log" || true)
done

echo
echo "Concluído. Cópias de comparação geradas:"
ls -1 ./*-comparacao.pdf
if [ "$TRANSBORDOU" -eq 1 ]; then
    echo
    echo "ATENÇÃO: alguma linha transbordou a caixa de texto (avisos acima)."
    echo "Confira os PDFs antes de anexar: texto fora da margem é defeito de forma."
fi
echo
echo "Lembre-se: estes arquivos acompanham a petição (art. 57, II)."
echo "Os documentos do pedido são os de 'make pdf', sem sinalização (art. 57, I)."
