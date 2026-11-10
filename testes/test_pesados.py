# -*- coding: utf-8 -*-
"""Os testes que custam minutos: as ordens 8 e 9.

Cada varredura roda UMA VEZ, guardada pelo `medidas.varredura`, e todos os
testes daqui leem o mesmo resultado.
"""
from tresemlinha.juiz import (duas_por_linha_e_por_coluna,
                              fechado_por_simetria, soma_das_orbitas)
from tresemlinha.medidas import tabela_casas, varredura
from tresemlinha.nucleo import e_valida


def test_ordem_8_inteira():
    r = varredura(8)
    assert r.quantas == 380
    assert r.desenhos() == 57
    assert r.nos == 4140573
    assert soma_das_orbitas(8, r.solucoes) == 380
    assert fechado_por_simetria(8, r.solucoes)


def test_ordem_9_inteira():
    r = varredura(9)
    assert r.quantas == 368
    assert r.desenhos() == 51
    assert r.nos == 53977761
    assert soma_das_orbitas(9, r.solucoes) == 368
    assert fechado_por_simetria(9, r.solucoes)


def test_a_ordem_9_tem_menos_solucoes_que_a_8():
    # Grade maior, menos jeitos: 81 casas dao 51 desenhos, 64 casas dao 57.
    assert varredura(9).quantas < varredura(8).quantas
    assert varredura(9).desenhos() < varredura(8).desenhos()


def test_o_centro_da_ordem_9_nao_e_proibido():
    # A ordem 9 derruba a regra que as ordens 3, 5 e 7 sugeriam.
    mapa, menor, _maior, _total = tabela_casas(9)
    assert menor == 10
    assert mapa[(4, 4)] == 16     # o centro aparece, e nem e o menos usado
    assert all(v > 0 for v in mapa.values())


def test_as_solucoes_das_ordens_8_e_9_passam_na_definicao():
    for n in (8, 9):
        r = varredura(n)
        for s in r.solucoes:
            assert len(s) == 2 * n
            assert e_valida(n, s)
            assert duas_por_linha_e_por_coluna(n, s)


def test_a_poda_de_alinhamento_derruba_quase_nove_em_dez_nos():
    r = varredura(8)
    assert r.podas_alinhamento == 3590612
    assert round(100 * r.podas_alinhamento / r.nos, 1) == 86.7
