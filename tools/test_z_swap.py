import numpy as np
from PIL import Image

def test_z():
    key = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png')
    body = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/body/paint_brass_gold.png')
    head = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/head_unit/ear_lion_gilded_mane_brass.png')
    eyes = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/eyes/eyes_amber_gold.png')
    lance = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/weapon/wpn_knight_lance.png')
    costume = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/costume/costume_royal_guard.png')

    # Front: key Z=5 (back), lance Z=40 (front)
    c_front = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    c_front.alpha_composite(key, (322, 183)) # Z=5
    c_front.alpha_composite(body, (0, 0))    # Z=10
    c_front.alpha_composite(head, (131, 51)) # Z=20
    c_front.alpha_composite(costume, (130, 230)) # Z=25
    c_front.alpha_composite(eyes, (168, 143)) # Z=30
    c_front.alpha_composite(lance, (75, 27))  # Z=40

    # Back: lance Z=4 (back), key Z=50 (very front)
    c_back = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    c_back.alpha_composite(lance, (75, 27))   # Z=4
    c_back.alpha_composite(body, (0, 0))     # Z=10
    c_back.alpha_composite(head, (131, 51))  # Z=20
    c_back.alpha_composite(costume, (130, 230)) # Z=25
    c_back.alpha_composite(eyes, (168, 143)) # Z=30
    c_back.alpha_composite(key, (322, 183))  # Z=50

    proof_d = Image.new("RGBA", (1024, 512), (255, 252, 247, 255))
    proof_d.alpha_composite(c_front, (0, 0))
    proof_d.alpha_composite(c_back, (512, 0))
    proof_d.save('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/test_z_proof.png')
    print("Saved test_z_proof.png")

if __name__ == "__main__":
    test_z()
