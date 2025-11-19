# Getting Started with Chess Heatmap Visualizer

## Quick Start (3 Steps!)

### Step 1: Run the Demo
```bash
python quickstart.py
```
This will show you a simple chess game visualized as a heatmap.

### Step 2: Try the Sample Game
```bash
python cli.py sample_game.pgn
```
This loads the famous "Immortal Game" from 1851!

### Step 3: Use Your Own Game
1. Go to Chess.com and play/find a game
2. Click **Share → Copy PGN**
3. Save to a file like `my_game.pgn`
4. Run: `python cli.py my_game.pgn`

## How It Works

Each chess piece has a point value:
- **Queen = 10** (brightest on heatmap)
- **Rook = 5**
- **King = 4**
- **Bishop = 3**
- **Knight = 3**
- **Pawn = 1** (dimmest on heatmap)

The heatmap shows these values as colors - brighter = more valuable piece!

## Navigation Controls

When viewing a game interactively:
- **→ (Right Arrow)** = Next move
- **← (Left Arrow)** = Previous move
- **Close window** = Exit

## Common Commands

### Interactive Mode (Step Through)
```bash
python cli.py sample_game.pgn
```

### Animated Mode (Auto-play)
```bash
python cli.py sample_game.pgn --animate
```

### Save as GIF
```bash
python cli.py sample_game.pgn --animate --save mygame.gif
```

### View Specific Move
```bash
python cli.py sample_game.pgn --move 15
```

## Using in Python Code

```python
from chess_heatmap import ChessHeatmapVisualizer

# Create visualizer
viz = ChessHeatmapVisualizer()

# Load game
game = viz.load_pgn_from_file('sample_game.pgn')
viz.process_game(game)

# View it!
viz.step_through_game()
```

## More Examples

Check out `examples.py` for more ways to use the visualizer:
```bash
python examples.py
```

Choose from:
1. Step through a game interactively
2. Watch an animated game
3. View a specific position

## What You'll See

The visualization shows:
- **8x8 chess board** with coordinates (a-h, 1-8)
- **Numbers on each square** showing piece values
- **Color intensity** representing piece value (dark = empty/low, bright = high value)
- **Current move** in the title

## Tips

1. **First time?** Run `python quickstart.py`
2. **Want to explore?** Use interactive mode (default)
3. **Making a video?** Use `--animate --save`
4. **Analyzing a position?** Use `--move <number>`

## Where to Get PGN Files

### Chess.com
1. Go to any game
2. Click "Share"
3. Click "Copy PGN"
4. Save to a `.pgn` file

### Lichess
1. Open any game
2. Click "Share & Export"
3. Download PGN

### Built-in
- `sample_game.pgn` - The Immortal Game (1851)
- Built-in examples in the code

## Need Help?

- Read `README.md` for full documentation
- Check `PROJECT_SUMMARY.md` for technical details
- Look at `examples.py` for code samples

## Enjoy visualizing chess! 🔥♟️
