# -*- coding: utf-8 -*-
"""Os numeros do README, presos aqui.

Nenhum valor daqui foi estimado: todos sairam do `ferramentas/medidor.py`.
A ordem 8, que leva meio minuto, mora no `test_pesados.py`.
"""
from tresemlinha.medidas import (tabela_casas, tabela_juizes, tabela_maximos,
                                 tabela_ordens, tabela_simetria)


def test_tabela_de_ordens_ate_7():
    esperado = {
        2: (4, 1, 1, 2), 3: (6, 2, 1, 18), 4: (8, 11, 4, 192),
        5: (10, 32, 5, 2170), 6: (12, 50, 11, 27874),
        7: (14, 132, 22, 313810),
    }
    for n, t, solucoes, desenhos, nos, _podas in tabela_ordens(range(2, 8)):
        assert (t, solucoes, desenhos, nos) == esperado[n], n


def test_os_desenhos_dao_a_contagem_publicada():
    # 1, 1, 4, 5, 11, 22 a partir da ordem 2: e a contagem de colocacoes de 2n
    # pontos a menos de girar e espelhar.
    desenhos = [d for _n, _t, _s, d, _nos, _p in tabela_ordens(range(2, 8))]
    assert desenhos == [1, 1, 4, 5, 11, 22]


def test_todos_os_juizes_fecham():
    for n, solucoes, orbitas, fechado, duas in tabela_juizes(range(2, 8)):
        assert solucoes == orbitas, n
        assert fechado, n
        assert duas, n


def test_o_teto_foi_atingido_em_toda_ordem_medida():
    for n, t, maior in tabela_maximos(range(2, 8)):
        assert maior == t == 2 * n, n


def test_simetria_dos_desenhos():
    esperado = {2: (1, 1), 3: (1, 1), 4: (4, 4), 5: (5, 2), 6: (11, 7),
                7: (22, 11)}
    for n, desenhos, simetricos, _s, _t in tabela_simetria(range(2, 8)):
        assert (desenhos, simetricos) == esperado[n], n
    # A ordem 4 e a ultima em que TODO desenho e simetrico.
    linhas = {n: (d, s) for n, d, s, _x, _y in tabela_simetria(range(2, 8))}
    assert linhas[4][0] == linhas[4][1]
    assert linhas[5][0] != linhas[5][1]


def test_o_centro_e_proibido_nas_ordens_3_5_e_7():
    # E SO nelas: a ordem 9 tem o centro em 10 solucoes. A regra que eu ia
    # escrever morreu na primeira ordem que nao cabia na tabela.
    for n in (3, 5, 7):
        mapa, menor, _maior, _total = tabela_casas(n)
        proibidas = sorted(p for p, v in mapa.items() if v == 0)
        assert menor == 0, n
        assert proibidas == [(n // 2, n // 2)], n


def test_na_grade_par_nao_ha_casa_proibida():
    for n in (4, 6):
        mapa, menor, _maior, _total = tabela_casas(n)
        assert menor > 0, n
        assert all(v > 0 for v in mapa.values()), n


def test_a_casa_mais_usada_fica_no_meio_da_borda():
    for n in (5, 6, 7):
        mapa, _menor, maior, _total = tabela_casas(n)
        campeas = sorted(p for p, v in mapa.items() if v == maior)
        for x, y in campeas:
            na_borda = x in (0, n - 1) or y in (0, n - 1)
            assert na_borda, (n, x, y)


def test_percentuais_da_casa_mais_usada():
    _mapa, _menor, maior, total = tabela_casas(7)
    assert (maior, total) == (66, 132)
    assert round(100 * maior / total, 1) == 50.0
    _mapa, _menor, maior, total = tabela_casas(5)
    assert (maior, total) == (22, 32)
    assert round(100 * maior / total, 1) == 68.8
