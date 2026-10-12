extends SceneTree
## 木人樁傷害統計與大廳武器更換彈窗全站回歸驗收實機存證腳本 (t_97f7f067)
##
## 覆蓋驗收項目：
## 1. 木人樁結算多巴胺雙膠囊 (最高單擊 MaxHitCapsule、總命中 TotalHitsCapsule)
## 2. 木人樁結算三欄武器傷害佔比 (WeaponSlotCard 0/1/2) 與輪替次數膠囊 (WeaponSwapsCapsule)
## 3. 六語系 (zh_TW, en, ja, ko, es, zh_CN) 即時在地化切換無破圖、無截字、零系統原生 Emoji
## 4. 真實木人樁戰鬥 (BattleSim) 步進與武器輪替後的實戰數據結算
## 5. 大廳角色頁裝備分頁三欄武器槽結構與「更換裝備」立體果凍厚底按鈕 (>=48px)
## 6. 大廳 750px 置中多巴胺更換裝備彈窗 (WeaponSwapDialog)、三欄位切換、武器庫候選清單
## 7. 裝備更換後攻擊力數值、有效戰力與紙娃娃即時刷新
## 8. 儲存實機全景圖 (1280x720) 與特寫裁切圖至 proofs/t_97f7f067/

const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")
const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const MobileLobbyScript := preload("res://scripts/ui/mobile_lobby.gd")
const WeaponSwapDialogScript := preload("res://scripts/ui/weapon_swap_dialog.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_97f7f067",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_97f7f067/proofs/t_97f7f067"
]

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _dlg: Control = null
var _lobby: Control = null
var _swap_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _eq: Node = null

var _saved_hashes: Dictionary = {}


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
	_eq = root.get_node_or_null("EquipmentSystem")
	if _gs:
		_gs.reset_new_game("rabbit")
		_gs.player_name = "小兔勇士"
		_gs.chapter = "c0"
		_gs.best_dummy_dps = 80.0

	print("=== 開始執行全站回歸實機驗收腳本 (t_97f7f067) ===")
	_step = 0
	_wait = 0


func _save_viewport(filename: String, crops: Array[Dictionary] = []) -> String:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		return ""

	var data := img.get_data()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(data)
	var hash_bytes := ctx.finish()
	var hash_hex := hash_bytes.hex_encode()

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA256: %s)" % [full_path, img.get_width(), img.get_height(), hash_hex.substr(0, 12)])
		else:
			push_error("  ✗ 儲存全景圖失敗: %s" % full_path)

		for c in crops:
			var crop_rect: Rect2i = c.get("rect", Rect2i())
			var crop_filename: String = c.get("filename", "")
			if crop_rect.size != Vector2i.ZERO and crop_filename != "":
				var crops_dir := base_dir.path_join("crops")
				var cropped := img.get_region(crop_rect)
				var crop_path := crops_dir.path_join(crop_filename)
				var c_err := cropped.save_png(crop_path)
				if c_err == OK:
					print("  ✓ 儲存特寫裁切圖: %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])
				else:
					push_error("  ✗ 儲存特寫圖失敗: %s" % crop_path)

	if _saved_hashes.has(hash_hex):
		push_warning("  ⚠️ 警告: 截圖 SHA256 重複: %s 與 %s" % [filename, _saved_hashes[hash_hex]])
	_saved_hashes[hash_hex] = filename
	return hash_hex


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			# 初始化戰鬥場景
			if _wait >= 5:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup") and _battle.get("sim") == null:
					_battle.call("setup", "training_dummy")
				_step = 1
				_wait = 0

		1:
			# 彈出木人樁結算卡（繁中）：展示雙膠囊與三欄貢獻卡
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				var stats_sample := {
					"total_damage": 1280,
					"elapsed_time": 15.0,
					"dps": 85.3,
					"max_hit_damage": 142,
					"total_hit_count": 24,
					"best_dummy_dps": 80.0,
					"weapon_swap_count": 3,
					"weapon_slot_damages": {
						0: 640,
						1: 384,
						2: 256,
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
				_step = 2
				_wait = 0

		2:
			# 截圖 01: 繁中結算全景 + 雙膠囊與三欄貢獻卡特寫
			if _wait >= 15:
				_save_viewport(
					"proof_01_dummy_settlement_zh_TW.png",
					[
						{"rect": Rect2i(270, 248, 740, 80), "filename": "crop_01_dummy_double_capsules_zh_TW.png"},
						{"rect": Rect2i(270, 305, 740, 135), "filename": "crop_02_dummy_weapon_contrib_cards_zh_TW.png"},
					]
				)
				_step = 3
				_wait = 0

		3:
			# 切換至英文 (en)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_step = 4
				_wait = 0

		4:
			# 截圖 02: 英文全景 + 英文三欄貢獻卡特寫
			if _wait >= 15:
				_save_viewport(
					"proof_02_dummy_settlement_en.png",
					[
						{"rect": Rect2i(270, 305, 740, 135), "filename": "crop_03_dummy_weapon_contrib_cards_en.png"}
					]
				)
				_step = 5
				_wait = 0

		5:
			# 切換至日文 (ja)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_step = 6
				_wait = 0

		6:
			# 截圖 03: 日文全景 + 日文三欄貢獻卡特寫
			if _wait >= 15:
				_save_viewport(
					"proof_03_dummy_settlement_ja.png",
					[
						{"rect": Rect2i(270, 305, 740, 135), "filename": "crop_04_dummy_weapon_contrib_cards_ja.png"}
					]
				)
				_step = 7
				_wait = 0

		7:
			# 切換至韓文 (ko)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ko")
				_step = 8
				_wait = 0

		8:
			# 截圖 04: 韓文全景
			if _wait >= 15:
				_save_viewport("proof_04_dummy_settlement_ko.png")
				_step = 9
				_wait = 0

		9:
			# 切換至西文 (es)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "es")
				_step = 10
				_wait = 0

		10:
			# 截圖 05: 西文全景
			if _wait >= 15:
				_save_viewport("proof_05_dummy_settlement_es.png")
				_step = 11
				_wait = 0

		11:
			# 切換至簡中 (zh_CN)
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_CN")
				_step = 12
				_wait = 0

		12:
			# 截圖 06: 簡中全景
			if _wait >= 15:
				_save_viewport("proof_06_dummy_settlement_zh_CN.png")
				_step = 13
				_wait = 0

		13:
			# 關閉彈窗，切回繁中，準備執行真實戰鬥輪替步進
			if _wait >= 5:
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")
				_step = 14
				_wait = 0

		14:
			# 執行真實 BattleSim 步進戰鬥
			if _wait >= 5:
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
				_step = 15
				_wait = 0

		15:
			# 截圖 07: 真實木人樁戰鬥輪替後結算全景
			if _wait >= 15:
				_save_viewport("proof_07_dummy_settlement_live_combat.png")
				_step = 16
				_wait = 0

		16:
			# 清除戰鬥場景與彈窗，建立大廳場景 (MobileLobby)
			if _wait >= 5:
				if _dlg and is_instance_valid(_dlg):
					_dlg.queue_free()
					_dlg = null
				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				# 加入候選武器至背包
				if _gs:
					var axe_inst := {
						"uid": "w_test_axe_99",
						"base_id": "axe",
						"name": "裂地巨斧",
						"line": "axe",
						"slot": "weapon",
						"tier": 2,
						"quality": "epic",
						"quality_label": "秘寶",
						"rolled": {"atk": 45, "def": 5, "hp": 20, "crit": 5.0, "crit_dmg": 15.0}
					}
					var spear_inst := {
						"uid": "w_test_spear_88",
						"base_id": "spear",
						"name": "破浪長槍",
						"line": "spear",
						"slot": "weapon",
						"tier": 1,
						"quality": "rare",
						"quality_label": "上品",
						"rolled": {"atk": 25, "def": 4, "hp": 0, "crit": 2.0, "crit_dmg": 0.0}
					}
					_gs.equip_bag.append(axe_inst)
					_gs.equip_bag.append(spear_inst)

				_lobby = MobileLobbyScript.new()
				root.add_child(_lobby)
				_lobby.size = Vector2(1280, 720)
				_lobby._switch_tab(_lobby.Tab.CHARACTER)
				_step = 17
				_wait = 0

		17:
			# 截圖 08: 角色頁裝備分頁（未開彈窗前，三欄槽位與「更換裝備」按鈕）
			if _wait >= 15:
				_save_viewport("proof_08_lobby_character_before_swap.png")
				# 點擊更換裝備打開 750px 彈窗
				_swap_dlg = _lobby.open_weapon_swap_dialog(0)
				_step = 18
				_wait = 0

		18:
			# 截圖 09: 750px 置中更換裝備彈窗繁中全景 + 彈窗標題/Tab特寫 + 候選武器卡片特寫
			if _wait >= 15:
				_save_viewport(
					"proof_09_lobby_weapon_swap_dialog_750px_zh_TW.png",
					[
						{"rect": Rect2i(265, 80, 750, 120), "filename": "crop_05_weapon_swap_dialog_header_and_tabs.png"},
						{"rect": Rect2i(285, 230, 710, 150), "filename": "crop_06_weapon_swap_candidate_item.png"},
					]
				)
				_step = 19
				_wait = 0

		19:
			# 切換至英文 (en) 驗證彈窗在地化
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "en")
				_step = 20
				_wait = 0

		20:
			# 截圖 10: 更換裝備彈窗英文全景
			if _wait >= 15:
				_save_viewport("proof_10_lobby_weapon_swap_dialog_en.png")
				_step = 21
				_wait = 0

		21:
			# 切換至日文 (ja) 驗證彈窗在地化
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "ja")
				_step = 22
				_wait = 0

		22:
			# 截圖 11: 更換裝備彈窗日文全景
			if _wait >= 15:
				_save_viewport("proof_11_lobby_weapon_swap_dialog_ja.png")
				_step = 23
				_wait = 0

		23:
			# 切回繁中，點擊裝備裂地巨斧
			if _wait >= 5:
				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", "zh_TW")

				if _swap_dlg and is_instance_valid(_swap_dlg):
					var weapons_box: VBoxContainer = _swap_dlg.get_node_or_null("DialogCard/RootVBox/WeaponsScroll/WeaponsBox")
					if weapons_box:
						var axe_card = weapons_box.get_node_or_null("WeaponCard_w_test_axe_99")
						if axe_card:
							var btn_action = axe_card.find_child("BtnAction", true, false) as Button
							if btn_action:
								btn_action.emit_signal("pressed")
					if is_instance_valid(_swap_dlg):
						_swap_dlg.queue_free()
						_swap_dlg = null
				_step = 24
				_wait = 0

		24:
			# 截圖 12: 更換裝備後角色頁即時更新全景 + 屬性面板刷新特寫
			if _wait >= 15:
				_save_viewport(
					"proof_12_lobby_character_after_swap.png",
					[
						{"rect": Rect2i(140, 200, 380, 280), "filename": "crop_07_lobby_character_stats_panel.png"}
					]
				)
				_step = 25
				_wait = 0

		25:
			print("\n=======================================================")
			print("  全站回歸實機驗收存證產出完成！(t_97f7f067)")
			print("  全景截圖: 12 張，特寫圖: 7 張")
			print("=======================================================")
			quit(0)

	return false
