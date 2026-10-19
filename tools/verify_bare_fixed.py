import numpy as np
from PIL import Image

def test_bare():
    body = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/body/paint_brass_gold.png')
    head = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/head_unit/ear_lion_gilded_mane_brass.png')
    eyes = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/eyes/eyes_amber_gold.png')
    lance = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/weapon/wpn_knight_lance.png')
    key = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/winding_key/key_classic_brass.png')
    tail = Image.open('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts/back_curio/curio_lion_fan_tail.png')

    comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    comp.alpha_composite(key, (322, 183))
    comp.alpha_composite(tail, (351, 364))
    comp.alpha_composite(body, (0, 0))
    comp.alpha_composite(head, (131, 51))
    comp.alpha_composite(eyes, (168, 143))
    comp.alpha_composite(lance, (75, 27))

    comp.save('/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_test_bare_fixed.png')

    # Check for any transparent hole near hand/lance: x=140..160, y=280..340
    arr = np.array(comp)
    holes = 0
    for y in range(280, 340):
        for x in range(140, 160):
            if arr[y, x, 3] == 0:
                print(f"Hole at ({x}, {y})")
                holes += 1
    print(f"Total transparent holes near hand/lance on BARE CHASSIS: {holes}")

if __name__ == "__main__":
    test_bare()
