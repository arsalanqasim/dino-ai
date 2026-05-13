"""Main game loop and per-generation simulation."""

from __future__ import annotations

import random

import pygame

from .config import (
    BASE_GAME_SPEED,
    BLACK,
    FPS,
    GAME_SPEED_STEP,
    GROUND_Y,
    HEIGHT,
    MAX_GAME_SPEED,
    SKY_COLOR,
    WIDTH,
)
from .entities import Agent, Obstacle


class DinoGame:
    def __init__(self, sprite_data: dict[str, pygame.Surface]) -> None:
        self.sprite_data = sprite_data
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dino AI Evolution")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.generation = 1
        self.high_score = 0

    @staticmethod
    def get_next_obstacles(agents: list[Agent], obstacles: list[Obstacle]) -> list[Obstacle]:
        if not agents:
            return []

        agent_x = agents[0].x
        upcoming = [obs for obs in obstacles if obs.rect.x + obs.rect.width > agent_x]
        return upcoming[:2]

    def play_generation(self, population: list[Agent]) -> None:
        agents = population[:]
        obstacles: list[Obstacle] = []
        speed = BASE_GAME_SPEED
        spawn_timer = 0
        ground_x = 0

        running = True
        while running and agents:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            speed = min(MAX_GAME_SPEED, speed + GAME_SPEED_STEP)

            spawn_timer -= 1
            if spawn_timer <= 0:
                obstacles.append(Obstacle(self.sprite_data))
                speed_scale = speed / BASE_GAME_SPEED
                spawn_timer = random.randint(int(60 / speed_scale), int(120 / speed_scale))

            next_obstacles = self.get_next_obstacles(agents, obstacles)

            for agent in agents:
                agent.think(next_obstacles, speed)
                agent.update()

            for obstacle in obstacles:
                obstacle.update(speed)

            alive_agents: list[Agent] = []
            for agent in agents:
                collision = False
                hitbox = agent.rect.inflate(-15, -15)

                for obstacle in obstacles:
                    obstacle_hitbox = obstacle.rect.inflate(-15, -15)
                    if hitbox.colliderect(obstacle_hitbox):
                        collision = True
                        break

                if collision:
                    agent.dead = True
                    agent.fitness = agent.score
                else:
                    alive_agents.append(agent)

            agents = alive_agents
            obstacles = [obs for obs in obstacles if obs.rect.x + obs.rect.width > 0]

            self.screen.fill(SKY_COLOR)
            ground_x -= speed
            if ground_x <= -1200:
                ground_x = 0

            self.screen.blit(self.sprite_data["ground"], (ground_x, GROUND_Y - 10))
            self.screen.blit(self.sprite_data["ground"], (ground_x + 1200, GROUND_Y - 10))

            for obstacle in obstacles:
                obstacle.draw(self.screen)
            for agent in agents:
                agent.draw(self.screen)

            current_score = max((a.score for a in agents), default=0)
            best_score = max((a.score for a in population), default=0)
            self.high_score = max(self.high_score, current_score, best_score)

            text_gen = self.font.render(f"Gen: {self.generation}", True, BLACK)
            text_alive = self.font.render(f"Alive: {len(agents)}", True, BLACK)
            text_score = self.font.render(f"Score: {current_score // 10}", True, BLACK)
            text_hi = self.font.render(f"HI: {self.high_score // 10}", True, BLACK)

            self.screen.blit(text_gen, (10, 10))
            self.screen.blit(text_alive, (10, 40))
            self.screen.blit(text_score, (WIDTH - 150, 40))
            self.screen.blit(text_hi, (WIDTH - 150, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        for agent in population:
            if agent.fitness == 0:
                agent.fitness = agent.score
