# Chess Heatmap Visualizer

A Python-based chess game visualizer that displays games as interactive heatmaps, where each piece is represented by its point value. Features attack wave animations and multiple visualization modes.

## Demo

[Watch the demo video](chess_game_pieces.mp4)

![Chess Heatmap](https://raw.githubusercontent.com/Cheesecake99/CHESS_MESH_HEATMAP/main/chess_game_pieces.mp4)

## Features

- **Piece Value Mapping**: Each piece has a numerical value (Queen=10, Rook=5, Bishop=3, Knight=3, Pawn=1, King=4)
- **Unicode Piece Symbols**: Display pieces as ♙♘♗♖♕♔ or numerical values
- **Attack Wave Animations**: Visual effects showing possible captures with traveling wave patterns
- **PGN Support**: Load games from Chess.com or any standard PGN format
- **Multiple Visualization Modes**:
  - Static view of any position
  - Animated playback of entire game
  - Interactive step-through with keyboard controls
  - Export to MP4/GIF video files
- **Heatmap Intensity**: Color-coded visualization showing piece concentrations
- **Full Playback Controls**: Buttons, sliders, and keyboard shortcuts

## Installation

1. Make sure you have Python 3.7+ installed

2. Install required dependencies:
```bash
pip install python-chess matplotlib numpy seaborn imageio imageio-ffmpeg
```

Or use the virtual environment (already set up):
```bash
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/MacOS
```

## Usage

### Quick Start - Interactive Mode

Run the test script to see the interactive visualizer:
```bash
python test_interactive.py
```

**Controls:**
- **Arrow Keys**: LEFT (previous) | RIGHT (next) | SPACE (play/pause)
- **Buttons**: First | Prev | Play/Pause | Next | Last
- **Speed Slider**: Adjust playback speed (100-2000 ms)
- **Show Pieces**: Toggle between piece symbols (♙♘♗♖♕♔) and values (1,3,5,10)
- **Show Rays**: Toggle attack square highlighting with wave effects
- **Ray Color**: Select highlight color (Red/Blue/Green/Yellow/Magenta/Cyan)

### Record to Video

Generate an MP4 video of your game:
```bash
python record_game.py
```

This creates `chess_game_pieces.mp4` with all wave animations included.

### Loading Games

#### From PGN File
```python
from chess_heatmap import ChessHeatmapVisualizer

visualizer = ChessHeatmapVisualizer()
game = visualizer.load_pgn_from_file('your_game.pgn')
visualizer.process_game(game)
```

#### From PGN String
```python
pgn_string = """
[Event "My Game"]
[Site "Chess.com"]
[Date "2025.11.19"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
"""

visualizer = ChessHeatmapVisualizer()
game = visualizer.load_pgn_from_string(pgn_string)
visualizer.process_game(game)
```

### Visualization Modes

#### 1. Interactive Step-Through (Recommended)
Navigate through the game move by move using arrow keys:
```python
visualizer.step_through_game()
# Use LEFT/RIGHT arrow keys to navigate
```

#### 2. Animated Playback
Watch the entire game play out automatically:
```python
visualizer.animate_game(interval=500)  # 500ms between moves
```

Save animation to file:
```python
visualizer.animate_game(interval=500, save_as='my_game.gif')
```

#### 3. Static Position View
View a specific move:
```python
visualizer.visualize_static(move_index=10)  # View move 10
```

## Piece Values

The heatmap uses the following piece values:
- **Queen**: 10 points (brightest/hottest)
- **Rook**: 5 points
- **King**: 4 points
- **Bishop**: 3 points
- **Knight**: 3 points
- **Pawn**: 1 point (dimmest/coolest)

## How to Get PGN Files

### From Chess.com
1. Go to your game
2. Click the "Share" button
3. Select "Copy PGN"
4. Paste into a `.pgn` file

### From Lichess.org
1. Open any game
2. Click "Share & Export"
3. Download PGN

## Example Output

The heatmap shows:
- **Dark colors**: Empty squares or low-value pieces (pawns)
- **Medium colors**: Medium-value pieces (bishops, knights, rooks)
- **Bright colors**: High-value pieces (queens)
- **Numbers**: The exact piece value on each square

## Files Included

- `chess_heatmap.py` - Main visualizer class
- `examples.py` - Usage examples
- `sample_game.pgn` - Sample chess game for testing
- `README.md` - This file

## Controls (Interactive Mode)

- **RIGHT Arrow**: Next move
- **LEFT Arrow**: Previous move
- **Close Window**: Exit

## Customization

You can modify piece values in `chess_heatmap.py`:
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

## Requirements

- Python 3.7+
- chess (python-chess library)
- matplotlib
- numpy
- seaborn

## License

This project is open source and available for educational purposes.

## Future Enhancements

Potential features to add:
- Cumulative heatmap showing all positions throughout the game
- Separate heatmaps for white and black pieces
- Export individual frames as images
- Side-by-side comparison of multiple games
- Integration with chess engines for evaluation overlay

## Troubleshooting

**Issue**: Animation is too fast/slow
- Adjust the `interval` parameter (in milliseconds)

**Issue**: Can't see the heatmap
- Make sure matplotlib is properly installed
- Try running with `plt.show()` in interactive Python shell

**Issue**: PGN file won't load
- Verify the PGN format is valid
- Check that the file path is correct

## Contact

For questions or suggestions, please open an issue on the repository.
