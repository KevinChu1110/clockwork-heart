from PIL import Image

im = Image.open('screenshots/proof_battle_macaque_attack_full_screen.png')
player = im.crop((150, 150, 480, 520))
player.save('screenshots/test_player_attack_full.png')
print("Saved test_player_attack_full.png, size=", player.size)
