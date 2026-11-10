# -*- coding: utf-8 -*-
"""Linha de comando: `python -m tresemlinha <comando>`.

    varrer <n>    as colocacoes de 2n pontos na grade n x n
    casas <n>     em quantas solucoes cada casa da grade aparece
    maior <n>     o maior numero de pontos que a grade aceita
    desenhar <n>  uma solucao da grade n x n, em texto
"""
from __future__ import annotations

import sys

from .busca import maior_colocacao, varrer
from .juiz import soma_das_orbitas
from .medidas import tabela_casas
from .nucleo import teto


def _lado(args, padrao=6) -> int:
    return int(args[0]) if args else padrao


def _varrer(args) -> int:
    n = _lado(args)
    r = varrer(n)
    print("grade %d x %d, teto de %d pontos" % (n, n, teto(n)))
    print("  solucoes            %d" % r.quantas)
    print("  desenhos diferentes %d" % r.desenhos())
    print("  soma das orbitas    %d" % soma_das_orbitas(n, r.solucoes))
    print("  nos visitados       %d" % r.nos)
    print("  podas de alinhamento %d" % r.podas_alinhamento)
    return 0


def _casas(args) -> int:
    n = _lado(args)
    mapa, menor, maior, total = tabela_casas(n)
    print("grade %d x %d, %d solucoes" % (n, n, total))
    for y in range(n):
        print("  " + " ".join("%4d" % mapa[(x, y)] for x in range(n)))
    print("  menos usada %d, mais usada %d" % (menor, maior))
    proibidas = sorted(p for p, v in mapa.items() if v == 0)
    print("  casas que nunca aparecem: %s" % (proibidas or "nenhuma"))
    return 0


def _maior(args) -> int:
    n = _lado(args)
    print("grade %d x %d: teto %d, maior colocacao %d"
          % (n, n, teto(n), maior_colocacao(n)))
    return 0


def _desenhar(args) -> int:
    n = _lado(args)
    r = varrer(n, parar_na_primeira=True)
    if not r.quantas:
        print("nenhuma solucao")
        return 1
    pontos = set(r.solucoes[0])
    for y in range(n):
        print("  " + " ".join("o" if (x, y) in pontos else "." for x in range(n)))
    return 0


COMANDOS = {"varrer": _varrer, "casas": _casas, "maior": _maior,
            "desenhar": _desenhar}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 0 if not argv else 2
    return COMANDOS[argv[0]](argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
