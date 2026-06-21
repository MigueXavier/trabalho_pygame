# Proposta do Trabalho Prático

> **Nota:** este documento foi estruturado a partir do conteúdo já consolidado no `README.md` e nas demais entregas do projeto, seguindo o formato comum de propostas de trabalho prático (identificação, justificativa, objetivos, mecânicas, tecnologias e cronograma). Como o enunciado oficial está disponível apenas via login institucional no Canvas, recomenda-se que o grupo confira esta proposta contra o template/critérios exatos exigidos pelo professor antes do envio final, ajustando seções específicas se necessário.

---

## 1. Identificação

| Campo | Informação |
|---|---|
| **Nome do jogo** | Perdido no Algoritmo |
| **Gênero** | Puzzle de lógica / programação em blocos |
| **Engine / Tecnologia** | Python 3.10+ com Pygame |
| **Integrantes** | Arthur Fernandes Fialho e Silva, Arthur Rodrigues de Macedo, Miguel Xavier dos Santos, Pamela Fernandes Nilo, Túlio Marcus de Oliveira Gonçalves |

---

## 2. Tema e Justificativa

**Perdido no Algoritmo** propõe ensinar e exercitar, de forma lúdica, os conceitos fundamentais de **sequenciamento de instruções** e **estruturas de repetição (laços)** — pilares de qualquer disciplina introdutória de lógica de programação.

Em vez de controlar o personagem diretamente pelo teclado, o jogador deve **compor um programa** com blocos de comando (mover para cima, baixo, esquerda, direita e repetir) e executá-lo de uma vez, observando o resultado. Esse formato aproxima a experiência de jogo da experiência de programar de fato: planejar antes de executar, prever o comportamento do código e depurar quando o resultado não é o esperado.

A escolha por um labirinto progressivo, com fases que aumentam em complexidade, reforça o uso de laços de repetição como ferramenta para reduzir o número de comandos necessários — incentivando o jogador a buscar soluções mais eficientes, e não apenas soluções que funcionem.

---

## 3. Descrição da Proposta

O jogo apresenta um personagem posicionado em um cenário organizado em grade (labirinto). Nesse cenário existem:

- **Obstáculos**, que bloqueiam a passagem;
- **Itens coletáveis**, que somam pontos quando alcançados;
- **Um objetivo final**, que marca a conclusão da fase.

Por meio de um painel lateral de blocos de comando, o jogador monta uma sequência de instruções (incluindo blocos de repetição com quantidade configurável) e clica em **Executar** para que o personagem siga essa sequência passo a passo, com efeitos visuais e sonoros a cada movimento, coleta ou colisão.

O jogo é dividido em **3 fases**, com dificuldade crescente, progresso salvo automaticamente e um sistema de vidas que limita o número de tentativas por fase.

---

## 4. Objetivos

### 4.1 Objetivo Geral

Desenvolver um jogo 2D funcional em Python/Pygame que trabalhe, por meio de mecânicas de jogo, os conceitos de sequência lógica e repetição aplicados à movimentação de um personagem em um labirinto.

### 4.2 Objetivos Específicos

- Implementar um sistema de blocos de comando arrastáveis/clicáveis, incluindo um bloco de repetição com parâmetro configurável;
- Implementar um motor de execução de comandos que interprete a sequência montada pelo jogador e movimente o personagem de forma sequencial e temporizada;
- Implementar detecção de colisão com obstáculos, coleta de itens e identificação do objetivo da fase;
- Implementar sistema de vidas, pontuação e progressão entre fases;
- Implementar persistência de progresso (fase atual e recorde) entre execuções do jogo;
- Organizar o código em módulos coesos, orientados a objetos, facilitando manutenção e extensão por múltiplos integrantes do grupo;
- Cobrir as principais regras de negócio do jogo com testes automatizados.

---

## 5. Mecânicas e Regras

| # | Regra |
|---|-------|
| 1 | O jogador começa no ponto **A** e deve chegar ao ponto **B** |
| 2 | A movimentação é definida por meio de **blocos de programação**, não pelo teclado |
| 3 | Caso a sequência termine sem que o personagem chegue ao objetivo, ele perde **uma vida** |
| 4 | O jogador começa com **3 vidas** (tentativas) por fase |
| 5 | Se as vidas acabarem, a fase é reiniciada |
| 6 | O progresso (fase atual e recorde) é salvo automaticamente |

**Condição de vitória:** chegar ao final da fase seguindo as regras impostas.
**Condição de derrota:** perder todas as vidas sem chegar ao objetivo.

---

## 6. Tecnologias e Ferramentas

- **Linguagem:** Python 3.10+
- **Biblioteca gráfica:** Pygame (renderização, eventos, áudio)
- **Persistência:** arquivos JSON (`dados.json` para progresso/recorde, `fases/*.json` para definição de cada fase)
- **Empacotamento:** PyInstaller (`main.spec`), para gerar um executável standalone
- **Testes:** Pytest, com suíte de testes automatizados em `tests/`
- **Controle de versão:** Git/GitHub, com desenvolvimento distribuído entre integrantes por meio de branches mescladas ao branch principal

---

## 7. Conceitos da Disciplina Aplicados

- **Sequenciamento e estruturas de repetição:** mecânica central do jogo, traduzida na montagem e execução dos blocos de comando;
- **Programação orientada a objetos:** entidades do jogo (`Personagem`, `Barreira`, `Item`, `Objetivo`, `Bloco` e subclasses, `Jogo`, `Menu`) implementadas como classes com responsabilidades bem definidas;
- **Estruturas de dados:** matrizes (listas de listas) para representar o labirinto; listas para a sequência de comandos montada;
- **Manipulação de arquivos e serialização:** leitura/escrita de JSON para fases e para o save do jogador;
- **Máquina de estados:** controle do fluxo entre menu, fase em andamento, pausa, game over e vitória;
- **Tratamento de eventos:** loop de eventos do Pygame para entrada do usuário (mouse e teclado);
- **Testes automatizados:** verificação programática de regras de negócio (persistência, pontuação, blocos e movimentação) independente da interface gráfica.

---

## 8. Organização do Código

A estrutura completa de pastas e a responsabilidade de cada módulo estão detalhadas na seção [Organização do Código](../README.md#️-organização-do-código) do `README.md`, mantida como fonte única de verdade para não duplicar informação entre os documentos.

---

## 9. Testes

A pasta `tests/` contém:

- **Testes automatizados (Pytest)**, cobrindo persistência de dados (`dados.py`), pontuação (`pontuacao.py`), blocos de comando (`blocos.py`), construção do labirinto a partir do JSON da fase (`matriz.py`), movimentação/colisão/coleta/condição de vitória do personagem (`personagem.py`) e a integridade estrutural dos arquivos de fase (`fases/*.json`);
- **Teste visual manual** (`teste_visual.py`), utilizado para inspeção visual rápida da renderização dos componentes gráficos durante o desenvolvimento.

Instruções de execução estão na seção *Como Rodar os Testes* do `README.md`.

---

## 10. Cronograma (Pontos de Controle)

| Ponto de Controle | Entrega |
|---|---|
| 01 | Definição da proposta inicial, mecânica principal e protótipo básico (ver `prototipos/`) |
| 02 | Estruturação do código em módulos, primeira fase jogável |
| 03 | Sistema de fases, persistência de progresso, efeitos sonoros, interface refinada |
| 04 *(atual)* | Versão final do jogo completa e funcional, README atualizado, proposta documentada, testes implementados e referências de recursos externos |

---

## 11. Referências e Recursos Externos

Todos os recursos de terceiros utilizados respeitam suas respectivas licenças de uso gratuito. Lista completa na seção [Recursos Externos e Bibliografia](../README.md#-recursos-externos-e-bibliografia) do `README.md`.