"""
Quick test of interactive heatmap
"""
from chess_heatmap import ChessHeatmapVisualizer

# Create visualizer
v = ChessHeatmapVisualizer()

# Load the sample game
print("Loading game...")
game = v.load_pgn_from_file('sample_game.pgn')
v.process_game(game)

print(f"Loaded {len(v.board_states)} positions")
print("\nOpening interactive visualization...")
print("Instructions:")
print("  - Press RIGHT ARROW to advance to next move")
print("  - Press LEFT ARROW to go back to previous move")
print("  - You should see the heatmap update with each move")
print("  - Close the window when done\n")

# Start interactive mode
v.step_through_game()

print("\nVisualization closed!")
