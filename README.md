# O problema dos três em linha

Quantos pontos cabem numa grade `n x n` sem que **três fiquem na mesma reta**?

Reta aqui é reta de verdade, em qualquer direção — não só as horizontais, as
verticais e as duas diagonais principais. Os pontos `(0,0)`, `(1,2)` e `(2,4)`
estão alinhados, e é exatamente esse tipo de trinca que separa um programa certo
de um plausível.

O teto é `2n`, e sai do princípio da casa dos pombos: se alguma linha horizontal
tivesse três pontos, esses três já estariam alinhados. Se `2n` é **sempre**
atingível ninguém sabe — Guy e Kelly conjecturaram em 1968 que a partir de certo
ponto não é, e que o máximo cai para perto de `1,874n`.

Este repositório varre as ordens que cabem num computador. Todas as colocações,
não uma amostra.

Python puro, sem dependência. 35 testes.

```bash
pip install -e ".[dev]"
python -m pytest
python -m tresemlinha varrer 7
python -m tresemlinha casas 7
python -m tresemlinha desenhar 8
python ferramentas/medidor.py --tudo
```

## As colocações, ordem por ordem

| n | teto | colocações | desenhos | nós |
|---:|---:|---:|---:|---:|
| 4 | 8 | 11 | 4 | 192 |
| 5 | 10 | 32 | 5 | 2.170 |
| 6 | 12 | 50 | 11 | 27.874 |
| 7 | 14 | 132 | 22 | 313.810 |
| 8 | 16 | 380 | 57 | 4.140.573 |
| 9 | 18 | **368** | **51** | 53.977.761 |

**Desenhos** são as colocações a menos de girar e espelhar. O teto `2n` foi
atingido em todas as ordens medidas.

## A poda que faz o problema caber

Cada par de pontos já postos determina uma reta, e essa reta corta cada coluna
seguinte em **no máximo uma** casa. Então, assim que um par existe, as casas que
ele proíbe mais à frente são marcadas num contador por casa, e perguntar "cabe
aqui?" vira ler um número.

Na ordem 8, **86,7%** dos nós morrem nessa pergunta: 3.590.612 de 4.140.573.

A primeira versão perguntava olhando os pontos já postos, um por um, e a ordem 9
levava 323 segundos. Com a pergunta em O(1), **190**. O número de nós é
exatamente o mesmo nas duas versões — o que mudou foi o preço de cada um.

## Os juízes

Não há fórmula fechada para este problema. Então o juiz é feito de regras que
valem sempre, e de uma segunda implementação de tudo o que importa:

- **Alinhamento por dois caminhos.** O determinante e a comparação de direções
  reduzidas por máximo divisor comum concordam em todas as 560 trincas da grade
  4 x 4 e em toda trinca de toda solução.
- **Órbitas.** Girar e espelhar leva solução em solução. Pelo teorema da órbita e
  do estabilizador, o número de colocações tem de ser a soma, sobre os desenhos,
  de `8 / |estabilizador|`. **Fecha em todas as ordens medidas** — se a varredura
  perdesse uma colocação, essa soma não bateria.
- **Fechamento.** O conjunto de soluções é fechado pelas oito simetrias.
- **Duas por linha e por coluna.** Toda colocação de `2n` pontos tem exatamente
  dois em cada linha e dois em cada coluna, que é a casa dos pombos cobrada do
  outro lado.

## Quatro achados

**1. A grade maior tem menos soluções.** A ordem 8 tem **380** colocações e
**57** desenhos; a ordem 9, com 81 casas em vez de 64, tem **368** e **51**. O
problema não fica mais fácil com espaço: as retas que aparecem numa grade maior
proíbem mais do que as casas novas liberam.

**2. O centro da grade ímpar é proibido — até a ordem 7, e aí deixa de ser.**
Nas ordens 3, 5 e 7 existe exatamente **uma** casa que não aparece em nenhuma
colocação, e é sempre o centro. Eu ia escrever que isso vale para toda ordem
ímpar. Na ordem 9 o centro aparece em **16** das 368 colocações, não há casa
proibida nenhuma, e as casas menos usadas passam a ser **os quatro cantos**, com
10 cada. A regra durou três ordens, e na quarta trocou até de lugar.

**3. A casa mais usada fica sempre no meio de uma borda, e na ordem 7 ela aparece
em exatamente metade das colocações.** São 66 de 132. Na ordem 5 são 22 de 32
(**68,8%**), na ordem 8 são 158 de 380 (**41,6%**). Nenhuma casa é obrigatória em
ordem nenhuma, mas o meio da borda chega perto.

**4. Quase toda solução pequena é simétrica, e isso acaba rápido.** Até a ordem 4
**todo** desenho tem simetria não trivial. Na ordem 5 só 2 de 5; na 7, 11 de 22
(metade); na 8, **17 de 57** (29,8%). Se nada fosse simétrico, os 57 desenhos da
ordem 8 dariam 456 colocações; dão 380, **83,3%** disso.

## O que as medidas me corrigiram

- **Eu ia escrever que o centro da grade ímpar é sempre proibido.** Três ordens
  seguidas diziam isso, com a mesma casa, e eu já tinha a frase pronta. A ordem 9
  derrubou. Três pontos numa curva não são uma lei; são três pontos numa curva.
- **Eu esperava que o número de soluções crescesse com a ordem.** Ele cai da 8
  para a 9. Fui procurar bug na varredura e encontrei a soma das órbitas
  fechando certinha nas duas: 380 e 368, as duas conferidas por um caminho que
  não é o da busca.
- **A primeira checagem de alinhamento olhava linha, coluna e as duas
  diagonais.** Passava direto por `(0,0)`, `(1,2)`, `(2,4)`, que é a trinca mais
  comum que existe. O teste que pegou isso está no repositório com esse nome:
  "alinhados que passam batido".
- **Eu media a poda contra o número de folhas do espaço.** Comparar nó com folha
  infla a conta. O que está na tabela é nó contra nó: quantos dos nós visitados
  morreram na pergunta do alinhamento.
- **Eu achei que acelerar a busca mudaria os números.** Não mudou nada: a versão
  com contador por casa visita exatamente os mesmos 53.977.761 nós da versão
  lenta na ordem 9. Foi o que me deu confiança de que a troca estava certa — se
  um nó tivesse sumido, seria bug, não otimização.

## Arquivos

```
tresemlinha/nucleo.py   alinhamento pelos dois caminhos, e o grupo do quadrado
tresemlinha/busca.py    a varredura coluna por coluna, com o contador de bloqueio
tresemlinha/juiz.py     teto, órbitas e fechamento, cobrados da busca
tresemlinha/medidas.py  as tabelas deste README
ferramentas/medidor.py
testes/                 35 testes, os pesados separados
```

`juiz.py` não importa `busca.py` e `busca.py` não importa `juiz.py`.
