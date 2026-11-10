# -*- coding: utf-8 -*-
"""O problema dos tres em linha, varrido na unha.

O pacote tem quatro pedacos que nao se misturam:

    nucleo   o que e estar alinhado, por dois caminhos, e o grupo do quadrado
    busca    a varredura coluna por coluna, com a poda de alinhamento
    juiz     teto, orbitas e fechamento por simetria, cobrados da busca
    medidas  as tabelas que vao para o README

O `juiz` nao importa a `busca` e a `busca` nao importa o `juiz`.
"""
from .busca import Resultado, maior_colocacao, varrer
from .juiz import (duas_por_linha_e_por_coluna, estabilizador,
                   fechado_por_simetria, os_dois_caminhos_concordam,
                   respeita_o_teto, soma_das_orbitas)
from .nucleo import (alinhados_por_determinante, alinhados_por_direcao,
                     canonico, direcao, e_valida, simetrias,
                     tem_tres_alinhados, tem_tres_alinhados_na_marra, teto)

__all__ = [
    "Resultado", "alinhados_por_determinante", "alinhados_por_direcao",
    "canonico", "direcao", "duas_por_linha_e_por_coluna", "e_valida",
    "estabilizador", "fechado_por_simetria", "maior_colocacao",
    "os_dois_caminhos_concordam", "respeita_o_teto", "simetrias",
    "soma_das_orbitas", "tem_tres_alinhados", "tem_tres_alinhados_na_marra",
    "teto", "varrer",
]

__version__ = "1.0.0"
