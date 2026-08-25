extends SceneTree
## godot --headless -s res://scripts/battle/test_skirmish_auto.gd
## 雜魚當場結算哨兵：resolve_auto 能分勝負、強者勝弱者敗、
## gather_player_stats 給得出開戰數值。

const BattleSim = preload("res://scripts/battle/battle_sim.gd")


func _stats(hp: int, atk: int, df: int) -> Dictionary:
	return {
		"name": "測試兔", "max_hp": hp, "hp": hp,
		"atk": atk, "def": df, "speed": 13,
		"crit": 8.0, "crit_dmg": 50.0, "dmg_variance": 0.06,
		"can_skill": false,
	}


func _initialize() -> void:
	var ok := true

	## 1) 強配置：必勝且帶血離場
	var sim = BattleSim.make_world_fight(_stats(400, 60, 25), "ash_rat")
	sim.rng.seed = 7
	var res: Dictionary = BattleSim.resolve_auto(sim)
	if not bool(res.get("won", false)):
		push_error("strong player should win: %s" % str(res))
		ok = false
	elif int(res.get("hp_left", 0)) <= 0:
		push_error("winner should keep hp: %s" % str(res))
		ok = false
	else:
		print("strong win OK hp_left=", res.get("hp_left"))

	## 2) 弱配置：該輸（不會無限拖台錢）
	var sim2 = BattleSim.make_world_fight(_stats(20, 1, 0), "ash_rat")
	sim2.rng.seed = 7
	var res2: Dictionary = BattleSim.resolve_auto(sim2)
	if bool(res2.get("won", false)):
		push_error("feeble player should lose: %s" % str(res2))
		ok = false
	else:
		print("weak lose OK steps=", res2.get("steps"))

	## 3) gather_player_stats：關鍵欄位齊全（探索端開戰靠它）
	var gs: Dictionary = BattleSim.gather_player_stats()
	for key in ["max_hp", "hp", "atk", "def", "speed", "crit", "hit", "eva"]:
		if not gs.has(key):
			push_error("gather_player_stats missing key %s" % key)
			ok = false
	if int(gs.get("max_hp", 0)) <= 0:
		push_error("max_hp should be positive")
		ok = false
	else:
		print("gather stats OK max_hp=", gs.get("max_hp"))

	if ok:
		print("SKIRMISH_AUTO_OK")
		quit(0)
	else:
		print("SKIRMISH_AUTO_FAIL")
		quit(1)
