"""Game entities: agents and obstacles."""

from __future__ import annotations

import random

import pygame

from .config import (
    GROUND_Y,
    HEIGHT,
    JUMP_POWER,
    MAX_GAME_SPEED,
    WIDTH,
    GRAVITY,
)
from .neural import NeuralNetwork


class Agent:
    def __init__(self, sprite_data: dict[str, pygame.Surface], brain: NeuralNetwork | None = None) -> None:
        self.sprite_data = sprite_data
        self.brain = brain.clone() if brain else NeuralNetwork(11, 10, 2)

        self.fitness = 0
        self.score = 0
        self.x = 50
        self.y = GROUND_Y - 47
        self.velocity = 0
        self.on_ground = True
        self.is_ducking = False
        self.anim_timer = 0
        self.rect = pygame.Rect(self.x, self.y, 44, 47)
        self.dead = False

    def get_inputs(self, next_obstacles: list["Obstacle"], speed: float) -> list[float]:
        inputs = [
            self.y / HEIGHT,
            self.velocity / 15,
            speed / MAX_GAME_SPEED,
            1.0,
            0.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
        ]

        if len(next_obstacles) > 0:
            obs1 = next_obstacles[0]
            inputs[3] = (obs1.rect.x - self.x) / WIDTH
            inputs[4] = obs1.rect.width / WIDTH
            inputs[5] = obs1.rect.height / HEIGHT
            inputs[6] = obs1.rect.y / HEIGHT

        if len(next_obstacles) > 1:
            obs2 = next_obstacles[1]
            inputs[7] = (obs2.rect.x - self.x) / WIDTH
            inputs[8] = obs2.rect.width / WIDTH
            inputs[9] = obs2.rect.height / HEIGHT
            inputs[10] = obs2.rect.y / HEIGHT

        return inputs

    def jump(self) -> None:
        if self.on_ground and not self.is_ducking:
            self.velocity = JUMP_POWER
            self.on_ground = False

    def duck(self, state: bool) -> None:
        if self.on_ground:
            self.is_ducking = state

    def think(self, next_obstacles: list["Obstacle"], speed: float) -> None:
        inputs = self.get_inputs(next_obstacles, speed)
        outputs = self.brain.predict(inputs)

        if outputs[0] > 0.5:
            self.jump()

        if outputs[1] > 0.5:
            self.duck(True)
        else:
            self.duck(False)

    def update(self) -> None:
        if not self.on_ground:
            self.velocity += GRAVITY
            self.y += self.velocity
            if self.y >= GROUND_Y - 47:
                self.y = GROUND_Y - 47
                self.velocity = 0
                self.on_ground = True

        if self.is_ducking and self.on_ground:
            self.rect = pygame.Rect(self.x, GROUND_Y - 30, 59, 30)
        else:
            self.rect = pygame.Rect(self.x, self.y, 44, 47)

        self.anim_timer += 1
        self.score += 1

    def draw(self, screen: pygame.Surface) -> None:
        if self.dead:
            screen.blit(self.sprite_data["dino_idle"], (self.rect.x, self.rect.y))
        elif not self.on_ground:
            screen.blit(self.sprite_data["dino_idle"], (self.rect.x, self.rect.y))
        elif self.is_ducking:
            if (self.anim_timer // 5) % 2 == 0:
                screen.blit(self.sprite_data["dino_duck1"], (self.rect.x, self.rect.y))
            else:
                screen.blit(self.sprite_data["dino_duck2"], (self.rect.x, self.rect.y))
        else:
            if (self.anim_timer // 5) % 2 == 0:
                screen.blit(self.sprite_data["dino_run1"], (self.rect.x, self.rect.y))
            else:
                screen.blit(self.sprite_data["dino_run2"], (self.rect.x, self.rect.y))


class Obstacle:
    def __init__(self, sprite_data: dict[str, pygame.Surface]) -> None:
        self.sprite_data = sprite_data
        self.passed = False
        obs_type = random.choices(
            ["small_cactus", "large_cactus", "ptero"], weights=[40, 40, 20]
        )[0]

        if obs_type == "small_cactus":
            count = random.randint(1, 3)
            self.sprite = pygame.Surface((17 * count, 35), pygame.SRCALPHA)
            for i in range(count):
                self.sprite.blit(self.sprite_data["cactus_small"], (i * 17, 0))
            self.rect = pygame.Rect(WIDTH, GROUND_Y - 35, 17 * count, 35)
            self.type = "cactus"
        elif obs_type == "large_cactus":
            count = random.randint(1, 3)
            self.sprite = pygame.Surface((25 * count, 50), pygame.SRCALPHA)
            for i in range(count):
                self.sprite.blit(self.sprite_data["cactus_large"], (i * 25, 0))
            self.rect = pygame.Rect(WIDTH, GROUND_Y - 50, 25 * count, 50)
            self.type = "cactus"
        else:
            self.type = "ptero"
            ptero_heights = [GROUND_Y - 30, GROUND_Y - 50, GROUND_Y - 75]
            self.y = random.choice(ptero_heights)
            self.rect = pygame.Rect(WIDTH, self.y, 46, 40)
            self.anim_timer = 0

    def update(self, speed: float) -> None:
        self.rect.x -= speed
        if self.type == "ptero":
            self.anim_timer += 1
            self.rect.x -= speed * 0.2

    def draw(self, screen: pygame.Surface) -> None:
        if self.type == "cactus":
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            if (self.anim_timer // 10) % 2 == 0:
                screen.blit(self.sprite_data["ptero1"], (self.rect.x, self.rect.y))
            else:
                screen.blit(self.sprite_data["ptero2"], (self.rect.x, self.rect.y))
