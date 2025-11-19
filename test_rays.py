"""Test script for ray wave animation"""
import traceback
from chess_heatmap import ChessHeatmapVisualizer

try:
    # Create visualizer
    viz = ChessHeatmapVisualizer()
    
    # Load the sample game
    print("Loading game...")
    game = viz.load_pgn_from_file('sample_game.pgn')
    
    # Process the game
    viz.process_game(game)
    print(f"Loaded {len(viz.board_states)} positions")
    
    # Test attack rays for initial position
    print("\nTesting attack rays calculation...")
    rays = viz.get_attack_rays(viz.board_objects[0])
    print(f"Found {len(rays)} attack rays in initial position")
    
    print("\nOpening interactive visualization with ray waves...")
    viz.step_through_game()
    
    print("\nVisualization closed!")
    
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    traceback.print_exc()
