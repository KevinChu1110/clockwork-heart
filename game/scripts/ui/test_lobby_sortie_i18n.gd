extends SceneTree
## 大廳出征卡與聚魂分頁按鈕六語系單元測試 (test_lobby_sortie_i18n.gd)
## 驗證：
## 1. 出征卡（推薦戰力／消耗能量／出征／挑戰首領）、有效戰力、一鍵吸收灰魂、聚魂十連在六語系下映射正確。
## 2. 大廳切換語系後，出征卡標籤與按鈕即時刷新。
## 3. 大廳切換語系後，角色頁「有效戰力」徽章即時刷新。
## 4. 大廳切換語系後，聚魂分頁底部「一鍵吸收灰魂」「聚魂十連」按鈕即時刷新。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_lobby_sortie_i18n 測試 ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	var gs := root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	# 1. 字典映射檢查
	var expected_power := {
		"zh_TW": "推薦戰力: 380",
		"zh_CN": "推荐战力: 380",
		"en": "Rec. Power: 380",
		"ja": "推奨戦力: 380",
		"ko": "권장 전투력: 380",
		"es": "Poder Rec.: 380"
	}
	var expected_cost := {
		"zh_TW": "消耗能量: 1",
		"zh_CN": "消耗能量: 1",
		"en": "Energy Cost: 1",
		"ja": "消費エネルギー: 1",
		"ko": "에너지 소모: 1",
		"es": "Consumo Energía: 1"
	}
	var expected_battle := {
		"zh_TW": "出征",
		"zh_CN": "出征",
		"en": "Sortie",
		"ja": "出征",
		"ko": "출정",
		"es": "Batalla"
	}
	var expected_boss := {
		"zh_TW": "挑戰首領",
		"zh_CN": "挑战首领",
		"en": "Challenge Boss",
		"ja": "ボスに挑戦",
		"ko": "보스 도전",
		"es": "Desafiar Jefe"
	}
	var expected_char_power := {
		"zh_TW": "有效戰力 482",
		"zh_CN": "有效战力 482",
		"en": "Effective Power 482",
		"ja": "有効戦力 482",
		"ko": "유효 전투력 482",
		"es": "Poder Efectivo 482"
	}
	var expected_absorb := {
		"zh_TW": "一鍵吸收灰魂",
		"zh_CN": "一键吸收灰魂",
		"en": "Absorb Gray Souls",
		"ja": "灰魂を一括吸収",
		"ko": "잿빛 혼 일괄 흡수",
		"es": "Absorber Almas Grises"
	}
	var expected_draw := {
		"zh_TW": "聚魂十連",
		"zh_CN": "聚魂十连",
		"en": "Draw 10 Souls",
		"ja": "聚魂十連",
		"ko": "10연속 집혼",
		"es": "Invocar 10 Almas"
	}

	for code in LOCALES:
		if _loc_node:
			_loc_node.call("set_locale", code)

		var tp := ContentLoc.text("ui", "推薦戰力: %d") % 380
		if tp != expected_power[code]:
			_fail("[%s] 推薦戰力不符: 期望 '%s'，實際 '%s'" % [code, expected_power[code], tp])
		else:
			print("  ✓ [%s] 推薦戰力 -> %s" % [code, tp])

		var tc := ContentLoc.text("ui", "消耗能量: %d") % 1
		if tc != expected_cost[code]:
			_fail("[%s] 消耗能量不符: 期望 '%s'，實際 '%s'" % [code, expected_cost[code], tc])
		else:
			print("  ✓ [%s] 消耗能量 -> %s" % [code, tc])

		var tb := ContentLoc.text("ui", "出征")
		if tb != expected_battle[code]:
			_fail("[%s] 出征不符: 期望 '%s'，實際 '%s'" % [code, expected_battle[code], tb])
		else:
			print("  ✓ [%s] 出征 -> %s" % [code, tb])

		var tboss := ContentLoc.text("ui", "挑戰首領")
		if tboss != expected_boss[code]:
			_fail("[%s] 挑戰首領不符: 期望 '%s'，實際 '%s'" % [code, expected_boss[code], tboss])
		else:
			print("  ✓ [%s] 挑戰首領 -> %s" % [code, tboss])

		var tcp := ContentLoc.text("ui", "有效戰力 %d") % 482
		if tcp != expected_char_power[code]:
			_fail("[%s] 有效戰力不符: 期望 '%s'，實際 '%s'" % [code, expected_char_power[code], tcp])
		else:
			print("  ✓ [%s] 有效戰力 -> %s" % [code, tcp])

		var tabsb := ContentLoc.text("ui", "一鍵吸收灰魂")
		if tabsb != expected_absorb[code]:
			_fail("[%s] 一鍵吸收灰魂不符: 期望 '%s'，實際 '%s'" % [code, expected_absorb[code], tabsb])
		else:
			print("  ✓ [%s] 一鍵吸收灰魂 -> %s" % [code, tabsb])

		var td := ContentLoc.text("ui", "聚魂十連")
		if td != expected_draw[code]:
			_fail("[%s] 聚魂十連不符: 期望 '%s'，實際 '%s'" % [code, expected_draw[code], td])
		else:
			print("  ✓ [%s] 聚魂十連 -> %s" % [code, td])

	# 2. 建立 MobileLobby 進行節點連動測試
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

		# 切到出征分頁 (Tab.ADVENTURE = 2)
		_lobby.call("_switch_tab", 2)
		_check_sortie_texts("zh_TW", "推薦戰力: 380", "消耗能量: 1", "出征", "挑戰首領")

		# 切換到 en
		if _loc_node:
			_loc_node.call("set_locale", "en")
		_check_sortie_texts("en", "Rec. Power: 380", "Energy Cost: 1", "Sortie", "Challenge Boss")

		# 切換到 ja
		if _loc_node:
			_loc_node.call("set_locale", "ja")
		_check_sortie_texts("ja", "推奨戦力: 380", "消費エネルギー: 1", "出征", "ボスに挑戦")

		# 切到角色分頁 (Tab.CHARACTER = 1)
		_lobby.call("_switch_tab", 1)
		var pbadge: Label = _lobby.get("_char_power_badge") as Label
		if pbadge == null or "有効戦力" not in pbadge.text:
			_fail("ja 角色有效戰力未刷新: %s" % (pbadge.text if pbadge else "null"))
		else:
			print("  ✓ [ja] 角色有效戰力: %s" % pbadge.text)

		# 切回 en 測角色分頁
		if _loc_node:
			_loc_node.call("set_locale", "en")
		if pbadge == null or "Effective Power" not in pbadge.text:
			_fail("en 角色有效戰力未刷新: %s" % (pbadge.text if pbadge else "null"))
		else:
			print("  ✓ [en] 角色有效戰力: %s" % pbadge.text)

		# 切到聚魂分頁 (Tab.SOUL_HALL = 3)
		_lobby.call("_switch_tab", 3)
		var btn_absorb: Button = _lobby.get("_gourd_btn_absorb") as Button
		var btn_draw: Button = _lobby.get("_gourd_btn_draw") as Button
		if btn_absorb == null or btn_absorb.text != "Absorb Gray Souls":
			_fail("en 一鍵吸收灰魂未刷新: %s" % (btn_absorb.text if btn_absorb else "null"))
		else:
			print("  ✓ [en] 聚魂吸收灰魂: %s" % btn_absorb.text)
		if btn_draw == null or btn_draw.text != "Draw 10 Souls":
			_fail("en 聚魂十連未刷新: %s" % (btn_draw.text if btn_draw else "null"))
		else:
			print("  ✓ [en] 聚魂十連: %s" % btn_draw.text)

		# 切換到 ja 測聚魂分頁
		if _loc_node:
			_loc_node.call("set_locale", "ja")
		if btn_absorb == null or btn_absorb.text != "灰魂を一括吸収":
			_fail("ja 一鍵吸收灰魂未刷新: %s" % (btn_absorb.text if btn_absorb else "null"))
		else:
			print("  ✓ [ja] 聚魂吸收灰魂: %s" % btn_absorb.text)
		if btn_draw == null or btn_draw.text != "聚魂十連":
			_fail("ja 聚魂十連未刷新: %s" % (btn_draw.text if btn_draw else "null"))
		else:
			print("  ✓ [ja] 聚魂十連: %s" % btn_draw.text)

		if _ok:
			print("LOBBY_SORTIE_I18N_OK")
			quit(0)
		else:
			print("LOBBY_SORTIE_I18N_FAIL")
			quit(1)
		return true
	return false

func _check_sortie_texts(loc: String, exp_pwr: String, exp_cost: String, exp_btn: String, exp_boss_btn: String) -> void:
	var container: VBoxContainer = _lobby.get("_stages_container") as VBoxContainer
	if container == null:
		_fail("[%s] 找不到 _stages_container" % loc)
		return

	# 第一張卡 (2-1 前哨)
	var card0 = container.find_child("StageCard_2_1", true, false)
	if card0 == null:
		_fail("[%s] 找不到 StageCard_2_1" % loc)
		return
	var pwr0: Label = card0.find_child("PowerLabel", true, false) as Label
	var cost0: Label = card0.find_child("CostLabel", true, false) as Label
	var btn0: Button = card0.find_child("BattleButton", true, false) as Button

	if pwr0 == null or pwr0.text != exp_pwr:
		_fail("[%s] 2-1 推薦戰力不符: 期望 '%s'，實際 '%s'" % [loc, exp_pwr, pwr0.text if pwr0 else "null"])
	else:
		print("  ✓ [%s] 2-1 推薦戰力: %s" % [loc, pwr0.text])

	if cost0 == null or cost0.text != exp_cost:
		_fail("[%s] 2-1 消耗能量不符: 期望 '%s'，實際 '%s'" % [loc, exp_cost, cost0.text if cost0 else "null"])
	else:
		print("  ✓ [%s] 2-1 消耗能量: %s" % [loc, cost0.text])

	if btn0 == null or btn0.text != exp_btn:
		_fail("[%s] 2-1 出征按鈕不符: 期望 '%s'，實際 '%s'" % [loc, exp_btn, btn0.text if btn0 else "null"])
	else:
		print("  ✓ [%s] 2-1 出征按鈕: %s" % [loc, btn0.text])

	# 第四張卡 (2-4 BOSS)
	var card3 = container.find_child("StageCard_2_4", true, false)
	if card3 == null:
		_fail("[%s] 找不到 StageCard_2_4" % loc)
		return
	var btn3: Button = card3.find_child("BattleButton", true, false) as Button
	if btn3 == null or btn3.text != exp_boss_btn:
		_fail("[%s] 2-4 BOSS按鈕不符: 期望 '%s'，實際 '%s'" % [loc, exp_boss_btn, btn3.text if btn3 else "null"])
	else:
		print("  ✓ [%s] 2-4 BOSS按鈕: %s" % [loc, btn3.text])
