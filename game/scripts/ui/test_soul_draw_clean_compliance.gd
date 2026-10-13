extends SceneTree
## 聚魂召喚系統（soul_draw）清除特殊符號『✦』殘留與合規對齊單元測試
## (res://scripts/ui/test_soul_draw_clean_compliance.gd)
##
## 驗證項目：
## 1. soul_ten_pull_view.gd、soul_summon_fx.gd 與 soul_result_card_view.gd 徹底清除『✦』與星星符號。
## 2. 標題與引導文字改為純淨文本（『封靈連轉結果』、『發條解鎖 · 聚魂召喚』），星級展示對齊官方品質色階純文字階級。
## 3. 六語系 (zh_TW, zh_CN, en, ja, ko, es) ui.json 與語言字典無特殊符號殘留，即時刷新切換完全合規。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const SoulTenPullView := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")
const SoulSummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const SoulResultCardView := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")

const FORBIDDEN_SYMBOLS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑"
]

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_forbidden(text: String) -> bool:
	for sym in FORBIDDEN_SYMBOLS:
		if text.find(sym) >= 0:
			return true
	return false


func _assert_no_forbidden_in_tree(node: Node, context: String) -> void:
	if node is Label:
		var lbl := node as Label
		if _has_forbidden(lbl.text):
			_fail("%s 標籤 '%s' 含有違規特殊字符: '%s'" % [context, lbl.name, lbl.text])
	elif node is Button:
		var btn := node as Button
		if _has_forbidden(btn.text):
			_fail("%s 按鈕 '%s' 含有違規特殊字符: '%s'" % [context, btn.name, btn.text])
	for child in node.get_children():
		_assert_no_forbidden_in_tree(child, context)


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
				_run_all_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_SOUL_DRAW_CLEAN_COMPLIANCE_OK")
					quit(0)
				else:
					push_error("TEST_SOUL_DRAW_CLEAN_COMPLIANCE_FAIL")
					print("TEST_SOUL_DRAW_CLEAN_COMPLIANCE_FAIL")
					quit(1)
				return true
	return false


func _run_all_tests() -> void:
	print("=== 開始 test_soul_draw_clean_compliance 驗收測試 ===")

	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	# ──────────────────────────────────────────────────────────────────────────
	# 測試 1：驗證六語系詞條定義中無『✦』且符合純淨文本規範
	# ──────────────────────────────────────────────────────────────────────────
	print("\n--- 1. 驗證六語系字典詞條符合純淨文本且零特殊符號 ---")
	var expected_ten_pull_title := {
		"zh_TW": "封靈連轉結果",
		"zh_CN": "封灵连转结果",
		"en": "Ten Pull Results",
		"ja": "連続召喚結果",
		"ko": "10연속 소환 결과",
		"es": "Resultados de 10 Extracciones",
	}
	var expected_summon_hint := {
		"zh_TW": "發條解鎖 · 聚魂召喚",
		"zh_CN": "发条解锁 · 聚魂召唤",
		"en": "Clockwork Unlock · Soul Summon",
		"ja": "ゼンマイ解錠・魂集め召喚",
		"ko": "태엽 해제 · 집혼 소환",
		"es": "Desbloqueo de Cuerda · Invocación de Almas",
	}
	var expected_skip_btn := {
		"zh_TW": "跳過",
		"zh_CN": "跳过",
		"en": "Skip",
		"ja": "スキップ",
		"ko": "건너뛰기",
		"es": "Saltar",
	}

	for code in LOCALES:
		loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "封靈連轉結果")
		if t_title != expected_ten_pull_title[code]:
			_fail("[%s] 詞條 '封靈連轉結果' 預期 '%s' 實得 '%s'" % [code, expected_ten_pull_title[code], t_title])
		if _has_forbidden(t_title):
			_fail("[%s] 詞條 '封靈連轉結果' 含有違規字符: %s" % [code, t_title])
		print("  ✓ [%s] 封靈連轉結果: %s" % [code, t_title])

		var t_hint := ContentLoc.text("ui", "發條解鎖 · 聚魂召喚")
		if t_hint != expected_summon_hint[code]:
			_fail("[%s] 詞條 '發條解鎖 · 聚魂召喚' 預期 '%s' 實得 '%s'" % [code, expected_summon_hint[code], t_hint])
		if _has_forbidden(t_hint):
			_fail("[%s] 詞條 '發條解鎖 · 聚魂召喚' 含有違規字符: %s" % [code, t_hint])
		print("  ✓ [%s] 發條解鎖 · 聚魂召喚: %s" % [code, t_hint])

		var t_skip := ContentLoc.text("ui", "跳過")
		if t_skip != expected_skip_btn[code]:
			_fail("[%s] 詞條 '跳過' 預期 '%s' 實得 '%s'" % [code, expected_skip_btn[code], t_skip])
		if _has_forbidden(t_skip):
			_fail("[%s] 詞條 '跳過' 含有違規字符: %s" % [code, t_skip])

	# ──────────────────────────────────────────────────────────────────────────
	# 測試 2：測試 SoulTenPullView（十連抽面板）純淨標題與純文字色階
	# ──────────────────────────────────────────────────────────────────────────
	print("\n--- 2. 測試 SoulTenPullView 十連抽面板 UI 與純文字階級 ---")
	loc_node.call("set_locale", "zh_TW")
	var ten_view := SoulTenPullView.new()
	root.add_child(ten_view)

	var title_lbl: Label = ten_view.get("_title_lbl")
	if title_lbl == null:
		_fail("SoulTenPullView 缺少 _title_lbl")
	else:
		if title_lbl.text != "封靈連轉結果":
			_fail("SoulTenPullView 預設標題應為 '封靈連轉結果'，實際為: '%s'" % title_lbl.text)
		if _has_forbidden(title_lbl.text):
			_fail("SoulTenPullView 標題含有違規字符: '%s'" % title_lbl.text)
		print("  ✓ SoulTenPullView 標題純淨無特殊符號: ", title_lbl.text)

	# 檢驗 TIER_COLORS 內部星星定義已完全清空
	for tier_k in SoulTenPullView.TIER_COLORS.keys():
		var t_data: Dictionary = SoulTenPullView.TIER_COLORS[tier_k]
		var stars_str: String = str(t_data.get("stars", ""))
		if stars_str != "":
			_fail("SoulTenPullView.TIER_COLORS['%s']['stars'] 應為空字串，實際為: '%s'" % [tier_k, stars_str])

	# 測試六語系切換時標題即時連動
	for code in LOCALES:
		loc_node.call("set_locale", code)
		if title_lbl and title_lbl.text != expected_ten_pull_title[code]:
			_fail("[%s] SoulTenPullView 標題即時刷新錯誤: 預期 '%s' 實得 '%s'" % [code, expected_ten_pull_title[code], title_lbl.text])
		_assert_no_forbidden_in_tree(ten_view, "SoulTenPullView [%s]" % code)

	# 測試展示多種品質色階掉落卡
	var mock_drops: Array[Dictionary] = [
		{"kind": "junk", "DropId": "junk_enamel_chip"},     # white: 普通
		{"kind": "part", "DropId": "drop_brass_gear"},      # orange: 優良
		{"kind": "part", "DropId": "drop_spring_coil"},     # blue: 稀有
		{"kind": "outfit", "DropId": "outfit_cream"},        # purple: 史詩
		{"kind": "part", "DropId": "drop_core_shard"},      # gold: 傳奇
		{"kind": "outfit", "DropId": "outfit_brass_vest"},  # purple: 史詩
		{"kind": "outfit", "DropId": "outfit_scarf_tunic"}, # purple: 史詩
		{"kind": "outfit", "DropId": "outfit_worker_apron"},# purple: 史詩
		{"kind": "part", "DropId": "drop_brass_gear"},      # orange: 優良
		{"kind": "part", "DropId": "drop_spring_coil"},     # blue: 稀有
	]
	ten_view.show_drops(mock_drops)
	var cards: Array = ten_view.get("_cards")
	if cards.size() != 10:
		_fail("show_drops 產生的卡片數量應為 10，實際為: %d" % cards.size())
	else:
		print("  ✓ show_drops 成功建立 10 張卡片，檢查各卡頂部純文字階級與零特殊字符")
		for i in range(cards.size()):
			var c: Control = cards[i]
			_assert_no_forbidden_in_tree(c, "MiniCard #%d" % i)

	ten_view.queue_free()

	# ──────────────────────────────────────────────────────────────────────────
	# 測試 3：測試 SoulSummonFx（召喚動效儀式）標題提示與跳過按鈕
	# ──────────────────────────────────────────────────────────────────────────
	print("\n--- 3. 測試 SoulSummonFx 召喚動效提示與按鈕純淨文字 ---")
	loc_node.call("set_locale", "zh_TW")
	var fx := SoulSummonFx.new()
	root.add_child(fx)

	var fx_title: Label = fx.get("_title_hint")
	var fx_skip: Button = fx.get("_skip_btn")
	if fx_title == null or fx_skip == null:
		_fail("SoulSummonFx 缺少 _title_hint 或 _skip_btn")
	else:
		if fx_title.text != "發條解鎖 · 聚魂召喚":
			_fail("SoulSummonFx 提示標題應為 '發條解鎖 · 聚魂召喚'，實際為: '%s'" % fx_title.text)
		if fx_skip.text != "跳過":
			_fail("SoulSummonFx 跳過按鈕應為 '跳過'，實際為: '%s'" % fx_skip.text)
		_assert_no_forbidden_in_tree(fx, "SoulSummonFx [zh_TW]")
		print("  ✓ SoulSummonFx 提示標題與跳過按鈕純淨無特殊字符")

	# 測試六語系即時切換連動
	for code in LOCALES:
		loc_node.call("set_locale", code)
		if fx_title and fx_title.text != expected_summon_hint[code]:
			_fail("[%s] SoulSummonFx 標題即時刷新錯誤: 預期 '%s' 實得 '%s'" % [code, expected_summon_hint[code], fx_title.text])
		if fx_skip and fx_skip.text != expected_skip_btn[code]:
			_fail("[%s] SoulSummonFx 跳過按鈕即時刷新錯誤: 預期 '%s' 實得 '%s'" % [code, expected_skip_btn[code], fx_skip.text])
		_assert_no_forbidden_in_tree(fx, "SoulSummonFx [%s]" % code)

	fx.queue_free()

	# ──────────────────────────────────────────────────────────────────────────
	# 測試 4：測試 SoulResultCardView（單抽結果卡）純文字階級展示
	# ──────────────────────────────────────────────────────────────────────────
	print("\n--- 4. 測試 SoulResultCardView 單抽結果卡純文字階級展示 ---")
	loc_node.call("set_locale", "zh_TW")
	var card := SoulResultCardView.new()
	root.add_child(card)

	# 檢驗 TIER_COLORS 內部星星定義已完全清空
	for tier_k in SoulResultCardView.TIER_COLORS.keys():
		var t_data: Dictionary = SoulResultCardView.TIER_COLORS[tier_k]
		var stars_str: String = str(t_data.get("stars", ""))
		if stars_str != "":
			_fail("SoulResultCardView.TIER_COLORS['%s']['stars'] 應為空字串，實際為: '%s'" % [tier_k, stars_str])

	# 檢驗 placeholder 狀態無 『✦』
	card.show_placeholder()
	var stars_lbl: Label = card.get("_stars_lbl")
	if stars_lbl == null:
		_fail("SoulResultCardView 缺少 _stars_lbl")
	else:
		if stars_lbl.text != "傳奇":
			_fail("SoulResultCardView placeholder 星級標籤應為純文字 '傳奇'，實際為: '%s'" % stars_lbl.text)
		if _has_forbidden(stars_lbl.text):
			_fail("SoulResultCardView placeholder 星級含有違規符號: '%s'" % stars_lbl.text)
		print("  ✓ placeholder 星級標籤正確呈現純文字: ", stars_lbl.text)

	# 檢驗各種品質 drop 之純文字階級展示
	var single_test_drops := [
		{"drop": {"kind": "junk", "DropId": "junk_enamel_chip"}, "expected_tier": "普通"},
		{"drop": {"kind": "part", "DropId": "drop_brass_gear"}, "expected_tier": "優良"},
		{"drop": {"kind": "part", "DropId": "drop_spring_coil"}, "expected_tier": "稀有"},
		{"drop": {"kind": "outfit", "DropId": "outfit_cream"}, "expected_tier": "史詩"},
		{"drop": {"kind": "part", "DropId": "drop_core_shard"}, "expected_tier": "傳奇"},
	]

	for item in single_test_drops:
		var d: Dictionary = item["drop"]
		var exp_t: String = item["expected_tier"]
		card.show_drop(d)
		if stars_lbl.text != exp_t:
			_fail("Drop %s 階級標籤預期為 '%s'，實際為: '%s'" % [d.DropId, exp_t, stars_lbl.text])
		if _has_forbidden(stars_lbl.text):
			_fail("Drop %s 階級標籤含有違規符號: '%s'" % [d.DropId, stars_lbl.text])
		_assert_no_forbidden_in_tree(card, "SoulResultCard [%s]" % d.DropId)
		print("  ✓ Drop %s 正確顯示純文字階級: %s" % [d.DropId, stars_lbl.text])

	card.queue_free()
	print("✓ 所有聚魂召喚特殊字符清除與純文字階級展示斷言全數通過！")
