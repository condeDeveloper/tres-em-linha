# -*- coding: utf-8 -*-
"""Tres em linha: o que e estar alinhado, e como se confere.

O problema: quantos pontos cabem numa grade `n x n` sem que tres fiquem na
mesma reta? Reta aqui e reta de verdade, em qualquer direcao -- nao so as
horizontais, verticais e as duas diagonais principais. Os pontos (0,0), (1,2) e
(2,4) estao alinhados.

O teto e **2n**, e sai do principio da casa dos pombos: se alguma linha
horizontal tivesse tres pontos, esses tres ja estariam alinhados. Entao cada
linha leva no maximo dois, e o mesmo vale para cada coluna.

Se 2n e sempre atingivel ninguem sabe. Guy e Kelly conjecturaram em 1968 que a
partir de certo ponto nao e, e que o maximo cai para perto de 1,874n. Este
repositorio varre as ordens em que a resposta cabe num computador.

A colinearidade e decidida de dois jeitos que nao compartilham uma linha de
codigo: um determinante, e a comparacao de direcoes reduzidas por maximo divisor
comum. Os dois tem de concordar em toda trinca.
"""
from __future__ import annotations

from math import gcd


def alinhados_por_determinante(a, b, c) -> bool:
    """Tres pontos estao alinhados quando a area do triangulo e zero."""
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0


def direcao(a, b) -> tuple[int, int]:
    """A direcao de `a` para `b`, reduzida e com sinal canonico.

    Dois pontos vistos do mesmo lugar com a mesma direcao estao na mesma reta
    que ele. O sinal e normalizado para que `(1, 2)` e `(-1, -2)` sejam a mesma
    direcao: a reta nao tem lado.
    """
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0 and dy == 0:
        raise ValueError("os dois pontos sao o mesmo: %r" % (a,))
    g = gcd(abs(dx), abs(dy))
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):
        dx, dy = -dx, -dy
    return (dx, dy)


def alinhados_por_direcao(a, b, c) -> bool:
    """O mesmo, pelas direcoes reduzidas. Nao usa o determinante."""
    return direcao(a, b) == direcao(a, c)


def tem_tres_alinhados(pontos) -> bool:
    """Existe trinca alinhada no conjunto? Pelo caminho das direcoes.

    Para cada ponto, olha a direcao ate todos os outros: direcao repetida e
    trinca alinhada. Custa O(k^2) no total, contra O(k^3) de olhar todas as
    trincas.
    """
    pontos = list(pontos)
    for i, p in enumerate(pontos):
        vistas = set()
        for j, q in enumerate(pontos):
            if i == j:
                continue
            d = direcao(p, q)
            if d in vistas:
                return True
            vistas.add(d)
    return False


def tem_tres_alinhados_na_marra(pontos) -> bool:
    """O mesmo, abrindo todas as trincas e chamando o determinante.

    E O(k^3) e nao serve para a busca. Serve para julgar a versao de cima: as
    duas tem de dar a mesma resposta em todo conjunto.
    """
    pontos = list(pontos)
    k = len(pontos)
    for i in range(k):
        for j in range(i + 1, k):
            for m in range(j + 1, k):
                if alinhados_por_determinante(pontos[i], pontos[j], pontos[m]):
                    return True
    return False


def e_valida(n: int, pontos) -> bool:
    """O conjunto cabe na grade, nao repete ponto e nao tem tres alinhados."""
    pontos = list(pontos)
    if len(set(pontos)) != len(pontos):
        return False
    if any(not (0 <= x < n and 0 <= y < n) for x, y in pontos):
        return False
    return not tem_tres_alinhados(pontos)


def teto(n: int) -> int:
    """O teto 2n, da casa dos pombos: no maximo dois pontos por linha."""
    if n < 1:
        raise ValueError("a grade comeca em 1")
    return 2 * n if n > 1 else 1


def simetrias(n: int, pontos) -> list[tuple]:
    """As oito imagens do conjunto pelo grupo do quadrado, cada uma ordenada.

    Girar e espelhar a grade leva reta em reta, entao leva conjunto valido em
    conjunto valido. E por isso que as solucoes vem em grupos de oito -- menos
    quando a propria solucao e simetrica, e ai o grupo e menor.
    """
    saida = []
    for virar in (False, True):
        base = [(y, x) for x, y in pontos] if virar else list(pontos)
        for giro in range(4):
            atual = base
            for _ in range(giro):
                atual = [(y, n - 1 - x) for x, y in atual]
            saida.append(tuple(sorted(atual)))
    return saida


def canonico(n: int, pontos) -> tuple:
    """A menor das oito imagens: um nome so por desenho."""
    return min(simetrias(n, pontos))
