from PIL import Image

im = Image.open('screenshots/proof_battle_macaque_full_screen.png')
# Crop player area
player = im.crop((150, 150, 480, 520))
player.save('screenshots/test_player_full.png')
print("Saved test_player_full.png, size=", player.size)

# Crop player feet area
player_feet = im.crop((150, 380, 480, 510))
player_feet.save('screenshots/test_player_feet.png')
print("Saved test_player_feet.png, size=", player_feet.size)

# Crop enemy feet area
enemy_feet = im.crop((800, 380, 1130, 510))
enemy_feet.save('screenshots/test_enemy_feet.png')
print("Saved test_enemy_feet.png, size=", enemy_feet.size)
