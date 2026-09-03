# Configuração do latexmk para o template de pedido de patente do INPI.
#
# As quatro peças do pedido são raízes independentes (relatorio-descritivo.tex,
# reivindicacoes.tex, desenhos.tex e resumo.tex), cada uma gerando o seu PDF.
#
# Não há glossário, lista de siglas, índice remissivo nem bibliografia: nenhum
# desses elementos integra um pedido de patente (art. 3º da Portaria/INPI/DIRPA
# nº 14/2024). Por isso não há dependências personalizadas a registrar aqui —
# ao contrário do template ABNT que originou este repositório.

$pdf_mode = 1;          # pdflatex
$out_dir  = '.';

# A paginação n/N depende do \pageref{LastPage} do pacote lastpage, que só
# estabiliza na segunda passada. O latexmk já recompila enquanto houver
# referência pendente; este limite evita laço infinito num caso patológico.
$max_repeat = 5;
