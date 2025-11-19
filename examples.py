"""
Example usage of the Chess Heatmap Visualizer
"""

from chess_heatmap import ChessHeatmapVisualizer


def example_from_pgn_file():
    """Load a game from a PGN file and visualize it"""
    visualizer = ChessHeatmapVisualizer()
    
    # Load game from file
    print("Loading game from sample_game.pgn...")
    game = visualizer.load_pgn_from_file('sample_game.pgn')
    
    # Process the game
    visualizer.process_game(game)
    print(f"Game loaded with {len(visualizer.board_states)} positions\n")
    
    # Step through the game interactively
    print("Starting interactive step-through mode...")
    print("Use LEFT/RIGHT arrow keys to navigate through moves")
    visualizer.step_through_game()


def example_from_string():
    """Load a game from a PGN string and create animation"""
    visualizer = ChessHeatmapVisualizer()
    
    # Example: The "Opera Game" - Paul Morphy vs Duke of Brunswick and Count Isouard
    opera_game = """
[Event "Opera Game"]
[Site "Paris"]
[Date "1858.??.??"]
[White "Morphy, Paul"]
[Black "Duke of Brunswick and Count Isouard"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 
7. Qb3 Qe7 8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 
13. Rxd7 Rxd7 14. Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0
"""
    
    print("Loading the famous 'Opera Game' by Paul Morphy...")
    game = visualizer.load_pgn_from_string(opera_game)
    
    # Process the game
    visualizer.process_game(game)
    print(f"Game loaded with {len(visualizer.board_states)} positions\n")
    
    # Animate the game
    print("Creating animation...")
    visualizer.animate_game(interval=800)  # 800ms between moves


def example_view_position():
    """View a specific position in the game"""
    visualizer = ChessHeatmapVisualizer()
    
    # Simple game
    simple_game = """
[Event "Example"]
[Site "?"]
[Date "2025.11.19"]
[Result "*"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O *
"""
    
    print("Loading a game...")
    game = visualizer.load_pgn_from_string(simple_game)
    visualizer.process_game(game)
    
    # View the position after move 5
    print("Displaying position after move 5...")
    visualizer.visualize_static(move_index=5)


if __name__ == "__main__":
    print("Chess Heatmap Visualizer - Examples")
    print("=" * 50)
    print("\nChoose an example:")
    print("1. Load from PGN file and step through interactively")
    print("2. Load 'Opera Game' and animate")
    print("3. View specific position")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        example_from_pgn_file()
    elif choice == "2":
        example_from_string()
    elif choice == "3":
        example_view_position()
    else:
        print("Invalid choice. Running default (step-through)...")
        example_from_pgn_file()
