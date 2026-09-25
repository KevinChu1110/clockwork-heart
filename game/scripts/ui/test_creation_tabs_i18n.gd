extends SceneTree
## 創角分頁與確認鈕六語系單元測試 (Creation Tabs i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含「首發」、「擴充」、「確認選擇 · 踏上旅途」、「返回」對應翻譯。
## 2. 創角介面在六語系切換下，頂部分頁與底部確認／返回鈕即時連動刷新。
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字精確度。

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
			print("CREATION_TABS_I18N_OK")
			quit(0)
		else:
			push_error("CREATION_TABS_I18N_FAIL")
			print("CREATION_TABS_I18N_FAIL")
			quit(1)
		return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_creation_tabs_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證詞條字典解析
	var expected_launch := {
		"zh_TW": "首發",
		"zh_CN": "首发",
		"en": "Launch",
		"ja": "初期",
		"ko": "초기",
		"es": "Lanzamiento"
	}
	var expected_expansion := {
		"zh_TW": "擴充",
		"zh_CN": "扩充",
		"en": "Expansion",
		"ja": "拡張",
		"ko": "확장",
		"es": "Expansión"
	}
	var expected_confirm := {
		"zh_TW": "確認選擇 · 踏上旅途",
		"zh_CN": "确认选择 · 踏上旅途",
		"en": "Confirm Selection · Begin Journey",
		"ja": "選択確認 · 旅立ち",
		"ko": "선택 확인 · 여정 시작",
		"es": "Confirmar Selección · Emprender el Viaje"
	}
	var expected_back := {
		"zh_TW": "返回",
		"zh_CN": "返回",
		"en": "Back",
		"ja": "戻る",
		"ko": "돌아가기",
		"es": "Volver"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		var t_launch := ContentLoc.text("ui", "首發")
		if t_launch != expected_launch[code]:
			_fail("語系 [%s] 首發 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_launch[code], t_launch])
		else:
			print("  ✓ [%s] 首發 -> %s" % [code, t_launch])

		var t_exp := ContentLoc.text("ui", "擴充")
		if t_exp != expected_expansion[code]:
			_fail("語系 [%s] 擴充 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_expansion[code], t_exp])
		else:
			print("  ✓ [%s] 擴充 -> %s" % [code, t_exp])

		var t_conf := ContentLoc.text("ui", "確認選擇 · 踏上旅途")
		if t_conf != expected_confirm[code]:
			_fail("語系 [%s] 確認選擇 · 踏上旅途 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_confirm[code], t_conf])
		else:
			print("  ✓ [%s] 確認選擇 · 踏上旅途 -> %s" % [code, t_conf])

		var t_back := ContentLoc.text("ui", "返回")
		if t_back != expected_back[code]:
			_fail("語系 [%s] 返回 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_back[code], t_back])
		else:
			print("  ✓ [%s] 返回 -> %s" % [code, t_back])

	# 2. 驗證節點實例化與動態即時切換
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root_node.add_child(demo)

	var btn_launch = demo.get_node_or_null("RaceTabBar/BtnTab_launch") as Button
	var btn_expansion = demo.get_node_or_null("RaceTabBar/BtnTab_expansion") as Button
	var btn_confirm = demo.get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnConfirm") as Button
	var btn_back = demo.get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnBack") as Button

	if btn_launch == null or btn_expansion == null:
		_fail("無法取得 RaceTabBar 按鈕節點")
	if btn_confirm == null or btn_back == null:
		_fail("無法取得 ActionsRow 按鈕節點")

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		if btn_launch and btn_launch.text != expected_launch[code]:
			_fail("[%s] 首發 tab 文字未即時更新: 期望 '%s'，實際 '%s'" % [code, expected_launch[code], btn_launch.text])
		if btn_expansion and btn_expansion.text != expected_expansion[code]:
			_fail("[%s] 擴充 tab 文字未即時更新: 期望 '%s'，實際 '%s'" % [code, expected_expansion[code], btn_expansion.text])
		if btn_confirm and btn_confirm.text != expected_confirm[code]:
			_fail("[%s] 確認按鈕文字未即時更新: 期望 '%s'，實際 '%s'" % [code, expected_confirm[code], btn_confirm.text])
		if btn_back and btn_back.text != expected_back[code]:
			_fail("[%s] 返回按鈕文字未即時更新: 期望 '%s'，實際 '%s'" % [code, expected_back[code], btn_back.text])

		print("  ✓ [%s] 創角分頁與按鈕即時更新驗證通過" % code)

	# 3. 驗證在非 zh_TW 下 switch_tab 支援
	demo.call("switch_tab", "expansion")
	if demo.call("get_current_tab") != "expansion":
		_fail("switch_tab expansion 失敗")
	demo.call("switch_tab", "launch")
	if demo.call("get_current_tab") != "launch":
		_fail("switch_tab launch 失敗")

	demo.queue_free()

	# 切回預設 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
