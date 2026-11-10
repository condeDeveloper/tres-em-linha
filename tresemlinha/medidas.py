# -*- coding: utf-8 -*-
"""As tabelas do README, calculadas aqui e em lugar nenhum mais.

Nenhum numero deste projeto foi digitado a mao: o `ferramentas/medidor.py`
imprime o que sai daqui, e os testes prendem os mesmos valores.

A varredura da ordem 8 passa de quatro milhoes de nos e leva meio minuto; a da
9, bem mais. As duas ficam guardadas por ordem.
"""
from __future__ import annotations

from .busca import maior_colocacao, varrer
from .juiz import (duas_por_linha_e_por_coluna, estabilizador,
                   fechado_por_simetria, soma_das_orbitas)
from .nucleo import canonico, teto

_cache: dict[int, object] = {}


def varredura(n: int):
    if n not in _cache:
        _cache[n] = varrer(n)
    return _cache[n]


def tabela_ordens(ordens=range(2, 9)):
    """Uma linha por ordem.

    `(n, teto, solucoes, desenhos, nos, podas_de_alinhamento)`.
    """
    linhas = []
    for n in ordens:
        r = varredura(n)
        linhas.append((n, teto(n), r.quantas, r.desenhos(), r.nos,
                       r.podas_alinhamento))
    return linhas


def tabela_juizes(ordens=range(2, 9)):
    """As conferencias, ordem por ordem.

    `(n, solucoes, soma_das_orbitas, fechado_por_simetria, duas_por_linha)`.
    """
    linhas = []
    for n in ordens:
        r = varredura(n)
        linhas.append((n, r.quantas, soma_das_orbitas(n, r.solucoes),
                       fechado_por_simetria(n, r.solucoes),
                       all(duas_por_linha_e_por_coluna(n, s) for s in r.solucoes)))
    return linhas


def tabela_simetria(ordens=range(2, 9)):
    """Quantos desenhos tem simetria de verdade.

    `(n, desenhos, desenhos_simetricos, solucoes, solucoes_se_nada_fosse_simetrico)`.
    O ultimo numero e `8 * desenhos`: o que o total seria se todo desenho
    tivesse as oito imagens diferentes.
    """
    linhas = []
    for n in ordens:
        r = varredura(n)
        vistos: dict = {}
        for s in r.solucoes:
            c = canonico(n, s)
            if c not in vistos:
                vistos[c] = estabilizador(n, s)
        simetricos = sum(1 for e in vistos.values() if e > 1)
        linhas.append((n, len(vistos), simetricos, r.quantas, 8 * len(vistos)))
    return linhas


def tabela_casas(n: int):
    """Quantas solucoes usam cada casa da grade, e os extremos.

    Devolve `(mapa, menor, maior, total_de_solucoes)`, com `mapa[(x, y)]` = em
    quantas solucoes aquela casa aparece.
    """
    r = varredura(n)
    mapa = {(x, y): 0 for x in range(n) for y in range(n)}
    for s in r.solucoes:
        for p in s:
            mapa[p] += 1
    valores = list(mapa.values())
    return (mapa, min(valores), max(valores), r.quantas)


def tabela_maximos(ordens=range(2, 9)):
    """O maior numero de pontos que cabe, contra o teto: `(n, teto, maior)`."""
    return [(n, teto(n), maior_colocacao(n)) for n in ordens]
