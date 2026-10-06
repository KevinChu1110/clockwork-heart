extends SceneTree
## 翠角鹿（第十四族）六語系玩家可見名稱與連動單元測試 (Fawn i18n Unit Test)
## 驗證：
## 1. 六語系 ui.json 包含翠角鹿、職業稱謂（遊俠）、短稱（鹿）、外裝、塗裝、武器與說明翻譯。
## 2. 創角介面在六語系切換下，翠角鹿標題、職業、外裝、塗裝、武器與按鈕即時動態刷新。
## 3. 衣櫥畫面在六語系切換下，翠角鹿外觀卡片與族標籤即時動態刷新（玩具家族分頁後卡片不帶種族前綴）。
## 4. 大廳畫面英雄名稱在六語系即時切換下同步更新。

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
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
			print("FAWN_I18N_OK")
			quit(0)
		else:
			push_error("FAWN_I18N_FAIL")
			print("FAWN_I18N_FAIL")
			quit(1)
		return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_fawn_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	var gs = root_node.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root_node.add_child(gs)

	# 1. 字典詞條查驗
	var expected_dict := {
		"翠角鹿": {
			"zh_TW": "翠角鹿", "zh_CN": "翠角鹿", "en": "The Emerald Fawn",
			"ja": "翠角鹿", "ko": "취각록", "es": "El Ciervo Esmeralda"
		},
		"鹿": {
			"zh_TW": "鹿", "zh_CN": "鹿", "en": "Fawn",
			"ja": "鹿", "ko": "사슴", "es": "Ciervo"
		},
		"遊俠": {
			"zh_TW": "遊俠", "zh_CN": "游侠", "en": "Ranger",
			"ja": "レンジャー", "ko": "레인저", "es": "Guardabosques"
		},
		"翡翠林緣巡守工裝": {
			"zh_TW": "翡翠林緣巡守工裝", "zh_CN": "翡翠林缘巡守工装", "en": "Emerald Verge Scout Uniform",
			"ja": "翡翠の森巡守工装", "ko": "비취 숲 순찰 작업복", "es": "Uniforme de Explorador del Bosque Esmeralda"
		},
		"翡翠林緣巡守背帶工裝": {
			"zh_TW": "翡翠林緣巡守背帶工裝", "zh_CN": "翡翠林缘巡守背带工装", "en": "Emerald Scout Harness Tunic",
			"ja": "翡翠林縁巡守サスペンダー作業着", "ko": "비취 숲 가장자리 순찰 멜빵 작업복", "es": "Arnés de Explorador del Bosque Esmeralda"
		},
		"雙色沖壓原木紋金屬板": {
			"zh_TW": "雙色沖壓原木紋金屬板", "zh_CN": "双色冲压原木纹金属板", "en": "Two-tone Stamped Woodgrain Plate",
			"ja": "2色スタンピング木目調金属板", "ko": "투톤 스탬핑 원목 무늬 금속판", "es": "Chapa Metálica Bicolor con Veta de Madera"
		},
		"沖壓雙色象牙米白與淺褐原木紋金屬板": {
			"zh_TW": "沖壓雙色象牙米白與淺褐原木紋金屬板", "zh_CN": "冲压双色象牙米白与浅褐原木纹金属板", "en": "Stamped Ivory & Light Woodgrain Plate",
			"ja": "スタンピング象牙ホワイト＆薄褐色木目調板", "ko": "스탬핑 아이보리 및 연갈색 원목무늬 판", "es": "Chapa Estampada Marfil y Veta de Madera Clara"
		},
		"翠木角尺複合機關弓": {
			"zh_TW": "翠木角尺複合機關弓", "zh_CN": "翠木角尺复合机关弓", "en": "Verdant Caliber-Horn Composite Bow",
			"ja": "翠木角尺複合からくり弓", "ko": "취목 각척 복합 기관 활", "es": "Arco Compuesto Mecánico de Regla de Cuerno Esmeralda"
		}
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		for key in expected_dict.keys():
			var act := ContentLoc.text("ui", key)
			var exp := str(expected_dict[key][code])
			if act != exp:
				_fail("[%s] 詞條 '%s' 翻譯不符: 期望 '%s'，實際 '%s'" % [code, key, exp, act])
		print("  ✓ [%s] 翠角鹿核心詞條字典查驗通過" % code)

	# 2. 創角介面實例化與六語系即時切換驗證
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root_node.add_child(demo)
	demo.call("switch_tab", "expansion")
	demo.call("select_race", "fawn")

	var hero_title = demo.hero_title_label
	var hero_arch = demo.hero_archetype_label
	var hero_desc = demo.hero_desc_label
	var c_name_lbl = demo.costume_name_label
	var ch_name_lbl = demo.chassis_name_label
	var wpn_name_lbl = demo.weapon_name_label
	var btn_fawn = demo.get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_fawn") as Button

	if hero_title == null or hero_arch == null or hero_desc == null:
		_fail("無法取得創角英雄資訊標籤")

	var exp_creation_titles := {
		"zh_TW": "翠角鹿 (The Emerald Fawn)",
		"zh_CN": "翠角鹿",
		"en": "The Emerald Fawn",
		"ja": "翠角鹿",
		"ko": "취각록 (The Emerald Fawn)",
		"es": "El Ciervo Esmeralda (The Emerald Fawn)"
	}

	var exp_archetypes := {
		"zh_TW": "【遊俠 (Ranger)】",
		"zh_CN": "【游侠】",
		"en": "【Ranger】",
		"ja": "【レンジャー】",
		"ko": "【레인저】",
		"es": "【Guardabosques】"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		if hero_title.text != exp_creation_titles[code]:
			_fail("[%s] 創角翠角鹿標題不符: 期望 '%s'，實際 '%s'" % [code, exp_creation_titles[code], hero_title.text])

		if hero_arch.text != exp_archetypes[code]:
			_fail("[%s] 創角翠角鹿職業稱謂不符: 期望 '%s'，實際 '%s'" % [code, exp_archetypes[code], hero_arch.text])

		if btn_fawn:
			var name_lbl = btn_fawn.get_node_or_null("Margin/VBox/NameLabel") as Label
			if name_lbl and name_lbl.text != expected_dict["翠角鹿"][code]:
				_fail("[%s] 創角種族按鈕文字不符: 期望 '%s'，實際 '%s'" % [code, expected_dict["翠角鹿"][code], name_lbl.text])

		# 驗證英文下無中文字符殘留
		if code == "en":
			if "翠角鹿" in hero_title.text or "遊俠" in hero_arch.text or "自翡翠深林" in hero_desc.text:
				_fail("[en] 創角右側面板殘留中文")
			if "背帶工裝" in c_name_lbl.text or "金屬板" in ch_name_lbl.text or "機關弓" in wpn_name_lbl.text:
				_fail("[en] 創角外觀或武器名稱殘留中文: costume='%s', chassis='%s', wpn='%s'" % [c_name_lbl.text, ch_name_lbl.text, wpn_name_lbl.text])

		print("  ✓ [%s] 創角介面即時語言切換與文字驗證通過" % code)

	demo.queue_free()

	# 3. 衣櫥彈窗六語系即時切換驗證
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	if gs:
		gs.call("reset_new_game", "fawn")
		gs.set("player_name", "翠角鹿")

	var dlg = WardrobeDialog.new()
	root_node.add_child(dlg)
	dlg.set_race_filter("fawn")

	var exp_wardrobe_badges := {
		"zh_TW": "【翠角鹿 · 遊俠 (Ranger)】",
		"zh_CN": "【翠角鹿 · 游侠】",
		"en": "【The Emerald Fawn · Ranger】",
		"ja": "【翠角鹿 · レンジャー】",
		"ko": "【취각록 · 레인저】",
		"es": "【El Ciervo Esmeralda · Guardabosques】"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		# 驗證左側徽章
		if dlg._badge_race_label.text != exp_wardrobe_badges[code]:
			_fail("[%s] 衣櫥左側種族徽章不符: 期望 '%s'，實際 '%s'" % [code, exp_wardrobe_badges[code], dlg._badge_race_label.text])

		if dlg._badge_name_label.text != expected_dict["翠角鹿"][code]:
			_fail("[%s] 衣櫥左側英雄名稱不符: 期望 '%s'，實際 '%s'" % [code, expected_dict["翠角鹿"][code], dlg._badge_name_label.text])

		# 驗證晶片按鈕 (Chip_fawn) 顯示短稱 "鹿" / "Fawn"
		if dlg._filter_chips.has("fawn"):
			var chip_btn: Button = dlg._filter_chips["fawn"]
			if chip_btn.text != expected_dict["鹿"][code]:
				_fail("[%s] 衣櫥鹿晶片標籤文字不符: 期望 '%s'，實際 '%s'" % [code, expected_dict["鹿"][code], chip_btn.text])

		# 驗證卡片名稱
		var found_costume := false
		for btn in dlg._costume_cards:
			var lbl = btn.find_child("NameLabel", true, false)
			if lbl is Label and lbl.text == expected_dict["翡翠林緣巡守工裝"][code]:
				found_costume = true
				break
		if not found_costume:
			_fail("[%s] 衣櫥未找到翠角鹿外裝卡片 '%s'" % [code, expected_dict["翡翠林緣巡守工裝"][code]])

		var found_chassis := false
		for btn in dlg._chassis_cards:
			var lbl = btn.find_child("NameLabel", true, false)
			if lbl is Label and lbl.text == expected_dict["雙色沖壓原木紋金屬板"][code]:
				found_chassis = true
				break
		if not found_chassis:
			_fail("[%s] 衣櫥未找到翠角鹿塗裝卡片 '%s'" % [code, expected_dict["雙色沖壓原木紋金屬板"][code]])

		print("  ✓ [%s] 衣櫥單一篩選即時切換驗證通過" % code)

	# 衣櫥改成玩具家族分頁後，卡片名稱不再加種族前綴（[鹿] 之類）
	dlg.set_race_filter("all")
	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		var exp_plain: String = expected_dict["翡翠林緣巡守工裝"][code]
		var found_plain := false
		for btn in dlg._costume_cards:
			var lbl = btn.find_child("NameLabel", true, false)
			if lbl is Label:
				if lbl.text.begins_with("["):
					_fail("[%s] 衣櫥卡片仍帶種族前綴 '%s'" % [code, lbl.text])
				if lbl.text == exp_plain:
					found_plain = true
		if not found_plain:
			_fail("[%s] 衣櫥未找到翠角鹿外裝卡片 '%s'" % [code, exp_plain])

	print("  ✓ 衣櫥卡片不帶種族前綴，六語系驗證通過")
	dlg.queue_free()

	# 4. 大廳名稱連動驗證
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var lobby = MobileLobby.new()
	root_node.add_child(lobby)

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		var hero_n := str(lobby.call("_get_hero_name"))
		if hero_n != expected_dict["翠角鹿"][code]:
			_fail("[%s] 大廳 _get_hero_name 不符: 期望 '%s'，實際 '%s'" % [code, expected_dict["翠角鹿"][code], hero_n])

	print("  ✓ 大廳英雄名稱六語系即時切換驗證通過")
	lobby.queue_free()

	if loc_node:
		loc_node.call("set_locale", "zh_TW")
