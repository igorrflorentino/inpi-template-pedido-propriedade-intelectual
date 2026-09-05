#!/usr/bin/env bash
#
# Rede de conformidade normativa do template.
#
# Compila as quatro peças do pedido e AFIRMA, sobre os PDFs gerados, cada
# exigência de forma da Portaria/INPI/DIRPA nº 14/2024 que é verificável
# automaticamente. Cada afirmação cita o artigo que a impõe.
#
# Não substitui a leitura de um profissional: verifica FORMA, não conteúdo.
# Nada aqui diz se a sua invenção é nova, inventiva ou suficientemente descrita
# (arts. 8º, 11, 13, 24 e 25 da LPI) — isso é exame técnico, não conferência.
#
# Uso:
#     ./verificar-conformidade.sh                 compila e verifica
#     ./verificar-conformidade.sh --check-only    só verifica os PDFs atuais
#
# Requer: latexmk e poppler-utils (pdftotext, pdfimages).
#
# Saída: lista de OK / FALHA / AVISO e código de saída 0 (tudo conforme) ou 1
# (alguma falha). AVISO não altera o código de saída.
set -uo pipefail

cd "$(dirname "$0")"

APENAS_VERIFICAR=0
[ "${1:-}" = "--check-only" ] && APENAS_VERIFICAR=1

PECAS=(relatorio-descritivo reivindicacoes desenhos resumo)
FALHAS=0
AVISOS=0

# ---------------------------------------------------------------------------
# Utilidades de relato
# ---------------------------------------------------------------------------
ok()    { printf '  OK     %s\n' "$1"; }
falha() { printf '  FALHA  %s\n' "$1"; FALHAS=$((FALHAS + 1)); }
aviso() { printf '  AVISO  %s\n' "$1"; AVISOS=$((AVISOS + 1)); }
secao() { printf '\n== %s\n' "$1"; }

exigir() {
    # exigir <condição-já-avaliada:0|1> <mensagem>
    if [ "$1" -eq 0 ]; then ok "$2"; else falha "$2"; fi
}

# ---------------------------------------------------------------------------
# Descobre a natureza declarada, para aplicar as regras que dependem dela
# ---------------------------------------------------------------------------
NATUREZA=$(sed -n 's/^[[:space:]]*\\providecommand{\\NaturezaDoPedido}{\([^}]*\)}.*/\1/p' \
    dados-do-pedido.tex | tail -1)
[ -z "$NATUREZA" ] && NATUREZA=invencao

# ---------------------------------------------------------------------------
# Art. 57, I — os documentos do pedido vão "sem qualquer tipo de rasura ou
# sinalização". A cópia de comparação do art. 57, II é documento SEPARADO, que
# acompanha a petição, e se gera com ./gerar-copia-de-comparacao.sh.
#
# Deixar \CopiaDeComparacao{sim} em dados-do-pedido.tex faria os PDFs do pedido
# saírem tachados e sublinhados. Isso aborta a verificação aqui, antes mesmo de
# compilar: é o erro mais caro que este template permitiria cometer, porque o
# documento sairia formalmente inaceitável sem nada parecer errado.
# ---------------------------------------------------------------------------
MODO_COMPARACAO=$(sed -n 's/^[[:space:]]*\\providecommand{\\CopiaDeComparacao}{\([^}]*\)}.*/\1/p' \
    dados-do-pedido.tex | tail -1)
if [ "${MODO_COMPARACAO:-nao}" = "sim" ]; then
    secao "Art. 57, I — documentos do pedido sem sinalização"
    falha "dados-do-pedido.tex está com \\CopiaDeComparacao{sim}: os PDFs do pedido sairiam marcados"
    printf '%s\n' "           Volte o valor para 'nao'. Para gerar a cópia de comparação do"
    printf '%s\n' "           art. 57, II use 'make comparacao', que não altera este arquivo."
    printf '\n%s\n' "Conformidade de forma: 1 FALHA(S)"
    exit 1
fi

# ---------------------------------------------------------------------------
# Compilação
# ---------------------------------------------------------------------------
if [ "$APENAS_VERIFICAR" -eq 0 ]; then
    secao "Compilação das quatro peças"
    for peca in "${PECAS[@]}"; do
        # -halt-on-error é essencial: sob nonstopmode sem ele, um erro grave é
        # SILENCIOSO — o LaTeX "se recupera" e ainda entrega um PDF.
        if latexmk -pdf -halt-on-error -interaction=nonstopmode -file-line-error \
                "$peca.tex" > /dev/null 2>&1; then
            ok "$peca.tex compilou"
        else
            falha "$peca.tex NÃO compilou (rode: latexmk -pdf $peca.tex)"
        fi
    done
fi

for peca in "${PECAS[@]}"; do
    if [ ! -f "$peca.pdf" ]; then
        falha "$peca.pdf não existe — nada a verificar nesta peça"
        FALTA_PDF=1
    fi
done
if [ "${FALTA_PDF:-0}" -eq 1 ]; then
    printf '\n%s\n' "Abortado: gere os PDFs antes de verificar (make pdf)."
    exit 1
fi

# Texto extraído de cada peça, uma vez, reaproveitado pelas checagens.
#
# São gerados DOIS arquivos por peça, porque as checagens têm necessidades
# opostas:
#
#   $peca.txt       extração fiel, com a estrutura de linhas preservada. É o
#                   que as checagens de paginação e de linhas por página usam.
#   $peca.norm.txt  o mesmo texto DES-HIFENIZADO. O LaTeX quebra palavras no
#                   fim da linha e o pdftotext preserva o hífen ("compre-
#                   endendo"), o que fura qualquer busca textual — foi
#                   exatamente o que fazia a contagem de "caracterizado por"
#                   passar batida. Juntar as metades remove uma quebra de
#                   linha, e por isso este arquivo NÃO serve para contar
#                   linhas: as duas checagens ficam em arquivos separados.
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
for peca in "${PECAS[@]}"; do
    pdftotext -layout "$peca.pdf" "$TMP/$peca.txt" 2>/dev/null
    python3 -c '
import re, sys
bruto = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# Junta só dentro da mesma página (nunca através do form feed).
paginas = [re.sub(r"(\w)-\n[ \t]*(\w)", r"\1\2", p) for p in bruto.split("\f")]
open(sys.argv[2], "w", encoding="utf-8").write("\f".join(paginas))
' "$TMP/$peca.txt" "$TMP/$peca.norm.txt"
done

# ---------------------------------------------------------------------------
# Art. 16 — documentos separados, numeração independente, paginação n/N
#           centralizada na margem superior
# ---------------------------------------------------------------------------
secao "Art. 16 — paginação n/N independente por peça"
for peca in "${PECAS[@]}"; do
    total=$(pdfinfo "$peca.pdf" 2>/dev/null | sed -n 's/^Pages:[[:space:]]*//p')
    # A paginação é a primeira linha não-vazia de cada página. O pdftotext
    # separa páginas com form feed (\f).
    encontradas=$(awk -v RS='\f' '{
        for (i = 1; i <= NF; i++) { print $i; break }
    }' "$TMP/$peca.txt" | tr -d ' ')
    esperadas=$(seq 1 "$total" | sed "s|\$|/$total|")
    if [ "$encontradas" = "$esperadas" ]; then
        ok "$peca: $total página(s), numeradas 1/$total .. $total/$total"
    else
        falha "$peca: paginação n/N ausente ou fora de sequência (esperado 1/$total .. $total/$total)"
    fi
done

# ---------------------------------------------------------------------------
# Art. 17 — entre 20 e 35 linhas de texto por página
#
# A última página de cada peça é dispensada do MÍNIMO: ela termina onde o texto
# termina, e a norma visa densidade, não preenchimento artificial. O documento
# de desenhos também fica fora — o art. 17 trata de texto, e os desenhos têm
# regra própria no art. 38.
# ---------------------------------------------------------------------------
secao "Art. 17 — de 20 a 35 linhas de texto por página"
for peca in relatorio-descritivo reivindicacoes resumo; do
    total=$(pdfinfo "$peca.pdf" 2>/dev/null | sed -n 's/^Pages:[[:space:]]*//p')
    problema=0
    pagina=0
    while IFS= read -r n; do
        pagina=$((pagina + 1))
        # Desconta a linha da própria paginação.
        linhas=$((n - 1))
        if [ "$linhas" -gt 35 ]; then
            falha "$peca, página $pagina: $linhas linhas (máximo 35)"
            problema=1
        elif [ "$linhas" -lt 20 ] && [ "$pagina" -ne "$total" ]; then
            falha "$peca, página $pagina: $linhas linhas (mínimo 20)"
            problema=1
        fi
        # Conta as linhas não-vazias de cada página: a primeira, mais uma por
        # quebra de linha seguida de conteúdo.
    done < <(awk -v RS='\f' '{ print gsub(/\n[ \t]*[^ \t\n]/, "&") + 1 }' "$TMP/$peca.txt")
    [ "$problema" -eq 0 ] && ok "$peca: todas as $total página(s) dentro da faixa"
done

# ---------------------------------------------------------------------------
# Arts. 19 e 21 — nenhuma representação gráfica no relatório, nas
#                 reivindicações e no resumo; nenhum timbre ou logotipo
# ---------------------------------------------------------------------------
secao "Arts. 19 e 21 — sem representação gráfica fora do documento de desenhos"
# Duas checagens complementares, porque nenhuma das duas basta sozinha.
#
# (a) NA FONTE. O art. 19 proíbe "representações gráficas" — e isso inclui
#     desenho vetorial, que o pdfimages NÃO vê (ele lista apenas imagens
#     rasterizadas). Uma figura em PDF vetorial, como as deste template,
#     passaria incólume por uma checagem só de PDF. Procurar o comando na
#     fonte pega o caso real (alguém inserir uma figura no texto) e ainda
#     aponta o arquivo e a linha.
# (b) NO PDF. Pega imagem rasterizada que tenha chegado ao PDF por outro
#     caminho, sem um \includegraphics visível nos arquivos de conteúdo.
COMANDOS_GRAFICOS='\\includegraphics|\\figura|\\imprimirdesenhos|\\imprimirdescricaodosdesenhos|begin\{tikzpicture\}|begin\{figure\}'
declare -A FONTES_DA_PECA=(
    [relatorio-descritivo]='pedido/relatorio-descritivo'
    [reivindicacoes]='pedido/reivindicacoes'
    [resumo]='pedido/resumo'
)
for peca in relatorio-descritivo reivindicacoes resumo; do
    achados=$(grep -rnE "$COMANDOS_GRAFICOS" "${FONTES_DA_PECA[$peca]}" 2>/dev/null \
        | grep -v '^[^:]*:[0-9]*:[[:space:]]*%' || true)
    imagens=$(pdfimages -list "$peca.pdf" 2>/dev/null | tail -n +3 | grep -c . || true)
    if [ -z "$achados" ] && [ "$imagens" -eq 0 ]; then
        ok "$peca: nenhuma representação gráfica"
    else
        if [ -n "$achados" ]; then
            falha "$peca: comando gráfico na fonte — o art. 19 não admite figura aqui"
            printf '%s\n' "$achados" | sed 's/^/           /'
        fi
        [ "$imagens" -gt 0 ] && falha "$peca: $imagens imagem(ns) rasterizada(s) no PDF (art. 19)"
    fi
done

# ---------------------------------------------------------------------------
# Art. 24 — título idêntico no relatório e no resumo, com até 500 caracteres
# ---------------------------------------------------------------------------
secao "Art. 24 — título"
# No relatório o título abre a primeira página, logo após a paginação. No resumo
# vem depois da palavra RESUMO. Normalizamos espaços porque a extração de texto
# introduz espaçamento de kerning ("VÁL VULA").
titulo_de() {
    awk -v RS='\f' 'NR == 1 { print }' "$1" \
        | sed -e '1{/^[[:space:]]*[0-9][0-9]*\/[0-9][0-9]*[[:space:]]*$/d}' \
        | sed -e '/^[[:space:]]*RESUMO[[:space:]]*$/d' \
        | awk 'BEGIN { t = "" }
               /^[[:space:]]*$/ { if (t != "") exit; next }
               { t = t " " $0 }
               END { print t }' \
        | tr -s ' \t' ' ' | sed -e 's/^ //' -e 's/ $//' -e 's/ //g'
}
t_rd=$(titulo_de "$TMP/relatorio-descritivo.norm.txt")
t_re=$(titulo_de "$TMP/resumo.norm.txt")
if [ -n "$t_rd" ] && [ "$t_rd" = "$t_re" ]; then
    ok "título idêntico no relatório descritivo e no resumo (art. 24, IV)"
else
    falha "título divergente entre relatório e resumo (art. 24, IV)"
    printf '           relatório: %s\n' "$t_rd"
    printf '           resumo   : %s\n' "$t_re"
fi
n_titulo=$(printf '%s' "$t_rd" | wc -m | tr -d ' ')
if [ "$n_titulo" -le 500 ]; then
    ok "título com $n_titulo caracteres (máximo 500 — art. 24, I)"
else
    falha "título com $n_titulo caracteres, acima do máximo de 500 (art. 24, I)"
fi

# ---------------------------------------------------------------------------
# Art. 26, II — parágrafos do relatório numerados sequencialmente
# ---------------------------------------------------------------------------
secao "Art. 26, II — numeração sequencial dos parágrafos"
rotulos=$(grep -o '\[[0-9]\{1,4\}\]' "$TMP/relatorio-descritivo.norm.txt" \
    | tr -d '[]' | sed 's/^0*//')
n_rotulos=$(printf '%s\n' "$rotulos" | grep -c . || true)
if [ "$n_rotulos" -eq 0 ]; then
    falha "o relatório descritivo não tem nenhum parágrafo numerado — use \\pnum"
else
    esperado=$(seq 1 "$n_rotulos")
    if [ "$rotulos" = "$esperado" ]; then
        ok "$n_rotulos parágrafos, de [001] a [$(printf '%03d' "$n_rotulos")], sem lacuna nem repetição"
    else
        falha "numeração dos parágrafos fora de sequência (esperado 1..$n_rotulos)"
        printf '           obtido: %s\n' "$(printf '%s' "$rotulos" | tr '\n' ' ')"
    fi
fi

# ---------------------------------------------------------------------------
# Arts. 26, III e 39, V — toda figura declarada aparece na listagem do
#                         relatório e no documento de desenhos
# ---------------------------------------------------------------------------
secao "Arts. 26, III e 39, V — congruência das figuras"
n_declaradas=$(grep -c '^[[:space:]]*\\figura' pedido/desenhos/figuras.tex || true)
n_listadas=$(grep -o 'A Figura [0-9]\{1,3\} apresenta' "$TMP/relatorio-descritivo.norm.txt" | wc -l | tr -d ' ')
n_desenhadas=$(grep -c '^[[:space:]]*Figura [0-9]\{1,3\}[[:space:]]*$' "$TMP/desenhos.txt" || true)
if [ "$n_declaradas" -eq "$n_listadas" ] && [ "$n_declaradas" -eq "$n_desenhadas" ]; then
    ok "$n_declaradas figura(s) declarada(s), listada(s) no relatório e desenhada(s)"
else
    falha "figuras incongruentes: $n_declaradas declarada(s), $n_listadas na listagem do relatório, $n_desenhadas no documento de desenhos"
fi

# Art. 22 — desenhos obrigatórios em modelo de utilidade.
if [ "$NATUREZA" = "modelo-de-utilidade" ]; then
    if [ "$n_desenhadas" -ge 1 ]; then
        ok "modelo de utilidade com desenhos (art. 22)"
    else
        falha "modelo de utilidade SEM desenhos — o art. 22 os torna obrigatórios"
    fi
fi

# ---------------------------------------------------------------------------
# Art. 28 — forma das reivindicações
# ---------------------------------------------------------------------------
secao "Art. 28 — forma das reivindicações"
# Extrai o quadro reivindicatório: do cabeçalho em diante, uma reivindicação
# por número no início de linha.
python3 - "$TMP/reivindicacoes.norm.txt" "$NATUREZA" <<'PY'
import re, sys

caminho, natureza = sys.argv[1], sys.argv[2]
texto = open(caminho, encoding='utf-8', errors='replace').read()

# Remove a linha de paginação de cada página e o cabeçalho "REIVINDICAÇÕES".
texto = re.sub(r'(?m)^\s*\d+/\d+\s*$', '', texto)
texto = re.sub(r'(?m)^\s*REIVINDICA\S*\s*$', '', texto)
texto = texto.replace('\f', '\n')

# Junta as quebras de linha internas de cada reivindicação: uma reivindicação
# começa em "N." no início da linha.
partes = re.split(r'(?m)^\s*(\d+)\.\s+', texto)
reivs = []
for i in range(1, len(partes) - 1, 2):
    numero = int(partes[i])
    corpo = ' '.join(partes[i + 1].split())
    reivs.append((numero, corpo))

falhas = 0
def ok(m):    print(f'  OK     {m}')
def falha(m):
    global falhas
    print(f'  FALHA  {m}')
    falhas += 1

if not reivs:
    falha('nenhuma reivindicação encontrada no PDF')
    sys.exit(2)

# Art. 28, I — numeradas consecutivamente em algarismos arábicos.
numeros = [n for n, _ in reivs]
if numeros == list(range(1, len(numeros) + 1)):
    ok(f'{len(numeros)} reivindicação(ões), numeradas consecutivamente de 1 a {len(numeros)}')
else:
    falha(f'numeração não consecutiva: {numeros}')

# Art. 28, II — uma ÚNICA expressão "caracterizado por".
# Art. 28, III — redigida sem interrupção por pontos: um único ponto final.
for numero, corpo in reivs:
    n_carac = len(re.findall(r'caracteriza[dm]\w*\s+p(?:or|elo|ela)', corpo, re.IGNORECASE))
    if n_carac != 1:
        falha(f'reivindicação {numero}: {n_carac} expressões "caracterizado por" (art. 28, II exige exatamente uma)')

    # Desconta o hífen de fim de linha reinserido pela extração e os pontos de
    # numeração de documentos citados; o que importa é o ponto de fim de frase.
    pontos = re.findall(r'\.(?=\s|$)', corpo)
    if len(pontos) != 1 or not corpo.rstrip().endswith('.'):
        falha(f'reivindicação {numero}: {len(pontos)} ponto(s) final(is) (art. 28, III exige um único, ao final)')

if falhas == 0:
    ok('cada reivindicação com uma única expressão "caracterizado por" e um único ponto final')

# Art. 33 — em modelo de utilidade, uma ÚNICA reivindicação independente.
independentes = [n for n, c in reivs
                 if not re.search(r'de acordo com (?:a|as) reivindica', c, re.IGNORECASE)]
if natureza == 'modelo-de-utilidade':
    if len(independentes) == 1:
        ok('modelo de utilidade com uma única reivindicação independente (art. 33)')
    else:
        falha(f'modelo de utilidade com {len(independentes)} reivindicações independentes '
              f'({independentes}) — o art. 33 admite uma única')
else:
    ok(f'{len(independentes)} reivindicação(ões) independente(s): {independentes}')

sys.exit(1 if falhas else 0)
PY
[ $? -ne 0 ] && FALHAS=$((FALHAS + 1))

# ---------------------------------------------------------------------------
# Art. 40 — resumo: 50 a 200 palavras, não excedendo uma página
# ---------------------------------------------------------------------------
secao "Art. 40 — extensão do resumo"
paginas_resumo=$(pdfinfo resumo.pdf 2>/dev/null | sed -n 's/^Pages:[[:space:]]*//p')
if [ "$paginas_resumo" -eq 1 ]; then
    ok "resumo em uma página (art. 40, II)"
else
    falha "resumo com $paginas_resumo páginas — o art. 40, II admite no máximo uma"
fi
# Conta as palavras do corpo, descontando a paginação, o cabeçalho e o título.
palavras=$(sed -e '/^[[:space:]]*[0-9][0-9]*\/[0-9][0-9]*[[:space:]]*$/d' \
               -e '/^[[:space:]]*RESUMO[[:space:]]*$/d' "$TMP/resumo.norm.txt" \
    | awk 'BEGIN { corpo = 0 }
           corpo == 0 && /^[[:space:]]*$/ { vazias++; if (vazias >= 1 && titulo) corpo = 1; next }
           corpo == 0 { titulo = 1; next }
           { print }' | wc -w | tr -d ' ')
if [ "$palavras" -ge 50 ] && [ "$palavras" -le 200 ]; then
    ok "resumo com $palavras palavras (faixa preferencial de 50 a 200 — art. 40, II)"
else
    # Advisory de propósito: o art. 40, II pede "preferencialmente entre 50 e
    # 200 palavras". Só o "não exceder uma página" é imperativo, e esse é
    # checado acima.
    aviso "resumo com $palavras palavras, fora da faixa preferencial de 50 a 200 (art. 40, II)"
fi

# ---------------------------------------------------------------------------
# ADVISORY — congruência dos sinais de referência
#
# Art. 29, VIII e art. 32, III; Resolução INPI/PR nº 124/2013, itens 2.27 a
# 2.29 e 4.01: os sinais de referência devem ser uniformes em todo o pedido, e
# o relatório e os desenhos devem ser consistentes entre si.
#
# É heurística de fonte, por isso NÃO bloqueia: o script compara os sinais
# "(N)" citados no relatório e nas reivindicações com os declarados do lado
# das figuras. Ele não vê o interior das imagens — se um sinal está desenhado
# na figura mas não citado do lado das figuras, aparece aqui como aviso a
# conferir à mão.
#
# "Declarados do lado das figuras" soma DUAS fontes: pedido/desenhos/
# figuras.tex (a frase única de cada figura, que só cita o sinal mais
# relevante — art. 27, V pede descrição breve) e, se existir,
# figuras/sinais-de-referencia.md (o glossário completo de sinais que o
# depositante preenche, sem o limite de brevidade da frase impressa no PDF).
# Some as duas: nenhuma das duas sozinha é obrigada a listar todo sinal.
# ---------------------------------------------------------------------------
secao "Sinais de referência (advisory)"
sinais_texto=$(grep -oh '([0-9]\{1,3\})' "$TMP/relatorio-descritivo.norm.txt" "$TMP/reivindicacoes.norm.txt" \
    | tr -d '()' | sort -un)
fontes_sinais_figuras=(pedido/desenhos/figuras.tex)
[ -f figuras/sinais-de-referencia.md ] && fontes_sinais_figuras+=(figuras/sinais-de-referencia.md)
sinais_figuras=$(grep -oh '([0-9]\{1,3\})' "${fontes_sinais_figuras[@]}" \
    | tr -d '()' | sort -un)
so_no_texto=$(comm -23 <(printf '%s\n' "$sinais_texto") <(printf '%s\n' "$sinais_figuras") | grep -c . || true)
so_nas_figuras=$(comm -13 <(printf '%s\n' "$sinais_texto") <(printf '%s\n' "$sinais_figuras") | grep -c . || true)
if [ "$so_no_texto" -eq 0 ] && [ "$so_nas_figuras" -eq 0 ]; then
    ok "os sinais de referência do texto e do lado das figuras coincidem"
else
    [ "$so_no_texto" -gt 0 ] && aviso "sinais citados no texto e ausentes do lado das figuras: $(comm -23 <(printf '%s\n' "$sinais_texto") <(printf '%s\n' "$sinais_figuras") | tr '\n' ' ')"
    [ "$so_nas_figuras" -gt 0 ] && aviso "sinais do lado das figuras e ausentes do texto: $(comm -13 <(printf '%s\n' "$sinais_texto") <(printf '%s\n' "$sinais_figuras") | tr '\n' ' ')"
fi

# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------
printf '\n%s\n' "----------------------------------------------------------------"
if [ "$FALHAS" -eq 0 ]; then
    printf 'Conformidade de forma: OK'
    [ "$AVISOS" -gt 0 ] && printf ' (%d aviso[s] a conferir)' "$AVISOS"
    printf '\n'
    printf '%s\n' "Lembre-se: isto verifica FORMA. Conteúdo e patenteabilidade são exame técnico."
    exit 0
else
    printf 'Conformidade de forma: %d FALHA(S)\n' "$FALHAS"
    exit 1
fi
