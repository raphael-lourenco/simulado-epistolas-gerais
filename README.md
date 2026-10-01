# Simulados AV1 — Epístolas Gerais

Site de estudo para a AV1 de Epístolas Gerais (FABAT, 2026.2): Hebreus e os verbos imperativos em Tiago.

- Simulados no formato da prova: 7 objetivas + 2 discursivas (uma delas sempre sobre Hebreus 8–10)
- 8 simulados fixos, prova aleatória no mesmo formato e treino por tópico
- 114 questões objetivas, cada uma com comentário e link para o trecho do material
- 20 discursivas com gabarito, com destaque para as que seguem a orientação do professor
- As questões de Hebreus saem do Carson & Moo (a prova não exige consulta à Bíblia); as alternativas erradas são posições reais do texto atribuídas a outra pessoa ou fora de contexto
- Material de estudo: guia "O que cai na prova", resumo de Carson & Moo (Hebreus) e dos slides das aulas 4 a 7

Pontos que o professor indicou: propósito de Hebreus (destinatários judeus-cristãos querendo voltar ao judaísmo; superioridade de Jesus sobre a instituição judaica e o sistema sacrificial levítico); gênero (homilia, “palavra de exortação”, 13.22); vínculo com a Itália (13.24 e contato literário com 1 Pedro e 1 Clemente); Tiago como texto exortatório por causa do alto número de imperativos; e a discursiva de Hebreus 8–10.

## Como editar

O `index.html` é gerado. Não edite à mão: altere os arquivos em `build/` e rode o build.

- `build/materia.py`: material de estudo (cada parágrafo ganha um id `prefixo-seção-parágrafo`)
- `build/questoes.py`: tópicos, molde da prova, questões objetivas e discursivas
- `build/template.html` e `build/base.css`: layout

```sh
python3 build/build.py
```

O build confere se todas as referências ao material existem e sorteia, com semente fixa, a posição da alternativa correta.

## Publicação

O site é publicado pelo GitHub Pages a partir da raiz da branch `main`.
