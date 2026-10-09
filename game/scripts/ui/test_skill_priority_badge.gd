extends SceneTree
## SkillDialog 招式卡片出招優先膠囊標籤單元測試 (Skill Priority Badge Test)
## 驗證：
## 1. 實例化 SkillDialog 並產生卡片後，當前平常出招招式卡片帶有 PriorityBadge 節點，文案與顏色符合規範。
## 2. 當血量/優先權條件變更時，標籤與頂部摘要一致。
## 3. 切換語系 (ContentLoc / Loc.locale_changed) 時，標籤文案即時刷新（六語系支援），無文字穿框或重疊。
## 4. 退出 0 並印出 SKILL_PRIORITY_BADGE_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("SKILL_PRIORITY_BADGE_OK")
					quit(0)
				else:
					push_error("SKILL_PRIORITY_BADGE_FAIL")
					print("SKILL_PRIORITY_BADGE_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_skill_priority_badge 測試 ===")

	var root_node := root.get_node_or_null("Main")
	if root_node == null:
		_fail("找不到 Main 根節點")
		return

	var sk_node: Node = root.get_node_or_null("SkillSystem")
	if sk_node == null:
		_fail("找不到 SkillSystem autoload")
		return

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		_fail("找不到 GameState autoload")
		return

	loc_node.call("set_locale", "zh_TW")

	# 重設初始技能：騎士預設僅習得 slash
	gs.skill_data = {
		"slash": {"lv": 1, "mastery": 0}
	}

	# -------------------------------------------------------------
	# 1. 驗證初始狀態：slash 帶有金黃【平常首發】膠囊標籤
	# -------------------------------------------------------------
	print("\n--- 1. 驗證初始狀態下平常出招卡片帶有 PriorityBadge ---")
	var dlg: Control = SkillDialogScn.new()
	root_node.add_child(dlg)

	var slash_card: PanelContainer = dlg.call("get_skill_card", "slash")
	if slash_card == null:
		_fail("找不到 slash 技能卡片")
		dlg.queue_free()
		return

	var badge: Control = dlg.call("get_skill_priority_badge", "slash")
	if badge == null:
		badge = slash_card.find_child("PriorityBadge", true, false) as Control

	if badge == null:
		_fail("slash 卡片缺少 PriorityBadge 節點")
	else:
		print("  ✓ slash 卡片包含 PriorityBadge 節點: %s" % badge.name)

		# 驗證 StyleBoxFlat (12px 圓角、4px 內距、金黃柔和底 #FFF4D0)
		var sb: StyleBoxFlat = badge.get_theme_stylebox("panel") as StyleBoxFlat
		if sb == null:
			_fail("PriorityBadge 缺少 panel StyleBoxFlat")
		else:
			if sb.bg_color.to_html(false).to_upper() != "FFF4D0":
				_fail("平常首發底色不符: 期望 #FFF4D0，實際 #%s" % sb.bg_color.to_html(false))
			else:
				print("  ✓ 平常首發底色合規: #FFF4D0")

			if sb.get_corner_radius(CORNER_TOP_LEFT) != 12:
				_fail("平常首發圓角不符: 期望 12，實際 %d" % sb.get_corner_radius(CORNER_TOP_LEFT))
			else:
				print("  ✓ 膠囊圓角合規: 12px")

			if sb.content_margin_top != 4 or sb.content_margin_bottom != 4:
				_fail("平常首發上下內距不符: 期望 4px，實際 top=%d bottom=%d" % [sb.content_margin_top, sb.content_margin_bottom])
			else:
				print("  ✓ 膠囊上下內距合規: 4px")

		# 驗證 BadgeLabel (文字字級 13px 加粗、壓明度金黃字 #9A6B00、文案 '平常首發')
		var badge_lbl: Label = badge.find_child("BadgeLabel", true, false) as Label
		if badge_lbl == null:
			_fail("PriorityBadge 缺少 BadgeLabel 節點")
		else:
			if badge_lbl.text != "平常首發":
				_fail("平常首發標籤文案不符: 期望 '平常首發'，實際 '%s'" % badge_lbl.text)
			else:
				print("  ✓ 平常首發文案正確: 平常首發")

			var font_size: int = badge_lbl.get_theme_font_size("font_size")
			if font_size != 13:
				_fail("標籤字級不符: 期望 13px，實際 %dpx" % font_size)
			else:
				print("  ✓ 標籤字級合規: 13px 加粗")

			var font_col: Color = badge_lbl.get_theme_color("font_color")
			if font_col.to_html(false).to_upper() != "9A6B00":
				_fail("平常首發字色不符: 期望 #9A6B00，實際 #%s" % font_col.to_html(false))
			else:
				print("  ✓ 平常首發字色合規: #9A6B00")

	# 驗證未被選中的招式卡片（如 counter_strike）無 PriorityBadge
	var cs_badge: Control = dlg.call("get_skill_priority_badge", "counter_strike")
	if cs_badge != null:
		_fail("未被選中出招之 counter_strike 不應帶有 PriorityBadge")
	else:
		print("  ✓ 非優先出招 counter_strike 無 PriorityBadge")

	# 驗證頂部戰鬥優先摘要與標籤一致
	var prio_normal_txt: String = dlg.call("get_prio_normal_text")
	if not prio_normal_txt.contains("橫斬"):
		_fail("頂部摘要平常出招未包含 '橫斬': %s" % prio_normal_txt)
	else:
		print("  ✓ 頂部摘要連動一致: %s" % prio_normal_txt)

	# -------------------------------------------------------------
	# 2. 驗證條件變更：習得危急治療技能 (emergency_heal)
	# -------------------------------------------------------------
	print("\n--- 2. 驗證血量/危急治療條件變更時的標籤與頂部連動 ---")
	sk_node.call("_set_lv", "emergency_heal", 1)
	dlg.call("_refresh_display")

	var heal_badge: Control = dlg.call("get_skill_priority_badge", "emergency_heal")
	if heal_badge == null:
		var heal_card: PanelContainer = dlg.call("get_skill_card", "emergency_heal")
		if heal_card:
			heal_badge = heal_card.find_child("PriorityBadge", true, false) as Control

	if heal_badge == null:
		_fail("習得危急技能後 emergency_heal 卡片缺少 PriorityBadge")
	else:
		print("  ✓ emergency_heal 卡片成功掛載 PriorityBadge")

		# 驗證 StyleBoxFlat (天藍柔和底 #F0F7FF, 12px 圓角, 4px 內距)
		var sb_heal: StyleBoxFlat = heal_badge.get_theme_stylebox("panel") as StyleBoxFlat
		if sb_heal == null:
			_fail("危急標籤缺少 panel StyleBoxFlat")
		else:
			if sb_heal.bg_color.to_html(false).to_upper() != "F0F7FF":
				_fail("危急應急底色不符: 期望 #F0F7FF，實際 #%s" % sb_heal.bg_color.to_html(false))
			else:
				print("  ✓ 危急應急底色合規: #F0F7FF")

			if sb_heal.get_corner_radius(CORNER_TOP_LEFT) != 12:
				_fail("危急應急圓角不符: 期望 12，實際 %d" % sb_heal.get_corner_radius(CORNER_TOP_LEFT))
			else:
				print("  ✓ 危急應急圓角合規: 12px")

		var heal_lbl: Label = heal_badge.find_child("BadgeLabel", true, false) as Label
		if heal_lbl == null:
			_fail("危急標籤缺少 BadgeLabel 節點")
		else:
			if heal_lbl.text != "危急應急":
				_fail("危急應急標籤文案不符: 期望 '危急應急'，實際 '%s'" % heal_lbl.text)
			else:
				print("  ✓ 危急應急文案正確: 危急應急")

			var font_col_heal: Color = heal_lbl.get_theme_color("font_color")
			if font_col_heal.to_html(false).to_upper() != "38A0FF":
				_fail("危急應急字色不符: 期望 #38A0FF，實際 #%s" % font_col_heal.to_html(false))
			else:
				print("  ✓ 危急應急字色合規: #38A0FF")

	var prio_panic_txt: String = dlg.call("get_prio_panic_text")
	if not prio_panic_txt.contains("緊急恢復"):
		_fail("頂部摘要危急治療未包含 '緊急恢復': %s" % prio_panic_txt)
	else:
		print("  ✓ 頂部危急摘要連動一致: %s" % prio_panic_txt)

	# -------------------------------------------------------------
	# 3. 驗證優先權切換：習得更高優先級攻擊招式 (counter_strike)
	# -------------------------------------------------------------
	print("\n--- 3. 驗證攻擊招式優先權轉移時標籤動態切換 ---")
	# counter_strike priority 22 > slash priority 10
	sk_node.call("_set_lv", "counter_strike", 1)
	dlg.call("_refresh_display")

	# 現在 counter_strike 應為平常首發
	var cs_new_badge: Control = dlg.call("get_skill_priority_badge", "counter_strike")
	if cs_new_badge == null:
		_fail("更高優先級招式 counter_strike 缺少 PriorityBadge")
	else:
		var cs_text: String = dlg.call("get_skill_priority_badge_text", "counter_strike")
		if cs_text != "平常首發":
			_fail("counter_strike 標籤文案應為 '平常首發'，實際 '%s'" % cs_text)
		else:
			print("  ✓ counter_strike 成功獲得【平常首發】標籤")

	# 原 slash 標籤應被卸載
	var slash_old_badge: Control = dlg.call("get_skill_priority_badge", "slash")
	if slash_old_badge != null:
		_fail("優先權轉移後原招式 slash 不應再保留 PriorityBadge")
	else:
		print("  ✓ 原招式 slash 已正確移除 PriorityBadge")

	var prio_normal_txt_updated: String = dlg.call("get_prio_normal_text")
	if not prio_normal_txt_updated.contains("反戈一擊"):
		_fail("頂部摘要平常出招未更新為 '反戈一擊': %s" % prio_normal_txt_updated)
	else:
		print("  ✓ 頂部摘要連動更新: %s" % prio_normal_txt_updated)

	# -------------------------------------------------------------
	# 4. 驗證六語系切換時標籤文案即時刷新 (ContentLoc / Loc.locale_changed)
	# -------------------------------------------------------------
	print("\n--- 4. 驗證六語系切換 (locale_changed) 標籤即時刷新 ---")
	var expected_badges := {
		"zh_TW": {"normal": "平常首發", "panic": "危急應急"},
		"zh_CN": {"normal": "平时首发", "panic": "危急应急"},
		"en":    {"normal": "Normal Opener", "panic": "Crisis Emergency"},
		"ja":    {"normal": "通常初手", "panic": "緊急応急"},
		"ko":    {"normal": "통상 선공", "panic": "위급 대처"},
		"es":    {"normal": "Apertura normal", "panic": "Respuesta de crisis"},
	}

	for loc in LOCALES:
		loc_node.call("set_locale", loc)
		var exp_norm: String = expected_badges[loc]["normal"]
		var exp_panic: String = expected_badges[loc]["panic"]

		var cur_norm: String = dlg.call("get_skill_priority_badge_text", "counter_strike")
		var cur_panic: String = dlg.call("get_skill_priority_badge_text", "emergency_heal")

		if cur_norm != exp_norm:
			_fail("[%s] 平常首發標籤未刷新: 期望 '%s'，實際 '%s'" % [loc, exp_norm, cur_norm])
		else:
			print("  ✓ [%s] 平常首發標籤即時刷新: %s" % [loc, cur_norm])

		if cur_panic != exp_panic:
			_fail("[%s] 危急應急標籤未刷新: 期望 '%s'，實際 '%s'" % [loc, exp_panic, cur_panic])
		else:
			print("  ✓ [%s] 危急應急標籤即時刷新: %s" % [loc, cur_panic])

	# 恢復繁中
	loc_node.call("set_locale", "zh_TW")
	dlg.queue_free()

