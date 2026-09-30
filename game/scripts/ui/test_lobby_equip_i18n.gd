extends SceneTree
## 大廳裝備欄六語系單元測試 (test_lobby_equip_i18n.gd)
## 驗證：
## 1. 裝備欄槽位標籤（外裝／武器／發條／奇玩）六語系映射正確。
## 2. 兔族裝備部件（晨曦發條單手長劍、雙孔古銅發條鑰匙、自走發條通訊小信鴿）六語系映射正確。
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

	# 1. 驗證白金兔三大裝備名稱在各語系下的翻譯不為空且非繁中（除 zh_TW 外）
	var expected_weapon := {
		"zh_TW": "晨曦發條單手長劍",
		"zh_CN": "晨曦发条单手长剑",
		"en": "Dawn Clockwork Longsword",
		"ja": "晨曦のゼンマイ片手長剣",
		"ko": "새벽 태엽 한손 장검",
		"es": "Espada Larga de Cuerda del Alba"
	}
	var expected_key := {
		"zh_TW": "雙孔古銅發條鑰匙",
		"zh_CN": "双孔古铜发条钥匙",
		"en": "Double-Hole Bronze Clockwork Key",
		"ja": "双孔青銅ゼンマイキー",
		"ko": "쌍구 황동 태엽 열쇠",
		"es": "Llave de Cuerda de Bronce de Doble Orificio"
	}
	var expected_curio := {
		"zh_TW": "自走發條通訊小信鴿",
		"zh_CN": "自走发条通讯小信鸽",
		"en": "Self-Walking Clockwork Carrier Pigeon",
		"ja": "自走ゼンマイ通信伝書鳩",
		"ko": "자주 태엽 통신 비둘기",
		"es": "Paloma Mensajera Mecánica Autómata"
	}

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)

		var tw := ContentLoc.text("ui", "晨曦發條單手長劍")
		if tw != expected_weapon[code]:
			_fail("[%s] 武器翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_weapon[code], tw])
		else:
			print("  ✓ [%s] 晨曦發條單手長劍 -> %s" % [code, tw])

		var tk := ContentLoc.text("ui", "雙孔古銅發條鑰匙")
		if tk != expected_key[code]:
			_fail("[%s] 發條翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_key[code], tk])
		else:
			print("  ✓ [%s] 雙孔古銅發條鑰匙 -> %s" % [code, tk])

		var tc := ContentLoc.text("ui", "自走發條通訊小信鴿")
		if tc != expected_curio[code]:
			_fail("[%s] 奇玩翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_curio[code], tc])
		else:
			print("  ✓ [%s] 自走發條通訊小信鴿 -> %s" % [code, tc])

	# 2. 測試 MobileLobby 裝備清單即時連動
	var gs := root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	if gs:
		gs.player_race = "rabbit"
		gs.paperdoll_slots = {
			"costume": "costume_nutcracker_guard",
			"weapon": "wpn_dawn_blade",
			"winding_key": "key_classic_brass",
			"back_curio": "curio_clockwork_pigeon"
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
		return false

	elif _step == 1:
		if _wait < 8:
			return false
		_step = 2

		var equip_box: VBoxContainer = _lobby.get("_equip_schematic") as VBoxContainer
		if equip_box == null:
			equip_box = _find_named(_lobby, "EquipSchematic") as VBoxContainer
		if equip_box != null:
			var chips := equip_box.get_children()
			if chips.size() >= 4:
				var t0 := (chips[0] as Button).text
				var t1 := (chips[1] as Button).text
				var t2 := (chips[2] as Button).text
				var t3 := (chips[3] as Button).text
				print("    [en] 0: %s" % t0)
				print("    [en] 1: %s" % t1)
				print("    [en] 2: %s" % t2)
				print("    [en] 3: %s" % t3)
				if not ("Costume" in t0 or "Outfit" in t0):
					_fail("en 外裝未正確翻譯: %s" % t0)
				if not ("Dawn Clockwork Longsword" in t1 or "Weapon" in t1):
					_fail("en 武器未正確翻譯: %s" % t1)
				if not ("Double-Hole" in t2 or "Key" in t2):
					_fail("en 發條未正確翻譯: %s" % t2)
				if not ("Carrier Pigeon" in t3 or "Curio" in t3):
					_fail("en 奇玩未正確翻譯: %s" % t3)

		# 切換至 ja，檢查即時刷新
		if _loc_node:
			_loc_node.call("set_locale", "ja")
		return false

	elif _step == 2:
		if _wait < 12:
			return false
		_step = 3

		var equip_box: VBoxContainer = _lobby.get("_equip_schematic") as VBoxContainer
		if equip_box == null:
			equip_box = _find_named(_lobby, "EquipSchematic") as VBoxContainer
		if equip_box != null:
			var chips := equip_box.get_children()
			if chips.size() >= 4:
				var t0 := (chips[0] as Button).text
				var t1 := (chips[1] as Button).text
				var t2 := (chips[2] as Button).text
				var t3 := (chips[3] as Button).text
				print("    [ja] 0: %s" % t0)
				print("    [ja] 1: %s" % t1)
				print("    [ja] 2: %s" % t2)
				print("    [ja] 3: %s" % t3)
				if not ("衣装" in t0):
					_fail("ja 外裝未正確翻譯: %s" % t0)
				if not ("晨曦のゼンマイ" in t1 or "武器" in t1):
					_fail("ja 武器未正確翻譯: %s" % t1)
				if not ("双孔青銅" in t2 or "ゼンマイ" in t2):
					_fail("ja 發條未正確翻譯: %s" % t2)
				if not ("伝書鳩" in t3 or "骨董品" in t3):
					_fail("ja 奇玩未正確翻譯: %s" % t3)

		# 收工還原
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		if _lobby:
			_lobby.queue_free()

		if _ok:
			print("LOBBY_EQUIP_I18N_OK")
			quit(0)
		else:
			print("LOBBY_EQUIP_I18N_FAIL")
			quit(1)
		return true

	return false
