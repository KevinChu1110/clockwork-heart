extends SceneTree
## 木人樁試招三欄武器輪替次數與傷害貢獻統計實機存證腳本 (t_8f9d6203)
## 覆蓋：
## 1. DummySettlementDialog 多巴胺三欄武器傷害佔比卡與輪替切換膠囊展示
## 2. 繁中 (zh_TW)、英文 (en)、日文 (ja) 六語系即時切換連動存證
## 3. 真實戰鬥步進 (BattleSim step) 與手動/自動武器輪替，累積三欄武器傷害與切換次數
## 4. 零系統原生 Emoji，OpenGL3/Compatibility 實機真畫面渲染

const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")
const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_8f9d6203",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_8f9d6203/proofs/t_8f9d6203"
]

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "小白"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	print("=== 開始執行木人樁三欄武器貢獻與輪替統計實機截圖腳本 (t_8f9d6203) ===")
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)

	_step = 0
	_wait = 0


func _save_viewport(filename: String, crop_rect: Rect2i = Rect2i(), crop_filename: String = "") -> void:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d)" % [full_path, img.get_width(), img.get_height()])
		else:
			push_error("  ✗ 儲存全景圖失敗: %s" % full_path)

		if crop_rect.size != Vector2i.ZERO and crop_filename != "":
			var crops_dir := base_dir.path_join("crops")
			var cropped := img.get_region(crop_rect)
			var crop_path := crops_dir.path_join(crop_filename)
			var c_err := cropped.save_png(crop_path)
			if c_err == OK:
				print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
			else:
				push_error("  ✗ 儲存特寫圖失敗: %s" % crop_path)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 初始化戰鬥並彈出繁中三欄武器貢獻結算卡
			if _wait >= 5:
				if _battle.has_method("setup") and _battle.get("sim") == null:
					_battle.call("setup", "training_dummy")
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				var stats_sample := {
					"total_damage": 840,
					"elapsed_time": 13.0,
					"dps": 64.6,
					"max_hit_damage": 98,
					"total_hit_count": 18,
					"best_dummy_dps": 80.0,
					"weapon_swap_count": 3,
					"weapon_slot_damages": {
						0: 420,
						1: 252,
						2: 168,
					},
					"weapon_slot_swaps": {
						0: 1,
						1: 1,
						2: 1,
					},
					"weapon_bars": [
						{
							"index": 0,
							"name": "白鐵長劍",
							"quality": "common",
							"quality_label": "凡品",
							"empty": false,
						},
						{
							"index": 1,
							"name": "淬毒短刃",
							"quality": "uncommon",
							"quality_label": "良品",
							"empty": false,
						},
						{
							"index": 2,
							"name": "破軍巨錘",
							"quality": "rare",
							"quality_label": "上品",
							"empty": false,
						},
					],
				}
				_dlg = DummySettlementDialogClass.show_dialog(
					_battle,
					stats_sample,
					func(): pass,
					func(): pass
				)
				_step = 1
				_wait = 0

		1:
			# 截圖 01: 繁中全景 (zh_TW) + 三欄武器貢獻卡特寫
			if _wait >= 20:
				_save_viewport(
					"proof_01_dummy_weapon_contrib_zh_TW.png",
					Rect2i(270, 305, 740, 135),
					"crop_01_weapon_contrib_zh_TW.png"
				)
				_step = 2
				_wait = 0

		2:
			# 切換至英文 (en)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_step = 3
				_wait = 0

		3:
			# 截圖 02: 英文全景 (en) + 英文三欄武器貢獻卡特寫
			if _wait >= 20:
				_save_viewport(
					"proof_02_dummy_weapon_contrib_en.png",
					Rect2i(270, 305, 740, 135),
					"crop_02_weapon_contrib_en.png"
				)
				_step = 4
				_wait = 0

		4:
			# 切換至日文 (ja)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_step = 5
				_wait = 0

		5:
			# 截圖 03: 日文全景 (ja) + 日文三欄武器貢獻卡特寫
			if _wait >= 20:
				_save_viewport(
					"proof_03_dummy_weapon_contrib_ja.png",
					Rect2i(270, 305, 740, 135),
					"crop_03_weapon_contrib_ja.png"
				)
				_step = 6
				_wait = 0

		6:
			# 關閉彈窗，切回繁中，執行真實 BattleSim 三欄武器輪替戰鬥
			if _wait >= 5:
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")

				# 建立真實多武器模擬戰鬥並步進
				var sim_stats := {
					"name": "小白",
					"max_hp": 80,
					"hp": 80,
					"atk": 25,
					"def": 6,
					"speed": 35.0,
					"crit": 15.0,
					"crit_dmg": 50.0,
					"dmg_variance": 0.05,
					"can_skill": true,
					"slash_lv": 1,
					"weapon_class": "sword",
					"weapon_loadout_active": 0,
					"weapon_loadout": [
						{
							"index": 0,
							"uid": "w_sword_live",
							"name": "白鐵長劍",
							"line": "sword",
							"weapon_atk": 12,
							"unlocked": true,
							"empty": false,
							"quality": "common",
							"quality_label": "凡品",
							"active": true,
						},
						{
							"index": 1,
							"uid": "w_dagger_live",
							"name": "淬毒短刃",
							"line": "dagger",
							"weapon_atk": 16,
							"unlocked": true,
							"empty": false,
							"quality": "uncommon",
							"quality_label": "良品",
							"active": false,
						},
						{
							"index": 2,
							"uid": "w_hammer_live",
							"name": "破軍巨錘",
							"line": "hammer",
							"weapon_atk": 22,
							"unlocked": true,
							"empty": false,
							"quality": "rare",
							"quality_label": "上品",
							"active": false,
						},
					],
				}
				var live_sim: BattleSimClass = BattleSimClass.make_dummy_fight(sim_stats)

				# Slot 0 打擊
				for _i in range(35):
					live_sim.step(0.1)

				# 切換至 Slot 1
				live_sim.switch_weapon_slot(1)
				for _i in range(35):
					live_sim.step(0.1)

				# 切換至 Slot 2
				live_sim.switch_weapon_slot(2)
				for _i in range(35):
					live_sim.step(0.1)

				var real_combat_stats: Dictionary = live_sim.get_dummy_combat_stats()
				print("  真實多武器戰鬥累計: dmg=%d, swaps=%d, slot0=%d, slot1=%d, slot2=%d" % [
					int(real_combat_stats.get("total_damage", 0)),
					int(real_combat_stats.get("weapon_swap_count", 0)),
					int((real_combat_stats.get("weapon_slot_damages", {}) as Dictionary).get(0, 0)),
					int((real_combat_stats.get("weapon_slot_damages", {}) as Dictionary).get(1, 0)),
					int((real_combat_stats.get("weapon_slot_damages", {}) as Dictionary).get(2, 0)),
				])
				_dlg = DummySettlementDialogClass.show_dialog(
					_battle,
					real_combat_stats,
					func(): pass,
					func(): pass
				)
				_step = 7
				_wait = 0

		7:
			# 截圖 04: 真實多武器戰鬥數據結算卡全景 + 特寫
			if _wait >= 20:
				_save_viewport(
					"proof_04_dummy_weapon_contrib_live.png",
					Rect2i(270, 305, 740, 135),
					"crop_04_weapon_contrib_live.png"
				)
				_step = 8
				_wait = 0

		8:
			print("=== 實機截圖存證完成 (t_8f9d6203) ===")
			quit(0)
			return true

	return false
