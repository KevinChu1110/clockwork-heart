extends SceneTree
## 大廳裝備欄六語系單元測試 (test_lobby_equip_i18n.gd)
## 驗證：
## 1. 裝備欄槽位標籤（外裝／武器／發條／奇玩）六語系映射正確。
## 2. 蛙族裝備部件（碧葉旋刃機關鏢、雙蝶翼同心圓黃銅發條鑰匙、微型發條荷葉浮空傘）六語系映射正確。
## 3. 大廳切換語系後，EquipSchematic 按鈕文字即時刷新（review.md 0-QA25）。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Node = null
var _loc_node: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _find_named(n: Node, target_name: String) -> Node:
	if n == null:
		return null
	if n.name == target_name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, target_name)
		if hit != null:
			return hit
	return null

func _initialize() -> void:
	print("=== 開始 test_lobby_equip_i18n 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	# 1. 驗證青蛙三大裝備名稱在各語系下的翻譯不為空且非繁中（除 zh_TW 外）
	var expected_weapon := {
		"zh_TW": "碧葉旋刃機關鏢",
		"zh_CN": "碧叶旋刃机关镖",
		"en": "Lotus Cog Dart",
		"ja": "碧葉旋刃からくり鏢",
		"ko": "벽엽선인 기관 표창",
		"es": "Dardo Mecánico de Hoja de Loto"
	}
	var expected_key := {
		"zh_TW": "雙蝶翼同心圓黃銅發條鑰匙",
		"zh_CN": "双蝶翼同心圆黄铜发条钥匙",
		"en": "Twin-Wing Concentric Brass Key",
		"ja": "双蝶翼同心円黄銅ゼンマイキー",
		"ko": "쌍접익 동심원 황동 태엽 열쇠",
		"es": "Llave de Cuerda Concéntrica de Doble Ala de Latón"
	}
	var expected_curio := {
		"zh_TW": "微型發條荷葉浮空傘",
		"zh_CN": "微型发条荷叶浮空伞",
		"en": "Floating Lotus Leaf Parasol",
		"ja": "超小型ゼンマイ蓮葉浮空傘",
		"ko": "초소형 태엽 연잎 부유 우산",
		"es": "Parasol Flotante de Hoja de Loto Mecánico"
	}

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)

		var tw := ContentLoc.text("ui", "碧葉旋刃機關鏢")
		if tw != expected_weapon[code]:
			_fail("[%s] 武器翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_weapon[code], tw])
		else:
			print("  ✓ [%s] 碧葉旋刃機關鏢 -> %s" % [code, tw])

		var tk := ContentLoc.text("ui", "雙蝶翼同心圓黃銅發條鑰匙")
		if tk != expected_key[code]:
			_fail("[%s] 發條翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_key[code], tk])
		else:
			print("  ✓ [%s] 雙蝶翼同心圓黃銅發條鑰匙 -> %s" % [code, tk])

		var tc := ContentLoc.text("ui", "微型發條荷葉浮空傘")
		if tc != expected_curio[code]:
			_fail("[%s] 奇玩翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_curio[code], tc])
		else:
			print("  ✓ [%s] 微型發條荷葉浮空傘 -> %s" % [code, tc])

	# 2. 測試 MobileLobby 裝備清單即時連動
	var gs := root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	if gs:
		gs.player_race = "frog"
		gs.paperdoll_slots = {
			"costume": "costume_spring_forest_courier",
			"weapon": "wpn_lotus_cog_dart",
			"winding_key": "key_twin_wing_concentric",
			"back_curio": "curio_lotus_leaf_parasol"
		}

	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

func _process(_d: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 4:
			return false
		_step = 1

		var equip_box: VBoxContainer = _lobby.get("_equip_schematic") as VBoxContainer
		if equip_box == null:
			equip_box = _find_named(_lobby, "EquipSchematic") as VBoxContainer
		if equip_box == null:
			_fail("找不到 EquipSchematic 容器")
		else:
			print("  ✓ 找到 EquipSchematic 容器，子項目數：%d" % equip_box.get_child_count())
			var chips := equip_box.get_children()
			if chips.size() >= 4:
				print("    [zh_TW] 0: %s" % (chips[0] as Button).text)
				print("    [zh_TW] 1: %s" % (chips[1] as Button).text)
				print("    [zh_TW] 2: %s" % (chips[2] as Button).text)
				print("    [zh_TW] 3: %s" % (chips[3] as Button).text)

		# 切換至 en，檢查即時刷新
		if _loc_node:
			_loc_node.call("set_locale", "en")

		equip_box = _lobby.get("_equip_schematic") as VBoxContainer
		if equip_box == null:
			equip_box = _find_named(_lobby, "EquipSchematic") as VBoxContainer
		if equip_box:
			var chips_en := equip_box.get_children()
			if chips_en.size() >= 4:
				var txt_costume: String = (chips_en[0] as Button).text
				var txt_weapon: String = (chips_en[1] as Button).text
				var txt_key: String = (chips_en[2] as Button).text
				var txt_curio: String = (chips_en[3] as Button).text

				print("    [en] 0: %s" % txt_costume)
				print("    [en] 1: %s" % txt_weapon)
				print("    [en] 2: %s" % txt_key)
				print("    [en] 3: %s" % txt_curio)

				if "Outfit" not in txt_costume or "Spring Forest Courier Overalls" not in txt_costume:
					_fail("en 外裝未正確翻譯: %s" % txt_costume)
				if "Weapon" not in txt_weapon or "Lotus Cog Dart" not in txt_weapon:
					_fail("en 武器未正確翻譯: %s" % txt_weapon)
				if "Clockwork" not in txt_key or "Twin-Wing Concentric Brass Key" not in txt_key:
					_fail("en 發條未正確翻譯: %s" % txt_key)
				if "Curio" not in txt_curio or "Floating Lotus Leaf Parasol" not in txt_curio:
					_fail("en 奇玩未正確翻譯: %s" % txt_curio)

		# 切換至 ja，檢查即時刷新
		if _loc_node:
			_loc_node.call("set_locale", "ja")

		equip_box = _lobby.get("_equip_schematic") as VBoxContainer
		if equip_box == null:
			equip_box = _find_named(_lobby, "EquipSchematic") as VBoxContainer
		if equip_box:
			var chips_ja := equip_box.get_children()
			if chips_ja.size() >= 4:
				var txt_costume: String = (chips_ja[0] as Button).text
				var txt_weapon: String = (chips_ja[1] as Button).text
				var txt_key: String = (chips_ja[2] as Button).text
				var txt_curio: String = (chips_ja[3] as Button).text

				print("    [ja] 0: %s" % txt_costume)
				print("    [ja] 1: %s" % txt_weapon)
				print("    [ja] 2: %s" % txt_key)
				print("    [ja] 3: %s" % txt_curio)

				if "衣装" not in txt_costume:
					_fail("ja 外裝標題未正確翻譯: %s" % txt_costume)
				if "からくり鏢" not in txt_weapon:
					_fail("ja 武器未正確翻譯: %s" % txt_weapon)
				if "ゼンマイキー" not in txt_key:
					_fail("ja 發條未正確翻譯: %s" % txt_key)
				if "蓮葉浮空傘" not in txt_curio:
					_fail("ja 奇玩未正確翻譯: %s" % txt_curio)

		if _ok:
			print("LOBBY_EQUIP_I18N_OK")
			quit(0)
		else:
			print("LOBBY_EQUIP_I18N_FAIL")
			quit(1)
		return true
	return false
