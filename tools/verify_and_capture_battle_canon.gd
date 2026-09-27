extends SceneTree
## 戰鬥日誌世界觀用詞、英文攻擊鈕折字修復、王者斬日誌標籤驗證與截圖

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

	_out_dir = ProjectSettings.globalize_path("res://../proofs/battle-log-canon-hud")
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
		_gs.set("level", 25)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)

	print("=== 開始驗證 3 大修復項 ===")
	_run_unit_checks()
	_step = 1
	_wait = 0

func _run_unit_checks() -> void:
	var BattleViewClass = load("res://scripts/battle/battle_view.gd")

	# 1. 驗證繁中與六語系 viking 相剋提示
	print("--- 1. 驗證戰鬥相剋提示世界觀 ---")
	if _loc_node: _loc_node.call("set_locale", "zh_TW")
	ContentLocClass.reload()
	var zh_hint: String = BattleViewClass.call("_kin_hint", "viking")
	print("  zh_TW viking hint: ", zh_hint)
	assert(zh_hint.contains("金屬板件") or zh_hint.contains("板件"), "繁中相剋提示必須包含板件")
	assert(zh_hint.contains("發條"), "繁中相剋提示必須包含發條")
	assert(not zh_hint.contains("筋骨"), "繁中相剋提示不准出現筋骨")
	assert(not zh_hint.contains("斧鎚") and not zh_hint.contains("斧錘"), "繁中相剋提示不准出現斧鎚")
	print("  ✓ 繁中相剋提示合規 (金屬板件/發條，零筋骨/斧錘)")

	var locales := ["zh_CN", "en", "ja", "ko", "es"]
	for loc in locales:
		if _loc_node: _loc_node.call("set_locale", loc)
		ContentLocClass.reload()
		var h: String = BattleViewClass.call("_kin_hint", "viking")
		print("  [%s] viking hint: %s" % [loc, h])
		assert(not h.contains("筋骨") and not h.contains("axe and hammer"), "[%s] 相剋提示不准出現筋骨或斧鎚" % loc)
	print("  ✓ 六語系相剋提示同步合規")

	# 2. 驗證王者斬與日誌 BBCode 解析
	print("--- 2. 驗證王者斬日誌 BBCode 解析 ---")
	if _loc_node: _loc_node.call("set_locale", "en")
	ContentLocClass.reload()
	var bv = BattleViewClass.new()
	var rtl := RichTextLabel.new()
	rtl.bbcode_enabled = true
	var rec := {
		"type": "plain",
		"text": "[The King's Cut] Rampant Clockwork Lion deals 37 damage"
	}
	var rendered: String = bv.call("_render_log_record", rec)
	rtl.append_text(rendered)
	var parsed: String = rtl.get_parsed_text()
	print("  Rendered: ", rendered)
	print("  Parsed:   ", parsed)
	assert(not parsed.contains("[/b]"), "日誌不可露出 [/b]")
	assert(parsed.contains("[The King's Cut] Rampant Clockwork Lion"), "技能名與敵名中間必須有空格")
	print("  ✓ 英文日誌王者斬結算零 [/b] 露出，技能名與敵名有空格分隔")
	bv.free()
	rtl.free()

func _setup_battle(mode: String = "colossus_lion") -> void:
	if is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if b_scn == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		quit(1)
		return
	_battle = b_scn.instantiate()
	_battle.set_anchors_preset(Control.PRESET_FULL_RECT)
	_battle.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_battle.size_flags_vertical = Control.SIZE_EXPAND_FILL
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", mode)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 繁中 (zh_TW) 實機：巨偶王者斬命中 / 格擋失敗受創畫面
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				_setup_battle("colossus_lion")
			elif _wait == 8:
				var sim: Object = _battle.get("sim")
				if sim:
					sim.call("trigger_colossus_windup")
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						lion.set("state_timer", 1.60)
						_battle.call("_update_parry_countdown", lion)
			elif _wait == 10:
				_battle.call("_do_parry")
			elif _wait == 14:
				var sim: Object = _battle.get("sim")
				if sim:
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						sim.call("_resolve_king_slash_hit", lion)
			elif _wait == 20:
				_battle.set_process(false)
			elif _wait == 24:
				var path := "%s/proof_01_zh_parry_failure_kings_cut.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/2] 繁中 (zh_TW) 格擋失敗受王者斬實機截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		2:
			# 英文 (en) 實機：英文常態 Attack 按鈕 + 巨偶王者斬命中 / 格擋失敗受創畫面
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				_setup_battle("colossus_lion")
			elif _wait == 8:
				var sim: Object = _battle.get("sim")
				if sim:
					sim.call("trigger_colossus_windup")
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						lion.set("state_timer", 1.60)
						_battle.call("_update_parry_countdown", lion)
			elif _wait == 10:
				_battle.call("_do_parry")
			elif _wait == 14:
				var sim: Object = _battle.get("sim")
				if sim:
					var lion = sim.call("get_unit", "colossus_lion")
					if lion:
						sim.call("_resolve_king_slash_hit", lion)
			elif _wait == 20:
				_battle.set_process(false)
			elif _wait == 24:
				# 檢查英文 Attack 按鈕屬性
				var btn_attack: Button = _battle.get("_btn_attack")
				if btn_attack:
					print("  [en] Attack button text: '", btn_attack.text, "'")
					print("  [en] Attack button size: ", btn_attack.size, ", min_size: ", btn_attack.custom_minimum_size)
					print("  [en] Attack autowrap_mode: ", btn_attack.autowrap_mode)
					assert(btn_attack.custom_minimum_size.y >= 48.0, "按鈕熱區高 >= 48px")
					assert(btn_attack.autowrap_mode == TextServer.AUTOWRAP_OFF, "英文攻擊鈕單字不可折行")
				var path := "%s/proof_02_en_parry_failure_kings_cut.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/2] 英文 (en) 格擋失敗受王者斬實機截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("=== 全數驗證通過，截圖已產出至 %s ===" % _out_dir)
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img != null:
		var err := img.save_png(abs_path)
		if err != OK:
			push_error("無法儲存截圖至: " + abs_path)
