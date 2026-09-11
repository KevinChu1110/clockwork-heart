#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png")
w, h = im.size

# Let's crop vertical slices across player and enemy
# Player is on left half (x: 200~600), Enemy on right half (x: 650~1050)
# Y spans from 140 to 520
crop_player_full = im.crop((200, 140, 600, 520))
crop_player_full.save("/tmp/hud_crops/player_full.png")

crop_enemy_full = im.crop((650, 140, 1100, 520))
crop_enemy_full.save("/tmp/hud_crops/enemy_full.png")

# Also crop the top of player and enemy specifically (y: 140 to 280)
crop_player_head = im.crop((250, 140, 550, 260))
crop_player_head.save("/tmp/hud_crops/player_head.png")

crop_enemy_head = im.crop((700, 140, 1000, 260))
crop_enemy_head.save("/tmp/hud_crops/enemy_head.png")

print("Saved player and enemy full and head crops.")
