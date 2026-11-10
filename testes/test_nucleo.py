# -*- coding: utf-8 -*-
"""Alinhamento pelos dois caminhos, e o grupo do quadrado."""
from itertools import combinations

from tresemlinha.nucleo import (alinhados_por_determinante,
                                alinhados_por_direcao, canonico, direcao,
                                e_valida, simetrias, tem_tres_alinhados,
                                tem_tres_alinhados_na_marra, teto)


def test_alinhados_obvios():
    assert alinhados_por_determinante((0, 0), (1, 0), (2, 0))
    assert alinhados_por_determinante((0, 0), (0, 1), (0, 2))
    assert alinhados_por_determinante((0, 0), (1, 1), (2, 2))
    assert not alinhados_por_determinante((0, 0), (1, 0), (0, 1))


def test_alinhados_que_passam_batido():
    # A reta de inclinacao 1/2: o caso que uma checagem so de linha, coluna e
    # diagonal deixaria passar.
    assert alinhados_por_determinante((0, 0), (1, 2), (2, 4))
    assert alinhados_por_direcao((0, 0), (1, 2), (2, 4))
    assert alinhados_por_determinante((0, 0), (2, 1), (4, 2))
    assert alinhados_por_determinante((1, 0), (3, 1), (5, 2))


def test_os_dois_caminhos_concordam_em_toda_trinca_da_grade_4():
    casas = [(x, y) for x in range(4) for y in range(4)]
    for a, b, c in combinations(casas, 3):
        assert alinhados_por_determinante(a, b, c) == alinhados_por_direcao(a, b, c)


def test_direcao_e_reduzida_e_sem_lado():
    assert direcao((0, 0), (2, 4)) == (1, 2)
    assert direcao((0, 0), (-2, -4)) == (1, 2)
    assert direcao((0, 0), (0, 3)) == (0, 1)
    assert direcao((0, 0), (0, -3)) == (0, 1)
    assert direcao((0, 0), (-3, 0)) == (1, 0)


def test_direcao_de_um_ponto_para_ele_mesmo_e_recusada():
    try:
        direcao((2, 2), (2, 2))
    except ValueError:
        return
    raise AssertionError("passou com o mesmo ponto")


def test_as_duas_varreduras_de_trinca_concordam():
    casos = [
        [(0, 0), (1, 2), (2, 4)],
        [(0, 0), (1, 2), (2, 3)],
        [(0, 1), (1, 0), (2, 2), (3, 3)],
        [(0, 0), (1, 1), (2, 0), (3, 1)],
    ]
    for pontos in casos:
        assert tem_tres_alinhados(pontos) == tem_tres_alinhados_na_marra(pontos)


def test_teto_e_dois_n():
    assert teto(1) == 1
    for n in range(2, 12):
        assert teto(n) == 2 * n
    try:
        teto(0)
    except ValueError:
        return
    raise AssertionError("lado 0 passou")


def test_validade_cobra_a_grade_e_a_repeticao():
    assert e_valida(3, [(0, 0), (1, 2)])
    assert not e_valida(3, [(0, 0), (0, 0)])
    assert not e_valida(3, [(0, 0), (3, 1)])
    assert not e_valida(3, [(0, 0), (1, 1), (2, 2)])


def test_as_oito_simetrias():
    pontos = [(0, 0), (1, 2)]
    imagens = simetrias(3, pontos)
    assert len(imagens) == 8
    assert tuple(sorted(pontos)) in imagens
    for imagem in imagens:
        assert all(0 <= x < 3 and 0 <= y < 3 for x, y in imagem)
    assert canonico(3, pontos) == min(imagens)


def test_simetria_preserva_o_alinhamento():
    pontos = [(0, 0), (1, 1), (2, 2)]
    for imagem in simetrias(4, pontos):
        assert tem_tres_alinhados(imagem)
    soltos = [(0, 0), (1, 2), (2, 1)]
    for imagem in simetrias(4, soltos):
        assert not tem_tres_alinhados(imagem)
