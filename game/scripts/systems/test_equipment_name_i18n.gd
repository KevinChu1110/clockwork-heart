extends SceneTree
## 裝備與武器名稱六語系單元測試 (test_equipment_name_i18n.gd)
## 驗證規範：
## 1. 改 locale 後，抽 3 件缺譯裝備的顯示名等於該語系詞條。
## 2. 銹劍（以及微末之刃、空手）維持既有譯名。
## 3. 數值、品階、強化數字不變（EquipmentSystem.label 與角色分頁屬性）。
## 4. 全程零系統 emoji。
## 5. review.md 0-QA24（en/es 無中文字元殘留；ja/ko 漢字完全對齊語系檔）。
## 6. review.md 0-QA25（同屏即時刷新）。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _step := 0
var _wait := 0
var _loc_node: Node = null
var _gs: Node = null
var _dt: Node = null
var _eq_sys: Node = null
var _lobby: MobileLobby = null

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
	print("=== 開始 test_equipment_name_i18n 測試 ===")
	root.size = Vector2i(1280, 720)

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

	_dt = root.get_node_or_null("DataTables")
	if _dt == null:
		var DtClass = load("res://scripts/systems/data_tables.gd")
		if DtClass:
			_dt = DtClass.new()
			_dt.name = "DataTables"
			root.add_child(_dt)

	_eq_sys = root.get_node_or_null("EquipmentSystem")
	if _eq_sys == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq_sys = EqClass.new()
			_eq_sys.name = "EquipmentSystem"
			root.add_child(_eq_sys)

	# ── 1. 驗證 3 件缺譯裝備與既有譯名（銹劍、微末之刃、空手）的六語系顯示名 ──
	var expected_knight_saber := {
		"zh_TW": "騎士軍刀",
		"zh_CN": "骑士军刀",
		"en": "Knight's Saber",
		"ja": "騎士の軍刀",
		"ko": "기사의 군도",
		"es": "Sable de caballero"
	}
	var expected_ash_mail := {
		"zh_TW": "灰燼甲片",
		"zh_CN": "灰烬甲片",
		"en": "Ash Scale Mail",
		"ja": "灰のスケイルメイル",
		"ko": "잿빛 비늘갑옷",
		"es": "Malla de ceniza"
	}
	var expected_dawn_blade := {
		"zh_TW": "晨光長劍",
		"zh_CN": "晨光长剑",
		"en": "Dawn Blade",
		"ja": "暁光の長剣",
		"ko": "여명의 장검",
		"es": "Espada del alba"
	}
	var expected_rusty_blade := {
		"zh_TW": "鏽劍",
		"zh_CN": "锈剑",
		"en": "Rusty Sword",
		"ja": "錆びた剣",
		"ko": "녹슨 검",
		"es": "Espada oxidada"
	}
	var expected_meager_edge := {
		"zh_TW": "微末之刃",
		"zh_CN": "微末之刃",
		"en": "Meager Edge",
		"ja": "微末の刃",
		"ko": "미말의 칼날",
		"es": "Filo Ínfimo"
	}
	var expected_bare_hands := {
		"zh_TW": "空手",
		"zh_CN": "空手",
		"en": "Bare hands",
		"ja": "素手",
		"ko": "맨손",
		"es": "Manos vacías"
	}

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)

		# (a) 抽驗 3 件缺譯裝備
		# 1. 騎士軍刀 (knight_saber)
		var inst_ks: Dictionary = _eq_sys.call("roll_instance", "knight_saber", "rare")
		var name_ks: String = _eq_sys.call("display_name", inst_ks)
		if name_ks != expected_knight_saber[code]:
			_fail("[%s] 騎士軍刀 display_name 錯誤: 期望 '%s'，實際 '%s'" % [code, expected_knight_saber[code], name_ks])
		else:
			print("  ✓ [%s] 抽驗 1 騎士軍刀 -> %s" % [code, name_ks])

		# 2. 灰燼甲片 (ash_mail) - 防具
		var inst_am: Dictionary = _eq_sys.call("roll_instance", "ash_mail", "common")
		var name_am: String = _eq_sys.call("display_name", inst_am)
		if name_am != expected_ash_mail[code]:
			_fail("[%s] 灰燼甲片 display_name 錯誤: 期望 '%s'，實際 '%s'" % [code, expected_ash_mail[code], name_am])
		else:
			print("  ✓ [%s] 抽驗 2 灰燼甲片 (防具) -> %s" % [code, name_am])

		# 3. 晨光長劍 (dawn_blade)
		var inst_db: Dictionary = _eq_sys.call("roll_instance", "dawn_blade", "epic")
		var name_db: String = _eq_sys.call("display_name", inst_db)
		if name_db != expected_dawn_blade[code]:
			_fail("[%s] 晨光長劍 display_name 錯誤: 期望 '%s'，實際 '%s'" % [code, expected_dawn_blade[code], name_db])
		else:
			print("  ✓ [%s] 抽驗 3 晨光長劍 -> %s" % [code, name_db])

		# (b) 既有譯名維持不變驗證
		# 銹劍 / 鏽劍
		var name_rb: String = _eq_sys.call("display_name", "鏽劍")
		if name_rb != expected_rusty_blade[code]:
			_fail("[%s] 鏽劍維持既有譯名失敗: 期望 '%s'，實際 '%s'" % [code, expected_rusty_blade[code], name_rb])
		else:
			print("  ✓ [%s] 鏽劍既有譯名維持 -> %s" % [code, name_rb])

		var name_rb_alias: String = _eq_sys.call("display_name", "銹劍")
		if name_rb_alias != expected_rusty_blade[code]:
			_fail("[%s] 銹劍別名維持既有譯名失敗: 期望 '%s'，實際 '%s'" % [code, expected_rusty_blade[code], name_rb_alias])

		# 微末之刃
		var name_me: String = _eq_sys.call("display_name", "微末之刃")
		if name_me != expected_meager_edge[code]:
			_fail("[%s] 微末之刃維持既有譯名失敗: 期望 '%s'，實際 '%s'" % [code, expected_meager_edge[code], name_me])
		else:
			print("  ✓ [%s] 微末之刃既有譯名維持 -> %s" % [code, name_me])

		# 空手
		var name_bh: String = _eq_sys.call("display_name", "空手")
		if name_bh != expected_bare_hands[code]:
			_fail("[%s] 空手維持既有譯名失敗: 期望 '%s'，實際 '%s'" % [code, expected_bare_hands[code], name_bh])

		# (c) 驗證 EquipmentSystem.label 數值維持與名稱在地化
		var lbl: String = _eq_sys.call("label", inst_ks)
		if not lbl.begins_with(expected_knight_saber[code]):
			_fail("[%s] EquipmentSystem.label 未以翻譯名稱開頭: %s" % [code, lbl])
		if _has_emoji(lbl):
			_fail("[%s] EquipmentSystem.label 含有系統 Emoji: %s" % [code, lbl])

		# (d) 驗證 GameState.weapon_display
		if _gs:
			_gs.set("weapon_name", "騎士軍刀")
			var g_wname: String = _gs.call("weapon_display")
			if g_wname != expected_knight_saber[code]:
				_fail("[%s] GameState.weapon_display 錯誤: 期望 '%s'，實際 '%s'" % [code, expected_knight_saber[code], g_wname])

		# (e) review.md 0-QA24 檢驗：en/es 無 CJK 殘留
		if code in ["en", "es"]:
			if _has_cjk(name_ks):
				_fail("[%s] 騎士軍刀含有未翻譯中文: %s" % [code, name_ks])
			if _has_cjk(name_am):
				_fail("[%s] 灰燼甲片含有未翻譯中文: %s" % [code, name_am])
			if _has_cjk(name_db):
				_fail("[%s] 晨光長劍含有未翻譯中文: %s" % [code, name_db])
			if _has_cjk(name_rb):
				_fail("[%s] 鏽劍含有未翻譯中文: %s" % [code, name_rb])

	# ── 2. 測試大廳角色分頁切語系 (review.md 0-QA25) ──
	_loc_node.call("set_locale", "zh_TW")
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			if _wait < 4:
				return false
			_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			_step = 2
			_wait = 0
			# 切到 en 測試
			_loc_node.call("set_locale", "en")
		2:
			if _wait < 4:
				return false
			# 驗證 en 下角色分頁與大廳狀態
			var char_layer = _lobby.get("_char_layer") as Control
			if char_layer == null or not char_layer.visible:
				_fail("切換到 en 後 _char_layer 應保持 visible")

			var w_title = _lobby.get("_char_weapon_title_label") as Label
			if w_title == null or w_title.text != "Weapon Rotation Loadout":
				_fail("en 下武器輪替標題應為 'Weapon Rotation Loadout'，實際: %s" % (w_title.text if w_title else "null"))

			var stat_title = _lobby.get("_char_stat_title_label") as Label
			if stat_title == null or stat_title.text != "Chassis Combat Stats":
				_fail("en 下戰鬥屬性標題應為 'Chassis Combat Stats'，實際: %s" % (stat_title.text if stat_title else "null"))

			# 數值維持不變檢查
			var stat_cards: Array = _lobby.get("_stat_cards")
			if stat_cards.size() >= 3:
				var atk_val_lbl = stat_cards[1].find_child("ValLabel", true, false) as Label
				var def_val_lbl = stat_cards[2].find_child("ValLabel", true, false) as Label
				if atk_val_lbl == null or atk_val_lbl.text != "95":
					_fail("en 下攻擊數值應保持 95，實際: %s" % (atk_val_lbl.text if atk_val_lbl else "null"))
				if def_val_lbl == null or def_val_lbl.text != "48":
					_fail("en 下防禦數值應保持 48，實際: %s" % (def_val_lbl.text if def_val_lbl else "null"))

			_step = 3
			_wait = 0
			# 切到 ja 測試
			_loc_node.call("set_locale", "ja")
		3:
			if _wait < 3:
				return false
			# 驗證 ja 下角色分頁與大廳狀態
			var w_title_ja = _lobby.get("_char_weapon_title_label") as Label
			if w_title_ja == null or w_title_ja.text != "武器ローテーション配置":
				_fail("ja 下武器輪替標題應為 '武器ローテーション配置'，實際: %s" % (w_title_ja.text if w_title_ja else "null"))

			var stat_title_ja = _lobby.get("_char_stat_title_label") as Label
			if stat_title_ja == null or stat_title_ja.text != "機体戦闘属性":
				_fail("ja 下戰鬥屬性標題應為 '機体戦闘属性'，實際: %s" % (stat_title_ja.text if stat_title_ja else "null"))

			# 數值維持不變檢查
			var stat_cards_ja: Array = _lobby.get("_stat_cards")
			if stat_cards_ja.size() >= 3:
				var atk_val_lbl = stat_cards_ja[1].find_child("ValLabel", true, false) as Label
				var def_val_lbl = stat_cards_ja[2].find_child("ValLabel", true, false) as Label
				if atk_val_lbl == null or atk_val_lbl.text != "95":
					_fail("ja 下攻擊數值應保持 95，实际: %s" % (atk_val_lbl.text if atk_val_lbl else "null"))
				if def_val_lbl == null or def_val_lbl.text != "48":
					_fail("ja 下防禦數值應保持 48，实际: %s" % (def_val_lbl.text if def_val_lbl else "null"))

			_finish()
			return true

	return false

func _finish() -> bool:
	_loc_node.call("set_locale", "zh_TW")
	if _ok:
		print("\nEQUIPMENT_NAME_I18N_OK")
		quit(0)
	else:
		push_error("test_equipment_name_i18n 測試失敗")
		quit(1)
	return true
