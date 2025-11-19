"""Record chess game visualization as MP4 directly"""
from chess_heatmap import ChessHeatmapVisualizer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np
import imageio
import chess

# Create visualizer
viz = ChessHeatmapVisualizer()

# Load your game
print("Loading game...")
game = viz.load_pgn_from_file('sample_game.pgn')

# Process the game
viz.process_game(game)
print(f"Loaded {len(viz.board_states)} positions")

print("\nRendering MP4 with wave effects and piece symbols...")
print("This may take a moment...")

# Setup
fig, ax = plt.subplots(figsize=(10, 10))
colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=100)

frames_per_move = 5
wave_color = '#ff00ff'
ray_artists = []
all_frames = []

def get_annotations(move_index):
    board = viz.board_objects[move_index]
    annot_matrix = np.empty((8, 8), dtype=object)
    
    for row in range(8):
        for col in range(8):
            rank = 7 - row
            file = col
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            
            if piece:
                annot_matrix[row, col] = viz.PIECE_SYMBOLS.get((piece.piece_type, piece.color), '')
            else:
                annot_matrix[row, col] = ''
    
    return annot_matrix

# Create initial heatmap
sns.heatmap(viz.board_states[0], 
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

# Render each frame
total_frames = len(viz.board_states) * frames_per_move
for frame_num in range(total_frames):
    move_index = frame_num // frames_per_move
    wave_frame = frame_num % frames_per_move
    
    print(f"\rRendering frame {frame_num+1}/{total_frames}...", end='', flush=True)
    
    # Update board on first wave frame
    if wave_frame == 0:
        for artist in ax.collections + ax.texts:
            artist.remove()
        
        sns.heatmap(viz.board_states[move_index], 
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
        ax.set_title(f'Chess Board Heatmap - {viz.moves_list[move_index]}', 
                    fontsize=14, fontweight='bold')
    
    # Draw waves
    for artist in ray_artists:
        try:
            artist.remove()
        except:
            pass
    ray_artists.clear()
    
    phase = wave_frame / frames_per_move
    board = viz.board_objects[move_index]
    attack_rays = viz.get_attack_rays(board)
    
    for (from_pos, to_pos) in attack_rays:
        path_squares = viz.get_path_squares(from_pos, to_pos)
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
    
    # Capture frame
    fig.canvas.draw()
    frame_data = np.array(fig.canvas.renderer.buffer_rgba())
    frame_data = frame_data[:, :, :3]  # Remove alpha channel
    all_frames.append(frame_data)

print("\n\nSaving MP4...")
imageio.mimsave('chess_game_pieces.mp4', all_frames, fps=5)
plt.close(fig)

print(f"✓ Saved {len(all_frames)} frames as chess_game_pieces.mp4")
print("\nDone! Check your directory for the output file.")
