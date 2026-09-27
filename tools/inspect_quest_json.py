import json
import os

root = "/opt/side/bravesoul-game/game/data/i18n/content"
comm_ids = ["d_train", "d_skirmish", "d_skirmish2", "d_mats", "d_craft", "d_shop", "d_hunt", "d_arena"]
miss_ids = [
    "m_first_boss", "m_letter", "m_sprout", "m_ding_debt", "m_fog_letter",
    "m_ronin", "m_codex", "m_side4", "m_three_kings", "m_optional", "m_clear",
    "m_titles5", "m_chests5", "m_chests12", "m_visit15", "m_visit30",
    "m_skirmish10", "m_scar", "m_mirror", "m_wreck", "m_three_secrets", "m_hunt3",
    "m_lantern", "m_nest", "m_star_wish", "m_fog_incense", "m_hearth", "m_life5"
]
all_ids = comm_ids + miss_ids

for lc in ["en", "ja", "zh_CN", "ko", "es"]:
    path = os.path.join(root, lc, "quest.json")
    data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    missing = [qid for qid in all_ids if qid not in data or not data[qid].get("name") or not data[qid].get("desc")]
    print(f"[{lc}] total in all_ids: {len(all_ids)}, missing: {len(missing)}")
    if missing:
        print(f"  missing ids: {missing}")
