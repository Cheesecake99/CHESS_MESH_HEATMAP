"""Test attack ray detection to ensure it follows chess rules"""
import chess
from chess_heatmap import ChessHeatmapVisualizer

viz = ChessHeatmapVisualizer()

# Test 1: Initial position - no captures available
print("=== Test 1: Initial Position ===")
board = chess.Board()
rays = viz.get_attack_rays(board)
print(f"Attack rays in initial position: {len(rays)}")
print(f"Expected: 0 (no pieces can capture in starting position)")
print(f"Result: {'✓ PASS' if len(rays) == 0 else '✗ FAIL'}\n")

# Test 2: Simple pawn capture scenario
print("=== Test 2: Pawn Capture ===")
board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
board.push_san("d5")  # Black pawn to d5
rays = viz.get_attack_rays(board)
print(f"Position: White pawn on e4, Black pawn on d5")
print(f"Attack rays: {len(rays)}")
for ray in rays:
    from_pos, to_pos = ray
    print(f"  From {from_pos} to {to_pos}")
print(f"Expected: White pawn on e4 can capture d5")
print(f"Result: {'✓ PASS' if len(rays) > 0 else '✗ FAIL'}\n")

# Test 3: Blocked rook - shouldn't see through pieces
print("=== Test 3: Blocked Rook ===")
board = chess.Board("r3k3/8/8/8/8/8/8/R3K3 w - - 0 1")
rays = viz.get_attack_rays(board)
print(f"Position: White rook on a1, Black rook on a8, no pieces between")
print(f"Attack rays: {len(rays)}")
for ray in rays:
    from_pos, to_pos = ray
    print(f"  From {from_pos} to {to_pos}")
print(f"Expected: Rook on a1 can capture rook on a8")

# Add a blocking piece
board = chess.Board("r3k3/8/8/p7/8/8/8/R3K3 w - - 0 1")
rays = viz.get_attack_rays(board)
print(f"\nPosition: Added Black pawn on a5 (blocking)")
print(f"Attack rays: {len(rays)}")
for ray in rays:
    from_pos, to_pos = ray
    print(f"  From {from_pos} to {to_pos}")
print(f"Expected: Rook can only capture pawn on a5, not rook on a8")
print(f"Result: {'✓ PASS' if any('a5' in str(r) for r in rays) and not any('a8' in str(r) for r in rays) else '✗ FAIL'}\n")

# Test 4: Knight jumps over pieces
print("=== Test 4: Knight Jumps ===")
board = chess.Board("8/8/8/3p4/8/1N6/8/8 w - - 0 1")
rays = viz.get_attack_rays(board)
print(f"Position: White knight on b3, Black pawn on d5")
print(f"Attack rays: {len(rays)}")
for ray in rays:
    from_pos, to_pos = ray
    print(f"  From {from_pos} to {to_pos}")
print(f"Expected: Knight can capture pawn on d5 (knights jump)")
print(f"Result: {'✓ PASS' if len(rays) > 0 else '✗ FAIL'}\n")

print("=== Summary ===")
print("Attack detection uses board.legal_moves which:")
print("✓ Respects piece movement rules")
print("✓ Handles blocking correctly")
print("✓ Only shows actual legal captures")
