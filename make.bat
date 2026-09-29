@echo off
rem make.bat - atalhos do template no Windows, equivalentes ao Makefile.
rem
rem     make pdf        no Prompt de Comando (cmd)
rem     .\make pdf      no PowerShell, que so executa arquivo da pasta atual
rem                     com o .\ na frente
rem
rem Rode "make ajuda" para ver os alvos.
rem
rem NAO ESCREVA RECEITA AQUI. Toda a logica esta em tarefas.py, em Python com
rem so a biblioteca padrao, para funcionar igual no Linux e no Windows; este
rem arquivo so acha o Python e repassa os argumentos. Uma receita escrita aqui
rem nao existiria para quem usa o Makefile, e as duas maneiras de compilar
rem passariam a divergir em silencio.
rem
rem Sem acento de proposito: o cmd le o .bat na pagina de codigo do console
rem (850 ou 1252), e nao em UTF-8, e o acento sairia trocado na tela. Pela
rem mesma familia de motivos este arquivo tem fim de linha CRLF, fixado no
rem .gitattributes: com LF o cmd erra rotulos e saltos de forma intermitente.

setlocal
cd /d "%~dp0"

rem Qual Python usar. O "py" (o lancador que o instalador do python.org poe no
rem sistema) vem primeiro. O "python" pode ser o atalho da Microsoft Store, que
rem so abre a loja sem instalar nada: por isso cada candidato e testado
rem rodando de verdade, e nao apenas procurado no PATH.
set "PYTHON="
py -3 -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1 && set "PYTHON=py -3"
if not defined PYTHON python -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1 && set "PYTHON=python"
if not defined PYTHON python3 -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1 && set "PYTHON=python3"
if not defined PYTHON (
    echo ERRO: Python 3.8 ou mais novo nao encontrado. 1>&2
    echo   Instale com: winget install Python.Python.3.12 1>&2
    echo   ou pelo instalador de https://www.python.org/downloads/ 1>&2
    echo   Depois feche e abra de novo o terminal. 1>&2
    exit /b 2
)

%PYTHON% tarefas.py %*
exit /b %ERRORLEVEL%
