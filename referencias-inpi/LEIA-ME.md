# Referências do INPI

Material de consulta, **somente leitura**. Nada aqui é compilado pelo template.

**Só entra norma em vigor.** Quando uma norma é revogada ou superada, ela é
removida desta pasta em vez de ficar guardada com ressalva — material
desatualizado à mão é convite a decisão errada, ainda mais em matéria em que o
INPI mudou as regras recentemente. Se você encontrar orientação (na internet, em
modelo antigo, em texto de terceiro) apoiada em norma que não está aqui,
desconfie e confira contra a Portaria 14/2024 antes de aplicar.

## `normas/`

| Arquivo | Papel |
| --- | --- |
| `Portaria INPI-DIRPA 14-2024` | **A norma central deste template.** Forma e conteúdo dos pedidos de patente e certificados de adição. É dela que vêm praticamente todas as regras implementadas em `lib/inpitex.sty` e verificadas em `verificar-conformidade.sh`. |
| `Resolucao INPI-PR 124-2013` | Diretrizes de exame — conteúdo do pedido. Orienta a redação (suficiência descritiva, formulação de reivindicações, terminologia); alimenta os comentários-guia dos arquivos de `pedido/`. |
| `Portaria INPI 39-2021` | Entrada na fase nacional de pedidos internacionais (PCT). A forma dos documentos é a mesma da Portaria 14/2024 (art. 65 dela, e art. 9º, § 1º desta). |
| `Portaria INPI 79-2022` | Trâmite prioritário. Procedimental — **não afeta** a forma dos documentos. |

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

## Ao atualizar esta pasta

O INPI revisa seus normativos com alguma frequência. Ao trocar uma norma por
versão mais recente:

1. substitua o PDF e mantenha o nome no mesmo padrão (`<tipo> <número>-<ano> -
   <assunto>.pdf`), sem prefixo de situação;
2. **apague a versão antiga** — não a mantenha "por referência";
3. releia os artigos citados em `lib/inpitex.sty` e em
   `verificar-conformidade.sh`: a numeração dos artigos muda entre normas, e uma
   citação que aponta para o artigo errado é pior do que citação nenhuma;
4. rode `make verificar` e confira se alguma exigência mudou de conteúdo, não só
   de número.
