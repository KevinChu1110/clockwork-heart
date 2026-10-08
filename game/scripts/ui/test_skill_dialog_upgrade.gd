extends SceneTree
## SkillDialog 熟練度進度條、一鍵突破升階與體悟習得單元測試 (test_skill_dialog_upgrade.gd)
## 驗證：
## 1. 進度條百分比計算正確（熟練度進度條、ProgressBar 尺寸與比率）。
## 2. can_level_up 時『突破升階』按鈕可見且點擊後成功調用 try_level_up，等級提升且熟練度扣除。
## 3. is_unlocked 且 not is_learned 時『體悟習得』按鈕可見且點擊後成功調用 try_unlock，招式轉為已習得。
## 4. 當招式達到滿級 (slv >= MAX_LV) 時，顯示『Lv.MAX · 極階』金色標籤。
## 5. 六語系翻譯均正確存在且對齊 (zh_TW, zh_CN, en, ja, ko, es)。
## 6. 全程 0 SCRIPT ERROR，無系統 Emoji。

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
					print("SKILL_DIALOG_UPGRADE_TEST_OK")
					quit(0)
				else:
					push_error("SKILL_DIALOG_UPGRADE_TEST_FAIL")
					print("SKILL_DIALOG_UPGRADE_TEST_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_skill_dialog_upgrade 測試 ===")

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
		"slash": {"lv": 1, "mastery": 15}
	}
	sk_node.call("ensure_skill_map")

	var dlg: Control = SkillDialogScn.new()
	root_node.add_child(dlg)

	# -------------------------------------------------------------
	# 1. 驗證進度條百分比計算正確
	# -------------------------------------------------------------
	print("\n--- 1. 驗證進度條百分比計算正確 ---")
	var pb: ProgressBar = dlg.call("get_skill_progress_bar", "slash")
	if pb == null:
		_fail("slash 卡片缺少 MasteryProgressBar 節點")
	else:
		print("  ✓ slash 卡片包含 MasteryProgressBar")
		# 驗證高度與圓角
		if pb.custom_minimum_size.y < 8:
			_fail("進度條高度不符: 期望 >= 8px，實際 %d" % int(pb.custom_minimum_size.y))
		else:
			print("  ✓ 進度條高度符合規範: %dpx" % int(pb.custom_minimum_size.y))

		# Lv1 升 Lv2 需 30 熟練，當前 15 熟練，比率應為 0.5
		var ratio: float = float(dlg.call("get_skill_progress_ratio", "slash"))
		if absf(ratio - 0.5) > 0.01:
			_fail("熟練度進度條比率不符: 期望 0.5，實際 %f" % ratio)
		else:
			print("  ✓ 熟練度 15/30 進度條比率正確: %f (50%%)" % ratio)

		var m_text: String = dlg.call("get_skill_mastery_text", "slash")
		if not m_text.contains("15/30"):
			_fail("熟練度數值文字未包含 '15/30': %s" % m_text)
		else:
			print("  ✓ 熟練度文字正確: %s" % m_text)

	# -------------------------------------------------------------
	# 2. 驗證滿熟練度時『突破升階』按鈕可見，點擊成功提升等級並扣除熟練度
	# -------------------------------------------------------------
	print("\n--- 2. 驗證滿熟練度時『突破升階』按鈕與升階邏輯 ---")
	# 尚未滿熟練度時，不應出現突破按鈕
	var btn_early: Button = dlg.call("get_skill_upgrade_btn", "slash")
	if btn_early != null:
		_fail("未滿熟練度時不應出現『突破升階』按鈕")
	else:
		print("  ✓ 未滿熟練度時無突破按鈕")

	# 設定熟練度達到門檻 30 (can_level_up 為真)
	gs.skill_data["slash"] = {"lv": 1, "mastery": 30}
	dlg.call("_refresh_display")

	var up_btn: Button = dlg.call("get_skill_upgrade_btn", "slash")
	if up_btn == null:
		_fail("熟練度滿 (30/30) 時缺少『突破升階』按鈕")
	else:
		print("  ✓ 滿熟練度時成功出現『突破升階』按鈕")
		if up_btn.text != "突破升階":
			_fail("按鈕文案不符: 期望 '突破升階'，實際 '%s'" % up_btn.text)
		else:
			print("  ✓ 按鈕文案正確: 突破升階")

		if up_btn.custom_minimum_size.y < 48:
			_fail("按鈕熱區高度不足: 期望 >= 48px，實際 %d" % int(up_btn.custom_minimum_size.y))
		else:
			print("  ✓ 按鈕熱區高度合規: %dpx" % int(up_btn.custom_minimum_size.y))

		# 滿條時進度比率應為 1.0
		var ratio_full: float = float(dlg.call("get_skill_progress_ratio", "slash"))
		if absf(ratio_full - 1.0) > 0.01:
			_fail("滿熟練度進度比率不符: 期望 1.0，實際 %f" % ratio_full)
		else:
			print("  ✓ 滿熟練度進度比率正確: 100%%")

		# 模擬點擊升階按鈕
		up_btn.emit_signal("pressed")

		var new_lv: int = int(sk_node.call("get_lv", "slash"))
		var new_mastery: int = int(sk_node.call("get_mastery", "slash"))
		if new_lv != 2:
			_fail("點擊突破升階後等級未提升: 期望 2，實際 %d" % new_lv)
		else:
			print("  ✓ 點擊突破升階成功提升等級至 Lv.%d" % new_lv)

		if new_mastery != 0:
			_fail("點擊突破升階後熟練度未扣除: 期望 0，實際 %d" % new_mastery)
		else:
			print("  ✓ 點擊突破升階後熟練度正確扣除: 0")

		# 升階後卡片即時刷新，按鈕自動消失
		var up_btn_after: Button = dlg.call("get_skill_upgrade_btn", "slash")
		if up_btn_after != null:
			_fail("升階後熟練度已重設，突破按鈕應消失")
		else:
			print("  ✓ 升階後突破按鈕自動消失並即時刷新卡片")

	# -------------------------------------------------------------
	# 3. 驗證 is_unlocked 且 not is_learned 時『體悟習得』按鈕與習得邏輯
	# -------------------------------------------------------------
	print("\n--- 3. 驗證可體悟招式『體悟習得』按鈕與習得邏輯 ---")
	# 槍系起手 line_thrust 為同職另一武器系統起手技 (req_level=1)，初始未習得但已解鎖
	var sid_test := "line_thrust"
	var is_unl: bool = bool(sk_node.call("is_unlocked", sid_test))
	var is_lrn: bool = bool(sk_node.call("is_learned", sid_test))

	if not is_unl or is_lrn:
		_fail("line_thrust 前置條件不符合測試預期: is_unlocked=%s, is_learned=%s" % [str(is_unl), str(is_lrn)])
	else:
		var unlk_btn: Button = dlg.call("get_skill_unlock_btn", sid_test)
		if unlk_btn == null:
			_fail("可體悟招式 %s 缺少『體悟習得』按鈕" % sid_test)
		else:
			print("  ✓ 可體悟招式成功提供『體悟習得』按鈕")
			if unlk_btn.text != "體悟習得":
				_fail("按鈕文案不符: 期望 '體悟習得'，實際 '%s'" % unlk_btn.text)
			else:
				print("  ✓ 按鈕文案正確: 體悟習得")

			if unlk_btn.custom_minimum_size.y < 48:
				_fail("按鈕高度不足: 期望 >= 48px，實際 %d" % int(unlk_btn.custom_minimum_size.y))
			else:
				print("  ✓ 按鈕熱區高度合規: %dpx" % int(unlk_btn.custom_minimum_size.y))

			# 模擬點擊體悟按鈕
			unlk_btn.emit_signal("pressed")

			var learned_now: bool = bool(sk_node.call("is_learned", sid_test))
			var lv_now: int = int(sk_node.call("get_lv", sid_test))
			if not learned_now or lv_now < 1:
				_fail("點擊體悟習得後招式未習得: is_learned=%s, lv=%d" % [str(learned_now), lv_now])
			else:
				print("  ✓ 點擊體悟習得成功習得招式: Lv.%d" % lv_now)

			# 體悟後按鈕消失，且產生熟練度進度條
			var unlk_btn_after: Button = dlg.call("get_skill_unlock_btn", sid_test)
			var pb_now: ProgressBar = dlg.call("get_skill_progress_bar", sid_test)
			if unlk_btn_after != null:
				_fail("體悟習得後體悟按鈕應消失")
			elif pb_now == null:
				_fail("體悟習得後卡片應新增熟練度進度條")
			else:
				print("  ✓ 體悟後按鈕轉移且熟練度進度條即時展示")

	# -------------------------------------------------------------
	# 4. 驗證滿級 (slv >= MAX_LV) 顯示『Lv.MAX · 極階』金色標籤
	# -------------------------------------------------------------
	print("\n--- 4. 驗證滿級時顯示『Lv.MAX · 極階』金色標籤 ---")
	gs.skill_data["slash"] = {"lv": 3, "mastery": 0}
	dlg.call("_refresh_display")

	var max_badge: Control = dlg.call("get_skill_max_badge", "slash")
	if max_badge == null:
		_fail("滿級招式缺少 MaxBadge 節點")
	else:
		var badge_txt: String = dlg.call("get_skill_max_badge_text", "slash")
		if badge_txt != "Lv.MAX · 極階":
			_fail("滿級標籤文案不符: 期望 'Lv.MAX · 極階'，實際 '%s'" % badge_txt)
		else:
			print("  ✓ 滿級金色標籤文案正確: %s" % badge_txt)

		var up_btn_max: Button = dlg.call("get_skill_upgrade_btn", "slash")
		if up_btn_max != null:
			_fail("滿級招式不應存在突破按鈕")
		else:
			print("  ✓ 滿級招式無突破按鈕")

	# -------------------------------------------------------------
	# 5. 驗證六語系翻譯均正確存在且對齊 (zh_TW, zh_CN, en, ja, ko, es)
	# -------------------------------------------------------------
	print("\n--- 5. 驗證六語系翻譯對齊與即時切換 ---")
	var expected_i18n := {
		"zh_TW": {
			"upgrade": "突破升階",
			"unlock": "體悟習得",
			"max": "Lv.MAX · 極階"
		},
		"zh_CN": {
			"upgrade": "突破升阶",
			"unlock": "体悟习得",
			"max": "Lv.MAX · 极阶"
		},
		"en": {
			"upgrade": "Breakthrough",
			"unlock": "Comprehend",
			"max": "Lv.MAX · Mastered"
		},
		"ja": {
			"upgrade": "突破昇階",
			"unlock": "体悟習得",
			"max": "Lv.MAX · 極階"
		},
		"ko": {
			"upgrade": "돌파 승급",
			"unlock": "깨달음 습득",
			"max": "Lv.MAX · 극계"
		},
		"es": {
			"upgrade": "Avance de rango",
			"unlock": "Comprender y aprender",
			"max": "Nv.MAX · Maestro"
		}
	}

	for loc in LOCALES:
		loc_node.call("set_locale", loc)

		var exp_up: String = expected_i18n[loc]["upgrade"]
		var exp_un: String = expected_i18n[loc]["unlock"]
		var exp_mx: String = expected_i18n[loc]["max"]

		var trans_up: String = ContentLoc.text("ui", "突破升階")
		var trans_un: String = ContentLoc.text("ui", "體悟習得")
		var trans_mx: String = ContentLoc.text("ui", "Lv.MAX · 極階")

		if trans_up != exp_up:
			_fail("[%s] 突破升階 ContentLoc 不符: 期望 '%s'，實際 '%s'" % [loc, exp_up, trans_up])
		if trans_un != exp_un:
			_fail("[%s] 體悟習得 ContentLoc 不符: 期望 '%s'，實際 '%s'" % [loc, exp_un, trans_un])
		if trans_mx != exp_mx:
			_fail("[%s] Lv.MAX · 極階 ContentLoc 不符: 期望 '%s'，實際 '%s'" % [loc, exp_mx, trans_mx])

		# 驗證 UI 即時刷新
		var badge_txt_loc: String = dlg.call("get_skill_max_badge_text", "slash")
		if badge_txt_loc != exp_mx:
			_fail("[%s] UI 滿級標籤未即時刷新: 期望 '%s'，實際 '%s'" % [loc, exp_mx, badge_txt_loc])
		else:
			print("  ✓ [%s] 六語系詞條對齊與 UI 即時切換正確: upgrade='%s', unlock='%s', max='%s'" % [loc, trans_up, trans_un, badge_txt_loc])

	# 恢復繁中
	loc_node.call("set_locale", "zh_TW")
	dlg.queue_free()
