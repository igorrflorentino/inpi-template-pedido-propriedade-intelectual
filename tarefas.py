#!/usr/bin/env python3
"""Tarefas do template: compilar, verificar, gerar e limpar.

É o executor por trás do Makefile (Linux e macOS) e do make.bat (Windows): os
dois só repassam o alvo para cá. Toda a lógica das tarefas mora neste arquivo e
nos três scripts que ele chama, em Python com só a biblioteca padrão, para que
o template funcione do mesmo jeito nos dois sistemas.

Uso:
    make <alvo>                  Linux, macOS e Prompt de Comando do Windows
    .\\make <alvo>                PowerShell
    python3 tarefas.py <alvo>    Linux e macOS, sem o make
    py tarefas.py <alvo>         Windows, sem o make.bat

Sem alvo, compila as quatro peças, como `make`. Vários alvos rodam em sequência
e param no primeiro que falhar (`make limpar pdf`). `make ajuda` lista os alvos.
"""

# POR QUE PYTHON, E NÃO SHELL
#
# O template já foi Makefile mais três scripts em bash, com sed, awk, grep,
# mktemp e seq pelo meio. Nada disso existe num Windows comum, e emular (Git
# Bash, MSYS2, WSL) troca um problema por outro: fim de linha CRLF quebrando o
# bash, página de código trocando os acentos, ferramentas com opções
# diferentes. Python é uma instalação só, roda nativo no PowerShell e no Prompt
# de Comando, e as checagens mais delicadas já eram escritas nele.
#
# A regra que decorre disso: o Makefile e o make.bat NÃO têm receita. O que uma
# tarefa faz está aqui; se estivesse num deles, não existiria no outro sistema.

import glob
import os
import shutil
import subprocess
import sys

if sys.version_info < (3, 8):
    sys.exit('ERRO: o template precisa do Python 3.8 ou mais novo (este é o %d.%d).'
             % sys.version_info[:2])

RAIZ = os.path.dirname(os.path.abspath(__file__))

# As quatro peças do pedido (art. 16 da Portaria/INPI/DIRPA nº 14/2024): cada
# uma é uma raiz LaTeX própria e gera o PDF que se anexa ao peticionamento.
PECAS = ('relatorio-descritivo', 'reivindicacoes', 'desenhos', 'resumo')

# -halt-on-error: erro grave derruba o build em vez de o nonstopmode "se
# recuperar" e entregar um PDF com erro silencioso. Definido uma vez só, aqui,
# e usado por todas as tarefas e pelos três scripts.
LATEXMK = ('latexmk', '-pdf', '-halt-on-error', '-interaction=nonstopmode',
           '-file-line-error')

# Avisos do chktex silenciados (ruído de macros/comentários neste template):
#  1 espaço após comando · 8 traços · 12/36 espaçamento · 24 espaço após \label
#  44 nudge de booktabs
# -I0 impede o chktex de seguir \input/\usepackage: cada arquivo já é passado
# explicitamente, e sem isso ele tenta abrir \input{\macro} e despeja avisos
# que não são do código.
CHKTEX_SILENCIA = ('-I0', '-n1', '-n8', '-n12', '-n24', '-n36', '-n44')
# O .sty vai à parte, com supressões próprias: ali o chktex não resolve
# \input{\macro} (27), lê os "..." das mensagens de erro como reticências (11) e
# trata os artigos citados nas mensagens ("art. 38, I:") como fim de frase
# (13). Nenhum dos três é problema em código de pacote.
CHKTEX_SILENCIA_STY = ('-n11', '-n13', '-n27')


# ---------------------------------------------------------------------------
# Utilidades comuns (usadas também pelos três scripts)
# ---------------------------------------------------------------------------

def sistema():
    """'windows', 'macos' ou 'linux' — para escolher a instrução de instalação."""
    if sys.platform.startswith('win'):
        return 'windows'
    if sys.platform == 'darwin':
        return 'macos'
    return 'linux'


def preparar_terminal():
    """Deixa a saída à prova de acento em qualquer sistema.

    No Windows, com a saída redirecionada (arquivo, pipe, log da CI), o Python
    escreve na página de código do sistema (cp1252), e um caractere fora dela
    derrubaria o script com UnicodeEncodeError no meio do relatório. Fora do
    terminal a saída passa a ser UTF-8; no terminal, o próprio Python já
    escreve em Unicode, e só se troca o erro por '?'.

    O line_buffering garante que cada linha saia na hora, antes da saída dos
    programas chamados (latexmk, chktex), que escrevem direto no terminal —
    sem ele, no log da CI as mensagens do script apareceriam fora de ordem."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            if fluxo.isatty():
                fluxo.reconfigure(errors='replace', line_buffering=True)
            else:
                fluxo.reconfigure(encoding='utf-8', errors='replace',
                                  line_buffering=True)
        except (AttributeError, OSError, ValueError):
            pass


# Como instalar cada programa externo, por sistema. Sai quando o programa não
# está no PATH, no lugar do "command not found" — ou do silêncio, que era o que
# a verificação fazia sem o pdftotext: extraía texto vazio e acusava falhas
# que não existiam.
_LATEX = {
    'linux': 'Instale com (Debian/Ubuntu): sudo apt install latexmk '
             'texlive-latex-extra texlive-fonts-recommended '
             'texlive-lang-portuguese texlive-plain-generic',
    'windows': 'Instale o TeX Live (https://tug.org/texlive/windows.html) ou o '
               'MiKTeX (winget install MiKTeX.MiKTeX). No MiKTeX, o latexmk '
               'precisa também do Perl: winget install StrawberryPerl.StrawberryPerl',
    'macos': 'Instale o MacTeX: https://tug.org/mactex/',
}
_POPPLER = {
    'linux': 'Instale com (Debian/Ubuntu): sudo apt install poppler-utils',
    'windows': 'Instale com: winget install oschwartz10612.Poppler',
    'macos': 'Instale com: brew install poppler',
}
COMO_INSTALAR = {
    'latexmk': _LATEX,
    'chktex': {
        'linux': 'Instale com (Debian/Ubuntu): sudo apt install chktex',
        'windows': 'O chktex vem com o TeX Live e com o MiKTeX: confira se a '
                   'pasta bin da distribuição está no PATH.',
        'macos': 'O chktex vem com o MacTeX.',
    },
    'pdftotext': _POPPLER,
    'pdfinfo': _POPPLER,
    'pdfimages': _POPPLER,
}


def localizar(*programas):
    """Caminho completo de cada programa, na ordem pedida.

    Se faltar algum, explica como instalar e encerra com código 2. O caminho
    completo, e não só o nome, importa no Windows: sem shell, o subprocess só
    acha um .exe pelo nome, e uma distribuição pode trazer o programa como .bat
    ou .cmd. O shutil.which consulta o PATHEXT e acha os três."""
    caminhos = [shutil.which(programa) for programa in programas]
    faltando = [p for p, c in zip(programas, caminhos) if c is None]
    if faltando:
        print('ERRO: não encontrado no PATH: ' + ', '.join(faltando), file=sys.stderr)
        dicas = []
        for programa in faltando:
            dica = COMO_INSTALAR.get(programa, {}).get(sistema())
            if dica and dica not in dicas:
                dicas.append(dica)
        for dica in dicas:
            print('  ' + dica, file=sys.stderr)
        if sistema() == 'windows':
            print('  Depois de instalar, feche e abra de novo o terminal: '
                  'o PATH só é lido na abertura.', file=sys.stderr)
        sys.exit(2)
    return caminhos


def latexmk(*argumentos, stdout=None, stderr=None):
    """Roda o latexmk com as opções do template e devolve o código de saída.

    Os argumentos vão como lista, sem shell: nada de aspas a escapar, nem de
    diferença entre o sh e o cmd.exe na interpretação da linha."""
    comando = localizar('latexmk') + list(LATEXMK[1:]) + list(argumentos)
    return subprocess.call(comando, stdout=stdout, stderr=stderr)


# ---------------------------------------------------------------------------
# Tarefas
# ---------------------------------------------------------------------------

def _mostrar(comando):
    # Ecoa o comando antes de rodá-lo, como o make fazia: quem lê a saída vê o
    # que foi executado e pode repetir à mão.
    print(' '.join(comando))


# QUEM DECIDE SE RECOMPILA É O LATEXMK, NÃO ESTE ARQUIVO.
#
# A tentação é pular a compilação quando o PDF é mais novo que o .tex. Não faça
# isso, nem aqui nem no Makefile: o texto do pedido mora em pedido/**, as
# imagens em figuras/**, e uma lista de dependências escrita à mão esquece os
# dois. O resultado é `make pdf` responder "Nothing to be done" depois de você
# editar o relatório, e o PDF que você anexa ao peticionamento continuar sendo
# o da versão anterior — em silêncio, que é o pior jeito de errar aqui.
#
# O latexmk já rastreia dependência de verdade, pelo .fls que o pdflatex emite:
# ele enxerga todo \input e todo \includegraphics, inclusive os que aparecerem
# depois. Então ele é SEMPRE chamado, e é ele que não faz nada quando nada
# mudou — o custo de uma chamada ociosa é uma fração de segundo.
def compilar(*pecas):
    localizar('latexmk')
    for peca in pecas:
        _mostrar(list(LATEXMK) + [peca + '.tex'])
        codigo = latexmk(peca + '.tex')
        if codigo != 0:
            return codigo
    return 0


def _script(nome, opcoes=()):
    # O mesmo interpretador que roda este arquivo: nada de adivinhar se o
    # sistema chama o Python de python3, python ou py.
    return subprocess.call([sys.executable, os.path.join(RAIZ, nome)] + list(opcoes))


def lint(_opcoes):
    chktex = localizar('chktex')[0]
    # Arquivos de prosa. As quatro raízes entram junto: erro de sintaxe ali
    # derruba as quatro peças de uma vez.
    prosa = (sorted(p.replace(os.sep, '/') for p in glob.glob('pedido/*/*.tex'))
             + ['dados-do-pedido.tex'] + [p + '.tex' for p in PECAS])
    comando = ['chktex', '-q'] + list(CHKTEX_SILENCIA) + prosa
    _mostrar(comando)
    codigo = subprocess.call([chktex] + comando[1:])
    comando = (['chktex', '-q'] + list(CHKTEX_SILENCIA) + list(CHKTEX_SILENCIA_STY)
               + ['lib/inpitex.sty'])
    _mostrar(comando)
    # Os dois rodam sempre: um aviso na prosa não pode esconder os do pacote.
    return subprocess.call([chktex] + comando[1:]) or codigo


def limpar(_opcoes):
    caminho = shutil.which('latexmk')
    if caminho:
        comando = ['latexmk', '-C'] + [p + '.tex' for p in PECAS]
        _mostrar(comando)
        # Falhar aqui não importa: os arquivos são removidos abaixo de todo jeito.
        subprocess.call([caminho] + comando[1:])
    # PDFs compilados, não todo *.pdf: as figuras em PDF de figuras/ são fonte.
    padroes = ([p + '.pdf' for p in PECAS]
               + ['exemplo-*.pdf', '*-comparacao.pdf',
                  '*.aux', '*.log', '*.out', '*.fls', '*.fdb_latexmk', '*.synctex.gz',
                  'figuras/fontes-dos-exemplos/*.aux',
                  'figuras/fontes-dos-exemplos/*.log',
                  'figuras/fontes-dos-exemplos/*.pdf'])
    removidos, presos = 0, []
    for padrao in padroes:
        for arquivo in sorted(glob.glob(padrao)):
            try:
                os.remove(arquivo)
                removidos += 1
            except FileNotFoundError:
                pass
            except OSError:
                presos.append(arquivo.replace(os.sep, '/'))
    print('Removido(s) %d arquivo(s) gerado(s).' % removidos)
    if presos:
        # No Windows, um PDF aberto no Adobe Reader fica travado e não pode ser
        # apagado — nem sobrescrito pela próxima compilação.
        print('ERRO: não foi possível remover: ' + ', '.join(presos), file=sys.stderr)
        print('  Feche esses arquivos no leitor de PDF e rode de novo.', file=sys.stderr)
        return 1
    return 0


def ajuda(_opcoes):
    print('Alvos disponíveis:')
    for nome, _, descricao in ALVOS:
        print('  %-15s%s' % (nome, descricao))
    print()
    if sistema() == 'windows':
        print('Use: make <alvo> no Prompt de Comando, .\\make <alvo> no PowerShell,')
        print('     ou py tarefas.py <alvo> em qualquer terminal.')
    else:
        print('Use: make <alvo>, ou python3 tarefas.py <alvo>.')
    return 0


ALVOS = (
    ('pdf', lambda _: compilar(*PECAS),
     'Compila as quatro peças do pedido (alvo padrão)'),
    ('relatorio', lambda _: compilar('relatorio-descritivo'),
     'Compila só o relatório descritivo'),
    ('reivindicacoes', lambda _: compilar('reivindicacoes'),
     'Compila só as reivindicações'),
    ('desenhos', lambda _: compilar('desenhos'),
     'Compila só o documento de desenhos'),
    ('resumo', lambda _: compilar('resumo'),
     'Compila só o resumo'),
    ('exemplos', lambda _: _script('gerar-exemplos.py'),
     'Gera o showcase dos dois eixos de seleção (invenção, MU, divisão)'),
    ('comparacao', lambda _: _script('gerar-copia-de-comparacao.py'),
     'Gera a cópia de comparação das peças (arts. 51, III e 57, II)'),
    ('verificar', lambda opcoes: _script('verificar-conformidade.py', opcoes),
     'Roda a rede de conformidade normativa (--check-only: só verifica)'),
    ('lint', lint,
     'Análise estática (chktex) da prosa, das raízes e do pacote de estilo'),
    ('limpar', limpar,
     'Remove artefatos de compilação (inclui os PDFs do showcase)'),
    ('ajuda', ajuda,
     'Mostra esta lista de alvos'),
)
TABELA = {nome: tarefa for nome, tarefa, _ in ALVOS}

# Opções aceitas, e o alvo a que cada uma se aplica.
OPCOES = {'--check-only': 'verificar'}


def main(argumentos):
    preparar_terminal()
    os.chdir(RAIZ)
    if any(a in ('-h', '--help') for a in argumentos):
        return ajuda([])
    opcoes = [a for a in argumentos if a.startswith('-')]
    alvos = [a for a in argumentos if not a.startswith('-')] or ['pdf']
    desconhecidos = [a for a in alvos if a not in TABELA]
    if desconhecidos:
        print('ERRO: alvo desconhecido: ' + ', '.join(desconhecidos), file=sys.stderr)
        print('Rode "make ajuda" para ver os alvos.', file=sys.stderr)
        return 2
    for opcao in opcoes:
        dono = OPCOES.get(opcao)
        if dono is None:
            print('ERRO: opção desconhecida: ' + opcao, file=sys.stderr)
            return 2
        if dono not in alvos:
            print('ERRO: a opção %s só vale para o alvo %s' % (opcao, dono),
                  file=sys.stderr)
            return 2
    for alvo in alvos:
        codigo = TABELA[alvo]([o for o in opcoes if OPCOES[o] == alvo])
        if codigo:
            return codigo
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
