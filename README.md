# Dino AI Evolution

A Python project that trains Dino agents using a simple neural network + genetic algorithm, then visualizes each generation in a pygame simulation.

## Demo

<video src="https://github.com/arsalanqasim/dino-ai/blob/main/assets/dino-ai-demo-video.mp4" controls muted autoplay loop playsinline width="100%">
	Your browser does not support the video tag.
</video>

## Highlights

- Neuroevolution loop with crossover, mutation, and elitism
- Multiple obstacle types (small cactus, large cactus, ptero)
- Difficulty scaling via increasing game speed
- Modular project structure for maintainability and extension

## Project Structure

```text
.
├── assets/
│   ├── dino-ai-demo.mp4
│   └── sprite.png
├── src/
│   └── dino_ai/
│       ├── assets.py
│       ├── config.py
│       ├── entities.py
│       ├── evolution.py
│       ├── game.py
│       ├── main.py
│       └── neural.py
├── tests/
│   └── test_neural.py
├── pyproject.toml
├── requirements.txt
└── run.py
```

## Quick Start

1. Create and activate a virtual environment
2. Install dependencies
3. Run the simulation

```bash
pip install -r requirements.txt
python run.py
```

## Development

Install dev tools:

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Roadmap Ideas

- Save and load best agent brains
- Plot generation fitness over time
- Add keyboard/manual mode for comparison
- Add CI workflow for tests + lint

## License

MIT
