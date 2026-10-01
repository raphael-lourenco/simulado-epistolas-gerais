#!/usr/bin/env python3
"""Gera ../index.html a partir de materia.py, questoes.py e template.html.

Uso: python3 build/build.py
"""
import json
import random
from pathlib import Path

from materia import MATERIA
from questoes import TOPICOS, MULTIPLA, DISSERTATIVAS

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI.parent / "index.html"
LETRAS = "ABCD"
N_SIMULADOS = 7
PROVA_TOPICOS = ["autoria", "italia", "proposito", "alianca", "tiago"]
SEMENTE = 2026


def montar_materia():
    materia, ids = [], set()
    for parte in MATERIA:
        secoes = []
        for s, (subtitulo, paragrafos) in enumerate(parte["secoes"]):
            pids = [f"{parte['prefixo']}-{s}-{p}" for p in range(len(paragrafos))]
            ids.update(pids)
            secoes.append({"subtitulo": subtitulo, "paragrafos": paragrafos, "paragrafoIds": pids})
        materia.append({k: parte[k] for k in ("numero", "rotulo", "titulo", "fonte")} | {"secoes": secoes})
    return materia, ids


def checar_fontes(fontes, ids, onde):
    for f in fontes:
        if f not in ids:
            raise SystemExit(f"Fonte inexistente '{f}' em: {onde}")


def montar_questoes(ids_materia, rng):
    # Posições da correta distribuídas por igual entre A–D, em ordem sorteada.
    posicoes = [i % 4 for i in range(len(MULTIPLA))]
    rng.shuffle(posicoes)
    questoes = []
    for n, (topico, enunciado, correta, erradas, comentario, fontes) in enumerate(MULTIPLA):
        if topico not in TOPICOS:
            raise SystemExit(f"Tópico desconhecido '{topico}' em: {enunciado}")
        if len(erradas) != 3 or correta in erradas:
            raise SystemExit(f"Alternativas inválidas em: {enunciado}")
        checar_fontes(fontes, ids_materia, enunciado)
        textos = list(erradas)
        rng.shuffle(textos)
        textos.insert(posicoes[n], correta)
        questoes.append({
            "id": f"q{n + 1}",
            "topico": topico,
            "enunciado": enunciado,
            "alternativas": [{"letra": LETRAS[i], "texto": t} for i, t in enumerate(textos)],
            "correta": LETRAS[posicoes[n]],
            "comentario": comentario,
            "fonte": fontes,
        })
    return questoes


def montar_simulados(questoes, rng):
    # Distribui as questões de cada tópico em rodízio, para que todo simulado misture os tópicos.
    baldes = [[] for _ in range(N_SIMULADOS)]
    k = 0
    for topico in TOPICOS:
        do_topico = [q["id"] for q in questoes if q["topico"] == topico]
        rng.shuffle(do_topico)
        for qid in do_topico:
            baldes[k % N_SIMULADOS].append(qid)
            k += 1
    for b in baldes:
        rng.shuffle(b)
    return [{"numero": i + 1, "ids": b} for i, b in enumerate(baldes)]


def montar_dissertativas(ids_materia):
    out = []
    for n, (topico, enunciado, gabarito, fontes) in enumerate(DISSERTATIVAS):
        if topico not in TOPICOS:
            raise SystemExit(f"Tópico desconhecido '{topico}' em: {enunciado}")
        checar_fontes(fontes, ids_materia, enunciado)
        out.append({"numero": n + 1, "topico": topico, "enunciado": enunciado, "gabarito": gabarito, "fonte": fontes})
    return out


def js(valor):
    # </ dentro de strings poderia fechar a tag <script>
    return json.dumps(valor, ensure_ascii=False).replace("</", "<\\/")


def main():
    rng = random.Random(SEMENTE)
    materia, ids = montar_materia()
    questoes = montar_questoes(ids, rng)
    simulados = montar_simulados(questoes, rng)
    dissertativas = montar_dissertativas(ids)

    html = (AQUI / "template.html").read_text(encoding="utf-8")
    trocas = {
        "/*__BASE_CSS__*/": (AQUI / "base.css").read_text(encoding="utf-8"),
        "/*__TOPICOS__*/": js(TOPICOS),
        "/*__PROVA_TOPICOS__*/": js(PROVA_TOPICOS),
        "/*__QUESTOES__*/": js(questoes),
        "/*__SIMULADOS__*/": js(simulados),
        "/*__DISSERTATIVAS__*/": js(dissertativas),
        "/*__MATERIA__*/": js(materia),
    }
    for marca, valor in trocas.items():
        if marca not in html:
            raise SystemExit(f"Marcador ausente no template: {marca}")
        html = html.replace(marca, valor)
    SAIDA.write_text(html, encoding="utf-8")

    from collections import Counter
    print(f"{len(questoes)} múltipla escolha, {len(dissertativas)} dissertativas, {len(simulados)} simulados")
    print("por tópico:", dict(Counter(q["topico"] for q in questoes)))
    print("corretas:", dict(Counter(q["correta"] for q in questoes)))
    print("tamanho dos simulados:", [len(s["ids"]) for s in simulados])
    print(f"gerado: {SAIDA} ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
