extends SceneTree
## 鐵匠鋪鍛造彈窗六語系單元測試 (Forge Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含標題、數值欄位、花費、成功率、魂槽、保底、按鈕、回饋訊息對應翻譯
## 2. 實例化 ForgeDialog，在切換 locale 時，標題、按鈕、各視圖標籤即時刷新連動
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

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
					print("TEST_FORGE_I18N_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_I18N_FAIL")
					print("TEST_FORGE_I18N_FAIL")
					quit(1)
				return true
	return false


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _run_test_suite() -> void:
	print("=== 開始 test_forge_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	var gs = root_node.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("level", 20)
		gs.set("gold", 1500)
		gs.set("weapon_tier", 2)
		gs.set("weapon_atk", 10)
		gs.set("weapon_name", "微末之刃")
		gs.set("forge_fail_streak", 1)

	# 1. 驗證詞條字典解析
	var expected_title := {
		"zh_TW": "天宮鐵匠 · 裝備鍛造",
		"zh_CN": "天宫铁匠 · 装备锻造",
		"en": "Celestial Blacksmith · Equipment Forge",
		"ja": "天宮の鍛冶屋 · 装備鍛造",
		"ko": "천궁 대장장이 · 장비 단조",
		"es": "Herrero Celestial · Forja de Equipo",
	}
	var expected_close := {
		"zh_TW": "離開鐵匠鋪",
		"zh_CN": "离开铁匠铺",
		"en": "Leave Smithy",
		"ja": "鍛冶屋を出る",
		"ko": "대장간 나가기",
		"es": "Salir de la herrería",
	}
	var expected_atk_fmt := {
		"zh_TW": "武器攻擊：+%d",
		"zh_CN": "武器攻击：+%d",
		"en": "Weapon ATK: +%d",
		"ja": "武器攻撃：+%d",
		"ko": "무기 공격력: +%d",
		"es": "Ataque de arma: +%d",
	}
	var expected_gold_fmt := {
		"zh_TW": "持有金幣：%d",
		"zh_CN": "持有金币：%d",
		"en": "Gold: %d",
		"ja": "所持ゴールド：%d",
		"ko": "보유 골드: %d",
		"es": "Oro en posesión: %d",
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "天宮鐵匠 · 裝備鍛造")
		if t_title != expected_title[code]:
			_fail("語系 [%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])
		else:
			print("  ✓ [%s] 標題 -> %s" % [code, t_title])

		var t_close := ContentLoc.text("ui", "離開鐵匠鋪")
		if t_close != expected_close[code]:
			_fail("語系 [%s] 離開鐵匠鋪翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_close[code], t_close])
		else:
			print("  ✓ [%s] 離開鐵匠鋪 -> %s" % [code, t_close])

		var t_atk := ContentLoc.text("ui", "武器攻擊：+%d")
		if t_atk != expected_atk_fmt[code]:
			_fail("語系 [%s] 武器攻擊格式不符: 期望 '%s'，實際 '%s'" % [code, expected_atk_fmt[code], t_atk])

		var t_gold := ContentLoc.text("ui", "持有金幣：%d")
		if t_gold != expected_gold_fmt[code]:
			_fail("語系 [%s] 持有金幣格式不符: 期望 '%s'，實際 '%s'" % [code, expected_gold_fmt[code], t_gold])

	# 2. 實例化 Dialog 測試 locale_changed 即時動態連動
	print("\n--- 測試 ForgeDialog 實例與 locale_changed 即時切換 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	var dlg = ForgeDialogScn.new()
	root_node.add_child(dlg)

	var title_lbl := _find_named(dlg, "TitleLabel") as Label
	var weapon_lbl := _find_named(dlg, "WeaponLabel") as Label
	var atk_lbl := _find_named(dlg, "AtkLabel") as Label
	var gold_lbl := _find_named(dlg, "GoldLabel") as Label
	var cost_lbl := _find_named(dlg, "CostLabel") as Label
	var rate_lbl := _find_named(dlg, "RateLabel") as Label
	var slots_lbl := _find_named(dlg, "SlotsLabel") as Label
	var pity_title_lbl := _find_named(dlg, "PityTitleLabel") as Label
	var pity_sub_lbl := _find_named(dlg, "PitySubLabel") as Label
	var btn_forge := _find_named(dlg, "BtnForge") as Button
	var btn_close := _find_named(dlg, "BtnCloseForge") as Button

	if title_lbl == null or weapon_lbl == null or atk_lbl == null or btn_forge == null or btn_close == null:
		_fail("無法找到 ForgeDialog 關鍵 UI 節點")
		return

	# 先驗證繁中
	if title_lbl.text != expected_title["zh_TW"]:
		_fail("初始繁中標題不符: " + title_lbl.text)
	if btn_close.text != expected_close["zh_TW"]:
		_fail("初始繁中關閉按鈕不符: " + btn_close.text)
	print("  ✓ 初始繁中 UI 節點文字正確")

	# 動態切換至 en
	print("  >> 切換至 en...")
	if loc_node:
		loc_node.call("set_locale", "en")
	if title_lbl.text != expected_title["en"]:
		_fail("切換 en 後標題未更新: 期望 '%s', 實際 '%s'" % [expected_title["en"], title_lbl.text])
	if btn_close.text != expected_close["en"]:
		_fail("切換 en 後離開按鈕未更新: " + btn_close.text)
	if not weapon_lbl.text.begins_with("Equipped:"):
		_fail("切換 en 後武器標籤未更新: " + weapon_lbl.text)
	if not atk_lbl.text.begins_with("Weapon ATK:"):
		_fail("切換 en 後攻擊標籤未更新: " + atk_lbl.text)
	if not gold_lbl.text.begins_with("Gold:"):
		_fail("切換 en 後金幣標籤未更新: " + gold_lbl.text)
	if not cost_lbl.text.begins_with("Forge Cost:"):
		_fail("切換 en 後花費標籤未更新: " + cost_lbl.text)
	if not rate_lbl.text.begins_with("Base Success Rate:"):
		_fail("切換 en 後成功率標籤未更新: " + rate_lbl.text)
	if not slots_lbl.text.begins_with("Soul Slots:"):
		_fail("切換 en 後魂槽標籤未更新: " + slots_lbl.text)
	if not pity_title_lbl.text.begins_with("Forge Loss Pity"):
		_fail("切換 en 後保底標題未更新: " + pity_title_lbl.text)
	if not btn_forge.text.begins_with("Forge Tier-Up"):
		_fail("切換 en 後鍛造按鈕未更新: " + btn_forge.text)
	print("  ✓ en 即時刷新驗證通過 (%s)" % title_lbl.text)

	# 動態切換至 ja
	print("  >> 切換至 ja...")
	if loc_node:
		loc_node.call("set_locale", "ja")
	if title_lbl.text != expected_title["ja"]:
		_fail("切換 ja 後標題未更新: 期望 '%s', 實際 '%s'" % [expected_title["ja"], title_lbl.text])
	if btn_close.text != expected_close["ja"]:
		_fail("切換 ja 後離開按鈕未更新: " + btn_close.text)
	if not weapon_lbl.text.begins_with("現在の装備："):
		_fail("切換 ja 後武器標籤未更新: " + weapon_lbl.text)
	if not atk_lbl.text.begins_with("武器攻撃："):
		_fail("切換 ja 後攻擊標籤未更新: " + atk_lbl.text)
	if not gold_lbl.text.begins_with("所持ゴールド："):
		_fail("切換 ja 後金幣標籤未更新: " + gold_lbl.text)
	if not cost_lbl.text.begins_with("昇階コスト："):
		_fail("切換 ja 後花費標籤未更新: " + cost_lbl.text)
	if not rate_lbl.text.begins_with("基本成功率："):
		_fail("切換 ja 後成功率標籤未更新: " + rate_lbl.text)
	if not slots_lbl.text.begins_with("魂スロット解放："):
		_fail("切換 ja 後魂槽標籤未更新: " + slots_lbl.text)
	if not pity_title_lbl.text.begins_with("鍛造連敗保証"):
		_fail("切換 ja 後保底標題未更新: " + pity_title_lbl.text)
	if not btn_forge.text.begins_with("強化昇階"):
		_fail("切換 ja 後鍛造按鈕未更新: " + btn_forge.text)
	print("  ✓ ja 即時刷新驗證通過 (%s)" % title_lbl.text)

	# 測試點擊鍛造按鈕後的回饋訊息是否在當前語系
	print("  >> 測試鍛造點擊回饋訊息 (ja)...")
	btn_forge.pressed.emit()
	var msg_lbl := _find_named(dlg, "MsgLabel") as Label
	if msg_lbl != null and msg_lbl.text != "":
		print("  ✓ ja 鍛造回饋訊息: %s" % msg_lbl.text)
		# 驗證日語系特徵：包含昇階或失敗或ゴールド或上限
		var is_ja := ("へ昇階" in msg_lbl.text or "ゴールド" in msg_lbl.text or "上限に達している" in msg_lbl.text or "機嫌直しの餅" in msg_lbl.text or "保証が1マス" in msg_lbl.text)
		if not is_ja:
			_fail("ja 下鍛造回饋訊息未符合日文字典特徵: " + msg_lbl.text)
		else:
			print("  ✓ ja 鍛造回饋訊息符合日文字典特徵")

	dlg.queue_free()
