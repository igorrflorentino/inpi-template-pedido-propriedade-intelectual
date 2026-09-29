#!/usr/bin/env python3
"""Rede de conformidade normativa do template.

Compila as quatro peças do pedido e AFIRMA, sobre os PDFs gerados, cada
exigência de forma da Portaria/INPI/DIRPA nº 14/2024 que é verificável
automaticamente. Cada afirmação cita o artigo que a impõe.

Não substitui a leitura de um profissional: verifica FORMA, não conteúdo. Nada
aqui diz se a sua invenção é nova, inventiva ou suficientemente descrita (arts.
8º, 11, 13, 24 e 25 da LPI) — isso é exame técnico, não conferência.

Uso:
    make verificar                                    compila e verifica
    python3 verificar-conformidade.py                 idem, sem o make
    python3 verificar-conformidade.py --check-only    só verifica os PDFs atuais

(No Windows, "py" no lugar de "python3", ou .\\make verificar no PowerShell.)

Requer: Python 3.8+, latexmk e o poppler (pdftotext, pdfinfo, pdfimages).

Saída: lista de OK / FALHA / AVISO e código de saída 0 (tudo conforme), 1
(alguma falha) ou 2 (não deu para verificar: uso incorreto ou programa
ausente). AVISO não altera o código de saída.
"""

import os
import re
import subprocess
import sys

# Sem __pycache__ na pasta do pedido: o import abaixo compilaria o tarefas.py e
# deixaria a pasta de cache ao lado dos .tex, ruído para quem só redige o pedido.
sys.dont_write_bytecode = True
import tarefas
from tarefas import PECAS

# O [[:space:]] do POSIX, sem a quebra de linha. Explícito, e não \s, porque o
# \s do Python casa também espaços Unicode (U+00A0, U+2009...) e a checagem
# mudaria de comportamento conforme o que o pdftotext extraísse.
ESPACO = r'[ \t\r\f\v]'

FALHAS = 0
AVISOS = 0


# ---------------------------------------------------------------------------
# Utilidades de relato
# ---------------------------------------------------------------------------
def ok(mensagem):
    print('  OK     ' + mensagem)


def falha(mensagem):
    global FALHAS
    print('  FALHA  ' + mensagem)
    FALHAS += 1


def aviso(mensagem):
    global AVISOS
    print('  AVISO  ' + mensagem)
    AVISOS += 1


def secao(titulo):
    print('\n== ' + titulo)


def detalhe(texto):
    # Linha de apoio sob uma FALHA, recuada para alinhar com a mensagem.
    print('           ' + texto)


def relatar(achados):
    # As checagens mais longas devolvem pares (nível, mensagem) em vez de
    # imprimir direto, e a contagem sai daqui. Imprimir de dentro delas já fez
    # o rodapé anunciar "1 FALHA(S)" com duas falhas relatadas logo acima.
    for nivel, mensagem in achados:
        {'OK': ok, 'AVISO': aviso}.get(nivel, falha)(mensagem)


# ---------------------------------------------------------------------------
# Leitura de arquivos e de PDFs
# ---------------------------------------------------------------------------
def ler(caminho):
    # Sempre com encoding explícito: sem ele o Python usa a página de código do
    # sistema — cp1252 no Windows — e todo acento viraria outro caractere. O
    # modo texto já converte CRLF em LF, então o arquivo pode ter vindo com o
    # fim de linha do Windows.
    with open(caminho, encoding='utf-8', errors='replace') as arquivo:
        return arquivo.read()


def linhas_de(texto):
    # As linhas como o sed e o grep as veem: o \n final encerra a última linha,
    # não abre uma linha vazia depois dela.
    linhas = texto.split('\n')
    if linhas and linhas[-1] == '':
        linhas.pop()
    return linhas


def paginas_de(texto):
    # As páginas do texto extraído. O pdftotext encerra CADA página com um \f,
    # inclusive a última: o \f final fecha a última página, não abre uma vazia.
    paginas = texto.split('\f')
    if paginas and paginas[-1] == '':
        paginas.pop()
    return paginas


def campos(texto):
    # Palavras separadas por espaço, tabulação ou quebra de linha — só essas.
    return re.findall(r'[^ \t\n]+', texto)


def rodar(comando):
    # Saída padrão de um programa, em texto com fim de linha Unix, ou None se
    # ele falhar.
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if resultado.returncode != 0:
        return None
    return resultado.stdout.decode('utf-8', errors='replace').replace('\r\n', '\n')


def valor_declarado(fonte, macro):
    # Último valor de \providecommand{\<macro>}{<valor>} em início de linha.
    # Linha comentada não casa: o % não é espaço.
    valores = re.findall(r'(?m)^' + ESPACO + r'*\\providecommand\{\\' + macro
                         + r'\}\{([^}\n]*)\}', fonte)
    return valores[-1] if valores else ''


# ---------------------------------------------------------------------------
# Transbordamento de caixa — matéria que a fonte tem e o PDF não
#
# Esta é a checagem mais importante do script, e a menos óbvia. O LaTeX trata
# transbordamento como AVISO, não como erro: o -halt-on-error não pega, o
# latexmk devolve status 0 e o PDF sai "com sucesso". Só que:
#
#   Overfull \vbox   material empurrado para FORA da página. Uma tabela mais
#                    alta que a página perde as linhas excedentes — elas
#                    simplesmente não existem no PDF que você anexa ao
#                    peticionamento. Matéria escrita e não entregue é o erro
#                    mais caro que este template poderia deixar passar.
#   Overfull \hbox   tinta impressa fora da caixa de texto, por cima da margem.
#
# Por isso é FALHA aqui, e não aviso. Abaixo de 2 pt (0,7 mm) o excesso é
# invisível na página impressa e vira apenas AVISO, para o script não implicar
# com o que ninguém enxerga.
#
# Os .log vêm da compilação: no modo --check-only são os do build anterior (na
# CI, os que a latex-action deixou). Sem o .log a checagem não roda e diz isso.
# ---------------------------------------------------------------------------
def analisar_log(texto, peca):
    # "Overfull \vbox (774.38286pt too high) has occurred while \output is active"
    # "Overfull \hbox (56.44218pt too wide) in paragraph at lines 57--66"
    graves, leves = [], []
    for m in re.finditer(r'Overfull \\([hv])box \(([0-9.]+)pt too (?:wide|high)\)(.*)', texto):
        tipo, excesso, onde = m.group(1), float(m.group(2)), m.group(3).strip()
        onde = re.sub(r'\s+', ' ', onde)[:70]
        if tipo == 'v' or excesso > 2.0:
            graves.append((tipo, excesso, onde))
        else:
            leves.append((tipo, excesso, onde))

    achados = []
    for tipo, excesso, onde in graves:
        causa = ('matéria empurrada para fora da página'
                 if tipo == 'v' else 'texto impresso fora da margem')
        achados.append(('FALHA', f'{peca}: Overfull \\{tipo}box de {excesso:.1f}pt — {causa} {onde}'))
    for tipo, excesso, onde in leves:
        achados.append(('AVISO', f'{peca}: Overfull \\{tipo}box de {excesso:.1f}pt (menos de 2pt) {onde}'))

    # O próprio pacote de estilo reclama, no .log, de figura cuja margem lateral
    # sai da faixa do art. 38, I. É a única checagem que precisa medir a figura
    # COMPOSTA, coisa que só o TeX sabe fazer — daqui só dá para colher o aviso
    # e promovê-lo a falha, que é o peso que a norma lhe dá.
    # O bloco vai até a primeira linha em branco. Não dá para juntar linha a
    # linha pelo prefixo "(inpitex)": o pdflatex quebra a saída em 79 colunas,
    # e a continuação de uma linha longa vem sem prefixo nenhum — foi o que
    # truncava a mensagem em "84 mm de margem l".
    #
    # São DUAS quebras diferentes e elas não podem ser tratadas do mesmo jeito:
    # a de \MessageBreak vem como "\n(inpitex)   " e vale um espaço; a do
    # max_print_line corta a linha em 79 colunas SEM espaço nenhum, no meio da
    # palavra, e tem de ser costurada sem inserir nada — senão a mensagem sai
    # com "margem l ateral".
    avisos_pacote = []
    for m in re.finditer(r'Package inpitex Warning: (Art\. 38.*?)(?=\n[ \t]*\n)',
                         texto, re.S):
        limpo = re.sub(r'\n\(inpitex\)[ \t]*', ' ', m.group(1))
        limpo = limpo.replace('\n', '')
        limpo = re.sub(r'[ \t]+', ' ', limpo).strip()
        limpo = re.sub(r'\s*on input line \d+\.?$', '', limpo)
        avisos_pacote.append(limpo)
    for limpo in avisos_pacote:
        achados.append(('FALHA', f'{peca}: {limpo}'))

    if not graves and not leves and not avisos_pacote:
        achados.append(('OK', f'{peca}: nenhuma caixa transbordada e nenhuma figura fora da margem'))
    return achados


# Sem os padrões de hifenização do português no formato do LaTeX, o babel
# segue compondo — só avisa no .log e hifeniza com os padrões de outra língua,
# quebrando palavra onde o português não quebra. Nada falha e o PDF parece
# normal; é exatamente o tipo de diferença entre duas máquinas que ninguém nota
# a olho. Acontece em instalação enxuta — por exemplo, num MiKTeX com o
# português desmarcado nas línguas. Aviso, não falha: a norma não trata de
# hifenização, mas uma quebra errada em peça jurídica é defeito que se evita.
SEM_HIFENIZACAO = 'No hyphenation patterns were preloaded'


# ---------------------------------------------------------------------------
# Art. 24 — título
# ---------------------------------------------------------------------------
def titulo_de(texto_norm):
    # No relatório o título abre a primeira página, logo após a paginação. No
    # resumo vem depois da palavra RESUMO. Juntam-se as linhas até a primeira
    # em branco e tiram-se TODOS os espaços, porque a extração de texto
    # introduz espaçamento de kerning ("VÁL VULA").
    paginas = paginas_de(texto_norm)
    if not paginas:
        return ''
    linhas = linhas_de(paginas[0] + '\n')
    if linhas and re.match(ESPACO + r'*[0-9]+/[0-9]+' + ESPACO + r'*$', linhas[0]):
        linhas = linhas[1:]
    linhas = [l for l in linhas if not re.match(ESPACO + r'*RESUMO' + ESPACO + r'*$', l)]
    titulo = ''
    for linha in linhas:
        if re.match(ESPACO + r'*$', linha):
            if titulo:
                break
            continue
        titulo += ' ' + linha
    return re.sub(r'[ \t]', '', titulo)


def caracteres_do_titulo(caminho):
    # O LIMITE DE 500 CARACTERES SE MEDE NA FONTE, NÃO NO PDF.
    #
    # A comparação do art. 24, IV usa o texto extraído do PDF sem espaço
    # nenhum, porque o pdftotext inventa espaço de kerning ("VÁL VULA") e sem
    # isso a igualdade nunca fecharia. Só que essa mesma string não serve para
    # CONTAR: um título de 505 caracteres perde uns 65 espaços e passa como 439.
    #
    # O art. 24, I mede o título como ele foi escrito, e ele é escrito uma vez
    # só, em dados-do-pedido.tex. É de lá que a contagem sai, em caracteres
    # Unicode — len() de str conta caracteres, não bytes, em qualquer sistema e
    # em qualquer locale: "VÁLVULA" tem 7.
    fonte = ler(caminho)
    marca = r'\providecommand{\TituloDoPedido}{'
    i = fonte.find(marca)
    if i < 0:
        return -1
    # Fecha as chaves contando profundidade: o título pode ocupar várias linhas.
    j, nivel = i + len(marca), 1
    while j < len(fonte) and nivel:
        if fonte[j] == '{':
            nivel += 1
        elif fonte[j] == '}':
            nivel -= 1
        j += 1
    titulo = fonte[i + len(marca):j - 1]
    # A quebra de linha da fonte vira um espaço no documento composto.
    return len(re.sub(r'\s+', ' ', titulo).strip())


# ---------------------------------------------------------------------------
# Art. 28 — forma das reivindicações
# ---------------------------------------------------------------------------
def analisar_reivindicacoes(texto, natureza):
    # Extrai o quadro reivindicatório: do cabeçalho em diante, uma
    # reivindicação por número no início de linha.
    #
    # Remove a linha de paginação de cada página e o cabeçalho "REIVINDICAÇÕES".
    texto = re.sub(r'(?m)^\s*\d+/\d+\s*$', '', texto)
    texto = re.sub(r'(?m)^\s*REIVINDICA\S*\s*$', '', texto)
    texto = texto.replace('\f', '\n')

    # Junta as quebras de linha internas de cada reivindicação: uma
    # reivindicação começa em "N." no início da linha.
    partes = re.split(r'(?m)^\s*(\d+)\.\s+', texto)
    reivs = []
    for i in range(1, len(partes) - 1, 2):
        numero = int(partes[i])
        corpo = ' '.join(partes[i + 1].split())
        reivs.append((numero, corpo))

    achados = []
    falhas = 0

    def registrar_falha(mensagem):
        nonlocal falhas
        achados.append(('FALHA', mensagem))
        falhas += 1

    if not reivs:
        registrar_falha('nenhuma reivindicação encontrada no PDF')
        return achados

    # Art. 28, I — numeradas consecutivamente em algarismos arábicos.
    numeros = [n for n, _ in reivs]
    if numeros == list(range(1, len(numeros) + 1)):
        achados.append(('OK', f'{len(numeros)} reivindicação(ões), numeradas consecutivamente de 1 a {len(numeros)}'))
    else:
        registrar_falha(f'numeração não consecutiva: {numeros}')

    # Art. 28, II — uma ÚNICA expressão "caracterizado por".
    # Art. 28, III — redigida sem interrupção por pontos: um único ponto final.
    for numero, corpo in reivs:
        n_carac = len(re.findall(r'caracteriza[dm]\w*\s+p(?:or|elo|ela)', corpo, re.IGNORECASE))
        if n_carac != 1:
            registrar_falha(f'reivindicação {numero}: {n_carac} expressões "caracterizado por" (art. 28, II exige exatamente uma)')

        # Desconta o hífen de fim de linha reinserido pela extração e os pontos
        # de numeração de documentos citados; o que importa é o ponto de fim de
        # frase.
        pontos = re.findall(r'\.(?=\s|$)', corpo)
        if len(pontos) != 1 or not corpo.rstrip().endswith('.'):
            registrar_falha(f'reivindicação {numero}: {len(pontos)} ponto(s) final(is) (art. 28, III exige um único, ao final)')

    if falhas == 0:
        achados.append(('OK', 'cada reivindicação com uma única expressão "caracterizado por" e um único ponto final'))

    # Art. 33 — em modelo de utilidade, uma ÚNICA reivindicação independente.
    independentes = [n for n, c in reivs
                     if not re.search(r'de acordo com (?:a|as) reivindica', c, re.IGNORECASE)]
    if natureza == 'modelo-de-utilidade':
        if len(independentes) == 1:
            achados.append(('OK', 'modelo de utilidade com uma única reivindicação independente (art. 33)'))
        else:
            registrar_falha(f'modelo de utilidade com {len(independentes)} reivindicações independentes '
                            f'({independentes}) — o art. 33 admite uma única')
    else:
        achados.append(('OK', f'{len(independentes)} reivindicação(ões) independente(s): {independentes}'))
    return achados


# ---------------------------------------------------------------------------
# ADVISORY — congruência dos sinais de referência
#
# Art. 29, VIII e art. 32, III; Resolução INPI/PR nº 124/2013, itens 2.27 a
# 2.29 e 4.01: os sinais de referência devem ser uniformes em todo o pedido, e
# o relatório e os desenhos devem ser consistentes entre si.
#
# É heurística de fonte, por isso NÃO bloqueia: o script não vê o interior das
# imagens. O que ele consegue conferir é o triângulo
#
#   texto (relatório + reivindicações)  ×  frase de cada figura em
#   pedido/desenhos/figuras.tex  ×  glossário figuras/sinais-de-referencia.md,
#
# no qual o glossário é a ÚNICA fonte que sabe em que figura cada sinal está
# desenhado — por isso ele declara isso explicitamente:
#
#     - (4) haste de acionamento — Figuras 1, 2
#     - (9) assento de vedação — Figura 1
#
# O "— Figuras N" não é enfeite: é a declaração de quem abriu a imagem e
# conferiu. Sem ela o script só saberia que o sinal foi mencionado em algum
# lugar, que é exatamente o buraco que deixava passar sinal citado no texto e
# desenhado em figura nenhuma.
#
# Os sinais se comparam como CONJUNTOS DE INTEIROS, com set(), nunca como texto
# ordenado. Em ordem de texto o 10 vem antes do 2, e basta um sinal de dois
# dígitos — o caso normal num pedido real — para uma comparação de listas
# ordenadas desalinhar e acusar como ausente um sinal presente nos dois lados.
# Foi o que acontecia quando esta checagem era feita com `sort -un` e `comm`.
# ---------------------------------------------------------------------------
def analisar_sinais(texto_rd, texto_re, arquivo_figuras, arquivo_glossario):
    def le(caminho):
        if not os.path.exists(caminho):
            return ''
        return ler(caminho)

    def sem_comentarios(fonte):
        # Comentário LaTeX: de um '%' não escapado até o fim da linha. Sem isto
        # o bloco-guia no topo de figuras.tex, que cita \figura quatro vezes
        # para explicar o uso, contaria como quatro figuras declaradas.
        return re.sub(r'(?m)(?<!\\)%.*$', '', fonte)

    def sinais(texto):
        return {int(n) for n in re.findall(r'\((\d{1,3})\)', texto)}

    no_texto = sinais(texto_rd) | sinais(texto_re)
    fonte_figuras = sem_comentarios(le(arquivo_figuras))
    nas_frases = sinais(fonte_figuras)

    # Glossário: "- (4) haste de acionamento — Figuras 1, 2" ou "... — Figura 1".
    # O travessão pode ser em, en ou hífen duplo, porque quem preenche é humano.
    glossario, sem_figura = {}, set()
    for linha in le(arquivo_glossario).splitlines():
        m = re.match(r'\s*[-*]\s*\((\d{1,3})\)\s*(.*)', linha)
        if not m:
            continue
        sinal, resto = int(m.group(1)), m.group(2)
        figs = set()
        corte = re.split(r'\s(?:—|–|--)\s', resto, maxsplit=1)
        if len(corte) == 2:
            figs = {int(n) for n in re.findall(r'\d{1,3}', corte[1])}
        glossario[sinal] = figs
        if not figs:
            sem_figura.add(sinal)

    # Quantas figuras existem de fato, para pegar remissão a figura inexistente.
    n_figuras = len(re.findall(r'\\figura\b', fonte_figuras))

    declarados = set(glossario) | nas_frases

    achados = []

    faltando = sorted(no_texto - declarados)
    if faltando:
        achados.append(('AVISO', 'sinais citados no texto e não declarados do lado das figuras: '
                        + ' '.join(f'({n})' for n in faltando)))

    sobrando = sorted(declarados - no_texto)
    if sobrando:
        achados.append(('AVISO', 'sinais declarados do lado das figuras e nunca citados no texto: '
                        + ' '.join(f'({n})' for n in sobrando)))

    if glossario:
        orfaos = sorted(sem_figura & no_texto)
        if orfaos:
            achados.append(('AVISO', 'sinais citados no texto e que o glossário não localiza em '
                            'nenhuma figura: ' + ' '.join(f'({n})' for n in orfaos)
                            + ' — confira a imagem e complete o "— Figuras N" em '
                              'figuras/sinais-de-referencia.md'))

        inexistentes = sorted({f for figs in glossario.values() for f in figs
                               if n_figuras and (f < 1 or f > n_figuras)})
        if inexistentes:
            achados.append(('AVISO', 'o glossário remete a figura que não existe: '
                            + ' '.join(f'Figura {f}' for f in inexistentes)
                            + f' (há {n_figuras} figura(s) declarada(s))'))

        nao_catalogados = sorted(no_texto - set(glossario))
        if nao_catalogados:
            achados.append(('AVISO', 'sinais citados no texto e ausentes do glossário: '
                            + ' '.join(f'({n})' for n in nao_catalogados)))
    else:
        achados.append(('AVISO', 'figuras/sinais-de-referencia.md não tem nenhum sinal declarado — '
                        'sem ele não dá para conferir em que figura cada sinal aparece'))

    if not achados:
        achados.append(('OK', 'os %d sinais de referência do texto estão declarados e '
                        'localizados em figura' % len(no_texto)))
    return achados


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main(argumentos):
    tarefas.preparar_terminal()
    os.chdir(tarefas.RAIZ)

    if not argumentos:
        apenas_verificar = False
    elif argumentos == ['--check-only']:
        apenas_verificar = True
    else:
        print('Uso: verificar-conformidade.py [--check-only]', file=sys.stderr)
        print('  sem argumento   compila as quatro peças e verifica', file=sys.stderr)
        print('  --check-only    verifica os PDFs já existentes', file=sys.stderr)
        return 2

    dados = ler('dados-do-pedido.tex')

    # -----------------------------------------------------------------------
    # Descobre a natureza declarada, para aplicar as regras que dependem dela
    # -----------------------------------------------------------------------
    natureza = valor_declarado(dados, 'NaturezaDoPedido') or 'invencao'

    # -----------------------------------------------------------------------
    # Art. 57, I — os documentos do pedido vão "sem qualquer tipo de rasura ou
    # sinalização". A cópia de comparação do art. 57, II é documento SEPARADO,
    # que acompanha a petição, e se gera com make comparacao.
    #
    # Deixar \CopiaDeComparacao{sim} em dados-do-pedido.tex faria os PDFs do
    # pedido saírem tachados e sublinhados. Isso aborta a verificação aqui,
    # antes mesmo de compilar: é o erro mais caro que este template permitiria
    # cometer, porque o documento sairia formalmente inaceitável sem nada
    # parecer errado.
    # -----------------------------------------------------------------------
    if (valor_declarado(dados, 'CopiaDeComparacao') or 'nao') == 'sim':
        secao('Art. 57, I — documentos do pedido sem sinalização')
        falha('dados-do-pedido.tex está com \\CopiaDeComparacao{sim}: os PDFs do pedido sairiam marcados')
        detalhe("Volte o valor para 'nao'. Para gerar a cópia de comparação do")
        detalhe("art. 57, II use 'make comparacao', que não altera este arquivo.")
        print('\nConformidade de forma: 1 FALHA(S)')
        return 1

    # Sem o poppler, cada checagem abaixo leria texto vazio e acusaria falhas
    # que não existem. Melhor parar aqui, dizendo o que instalar.
    programas = ('pdftotext', 'pdfinfo', 'pdfimages') + (() if apenas_verificar else ('latexmk',))
    pdftotext, pdfinfo, pdfimages = tarefas.localizar(*programas)[:3]

    # -----------------------------------------------------------------------
    # Compilação
    # -----------------------------------------------------------------------
    if not apenas_verificar:
        secao('Compilação das quatro peças')
        for peca in PECAS:
            # -halt-on-error é essencial: sob nonstopmode sem ele, um erro grave
            # é SILENCIOSO — o LaTeX "se recupera" e ainda entrega um PDF.
            codigo = tarefas.latexmk(peca + '.tex', stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
            if codigo == 0:
                ok(f'{peca}.tex compilou')
            else:
                falha(f'{peca}.tex NÃO compilou (rode: latexmk -pdf {peca}.tex)')

    falta_pdf = False
    for peca in PECAS:
        if not os.path.isfile(peca + '.pdf'):
            falha(f'{peca}.pdf não existe — nada a verificar nesta peça')
            falta_pdf = True
    if falta_pdf:
        print('\nAbortado: gere os PDFs antes de verificar (make pdf).')
        return 1

    secao('Transbordamento e margens — matéria fora da página ou fora da caixa')
    sem_hifenizacao = False
    for peca in PECAS:
        if not os.path.isfile(peca + '.log'):
            aviso(f'{peca}.log não existe — transbordamento não verificado (rode sem --check-only)')
            continue
        log = ler(peca + '.log')
        relatar(analisar_log(log, peca))
        sem_hifenizacao = sem_hifenizacao or SEM_HIFENIZACAO in log
    if sem_hifenizacao:
        aviso('o LaTeX não tem os padrões de hifenização do português e hifenizou o texto '
              'com os de outra língua (aviso do babel no .log) — veja "Hifenização do '
              'português" no README')

    # Texto extraído de cada peça, uma vez, reaproveitado pelas checagens.
    #
    # São DUAS versões do texto de cada peça, porque as checagens têm
    # necessidades opostas:
    #
    #   texto[peca]  extração fiel, com a estrutura de linhas preservada. É o
    #                que as checagens de paginação e de linhas por página usam.
    #   norm[peca]   o mesmo texto DES-HIFENIZADO. O LaTeX quebra palavras no
    #                fim da linha e o pdftotext preserva o hífen ("compre-
    #                endendo"), o que fura qualquer busca textual — foi
    #                exatamente o que fazia a contagem de "caracterizado por"
    #                passar batida. Juntar as metades remove uma quebra de
    #                linha, e por isso esta versão NÃO serve para contar
    #                linhas: as duas checagens ficam em textos separados.
    #
    # O pdftotext é chamado com -enc UTF-8 e -eol unix, e a saída é lida já com
    # CRLF convertido: o padrão do poppler no Windows é o fim de linha DOS, e um
    # \r sobrando no fim de cada linha fura toda expressão que procura o fim da
    # linha — a paginação "1/5\r" deixa de ser "1/5".
    texto, norm, paginas = {}, {}, {}
    for peca in PECAS:
        extraido = rodar([pdftotext, '-layout', '-enc', 'UTF-8', '-eol', 'unix',
                          peca + '.pdf', '-'])
        if extraido is None:
            falha(f'{peca}: o pdftotext não conseguiu extrair o texto do PDF')
            extraido = ''
        texto[peca] = extraido
        # Junta só dentro da mesma página (nunca através do form feed).
        norm[peca] = '\f'.join(re.sub(r'(\w)-\n[ \t]*(\w)', r'\1\2', p)
                               for p in extraido.split('\f'))
        info = rodar([pdfinfo, peca + '.pdf']) or ''
        m = re.search(r'(?m)^Pages:[ \t]*(\d+)', info)
        paginas[peca] = int(m.group(1)) if m else 0

    # -----------------------------------------------------------------------
    # Art. 16 — documentos separados, numeração independente, paginação n/N
    #           centralizada na margem superior
    # -----------------------------------------------------------------------
    secao('Art. 16 — paginação n/N independente por peça')
    for peca in PECAS:
        total = paginas[peca]
        # A paginação é a primeira palavra de cada página.
        encontradas = [campos(p)[0] for p in paginas_de(texto[peca]) if campos(p)]
        esperadas = [f'{n}/{total}' for n in range(1, total + 1)]
        if total and encontradas == esperadas:
            ok(f'{peca}: {total} página(s), numeradas 1/{total} .. {total}/{total}')
        else:
            falha(f'{peca}: paginação n/N ausente ou fora de sequência (esperado 1/{total} .. {total}/{total})')

    # -----------------------------------------------------------------------
    # Art. 17 — entre 20 e 35 linhas de texto por página
    #
    # A última página de cada peça é dispensada do MÍNIMO: ela termina onde o
    # texto termina, e a norma visa densidade, não preenchimento artificial. O
    # documento de desenhos também fica fora — o art. 17 trata de texto, e os
    # desenhos têm regra própria no art. 38.
    # -----------------------------------------------------------------------
    secao('Art. 17 — de 20 a 35 linhas de texto por página')
    for peca in ('relatorio-descritivo', 'reivindicacoes', 'resumo'):
        total = paginas[peca]
        problema = False
        for pagina, conteudo in enumerate(paginas_de(texto[peca]), 1):
            # Conta as linhas não-vazias da página: a primeira, mais uma por
            # quebra de linha seguida de conteúdo.
            n = len(re.findall(r'\n[ \t]*[^ \t\n]', conteudo)) + 1
            # Desconta a linha da própria paginação.
            linhas = n - 1
            if linhas > 35:
                falha(f'{peca}, página {pagina}: {linhas} linhas (máximo 35)')
                problema = True
            elif linhas < 20 and pagina != total:
                falha(f'{peca}, página {pagina}: {linhas} linhas (mínimo 20)')
                problema = True
        if not problema:
            ok(f'{peca}: todas as {total} página(s) dentro da faixa')

    # -----------------------------------------------------------------------
    # Arts. 19 e 21 — nenhuma representação gráfica no relatório, nas
    #                 reivindicações e no resumo; nenhum timbre ou logotipo
    # -----------------------------------------------------------------------
    secao('Arts. 19 e 21 — sem representação gráfica fora do documento de desenhos')
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
    #
    # \imprimirdescricaodosdesenhos NÃO entra nesta lista, embora tenha
    # "desenhos" no nome: ela imprime a listagem textual dos arts. 26, III e
    # 27, V, sem nenhuma imagem. Chamá-la de comando gráfico era acusar de
    # violar o art. 19 justamente a macro que existe para cumpri-lo.
    comandos_graficos = re.compile(
        r'\\includegraphics|\\figura\b|\\imprimirdesenhos|begin\{tikzpicture\}|begin\{figure\}')
    fontes_da_peca = {
        'relatorio-descritivo': 'pedido/relatorio-descritivo',
        'reivindicacoes': 'pedido/reivindicacoes',
        'resumo': 'pedido/resumo',
    }
    for peca in ('relatorio-descritivo', 'reivindicacoes', 'resumo'):
        achados = []
        for raiz, pastas, arquivos in os.walk(fontes_da_peca[peca]):
            pastas.sort()
            for nome in sorted(arquivos):
                caminho = os.path.join(raiz, nome)
                with open(caminho, 'rb') as arquivo:
                    bruto = arquivo.read()
                if b'\0' in bruto:
                    continue    # arquivo binário: não é fonte
                exibido = caminho.replace(os.sep, '/')
                for numero, linha in enumerate(linhas_de(bruto.decode('utf-8', 'replace')), 1):
                    linha = linha.rstrip('\r')
                    # Linha comentada não conta: é o bloco-guia de cada arquivo.
                    if comandos_graficos.search(linha) and not re.match(ESPACO + '*%', linha):
                        achados.append(f'{exibido}:{numero}:{linha}')
        lista = rodar([pdfimages, '-list', peca + '.pdf'])
        if lista is None:
            falha(f'{peca}: o pdfimages não conseguiu ler o PDF')
            lista = ''
        # As duas primeiras linhas são o cabeçalho da tabela.
        imagens = sum(1 for linha in linhas_de(lista)[2:] if linha)
        if not achados and imagens == 0:
            ok(f'{peca}: nenhuma representação gráfica')
        else:
            if achados:
                falha(f'{peca}: comando gráfico na fonte — o art. 19 não admite figura aqui')
                for achado in achados:
                    detalhe(achado)
            if imagens > 0:
                falha(f'{peca}: {imagens} imagem(ns) rasterizada(s) no PDF (art. 19)')

    # -----------------------------------------------------------------------
    # Art. 24 — título idêntico no relatório e no resumo, com até 500 caracteres
    # -----------------------------------------------------------------------
    secao('Art. 24 — título')
    t_rd = titulo_de(norm['relatorio-descritivo'])
    t_re = titulo_de(norm['resumo'])
    if t_rd and t_rd == t_re:
        ok('título idêntico no relatório descritivo e no resumo (art. 24, IV)')
    else:
        falha('título divergente entre relatório e resumo (art. 24, IV)')
        detalhe('relatório: ' + t_rd)
        detalhe('resumo   : ' + t_re)
    n_titulo = caracteres_do_titulo('dados-do-pedido.tex')
    if n_titulo < 0:
        aviso('não foi possível ler \\TituloDoPedido em dados-do-pedido.tex — limite do art. 24, I não verificado')
    elif n_titulo <= 500:
        ok(f'título com {n_titulo} caracteres (máximo 500 — art. 24, I)')
    else:
        falha(f'título com {n_titulo} caracteres, acima do máximo de 500 (art. 24, I)')

    # -----------------------------------------------------------------------
    # Art. 26, II — parágrafos do relatório numerados sequencialmente
    # -----------------------------------------------------------------------
    secao('Art. 26, II — numeração sequencial dos parágrafos')
    rotulos = [re.sub(r'^0*', '', r[1:-1])
               for r in re.findall(r'\[[0-9]{1,4}\]', norm['relatorio-descritivo'])]
    # Um rótulo [000] vira vazio: não conta como parágrafo, mas desalinha a
    # sequência e aparece no "obtido". Vazios só no fim não desalinham nada.
    while rotulos and rotulos[-1] == '':
        rotulos.pop()
    n_rotulos = sum(1 for r in rotulos if r)
    if n_rotulos == 0:
        falha('o relatório descritivo não tem nenhum parágrafo numerado — use \\pnum')
    elif rotulos == [str(n) for n in range(1, n_rotulos + 1)]:
        ok(f'{n_rotulos} parágrafos, de [001] a [{n_rotulos:03d}], sem lacuna nem repetição')
    else:
        falha(f'numeração dos parágrafos fora de sequência (esperado 1..{n_rotulos})')
        detalhe('obtido: ' + ' '.join(rotulos))

    # -----------------------------------------------------------------------
    # Arts. 26, III e 39, V — toda figura declarada aparece na listagem do
    #                         relatório e no documento de desenhos
    # -----------------------------------------------------------------------
    secao('Arts. 26, III e 39, V — congruência das figuras')
    # Conta CHAMADAS de \figura, não linhas: contar linhas pegaria
    # "\figura{a}{..} \figura{b}{..}" na mesma linha como uma só, e a
    # congruência acusaria falha fantasma. Os comentários saem antes, senão o
    # bloco-guia do topo do arquivo — que cita \figura para explicar o uso —
    # entraria na conta.
    n_declaradas = 0
    for linha in linhas_de(ler('pedido/desenhos/figuras.tex')):
        linha = re.sub(r'([^\\])%.*$', r'\1', linha, count=1)
        linha = re.sub(r'^%.*$', '', linha)
        n_declaradas += len(re.findall(r'\\figura\b', linha))
    n_listadas = len(re.findall(r'A Figura [0-9]{1,3} apresenta', norm['relatorio-descritivo']))
    n_desenhadas = sum(1 for linha in linhas_de(texto['desenhos'])
                       if re.match(ESPACO + r'*Figura [0-9]{1,3}' + ESPACO + r'*$', linha))
    if n_declaradas == n_listadas == n_desenhadas:
        ok(f'{n_declaradas} figura(s) declarada(s), listada(s) no relatório e desenhada(s)')
    else:
        falha(f'figuras incongruentes: {n_declaradas} declarada(s), {n_listadas} na listagem '
              f'do relatório, {n_desenhadas} no documento de desenhos')

    # Art. 22 — desenhos obrigatórios em modelo de utilidade.
    if natureza == 'modelo-de-utilidade':
        if n_desenhadas >= 1:
            ok('modelo de utilidade com desenhos (art. 22)')
        else:
            falha('modelo de utilidade SEM desenhos — o art. 22 os torna obrigatórios')

    # -----------------------------------------------------------------------
    # Art. 28 — forma das reivindicações
    # -----------------------------------------------------------------------
    secao('Art. 28 — forma das reivindicações')
    relatar(analisar_reivindicacoes(norm['reivindicacoes'], natureza))

    # -----------------------------------------------------------------------
    # Art. 40 — resumo: 50 a 200 palavras, não excedendo uma página
    # -----------------------------------------------------------------------
    secao('Art. 40 — extensão do resumo')
    if paginas['resumo'] == 1:
        ok('resumo em uma página (art. 40, II)')
    else:
        falha(f'resumo com {paginas["resumo"]} páginas — o art. 40, II admite no máximo uma')
    # Conta as palavras do corpo, descontando a paginação, o cabeçalho e o
    # título: o corpo começa depois da primeira linha em branco que segue o
    # título.
    paginacao = re.compile(ESPACO + r'*[0-9]+/[0-9]+' + ESPACO + r'*$')
    cabecalho = re.compile(ESPACO + r'*RESUMO' + ESPACO + r'*$')
    em_branco = re.compile(ESPACO + r'*$')
    corpo, viu_titulo, palavras = False, False, 0
    for linha in linhas_de(norm['resumo']):
        if paginacao.match(linha) or cabecalho.match(linha):
            continue
        if not corpo:
            if em_branco.match(linha):
                corpo = viu_titulo
            else:
                viu_titulo = True
            continue
        palavras += len(re.findall(r'[^ \t\n\r\f\v]+', linha))
    if 50 <= palavras <= 200:
        ok(f'resumo com {palavras} palavras (faixa preferencial de 50 a 200 — art. 40, II)')
    else:
        # Advisory de propósito: o art. 40, II pede "preferencialmente entre 50
        # e 200 palavras". Só o "não exceder uma página" é imperativo, e esse é
        # checado acima.
        aviso(f'resumo com {palavras} palavras, fora da faixa preferencial de 50 a 200 (art. 40, II)')

    secao('Sinais de referência (advisory)')
    relatar(analisar_sinais(norm['relatorio-descritivo'], norm['reivindicacoes'],
                            'pedido/desenhos/figuras.tex', 'figuras/sinais-de-referencia.md'))

    # -----------------------------------------------------------------------
    # Resultado
    # -----------------------------------------------------------------------
    print('\n----------------------------------------------------------------')
    if FALHAS == 0:
        resumo = 'Conformidade de forma: OK'
        if AVISOS > 0:
            resumo += ' (%d aviso[s] a conferir)' % AVISOS
        print(resumo)
        print('Lembre-se: isto verifica FORMA. Conteúdo e patenteabilidade são exame técnico.')
        return 0
    print('Conformidade de forma: %d FALHA(S)' % FALHAS)
    return 1


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
