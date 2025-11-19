"""Create a smaller GIF optimized for GitHub README"""
from chess_heatmap import ChessHeatmapVisualizer
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np
import chess
from PIL import Image

# Create visualizer
viz = ChessHeatmapVisualizer()

# Load your game
print("Loading game...")
game = viz.load_pgn_from_file('sample_game.pgn')

# Process the game
viz.process_game(game)
print(f"Loaded {len(viz.board_states)} positions")

print("\nCreating optimized GIF for GitHub README...")

# Setup - smaller figure for README
fig, ax = plt.subplots(figsize=(8, 8))
colors = ['#2b2b2b', '#4a4a4a', '#ffa500', '#ff6b00', '#ff0000', '#ff00ff']
cmap = LinearSegmentedColormap.from_list('chess_heat', colors, N=100)

# Use fewer frames - only key positions
key_positions = list(range(0, len(viz.board_states), 3))  # Every 3rd move
wave_color = '#ff0000'  # Red
frames_per_move = 3  # Fewer frames per position
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

# Render frames
total_frames = len(key_positions) * frames_per_move
for frame_num in range(total_frames):
    pos_idx = frame_num // frames_per_move
    wave_frame = frame_num % frames_per_move
    move_index = key_positions[pos_idx]
    
    print(f"\rRendering frame {frame_num+1}/{total_frames}...", end='', flush=True)
    
    # Update board
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
                   annot_kws={'fontsize': 24})
        
        ax.set_xlabel('File (a-h)', fontsize=10)
        ax.set_ylabel('Rank (8-1)', fontsize=10)
        ax.set_title(f'Move {move_index}: {viz.moves_list[move_index]}', 
                    fontsize=12, fontweight='bold')
    
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
    frame_data = frame_data[:, :, :3]
    all_frames.append(Image.fromarray(frame_data))

print("\n\nSaving optimized GIF...")
# Save as optimized GIF with loop
all_frames[0].save(
    'demo.gif',
    save_all=True,
    append_images=all_frames[1:],
    optimize=True,
    duration=200,  # 200ms per frame
    loop=0  # Loop forever
)

plt.close(fig)

print(f"✓ Saved {len(all_frames)} frames as demo.gif")
print(f"File size: {len(open('demo.gif', 'rb').read()) / 1024:.1f} KB")
print("\nDone! This GIF is optimized for GitHub README display.")
