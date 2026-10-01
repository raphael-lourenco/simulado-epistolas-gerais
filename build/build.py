#!/usr/bin/env python3
"""Gera ../index.html a partir de materia.py, questoes.py e template.html.

Uso: python3 build/build.py
"""
import json
import random
from pathlib import Path

from materia import MATERIA
from questoes import TOPICOS, PROVA_TOPICOS, MOLDE_OBJETIVAS, MULTIPLA, DISSERTATIVAS

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI.parent / "index.html"
LETRAS = "ABCD"
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


def montar_simulados(questoes, dissertativas, rng):
    """Cada simulado segue o formato da prova: 7 objetivas (MOLDE_OBJETIVAS) + 2 discursivas.

    Discursiva 1: sempre a de Hb 8–10 indicada pelo professor.
    Discursiva 2: rodízio entre as demais discursivas em destaque.
    """
    pools = {}
    for t in TOPICOS:
        ids = [q["id"] for q in questoes if q["topico"] == t]
        rng.shuffle(ids)
        pools[t] = ids
    precisa = {t: MOLDE_OBJETIVAS.count(t) for t in set(MOLDE_OBJETIVAS) if t != "livre"}
    n_sims = min(len(pools[t]) // k for t, k in precisa.items())

    destaque = [d for d in dissertativas if d["destaque"]]
    d_fixa = next(d["numero"] for d in destaque if d["topico"] == "alianca")
    d_rodizio = [d["numero"] for d in destaque if d["numero"] != d_fixa]

    simulados = []
    for n in range(n_sims):
        ids = [pools[t].pop() for t in MOLDE_OBJETIVAS if t != "livre"]
        simulados.append({"numero": n + 1, "ids": ids, "diss": [d_fixa, d_rodizio[n % len(d_rodizio)]]})
    # vaga "livre": sorteada entre as questões que sobraram dos tópicos do guia
    sobra = [qid for t in PROVA_TOPICOS for qid in pools[t]]
    rng.shuffle(sobra)
    for n, sim in enumerate(simulados):
        sim["ids"].append(sobra[n])
        rng.shuffle(sim["ids"])
    return simulados


def montar_dissertativas(ids_materia):
    out = []
    for n, (topico, enunciado, gabarito, fontes, destaque) in enumerate(DISSERTATIVAS):
        if topico not in TOPICOS:
            raise SystemExit(f"Tópico desconhecido '{topico}' em: {enunciado}")
        checar_fontes(fontes, ids_materia, enunciado)
        out.append({"numero": n + 1, "topico": topico, "enunciado": enunciado, "gabarito": gabarito, "fonte": fontes, "destaque": destaque})
    return out


def js(valor):
    # </ dentro de strings poderia fechar a tag <script>
    return json.dumps(valor, ensure_ascii=False).replace("</", "<\\/")


def main():
    rng = random.Random(SEMENTE)
    materia, ids = montar_materia()
    questoes = montar_questoes(ids, rng)
    dissertativas = montar_dissertativas(ids)
    simulados = montar_simulados(questoes, dissertativas, rng)

    html = (AQUI / "template.html").read_text(encoding="utf-8")
    trocas = {
        "/*__BASE_CSS__*/": (AQUI / "base.css").read_text(encoding="utf-8"),
        "/*__TOPICOS__*/": js(TOPICOS),
        "/*__PROVA_TOPICOS__*/": js(PROVA_TOPICOS),
        "/*__MOLDE__*/": js(MOLDE_OBJETIVAS),
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
