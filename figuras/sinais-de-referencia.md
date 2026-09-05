# Sinais de referência

Aqui cada sinal numérico é mapeado, em poucas palavras, ao elemento que ele
designa nas figuras. É a matéria-prima de duas coisas que o agente escreve
depois: a frase única de cada figura na "Breve descrição dos desenhos"
(`pedido/desenhos/figuras.tex`) e a explicação detalhada de cada elemento no
corpo do relatório descritivo. Antes de escrever qualquer uma das duas, abra
cada imagem desta pasta e confira quais destes sinais aparecem nela.

O mesmo sinal designa sempre o mesmo elemento em todas as figuras (art. 23,
IV e art. 39, IV da Portaria/INPI/DIRPA nº 14/2024) — por isso a lista é
única para o pedido inteiro, não uma por figura.

## Formato da linha

```
- (N) o que o sinal designa — Figuras 1, 2
```

O trecho depois do travessão **não é enfeite**: é a declaração de quem abriu
a imagem e conferiu que aquele sinal está desenhado ali. É a única informação
do repositório que diz em que figura cada sinal aparece — nem o
`verificar-conformidade.sh` nem o agente de IA enxergam o interior de um PDF
de desenho. Sem ela, um sinal citado no relatório e desenhado em figura
nenhuma passa despercebido até o INPI formular exigência.

O `make verificar` usa essas declarações para avisar quando: um sinal do texto
não está no glossário; um sinal do glossário nunca é citado no texto; um sinal
citado no texto não é localizado em nenhuma figura; ou o glossário remete a
uma figura que não existe.

Se a figura for fotografia sem sinais marcados, ela não entra aqui — veja a
seção final.

Abaixo, o mapeamento do exemplo deste template. Ao redigir um pedido real,
substitua pelos sinais do seu próprio pedido.

## Sinais numerados

- (1) dispositivo de acionamento — Figura 1
- (2) corpo tubular — Figura 1
- (3) membrana elástica — Figura 1
- (4) haste de acionamento — Figura 1
- (5) mola de retorno — Figura 1
- (6) atuador eletromecânico — Figura 1
- (7) sensor de pressão — Figura 1
- (8) unidade de controle — Figuras 1, 2
- (9) assento de vedação de dupla face — Figura 1

## Fotografias sem identificação de partes

Se alguma imagem desta pasta for fotografia sem sinais de referência (ensaio,
protótipo, resultado visual), liste-a aqui e diga só o que ela mostra — sem
número, sem inventar sinal que não está marcado nela. O exemplo deste
template não tem nenhuma figura desse tipo.

- `<nome-do-arquivo>` — ...
