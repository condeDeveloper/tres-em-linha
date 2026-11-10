# -*- coding: utf-8 -*-
"""O juiz: o que uma varredura correta e obrigada a cumprir.

Nao ha formula fechada para este problema, e nao ha sequencia que eu possa
somar de cabeca. Entao o juiz e feito de regras que valem sempre, e de uma
segunda implementacao de tudo o que importa:

1. **Teto.** Nenhuma colocacao passa de 2n, e o motivo e de uma linha: tres
   pontos na mesma linha horizontal ja estao alinhados.
2. **Dois caminhos para alinhamento.** O determinante e as direcoes reduzidas
   tem de concordar em toda trinca, e os dois tem de concordar com a varredura
   O(k^3) sobre cada solucao.
3. **Orbitas.** Girar e espelhar leva solucao em solucao. Entao o numero de
   solucoes e a soma, sobre os desenhos, de 8 dividido pelo tamanho do
   estabilizador daquele desenho. E o teorema da orbita e do estabilizador, e
   ele cobra as duas contagens uma contra a outra: se a varredura perdesse uma
   solucao, essa soma nao fecharia.
4. **Fechamento.** O conjunto de solucoes e fechado pelas oito simetrias: a
   imagem de uma solucao esta na lista.
"""
from __future__ import annotations

from itertools import combinations

from .nucleo import (alinhados_por_determinante, alinhados_por_direcao,
                     canonico, simetrias, teto)


def estabilizador(n: int, pontos) -> int:
    """Quantas das oito simetrias deixam o desenho no lugar."""
    alvo = tuple(sorted(pontos))
    return sum(1 for imagem in simetrias(n, pontos) if imagem == alvo)


def soma_das_orbitas(n: int, solucoes) -> int:
    """A soma de 8 / |estabilizador| sobre os desenhos. Tem de dar o total."""
    vistos = {}
    for s in solucoes:
        c = canonico(n, s)
        if c not in vistos:
            vistos[c] = estabilizador(n, s)
    return sum(8 // tamanho for tamanho in vistos.values())


def fechado_por_simetria(n: int, solucoes) -> bool:
    """Toda imagem de toda solucao tambem e solucao."""
    conjunto = {tuple(sorted(s)) for s in solucoes}
    for s in conjunto:
        for imagem in simetrias(n, s):
            if imagem not in conjunto:
                return False
    return True


def os_dois_caminhos_concordam(n: int, solucoes, limite: int | None = None) -> bool:
    """O determinante e as direcoes dao a mesma resposta em toda trinca.

    Percorre as trincas de cada solucao e, de quebra, confere que nenhuma delas
    esta alinhada -- que e o que a solucao promete.
    """
    for s in list(solucoes)[:limite]:
        for a, b, c in combinations(s, 3):
            por_det = alinhados_por_determinante(a, b, c)
            por_dir = alinhados_por_direcao(a, b, c)
            if por_det != por_dir or por_det:
                return False
    return True


def respeita_o_teto(n: int, solucoes) -> bool:
    limite = teto(n)
    return all(len(s) <= limite for s in solucoes)


def duas_por_linha_e_por_coluna(n: int, pontos) -> bool:
    """Numa colocacao de 2n pontos, cada linha e cada coluna leva exatamente dois."""
    linhas = [0] * n
    colunas = [0] * n
    for x, y in pontos:
        colunas[x] += 1
        linhas[y] += 1
    return all(c == 2 for c in colunas) and all(l == 2 for l in linhas)
