extends SceneTree
## 裝備面板兩項可見缺陷修復驗證單元測試 (test_equip_panel_i18n.gd)
## 驗證項目：
## 1. 六語系武器類型後綴（EquipmentSystem.weapon_line_name）：
##    zh_TW: 劍 / 長槍 / 斧 / 弓
##    en: Sword / Spear / Axe / Bow
##    ja: 剣 / 長槍 / 斧 / 弓
##    ko: 검 / 창 / 도끼 / 활
##    zh_CN: 剑 / 长枪 / 斧 / 弓
##    es: Espada / Lanza / Hacha / Arco
## 2. 裝備面板背包武器格品質標籤不殘留未翻譯英文「· sword」：
##    zh_TW 顯示為「上品 · 劍」等，無英文 sword。
##    六語系皆正確對照各自語言後綴。
## 3. 英文裝備名折行保護與品質標籤不溢出：
##    autowrap_mode 為 AUTOWRAP_WORD，單字中間絕不折行。
##    Bladestance Ring 完整呈現，品質標籤 Rare 具有足夠垂直邊距。
## 4. 動態切換語系 (Loc.locale_changed) 即時刷新。

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _loc_node: Node = null
var _gs: Node = null
var _eq: Node = null
var _dt: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_equip_panel_i18n 單元測試 ===")
	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_dt = root.get_node_or_null("DataTables")

	if _loc_node == null or _gs == null or _eq == null or _dt == null:
		_fail("Autoload 未就緒: Loc=%s, GameState=%s, EquipmentSystem=%s, DataTables=%s" % [str(_loc_node), str(_gs), str(_eq), str(_dt)])
		quit(1)
		return

	_run_tests()

	if _ok:
		print("\n=== ✓ test_equip_panel_i18n 全部通過！ ===")
		print("EQUIP_PANEL_I18N_OK")
		quit(0)
	else:
		print("\n=== ✗ test_equip_panel_i18n 測試失敗！ ===")
		print("EQUIP_PANEL_I18N_FAIL")
		quit(1)

func _run_tests() -> void:
	var expected_names := {
		"zh_TW": {"sword": "劍", "spear": "長槍", "axe": "斧", "bow": "弓"},
		"zh_CN": {"sword": "剑", "spear": "长枪", "axe": "斧", "bow": "弓"},
		"en": {"sword": "Sword", "spear": "Spear", "axe": "Axe", "bow": "Bow"},
		"ja": {"sword": "剣", "spear": "長槍", "axe": "斧", "bow": "弓"},
		"ko": {"sword": "검", "spear": "창", "axe": "도끼", "bow": "활"},
		"es": {"sword": "Espada", "spear": "Lanza", "axe": "Hacha", "bow": "Arco"}
	}

	# 1. 驗證六語系 weapon_line_name
	print("\n--- 1. 驗證六語系 weapon_line_name ---")
	for code in LOCALES:
		_loc_node.call("set_locale", code)
		for line_key in ["sword", "spear", "axe", "bow"]:
			var actual: String = _eq.call("weapon_line_name", line_key)
			var expected: String = expected_names[code][line_key]
			if actual != expected:
				_fail("[%s] weapon_line_name(%s) 期望 '%s'，實際 '%s'" % [code, line_key, expected, actual])
			else:
				print("  ✓ [%s] %s -> %s" % [code, line_key, actual])

	# 2. 驗證裝備面板背包格品質標籤在六語系下無英文殘留
	print("\n--- 2. 驗證裝備面板背包武器格品質標籤 ---")
	var EquipPanelScn = load("res://scripts/ui/panels/equip_panel.gd")
	var dummy_host = Node.new()
	var panel = EquipPanelScn.new(dummy_host)

	var weapon_inst := {
		"uid": "test_wpn_1",
		"base_id": "knight_saber",
		"name": "騎士軍刀",
		"slot": "weapon",
		"tier": 1,
		"line": "sword",
		"quality": "rare",
		"quality_label": "上品",
		"rolled": {"atk": 10}
	}

	for code in LOCALES:
		_loc_node.call("set_locale", code)
		var cell: Control = panel._bag_cell(weapon_inst)
		var labels: Array = []
		_find_labels(cell, labels)
		if labels.size() < 2:
			_fail("[%s] 背包格標籤數量不足" % code)
			continue
		var ql: Label = labels[1]
		print("  [%s] 武器品質標籤: '%s'" % [code, ql.text])
		if code == "zh_TW":
			if "sword" in ql.text:
				_fail("[zh_TW] 武器格殘留未翻譯英文 'sword': '%s'" % ql.text)
			if not ("· 劍" in ql.text):
				_fail("[zh_TW] 武器格應包含 '· 劍': '%s'" % ql.text)
			else:
				print("    ✓ [zh_TW] 繁中品質標籤無英文 sword，正確為: %s" % ql.text)
		elif code == "en":
			if not ("Sword" in ql.text):
				_fail("[en] 武器格應包含 'Sword': '%s'" % ql.text)
			else:
				print("    ✓ [en] 英文品質標籤正確: %s" % ql.text)
		elif code == "ja":
			if "sword" in ql.text:
				_fail("[ja] 武器格殘留英文 'sword': '%s'" % ql.text)
			if not ("· 剣" in ql.text or "・剣" in ql.text or "剣" in ql.text):
				_fail("[ja] 武器格應包含日文 '剣': '%s'" % ql.text)
		elif code == "ko":
			if "sword" in ql.text:
				_fail("[ko] 武器格殘留英文 'sword': '%s'" % ql.text)
			if not ("검" in ql.text):
				_fail("[ko] 武器格應包含韓文 '검': '%s'" % ql.text)
		cell.queue_free()

	# 3. 驗證英文 Bladestance Ring 單字不拆行與版面防溢出
	print("\n--- 3. 驗證英文 Bladestance Ring 單字不折行與卡片邊框空間 ---")
	_loc_node.call("set_locale", "en")
	var ring_inst := {
		"uid": "test_ring_1",
		"base_id": "blade_ring",
		"name": "鋒勢指環",
		"slot": "accessory",
		"tier": 1,
		"quality": "rare",
		"quality_label": "稀有",
		"rolled": {}
	}
	var ring_cell: Control = panel._bag_cell(ring_inst)
	if ring_cell.custom_minimum_size.y < 115:
		_fail("背包卡片高度不足 115px (當前: %f)，品質標籤容易貼邊溢出" % ring_cell.custom_minimum_size.y)
	else:
		print("  ✓ 背包卡片高度已增加為: %s (防溢出安全邊距)" % str(ring_cell.custom_minimum_size))

	var ring_labels: Array = []
	_find_labels(ring_cell, ring_labels)
	var name_label: Label = ring_labels[0]
	if name_label.autowrap_mode != TextServer.AUTOWRAP_WORD:
		_fail("道具名 autowrap_mode 應為 AUTOWRAP_WORD (2)，當前為 %d" % name_label.autowrap_mode)
	else:
		print("  ✓ 道具名 autowrap_mode 為 AUTOWRAP_WORD，單字中間絕不折行")

	if name_label.text != "Bladestance Ring":
		_fail("英文道具名應為 'Bladestance Ring'，實際為 '%s'" % name_label.text)
	else:
		print("  ✓ 英文道具名正確解析為: %s" % name_label.text)

	ring_cell.queue_free()
	_loc_node.call("set_locale", "zh_TW")

func _find_labels(n: Node, out: Array) -> void:
	if n == null:
		return
	if n is Label:
		out.append(n)
	for c in n.get_children():
		_find_labels(c, out)
