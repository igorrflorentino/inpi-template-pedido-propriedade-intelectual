# Material de origem

É aqui que entra **o que você já tem** sobre a invenção: relatório do projeto,
tese, notas de laboratório, desenhos de CAD, fotos, resultados de ensaio,
apresentações, o que for. É a matéria-prima de onde as quatro peças do pedido
são redigidas.

Nada desta pasta é compilado pelo LaTeX, e nada dela é versionado **por
padrão** — veja "Versionar ou não o conteúdo: a decisão", adiante.

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

Esse arquivo **não é o índice do material**. Quem lê os arquivos e conclui o que
cada um é, pelo título e pelo conteúdo, é o agente — inventário escrito à mão é
trabalho que ele faz melhor, e que envelhece a cada arquivo novo que você joga
aqui. O fluxo é o inverso: o agente inventaria a pasta e devolve o inventário
para você conferir antes de redigir.

O que fica no arquivo é só o que **nenhuma leitura recupera**, e o essencial é
uma coisa: **o que não usar**. Nada dentro do `relatorio.pdf` diz que o
`relatorio-v2.pdf` o substituiu; nada no capítulo de ensaios avisa que aquela
série não se confirmou depois. Junte a isso o que já está decidido (natureza,
modalidade, título, categorias) e o que você sabe que ainda falta. Há um modelo
ao lado deste arquivo.

## Versionar ou não o conteúdo: a decisão

Por **padrão** o `.gitignore` ignora tudo nesta pasta, menos os dois arquivos de
instrução. É o padrão seguro, para proteger quem não pensou no assunto. Mas é
uma decisão a tomar, e há um caso legítimo para invertê-la.

### O caso para versionar

Repositório do pedido **privado**, equipe usando o repositório como **fonte
única** dos dados do pedido. Aí o argumento de sigilo praticamente cai: o
art. 11 da LPI fala do que foi "tornado acessível ao público", e repositório
privado com acesso controlado não é isso. Compartilhamento interno na equipe do
projeto não é divulgação pública. E ter tudo em um lugar só costuma valer mais
do que a arrumação teórica de manter o acervo em outro sistema.

Para versionar, **comente o BLOCO A** do `.gitignore` (as cinco linhas
marcadas). Mantenha o BLOCO B.

### O risco que sobra, e ele não é sobre hoje

**Histórico de git é permanente e visibilidade é um botão.** Se o repositório
virar público algum dia — por engano, por mudança de política, por alguém achar
que "já publicou mesmo" —, tudo o que já foi commitado aparece, **inclusive
arquivo apagado depois**: `git rm` não remove do histórico.

A assimetria decide: versionar e nunca publicar não custa nada; versionar e
publicar por engano antes do depósito custa a patente.

### As condições de quem versiona

1. **Decida antes do primeiro commit.** Retroagir exige reescrever histórico,
   operação chata e fácil de fazer pela metade.
2. **Escreva no README do repositório do pedido que ele nunca vira público.** É
   barato, e é o que protege contra o sucessor que não participou da decisão.
3. **Para publicar algo um dia** — depois da concessão, por exemplo — crie um
   repositório **novo** com o que deve ser público. Nunca virando o botão deste.
4. **Derive do template por "Use this template", não por fork.** O template cria
   repositório **sem histórico**; o fork carrega histórico e vínculo.
5. **A lista de quem tem acesso é a lista de quem viu a invenção antes do
   depósito.** Mantenha enxuta — importa se houver disputa de titularidade.

### Duas coisas que ficam de fora mesmo versionando

**`anterioridades/`** (BLOCO B do `.gitignore`, que não se comenta). Patente
publicada é de acesso livre e não preocupa; artigo de periódico é obra de
terceiro sob licença que costuma cobrir cópia para uso próprio, não
redistribuição por repositório de equipe.

**Binário grande.** O git guarda cada versão de arquivo binário por inteiro, sem
compressão delta: um CAD de 80 MB revisado seis vezes vira meio giga de
histórico que a equipe inteira clona para sempre. Se houver muito CAD, foto em
alta ou vídeo, use Git LFS ou deixe esses arquivos fora. Isso é engenharia, não
norma — mas estraga o dia a dia da equipe, que é justamente o que se quer
proteger ao centralizar tudo aqui.
