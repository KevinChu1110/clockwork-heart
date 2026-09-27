import json

for path in ["/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
             "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    races = data["races_specification"]["races"]
    wolf = None
    for r in races:
        if r.get("race_id") == "wolf":
            wolf = r
            break
    assert wolf is not None, f"Wolf not found in {path}"

    anc = wolf["asset_naming_conventions"]
    pose_entry = "game/assets/sprites/player/poses/wolf/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)"
    slices_entry = "game/assets/sprites/player/paperdoll/wolf/{slot_id}/{item_id}.png (紙娃娃切片圖層)"

    # Update status
    if pose_entry in anc["status"]["pending"]:
        anc["status"]["pending"].remove(pose_entry)
    if pose_entry not in anc["status"]["existing"]:
        anc["status"]["existing"].append(pose_entry)

    if slices_entry in anc["status"]["pending"]:
        anc["status"]["pending"].remove(slices_entry)
    if slices_entry not in anc["status"]["existing"]:
        anc["status"]["existing"].append(slices_entry)

    # Update game_action_poses and paperdoll_slices_dir
    anc["game_action_poses"] = "game/assets/sprites/player/poses/wolf/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [既有]"
    anc["paperdoll_slices_dir"] = "game/assets/sprites/player/paperdoll/wolf/{slot_id}/{item_id}.png [既有]"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✓ Updated {path}")
