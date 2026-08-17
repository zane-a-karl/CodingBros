# CodingBros TicTacToe

A TicTacToe game built by two brothers using [Pygame](https://www.pygame.org/), featuring both local play against a CPU opponent and online multiplayer over a network so you can play with a friend from a distance.

## Features

- 🎮 **Local vs CPU** — Play against a computer-controlled opponent on the same machine.
- 🌐 **Online with a Friend** — Connect over a network to play remotely in real time.
- 🖼️ **Custom UI** — Custom fonts, images, and sound effects for a polished game feel.
- ⚙️ **Configurable** — Contact/connection settings managed via a config file for online play.

## Project Structure

```
CODINGBROS/
├── font/                          # Custom fonts used in the UI
├── images/                        # Game sprites and UI images
├── misc/                          # Miscellaneous assets/utilities
├── sounds/                        # Sound effects and audio
├── src/
│   └── TicTacToe.py               # Main game entry point
├── contacts-template.config.json  # Template config for setting up online play
├── pyproject.toml                 # Project metadata and dependencies
├── uv.lock                        # Locked dependency versions
└── README.md
```

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management and running the project

## Installation

1. Install `uv` if you don't already have it:

   **macOS/Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **Windows (PowerShell):**
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Clone the repository:
   ```bash
   git clone <repo-url>
   cd CODINGBROS
   ```

3. That's it — `uv` will handle setting up the virtual environment and installing dependencies automatically when you run the game.

## Running the Game

From the project root:

```bash
uv run src/TicTacToe.py
```

This will create a local virtual environment (if one doesn't exist), install all dependencies from `uv.lock`, and launch the game.

## How to Play

1. Launch the game using the command above.
2. Choose a game mode from the main menu:
   - **Vs CPU** — Play locally against a computer opponent.
   - **Online with Friend** — Connect with another player over the network.
3. For online play, copy `contacts-template.config.json` and fill in the connection details needed to link up with your opponent.
4. Take turns placing X's and O's — first to get three in a row wins!

## Tech Stack

- **[Pygame](https://www.pygame.org/)** — Game rendering, input handling, and UI
- **[pygame-popup](https://pypi.org/project/pygame-popup/)** — In-game popups/UI elements
- Python's networking stack for online multiplayer

## Authors

Built by two brothers as a project to learn game development and networking in Python.

## License

_Add license information here if applicable._
