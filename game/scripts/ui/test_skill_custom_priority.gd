extends SceneTree
## SkillDialog 招式卡片自選首發出招與戰鬥連動單元測試 (test_skill_custom_priority.gd)
## 驗收規範：
## 1. SkillDialog 招式卡片提供『設為首發』按鈕，點擊後調用 SkillSystem 記錄偏好首發招式。
## 2. pick_battle_skill 優先回傳玩家偏好首發招式（即使其 CATALOG priority 小於其他已習得技能）。
## 3. 點擊切換『平常首發』膠囊標籤，頂部戰鬥優先出招摘要與卡片狀態同步連動。
## 4. 跨存檔保存：GameState.to_dict / from_dict 正確持久化 preferred_skills 映射。
## 5. 木人樁與實戰首發連動：在 full HP ratio 下挑選戰鬥技能確實首發該招式。
## 6. 六語系支援：zh_TW, zh_CN, en, ja, ko, es 翻譯齊全且即時生效。
## 7. 全程 0 SCRIPT ERROR，無系統 Emoji，退出碼 0。

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
					print("SKILL_CUSTOM_PRIORITY_OK")
					quit(0)
				else:
					push_error("SKILL_CUSTOM_PRIORITY_FAIL")
					print("SKILL_CUSTOM_PRIORITY_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_skill_custom_priority 測試 ===")

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

	# -------------------------------------------------------------
	# 準備狀態：劍流派，同時習得 slash (prio 10) 與 counter_strike (prio 22)
	# -------------------------------------------------------------
	gs.skill_data = {
		"slash": {"lv": 1, "mastery": 0},
		"counter_strike": {"lv": 1, "mastery": 0}
	}
	gs.preferred_skills = {}

	# -------------------------------------------------------------
	# 1. 驗證自然預設狀態：無偏好時 counter_strike (prio 22) 為首發
	# -------------------------------------------------------------
	print("\n--- 1. 驗證初始無偏好時自然優先出招 ---")
	var kit_init: Dictionary = sk_node.call("pick_battle_skill", 1.0, "sword")
	if kit_init.get("id", "") != "counter_strike":
		_fail("自然預設首發招式應為 counter_strike，實際為: %s" % kit_init.get("id", ""))
	else:
		print("  ✓ 自然優先出招正確: counter_strike (prio 22)")

	var dlg: Control = SkillDialogScn.new()
	root_node.add_child(dlg)

	var cs_badge: Control = dlg.call("get_skill_priority_badge", "counter_strike")
	if cs_badge == null:
		_fail("counter_strike 卡片應帶有 PriorityBadge (平常首發)")
	else:
		print("  ✓ counter_strike 帶有平常首發標籤")

	var slash_badge_init: Control = dlg.call("get_skill_priority_badge", "slash")
	if slash_badge_init != null:
		_fail("初始狀態 slash 不應帶有 PriorityBadge")
	else:
		print("  ✓ slash 初始無平常首發標籤")

	var slash_btn_text: String = dlg.call("get_skill_preferred_btn_text", "slash")
	if slash_btn_text != "設為首發":
		_fail("slash 按鈕文字應為 '設為首發'，實際為: '%s'" % slash_btn_text)
	else:
		print("  ✓ slash 操作按鈕文字正確: 設為首發")

	var cs_btn_text: String = dlg.call("get_skill_preferred_btn_text", "counter_strike")
	if cs_btn_text != "已設首發":
		_fail("counter_strike 當前為首發，按鈕文字應為 '已設首發'，實際為: '%s'" % cs_btn_text)
	else:
		print("  ✓ counter_strike 按鈕文字正確: 已設首發")

	# -------------------------------------------------------------
	# 2. 驗證點擊『設為首發』將 slash 設為首發
	# -------------------------------------------------------------
	print("\n--- 2. 驗證點擊『設為首發』自選 slash 並刷新標籤 ---")
	var slash_pref_btn: Button = dlg.call("get_skill_preferred_btn", "slash")
	if slash_pref_btn == null:
		_fail("找不到 slash 的 BtnSetPreferred 按鈕")
	else:
		slash_pref_btn.emit_signal("pressed")

	# 驗證 SkillSystem 偏好與 GameState 存檔記錄
	var pref_cur: String = sk_node.call("get_preferred_skill", "sword")
	if pref_cur != "slash":
		_fail("SkillSystem.get_preferred_skill('sword') 應為 'slash'，實際為: '%s'" % pref_cur)
	else:
		print("  ✓ SkillSystem 成功記錄偏好首發招式: slash")

	if gs.preferred_skills.get("sword", "") != "slash":
		_fail("GameState.preferred_skills['sword'] 應記錄 'slash'")
	else:
		print("  ✓ GameState.preferred_skills 持久化記錄: sword -> slash")

	# 驗證 pick_battle_skill 優先回傳 slash
	var kit_custom: Dictionary = sk_node.call("pick_battle_skill", 1.0, "sword")
	if kit_custom.get("id", "") != "slash":
		_fail("自選後 pick_battle_skill 應優先回傳 slash，實際為: %s" % kit_custom.get("id", ""))
	else:
		print("  ✓ pick_battle_skill 優先回傳自選招式: slash (成功超越 counter_strike)")

	# 驗證 UI 膠囊標籤切換
	var slash_badge_after: Control = dlg.call("get_skill_priority_badge", "slash")
	if slash_badge_after == null:
		_fail("自選後 slash 應獲得 PriorityBadge (平常首發)")
	else:
		print("  ✓ slash 成功獲得【平常首發】膠囊標籤")

	var cs_badge_after: Control = dlg.call("get_skill_priority_badge", "counter_strike")
	if cs_badge_after != null:
		_fail("自選後 counter_strike 應卸載 PriorityBadge")
	else:
		print("  ✓ counter_strike 已卸載 PriorityBadge")

	# 驗證按鈕狀態反轉
	if dlg.call("get_skill_preferred_btn_text", "slash") != "已設首發":
		_fail("slash 按鈕應轉為 '已設首發'")
	else:
		print("  ✓ slash 按鈕切換為: 已設首發")

	if dlg.call("get_skill_preferred_btn_text", "counter_strike") != "設為首發":
		_fail("counter_strike 按鈕應轉為 '設為首發'")
	else:
		print("  ✓ counter_strike 按鈕切換為: 設為首發")

	# 頂部戰鬥出招摘要同步更新為「橫斬」
	var prio_norm_txt: String = dlg.call("get_prio_normal_text")
	if not prio_norm_txt.contains("橫斬"):
		_fail("頂部出招摘要應包含 '橫斬'，實際為: %s" % prio_norm_txt)
	else:
		print("  ✓ 頂部戰鬥優先摘要連動正確: %s" % prio_norm_txt)

	# -------------------------------------------------------------
	# 3. 驗證切換為另一招式 (counter_strike)
	# -------------------------------------------------------------
	print("\n--- 3. 驗證點擊切換回 counter_strike ---")
	var cs_pref_btn: Button = dlg.call("get_skill_preferred_btn", "counter_strike")
	if cs_pref_btn == null:
		_fail("找不到 counter_strike 的 BtnSetPreferred 按鈕")
	else:
		cs_pref_btn.emit_signal("pressed")

	if sk_node.call("get_preferred_skill", "sword") != "counter_strike":
		_fail("切換後偏好招式應為 counter_strike")
	else:
		print("  ✓ 成功切換偏好首發招式為 counter_strike")

	var kit_cs: Dictionary = sk_node.call("pick_battle_skill", 1.0, "sword")
	if kit_cs.get("id", "") != "counter_strike":
		_fail("pick_battle_skill 應回傳 counter_strike")
	else:
		print("  ✓ pick_battle_skill 連動更新為 counter_strike")

	if dlg.call("get_skill_priority_badge", "counter_strike") == null:
		_fail("counter_strike 應帶有 PriorityBadge")
	else:
		print("  ✓ counter_strike 帶有 PriorityBadge")

	if dlg.call("get_skill_priority_badge", "slash") != null:
		_fail("slash 不應再帶有 PriorityBadge")
	else:
		print("  ✓ slash 已卸載 PriorityBadge")

	# -------------------------------------------------------------
	# 4. 驗證取消自選首發 (Toggle off / Clear)
	# -------------------------------------------------------------
	print("\n--- 4. 驗證點擊已設首發按鈕取消自選偏好 ---")
	var cs_btn_active: Button = dlg.call("get_skill_preferred_btn", "counter_strike")
	if cs_btn_active:
		cs_btn_active.emit_signal("pressed")

	if sk_node.call("get_preferred_skill", "sword") != "":
		_fail("點擊已設首發後應清除偏好，實際為: %s" % sk_node.call("get_preferred_skill", "sword"))
	else:
		print("  ✓ 成功清除自選偏好，恢復系統自然優先級")

	# -------------------------------------------------------------
	# 5. 驗證跨存檔保存 (GameState.to_dict / from_dict)
	# -------------------------------------------------------------
	print("\n--- 5. 驗證跨存檔保存 (to_dict / from_dict) ---")
	sk_node.call("set_preferred_skill", "slash", "sword")
	var save_dict: Dictionary = gs.call("to_dict")
	if not save_dict.has("preferred_skills"):
		_fail("GameState.to_dict 缺少 preferred_skills 欄位")
	elif save_dict["preferred_skills"].get("sword", "") != "slash":
		_fail("GameState.to_dict 的 preferred_skills 未正確保存 'sword': 'slash'")
	else:
		print("  ✓ GameState.to_dict 正確導出 preferred_skills: %s" % str(save_dict["preferred_skills"]))

	# 模擬載入存檔
	gs.preferred_skills = {}
	if sk_node.call("get_preferred_skill", "sword") != "":
		_fail("清空後偏好應為空")

	gs.call("from_dict", save_dict)
	if gs.preferred_skills.get("sword", "") != "slash":
		_fail("GameState.from_dict 未恢復 preferred_skills")
	else:
		print("  ✓ GameState.from_dict 成功恢復 preferred_skills")

	if sk_node.call("get_preferred_skill", "sword") != "slash":
		_fail("恢復存檔後 SkillSystem.get_preferred_skill 應為 'slash'")
	else:
		print("  ✓ SkillSystem 與載入存檔無縫連動: slash")

	# -------------------------------------------------------------
	# 6. 驗證六語系翻譯支援 (zh_TW, zh_CN, en, ja, ko, es)
	# -------------------------------------------------------------
	print("\n--- 6. 驗證六語系翻譯與即時刷新 ---")
	var expected_set := {
		"zh_TW": "設為首發",
		"zh_CN": "设为首发",
		"en": "Set as Opener",
		"ja": "初手に設定",
		"ko": "선발 설정",
		"es": "Fijar inicial"
	}
	var expected_active := {
		"zh_TW": "已設首發",
		"zh_CN": "已设首发",
		"en": "Opener Set",
		"ja": "初手設定済",
		"ko": "선발 지정됨",
		"es": "Inicial fijado"
	}

	for loc in LOCALES:
		loc_node.call("set_locale", loc)
		var t_set: String = ContentLoc.text("ui", "設為首發")
		var t_act: String = ContentLoc.text("ui", "已設首發")
		if t_set != expected_set[loc]:
			_fail("[%s] '設為首發' 翻譯不符: 期望 '%s'，實際 '%s'" % [loc, expected_set[loc], t_set])
		else:
			print("  ✓ [%s] '設為首發' -> %s" % [loc, t_set])
		if t_act != expected_active[loc]:
			_fail("[%s] '已設首發' 翻譯不符: 期望 '%s'，實際 '%s'" % [loc, expected_active[loc], t_act])
		else:
			print("  ✓ [%s] '已設首發' -> %s" % [loc, t_act])

	# 切回繁中
	loc_node.call("set_locale", "zh_TW")
	dlg.queue_free()
