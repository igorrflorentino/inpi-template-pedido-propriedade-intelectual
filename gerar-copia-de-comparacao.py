#!/usr/bin/env python3
"""Gera a CÓPIA DE COMPARAÇÃO das peças do pedido, exigida pelo art. 57, II da
Portaria/INPI/DIRPA nº 14/2024 (e, para o quadro reivindicatório do pedido
dividido, pelo art. 51, III): o mesmo texto do pedido, com marcação de TACHADO
indicando remoção e SUBLINHADO indicando inclusão ou substituição.

Uso:
    make comparacao
    python3 gerar-copia-de-comparacao.py   (no Windows: py gerar-copia-de-comparacao.py)

Saída (na raiz do repositório):
    relatorio-descritivo-comparacao.pdf
    reivindicacoes-comparacao.pdf
    desenhos-comparacao.pdf
    resumo-comparacao.pdf

Estes PDFs acompanham a petição; NÃO são os documentos do pedido. Os documentos
do pedido são os gerados por `make pdf`, que saem sem sinalização alguma, como
exige o art. 57, I. Os dois vêm da mesma fonte: as macros \\removido,
\\incluido e \\substituido imprimem a marca aqui e nada (ou texto limpo) lá.

O modo é injetado por linha de comando, sobre o \\providecommand de
dados-do-pedido.tex — assim o arquivo não precisa ser editado, e não há risco
de anexar ao peticionamento a versão marcada.

Requer: Python 3.8+ e latexmk (a mesma cadeia usada para compilar o pedido).
"""

import glob
import os
import re
import subprocess
import sys

# Sem __pycache__ na pasta do pedido (veja o verificar-conformidade.py).
sys.dont_write_bytecode = True
import tarefas
from tarefas import PECAS


def main():
    tarefas.preparar_terminal()
    os.chdir(tarefas.RAIZ)
    tarefas.localizar('latexmk')

    for peca in PECAS:
        print(f'>>> Gerando {peca}-comparacao.pdf')
        codigo = tarefas.latexmk(f'-jobname={peca}-comparacao',
                                 r'-pretex=\def\CopiaDeComparacao{sim}', '-usepretex',
                                 f'{peca}.tex', stdout=subprocess.DEVNULL)
        if codigo != 0:
            print(f'ERRO: {peca}-comparacao não compilou (veja {peca}-comparacao.log)',
                  file=sys.stderr)
            return codigo

    # A cópia de comparação também é peça que acompanha a petição, então também
    # não pode sair com texto por cima da margem. E ela é mais suscetível que o
    # documento do pedido: o ulem não hifeniza o que está dentro de \sout e
    # \uline, de modo que um trecho marcado no fim da linha pode não ter onde
    # quebrar. O lib/inpitex já afrouxa o espacejamento no modo comparação para
    # evitar isso; esta conferência existe para o caso em que a folga não
    # bastar.
    #
    # O verificar-conformidade.py cuida das quatro peças do pedido; estes PDFs
    # são gerados aqui e é aqui que se conferem.
    transbordou = False
    for peca in PECAS:
        log = f'{peca}-comparacao.log'
        if not os.path.isfile(log):
            continue
        with open(log, encoding='utf-8', errors='replace') as arquivo:
            texto = arquivo.read()
        for linha in re.findall(r'Overfull \\[hv]box \([0-9.]*pt too [a-z]*\)', texto):
            print(f'AVISO: {peca}-comparacao: {linha}', file=sys.stderr)
            transbordou = True

    print()
    print('Concluído. Cópias de comparação geradas:')
    for pdf in sorted(glob.glob('*-comparacao.pdf')):
        print(pdf)
    if transbordou:
        print()
        print('ATENÇÃO: alguma linha transbordou a caixa de texto (avisos acima).')
        print('Confira os PDFs antes de anexar: texto fora da margem é defeito de forma.')
    print()
    print('Lembre-se: estes arquivos acompanham a petição (art. 57, II).')
    print("Os documentos do pedido são os de 'make pdf', sem sinalização (art. 57, I).")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
