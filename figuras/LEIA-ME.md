# Figuras

É aqui que entra a imagem **final**, pronta para o documento de desenhos:
cada arquivo que `desenhos.tex` posiciona e que `pedido/desenhos/figuras.tex`
declara. Nada nesta pasta é rascunho — o que estiver aqui é o que sai no PDF.

## O agente nunca cria a imagem

Regra sem exceção: **o agente de IA não desenha, não gera e não redesenha
nenhuma imagem** para entrar aqui — nem com TikZ, nem com qualquer outra
ferramenta. A figura é sempre trazida por quem está redigindo o pedido (o
depositante, o inventor, o CAD do projeto, um ilustrador contratado), já no
formato exigido pela norma:

- **isenta de texto** (art. 39, I) — só termos indicativos indispensáveis
  ("corte AA", "aberto") e sinais de referência numéricos, nunca frase
  explicativa dentro da figura;
- **sem carimbo, logotipo, letreiro, assinatura ou marca d'água** (art. 21) —
  um print de CAD ou uma foto de protótipo direto da origem quase sempre traz
  algum desses elementos, e por isso não entra aqui sem antes ser limpo.

Faltou a imagem de uma figura de que a redação precisa? **Pare e peça ao
depositante**, do mesmo jeito que faltaria qualquer outro dado técnico — não
se preenche a lacuna com uma imagem gerada para a ocasião.

## Dois tipos de imagem

**Desenho técnico com sinais de referência** — o caso comum: vista, corte,
esquema, diagrama em bloco, fluxograma, com os elementos numerados entre
parênteses. Preencha `sinais-de-referencia.md`, nesta mesma pasta, dizendo
brevemente o que cada número representa — é a partir dali que a frase única
da "Breve descrição dos desenhos" e a explicação detalhada no corpo do
relatório são escritas.

**Fotografia sem identificação de partes** — ensaio, protótipo, resultado
visual, sem sinais de referência marcados. Também é aceita: nesse caso não há
número para mapear, e a "breve descrição" da figura é só uma frase dizendo o
que a imagem mostra, sem inventar sinal que não existe nela.

## Formato, proporção e nome do arquivo

PDF vetorial é o formato do template (é o que `\includegraphics` espera e o
que as figuras de exemplo usam); PNG e JPG também funcionam para fotografia.
Nome descritivo em kebab-case, sem espaço nem acento
(`vista-em-corte-longitudinal.pdf`, não `fig1.pdf`) — é por esse nome, sem
extensão, que `pedido/desenhos/figuras.tex` referencia o arquivo.

**A proporção da imagem importa, e é onde se erra com mais frequência.** O
art. 38, I exige margem esquerda e direita **entre 1,5 cm e 2,5 cm**, e quem ele
mede é a figura, não a caixa de texto. Uma imagem mais alta que larga (a partir
de mais ou menos 1,3:1) passa a ser limitada pela altura da página, encolhe na
horizontal e as margens laterais crescem sozinhas — uma figura em retrato 3:16
sai com mais de 8 cm de cada lado. O `make verificar` **falha** nesse caso, com
a medida em milímetros. As saídas, em ordem de preferência:

1. **girar a imagem para paisagem** — é o que a prática de desenho de patente
   faz, e o INPI aceita a figura deitada na página;
2. **recortar o espaço em branco** em volta do desenho, que costuma ser o
   verdadeiro culpado;
3. **dividir em mais de uma figura**, cada uma com sua numeração;
4. se ela divide a página com outra de propósito (art. 37), passar uma largura
   explícita: `\figura[width=0.45\linewidth]{...}{...}`. Nesse caso a
   conferência de margem não se aplica, porque a disposição é intencional.

## `fontes-dos-exemplos/`

Essa subpasta guarda as fontes TikZ que geram as **duas figuras de
demonstração** deste template (`figura-1-vista-em-corte.pdf` e
`figura-2-fluxograma.pdf`) — existe para o mantenedor do template regenerar o
showcase, não é padrão a seguir num pedido real.

Para regenerar uma delas:

```sh
cd figuras/fontes-dos-exemplos
pdflatex figura-1-vista-em-corte.tex
cp figura-1-vista-em-corte.pdf ..
```

O PDF que vale é o de `figuras/`; o que fica na subpasta é artefato de
compilação, ignorado pelo git e removido por `make limpar`. Num pedido de verdade, as
duas figuras de exemplo saem e esta subpasta some com elas; a imagem que
entra no lugar delas vem de fora, nunca de código escrito durante a redação.
