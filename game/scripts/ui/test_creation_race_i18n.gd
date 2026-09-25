extends SceneTree
## 創角種族卡與欄位標題六語系單元測試 (Creation Race & Slots i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含所有 13 種族名稱、欄位標題、狀態列與按鈕翻譯。
## 2. 創角介面在六語系切換下，已在畫面上的種族按鈕、欄位標題與狀態列即時刷新。
## 3. 切換種族卡高亮時，種族卡文字不退回繁體中文。
## 4. 翠角鹿 (fawn) 因美術資源未齊保持隱藏，不露出空卡。

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("CREATION_RACE_I18N_OK")
			quit(0)
		else:
			push_error("CREATION_RACE_I18N_FAIL")
			print("CREATION_RACE_I18N_FAIL")
			quit(1)
		return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_creation_race_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證詞條字典解析
	var expected_races := {
		"白金兔": {
			"zh_TW": "白金兔", "zh_CN": "白金兔", "en": "Clockwork Rabbit",
			"ja": "白金兎", "ko": "백금토끼", "es": "Conejo de Platino"
		},
		"靈尾狐": {
			"zh_TW": "靈尾狐", "zh_CN": "灵尾狐", "en": "Astral Fox",
			"ja": "霊尾狐", "ko": "영미호", "es": "Zorro Astral"
		},
		"烈鬃獅": {
			"zh_TW": "烈鬃獅", "zh_CN": "烈鬃狮", "en": "Gilded Lion",
			"ja": "烈鬃獅子", "ko": "열기사자", "es": "León Dorado"
		},
		"鋼牙豕": {
			"zh_TW": "鋼牙豕", "zh_CN": "钢牙豕", "en": "Forge Boar",
			"ja": "鋼牙猪", "ko": "강아저", "es": "Jabalí de la Forja"
		},
		"靈爪猴": {
			"zh_TW": "靈爪猴", "zh_CN": "灵爪猴", "en": "Spring Macaque",
			"ja": "霊爪猿", "ko": "영조원", "es": "Mono Resorte"
		},
		"烈焰虎": {
			"zh_TW": "烈焰虎", "zh_CN": "烈焰虎", "en": "The Ember Tiger",
			"ja": "烈焔虎", "ko": "열염호", "es": "El Tigre de Fuego"
		},
		"雲嵐鶴": {
			"zh_TW": "雲嵐鶴", "zh_CN": "云岚鹤", "en": "The Cloud Crane",
			"ja": "雲嵐鶴", "ko": "운람학", "es": "La Grulla de las Nubes"
		},
		"玄軸熊": {
			"zh_TW": "玄軸熊", "zh_CN": "玄轴熊", "en": "The Iron Bear",
			"ja": "玄軸熊", "ko": "현축웅", "es": "El Oso de Hierro"
		},
		"蒸氣企鵝": {
			"zh_TW": "蒸氣企鵝", "zh_CN": "蒸气企鹅", "en": "The Steam Penguin",
			"ja": "蒸気ペンギン", "ko": "증기 펭귄", "es": "El Pingüino de Vapor"
		},
		"玄機龜": {
			"zh_TW": "玄機龜", "zh_CN": "玄机龟", "en": "The Xuanji Tortoise",
			"ja": "玄機龜", "ko": "현기귀", "es": "La Tortuga Xuanji"
		},
		"鋼岳象": {
			"zh_TW": "鋼岳象", "zh_CN": "钢岳象", "en": "The Colossus Elephant",
			"ja": "鋼岳象", "ko": "강악상", "es": "El Elefante Colosal"
		},
		"碧箸蛙": {
			"zh_TW": "碧箸蛙", "zh_CN": "碧箸蛙", "en": "The Spring-Leg Frog",
			"ja": "碧箸蛙", "ko": "벽저와", "es": "Rana de Resorte de Jade"
		},
		"瓷韻熊貓": {
			"zh_TW": "瓷韻熊貓", "zh_CN": "瓷韵熊猫", "en": "The Porcelain Panda",
			"ja": "磁韻パンダ", "ko": "도운 판다", "es": "Panda de Porcelana"
		},
	}

	var expected_costume_slot := {
		"zh_TW": "• 外裝服飾槽 (Costume Slot - Z:25)",
		"zh_CN": "• 外装服饰槽 (Costume Slot - Z:25)",
		"en": "• Costume Slot (Costume Slot - Z:25)",
		"ja": "• 衣装スロット (Costume Slot - Z:25)",
		"ko": "• 의상 슬롯 (Costume Slot - Z:25)",
		"es": "• Ranura de Atuendo (Costume Slot - Z:25)"
	}

	var expected_chassis_slot := {
		"zh_TW": "• 軀體塗裝槽 (Chassis Shell - Z:10)",
		"zh_CN": "• 躯体涂装槽 (Chassis Shell - Z:10)",
		"en": "• Chassis Shell Slot (Chassis Shell - Z:10)",
		"ja": "• 機体塗装スロット (Chassis Shell - Z:10)",
		"ko": "• 기체 도장 슬롯 (Chassis Shell - Z:10)",
		"es": "• Ranura de Pintura (Chassis Shell - Z:10)"
	}

	var expected_weapon_slot := {
		"zh_TW": "• 手持武器槽 (Weapon Slot - Z:40)",
		"zh_CN": "• 手持武器槽 (Weapon Slot - Z:40)",
		"en": "• Handheld Weapon Slot (Weapon Slot - Z:40)",
		"ja": "• 手持ち武器スロット (Weapon Slot - Z:40)",
		"ko": "• 무기 슬롯 (Weapon Slot - Z:40)",
		"es": "• Ranura de Arma (Weapon Slot - Z:40)"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		for rzh in expected_races.keys():
			var act := ContentLoc.text("ui", rzh)
			var exp := str(expected_races[rzh][code])
			if act != exp:
				_fail("[%s] 種族 '%s' 翻譯不符: 期望 '%s'，實際 '%s'" % [code, rzh, exp, act])
		var c_slot := ContentLoc.text("ui", "• 外裝服飾槽 (Costume Slot - Z:25)")
		if c_slot != expected_costume_slot[code]:
			_fail("[%s] 外裝服飾槽翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_costume_slot[code], c_slot])
		print("  ✓ [%s] 字典詞條查驗通過" % code)

	# 2. 實例化介面並驗證動態切換
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root_node.add_child(demo)

	var costume_slot_lbl = demo.get_node_or_null("RightControlPanel/Margin/VBox/CostumeControl/SlotLabel") as Label
	var chassis_slot_lbl = demo.get_node_or_null("RightControlPanel/Margin/VBox/ChassisControl/SlotLabel") as Label
	var weapon_slot_lbl = demo.get_node_or_null("RightControlPanel/Margin/VBox/WeaponControl/SlotLabel") as Label
	var panel_title_lbl = demo.get_node_or_null("RightControlPanel/Margin/VBox/PanelTitle") as Label
	var slot_summary_lbl = demo.get_node_or_null("RightControlPanel/Margin/VBox/StatusCard/SlotSummaryLabel") as Label

	if costume_slot_lbl == null or chassis_slot_lbl == null or weapon_slot_lbl == null:
		_fail("無法取得槽位標籤節點")
	if slot_summary_lbl == null:
		_fail("無法取得狀態列標籤節點")

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		# 驗證欄位標題
		if costume_slot_lbl.text != expected_costume_slot[code]:
			_fail("[%s] 外裝槽位標籤未即時更新: '%s'" % [code, costume_slot_lbl.text])
		if chassis_slot_lbl.text != expected_chassis_slot[code]:
			_fail("[%s] 塗裝槽位標籤未即時更新: '%s'" % [code, chassis_slot_lbl.text])
		if weapon_slot_lbl.text != expected_weapon_slot[code]:
			_fail("[%s] 武器槽位標籤未即時更新: '%s'" % [code, weapon_slot_lbl.text])

		# 驗證狀態列（不能為繁中狀態）
		if code != "zh_TW" and code != "zh_CN":
			if "7 大槽位狀態" in slot_summary_lbl.text or "高清合成就緒" in slot_summary_lbl.text:
				_fail("[%s] 狀態列殘留繁中文本: '%s'" % [code, slot_summary_lbl.text])

		# 驗證首發分頁種族按鈕文字
		var btn_rabbit = demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_rabbit") as Button
		if btn_rabbit:
			var name_lbl = btn_rabbit.get_node_or_null("Margin/VBox/NameLabel") as Label
			if name_lbl and name_lbl.text != expected_races["白金兔"][code]:
				_fail("[%s] 白金兔卡片文字不符: 期望 '%s'，實際 '%s'" % [code, expected_races["白金兔"][code], name_lbl.text])

		# 切換種族後文字依舊符合該語系（不退回繁中）
		demo.call("select_race", "fox")
		var btn_fox = demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_fox") as Button
		if btn_fox:
			var name_lbl_fox = btn_fox.get_node_or_null("Margin/VBox/NameLabel") as Label
			if name_lbl_fox and name_lbl_fox.text != expected_races["靈尾狐"][code]:
				_fail("[%s] 點選後靈尾狐卡片文字不符: 期望 '%s'，實際 '%s'" % [code, expected_races["靈尾狐"][code], name_lbl_fox.text])

		# 切換到擴充分頁檢查
		demo.call("switch_tab", "expansion")
		var btn_tiger = demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_tiger") as Button
		if btn_tiger:
			var name_lbl_tiger = btn_tiger.get_node_or_null("Margin/VBox/NameLabel") as Label
			if name_lbl_tiger and name_lbl_tiger.text != expected_races["烈焰虎"][code]:
				_fail("[%s] 烈焰虎卡片文字不符: 期望 '%s'，實際 '%s'" % [code, expected_races["烈焰虎"][code], name_lbl_tiger.text])

		demo.call("switch_tab", "launch")
		print("  ✓ [%s] 實例化介面即時翻譯查驗通過" % code)

	# 3. 驗證翠角鹿 (fawn) 安全隱藏
	var btn_fawn = demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_fawn") as Button
	if btn_fawn != null and btn_fawn.visible:
		_fail("翠角鹿 (fawn) 未具備立繪資源，前端應隱藏，但目前為 visible")
	else:
		print("  ✓ 翠角鹿防護守衛生效（隱藏空卡）")

	demo.queue_free()

	if loc_node:
		loc_node.call("set_locale", "zh_TW")
