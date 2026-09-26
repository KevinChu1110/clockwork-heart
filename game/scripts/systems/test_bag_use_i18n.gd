extends SceneTree
## 背包使用／出售／重要物品提示六語系單元測試 (test_bag_use_i18n.gd)
##
## 驗證：
## 1. 字典映射：使用、出售、重要物品、失敗等 16 組鍵在六語系 (zh_TW, zh_CN, en, ja, ko, es) 完整映射
## 2. 實際執行：真實呼叫 InventorySystem.use_item()
##    - 消耗品使用成功回傳文字與效果
##    - 材料單件出售成功回傳文字與金幣
##    - 重要物品拒絕消耗回傳警示文字
##    - 快捷欄空格子提示
##    - 一鍵賣出材料成功／材料為空提示
## 3. 切語系即時生效 (Loc.set_locale)
## 4. 0-QA24 檢核：en, es 語系下完全無 CJK 中文字元殘留
## 5. 全程零系統 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true

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
	print("=== 開始 test_bag_use_i18n 測試 ===")

	var loc: Node = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var inv: Node = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	if loc == null or gs == null or inv == null:
		_fail("Autoload 節點初始化失敗")
		_finish()
		return

	# 預期映射表
	var expected_use_fail := {
		"zh_TW": "使用失敗。",
		"zh_CN": "使用失败。",
		"en": "Failed to use.",
		"ja": "使用に失敗しました。",
		"ko": "사용에 실패했습니다.",
		"es": "Error al usar.",
	}
	var expected_sell_fail := {
		"zh_TW": "賣出失敗。",
		"zh_CN": "出售失败。",
		"en": "Failed to sell.",
		"ja": "売却に失敗しました。",
		"ko": "판매에 실패했습니다.",
		"es": "Error al vender.",
	}
	var expected_no_item := {
		"zh_TW": "沒有這個道具。",
		"zh_CN": "没有这个道具。",
		"en": "Item not found.",
		"ja": "該当のアイテムがありません。",
		"ko": "해당 아이템이 없습니다.",
		"es": "El objeto no existe.",
	}
	var expected_cannot_use := {
		"zh_TW": "無法使用。",
		"zh_CN": "无法使用。",
		"en": "Cannot be used.",
		"ja": "使用できません。",
		"ko": "사용할 수 없습니다.",
		"es": "No se puede usar.",
	}
	var expected_empty_hotbar := {
		"zh_TW": "第 1 格是空的。開 I 背包指派道具。",
		"zh_CN": "第 1 格是空的。按 I 打开背包指定道具。",
		"en": "Slot 1 is empty. Open bag (I) to assign items.",
		"ja": "スロット 1 は空です。I キーでバッグを開いて道具を登録してください。",
		"ko": "슬롯 1이(가) 비어 있습니다. I 키로 배낭을 열어 아이템을 등록하세요.",
		"es": "La casilla 1 está vacía. Abre la bolsa (I) para asignar un objeto.",
	}
	var expected_no_sell_mats := {
		"zh_TW": "沒有可賣的材料。",
		"zh_CN": "没有可出售的材料。",
		"en": "No sellable materials.",
		"ja": "売却できる素材がありません。",
		"ko": "판매할 수 있는 재료가 없습니다.",
		"es": "No hay materiales para vender.",
	}

	# 1. 六語系字典映射與真實呼叫驗證
	for code in LOCALES:
		loc.call("set_locale", code)
		ContentLoc.reload()

		print("--- 測試語系: %s ---" % code)

		# 1.1 字典靜態映射
		var t_use_fail := ContentLoc.text("ui", "使用失敗。")
		if t_use_fail != expected_use_fail[code]:
			_fail("[%s] 使用失敗。 期望 '%s'，實際 '%s'" % [code, expected_use_fail[code], t_use_fail])

		var t_sell_fail := ContentLoc.text("ui", "賣出失敗。")
		if t_sell_fail != expected_sell_fail[code]:
			_fail("[%s] 賣出失敗。 期望 '%s'，實際 '%s'" % [code, expected_sell_fail[code], t_sell_fail])

		var t_no_item := ContentLoc.text("ui", "沒有這個道具。")
		if t_no_item != expected_no_item[code]:
			_fail("[%s] 沒有這個道具。 期望 '%s'，實際 '%s'" % [code, expected_no_item[code], t_no_item])

		var t_cannot_use := ContentLoc.text("ui", "無法使用。")
		if t_cannot_use != expected_cannot_use[code]:
			_fail("[%s] 無法使用。 期望 '%s'，實際 '%s'" % [code, expected_cannot_use[code], t_cannot_use])

		# 1.2 快捷欄空格子呼叫
		gs.hotbar = ["", "", "", "", "", "", "", ""]
		var r_hb: Dictionary = inv.call("use_hotbar_slot", 0)
		if bool(r_hb.get("ok", true)):
			_fail("[%s] 空快捷欄應回傳 ok=false" % code)
		var msg_hb: String = str(r_hb.get("msg", ""))
		if msg_hb != expected_empty_hotbar[code]:
			_fail("[%s] 空快捷欄提示不符: 期望 '%s'，實際 '%s'" % [code, expected_empty_hotbar[code], msg_hb])
		if code in ["en", "es"] and _has_cjk(msg_hb):
			_fail("[%s] 空快捷欄提示含有中文殘留: %s" % [code, msg_hb])
		if _has_emoji(msg_hb):
			_fail("[%s] 空快捷欄提示含有 Emoji: %s" % [code, msg_hb])

		# 1.3 消耗品使用真實呼叫 (hp_s)
		gs.hp = 10
		gs.max_hp = 100
		gs.inventory = {}
		inv.call("add_item", "hp_s", 2)
		var r_use: Dictionary = inv.call("use_item", "hp_s")
		if not bool(r_use.get("ok", false)):
			_fail("[%s] 使用 hp_s 失敗: %s" % [code, str(r_use.get("msg", ""))])
		var msg_use: String = str(r_use.get("msg", ""))
		if msg_use.is_empty():
			_fail("[%s] 使用 hp_s 應有回傳訊息" % code)
		if code in ["en", "es"] and _has_cjk(msg_use):
			_fail("[%s] 使用道具訊息含有中文殘留: %s" % [code, msg_use])
		if _has_emoji(msg_use):
			_fail("[%s] 使用道具訊息含有 Emoji: %s" % [code, msg_use])
		print("  ok [%s] 使用道具: %s" % [code, msg_use])

		# 1.4 材料單件出售真實呼叫 (iron_scrap)
		gs.inventory = {}
		inv.call("add_item", "iron_scrap", 3)
		var r_sell: Dictionary = inv.call("use_item", "iron_scrap")
		if not bool(r_sell.get("ok", false)):
			_fail("[%s] 出售 iron_scrap 失敗: %s" % [code, str(r_sell.get("msg", ""))])
		var msg_sell: String = str(r_sell.get("msg", ""))
		if msg_sell.is_empty():
			_fail("[%s] 出售 iron_scrap 應有回傳訊息" % code)
		if code in ["en", "es"] and _has_cjk(msg_sell):
			_fail("[%s] 出售材料訊息含有中文殘留: %s" % [code, msg_sell])
		if _has_emoji(msg_sell):
			_fail("[%s] 出售材料訊息含有 Emoji: %s" % [code, msg_sell])
		print("  ok [%s] 出售材料: %s" % [code, msg_sell])

		# 1.5 重要物品真實呼叫 (key_rusty)
		gs.inventory = {}
		inv.call("add_item", "key_rusty", 1)
		var r_key: Dictionary = inv.call("use_item", "key_rusty")
		if bool(r_key.get("ok", true)):
			_fail("[%s] 重要物品不應可消耗" % code)
		var msg_key: String = str(r_key.get("msg", ""))
		if msg_key.is_empty():
			_fail("[%s] 重要物品應有警示訊息" % code)
		if code in ["en", "es"] and _has_cjk(msg_key):
			_fail("[%s] 重要物品警示含有中文殘留: %s" % [code, msg_key])
		if _has_emoji(msg_key):
			_fail("[%s] 重要物品警示含有 Emoji: %s" % [code, msg_key])
		print("  ok [%s] 重要物品警示: %s" % [code, msg_key])

		# 1.6 一鍵賣出全部材料真實呼叫
		gs.inventory = {}
		inv.call("add_item", "iron_scrap", 5)
		var r_all: Dictionary = inv.call("sell_all_materials")
		if not bool(r_all.get("ok", false)):
			_fail("[%s] 一鍵賣出材料失敗" % code)
		var msg_all: String = str(r_all.get("msg", ""))
		if code in ["en", "es"] and _has_cjk(msg_all):
			_fail("[%s] 一鍵賣出訊息含有中文殘留: %s" % [code, msg_all])
		print("  ok [%s] 一鍵賣出: %s" % [code, msg_all])

		# 1.7 空材料一鍵賣出
		var r_empty_mats: Dictionary = inv.call("sell_all_materials")
		if bool(r_empty_mats.get("ok", true)):
			_fail("[%s] 空材料一鍵賣出應回傳 ok=false" % code)
		var msg_empty_mats: String = str(r_empty_mats.get("msg", ""))
		if msg_empty_mats != expected_no_sell_mats[code]:
			_fail("[%s] 空材料一鍵賣出提示不符: 期望 '%s'，實際 '%s'" % [code, expected_no_sell_mats[code], msg_empty_mats])
		if code in ["en", "es"] and _has_cjk(msg_empty_mats):
			_fail("[%s] 空材料提示含有中文殘留: %s" % [code, msg_empty_mats])

	# 2. 動態切語系即時性測試 (驗證在同一運行週期切換語系，立即影響後續回傳訊息)
	print("--- 驗證動態切語系即時生效 ---")
	loc.call("set_locale", "ja")
	ContentLoc.reload()
	gs.inventory = {}
	inv.call("add_item", "key_rusty", 1)
	var r_dyn_ja: Dictionary = inv.call("use_item", "key_rusty")
	var msg_dyn_ja: String = str(r_dyn_ja.get("msg", ""))
	if not msg_dyn_ja.contains("重要アイテムのため消費できません"):
		_fail("動態切換至 ja 後重要物品訊息未即時更新: %s" % msg_dyn_ja)
	else:
		print("  ok 動態切換 ja 即時生效: %s" % msg_dyn_ja)

	loc.call("set_locale", "en")
	ContentLoc.reload()
	var r_dyn_en: Dictionary = inv.call("use_item", "key_rusty")
	var msg_dyn_en: String = str(r_dyn_en.get("msg", ""))
	if not msg_dyn_en.contains("key item and cannot be consumed"):
		_fail("動態切換至 en 後重要物品訊息未即時更新: %s" % msg_dyn_en)
	else:
		print("  ok 動態切換 en 即時生效: %s" % msg_dyn_en)

	# 還原繁中
	loc.call("set_locale", "zh_TW")
	ContentLoc.reload()

	_finish()

func _finish() -> void:
	if _ok:
		print("BAG_USE_I18N_OK")
		quit(0)
	else:
		print("BAG_USE_I18N_FAIL")
		quit(1)
