# -*- coding: utf-8 -*-
"""A busca contra o juiz, e as solucoes contra a definicao."""
from tresemlinha.busca import maior_colocacao, varrer
from tresemlinha.juiz import (duas_por_linha_e_por_coluna,
                              fechado_por_simetria,
                              os_dois_caminhos_concordam, respeita_o_teto,
                              soma_das_orbitas)
from tresemlinha.nucleo import e_valida, tem_tres_alinhados_na_marra, teto


def test_contagens_medidas():
    esperado = {2: (1, 1), 3: (2, 1), 4: (11, 4), 5: (32, 5), 6: (50, 11),
                7: (132, 22)}
    for n, (solucoes, desenhos) in esperado.items():
        r = varrer(n)
        assert r.quantas == solucoes, n
        assert r.desenhos() == desenhos, n


def test_toda_solucao_passa_na_definicao():
    for n in range(2, 8):
        for s in varrer(n).solucoes:
            assert len(s) == teto(n)
            assert e_valida(n, s)
            assert not tem_tres_alinhados_na_marra(s)


def test_toda_solucao_tem_dois_por_linha_e_por_coluna():
    for n in range(2, 8):
        for s in varrer(n).solucoes:
            assert duas_por_linha_e_por_coluna(n, s)


def test_soma_das_orbitas_fecha_com_o_total():
    for n in range(2, 8):
        r = varrer(n)
        assert soma_das_orbitas(n, r.solucoes) == r.quantas, n


def test_o_conjunto_de_solucoes_e_fechado_por_simetria():
    for n in range(2, 8):
        assert fechado_por_simetria(n, varrer(n).solucoes), n


def test_os_dois_caminhos_concordam_nas_solucoes():
    for n in range(2, 8):
        assert os_dois_caminhos_concordam(n, varrer(n).solucoes, limite=40), n


def test_o_teto_e_respeitado_e_atingido():
    for n in range(2, 8):
        r = varrer(n)
        assert respeita_o_teto(n, r.solucoes)
        assert maior_colocacao(n) == teto(n), n


def test_acima_do_teto_nao_ha_nada():
    for n in range(2, 7):
        assert varrer(n, alvo=2 * n + 1).quantas == 0, n


def test_parar_na_primeira_para_mesmo():
    for n in range(3, 8):
        uma = varrer(n, parar_na_primeira=True)
        todas = varrer(n)
        assert uma.quantas == 1
        assert uma.nos <= todas.nos
        assert e_valida(n, uma.solucoes[0])


def test_grade_de_um_e_de_zero():
    assert varrer(1).quantas == 1
    try:
        varrer(0)
    except ValueError:
        return
    raise AssertionError("lado 0 passou")
