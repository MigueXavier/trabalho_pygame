<div align="center">
<div align="center">

```
██████╗ ███████╗██████╗ ██████╗ ██╗██████╗  ██████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║██╔══██╗██╔═══██╗
██████╔╝█████╗  ██████╔╝██║  ██║██║██║  ██║██║   ██║
██╔═══╝ ██╔══╝  ██╔══██╗██║  ██║██║██║  ██║██║   ██║
██║     ███████╗██║  ██║██████╔╝██║██████╔╝╚██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═════╝  ╚═════╝

███╗   ██╗ ██████╗      █████╗ ██╗      ██████╗  ██████╗ ██████╗ ██╗████████╗███╗   ███╗ ██████╗
████╗  ██║██╔═══██╗    ██╔══██╗██║     ██╔════╝ ██╔═══██╗██╔══██╗██║╚══██╔══╝████╗ ████║██╔═══██╗
██╔██╗ ██║██║   ██║    ███████║██║     ██║  ███╗██║   ██║██████╔╝██║   ██║   ██╔████╔██║██║   ██║
██║╚██╗██║██║   ██║    ██╔══██║██║     ██║   ██║██║   ██║██╔══██╗██║   ██║   ██║╚██╔╝██║██║   ██║
██║ ╚████║╚██████╔╝    ██║  ██║███████╗╚██████╔╝╚██████╔╝██║  ██║██║   ██║   ██║ ╚═╝ ██║╚██████╔╝
╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝
```

</div>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00B140?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-F4A01A?style=for-the-badge)

<br/>

> *"Num mundo onde tudo é controlado por algoritmos, apenas quem sabe programar encontra o caminho."*

<br/>
</div>

<div align="center">
  
| Integrantes |
|-----------|
| Arthur Fernandes Fialho e Silva |
| Arthur Rodrigues de Macedo |
| Miguel Xavier dos Santos |
| Pamela Fernandes Nilo |
| Túlio Marcus de Oliveira Gonçalves |

</div>

---

## Índice

- [Sobre o Jogo](#-sobre-o-jogo)
- [Como Rodar](#-como-rodar)
- [Como Jogar](#-como-jogar)
- [Objetivos](#-objetivos)
- [Regras](#-regras)
- [Elementos do Jogo](#-elementos-do-jogo)
- [Controles](#️-controles)
- [Organização do Código](#️-organização-do-código)
- [Recursos Externos](#️-recursos-externos)
- [Melhorias Previstas](#-melhorias-previstas)

---

## Sobre o Jogo

**Perdido no Algoritmo** é um jogo de labirinto simples onde o jogador não controla o personagem diretamente — ele **monta algoritmos** com blocos de programação para mover o personagem pelo cenário.

Na tela aparecem um personagem, diferentes cenários organizados em uma grade, e objetos relacionados aos desafios de cada fase: itens para coletar, obstáculos, o objetivo final e um painel com blocos de comandos. Por meio desse painel, o jogador monta uma sequência de comandos (incluindo blocos de repetição) e executa essa sequência para fazer o personagem andar, coletar itens e chegar ao objetivo.

Conforme as fases avançam, torna-se necessário utilizar o bloco de repetição (`Rep xN`) e estratégias para contornar obstáculos e resolver o trajeto no menor número de comandos possível.

---

## Como Jogar

<div align="center">

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  1. Analise o labirinto e os objetivos da fase           │
│              ↓                                           │
│  2. Monte sua sequência de blocos no painel              │
│              ↓                                           │
│  3. Clique em EXECUTAR para rodar a sequência             │
│              ↓                                           │
│  4. Observe o personagem seguindo seus comandos          │
│              ↓                                           │
│  5. Se não conseguir, perde uma vida e tenta de novo     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

</div>

---

## Objetivos

- Chegar até o final do labirinto
- Coletar itens
- Coletar os itens no **menor número de comandos possível**
- Evitar obstáculos

### Condição de vitória

> Chegar ao final da fase seguindo as regras impostas.

### Condição de derrota

> Perder todas as vidas sem chegar ao objetivo.

---

## Regras

<div align="center">

| # | Regra |
|---|-------|
| 1 | O jogador começa no ponto **A** e deve chegar ao ponto **B** |
| 2 | Para chegar ao ponto B, ele deve definir a movimentação com **blocos de programação** |
| 3 | Caso não consiga completar a fase, perde **uma vida** |
| 4 | O jogador começa com **3 vidas** (tentativas) por fase |
| 5 | Caso as vidas acabem, a fase é reiniciada |
| 6 | O progresso (fase atual e recorde) é salvo automaticamente ao voltar ao menu |

</div>

---

## Elementos do Jogo

### Personagem principal

Um personagem controlado pelos blocos de comando selecionados pelo jogador, com efeitos sonoros de passos, coleta e colisão.

### Obstáculos

Barreiras que impedem a passagem do personagem.

### Itens de interação

Itens coletáveis aumentam a pontuação quando coletados.

### Pontuação, Vidas e Progresso

```
♥ ♥ ♥  →  3 vidas iniciais

⭐ Coletar um item     → +10 pontos
💀 Perder todas vidas  → reinicia a fase
🚪 Concluir as 3 fases → vitória final
```

---

## Como Rodar

### Pré-requisitos

- **Python 3.10+**
- **pip** e **venv** (no Ubuntu/Debian: `sudo apt install python3-pip python3-venv`)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/python-game.git
cd python-game

# 2. Crie e ative um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate            # Linux / macOS
# .venv\Scripts\activate            # Windows (PowerShell)

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o jogo
python main.py
```

---

## Controles

<div align="center">

```
╔══════════════════════════════════════════════════════════╗
║                MANUAL DE BLOCOS E BOTÕES                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  [ → ]  Bloco Direita    → Move o personagem 1 casa      ║
║                            para a direita                ║
║  [ ← ]  Bloco Esquerda   → Move o personagem 1 casa      ║
║                            para a esquerda               ║
║  [ ↑ ]  Bloco Cima       → Move o personagem 1 casa      ║
║                            para cima                     ║
║  [ ↓ ]  Bloco Baixo      → Move o personagem 1 casa      ║
║                            para baixo                    ║
║                                                          ║
║  [Rep xN] Bloco Repetir  → Repete N vezes os blocos       ║
║                            inseridos dentro dele          ║
║                                                          ║
║  Clique num bloco já colocado na sequência para           ║
║  removê-lo dela.                                          ║
║                                                          ║
║ ════════════════════════════════════════════════════════ ║
║                                                          ║
║  [ EXECUTAR ] → Roda a sequência de comandos montada      ║
║  [ RESET    ] → Limpa a sequência e reabilita os blocos   ║
║  [ SAIR     ] → Salva o progresso e volta ao menu          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

</div>

---

## Organização do Código

```
main.py              →  ponto de entrada; controla o loop Menu ⇄ Jogo

src/
├── jogo.py          →  loop principal, montagem da sequência, execução e telas de resultado
├── menu.py          →  menu inicial (Novo Jogo / Continuar / Créditos / Sair)
├── configuracao.py  →  constantes globais (tela, cores, layout, fases)
├── personagem.py     →  movimentação do jogador e efeitos sonoros
├── blocos.py         →  blocos de comando (direção e repetição)
├── comandos.py        →  botão genérico reutilizado pela interface
├── matriz.py          →  construção do labirinto a partir do JSON da fase
├── barreira.py         →  obstáculos
├── item.py             →  itens coletáveis
├── objetivo.py          →  ponto de chegada da fase
├── pontuacao.py          →  contagem de pontos
└── dados.py              →  leitura/escrita do save (recorde e fase atual)

fases/                →  definição de cada fase em JSON (mapa, blocos disponíveis)
assets/fontes/        →  fonte pixelada usada na interface
assets/sons/          →  trilha sonora e efeitos sonoros
assets/sprites/       →  spritesheet e sprites do jogo
tests/                →  script de verificação visual manual
```

---

## Recursos Externos

- Imagens obtidas de banco gratuito
- Efeitos sonoros e trilha sonora obtidos de banco gratuito
- Fonte personalizada (Press Start 2P)

---

## Melhorias Previstas

Caso haja tempo durante o desenvolvimento:

- [ ] Novas fases
- [ ] Animações
- [ ] Diferentes personagens
- [ ] Novos tipos de obstáculos
- [ ] Aumento de dificuldade

---

<div align="center">

```
> Feito com ☕, 🧠 e muito  print("debug")
```

**Perdido no Algoritmo** — Projeto Acadêmico · 2026

</div>
