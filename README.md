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

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00B140?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-F4A01A?style=for-the-badge)

<br/>

> *"Num mundo onde tudo é controlado por algoritmos, apenas quem sabe programar encontra o caminho."*

<br/>

| Integrantes |
|---|
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
- [Recursos Externos e Bibliografia](#️-recursos-externos-e-bibliografia)

---

## 🎮 Sobre o Jogo

**Perdido no Algoritmo** é um jogo de labirinto onde o jogador não controla o personagem diretamente — ele **monta algoritmos** com blocos de programação para mover o personagem pelo cenário.

Na tela aparecem um personagem, diferentes cenários organizados em uma grade, e objetos relacionados aos desafios de cada fase: itens para coletar, obstáculos, o objetivo final e um painel com blocos de comandos. Por meio desse painel, o jogador monta uma sequência de comandos (incluindo blocos de repetição) e executa essa sequência para fazer o personagem andar, coletar itens e chegar ao objetivo.

Conforme as fases avançam, torna-se necessário utilizar o bloco de repetição (`Rep xN`) e estratégias para contornar obstáculos e resolver o trajeto no menor número de comandos possível.

---

## 🚀 Como Rodar

### Pré-requisitos

- **Python 3.10+**

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/MigueXavier/trabalho_pygame.git
cd python-game

# 2. Crie e ative um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows (PowerShell)

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o jogo
python main.py
```

---

## 🕹️ Como Jogar

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  1. Analise o labirinto e os objetivos da fase           │
│                         ↓                               │
│  2. Monte sua sequência de blocos no painel              │
│                         ↓                               │
│  3. Clique em EXECUTAR para rodar a sequência            │
│                         ↓                               │
│  4. Observe o personagem seguindo seus comandos          │
│                         ↓                               │
│  5. Se não conseguir, perde uma vida e tenta de novo     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Objetivos

- Chegar até o final do labirinto
- Coletar os itens no **menor número de comandos possível**
- Evitar obstáculos

### Condição de vitória

> Chegar ao final da fase seguindo as regras impostas.

### Condição de derrota

> Perder todas as vidas sem chegar ao objetivo.

---

## 📋 Regras

| # | Regra |
|---|-------|
| 1 | O jogador começa no ponto **A** e deve chegar ao ponto **B** |
| 2 | Para chegar ao ponto B, ele deve definir a movimentação com **blocos de programação** |
| 3 | Caso não consiga completar a fase, perde **uma vida** |
| 4 | O jogador começa com **3 vidas** (tentativas) por fase |
| 5 | Caso as vidas acabem, a fase é reiniciada |
| 6 | O progresso (fase atual e recorde) é salvo automaticamente ao voltar ao menu |

---

## 🧩 Elementos do Jogo

### Personagem principal

Um personagem controlado pelos blocos de comando selecionados pelo jogador, com efeitos sonoros de passos, coleta e colisão.

### Obstáculos

Barreiras que impedem a passagem do personagem.

### Itens de interação

Itens coletáveis que aumentam a pontuação quando coletados.

### Pontuação, Vidas e Progresso

```
♥ ♥ ♥  →  3 vidas iniciais

⭐ Coletar um item      → +10 pontos
💀 Perder todas as vidas → reinicia a fase
🚪 Concluir as 3 fases  → vitória final
```

---

## 🕹️ Controles

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
║  [Rep xN] Bloco Repetir  → Repete N vezes os blocos      ║
║                            inseridos dentro dele         ║
║                                                          ║
║  Clique num bloco já colocado na sequência para          ║
║  removê-lo dela.                                         ║
║                                                          ║
║ ════════════════════════════════════════════════════════ ║
║                                                          ║
║  [ EXECUTAR ] → Roda a sequência de comandos montada     ║
║  [ RESET    ] → Limpa a sequência e reabilita os blocos  ║
║  [ SAIR     ] → Salva o progresso e volta ao menu        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🗂️ Organização do Código

```
trabalho_pygame/
│
├── main.py                →  Ponto de entrada; controla o loop Menu ⇄ Jogo
├── main.spec              →  Configuração do PyInstaller para geração do executável
├── dados.json             →  Persistência do progresso e recordes salvos
├── requirements.txt       →  Dependências do projeto (ex: pygame)
├── .gitignore             →  Arquivos e pastas ignorados pelo Git
│
├── src/
│   ├── jogo.py            →  Loop principal, montagem da sequência e execução
│   ├── menu.py            →  Menu inicial (Novo Jogo / Continuar / Créditos / Sair)
│   ├── menus_resultado.py →  Telas de Game Over e Vitória de cada fase
│   ├── configuracao.py    →  Constantes globais (tela, cores, layout, fases)
│   ├── personagem.py      →  Movimentação do jogador e efeitos sonoros
│   ├── blocos.py          →  Blocos de comando (direção e repetição)
│   ├── comandos.py        →  Botão genérico reutilizado pela interface
│   ├── matriz.py          →  Construção do labirinto a partir do JSON da fase
│   ├── barreira.py        →  Obstáculos e colisões do cenário
│   ├── item.py            →  Itens coletáveis que somam pontuação
│   ├── objetivo.py        →  Ponto de chegada e validação de fim de fase
│   ├── pontuacao.py       →  Contagem e persistência de pontos
│   ├── dados.py           →  Leitura/escrita do arquivo de save
│   ├── vidas.py           →  Desenho e controle das vidas (corações)
│   └── creditos.py        →  Tela de créditos (acessível pelo menu principal)
│
├── fases/                 →  Definição de cada fase em formato JSON
├── prototipos/            →  Esboços e códigos experimentais iniciais
│
├── assets/
│   ├── fontes/            →  Fonte pixelada usada na interface
│   ├── sons/              →  Trilha sonora e efeitos sonoros
│   └── sprites/           →  Spritesheet e elementos visuais
│
└── tests/
    └── teste_visual.py    →  Script de verificação visual dos componentes gráficos
```

---

## 📚 Recursos Externos e Bibliografia

Todos os recursos de terceiros respeitam suas respectivas licenças de uso gratuito.

### 🎨 Elementos Visuais e Sprites

- **Sprites do Labirinto e Personagens:** Obtidos em bancos de assets públicos gratuitos ([Itch.io](https://itch.io) / [Kenney.nl](https://kenney.nl))
- **Interface e Botões:** Customizados e renderizados via Pygame com formas geométricas e sprites nativos do projeto

### 🎵 Áudio e Efeitos Sonoros

- **Trilha Sonora de Fundo (BGM):** Músicas no formato Chiptune/8-bit obtidas em plataformas de domínio público
- **Efeitos Sonoros (SFX):** Sons de passos, cliques, erros de comando, coleta de itens e transições de tela obtidos de forma livre

### ✍️ Tipografia

- **Fonte Principal:** [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) — distribuída gratuitamente sob licença open-source pela Google Fonts

---

<div align="center">

> Feito com ☕, 🧠 e muito `print("debug")`

**Perdido no Algoritmo** — Projeto Acadêmico · 2026

</div>