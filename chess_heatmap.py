"""
Chess Heatmap Visualizer
Visualizes chess games as heatmaps where piece values create intensity patterns
"""

import chess
import chess.pgn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from typing import List, Tuple, Optional
import io


class ChessHeatmapVisualizer:
    """Visualizes chess games as heatmaps based on piece values"""
    
    # Piece values mapping
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 10,
        chess.KING: 4  # King has special value
    }
    
    def __init__(self):
        self.board_states: List[np.ndarray] = []
        self.moves_list: List[str] = []
        
    def get_board_heatmap(self, board: chess.Board) -> np.ndarray:
        """
        Convert a chess board position to an 8x8 heatmap array
        based on piece values at each square
        """
        heatmap = np.zeros((8, 8))
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Get piece value
                value = self.PIECE_VALUES.get(piece.piece_type, 0)
                
                # Convert square to row, col (chess board is bottom-up, array is top-down)
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                
                heatmap[row, col] = value
                
        return heatmap
    
    def load_pgn_from_string(self, pgn_string: str) -> chess.pgn.Game:
        """Load a chess game from PGN string"""
        pgn = io.StringIO(pgn_string)
        game = chess.pgn.read_game(pgn)
        return game
    
    def load_pgn_from_file(self, filename: str) -> chess.pgn.Game:
        """Load a chess game from PGN file"""
        with open(filename, 'r') as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game
    
    def process_game(self, game: chess.pgn.Game):
        """Process a chess game and generate all board states"""
        self.board_states = []
        self.moves_list = []
        
        board = game.board()
        
        # Add initial position
        self.board_states.append(self.get_board_heatmap(board))
        self.moves_list.append("Initial Position")
        
        # Process each move
        for move_num, move in enumerate(game.mainline_moves(), 1):
            board.push(move)
            self.board_states.append(self.get_board_heatmap(board))
            self.moves_list.append(f"Move {move_num}: {move.uci()}")
    
    def visualize_static(self, move_index: int = 0):
        """Display a static heatmap for a specific move"""
        if not self.board_states:
            print("No game loaded. Please process a game first.")
            return
        
        if move_index >= len(self.board_states):
            move_index = len(self.board_states) - 1
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create custom colormap (dark to bright based on piece values)
        colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=n_bins)
        
        # Plot heatmap
        sns.heatmap(self.board_states[move_index], 
                   annot=True, 
                   fmt='.0f',
                   cmap=cmap,
                   vmin=0, 
                   vmax=10,
                   cbar_kws={'label': 'Piece Value'},
                   square=True,
                   linewidths=1,
                   linecolor='white',
                   ax=ax,
                   xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                   yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'])
        
        # Set labels
        ax.set_xlabel('File (a-h)', fontsize=12)
        ax.set_ylabel('Rank (8-1)', fontsize=12)
        ax.set_title(f'Chess Board Heatmap - {self.moves_list[move_index]}', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def animate_game(self, interval: int = 500, save_as: Optional[str] = None):
        """
        Create an animated visualization of the entire game
        
        Args:
            interval: Time between frames in milliseconds
            save_as: Optional filename to save animation (e.g., 'game.gif' or 'game.mp4')
        """
        if not self.board_states:
            print("No game loaded. Please process a game first.")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create custom colormap
        colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=n_bins)
        
        def update(frame):
            ax.clear()
            
            # Plot heatmap for current frame
            sns.heatmap(self.board_states[frame], 
                       annot=True, 
                       fmt='.0f',
                       cmap=cmap,
                       vmin=0, 
                       vmax=10,
                       cbar_kws={'label': 'Piece Value'},
                       square=True,
                       linewidths=1,
                       linecolor='white',
                       ax=ax,
                       xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                       yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'])
            
            # Set labels
            ax.set_xlabel('File (a-h)', fontsize=12)
            ax.set_ylabel('Rank (8-1)', fontsize=12)
            ax.set_title(f'Chess Board Heatmap - {self.moves_list[frame]}', 
                        fontsize=14, fontweight='bold')
            
            return ax,
        
        anim = animation.FuncAnimation(fig, update, 
                                      frames=len(self.board_states),
                                      interval=interval,
                                      repeat=True,
                                      blit=False)
        
        if save_as:
            if save_as.endswith('.gif'):
                anim.save(save_as, writer='pillow', fps=1000//interval)
                print(f"Animation saved as {save_as}")
            elif save_as.endswith('.mp4'):
                anim.save(save_as, writer='ffmpeg', fps=1000//interval)
                print(f"Animation saved as {save_as}")
        
        plt.tight_layout()
        plt.show()
    
    def step_through_game(self):
        """Interactive step-through of the game"""
        if not self.board_states:
            print("No game loaded. Please process a game first.")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create custom colormap
        colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=n_bins)
        
        current_move = [0]  # Use list to allow modification in nested function
        heatmap_obj = [None]  # Store the heatmap object
        
        def update_plot():
            # Clear the entire figure and recreate
            fig.clear()
            ax_new = fig.add_subplot(111)
            
            sns.heatmap(self.board_states[current_move[0]], 
                       annot=True, 
                       fmt='.0f',
                       cmap=cmap,
                       vmin=0, 
                       vmax=10,
                       cbar_kws={'label': 'Piece Value'},
                       square=True,
                       linewidths=1,
                       linecolor='white',
                       ax=ax_new,
                       xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                       yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'])
            
            ax_new.set_xlabel('File (a-h)', fontsize=12)
            ax_new.set_ylabel('Rank (8-1)', fontsize=12)
            ax_new.set_title(f'Chess Board Heatmap - {self.moves_list[current_move[0]]} ({current_move[0]+1}/{len(self.board_states)})', 
                        fontsize=14, fontweight='bold')
            
            fig.canvas.draw()
            fig.canvas.flush_events()
        
        def on_key(event):
            if event.key == 'right' and current_move[0] < len(self.board_states) - 1:
                current_move[0] += 1
                update_plot()
            elif event.key == 'left' and current_move[0] > 0:
                current_move[0] -= 1
                update_plot()
        
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        update_plot()
        plt.tight_layout()
        print("\nUse arrow keys: LEFT (previous move) | RIGHT (next move)")
        print("Close the window to exit.")
        plt.show()


def main():
    """Demo of the chess heatmap visualizer"""
    
    # Sample PGN game (Scholar's Mate)
    sample_pgn = """
[Event "Sample Game"]
[Site "Chess.com"]
[Date "2025.11.19"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0
"""
    
    # Create visualizer
    visualizer = ChessHeatmapVisualizer()
    
    # Load and process game
    print("Loading sample chess game...")
    game = visualizer.load_pgn_from_string(sample_pgn)
    visualizer.process_game(game)
    
    print(f"Game loaded with {len(visualizer.board_states)} positions")
    print("\nOptions:")
    print("1. Animate the entire game")
    print("2. Step through game interactively")
    print("3. View specific position")
    
    # For demonstration, let's do step-through
    visualizer.step_through_game()


if __name__ == "__main__":
    main()
