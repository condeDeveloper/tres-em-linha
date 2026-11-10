# -*- coding: utf-8 -*-
"""A busca: varre as colocacoes coluna por coluna.

Para chegar ao teto de 2n pontos, cada uma das n colunas precisa levar
EXATAMENTE dois -- se alguma levasse menos, nao sobraria espaco nas outras, que
tambem nao passam de dois. O mesmo vale para as linhas. Entao a busca escolhe,
para cada coluna, o par de linhas que recebe ponto, com a conta de quantas vezes
cada linha ja foi usada.

As podas, em ordem de quanto cortam:

1. **Alinhamento.** Ao por um ponto, se ele fecha uma trinca alinhada com dois
   ja postos, o ramo morre. E a poda que faz o problema caber.
2. **Linha cheia.** Linha que ja recebeu dois pontos nao recebe mais.
3. **Linha faminta.** Se faltam `c` colunas e alguma linha ainda precisa de mais
   de `c` pontos, acabou: nao da tempo.

A poda de alinhamento nao e feita olhando os pontos ja postos, um por um. Cada
par de pontos ja postos determina uma reta, e essa reta corta cada coluna
seguinte em no maximo UMA casa. Entao, assim que um par existe, as casas que ele
proibe mais a frente sao marcadas num contador por casa, e perguntar "cabe aqui?"
vira ler um numero. Com a pergunta em O(1) no lugar de O(k), a ordem 9 caiu de
323 para o que esta na tabela do README.

A simetria NAO e usada para podar. O grupo do quadrado e usado depois, para
agrupar as solucoes em desenhos -- e a diferenca entre os dois numeros e um dos
achados.
"""
from __future__ import annotations

from itertools import combinations

from math import gcd

from .nucleo import canonico, tem_tres_alinhados


class Resultado:
    """O que a varredura de uma ordem devolve.

    `nos` conta as vezes que a busca tentou fechar uma coluna, inclusive as que
    a poda derrubou no instante seguinte.
    """

    def __init__(self, n: int, alvo: int):
        self.n = n
        self.alvo = alvo
        self.nos = 0
        self.podas_alinhamento = 0
        self.podas_linha = 0
        self.solucoes: list[tuple] = []

    @property
    def quantas(self) -> int:
        return len(self.solucoes)

    def desenhos(self) -> int:
        """Quantas solucoes diferentes a menos de girar e espelhar."""
        return len({canonico(self.n, s) for s in self.solucoes})

    def __repr__(self) -> str:
        return ("Resultado(n=%d, alvo=%d, solucoes=%d, nos=%d)"
                % (self.n, self.alvo, self.quantas, self.nos))


def varrer(n: int, alvo: int | None = None,
           parar_na_primeira: bool = False) -> Resultado:
    """Varre as colocacoes de `alvo` pontos (por omissao, 2n) na grade n x n."""
    if n < 1:
        raise ValueError("a grade comeca em 1")
    if alvo is None:
        alvo = 2 * n if n > 1 else 1
    r = Resultado(n, alvo)
    if alvo > 2 * n:
        return r
    if n == 1:
        if alvo <= 1:
            r.solucoes.append(((0, 0),) if alvo == 1 else ())
        return r
    if alvo != 2 * n:
        return _varrer_abaixo_do_teto(n, alvo, parar_na_primeira, r)

    pontos: list[tuple[int, int]] = []
    usos = [0] * n
    # bloqueio[coluna][linha]: quantas retas ja decididas passam por essa casa.
    bloqueio = [[0] * n for _ in range(n)]
    pares = list(combinations(range(n), 2))

    def marca(p, q, delta: int) -> None:
        """Soma `delta` nas casas das colunas seguintes que a reta p-q corta."""
        (x1, y1), (x2, y2) = p, q
        dx, dy = x2 - x1, y2 - y1
        if dx == 0:
            # Reta vertical: nao alcanca coluna nenhuma alem da propria.
            return
        g = gcd(abs(dx), abs(dy))
        dx, dy = dx // g, dy // g
        if dx < 0:
            dx, dy = -dx, -dy
        inicio = max(x1, x2) + 1
        passo_x = dx
        y = y1 + (inicio - x1) // passo_x * dy if (inicio - x1) % passo_x == 0 else None
        if y is None:
            # A reta so toca colunas espacadas de dx; acha a primeira valida.
            resto = (inicio - x1) % passo_x
            primeira = inicio + (passo_x - resto)
            y = y1 + (primeira - x1) // passo_x * dy
            inicio = primeira
        coluna = inicio
        while coluna < n:
            if 0 <= y < n:
                bloqueio[coluna][y] += delta
            coluna += passo_x
            y += dy

    def poe(ponto) -> None:
        for p in pontos:
            marca(p, ponto, 1)
        pontos.append(ponto)

    def tira(ponto) -> None:
        pontos.pop()
        for p in pontos:
            marca(p, ponto, -1)

    def passo(coluna: int) -> bool:
        if coluna == n:
            r.solucoes.append(tuple(sorted(pontos)))
            return True
        faltam = n - coluna
        if any(2 - u > faltam for u in usos):
            r.podas_linha += 1
            return False
        livres = bloqueio[coluna]
        for a, b in pares:
            if usos[a] >= 2 or usos[b] >= 2:
                continue
            r.nos += 1
            if livres[a] or livres[b]:
                r.podas_alinhamento += 1
                continue
            pa, pb = (coluna, a), (coluna, b)
            poe(pa)
            if bloqueio[coluna][b]:
                # O proprio pa acabou de proibir pb: os dois com algum par
                # anterior ficariam alinhados.
                r.podas_alinhamento += 1
                tira(pa)
                continue
            poe(pb)
            usos[a] += 1
            usos[b] += 1
            achou = passo(coluna + 1)
            usos[a] -= 1
            usos[b] -= 1
            tira(pb)
            tira(pa)
            if achou and parar_na_primeira:
                return True
        return False

    passo(0)
    return r


def _varrer_abaixo_do_teto(n, alvo, parar_na_primeira, r):
    """Colocacoes com menos de 2n pontos, para responder `maior_colocacao`.

    Aqui as colunas podem levar 0, 1 ou 2 pontos, entao a busca e outra: ela
    escolhe, coluna por coluna, qual subconjunto de linhas recebe ponto.
    """
    pontos: list[tuple[int, int]] = []
    usos = [0] * n
    escolhas = [()] + [(i,) for i in range(n)] + list(combinations(range(n), 2))

    def passo(coluna: int, restam: int) -> bool:
        if restam == 0:
            r.solucoes.append(tuple(sorted(pontos)))
            return True
        if coluna == n:
            return False
        if restam > 2 * (n - coluna):
            return False
        for linhas in escolhas:
            if len(linhas) > restam:
                continue
            if any(usos[i] >= 2 for i in linhas):
                continue
            r.nos += 1
            novos = [(coluna, i) for i in linhas]
            if tem_tres_alinhados(pontos + novos):
                r.podas_alinhamento += 1
                continue
            pontos.extend(novos)
            for i in linhas:
                usos[i] += 1
            achou = passo(coluna + 1, restam - len(linhas))
            for i in linhas:
                usos[i] -= 1
            del pontos[len(pontos) - len(novos):]
            if achou and parar_na_primeira:
                return True
        return False

    passo(0, alvo)
    return r


def maior_colocacao(n: int) -> int:
    """O maior numero de pontos que a grade n x n aceita, descendo do teto.

    Desce de 2n ate achar um tamanho que tenha solucao. Enquanto 2n for
    atingivel -- e ate a ordem medida ele e -- a primeira tentativa ja responde.
    """
    for alvo in range(2 * n, 0, -1):
        if varrer(n, alvo, parar_na_primeira=True).quantas:
            return alvo
    return 0
