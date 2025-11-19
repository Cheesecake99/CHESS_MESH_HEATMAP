# Chess Heatmap Visualizer - Project Summary

## Overview
This program visualizes chess games as heatmaps where each piece is represented by its point value, creating an intensity-based visualization of the board state throughout a game.

## Piece Value System
- **Queen**: 10 points (brightest/hottest)
- **Rook**: 5 points
- **King**: 4 points
- **Bishop**: 3 points
- **Knight**: 3 points
- **Pawn**: 1 point (dimmest/coolest)

## Project Structure

```
CHESS_MESH_HEATMAP/
├── chess_heatmap.py    # Main visualizer class
├── cli.py              # Command-line interface
├── examples.py         # Usage examples
├── quickstart.py       # Simple demo script
├── sample_game.pgn     # Sample chess game
├── requirements.txt    # Python dependencies
└── README.md           # Full documentation
```

## Key Features

### 1. PGN Game Loading
- Load from Chess.com PGN format
- Load from file or string
- Automatic parsing of moves and positions

### 2. Three Visualization Modes

#### Interactive Step-Through (Default)
```python
visualizer.step_through_game()
```
Use arrow keys to navigate through moves.

#### Animated Playback
```python
visualizer.animate_game(interval=500)
```
Watch the game play automatically with customizable speed.

#### Static Position View
```python
visualizer.visualize_static(move_index=10)
```
View any specific position in the game.

### 3. Heatmap Visualization
- Color-coded intensity based on piece values
- Numbers displayed on each square
- Custom color gradient (dark → orange → red → magenta)
- Proper chess board coordinates (a-h, 1-8)

## Quick Start Guide

### Simplest Way to Run
```bash
python quickstart.py
```

### Run with Your Own Game
1. Download PGN from Chess.com (Share → Copy PGN)
2. Save to a `.pgn` file
3. Run:
```bash
python cli.py your_game.pgn
```

### Interactive Python
```python
from chess_heatmap import ChessHeatmapVisualizer

visualizer = ChessHeatmapVisualizer()
game = visualizer.load_pgn_from_file('sample_game.pgn')
visualizer.process_game(game)
visualizer.step_through_game()
```

## Technical Implementation

### Core Components

1. **ChessHeatmapVisualizer Class**
   - Manages game state and visualization
   - Converts chess positions to numerical arrays
   - Handles multiple display modes

2. **Board State Tracking**
   - Uses python-chess library for move validation
   - Converts piece positions to 8x8 numpy arrays
   - Maintains full game history

3. **Visualization Engine**
   - Matplotlib for rendering
   - Seaborn for heatmap styling
   - Custom colormap for intensity display

### Key Methods

- `load_pgn_from_file(filename)` - Load PGN from file
- `load_pgn_from_string(pgn_string)` - Load PGN from string
- `process_game(game)` - Parse all moves and create heatmaps
- `visualize_static(move_index)` - Show single position
- `animate_game(interval, save_as)` - Create animation
- `step_through_game()` - Interactive navigation

## Usage Examples

### Example 1: Simple Demo
```bash
python quickstart.py
```

### Example 2: Load and Explore
```bash
python examples.py
# Choose option 1, 2, or 3
```

### Example 3: Command Line
```bash
# Interactive mode
python cli.py sample_game.pgn

# Animated mode
python cli.py sample_game.pgn --animate

# Save as GIF
python cli.py sample_game.pgn --animate --save game.gif

# View specific move
python cli.py sample_game.pgn --move 20
```

## Customization Options

### Modify Piece Values
Edit in `chess_heatmap.py`:
```python
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 10,
    chess.KING: 4
}
```

### Change Animation Speed
```python
visualizer.animate_game(interval=1000)  # 1 second per move
```

### Modify Color Scheme
Edit in `chess_heatmap.py`:
```python
colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
```

## Dependencies
- `chess` - Chess game logic and PGN parsing
- `matplotlib` - Plotting and animation
- `numpy` - Numerical array operations
- `seaborn` - Enhanced heatmap styling

## How to Get PGN Files

### Chess.com
1. Go to your game
2. Click "Share" 
3. Select "Copy PGN"
4. Save to `.pgn` file

### Lichess.org
1. Open any game
2. Click "Share & Export"
3. Download PGN

## Future Enhancement Ideas
- Cumulative heatmap (all positions overlaid)
- Separate heatmaps for white vs black pieces
- Attack/defense heatmaps
- Integration with Stockfish for evaluation overlay
- Multiple game comparison
- 3D visualization option

## Troubleshooting

**Q: Heatmap doesn't show**
A: Ensure matplotlib backend is properly configured. Try running in interactive mode.

**Q: Animation too fast/slow**
A: Adjust the `interval` parameter (in milliseconds).

**Q: PGN won't load**
A: Verify the PGN format is valid. Most Chess.com and Lichess games work fine.

**Q: Arrow keys don't work**
A: Make sure the matplotlib window has focus (click on it).

## Performance Notes
- Games with 100+ moves work smoothly
- Animation can be saved to GIF (requires pillow) or MP4 (requires ffmpeg)
- Static views are instantaneous
- Step-through mode has no memory overhead

## License
Open source - free for educational and personal use.

---

**Ready to visualize some chess?** Run `python quickstart.py` to get started!
