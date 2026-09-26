extends SceneTree
## W8 Hub 殼玩家可見字六語系單元測試 (W8 Hub i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含橫幅、章節資訊、首通/掃蕩/回復/聚魂按鈕、提示等 ContentLoc 查表
## 2. 實例化 W8HubView，切換語系時，Banner、Info、4個操作按鈕、Hint 即時連動刷新
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留、零系統 emoji
## 4. 切回 zh_TW 正確還原繁中

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const W8HubView = preload("res://scripts/systems/wave8/w8_hub_view.gd")

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
					print("TEST_W8_HUB_I18N_OK")
					quit(0)
				else:
					push_error("TEST_W8_HUB_I18N_FAIL")
					print("TEST_W8_HUB_I18N_FAIL")
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


func _check_no_emoji(text: String, label: String) -> void:
	for ch in text:
		var cp := ch.unicode_at(0)
		if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF):
			_fail("發現系統 Emoji 違規 [%s]: %s" % [label, text])


func _run_test_suite() -> void:
	print("=== 開始 test_w8_hub_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	# 1. 驗證六語系字典靜態映射
	print("\n--- 1. 驗證六語系字典靜態映射與 ContentLoc.text ---")
	var expected_banner_onboard := {
		"zh_TW": "玩具堆邊緣 · 新手引導",
		"zh_CN": "玩具堆边缘 · 新手引导",
		"en": "Toy-pile Edge · Novice Guide",
		"ja": "玩具の山の縁 · 初心者ガイド",
		"ko": "장난감 더미 가장자리 · 초보자 가이드",
		"es": "Orilla del montón · Guía de principiante",
	}
	var expected_btn_first_clear := {
		"zh_TW": "首通 玩具堆邊緣",
		"zh_CN": "首通 玩具堆边缘",
		"en": "First Clear: Toy-pile Edge",
		"ja": "初回クリア 玩具の山の縁",
		"ko": "첫 클리어 장난감 더미 가장자리",
		"es": "Primera victoria: Orilla del montón",
	}
	var expected_btn_sweep := {
		"zh_TW": "掃蕩 玩具堆邊緣",
		"zh_CN": "扫荡 玩具堆边缘",
		"en": "Sweep: Toy-pile Edge",
		"ja": "掃討 玩具の山の縁",
		"ko": "소탕 장난감 더미 가장자리",
		"es": "Barrer: Orilla del montón",
	}
	var expected_btn_sim_regen := {
		"zh_TW": "等 8 分（模擬回復）",
		"zh_CN": "等 8 分（模拟回复）",
		"en": "Wait 8 min (Sim Regen)",
		"ja": "8分待機（回復シミュレーション）",
		"ko": "8분 대기 (회복 시뮬레이션)",
		"es": "Esperar 8 min (Simulación de recarga)",
	}
	var expected_btn_goto_soul := {
		"zh_TW": "前往聚魂",
		"zh_CN": "前往聚魂",
		"en": "Go to Soul Draw",
		"ja": "魂寄せへ",
		"ko": "영혼 뽑기로 이동",
		"es": "Ir a extracción de almas",
	}
	var expected_hint := {
		"zh_TW": "引導流程：新手引導 → 聚魂抽取 → 章節挑戰。日常發條每日一選，漏天不補。",
		"zh_CN": "引导流程：新手引导 → 聚魂抽取 → 章节挑战。日常发条每日一选，漏天不补。",
		"en": "Guide Flow: Novice Guide → Soul Drawing → Chapter Challenge. Daily wind-up once per day; missed days cannot be made up.",
		"ja": "進行ガイド：初心者ガイド → 魂寄せガチャ → 章チャレンジ。デイリーぜんまいは1日1回、逃した日は補填されません。",
		"ko": "진행 가이드: 초보자 가이드 → 영혼 뽑기 → 챕터 도전. 일일 태엽은 하루 한 번 선택, 지나간 날은 보충되지 않습니다.",
		"es": "Flujo de guía: Guía de principiante → Extracción de almas → Desafío de capítulo. La cuerda diaria se elige una vez al día; los días perdidos no se recuperan.",
	}

	for code in LOCALES:
		loc_node.call("set_locale", code)

		var val_onboard := ContentLoc.text("ui", "玩具堆邊緣 · 新手引導")
		if val_onboard != expected_banner_onboard[code]:
			_fail("ContentLoc ui '玩具堆邊緣 · 新手引導' [%s] 預期 '%s' 實得 '%s'" % [code, expected_banner_onboard[code], val_onboard])
		else:
			print("  ✓ [%s] Banner(Onboard) -> %s" % [code, val_onboard])

		var val_b1 := ContentLoc.text("ui", "首通 玩具堆邊緣")
		if val_b1 != expected_btn_first_clear[code]:
			_fail("ContentLoc ui '首通 玩具堆邊緣' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_first_clear[code], val_b1])

		var val_b2 := ContentLoc.text("ui", "掃蕩 玩具堆邊緣")
		if val_b2 != expected_btn_sweep[code]:
			_fail("ContentLoc ui '掃蕩 玩具堆邊緣' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_sweep[code], val_b2])

		var val_b3 := ContentLoc.text("ui", "等 8 分（模擬回復）")
		if val_b3 != expected_btn_sim_regen[code]:
			_fail("ContentLoc ui '等 8 分（模擬回復）' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_sim_regen[code], val_b3])

		var val_b4 := ContentLoc.text("ui", "前往聚魂")
		if val_b4 != expected_btn_goto_soul[code]:
			_fail("ContentLoc ui '前往聚魂' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_goto_soul[code], val_b4])

		var val_hint := ContentLoc.text("ui", "引導流程：新手引導 → 聚魂抽取 → 章節挑戰。日常發條每日一選，漏天不補。")
		if val_hint != expected_hint[code]:
			_fail("ContentLoc ui 'Hint' [%s] 預期 '%s' 實得 '%s'" % [code, expected_hint[code], val_hint])

		_check_no_emoji(val_onboard, "val_onboard")
		_check_no_emoji(val_b1, "val_b1")
		_check_no_emoji(val_b2, "val_b2")
		_check_no_emoji(val_b3, "val_b3")
		_check_no_emoji(val_b4, "val_b4")
		_check_no_emoji(val_hint, "val_hint")

	# 2. 實例化 W8HubView 進行動態即時切換驗證
	print("\n--- 2. 測試 W8HubView 實例與 locale_changed 即時切換 ---")
	loc_node.call("set_locale", "zh_TW")

	var hub = W8HubView.new()
	root_node.add_child(hub)
	hub.call("_goto", 2) # Phase.CHAPTER

	var banner := _find_named(hub, "Banner") as Label
	var info := _find_named(hub, "Info") as Label
	var btn_b1 := _find_named(hub, "BtnFirstClear") as Button
	var btn_b2 := _find_named(hub, "BtnSweep") as Button
	var btn_b3 := _find_named(hub, "BtnSimRegen") as Button
	var btn_b4 := _find_named(hub, "BtnGotoSoul") as Button
	var hint := _find_named(hub, "Hint") as Label

	if banner == null or info == null or btn_b1 == null or btn_b2 == null or btn_b3 == null or btn_b4 == null or hint == null:
		_fail("無法找到 W8Hub 關鍵 UI 節點")
		return

	# 驗證初始繁中
	if not banner.text.begins_with("玩具堆邊緣 · 首通與掃蕩"):
		_fail("初始繁中 Banner 未符合: " + banner.text)
	if not info.text.begins_with("章節「玩具堆邊緣」"):
		_fail("初始繁中 Info 未符合: " + info.text)
	if btn_b1.text != expected_btn_first_clear["zh_TW"]:
		_fail("初始繁中 BtnFirstClear 未符合: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["zh_TW"]:
		_fail("初始繁中 BtnSweep 未符合: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["zh_TW"]:
		_fail("初始繁中 BtnSimRegen 未符合: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["zh_TW"]:
		_fail("初始繁中 BtnGotoSoul 未符合: " + btn_b4.text)
	if btn_b4.text != expected_btn_goto_soul["zh_TW"]:
		_fail("初始繁中 BtnGotoSoul 未符合: " + btn_b4.text)
	if hint.text != expected_hint["zh_TW"]:
		_fail("初始繁中 Hint 未符合: " + hint.text)
	print("  ✓ 初始繁中 (zh_TW) 所有 UI 節點文字正確")

	# 動態切換至 en
	print("  >> 切換至 en...")
	loc_node.call("set_locale", "en")
	if not banner.text.begins_with("Toy-pile Edge · First Clear & Sweep"):
		_fail("切換至 en 後 Banner 未即時更新: " + banner.text)
	if not info.text.begins_with("Chapter \"Toy-pile Edge\""):
		_fail("切換至 en 後 Info 未即時更新: " + info.text)
	if btn_b1.text != expected_btn_first_clear["en"]:
		_fail("切換至 en 後 BtnFirstClear 未即時更新: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["en"]:
		_fail("切換至 en 後 BtnSweep 未即時更新: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["en"]:
		_fail("切換至 en 後 BtnSimRegen 未即時更新: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["en"]:
		_fail("切換至 en 後 BtnGotoSoul 未即時更新: " + btn_b4.text)
	if hint.text != expected_hint["en"]:
		_fail("切換至 en 後 Hint 未即時更新: " + hint.text)
	print("  ✓ [en] 即時刷新成功，無繁中殘留")

	# 動態切換至 ja
	print("  >> 切換至 ja...")
	loc_node.call("set_locale", "ja")
	if not banner.text.begins_with("玩具の山の縁 · 初回クリアと掃討"):
		_fail("切換至 ja 後 Banner 未即時更新: " + banner.text)
	if not info.text.begins_with("章「玩具の山の縁」"):
		_fail("切換至 ja 後 Info 未即時更新: " + info.text)
	if btn_b1.text != expected_btn_first_clear["ja"]:
		_fail("切換至 ja 後 BtnFirstClear 未即時更新: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["ja"]:
		_fail("切換至 ja 後 BtnSweep 未即時更新: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["ja"]:
		_fail("切換至 ja 後 BtnSimRegen 未即時更新: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["ja"]:
		_fail("切換至 ja 後 BtnGotoSoul 未即時更新: " + btn_b4.text)
	if hint.text != expected_hint["ja"]:
		_fail("切換至 ja 後 Hint 未即時更新: " + hint.text)
	print("  ✓ [ja] 即時刷新成功，無繁中殘留")

	# 動態切換至 ko
	print("  >> 切換至 ko...")
	loc_node.call("set_locale", "ko")
	if not banner.text.begins_with("장난감 더미 가장자리 · 첫 클리어 및 소탕"):
		_fail("切換至 ko 後 Banner 未即時更新: " + banner.text)
	if not info.text.begins_with("챕터 「장난감 더미 가장자리」"):
		_fail("切換至 ko 後 Info 未即時更新: " + info.text)
	if btn_b1.text != expected_btn_first_clear["ko"]:
		_fail("切換至 ko 後 BtnFirstClear 未即時更新: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["ko"]:
		_fail("切換至 ko 後 BtnSweep 未即時更新: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["ko"]:
		_fail("切換至 ko 後 BtnSimRegen 未即時更新: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["ko"]:
		_fail("切換至 ko 後 BtnGotoSoul 未即時更新: " + btn_b4.text)
	if hint.text != expected_hint["ko"]:
		_fail("切換至 ko 後 Hint 未即時更新: " + hint.text)
	print("  ✓ [ko] 即時刷新成功，無繁中殘留")

	# 動態切換至 es
	print("  >> 切換至 es...")
	loc_node.call("set_locale", "es")
	if not banner.text.begins_with("Orilla del montón · Primera victoria y barrido"):
		_fail("切換至 es 後 Banner 未即時更新: " + banner.text)
	if not info.text.begins_with("Capítulo \"Orilla del montón\""):
		_fail("切換至 es 後 Info 未即時更新: " + info.text)
	if btn_b1.text != expected_btn_first_clear["es"]:
		_fail("切換至 es 後 BtnFirstClear 未即時更新: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["es"]:
		_fail("切換至 es 後 BtnSweep 未即時更新: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["es"]:
		_fail("切換至 es 後 BtnSimRegen 未即時更新: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["es"]:
		_fail("切換至 es 後 BtnGotoSoul 未即時更新: " + btn_b4.text)
	if hint.text != expected_hint["es"]:
		_fail("切換至 es 後 Hint 未即時更新: " + hint.text)
	print("  ✓ [es] 即時刷新成功，無繁中殘留")

	# 動態切回 zh_TW
	print("  >> 切回 zh_TW...")
	loc_node.call("set_locale", "zh_TW")
	if not banner.text.begins_with("玩具堆邊緣 · 首通與掃蕩"):
		_fail("切回 zh_TW 後 Banner 未即時還原: " + banner.text)
	if not info.text.begins_with("章節「玩具堆邊緣」"):
		_fail("切回 zh_TW 後 Info 未即時還原: " + info.text)
	if btn_b1.text != expected_btn_first_clear["zh_TW"]:
		_fail("切回 zh_TW 後 BtnFirstClear 未即時還原: " + btn_b1.text)
	if btn_b2.text != expected_btn_sweep["zh_TW"]:
		_fail("切回 zh_TW 後 BtnSweep 未即時還原: " + btn_b2.text)
	if btn_b3.text != expected_btn_sim_regen["zh_TW"]:
		_fail("切回 zh_TW 後 BtnSimRegen 未即時還原: " + btn_b3.text)
	if btn_b4.text != expected_btn_goto_soul["zh_TW"]:
		_fail("切回 zh_TW 後 BtnGotoSoul 未即時還原: " + btn_b4.text)
	if hint.text != expected_hint["zh_TW"]:
		_fail("切回 zh_TW 後 Hint 未即時還原: " + hint.text)
	print("  ✓ [zh_TW] 還原成功")

	hub.queue_free()
