extends SceneTree
## 《發條之心》戰敗結算戰力診斷卡與前往整頓按鈕單元測試 (test_battle_defeat_diagnostic.gd)
##
## 驗證：
## 1. UI 結構：DefeatCard 內含 DiagnosticCard、DiagnosticTitleLbl 與 DiagnosticCapsules
## 2. 戰力建議膠囊：包含武器階數、裝備副詞條、招式調整三大膠囊
## 3. 按鈕規範：BtnGearUp（前往整頓）立體果凍厚底按鈕（高度 >= 50px，底邊 >= 5px）
## 4. 信號觸發：點擊後觸發 gear_up_requested 信號、呼叫回調並關閉彈窗
## 5. 六語系支援：zh_TW/zh_CN/en/ja/ko/es 開窗即時切換動態刷新
## 6. 規範檢核：en, es 語系零 CJK 殘留；全語系零系統 emoji；符合多巴胺色盤與 review.md

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const BattleDefeatDialogClass := preload("res://scripts/battle/battle_defeat_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_BATTLE_DEFEAT_DIAGNOSTIC_OK")
					quit(0)
				else:
					push_error("TEST_BATTLE_DEFEAT_DIAGNOSTIC_FAIL")
					print("TEST_BATTLE_DEFEAT_DIAGNOSTIC_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_battle_defeat_diagnostic 測試 ===")

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass: GDScript = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass: GDScript = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es: Node = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass: GDScript = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc_node == null or gs == null or es == null:
		_fail("Autoload 節點初始化失敗")
		return

	# -------------------------------------------------------------
	# 1. 驗證 UI 結構與節點名稱
	# -------------------------------------------------------------
	print("\n--- 1. 驗證 UI 結構與 DiagnosticCard / BtnGearUp 存在性 ---")
	var dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(dlg)

	var card_node: PanelContainer = dlg.find_child("DefeatCard", true, false) as PanelContainer
	if card_node == null:
		_fail("找不到 DefeatCard 容器")
		dlg.queue_free()
		return

	if card_node.custom_minimum_size.x < 740 or card_node.custom_minimum_size.x > 760:
		_fail("卡片寬度不符橫屏手遊規範 (740~760): %f" % card_node.custom_minimum_size.x)
	else:
		print("  ✓ DefeatCard 寬度符合規範: %f" % card_node.custom_minimum_size.x)

	var diag_card: PanelContainer = dlg.find_child("DiagnosticCard", true, false) as PanelContainer
	if diag_card == null:
		_fail("找不到 DiagnosticCard 戰力診斷卡容器")
	else:
		print("  ✓ 找到 DiagnosticCard 戰力診斷卡容器")

	var diag_title: Label = dlg.find_child("DiagnosticTitleLbl", true, false) as Label
	if diag_title == null:
		_fail("找不到 DiagnosticTitleLbl 標題")
	else:
		print("  ✓ 找到 DiagnosticTitleLbl 標題: '%s'" % diag_title.text)

	var cap_weapon: PanelContainer = dlg.find_child("DiagnosticCapsule_Weapon", true, false) as PanelContainer
	var cap_affix: PanelContainer = dlg.find_child("DiagnosticCapsule_Affix", true, false) as PanelContainer
	var cap_skill: PanelContainer = dlg.find_child("DiagnosticCapsule_Skill", true, false) as PanelContainer

	if cap_weapon == null or cap_affix == null or cap_skill == null:
		_fail("戰力建議膠囊節點缺失 (Weapon: %s, Affix: %s, Skill: %s)" % [
			str(cap_weapon != null), str(cap_affix != null), str(cap_skill != null)
		])
	else:
		print("  ✓ 找到武器階數、裝備副詞條、招式調整三大建議膠囊")

	# 檢查膠囊子元素
	var w_tag: Label = dlg.find_child("WeaponTagLbl", true, false) as Label
	var w_desc: Label = dlg.find_child("WeaponDescLbl", true, false) as Label
	var a_tag: Label = dlg.find_child("AffixTagLbl", true, false) as Label
	var a_desc: Label = dlg.find_child("AffixDescLbl", true, false) as Label
	var s_tag: Label = dlg.find_child("SkillTagLbl", true, false) as Label
	var s_desc: Label = dlg.find_child("SkillDescLbl", true, false) as Label

	if w_tag == null or w_desc == null or a_tag == null or a_desc == null or s_tag == null or s_desc == null:
		_fail("膠囊標籤與說明 Label 查找失敗")
	else:
		print("  ✓ 膠囊標籤與說明節點齊全: [%s: %s] | [%s: %s] | [%s: %s]" % [
			w_tag.text, w_desc.text, a_tag.text, a_desc.text, s_tag.text, s_desc.text
		])

	# -------------------------------------------------------------
	# 2. 驗證按鈕尺寸與底邊厚度 (立體果凍厚底按鈕)
	# -------------------------------------------------------------
	print("\n--- 2. 驗證 BtnGearUp 按鈕尺寸與立體果凍厚底 (高 >= 50, 底邊 >= 5) ---")
	var gear_up_btn: Button = dlg.find_child("BtnGearUp", true, false) as Button
	if gear_up_btn == null:
		_fail("找不到 BtnGearUp 按鈕")
		dlg.queue_free()
		return

	if gear_up_btn.custom_minimum_size.y < 50:
		_fail("BtnGearUp 按鈕高度未達 50px: %f" % gear_up_btn.custom_minimum_size.y)
	else:
		print("  ✓ BtnGearUp 按鈕高度符合手遊人體工學規範: %f (>= 50px)" % gear_up_btn.custom_minimum_size.y)

	var sb_normal: StyleBoxFlat = gear_up_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb_normal == null:
		_fail("BtnGearUp 未設定 normal StyleBoxFlat")
	else:
		if sb_normal.border_width_bottom < 5:
			_fail("BtnGearUp 底邊厚度未達 5px: %d" % sb_normal.border_width_bottom)
		else:
			print("  ✓ BtnGearUp 立體果凍厚底底邊厚度符合規範: %d (>= 5px)" % sb_normal.border_width_bottom)

	dlg.queue_free()

	# -------------------------------------------------------------
	# 3. 驗證信號與點擊觸發 (gear_up_requested)
	# -------------------------------------------------------------
	print("\n--- 3. 驗證點擊 BtnGearUp 發出 gear_up_requested 信號 ---")
	var events := {
		"signal_emitted": false,
		"callback_called": false
	}

	var test_dlg: Control = BattleDefeatDialogClass.new()
	test_dlg.setup(
		Callable(),
		Callable(),
		"",
		"",
		func(): events["callback_called"] = true
	)
	root.add_child(test_dlg)

	test_dlg.gear_up_requested.connect(func(): events["signal_emitted"] = true)
	var test_btn: Button = test_dlg.find_child("BtnGearUp", true, false) as Button
	if test_btn:
		test_btn.pressed.emit()
	else:
		_fail("test_dlg 找不到 BtnGearUp")

	if not events["signal_emitted"]:
		_fail("點擊 BtnGearUp 未發出 gear_up_requested 信號")
	else:
		print("  ✓ 成功收到 gear_up_requested 信號")

	if not events["callback_called"]:
		_fail("點擊 BtnGearUp 未執行 setup 傳入之 on_gear_up 回調")
	else:
		print("  ✓ 成功執行 on_gear_up 回調")

	if not test_dlg.is_queued_for_deletion():
		_fail("點擊 BtnGearUp 後彈窗未執行 queue_free")
	else:
		print("  ✓ 點擊 BtnGearUp 後彈窗正常關閉 (queue_free)")

	# -------------------------------------------------------------
	# 4. 驗證六語系即時切換與零 CJK 殘留
	# -------------------------------------------------------------
	print("\n--- 4. 驗證六語系 (zh_TW/zh_CN/en/ja/ko/es) 即時動態切換 ---")

	var expected_diag_title := {
		"zh_TW": "戰力診斷",
		"zh_CN": "战力诊断",
		"en": "Combat Diagnostics",
		"ja": "戦力診断",
		"ko": "전투력 진단",
		"es": "Diagnóstico de combate",
	}

	var expected_gear_up := {
		"zh_TW": "前往整頓",
		"zh_CN": "前往整顿",
		"en": "Gear Up",
		"ja": "装備強化へ",
		"ko": "정비하러 가기",
		"es": "Equiparse",
	}

	var expected_weapon_tag := {
		"zh_TW": "武器階數",
		"zh_CN": "武器阶数",
		"en": "Weapon Tier",
		"ja": "武器ランク",
		"ko": "무기 등급",
		"es": "Rango de arma",
	}

	var expected_weapon_desc := {
		"zh_TW": "天宮鐵匠鍛造強化",
		"zh_CN": "天宫铁匠锻造强化",
		"en": "Forge at Celestial Smith",
		"ja": "天宮の鍛冶屋で強化",
		"ko": "천궁 대장간에서 강화",
		"es": "Forjar en la Forja Celestial",
	}

	var expected_affix_tag := {
		"zh_TW": "裝備副詞條",
		"zh_CN": "装备副词条",
		"en": "Gear Affixes",
		"ja": "装備サブステ",
		"ko": "장비 보조옵션",
		"es": "Subatributos de equipo",
	}

	var expected_affix_desc := {
		"zh_TW": "調整機芯優化屬性",
		"zh_CN": "调整机芯优化属性",
		"en": "Tune Cores & Attributes",
		"ja": "コアを調整し属性強化",
		"ko": "코어 조정 및 속성 최적화",
		"es": "Ajustar núcleos y atributos",
	}

	var expected_skill_tag := {
		"zh_TW": "招式調整",
		"zh_CN": "招式调整",
		"en": "Skill Setup",
		"ja": "技の調整",
		"ko": "기술 조정",
		"es": "Ajuste de técnicas",
	}

	var expected_skill_desc := {
		"zh_TW": "武術館自訂招式順序",
		"zh_CN": "武术馆自订招式顺序",
		"en": "Set Priority at Dojo",
		"ja": "武術館で技順を設定",
		"ko": "무술관에서 기술 순서 조정",
		"es": "Ajustar orden en el dojo",
	}

	var live_dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(live_dlg)

	var l_title: Label = live_dlg.find_child("DiagnosticTitleLbl", true, false) as Label
	var l_btn: Button = live_dlg.find_child("BtnGearUp", true, false) as Button
	var l_w_tag: Label = live_dlg.find_child("WeaponTagLbl", true, false) as Label
	var l_w_desc: Label = live_dlg.find_child("WeaponDescLbl", true, false) as Label
	var l_a_tag: Label = live_dlg.find_child("AffixTagLbl", true, false) as Label
	var l_a_desc: Label = live_dlg.find_child("AffixDescLbl", true, false) as Label
	var l_s_tag: Label = live_dlg.find_child("SkillTagLbl", true, false) as Label
	var l_s_desc: Label = live_dlg.find_child("SkillDescLbl", true, false) as Label

	for code in LOCALES:
		loc_node.call("set_locale", code)

		var exp_title: String = expected_diag_title[code]
		var exp_btn: String = expected_gear_up[code]
		var exp_wt: String = expected_weapon_tag[code]
		var exp_wd: String = expected_weapon_desc[code]
		var exp_at: String = expected_affix_tag[code]
		var exp_ad: String = expected_affix_desc[code]
		var exp_st: String = expected_skill_tag[code]
		var exp_sd: String = expected_skill_desc[code]

		if l_title.text != exp_title:
			_fail("[%s] 戰力診斷標題未即時更新: 實際 '%s'，期望 '%s'" % [code, l_title.text, exp_title])
		if l_btn.text != exp_btn:
			_fail("[%s] 前往整頓按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, l_btn.text, exp_btn])
		if l_w_tag.text != exp_wt or l_w_desc.text != exp_wd:
			_fail("[%s] 武器膠囊未即時更新: [%s, %s]" % [code, l_w_tag.text, l_w_desc.text])
		if l_a_tag.text != exp_at or l_a_desc.text != exp_ad:
			_fail("[%s] 副詞條膠囊未即時更新: [%s, %s]" % [code, l_a_tag.text, l_a_desc.text])
		if l_s_tag.text != exp_st or l_s_desc.text != exp_sd:
			_fail("[%s] 招式膠囊未即時更新: [%s, %s]" % [code, l_s_tag.text, l_s_desc.text])

		# CJK 檢核 (en, es 語系下不得有中文字元)
		if code in ["en", "es"]:
			if _has_cjk(l_title.text) or _has_cjk(l_btn.text) or _has_cjk(l_w_tag.text) or _has_cjk(l_w_desc.text) or _has_cjk(l_a_tag.text) or _has_cjk(l_a_desc.text) or _has_cjk(l_s_tag.text) or _has_cjk(l_s_desc.text):
				_fail("[%s] 戰力診斷卡存在 CJK 中文字元殘留！" % code)

		# 零系統 emoji 檢核
		if _has_emoji(l_title.text) or _has_emoji(l_btn.text) or _has_emoji(l_w_tag.text) or _has_emoji(l_w_desc.text) or _has_emoji(l_a_tag.text) or _has_emoji(l_a_desc.text) or _has_emoji(l_s_tag.text) or _has_emoji(l_s_desc.text):
			_fail("[%s] 戰力診斷卡存在 Emoji！" % code)

		print("  ✓ [%s] 六語系即時切換驗證成功: 標題='%s' | 按鈕='%s' | 膠囊=[%s, %s, %s]" % [
			code, l_title.text, l_btn.text, l_w_tag.text, l_a_tag.text, l_s_tag.text
		])

	# 清理並還原語系
	live_dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	gs.reset_new_game()
	print("  ✓ 測試清理與語系還原完成")
