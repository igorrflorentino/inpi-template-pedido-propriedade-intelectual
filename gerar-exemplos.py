#!/usr/bin/env python3
"""Gera PDFs de DEMONSTRAÇÃO para cada combinação relevante dos dois eixos de
seleção do template, reaproveitando o MESMO conteúdo de pedido/.

Serve para ver como o template se comporta em cada caso e, principalmente, para
provar que os dois seletores de dados-do-pedido.tex realmente chaveiam o que
deveriam — é a razão de este script rodar na CI.

Uso:
    make exemplos
    python3 gerar-exemplos.py        (no Windows: py gerar-exemplos.py)

Saída (na raiz do repositório), quatro PDFs por exemplo:
    exemplo-invencao-*.pdf   natureza=invencao,            modalidade=originario
    exemplo-mu-*.pdf         natureza=modelo-de-utilidade, modalidade=originario
    exemplo-divisao-*.pdf    natureza=invencao,            modalidade=divisao

O terceiro exemplo existe para exercitar a menção pós-título exigida pelo art.
51, II da Portaria/INPI/DIRPA nº 14/2024 ("Dividido do ___"); a menção do art.
43, II (certificado de adição) usa o mesmo caminho de código.

Nenhum arquivo é duplicado: os valores dos seletores são injetados por linha de
comando (-pretex do latexmk), aproveitando os \\providecommand de
dados-do-pedido.tex.

Requer: Python 3.8+ e latexmk (a mesma cadeia usada para compilar o pedido).
"""

import glob
import os
import subprocess
import sys

# Sem __pycache__ na pasta do pedido (veja o verificar-conformidade.py).
sys.dont_write_bytecode = True
import tarefas
from tarefas import PECAS

# Cada exemplo é (prefixo, definições TeX injetadas antes do \documentclass).
#
# SÓ ASCII NA INJEÇÃO. Estas definições vão para a linha de comando do latexmk,
# e dali para a do pdflatex. No Windows, argumento com espaço E caractere
# acentuado chega corrompido ao pdflatex: no caminho entre o latexmk (Perl) e o
# pdflatex a linha de comando passa pela página de código do sistema, e o
# próprio latexmk registra o problema no seu código-fonte. Por isso o título
# acentuado vai com os comandos de acento do LaTeX — \'A, \c{C}, \~A —, que
# compõem exatamente os mesmos glifos que "Á", "Ç" e "Ã" digitados em UTF-8.
EXEMPLOS = (
    ('exemplo-invencao',
     r'\def\NaturezaDoPedido{invencao}\def\ModalidadeDoPedido{originario}'),
    ('exemplo-mu',
     r'\def\NaturezaDoPedido{modelo-de-utilidade}\def\ModalidadeDoPedido{originario}'
     r"\def\TituloDoPedido{DISPOSITIVO DE ACIONAMENTO PARA V\'ALVULA DE IRRIGA\c{C}\~AO}"),
    ('exemplo-divisao',
     r'\def\NaturezaDoPedido{invencao}\def\ModalidadeDoPedido{divisao}'
     r'\def\PedidoVinculado{BR 10 2024 000000 0}'),
)


def main():
    tarefas.preparar_terminal()
    os.chdir(tarefas.RAIZ)

    for prefixo, injecao in EXEMPLOS:
        if not injecao.isascii():
            print(f'ERRO: a injeção de {prefixo} tem caractere fora do ASCII. Escreva os '
                  "acentos como comandos do LaTeX (\\'A, \\c{C}, \\~A): no Windows, acento "
                  'na linha de comando chega corrompido ao pdflatex.', file=sys.stderr)
            return 2
    tarefas.localizar('latexmk')

    for prefixo, injecao in EXEMPLOS:
        print(f'>>> Gerando {prefixo}-*.pdf')
        for peca in PECAS:
            # -halt-on-error (paridade com a CI): erro grave derruba o build em
            # vez de o nonstopmode "se recuperar" e gerar um PDF com erro
            # silencioso.
            codigo = tarefas.latexmk(f'-jobname={prefixo}-{peca}',
                                     f'-pretex={injecao}', '-usepretex',
                                     f'{peca}.tex', stdout=subprocess.DEVNULL)
            if codigo != 0:
                print(f'ERRO: {prefixo}-{peca} não compilou (veja {prefixo}-{peca}.log)',
                      file=sys.stderr)
                return codigo

    print()
    print('Concluído. PDFs gerados:')
    for pdf in sorted(glob.glob('exemplo-*.pdf')):
        print(pdf)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
