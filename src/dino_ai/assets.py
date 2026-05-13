"""Sprite sheet download and extraction helpers."""

from __future__ import annotations

from pathlib import Path
import urllib.request

import pygame

from .config import SPRITE_SHEET_FILENAME, SPRITE_SHEET_URL


def _assets_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "assets"


def _sprite_sheet_path() -> Path:
    return _assets_dir() / SPRITE_SHEET_FILENAME


def ensure_sprite_sheet() -> Path:
    assets_dir = _assets_dir()
    assets_dir.mkdir(parents=True, exist_ok=True)

    path = _sprite_sheet_path()
    if not path.exists():
        print("Downloading sprite sheet...")
        urllib.request.urlretrieve(SPRITE_SHEET_URL, path)

    return path


def _get_sprite(sprite_sheet: pygame.Surface, x: int, y: int, w: int, h: int) -> pygame.Surface:
    sprite = pygame.Surface((w, h), pygame.SRCALPHA)
    sprite.blit(sprite_sheet, (0, 0), (x, y, w, h))
    return sprite


def load_sprites() -> dict[str, pygame.Surface]:
    sprite_path = ensure_sprite_sheet()
    sprite_sheet = pygame.image.load(str(sprite_path))

    return {
        "dino_idle": _get_sprite(sprite_sheet, 40, 0, 44, 47),
        "dino_run1": _get_sprite(sprite_sheet, 848, 2, 44, 47),
        "dino_run2": _get_sprite(sprite_sheet, 892, 2, 44, 47),
        "dino_duck1": _get_sprite(sprite_sheet, 1112, 19, 59, 30),
        "dino_duck2": _get_sprite(sprite_sheet, 1171, 19, 59, 30),
        "cactus_small": _get_sprite(sprite_sheet, 228, 2, 17, 35),
        "cactus_large": _get_sprite(sprite_sheet, 332, 2, 25, 50),
        "ptero1": _get_sprite(sprite_sheet, 134, 2, 46, 40),
        "ptero2": _get_sprite(sprite_sheet, 180, 2, 46, 40),
        "ground": _get_sprite(sprite_sheet, 2, 54, 1200, 12),
    }
