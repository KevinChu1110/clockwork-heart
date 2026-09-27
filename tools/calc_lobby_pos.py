from PIL import Image

bg = Image.open("proofs/exploratory_qa_t_e6bc1e6c/proof_lobby_hedgehog.png")
sc = Image.open("game/assets/sprites/player/showcase/hedgehog_idle_hd.png")

# MobileLobby: _hero_avatar has offset_left=-125, top=-140, right=125, bottom=125 (size: 250 x 265)
# stretch_mode = STRETCH_KEEP_ASPECT_CENTERED
# Texture size is 800 x 1200 (aspect 2:3)
# To fit into 250 x 265 keeping aspect ratio:
# scale = min(250/800, 265/1200) = min(0.3125, 0.220833) = 0.220833
# displayed size = 800 * 0.220833 = 176.67 x 265
# Centered horizontally: (250 - 176.67) / 2 = 36.67 px offset inside _hero_avatar
# _hero_avatar center is at stage_anchor.
# stage_anchor position in mobile lobby:
# Let's check stage_anchor position in mobile_lobby.gd!
