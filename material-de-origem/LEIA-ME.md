# Material de origem

É aqui que entra **o que você já tem** sobre a invenção: relatório do projeto,
tese, notas de laboratório, desenhos de CAD, fotos, resultados de ensaio,
apresentações, o que for. É a matéria-prima de onde as quatro peças do pedido
são redigidas.

Nada desta pasta é compilado pelo LaTeX, e **nada dela é versionado** — veja
"Por que o conteúdo não vai para o git", adiante.

## Jogue os arquivos aqui, sem classificar

A pasta é **plana de propósito**. Não tente separar o material por seção do
pedido (descrição, dados, desenhos): seu material não vem separado assim. Um
relatório de projeto costuma trazer, no mesmo arquivo, a descrição do objeto,
os resultados de ensaio e menção a trabalhos anteriores. Classificar isso
obrigaria a duplicar arquivo ou a arquivá-lo errado — e quem vai ler o
documento inteiro de qualquer forma é o agente ou você.

O que ajuda de verdade é **nome de arquivo que diga o que o documento é**:

```
relatorio-final-projeto-irrigacao-2024.pdf      bom
dissertacao-fulano-cap4-ensaios.pdf             bom
doc1.pdf                                        ruim
```

## A única separação: `anterioridades/`

Documentos do estado da técnica — patentes, artigos, catálogos encontrados na
busca — vão em `anterioridades/`. O critério não é "que seção do pedido isso
alimenta", é **de quem é o documento**, e a regra sobre ele é categoricamente
diferente:

- é obra de terceiro;
- **nenhum trecho dele pode ser transportado para o pedido**. Anterioridade se
  cita em prosa, dentro dos parágrafos numerados, pelo número de publicação
  (art. 27, II da Portaria/INPI/DIRPA nº 14/2024): "O documento
  BR 10 2015 000000 0 descreve um conjunto no qual...".

Confundir o que você inventou com o que outro já publicou é o erro mais caro
possível num pedido: põe matéria alheia na sua descrição ou, pior, faz você
reivindicá-la. Por isso essa pasta existe, e por isso ela é a única.

## `NOTAS-PARA-O-AGENTE.md`

Com a pasta plana, esse arquivo é a peça mais importante daqui. É o índice que
**você** escreve: o que é cada documento, o que já está decidido, o que está em
aberto. Há um modelo ao lado deste arquivo — preencha-o antes de acionar o
agente.

## Por que o conteúdo não vai para o git

O `.gitignore` ignora tudo nesta pasta, menos estes dois arquivos de instrução.
Três razões:

1. **Sigilo.** Divulgação antes do depósito destrói a novidade (art. 11 da LPI).
   O período de graça do art. 12 é rede de proteção, não plano — e o art. 11,
   § 2º da Portaria 14/2024 só aceita, para esse fim, divulgação de documentos
   não-patentários. Material que não é versionado não vaza por acidente de
   repositório.
2. **Direito de terceiro.** Os documentos de `anterioridades/` são obra alheia.
3. **Lugar canônico.** O acervo do projeto pertence ao sistema documental da sua
   instituição, não a um repositório de LaTeX.

Se você preferir versionar — repositório privado, tudo num lugar só,
rastreabilidade — é decisão legítima: basta remover as linhas correspondentes do
`.gitignore`. Só que seja decisão, não descuido.
