#!/usr/bin/env python3
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. game_state.gd
gs_path = os.path.join(repo_root, "game/scripts/autoload/game_state.gd")
with open(gs_path, "r", encoding="utf-8") as f:
    gs = f.read()

assert '\t"mantis": "hunt_claw",\n' in gs
gs = gs.replace(
    '\t"mantis": "hunt_claw",\n',
    '\t"mantis": "hunt_claw",\n\t"nightingale": "shard_focus",\n',
    1
)

assert '\t\t"mantis": default_name = "翠刃螳螂"\n' in gs
gs = gs.replace(
    '\t\t"mantis": default_name = "翠刃螳螂"\n',
    '\t\t"mantis": default_name = "翠刃螳螂"\n\t\t"nightingale": default_name = "晨音夜鶯"\n',
    1
)

with open(gs_path, "w", encoding="utf-8") as f:
    f.write(gs)
print("Updated game_state.gd")

# 2. equipment_system.gd
es_path = os.path.join(repo_root, "game/scripts/systems/equipment_system.gd")
with open(es_path, "r", encoding="utf-8") as f:
    es = f.read()

assert '\t"mantis": "hunt_claw",\n' in es
es = es.replace(
    '\t"mantis": "hunt_claw",\n',
    '\t"mantis": "hunt_claw",\n\t"nightingale": "shard_focus",\n',
    1
)

with open(es_path, "w", encoding="utf-8") as f:
    f.write(es)
print("Updated equipment_system.gd")

# 3. paperdoll_select_demo.gd
ps_path = os.path.join(repo_root, "game/scripts/ui/paperdoll_select_demo.gd")
with open(ps_path, "r", encoding="utf-8") as f:
    ps = f.read()

nightingale_races_data = '''\t},
\t"nightingale": {
\t\t"id": "nightingale",
\t\t"name_zh": "晨音夜鶯",
\t\t"name_en": "The Dawn Nightingale",
\t\t"archetype": "法師 (Mage)",
\t\t"thumb": "res://assets/sprites/player/showcase/nightingale_idle_hd.png",
\t\t"desc": "晨曦小鎮木偶集市鐘樓八音諧振護體靈晶大師法師，沖壓黃銅底盤配鐘面鏤空雕花面盔、黃玉琉璃目鏡與晨音八音諧振靈晶。",
\t\t"costumes": [
\t\t\t{"id": "costume_nightingale_chime_plate", "name_zh": "小鎮禮樂銅板八音胸甲", "desc": "晨曦小鎮工坊沖壓薄銅烤漆禮樂胸甲，飾以多巴胺暖橘與天藍飾帶，嵌石英視窗"},
\t\t\t{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現天元金黃沖壓鍍金薄銅板件與橡膠爪墊"}
\t\t],
\t\t"chassis": [
\t\t\t{"id": "chassis_nightingale_stock", "name_zh": "晨曦鍍金沖壓黃銅夜鶯底盤", "desc": "沖壓鍛造高剛性黃銅薄板件，表面天元金黃與薄荷綠琺瑯塗層，配耐磨橡膠爪墊"}
\t\t]
\t}
}'''

assert '\t}\n}\n\nconst RACE_KEYS' in ps
ps = ps.replace('\t}\n}\n\nconst RACE_KEYS', nightingale_races_data + '\n\nconst RACE_KEYS', 1)

old_rk = '"donkey", "scorpion", "mantis"]'
new_rk = '"donkey", "scorpion", "mantis", "nightingale"]'
assert ps.count(old_rk) == 2, f"Expected 2 occurrences of old_rk in paperdoll_select_demo.gd, found {ps.count(old_rk)}"
ps = ps.replace(old_rk, new_rk)

assert '\t\t\t\t"mantis": gs.player_name = "翠刃螳螂"\n' in ps
ps = ps.replace(
    '\t\t\t\t"mantis": gs.player_name = "翠刃螳螂"\n',
    '\t\t\t\t"mantis": gs.player_name = "翠刃螳螂"\n\t\t\t\t"nightingale": gs.player_name = "晨音夜鶯"\n',
    1
)

with open(ps_path, "w", encoding="utf-8") as f:
    f.write(ps)
print("Updated paperdoll_select_demo.gd")

# 4. wardrobe_dialog.gd
wd_path = os.path.join(repo_root, "game/scripts/ui/wardrobe_dialog.gd")
with open(wd_path, "r", encoding="utf-8") as f:
    wd = f.read()

assert '\t{"id": "mantis", "name_zh": "螳螂"},\n' in wd
wd = wd.replace(
    '\t{"id": "mantis", "name_zh": "螳螂"},\n',
    '\t{"id": "mantis", "name_zh": "螳螂"},\n\t{"id": "nightingale", "name_zh": "夜鶯"},\n',
    1
)

assert '\t\t"mantis": return "螳螂"\n' in wd
wd = wd.replace(
    '\t\t"mantis": return "螳螂"\n',
    '\t\t"mantis": return "螳螂"\n\t\t"nightingale": return "夜鶯"\n',
    1
)

old_wd_races = '"donkey", "scorpion", "mantis"]'
new_wd_races = '"donkey", "scorpion", "mantis", "nightingale"]'
assert wd.count(old_wd_races) == 3, f"Expected 3 occurrences of old_wd_races in wardrobe_dialog.gd, found {wd.count(old_wd_races)}"
wd = wd.replace(old_wd_races, new_wd_races)

with open(wd_path, "w", encoding="utf-8") as f:
    f.write(wd)
print("Updated wardrobe_dialog.gd")
