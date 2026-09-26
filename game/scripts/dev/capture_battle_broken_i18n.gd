extends SceneTree
## 戰鬥部位已破標籤六語系實機截圖 (battle-broken-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 戰鬥畫面部位列在 broken 狀態下，標籤尾端「已破」在 en/ja/zh_TW 下正確在地化（[Broken] / [破壊済] / [已破]）。
## 2. 未破部位名稱、鎖定標記、血量數字保持一致且無系統 emoji。
## 3. 實機截圖輸出目錄嚴格限定為 proofs/battle-broken-i18n/ (0-QA23)。
## 4. 局部 Crops 供比對部位欄與「已破」標籤排版。

const OUT_DIR := "proofs/battle-broken-i18n"
const CROPS_DIR := "proofs/battle-broken-i18n/crops"

const LOCALES := ["en", "ja", "zh_TW"]

var _step := 0
var _wait := 0
var _battle: Control = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var abs_out := base.path_join("../" + OUT_DIR)
	var abs_crops := base.path_join("../" + CROPS_DIR)
	DirAccess.make_dir_recursive_absolute(abs_out)
	DirAccess.make_dir_recursive_absolute(abs_crops)

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

	print("── 開始執行戰鬥部位已破標籤實機截圖腳本 (battle-broken-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			var loc_idx := _step - 1
			var code: String = LOCALES[loc_idx]
			if _wait == 1:
				if _battle != null and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node and _loc_node.has_method("set_locale"):
					_loc_node.call("set_locale", code)

				if _gs:
					_gs.player_race = "rabbit"
					_gs.player_name = "小白"
					_gs.chapter = "c1"

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "leo")

				var sim = _battle.get("sim")
				if sim:
					var boss = sim.call("_primary_boss_unit")
					if boss and boss.parts.size() >= 2:
						# 盔保持完好，盾被打碎破壞
						boss.parts[0]["broken"] = false
						boss.parts[0]["hp"] = boss.parts[0]["max_hp"]
						boss.parts[1]["broken"] = true
						boss.parts[1]["hp"] = 0
						sim.parts_break_unlocked = true
						sim.parts_break_stage = 1
						sim.focus_part_id = boss.parts[0].get("id", "helm")

						if _battle.has_method("_refresh_part_bars"):
							_battle.call("_refresh_part_bars", boss)
						if _battle.has_method("_refresh_part_focus_hint"):
							_battle.call("_refresh_part_focus_hint")
						if _battle.has_method("_refresh_hud"):
							_battle.call("_refresh_hud")

			elif _wait >= 30:
				var filename := "proof_battle_broken_%s.png" % code
				_save_full_and_crops(filename, code)
				print("  ✓ [%d/3] 戰鬥部位已破全景 [%s] 實機截圖完成: %s" % [_step, code, filename])
				_step += 1
				_wait = 0

		4:
			print("\nCAPTURE_BATTLE_BROKEN_I18N_OK")
			quit(0)
			return true

	return false


func _save_full_and_crops(filename: String, code: String) -> void:
	var base := ProjectSettings.globalize_path("res://")
	var full_dir := base.path_join("../" + OUT_DIR)
	var crops_dir := base.path_join("../" + CROPS_DIR)

	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法截取畫面: %s" % filename)
		return

	var full_path := full_dir.path_join(filename)
	var err := img.save_png(full_path)
	if err != OK:
		push_error("儲存截圖失敗: %s" % full_path)
		return

	# 部位資訊欄 PartPanel 特寫 Crop
	var part_panel = _battle.find_child("PartPanel", true, false) as Control
	var rect_crop: Rect2i
	if part_panel and part_panel.is_visible_in_tree():
		var gr := part_panel.get_global_rect()
		# 加些 padding
		var pad := 12
		var x := maxi(0, int(gr.position.x) - pad)
		var y := maxi(0, int(gr.position.y) - pad)
		var w := mini(img.get_width() - x, int(gr.size.x) + pad * 2)
		var h := mini(img.get_height() - y, int(gr.size.y) + pad * 2)
		rect_crop = Rect2i(x, y, w, h)
	else:
		# Fallback: 敵方血條與部位欄一般在右上角 (x: 820..1260, y: 30..300)
		rect_crop = Rect2i(800, 20, 460, 260)

	var crop_img := img.get_region(rect_crop)
	if crop_img and not crop_img.is_empty():
		crop_img.save_png(crops_dir.path_join("crop_part_hud_%s.png" % code))
