extends SceneTree
## 探索性 QA 實機 Framebuffer 截圖產生器 (capture_qa_t_42696b4f.gd)
##
## 任務卡號：t_42696b4f
## 驗收規範：
## - review.md 0-QA5 / 0-QA26: 必須透過 Godot framebuffer (ViewportTexture.get_image) 直接擷取，嚴禁 PIL / 假圖
## - review.md 0-QA23: OUT_DIR 鎖定本輪獨立目錄 proofs/t_42696b4f
## - 涵蓋範圍：
##   1. 抗性吃力場上提示（繁中 / 英文）
##   2. 抗性過載場上提示（繁中 / 英文）
##   3. 戰鬥日誌世界觀（繁中：金屬板件/發條，無舊武俠詞）
##   4. 英文攻擊鈕不折字＋英文日誌王者斬無 [/b] 漏標籤
##   5. 勝利結算機芯掉落卡（繁中 / 英文零 CJK 混雜）
##   6. 舊功能回歸（大廳主城、四區與巨偶出征、發條衣櫥）
##   7. 鐵匠英文校準日誌色階名「藍」巡檢存證（記帳不修）

const ContentLocClass := preload("res://scripts/systems/content_loc.gd")
const CoreSystemClass := preload("res://scripts/systems/core_system.gd")
const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")

var OUT_DIR_NAME := "proofs/t_42696b4f"
var _out_dir: String = ""

var _step := 0
var _wait := 0

var _loc_node: Node = null
var _gs: Node = null
var _cs: Node = null
var _es: Node = null
var _inv: Node = null
var _cds: Node = null

var _battle: Control = null
var _victory_dlg: Control = null
var _lobby: Control = null
var _forge_dlg: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var env_task := OS.get_environment("HERMES_KANBAN_TASK")
	if env_task != "":
		OUT_DIR_NAME = "proofs/" + env_task

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	# 1. 裝載 Autoloads
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

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			_cs = CsClass.new()
			_cs.name = "CoreSystem"
			root.add_child(_cs)

	_es = root.get_node_or_null("EnergySystem")
	if _es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			_es = EsClass.new()
			_es.name = "EnergySystem"
			root.add_child(_es)

	_inv = root.get_node_or_null("InventorySystem")
	if _inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			_inv = InvClass.new()
			_inv.name = "InventorySystem"
			root.add_child(_inv)

	_cds = root.get_node_or_null("ColossusDailySystem")
	if _cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			_cds = CdsClass.new()
			_cds.name = "ColossusDailySystem"
			root.add_child(_cds)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 10)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)
		_gs.set("gold", 12500)
		_gs.set("weapon_tier", 3)
		_gs.set("weapon_atk", 24)
		_gs.set("weapon_name", "精煉長劍")
		_gs.call("set_flag", "c1_forged", true)
		_gs.call("set_flag", "c1_entered_city", true)
		_gs.call("set_flag", "tut_done", true)

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	print("── 開始執行探索性 QA 實機 Framebuffer 截圖 (t_42696b4f) ──")
	print("   OUT_DIR: ", _out_dir)

	_step = 1
	_wait = 0

func _setup_battle_resist(locale: String, diff: int) -> void:
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
	_battle.call("setup", "colossus_lion")

func _save_screenshot(path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var tex := vp.get_texture()
		if tex:
			var img := tex.get_image()
			if img:
				img.save_png(path)
				print("  [Screenshot] 已儲存: %s (%dx%d)" % [path, img.get_width(), img.get_height()])

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# ──────────────────────────────────────────────────────────
		# 1. 繁中 (zh_TW) 吃力 (diff = 2 -> x1.2)
		# ──────────────────────────────────────────────────────────
		1:
			if _wait == 2:
				_setup_battle_resist("zh_TW", 2)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "繁中吃力 notice 必須顯示")
				assert(notice.text == "吃力 · 受傷 ×1.2", "繁中吃力文字必須為 '吃力 · 受傷 ×1.2'")
			elif _wait == 15:
				var path := "%s/proof_01_zh_resist_strained_combat.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/12] 繁中吃力 (x1.2) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 2. 繁中 (zh_TW) 過載 (diff = 6 -> x1.5)
		# ──────────────────────────────────────────────────────────
		2:
			if _wait == 2:
				_setup_battle_resist("zh_TW", 6)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "繁中過載 notice 必須顯示")
				assert(notice.text == "過載 · 受傷 ×1.5", "繁中過載文字必須為 '過載 · 受傷 ×1.5'")
			elif _wait == 15:
				var path := "%s/proof_02_zh_resist_overload_combat.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [2/12] 繁中過載 (x1.5) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 3
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 3. 英文 (en) 吃力 (diff = 2 -> x1.2)
		# ──────────────────────────────────────────────────────────
		3:
			if _wait == 2:
				_setup_battle_resist("en", 2)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "英文吃力 notice 必須顯示")
				assert(notice.text == "Strained · Dmg ×1.2", "英文吃力文字必須為 'Strained · Dmg ×1.2'")
			elif _wait == 15:
				var path := "%s/proof_03_en_resist_strained_combat.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [3/12] 英文吃力 (x1.2) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 4
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 4. 英文 (en) 過載 (diff = 6 -> x1.5)
		# ──────────────────────────────────────────────────────────
		4:
			if _wait == 2:
				_setup_battle_resist("en", 6)
			elif _wait == 8:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null and notice.visible, "英文過載 notice 必須顯示")
				assert(notice.text == "Overload · Dmg ×1.5", "英文過載文字必須為 'Overload · Dmg ×1.5'")
			elif _wait == 15:
				var path := "%s/proof_04_en_resist_overload_combat.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [4/12] 英文過載 (x1.5) 截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 5
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 5. 繁中 (zh_TW) 戰鬥日誌世界觀（金屬板件/發條，無舊武俠詞「筋骨」「斧鎚」）
		# ──────────────────────────────────────────────────────────
		5:
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				_setup_battle_resist("zh_TW", 0)
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
			elif _wait == 25:
				var path := "%s/proof_05_zh_battle_log_canon.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [5/12] 繁中戰鬥日誌世界觀截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 6
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 6. 英文 (en) 戰鬥日誌王者斬無 [/b] 露出＋英文攻擊鈕 Attack 不折字同一行
		# ──────────────────────────────────────────────────────────
		6:
			if _wait == 2:
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				_setup_battle_resist("en", 0)
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
			elif _wait == 25:
				var btn_attack: Button = _battle.get("_btn_attack")
				if btn_attack:
					print("  [en] Attack button text: '", btn_attack.text, "' size: ", btn_attack.size)
					assert(btn_attack.text == "Attack", "英文攻擊鈕文字必須為 Attack")
					assert(btn_attack.custom_minimum_size.y >= 48.0, "按鈕熱區高度 >= 48px")
					assert(btn_attack.autowrap_mode == TextServer.AUTOWRAP_OFF, "英文攻擊鈕單字不可折行")
				var path := "%s/proof_06_en_battle_log_attack_btn.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [6/12] 英文戰鬥日誌與攻擊鈕截圖完成: %s" % path)
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 7
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 7. 繁中 (zh_TW) 巨偶勝場機芯掉落結算卡片
		# ──────────────────────────────────────────────────────────
		7:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				if _gs:
					_gs.set("player_name", "小白")
					_gs.set("level", 25)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)

				var sample_part: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 47, "HP": 230})
				sample_part["is_colossus"] = true
				sample_part["mode"] = "colossus_lion"
				_victory_dlg = BattleVictoryDialogScript.show_dialog(root, sample_part, Callable(), 450, 2)
			elif _wait >= 25:
				var path := "%s/proof_07_zh_victory_core_drop.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [7/12] 繁中勝利結算機芯掉落卡截圖完成: %s" % path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 8
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 8. 英文 (en) 巨偶勝場機芯掉落結算卡片（零 CJK 中文殘留）
		# ──────────────────────────────────────────────────────────
		8:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				if _gs:
					_gs.set("player_name", "Xiaobai")
					_gs.set("level", 25)

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)

				var sample_part: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 47, "HP": 230})
				sample_part["is_colossus"] = true
				sample_part["mode"] = "colossus_lion"
				_victory_dlg = BattleVictoryDialogScript.show_dialog(root, sample_part, Callable(), 450, 2)
			elif _wait >= 25:
				var path := "%s/proof_08_en_victory_core_drop.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [8/12] 英文勝利結算機芯掉落卡截圖完成: %s" % path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 9
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 9. 舊功能回歸檢核：大廳繁中全景 (Tab.VILLAGE)
		# ──────────────────────────────────────────────────────────
		9:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_lobby = LobbyClass.new()
					root.add_child(_lobby)
					_lobby.call("switch_tab", 0) # Tab.VILLAGE
			elif _wait >= 25:
				var path := "%s/proof_09_zh_lobby_regression.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [9/12] 大廳主城舊功能回歸截圖完成: %s" % path)
				_step = 10
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 10. 舊功能回歸檢核：出征分頁巨偶模式繁中 (Tab.ADVENTURE)
		# ──────────────────────────────────────────────────────────
		10:
			if _wait == 1:
				if is_instance_valid(_lobby):
					_lobby.call("switch_tab", 2) # Tab.ADVENTURE
			elif _wait == 8:
				if is_instance_valid(_lobby):
					var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
					if colossus_btn:
						colossus_btn.emit_signal("pressed")
			elif _wait >= 25:
				var path := "%s/proof_10_zh_sortie_regression.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [10/12] 出征分頁停擺巨偶舊功能回歸截圖完成: %s" % path)
				_step = 11
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 11. 舊功能回歸檢核：發條衣櫥換裝
		# ──────────────────────────────────────────────────────────
		11:
			if _wait == 1:
				if is_instance_valid(_lobby):
					if _lobby.has_method("open_wardrobe"):
						_lobby.call("open_wardrobe")
			elif _wait >= 25:
				var path := "%s/proof_11_zh_wardrobe_regression.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [11/12] 衣櫥換裝舊功能回歸截圖完成: %s" % path)
				if is_instance_valid(_lobby):
					var wd = _lobby.find_child("WardrobeDialog", true, false)
					if wd:
						wd.queue_free()
					_lobby.queue_free()
					_lobby = null
				_step = 12
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 12. 英文 (en) 鐵匠校準日誌色階名「藍」巡檢存證（記帳不修）
		# ──────────────────────────────────────────────────────────
		12:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
				if ForgeDialogClass:
					_forge_dlg = ForgeDialogClass.new()
					root.add_child(_forge_dlg)
			elif _wait == 10:
				if is_instance_valid(_forge_dlg):
					_forge_dlg.set("_last_calibrate_state", {
						"slot_name": "發條發電機",
						"tip": "Jump 1 Tier Succeeded",
						"tip_key": "CALIBRATE_JUMP_1",
						"tier_name": "藍",
						"rem": 4,
						"ok": true
					})
					if _forge_dlg.has_method("_update_calibrate_message"):
						_forge_dlg.call("_update_calibrate_message")
			elif _wait >= 25:
				var path := "%s/proof_12_en_forge_calibration_log.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [12/12] 鐵匠英文校準日誌「藍」色階巡檢截圖完成: %s" % path)
				if is_instance_valid(_forge_dlg):
					_forge_dlg.queue_free()
					_forge_dlg = null

				# 恢復繁中
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數 12 張探索性 QA 實機截圖完成 ──")
				quit(0)
				return true

	return false
