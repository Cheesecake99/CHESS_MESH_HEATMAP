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
from matplotlib.widgets import Button, Slider, CheckButtons
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
    
    # Unicode chess pieces
    PIECE_SYMBOLS = {
        (chess.PAWN, chess.WHITE): '♙',
        (chess.KNIGHT, chess.WHITE): '♘',
        (chess.BISHOP, chess.WHITE): '♗',
        (chess.ROOK, chess.WHITE): '♖',
        (chess.QUEEN, chess.WHITE): '♕',
        (chess.KING, chess.WHITE): '♔',
        (chess.PAWN, chess.BLACK): '♟',
        (chess.KNIGHT, chess.BLACK): '♞',
        (chess.BISHOP, chess.BLACK): '♝',
        (chess.ROOK, chess.BLACK): '♜',
        (chess.QUEEN, chess.BLACK): '♛',
        (chess.KING, chess.BLACK): '♚',
    }
    
    def __init__(self):
        self.board_states: List[np.ndarray] = []
        self.moves_list: List[str] = []
        self.board_objects: List[chess.Board] = []  # Store actual board objects
        
    def get_attack_rays(self, board: chess.Board) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get all attack rays where a piece can capture an enemy piece.
        Returns list of tuples: ((from_row, from_col), (to_row, to_col))
        """
        rays = []
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Get all legal moves from this square
                for move in board.legal_moves:
                    if move.from_square == square:
                        # Check if this move is a capture
                        target_piece = board.piece_at(move.to_square)
                        if target_piece and target_piece.color != piece.color:
                            # Convert squares to row, col
                            from_row = 7 - chess.square_rank(move.from_square)
                            from_col = chess.square_file(move.from_square)
                            to_row = 7 - chess.square_rank(move.to_square)
                            to_col = chess.square_file(move.to_square)
                            rays.append(((from_row, from_col), (to_row, to_col)))
        
        return rays
    
    def get_path_squares(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get all squares along the path from one position to another.
        Returns list of (row, col) tuples representing the path.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        path = []
        
        # Calculate direction
        delta_row = to_row - from_row
        delta_col = to_col - from_col
        
        # Determine step size
        steps = max(abs(delta_row), abs(delta_col))
        
        if steps == 0:
            return [(from_row, from_col)]
        
        # Generate all squares along the path
        for i in range(steps + 1):
            row = from_row + (delta_row * i) // steps
            col = from_col + (delta_col * i) // steps
            path.append((row, col))
        
        return path
        
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
        self.board_objects = []
        
        board = game.board()
        
        # Add initial position
        self.board_states.append(self.get_board_heatmap(board))
        self.moves_list.append("Initial Position")
        self.board_objects.append(board.copy())
        
        # Process each move
        for move_num, move in enumerate(game.mainline_moves(), 1):
            board.push(move)
            self.board_states.append(self.get_board_heatmap(board))
            self.moves_list.append(f"Move {move_num}: {move.uci()}")
            self.board_objects.append(board.copy())
    
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
    
    def animate_game(self, interval: int = 200, save_as: Optional[str] = None, show_waves: bool = True):
        """
        Create an animated visualization of the entire game with attack waves
        
        Args:
            interval: Time between frames in milliseconds
            save_as: Optional filename to save animation (e.g., 'game.gif' or 'game.mp4')
            show_waves: Whether to show attack wave animations (default True)
        """
        if not self.board_states:
            print("No game loaded. Please process a game first.")
            return
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create custom colormap
        colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=n_bins)
        
        # Wave animation state
        ray_artists = []
        ray_wave_phase = [0.0]
        wave_color = '#ff00ff'  # Magenta
        frames_per_move = 5 if show_waves else 1  # Fewer frames for faster rendering
        
        def get_annotations(move_index):
            """Get annotations matrix - piece symbols"""
            board = self.board_objects[move_index]
            annot_matrix = np.empty((8, 8), dtype=object)
            
            for row in range(8):
                for col in range(8):
                    rank = 7 - row
                    file = col
                    square = chess.square(file, rank)
                    piece = board.piece_at(square)
                    
                    if piece:
                        annot_matrix[row, col] = self.PIECE_SYMBOLS.get((piece.piece_type, piece.color), '')
                    else:
                        annot_matrix[row, col] = ''
            
            return annot_matrix
        
        # Create initial heatmap with colorbar
        sns.heatmap(self.board_states[0], 
                   annot=get_annotations(0), 
                   fmt='',
                   cmap=cmap,
                   vmin=0, 
                   vmax=10,
                   cbar_kws={'label': 'Piece Value'},
                   square=True,
                   linewidths=1,
                   linecolor='white',
                   ax=ax,
                   xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                   yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'],
                   annot_kws={'fontsize': 32})
        
        def draw_waves(move_index, phase):
            """Draw wave effects for current move"""
            nonlocal ray_artists
            
            # Clear previous wave artists
            for artist in ray_artists:
                try:
                    artist.remove()
                except:
                    pass
            ray_artists = []
            
            if move_index >= len(self.board_objects):
                return
            
            # Get attack rays for current position
            board = self.board_objects[move_index]
            attack_rays = self.get_attack_rays(board)
            
            if not attack_rays:
                return
            
            # Draw waves along each attack path
            for (from_pos, to_pos) in attack_rays:
                path_squares = self.get_path_squares(from_pos, to_pos)
                
                for idx, (row, col) in enumerate(path_squares):
                    wave_delay = idx / max(len(path_squares), 1)
                    phase_offset = (phase - wave_delay) % 1.0
                    intensity = 0.3 + 0.5 * np.sin(phase_offset * 2 * np.pi)
                    
                    if intensity > 0.35:
                        rect = plt.Rectangle((col, row), 1, 1, 
                                            facecolor=wave_color, 
                                            alpha=intensity * 0.6,
                                            zorder=5,
                                            linewidth=0)
                        ax.add_patch(rect)
                        ray_artists.append(rect)
        
        def update(frame):
            move_index = frame // frames_per_move
            wave_frame = frame % frames_per_move
            
            # Only redraw board on first wave frame of each move
            if wave_frame == 0:
                # Remove old heatmap elements
                for artist in ax.collections + ax.texts:
                    artist.remove()
                
                # Redraw heatmap without colorbar
                sns.heatmap(self.board_states[move_index], 
                           annot=get_annotations(move_index), 
                           fmt='',
                           cmap=cmap,
                           vmin=0, 
                           vmax=10,
                           cbar=False,
                           square=True,
                           linewidths=1,
                           linecolor='white',
                           ax=ax,
                           xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                           yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'],
                           annot_kws={'fontsize': 32})
                
                ax.set_xlabel('File (a-h)', fontsize=12)
                ax.set_ylabel('Rank (8-1)', fontsize=12)
                ax.set_title(f'Chess Board Heatmap - {self.moves_list[move_index]}', 
                            fontsize=14, fontweight='bold')
            
            # Draw wave animation for this frame (if enabled)
            if show_waves and frames_per_move > 1:
                ray_wave_phase[0] = wave_frame / frames_per_move
                draw_waves(move_index, ray_wave_phase[0])
            
            return ax,
        
        total_frames = len(self.board_states) * frames_per_move
        anim = animation.FuncAnimation(fig, update, 
                                      frames=total_frames,
                                      interval=interval,
                                      repeat=False,
                                      blit=False)
        
        if save_as:
            print(f"Rendering {total_frames} frames...")
            if save_as.endswith('.gif'):
                anim.save(save_as, writer='pillow', fps=1000//interval)
                print(f"Animation saved as {save_as}")
            elif save_as.endswith('.mp4'):
                anim.save(save_as, writer='ffmpeg', fps=1000//interval)
                print(f"Animation saved as {save_as}")
            plt.close(fig)
        else:
            plt.tight_layout()
            plt.show()
    
    def step_through_game(self):
        """Interactive step-through of the game"""
        if not self.board_states:
            print("No game loaded. Please process a game first.")
            return
        
        fig = plt.figure(figsize=(12, 10))
        
        # Create layout: main plot and control panel
        gs = fig.add_gridspec(20, 1)
        ax = fig.add_subplot(gs[0:17, 0])
        
        # Create custom colormap
        colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=n_bins)
        
        # State variables
        current_move = [0]
        is_playing = [False]
        repeat_mode = [True]
        speed = [500]  # milliseconds between moves
        timer = [None]
        is_updating = [False]  # Prevent concurrent updates
        
        # Ray wave animation state
        show_rays = [True]
        show_pieces = [True]  # Toggle between piece symbols and values
        ray_wave_phase = [0.0]  # Current phase of the wave animation
        ray_pulse_count = [0]  # Count pulses - reset when position changes
        max_pulses = 3  # Number of times rays pulse before stopping
        ray_color = ['red']  # Adjustable ray color
        ray_artists = []  # Store ray line artists for cleanup
        ray_timer = [None]  # Manual timer for ray animation
        last_position = [-1]  # Track position changes to reset pulses
        
        def get_annotations(move_index):
            """Get annotations matrix - either piece symbols or values"""
            if not show_pieces[0]:
                # Return values as strings
                return self.board_states[move_index].astype(str)
            
            # Build piece symbol matrix
            board = self.board_objects[move_index]
            annot_matrix = np.empty((8, 8), dtype=object)
            
            for row in range(8):
                for col in range(8):
                    # Convert to chess square
                    rank = 7 - row
                    file = col
                    square = chess.square(file, rank)
                    piece = board.piece_at(square)
                    
                    if piece:
                        annot_matrix[row, col] = self.PIECE_SYMBOLS.get((piece.piece_type, piece.color), '')
                    else:
                        annot_matrix[row, col] = ''
            
            return annot_matrix
        
        # Create initial heatmap with colorbar
        initial_heatmap = sns.heatmap(self.board_states[0], 
                   annot=get_annotations(0), 
                   fmt='',
                   cmap=cmap,
                   vmin=0, 
                   vmax=10,
                   cbar_kws={'label': 'Piece Value'},
                   square=True,
                   linewidths=1,
                   linecolor='white',
                   ax=ax,
                   xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                   yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'],
                   annot_kws={'fontsize': 32})
        
        ax.set_xlabel('File (a-h)', fontsize=12)
        ax.set_ylabel('Rank (8-1)', fontsize=12)
        ax.set_title(f'Chess Board Heatmap - {self.moves_list[0]} (1/{len(self.board_states)})', 
                    fontsize=14, fontweight='bold')
        
        def draw_ray_waves():
            """Light up squares along attack paths with wave effect"""
            nonlocal ray_artists
            
            # Clear previous highlights
            for artist in ray_artists:
                try:
                    artist.remove()
                except:
                    pass
            ray_artists = []
            
            if not show_rays[0] or current_move[0] >= len(self.board_objects):
                return
            
            # Get attack rays for current position
            board = self.board_objects[current_move[0]]
            attack_rays = self.get_attack_rays(board)
            
            if not attack_rays:
                return
            
            # For each attack ray, light up all squares along the path
            for (from_pos, to_pos) in attack_rays:
                path_squares = self.get_path_squares(from_pos, to_pos)
                
                # Draw pulsing light on each square in the path
                for idx, (row, col) in enumerate(path_squares):
                    # Wave effect: each square in path pulses with progressive delay
                    # Wave travels FROM attacker TO target (starts at idx 0)
                    wave_delay = idx / max(len(path_squares), 1)
                    phase_offset = (ray_wave_phase[0] - wave_delay) % 1.0
                    
                    # Intensity pulses using sine wave
                    intensity = 0.3 + 0.5 * np.sin(phase_offset * 2 * np.pi)
                    
                    # Only show if intensity is above threshold (creates traveling wave effect)
                    if intensity > 0.35:
                        # Light up the square
                        rect = plt.Rectangle((col, row), 1, 1, 
                                            facecolor=ray_color[0], 
                                            alpha=intensity * 0.6,
                                            zorder=5,
                                            linewidth=0)
                        ax.add_patch(rect)
                        ray_artists.append(rect)
            
            fig.canvas.draw_idle()
        
        def update_ray_animation():
            """Update the ray wave animation - called by timer"""
            if not show_rays[0]:
                return
            
            # Check if position changed - reset pulse counter
            if last_position[0] != current_move[0]:
                last_position[0] = current_move[0]
                ray_pulse_count[0] = 0
                ray_wave_phase[0] = 0.0
            
            # Only animate if we haven't completed max pulses
            if ray_pulse_count[0] < max_pulses:
                # Increment phase for wave motion
                old_phase = ray_wave_phase[0]
                ray_wave_phase[0] = (ray_wave_phase[0] + 0.15) % 1.0
                
                # Count completed pulses (when phase wraps around)
                if ray_wave_phase[0] < old_phase:
                    ray_pulse_count[0] += 1
                
                # Draw rays
                draw_ray_waves()
                
                # Schedule next frame only if still pulsing
                if ray_pulse_count[0] < max_pulses:
                    try:
                        if ray_timer[0]:
                            ray_timer[0].stop()
                    except:
                        pass
                    ray_timer[0] = fig.canvas.new_timer(interval=50)
                    ray_timer[0].add_callback(update_ray_animation)
                    ray_timer[0].start()
                else:
                    # Clear rays after final pulse
                    for artist in ray_artists:
                        try:
                            artist.remove()
                        except:
                            pass
                    ray_artists.clear()
                    fig.canvas.draw_idle()
        
        def update_plot():
            # Prevent concurrent updates
            if is_updating[0]:
                return
            is_updating[0] = True
            
            try:
                # Clear and recreate to avoid artifacts
                for artist in ax.collections + ax.texts:
                    artist.remove()
                
                # Redraw heatmap
                sns.heatmap(self.board_states[current_move[0]], 
                           annot=get_annotations(current_move[0]), 
                           fmt='',
                           cmap=cmap,
                           vmin=0, 
                           vmax=10,
                           cbar=False,  # Don't create new colorbar
                           square=True,
                           linewidths=1,
                           linecolor='white',
                           ax=ax,
                           xticklabels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
                           yticklabels=['8', '7', '6', '5', '4', '3', '2', '1'],
                           annot_kws={'fontsize': 32})
                
                ax.set_xlabel('File (a-h)', fontsize=12)
                ax.set_ylabel('Rank (8-1)', fontsize=12)
                ax.set_title(f'Chess Board Heatmap - {self.moves_list[current_move[0]]} ({current_move[0]+1}/{len(self.board_states)})', 
                            fontsize=14, fontweight='bold')
                
                # Trigger ray animation for new position
                if show_rays[0]:
                    # Stop any existing timer
                    if ray_timer[0]:
                        try:
                            ray_timer[0].stop()
                        except:
                            pass
                    # Reset and start new pulse sequence
                    ray_pulse_count[0] = 0
                    ray_wave_phase[0] = 0.0
                    last_position[0] = current_move[0]
                    update_ray_animation()
                
                fig.canvas.draw()
                fig.canvas.flush_events()
            finally:
                is_updating[0] = False
        
        def auto_advance():
            if is_playing[0]:
                # Stop current timer if it exists
                if timer[0] is not None:
                    try:
                        timer[0].stop()
                    except:
                        pass
                
                if current_move[0] < len(self.board_states) - 1:
                    current_move[0] += 1
                    update_plot()
                    # Create new timer for next advance
                    timer[0] = fig.canvas.new_timer(interval=speed[0])
                    timer[0].add_callback(auto_advance)
                    timer[0].start()
                elif repeat_mode[0]:
                    # Loop back to beginning
                    current_move[0] = 0
                    update_plot()
                    timer[0] = fig.canvas.new_timer(interval=speed[0])
                    timer[0].add_callback(auto_advance)
                    timer[0].start()
                else:
                    # Stop at the end
                    is_playing[0] = False
                    play_btn.label.set_text('▶ Play')
                    fig.canvas.draw()
        
        def on_play(event):
            if is_playing[0]:
                # Stop playback
                is_playing[0] = False
                if timer[0]:
                    timer[0].stop()
                play_btn.label.set_text('▶ Play')
            else:
                # Start playback
                is_playing[0] = True
                play_btn.label.set_text('⏸ Pause')
                auto_advance()
        
        def on_prev(event):
            if current_move[0] > 0:
                current_move[0] -= 1
                update_plot()
        
        def on_next(event):
            if current_move[0] < len(self.board_states) - 1:
                current_move[0] += 1
                update_plot()
        
        def on_first(event):
            current_move[0] = 0
            update_plot()
        
        def on_last(event):
            current_move[0] = len(self.board_states) - 1
            update_plot()
        
        def on_speed_change(val):
            speed[0] = int(val)
        
        def on_repeat_toggle(label):
            repeat_mode[0] = not repeat_mode[0]
        
        def on_rays_toggle(label):
            show_rays[0] = not show_rays[0]
            if show_rays[0]:
                # Restart ray animation
                ray_pulse_count[0] = 0
                ray_wave_phase[0] = 0.0
                if ray_timer[0]:
                    try:
                        ray_timer[0].stop()
                    except:
                        pass
                update_ray_animation()
            else:
                # Stop and clear rays when disabled
                if ray_timer[0]:
                    try:
                        ray_timer[0].stop()
                    except:
                        pass
                for artist in ray_artists:
                    try:
                        artist.remove()
                    except:
                        pass
                ray_artists.clear()
                fig.canvas.draw()
        
        def on_color_change(label):
            color_map = {
                'Red': 'red',
                'Blue': 'blue',
                'Green': 'lime',
                'Yellow': 'yellow',
                'Magenta': 'magenta',
                'Cyan': 'cyan'
            }
            ray_color[0] = color_map.get(label, 'red')
            draw_ray_waves()
        
        def on_key(event):
            if event.key == 'right':
                on_next(None)
            elif event.key == 'left':
                on_prev(None)
            elif event.key == ' ':
                on_play(None)
        
        # Create buttons
        ax_first = plt.axes([0.15, 0.05, 0.08, 0.04])
        ax_prev = plt.axes([0.24, 0.05, 0.08, 0.04])
        ax_play = plt.axes([0.33, 0.05, 0.08, 0.04])
        ax_next = plt.axes([0.42, 0.05, 0.08, 0.04])
        ax_last = plt.axes([0.51, 0.05, 0.08, 0.04])
        
        btn_first = Button(ax_first, '⏮ First')
        btn_prev = Button(ax_prev, '⏪ Prev')
        play_btn = Button(ax_play, '▶ Play')
        btn_next = Button(ax_next, 'Next ⏩')
        btn_last = Button(ax_last, 'Last ⏭')
        
        btn_first.on_clicked(on_first)
        btn_prev.on_clicked(on_prev)
        play_btn.on_clicked(on_play)
        btn_next.on_clicked(on_next)
        btn_last.on_clicked(on_last)
        
        # Speed slider
        ax_speed = plt.axes([0.15, 0.12, 0.44, 0.02])
        speed_slider = Slider(ax_speed, 'Speed (ms)', 100, 2000, valinit=500, valstep=100)
        speed_slider.on_changed(on_speed_change)
        
        # Repeat checkbox
        ax_repeat = plt.axes([0.65, 0.08, 0.15, 0.04])
        repeat_check = CheckButtons(ax_repeat, ['Repeat'], [True])
        repeat_check.on_clicked(on_repeat_toggle)
        
        # Ray waves checkbox
        ax_rays = plt.axes([0.65, 0.12, 0.15, 0.04])
        rays_check = CheckButtons(ax_rays, ['Show Rays'], [True])
        rays_check.on_clicked(on_rays_toggle)
        
        # Show pieces checkbox
        ax_pieces = plt.axes([0.65, 0.16, 0.15, 0.04])
        pieces_check = CheckButtons(ax_pieces, ['Show Pieces'], [True])
        
        def on_pieces_toggle(label):
            show_pieces[0] = not show_pieces[0]
            update_plot()
        
        pieces_check.on_clicked(on_pieces_toggle)
        
        # Ray color selector
        from matplotlib.widgets import RadioButtons
        ax_color = plt.axes([0.82, 0.05, 0.12, 0.12])
        color_radio = RadioButtons(ax_color, ('Red', 'Blue', 'Green', 'Yellow', 'Magenta', 'Cyan'))
        color_radio.on_clicked(on_color_change)
        
        # Start ray animation timer
        if show_rays[0]:
            update_ray_animation()
        
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        plt.subplots_adjust(bottom=0.18)
        print("\nControls:")
        print("  Buttons: First | Prev | Play/Pause | Next | Last")
        print("  Arrow Keys: LEFT (previous) | RIGHT (next) | SPACE (play/pause)")
        print("  Speed Slider: Adjust playback speed (100-2000 ms)")
        print("  Repeat: Toggle looping when reaching the end")
        print("  Show Pieces: Toggle between piece symbols and values")
        print("  Show Rays: Toggle attack square highlighting")
        print("  Ray Color: Select highlight color (Red/Blue/Green/Yellow/Magenta/Cyan)")
        print("\nClose the window to exit.")
        
        try:
            plt.show()
        finally:
            # Cleanup timers
            if timer[0]:
                try:
                    timer[0].stop()
                except:
                    pass
            if ray_timer[0]:
                try:
                    ray_timer[0].stop()
                except:
                    pass


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
