"""
Simple Command-Line Interface for Chess Heatmap Visualizer
"""

import argparse
import sys
from chess_heatmap import ChessHeatmapVisualizer


def main():
    parser = argparse.ArgumentParser(
        description='Visualize chess games as heatmaps based on piece values',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive step-through mode
  python cli.py sample_game.pgn
  
  # Animate the game
  python cli.py sample_game.pgn --animate
  
  # Save animation as GIF
  python cli.py sample_game.pgn --animate --save output.gif
  
  # View specific move
  python cli.py sample_game.pgn --move 15
  
Piece Values:
  Queen: 10, Rook: 5, King: 4, Bishop: 3, Knight: 3, Pawn: 1
        """
    )
    
    parser.add_argument('pgn_file', 
                       help='Path to PGN file containing the chess game')
    
    parser.add_argument('--animate', 
                       action='store_true',
                       help='Animate the entire game instead of step-through')
    
    parser.add_argument('--interval', 
                       type=int, 
                       default=500,
                       help='Time between moves in animation (milliseconds, default: 500)')
    
    parser.add_argument('--save', 
                       type=str,
                       help='Save animation to file (.gif or .mp4)')
    
    parser.add_argument('--move', 
                       type=int,
                       help='Display a specific move number (0 = initial position)')
    
    args = parser.parse_args()
    
    # Create visualizer
    visualizer = ChessHeatmapVisualizer()
    
    # Load game
    try:
        print(f"Loading game from {args.pgn_file}...")
        game = visualizer.load_pgn_from_file(args.pgn_file)
        
        if game is None:
            print("Error: Could not read game from PGN file.")
            sys.exit(1)
            
    except FileNotFoundError:
        print(f"Error: File '{args.pgn_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading game: {e}")
        sys.exit(1)
    
    # Process game
    visualizer.process_game(game)
    print(f"Game loaded with {len(visualizer.board_states)} positions")
    
    # Display game info if available
    if game.headers:
        print("\nGame Information:")
        if "Event" in game.headers:
            print(f"  Event: {game.headers['Event']}")
        if "White" in game.headers and "Black" in game.headers:
            print(f"  Players: {game.headers['White']} vs {game.headers['Black']}")
        if "Date" in game.headers:
            print(f"  Date: {game.headers['Date']}")
        if "Result" in game.headers:
            print(f"  Result: {game.headers['Result']}")
    
    print()
    
    # Visualize based on mode
    if args.move is not None:
        # View specific move
        if args.move < 0 or args.move >= len(visualizer.board_states):
            print(f"Error: Move {args.move} is out of range (0-{len(visualizer.board_states)-1})")
            sys.exit(1)
        print(f"Displaying position at move {args.move}...")
        visualizer.visualize_static(args.move)
        
    elif args.animate:
        # Animate mode
        print(f"Animating game (interval: {args.interval}ms)...")
        if args.save:
            print(f"Saving to {args.save}...")
        visualizer.animate_game(interval=args.interval, save_as=args.save)
        
    else:
        # Interactive step-through (default)
        print("Starting interactive mode...")
        print("Use LEFT/RIGHT arrow keys to navigate through moves")
        print("Close the window to exit\n")
        visualizer.step_through_game()


if __name__ == "__main__":
    main()
