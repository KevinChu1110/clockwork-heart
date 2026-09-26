extends SceneTree
## 《發條之心》探索性 QA 第三十九輪 實機截圖腳本 (qa_round39)
## 涵蓋範圍：
## 1. 大廳繁中／英全景 (0-QA25 頂欄、四殿堂、出征、底部 Dock 同步切換)
## 2. 創角英文全景 (分頁、種族卡、外裝、塗裝名稱在地化)
## 3. 衣櫥英文全景 (英雄換裝彈窗、卡片、操作鈕在地化)
## 4. 戰鬥英文全景 (打雷歐時左右血條與角色名完整可見、頂欄鎖定提示自動折行限寬無溢出)
## 5. 戰鬥繁中全景 (部位列「已破」標籤、無截字、零 emoji)
## 6. 戰鬥西語全景 (長譯代表驗證)
## 7. OUT_DIR 獨立指定為 proofs/qa_round39/ (0-QA23)

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round39"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round39/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

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
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	print("── 開始執行 QA 第三十九輪實機截圖腳本 (qa_round39) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 大廳繁中全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait >= 25:
				var path := "%s/proof_01_lobby_zh_TW.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/7] 大廳繁中全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 大廳英文全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.call("reset_new_game")
					_gs.set("player_race", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("chapter", "c0")
					_gs.set("gold", 1000)
					_gs.set("level", 10)
					_gs.set("energy", 15)
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait >= 25:
				var path := "%s/proof_02_lobby_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/7] 大廳英文全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 創角英文全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "launch")
					demo.call("select_race", "rabbit")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 35:
				var path := "%s/proof_03_creation_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/7] 創角英文全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 衣櫥英文全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "rabbit")
						wardrobe.set("costume_index", 0)
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 45:
				var path := "%s/proof_04_wardrobe_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/7] 衣櫥英文全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 戰鬥部位已破繁中全景
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_spawn_battle("zh_TW")
			elif _wait >= 35:
				var path := "%s/proof_05_battle_broken_zh_TW.png" % OUT_DIR
				_save_screenshot(path)
				_save_hud_crop("crop_battle_hud_zh_TW.png")
				_save_part_crop("crop_part_hud_zh_TW.png")
				print("  ✓ [5/7] 戰鬥部位已破繁中全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 戰鬥部位已破英文全景 (驗收重點：英文打雷歐左右血條與角色名完整可見)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_spawn_battle("en")
			elif _wait >= 35:
				var path := "%s/proof_06_battle_broken_en.png" % OUT_DIR
				_save_screenshot(path)
				_save_hud_crop("crop_battle_hud_en.png")
				_save_part_crop("crop_part_hud_en.png")
				print("  ✓ [6/7] 戰鬥部位已破英文全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 戰鬥部位已破西語全景 (長譯代表)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "es")
				_spawn_battle("es")
			elif _wait >= 35:
				var path := "%s/proof_07_battle_broken_es.png" % OUT_DIR
				_save_screenshot(path)
				_save_hud_crop("crop_battle_hud_es.png")
				print("  ✓ [7/7] 戰鬥部位已破西語全景截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 8
				_wait = 0

		8:
			print("\nCAPTURE_QA_ROUND39_OK")
			quit(0)
			return true

	return false


func _spawn_battle(loc: String) -> void:
	if _gs:
		_gs.call("reset_new_game")
		_gs.set("player_race", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c1")
		_gs.set("level", 10)
		_gs.set("gold", 1000)

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle = b_scn.instantiate()
	root.add_child(battle)
	_current_node = battle
	if battle.has_method("setup"):
		battle.call("setup", "leo")

	var sim = battle.get("sim")
	if sim:
		var boss = sim.call("_primary_boss_unit")
		if boss and boss.parts.size() >= 2:
			boss.parts[0]["broken"] = false
			boss.parts[0]["hp"] = boss.parts[0]["max_hp"]
			boss.parts[1]["broken"] = true
			boss.parts[1]["hp"] = 0
			sim.parts_break_unlocked = true
			sim.parts_break_stage = 1
			sim.focus_part_id = boss.parts[0].get("id", "helm")

			if battle.has_method("_refresh_part_bars"):
				battle.call("_refresh_part_bars", boss)
			if battle.has_method("_refresh_part_focus_hint"):
				battle.call("_refresh_part_focus_hint")
			if battle.has_method("_refresh_hud"):
				battle.call("_refresh_hud")


func _save_screenshot(filepath: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filepath)
		return
	var err := img.save_png(filepath)
	if err != OK:
		push_error("儲存截圖失敗: %s" % filepath)


func _save_part_crop(crop_filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return

	var rect_crop := Rect2i(800, 20, 460, 260)
	if _current_node:
		var part_panel = _current_node.find_child("PartPanel", true, false) as Control
		if part_panel and part_panel.is_visible_in_tree():
			var gr := part_panel.get_global_rect()
			var pad := 12
			var x := maxi(0, int(gr.position.x) - pad)
			var y := maxi(0, int(gr.position.y) - pad)
			var w := mini(img.get_width() - x, int(gr.size.x) + pad * 2)
			var h := mini(img.get_height() - y, int(gr.size.y) + pad * 2)
			rect_crop = Rect2i(x, y, w, h)

	var crop_img := img.get_region(rect_crop)
	if crop_img and not crop_img.is_empty():
		crop_img.save_png("%s/%s" % [CROPS_DIR, crop_filename])


func _save_hud_crop(crop_filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return

	var rect_crop := Rect2i(0, 0, 1280, 160)
	if _current_node:
		var sb = _current_node.find_child("SideBars", true, false) as Control
		if sb and sb.is_visible_in_tree():
			var gr := sb.get_global_rect()
			var pad := 10
			var x := maxi(0, int(gr.position.x) - pad)
			var y := maxi(0, int(gr.position.y) - pad)
			var w := mini(img.get_width() - x, int(gr.size.x) + pad * 2)
			var h := mini(img.get_height() - y, int(gr.size.y) + pad * 2)
			rect_crop = Rect2i(x, y, w, h)

	var crop_img := img.get_region(rect_crop)
	if crop_img and not crop_img.is_empty():
		crop_img.save_png("%s/%s" % [CROPS_DIR, crop_filename])
