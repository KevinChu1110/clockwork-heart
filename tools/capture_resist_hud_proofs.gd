extends SceneTree
## 抗性吃力／過載戰鬥場上顯示受傷加深 實機截圖腳本 (1280x720)

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")

var _out_dir: String = ""
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

	_out_dir = ProjectSettings.globalize_path("res://../proofs/resist-combat-hud")
	DirAccess.make_dir_recursive_absolute(_out_dir)

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

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 10)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)

	print("=== 開始產出抗性吃力/過載 1280x720 實機截圖 ===")
	_step = 1
	_wait = 0

func _setup_battle_with_underlevel(locale: String, diff: int) -> void:
	if is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	if _loc_node:
		_loc_node.call("set_locale", locale)
	ContentLocClass.reload()

	if _gs:
		_gs.set("level", 10)
		var sug_lv := 10 + diff if diff > 0 else 10
		_gs.set("current_suggest_lv", sug_lv)

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	assert(b_scn != null, "無法載入 battle.tscn")
	_battle = b_scn.instantiate()
	_battle.set_anchors_preset(Control.PRESET_FULL_RECT)
	_battle.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_battle.size_flags_vertical = Control.SIZE_EXPAND_FILL
	root.add_child(_battle)
	_battle.call("setup", "wolf")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 1. 繁中 (zh_TW) 吃力 (diff = 2 -> x1.2)
			if _wait == 2:
				_setup_battle_with_underlevel("zh_TW", 2)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "繁中吃力 notice 必須顯示")
				assert(notice.text == "吃力 · 受傷 ×1.2", "繁中吃力文字必須為 '吃力 · 受傷 ×1.2'")
			elif _wait == 14:
				var path := "%s/proof_01_zh_strained_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/6] 繁中吃力 (x1.2) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		2:
			# 2. 繁中 (zh_TW) 過載 (diff = 6 -> x1.5)
			if _wait == 2:
				_setup_battle_with_underlevel("zh_TW", 6)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "繁中過載 notice 必須顯示")
				assert(notice.text == "過載 · 受傷 ×1.5", "繁中過載文字必須為 '過載 · 受傷 ×1.5'")
			elif _wait == 14:
				var path := "%s/proof_02_zh_overload_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/6] 繁中過載 (x1.5) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 3
				_wait = 0

		3:
			# 3. 英文 (en) 吃力 (diff = 2 -> x1.2)
			if _wait == 2:
				_setup_battle_with_underlevel("en", 2)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "英文吃力 notice 必須顯示")
				assert(notice.text == "Strained · Dmg ×1.2", "英文吃力文字必須為 'Strained · Dmg ×1.2'")
			elif _wait == 14:
				var path := "%s/proof_03_en_strained_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/6] 英文吃力 (x1.2) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 4
				_wait = 0

		4:
			# 4. 英文 (en) 過載 (diff = 6 -> x1.5)
			if _wait == 2:
				_setup_battle_with_underlevel("en", 6)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "英文過載 notice 必須顯示")
				assert(notice.text == "Overload · Dmg ×1.5", "英文過載文字必須為 'Overload · Dmg ×1.5'")
			elif _wait == 14:
				var path := "%s/proof_04_en_overload_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/6] 英文過載 (x1.5) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 5
				_wait = 0

		5:
			# 5. 繁中 (zh_TW) 安全檔 (達標 diff = 0 -> x1.0，無這句)
			if _wait == 2:
				_setup_battle_with_underlevel("zh_TW", 0)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and not notice.visible, "繁中安全檔 notice 必須隱藏")
				assert(notice.text == "", "繁中安全檔 notice 文字必須為空")
			elif _wait == 14:
				var path := "%s/proof_05_zh_safe_nodisplay_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [5/6] 繁中達標安全檔 (無提示) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 6
				_wait = 0

		6:
			# 6. 英文 (en) 安全檔 (達標 diff = 0 -> x1.0，無這句)
			if _wait == 2:
				_setup_battle_with_underlevel("en", 0)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and not notice.visible, "英文安全檔 notice 必須隱藏")
				assert(notice.text == "", "英文安全檔 notice 文字必須為空")
			elif _wait == 14:
				var path := "%s/proof_06_en_safe_nodisplay_1280x720.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [6/6] 英文達標安全檔 (無提示) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				# 恢復繁中與乾淨狀態
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				if _gs:
					_gs.set("current_suggest_lv", 0)

				print("=== 6 張實機截圖產出完畢，全部驗證通過！ ===")
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img != null:
		var err := img.save_png(abs_path)
		if err != OK:
			push_error("無法儲存截圖至: " + abs_path)
