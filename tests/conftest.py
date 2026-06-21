"""
Configuração compartilhada da suíte de testes.

Roda o Pygame em modo headless (sem janela/áudio reais), usando os
drivers "dummy" do SDL, e garante que a raiz do projeto esteja no
sys.path para que os imports `from src.xxx import yyy` funcionem.

IMPORTANTE: os módulos do jogo carregam assets com caminhos relativos
(ex.: "assets/sprites/..."), portanto os testes devem ser executados
a partir da raiz do projeto:

    pytest
"""

import os

# Precisa ser definido ANTES de importar pygame.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import sys
from pathlib import Path

import pygame
import pytest

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))


@pytest.fixture(scope="session", autouse=True)
def pygame_headless():
    """Inicializa o Pygame uma única vez para toda a sessão de testes."""
    os.chdir(RAIZ_PROJETO)
    pygame.init()
    pygame.display.set_mode((200, 200))
    yield
    pygame.quit()
