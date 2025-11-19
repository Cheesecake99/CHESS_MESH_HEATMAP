"""Convert GIF to MP4 using PIL and imageio"""
from PIL import Image
import imageio
import numpy as np

print("Loading GIF...")
gif = Image.open('chess_game_waves.gif')

frames = []
try:
    while True:
        # Convert frame to RGB (remove alpha channel if present)
        frame = gif.convert('RGB')
        frames.append(np.array(frame))
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

print(f"Loaded {len(frames)} frames")
print("Writing MP4...")

# Write as MP4
imageio.mimsave('chess_game_waves.mp4', frames, fps=5)  # 5 fps = 200ms per frame

print("✓ Saved as chess_game_waves.mp4")
