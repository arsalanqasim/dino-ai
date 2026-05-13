"""Genetic evolution strategy for the agent population."""

from __future__ import annotations

import random

import pygame

from .entities import Agent


def evolve(
    population: list[Agent],
    sprite_data: dict[str, pygame.Surface],
    population_size: int,
    elitism_rate: float,
    mutation_rate: float,
) -> list[Agent]:
    population.sort(key=lambda x: x.fitness, reverse=True)
    new_population: list[Agent] = []

    elites_count = int(population_size * elitism_rate)
    for i in range(elites_count):
        new_population.append(Agent(sprite_data=sprite_data, brain=population[i].brain))

    top_performers = population[: int(population_size * 0.4)]
    target_with_crossover = population_size - int(population_size * 0.05)

    while len(new_population) < target_with_crossover:
        parent_a = random.choice(top_performers)
        parent_b = random.choice(top_performers)
        child_brain = parent_a.brain.crossover(parent_b.brain)
        child_brain.mutate(mutation_rate)
        new_population.append(Agent(sprite_data=sprite_data, brain=child_brain))

    while len(new_population) < population_size:
        new_population.append(Agent(sprite_data=sprite_data))

    return new_population[:population_size]
