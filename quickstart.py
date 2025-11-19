"""
Quick Start - Run this to see the chess heatmap visualizer in action!
"""

from chess_heatmap import ChessHeatmapVisualizer

# Create a simple demo game (Scholar's Mate)
demo_game = """
[Event "Scholar's Mate Demo"]
[Site "Chess Heatmap Demo"]
[Date "2025.11.19"]
[White "White"]
[Black "Black"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0
"""

print("=" * 60)
print("CHESS HEATMAP VISUALIZER - Quick Start Demo")
print("=" * 60)
print("\nThis demo shows Scholar's Mate visualized as a heatmap")
print("where each piece is represented by its point value:")
print("  Queen = 10, Rook = 5, King = 4")
print("  Bishop = 3, Knight = 3, Pawn = 1")
print("\nControls:")
print("  → RIGHT ARROW: Next move")
print("  ← LEFT ARROW: Previous move")
print("  Close window to exit")
print("\n" + "=" * 60)

# Create and run visualizer
visualizer = ChessHeatmapVisualizer()
game = visualizer.load_pgn_from_string(demo_game)
visualizer.process_game(game)

print(f"\nGame loaded: {len(visualizer.board_states)} positions")
print("\nStarting visualization...\n")

visualizer.step_through_game()

print("\nDemo complete! Try these next:")
print("  1. Run 'python examples.py' for more examples")
print("  2. Run 'python cli.py sample_game.pgn' for a full game")
print("  3. Load your own PGN from Chess.com!")
