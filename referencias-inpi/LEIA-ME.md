# Referências do INPI

Material de consulta, **somente leitura**. Nada aqui é compilado pelo template.

## `normas/`

Os arquivos são prefixados por situação, para que ninguém use por engano uma
norma revogada.

| Arquivo | Papel |
| --- | --- |
| `VIGENTE - Portaria INPI-DIRPA 14-2024` | **A norma central deste template.** Forma e conteúdo dos pedidos de patente e certificados de adição. É dela que vêm praticamente todas as regras implementadas em `lib/inpitex.sty` e verificadas em `verificar-conformidade.sh`. |
| `VIGENTE - Resolucao INPI-PR 124-2013` | Diretrizes de exame — conteúdo do pedido. Orienta a redação (suficiência descritiva, formulação de reivindicações, terminologia); alimenta os comentários-guia dos arquivos de `pedido/`. |
| `VIGENTE - Portaria INPI 39-2021` | Entrada na fase nacional de pedidos internacionais (PCT). A forma dos documentos é a mesma da Portaria 14/2024 (art. 65 dela, e art. 9º, § 1º desta). |
| `VIGENTE - Portaria INPI 79-2022` | Trâmite prioritário. Procedimental — **não afeta** a forma dos documentos. |
| `REVOGADA - IN INPI-PR 30-2013` | **Revogada** pelo art. 66 da Portaria 14/2024. |
| `REVOGADA - IN INPI-PR 31-2013` | **Revogada** pelo art. 66 da Portaria 14/2024. |

As duas instruções normativas ficam aqui apenas como referência histórica: eram
elas que disciplinavam a forma dos pedidos até 2024, e é comum encontrar
orientação antiga na internet que ainda as cita. **Não devem guiar decisão
alguma neste repositório.**

Quando este repositório cita um artigo sem indicar a norma, trata-se da
Portaria/INPI/DIRPA nº 14/2024. "LPI" é a Lei de Propriedade Industrial
(Lei nº 9.279/1996).

## `formularios-oficiais/`

Os oito modelos `.docx` do e-Patentes 4.0 (Rev. 1) publicados pelo INPI, quatro
para invenção e quatro para modelo de utilidade. Serviram de referência para o
template em três aspectos:

- **estrutura das seções** do relatório descritivo, que reproduz a ordem dos
  incisos I a VIII do art. 27;
- **tipografia**: Arial, com 16 pt no título do pedido, 14 pt nos títulos de
  seção e 12 pt no corpo, entrelinha 1,5, e o recuo pendente de 0,63 cm do
  rótulo de parágrafo. O template usa Helvetica, equivalente métrica livre da
  Arial;
- **texto-guia**: as orientações dos formulários foram reescritas como
  comentários nos arquivos de `pedido/`, com o artigo correspondente.

Vale notar que os formulários numeram os parágrafos com um dígito (`[1]`),
enquanto o art. 26, II exemplifica com três (`[003]`). As duas formas atendem à
norma; o template adota três dígitos por padrão e permite trocar em
`dados-do-pedido.tex`.
