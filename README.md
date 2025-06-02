# Chess Engine Battle Program

A Python program for running automated games between different chess engines, specifically designed to pit Leela Chess Zero against Stockfish on a Raspberry Pi 4.

## Overview

This repository contains a chess engine battle program that facilitates automated matches between popular chess engines. The program handles engine communication via UCI (Universal Chess Interface), manages game flow, prevents draws by replaying games, and outputs results in standard PGN format.

## Features

- **Engine vs Engine Battles**: Run automated games between different chess engines
- **Draw Handling**: Automatically replays games that end in draws until a decisive result
- **PGN Output**: Saves games in standard Portable Game Notation format with timestamped filenames
- **Detailed Logging**: Comprehensive logging of moves, positions, and game statistics
- **Configurable Time Limits**: Set thinking time limits for engines
- **Multiple Game Support**: Run series of games with automatic game counting

## Supported Engines

The program is configured to work with:
- **Leela Chess Zero (lc0)** - Neural network-based chess engine
- **Stockfish** - Traditional alpha-beta search engine  
- **Drofa** - Additional engine option (currently configured but not actively used)

## Requirements

### Software Dependencies
- Python 3.x
- `python-chess` library for chess logic and engine communication
- Chess engines installed on the system

### Hardware Requirements
- Designed for Raspberry Pi 4 (but can be adapted for other systems)
- Sufficient storage for PGN files and log files

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install python-chess
   ```

2. **Install chess engines:**
   - Download and compile Stockfish
   - Download and compile Leela Chess Zero
   - Download and compile Drofa (optional)

3. **Update engine paths in the script:**
   Edit `chess_e1_vs_e2.py` and update the paths to match your engine installations:
   ```python
   sf    = '/path/to/your/stockfish/binary'
   lc0   = '/path/to/your/lc0/binary'
   drofa = '/path/to/your/drofa/binary'
   ```

## Configuration

Key configuration variables in `chess_e1_vs_e2.py`:

- `LIMIT`: Time limit per move in seconds (default: 1)
- `TOTAL_GAMES`: Number of games to play in the session (default: 1)

## Usage

Run the program directly:
```bash
python3 chess_e1_vs_e2.py
```

The program will:
1. Create a timestamped PGN file for the session
2. Play the configured number of games
3. Log all moves and game information
4. Handle draws by replaying until decisive results
5. Save final results to the PGN file

## Output Files

- **PGN Files**: `chess_games_YYYYMMDDHHMMSS.pgn` - Contains game results in standard chess notation
- **Log Files**: `chess.log` - Detailed logging of moves, positions, and game statistics

## Technical Details

- Uses UCI protocol for engine communication
- Implements automatic draw detection and replay logic
- Tracks FEN positions for each move
- Generates proper PGN headers with event information
- Handles engine process management (start/stop)

## Example PGN Output

```
[Event "chess engines playing with limit: 1"]
[Site "raspberry Pi4"] 
[Date "2024.01.15"]
[Round "1"]
[White "LEELA"]
[Black "STOCKFISH"]
[Result "1-0"]
```

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
