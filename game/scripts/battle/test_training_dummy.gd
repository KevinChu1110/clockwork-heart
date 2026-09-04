extends SceneTree
## 木人樁試招把關測試：godot --headless -s res://scripts/battle/test_training_dummy.gd
##
## 守四件事：
##   1. 能量消耗為 0（不耗能量／體力）
##   2. 木人樁不反擊、固定血量（500 HP）
##   3. 玩家攻擊累積怒氣、可放招、擊破後算勝利
##   4. SpriteDB 能讀到木人立繪資產

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")


func _stats() -> Dictionary:
	return {
		"name": "測試勇者",
		"max_hp": 80,
		"hp": 80,
		"atk": 20,
		"def": 6,
		"speed": 12.0,
		"crit": 5.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.05,
		"can_skill": true,
		"slash_lv": 1,
		"weapon_class": "sword",
	}


func _initialize() -> void:
	var ok := true

	## 1) 能量消耗檢驗：木人樁必須為 0
	var en: Node = root.get_node_or_null("EnergySystem")
	if en != null:
		var cost: int = int(en.cost_for_mode("training_dummy"))
		if cost != 0:
			push_error("木人樁試招應為 0 消耗，得 %d" % cost)
			ok = false
		else:
			print("energy cost OK: 0")
	else:
		push_error("找不到 EnergySystem autoload")
		ok = false

	## 2) 戰鬥模擬建立：不反擊、固定血量 500
	var stats := _stats()
	var sim = BattleSim.make_dummy_fight(stats)
	var player = sim.get_unit("player")
	var dummy = sim.get_unit("training_dummy")

	if player == null or dummy == null:
		push_error("make_dummy_fight 未正確生成 player 或 training_dummy")
		ok = false
	else:
		if dummy.max_hp != 500 or dummy.hp != 500:
			push_error("木人樁血量應為 500，得 %d / %d" % [dummy.hp, dummy.max_hp])
			ok = false
		if dummy.atk != 0:
			push_error("木人樁攻擊力應為 0，得 %d" % dummy.atk)
			ok = false
		if dummy.team != BattleUnit.Team.ENEMY:
			push_error("木人樁應為 ENEMY 陣營")
			ok = false
		print("dummy stats OK: hp=500, atk=0, team=ENEMY")

	## 3) 模擬步進：木人樁不反擊、玩家出招並累積怒氣
	if ok and sim != null and player != null and dummy != null:
		var start_player_hp: int = player.hp
		var total_dt := 0.0
		while total_dt < 6.0 and not sim.finished:
			sim.step(0.1)
			total_dt += 0.1

		## 玩家不該受傷（木人不反擊）
		if player.hp < start_player_hp:
			push_error("木人樁反擊了玩家！玩家 HP 由 %d 降至 %d" % [start_player_hp, player.hp])
			ok = false
		else:
			print("dummy no counter-attack OK: player hp kept %d" % player.hp)

		## 木人應受到玩家普通攻擊
		if dummy.hp >= 500:
			push_error("玩家未對木人造成傷害，dummy hp 仍為 %d" % dummy.hp)
			ok = false
		else:
			print("player hits dummy OK: dummy hp reduced to %d" % dummy.hp)

		## 玩家攻擊應累積怒氣
		if player.rage <= 0.0:
			push_error("玩家命中木人但未累積怒氣: rage=%.1f" % player.rage)
			ok = false
		else:
			print("player gains rage OK: rage=%.1f" % player.rage)

	## 4) 擊倒木人：結算為勝利
	if ok:
		var sim_kill = BattleSim.make_dummy_fight(_stats())
		var d_kill = sim_kill.get_unit("training_dummy")
		d_kill.take_damage(500)
		sim_kill.step(0.01)
		if not sim_kill.finished or not sim_kill.won:
			push_error("木人血量歸零應判定獲勝 finished=%s won=%s" % [sim_kill.finished, sim_kill.won])
			ok = false
		else:
			print("dummy kill win OK")

	## 5) 美術資產：SpriteDB 能取出木人立繪
	var tex = SpriteDB.boss("training_dummy")
	if tex == null:
		push_error("SpriteDB.boss('training_dummy') 未取得到木人立繪")
		ok = false
	else:
		print("dummy texture OK: ", tex.resource_path if tex is Resource else "loaded")

	if ok:
		print("TRAINING_DUMMY_OK")
		quit(0)
	else:
		print("TRAINING_DUMMY_FAIL")
		quit(1)
