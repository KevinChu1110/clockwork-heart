extends SceneTree
## 發條儲能庫放置收益雙倍領取與獎勵型廣告單元測試 (test_vault_double_claim.gd)
## 依據 docs/BUSINESS.md 變現規範與 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md
## 測試涵蓋：
## 1. DoubleClaimButton 樣式與規範（天藍 #38A0FF、厚底 5px、圓角 18px、字級 18px、零系統 Emoji）
## 2. 0 收益時按鈕 disabled 狀態
## 3. 普通領取 (1x 獎勵、入帳與計時重置)
## 4. 去廣告模式 (has_removed_ads = true) 免廣告直通雙倍領取與提示
## 5. 一般模式 (has_removed_ads = false) 彈出 MockAdDialog，廣告播完發放 2x 雙倍獎勵
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 完整在地化文字檢驗
## 執行指令：godot --path game --headless -s res://scripts/ui/test_vault_double_claim.gd

var _ok: bool = true
var _step: int = 0
var _wait: int = 0
var _dlg: Control = null

const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const ClockworkVaultDialog = preload("res://scripts/ui/clockwork_vault_dialog.gd")
const MockAdDialogScript = preload("res://scripts/ui/mock_ad_dialog.gd")

const FORBIDDEN_CHARS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑", "💰", "📦", "🎁", "📺", "🎬"
]


func _fail(msg: String) -> void:
	push_error("FAIL: " + msg)
	print("  FAIL: ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var gs := root.get_node_or_null("GameState")
	if gs != null:
		if gs.has_method("reset_new_game"):
			gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.gold = 1000
		if "has_removed_ads" in gs:
			gs.has_removed_ads = false

	var inv := root.get_node_or_null("InventorySystem")
	if inv != null and inv.has_method("clear"):
		inv.clear()

	_dlg = ClockworkVaultDialog.new()
	root.add_child(_dlg)


func _process(_delta: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 5:
			return false
		_step = 1

		print("── [1/6] 雙倍領取按鈕 (DoubleClaimButton) 規範檢驗 ──")
		_test_double_claim_button_specs()

		print("── [2/6] 無收益時按鈕禁用狀態測試 ──")
		_test_zero_reward_disabled()

		print("── [3/6] 普通領取 (1x 獎勵) 測試 ──")
		_test_normal_claim()

		print("── [4/6] 去廣告直通雙倍 (has_removed_ads = true) 測試 ──")
		_test_ad_removed_double_claim()

		print("── [5/6] 一般模式觀看廣告完成雙倍領取 (MockAdDialog) 測試 ──")
		_test_watch_ad_double_claim()

		print("── [6/6] 六語系在地化文字完整測試 ──")
		_test_i18n_locales()

		return _finish()
	return false


func _test_double_claim_button_specs() -> void:
	var double_btn: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button
	if double_btn == null:
		_fail("ClockworkVaultDialog 內找不到 DoubleClaimButton")
		return

	# 高度 >= 50px，熱區 >= 48px
	if double_btn.custom_minimum_size.y < 50.0:
		_fail("DoubleClaimButton 高度未達 50px 規範: 實得 %f" % double_btn.custom_minimum_size.y)
	else:
		print("  ✓ DoubleClaimButton 高度達標 (%f >= 50px)" % double_btn.custom_minimum_size.y)

	# 樣式 StyleBoxFlat
	var normal_sb := double_btn.get_theme_stylebox("normal") as StyleBoxFlat
	if normal_sb == null:
		_fail("DoubleClaimButton 缺少 normal StyleBoxFlat")
	else:
		var bg_hex := normal_sb.bg_color.to_html(false).to_upper()
		if bg_hex != "38A0FF":
			_fail("DoubleClaimButton 底色不符: 期望天藍 #38A0FF，實得 #%s" % bg_hex)
		else:
			print("  ✓ DoubleClaimButton 天藍多巴胺色盤合規: #38A0FF")

		var radius := normal_sb.get_corner_radius(CORNER_TOP_LEFT)
		if radius < 16 or radius > 22:
			_fail("DoubleClaimButton 圓角不符: 期望 18px，實得 %dpx" % radius)
		else:
			print("  ✓ DoubleClaimButton 圓角合規: %dpx" % radius)

		var bottom_border := normal_sb.border_width_bottom
		if bottom_border < 4 or bottom_border > 6:
			_fail("DoubleClaimButton 果凍厚底不符: 期望 5px，實得 %dpx" % bottom_border)
		else:
			print("  ✓ DoubleClaimButton 果凍厚底合規: %dpx" % bottom_border)

	# 字級
	var font_sz: int = double_btn.get_theme_font_size("font_size")
	if font_sz < 16:
		_fail("DoubleClaimButton 字級過小: 期望 18px，實得 %d" % font_sz)
	else:
		print("  ✓ DoubleClaimButton 字級合規: %dpx" % font_sz)

	# 零系統 Emoji
	_check_forbidden_symbols(_dlg)
	print("  ✓ 彈窗全節點零系統 Emoji 檢驗通過")


func _test_zero_reward_disabled() -> void:
	# 模擬當前時間等於上次領取時間（收益為 0）
	var now_t := Time.get_unix_time_from_system()
	IdleClockworkVault.set_last_claim_ts(now_t)
	_dlg.call("refresh_display")

	var claim_btn: Button = _dlg.find_child("ClaimButton", true, false) as Button
	var double_btn: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button

	if claim_btn == null or double_btn == null:
		_fail("找不到 ClaimButton 或 DoubleClaimButton")
		return

	if not claim_btn.disabled:
		_fail("無收益時 ClaimButton 應為 disabled")
	if not double_btn.disabled:
		_fail("無收益時 DoubleClaimButton 應為 disabled")

	print("  ✓ 無收益時普通領取與雙倍領取按鈕皆正確為 disabled")


func _test_normal_claim() -> void:
	var gs := root.get_node_or_null("GameState")
	var inv := root.get_node_or_null("InventorySystem")
	var initial_gold: int = gs.gold if gs else 0
	var initial_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	# 模擬累積 2 小時 (基礎收益：金幣 300，鐵屑 6)
	var base_t := Time.get_unix_time_from_system() - 7200.0
	IdleClockworkVault.set_last_claim_ts(base_t)
	_dlg.call("refresh_display")

	var claim_btn: Button = _dlg.find_child("ClaimButton", true, false) as Button
	var double_btn: Button = _dlg.find_child("DoubleClaimButton", true, false) as Button

	if claim_btn.disabled or double_btn.disabled:
		_fail("累積 2 小時收益時按鈕應為可點擊 (disabled = false)")

	# 執行普通領取
	_dlg.call("_on_claim_pressed")

	var after_gold: int = gs.gold if gs else 0
	var after_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	var diff_gold := after_gold - initial_gold
	var diff_scrap := after_scrap - initial_scrap

	if diff_gold != 300:
		_fail("普通領取金幣增加異常: 期望 +300，實得 +%d" % diff_gold)
	if diff_scrap != 6:
		_fail("普通領取鐵屑增加異常: 期望 +6，實得 +%d" % diff_scrap)

	# 領取後計時重置，按鈕應恢復 disabled
	if not claim_btn.disabled or not double_btn.disabled:
		_fail("普通領取後按鈕未恢復 disabled")

	print("  ✓ 普通領取 (1x) 數值結算正確: 金幣 +%d，鐵屑 +%d，計時重置正常" % [diff_gold, diff_scrap])


func _test_ad_removed_double_claim() -> void:
	var gs := root.get_node_or_null("GameState")
	var inv := root.get_node_or_null("InventorySystem")
	if gs:
		gs.has_removed_ads = true

	var initial_gold: int = gs.gold if gs else 0
	var initial_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	# 模擬累積 1 小時 (基礎收益：金幣 150，鐵屑 3；2 倍應為金幣 300，鐵屑 6)
	var base_t := Time.get_unix_time_from_system() - 3600.0
	IdleClockworkVault.set_last_claim_ts(base_t)
	_dlg.call("refresh_display")

	# 點擊雙倍領取
	_dlg.call("_on_double_claim_pressed")

	# 去廣告模式下不應生成 MockAdDialog
	var ad_child = _dlg.find_child("MockAdDialog", true, false)
	if ad_child != null:
		_fail("去廣告模式下不應生成 MockAdDialog")

	var after_gold: int = gs.gold if gs else 0
	var after_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	var diff_gold := after_gold - initial_gold
	var diff_scrap := after_scrap - initial_scrap

	if diff_gold != 300:
		_fail("去廣告直通雙倍金幣結算異常: 期望 2 倍 300，實得 +%d" % diff_gold)
	if diff_scrap != 6:
		_fail("去廣告直通雙倍鐵屑結算異常: 期望 2 倍 6，實得 +%d" % diff_scrap)

	# 提示文字檢驗
	var toast_text: String = str(_dlg.get("last_toast_text"))
	if toast_text.is_empty():
		_fail("去廣告直通雙倍領取時未彈出提示")
	else:
		print("  ✓ 去廣告提示彈窗文字正確: \"%s\"" % toast_text)

	# 還原 has_removed_ads
	if gs:
		gs.has_removed_ads = false

	print("  ✓ 去廣告直通雙倍結算成功: 金幣 +%d (2x)，鐵屑 +%d (2x)" % [diff_gold, diff_scrap])


func _test_watch_ad_double_claim() -> void:
	var gs := root.get_node_or_null("GameState")
	var inv := root.get_node_or_null("InventorySystem")
	if gs:
		gs.has_removed_ads = false

	var initial_gold: int = gs.gold if gs else 0
	var initial_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	# 模擬累積 4 小時 (基礎收益：金幣 600，鐵屑 12；2 倍應為金幣 1200，鐵屑 24)
	var base_t := Time.get_unix_time_from_system() - 14400.0
	IdleClockworkVault.set_last_claim_ts(base_t)
	_dlg.call("refresh_display")

	# 點擊雙倍領取
	_dlg.call("_on_double_claim_pressed")

	# 一般模式下應彈出 MockAdDialog
	var ad_child = _dlg.find_child("MockAdDialog", true, false)
	if ad_child == null:
		_fail("一般模式下點擊雙倍領取未生成 MockAdDialog")
		return

	print("  ✓ 點擊雙倍領取成功觸發 MockAdDialog")

	# 模擬觀看廣告完畢並領取
	if ad_child.has_method("skip_countdown"):
		ad_child.call("skip_countdown")
	if ad_child.has_method("_on_claim_reward"):
		ad_child.call("_on_claim_reward")

	var after_gold: int = gs.gold if gs else 0
	var after_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	var diff_gold := after_gold - initial_gold
	var diff_scrap := after_scrap - initial_scrap

	if diff_gold != 1200:
		_fail("觀看廣告完成雙倍金幣結算異常: 期望 2 倍 1200，實得 +%d" % diff_gold)
	if diff_scrap != 24:
		_fail("觀看廣告完成雙倍鐵屑結算異常: 期望 2 倍 24，實得 +%d" % diff_scrap)

	print("  ✓ 觀看廣告完畢成功獲取雙倍收益: 金幣 +%d (2x)，鐵屑 +%d (2x)" % [diff_gold, diff_scrap])


func _test_i18n_locales() -> void:
	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	var test_locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var required_keys := [
		"vault.btn_double_claim",
		"vault.ad_removed_double"
	]

	for loc in test_locales:
		loc_node.call("set_locale", loc)
		for k in required_keys:
			var translated := str(loc_node.call("t", k))
			if translated.is_empty() or translated == k:
				_fail("語系 %s 缺少在地化 key: %s (翻譯結果為空或回退至key)" % [loc, k])
			else:
				print("    [%s] %s => %s" % [loc, k, translated])

	# 還原繁中
	loc_node.call("set_locale", "zh_TW")
	print("  ✓ 六大語系雙倍領取與去廣告提示在地化文字 100% 齊全")


func _check_forbidden_symbols(node: Node) -> void:
	if node is Label:
		var txt := (node as Label).text
		for c in FORBIDDEN_CHARS:
			if c in txt:
				_fail("節點 %s 包含禁止符號/Emoji: %s (文字: %s)" % [node.name, c, txt])
	elif node is Button:
		var txt := (node as Button).text
		for c in FORBIDDEN_CHARS:
			if c in txt:
				_fail("按鈕 %s 包含禁止符號/Emoji: %s (文字: %s)" % [node.name, c, txt])

	for ch in node.get_children():
		_check_forbidden_symbols(ch)


func _finish() -> bool:
	if _ok:
		print("VAULT_DOUBLE_CLAIM_TEST_OK")
		quit(0)
	else:
		print("VAULT_DOUBLE_CLAIM_TEST_FAIL")
		quit(1)
	return true
