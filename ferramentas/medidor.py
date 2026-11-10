# -*- coding: utf-8 -*-
"""Imprime as tabelas que vao para o README. Nenhum numero sai daqui a mao.

    python ferramentas/medidor.py          ate a ordem 7
    python ferramentas/medidor.py --tudo   inclui a ordem 8

A ordem 8 passa de quatro milhoes de nos e leva meio minuto, por isso fica atras
de um sinalizador.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tresemlinha.medidas import (tabela_casas, tabela_juizes,  # noqa: E402
                                 tabela_maximos, tabela_ordens,
                                 tabela_simetria)


def titulo(texto: str) -> None:
    print()
    print(texto)
    print("-" * len(texto))


def ordens(ate_8: bool) -> None:
    titulo("As colocacoes de 2n pontos, ordem por ordem")
    print("  n   teto  solucoes  desenhos  nos         podas de alinhamento")
    inicio = time.time()
    for n, t, solucoes, desenhos, nos, podas in tabela_ordens(
            range(2, 9 if ate_8 else 8)):
        print("  %-3d %-5d %-9d %-9d %-11d %d" % (n, t, solucoes, desenhos, nos, podas))
    print("  %.1fs" % (time.time() - inicio))


def juizes(ate_8: bool) -> None:
    titulo("As conferencias")
    print("  n   solucoes  soma das orbitas  fechado  dois por linha")
    for n, solucoes, orbitas, fechado, duas in tabela_juizes(
            range(2, 9 if ate_8 else 8)):
        marca = "" if solucoes == orbitas and fechado and duas else "   DIVERGE"
        print("  %-3d %-9d %-17d %-8s %s%s"
              % (n, solucoes, orbitas, "sim" if fechado else "NAO",
                 "sim" if duas else "NAO", marca))


def maximos(ate_8: bool) -> None:
    titulo("O teto 2n foi atingido?")
    print("  n   teto  maior colocacao")
    for n, t, maior in tabela_maximos(range(2, 9 if ate_8 else 8)):
        print("  %-3d %-5d %-15d%s" % (n, t, maior, "" if maior == t else "  ABAIXO"))


def simetria(ate_8: bool) -> None:
    titulo("Quantos desenhos tem simetria de verdade")
    print("  n   desenhos  simetricos  solucoes  se nada fosse simetrico")
    for n, desenhos, simetricos, solucoes, teto8 in tabela_simetria(
            range(2, 9 if ate_8 else 8)):
        print("  %-3d %-9d %-11d %-9d %d" % (n, desenhos, simetricos, solucoes, teto8))


def casas(ate_8: bool) -> None:
    titulo("Em quantas solucoes cada casa aparece")
    print("  n   solucoes  menos usada  mais usada  casas proibidas")
    for n in range(3, 9 if ate_8 else 8):
        mapa, menor, maior, total = tabela_casas(n)
        proibidas = sorted(p for p, v in mapa.items() if v == 0)
        print("  %-3d %-9d %-12d %-11d %s"
              % (n, total, menor, maior, proibidas if proibidas else "nenhuma"))


def main() -> int:
    tudo = "--tudo" in sys.argv
    ordens(tudo)
    juizes(tudo)
    maximos(tudo)
    simetria(tudo)
    casas(tudo)
    if not tudo:
        print()
        print("(a ordem 8 so com --tudo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
