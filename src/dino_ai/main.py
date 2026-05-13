"""Application entry point for the Dino AI simulation."""

from __future__ import annotations

import pygame

from .assets import load_sprites
from .config import ELITISM_RATE, MUTATION_RATE, POPULATION_SIZE
from .entities import Agent
from .evolution import evolve
from .game import DinoGame


def run() -> None:
    pygame.init()
    sprites = load_sprites()

    game = DinoGame(sprite_data=sprites)
    population = [Agent(sprite_data=sprites) for _ in range(POPULATION_SIZE)]

    while True:
        game.play_generation(population)
        population = evolve(
            population=population,
            sprite_data=sprites,
            population_size=POPULATION_SIZE,
            elitism_rate=ELITISM_RATE,
            mutation_rate=MUTATION_RATE,
        )
        game.generation += 1


def main() -> None:
    run()


if __name__ == "__main__":
    main()
