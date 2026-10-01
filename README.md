# Simulados AV1 — Epístolas Gerais

Site de estudo para a AV1 de Epístolas Gerais (FABAT, 2026.2): Hebreus e os verbos imperativos em Tiago.

- 72 questões de múltipla escolha, cada uma com comentário e link para o trecho do material
- 7 simulados fixos, simulado aleatório (15 questões) e treino por tópico
- 15 questões dissertativas com gabarito
- Material de estudo: resumo de Carson & Moo (Hebreus) e dos slides das aulas 4 a 7

Tópicos indicados pelo professor: autoria de Hebreus; relação do texto com a Itália; motivações da escrita e superioridade do sacerdócio de Jesus; sacerdócio levítico como sombra do de Cristo e as duas alianças (Hb 8–10); verbos imperativos em Tiago.

## Como editar

O `index.html` é gerado. Não edite à mão: altere os arquivos em `build/` e rode o build.

- `build/materia.py`: material de estudo (cada parágrafo ganha um id `prefixo-seção-parágrafo`)
- `build/questoes.py`: questões de múltipla escolha e dissertativas
- `build/template.html` e `build/base.css`: layout

```sh
python3 build/build.py
```

O build confere se todas as referências ao material existem e sorteia, com semente fixa, a posição da alternativa correta.

## Publicação

O site é publicado pelo GitHub Pages a partir da raiz da branch `main`.
