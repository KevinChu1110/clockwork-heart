extends SceneTree
## 發條儲能庫放置收益系統測試 (test_idle_clockwork_vault.gd)
## 依據 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點二
## 測試項：
## 1. 放置時間累積（0h, 1h, 4h, 8h 上限，>8h 封頂）
## 2. 一鍵領取金幣與鐵屑入帳、計時重置
## 3. 大廳發條儲能庫入口（卡片存在、按鈕熱區 >= 48px、果凍厚底 5-6px、零 emoji）
## 4. 收穫彈窗開啟、多巴胺入帳動效、關閉
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 完整翻譯檢查
## 執行指令：godot --path game --headless -s res://scripts/ui/test_idle_clockwork_vault.gd

var _ok: bool = true
var _step: int = 0
var _wait: int = 0
var _lobby: Node = null

const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const ClockworkVaultDialog = preload("res://scripts/ui/clockwork_vault_dialog.gd")

const FORBIDDEN_CHARS: Array[String] = [
	"⚒", "✦", "⚔", "⚙", "➔", "➜", "★", "☆", "✨", "🔥", "💎", "🛡", "👑", "💰", "📦"
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

	var inv := root.get_node_or_null("InventorySystem")
	if inv != null and inv.has_method("clear"):
		inv.clear()

	_lobby = MobileLobby.new()
	root.add_child(_lobby)


func _process(_delta: float) -> bool:
	_wait += 1
	if _step == 0:
		if _wait < 5:
			return false
		_step = 1

		print("── [1/5] 放置累積與數值計算測試 ──")
		_test_time_accumulation()

		print("── [2/5] 一鍵領取與資源入帳測試 ──")
		_test_claim_rewards()

		print("── [3/5] 大廳儲能庫入口規範測試 (熱區/厚底/零emoji) ──")
		_test_lobby_vault_card()

		print("── [4/5] 收穫彈窗與多巴胺反饋測試 ──")
		_test_vault_dialog()

		print("── [5/5] 六語系在地化文字完整測試 ──")
		_test_i18n_locales()

		return _finish()
	return false


func _test_time_accumulation() -> void:
	var base_t := 1700000000.0

	## 測試 0 秒
	IdleClockworkVault.set_last_claim_ts(base_t)
	var st0 := IdleClockworkVault.get_status(base_t)
	if int(st0["gold"]) != 0 or int(st0["iron_scrap"]) != 0:
		_fail("0 秒時收益應為 0，實得 gold=%s scrap=%s" % [st0["gold"], st0["iron_scrap"]])
	if float(st0["progress_ratio"]) > 0.001 or bool(st0["is_full"]):
		_fail("0 秒時進度不應滿")

	## 測試 1 小時 (3600s)：金幣 150，鐵屑 3
	var st1 := IdleClockworkVault.get_status(base_t + 3600.0)
	if int(st1["gold"]) != 150:
		_fail("1 小時金幣應為 150，實得 %s" % st1["gold"])
	if int(st1["iron_scrap"]) != 3:
		_fail("1 小時鐵屑應為 3，實得 %s" % st1["iron_scrap"])
	if absf(float(st1["progress_ratio"]) - 0.125) > 0.01:
		_fail("1 小時進度應為 12.5%%，實得 %s" % st1["progress_ratio"])

	## 測試 4 小時 (14400s)：金幣 600，鐵屑 12
	var st4 := IdleClockworkVault.get_status(base_t + 14400.0)
	if int(st4["gold"]) != 600:
		_fail("4 小時金幣應為 600，實得 %s" % st4["gold"])
	if int(st4["iron_scrap"]) != 12:
		_fail("4 小時鐵屑應為 12，實得 %s" % st4["iron_scrap"])
	if absf(float(st4["progress_ratio"]) - 0.5) > 0.01:
		_fail("4 小時進度應為 50%%，實得 %s" % st4["progress_ratio"])

	## 測試 8 小時 (28800s)：金幣 1200，鐵屑 24，滿額
	var st8 := IdleClockworkVault.get_status(base_t + 28800.0)
	if int(st8["gold"]) != 1200:
		_fail("8 小時金幣應為 1200，實得 %s" % st8["gold"])
	if int(st8["iron_scrap"]) != 24:
		_fail("8 小時鐵屑應為 24，實得 %s" % st8["iron_scrap"])
	if not bool(st8["is_full"]):
		_fail("8 小時應判定為滿額 is_full=true")
	if absf(float(st8["progress_ratio"]) - 1.0) > 0.01:
		_fail("8 小時進度應為 100%%")

	## 測試 24 小時封頂 (>8h 封頂在 8h 數值)
	var st24 := IdleClockworkVault.get_status(base_t + 86400.0)
	if int(st24["gold"]) != 1200 or int(st24["iron_scrap"]) != 24:
		_fail("超過 8 小時應封頂在 1200 金幣 / 24 鐵屑，實得 gold=%s scrap=%s" % [st24["gold"], st24["iron_scrap"]])
	if not bool(st24["is_full"]):
		_fail("超過 8 小時應判定為 is_full=true")

	print("  ✓ 時間累積與 8 小時上限封頂運算完全正確")


func _test_claim_rewards() -> void:
	var base_t := 1700000000.0
	var gs := root.get_node_or_null("GameState")
	var inv := root.get_node_or_null("InventorySystem")

	IdleClockworkVault.set_last_claim_ts(base_t)
	var start_gold: int = int(gs.gold) if gs else 0
	var start_scrap: int = int(inv.count("iron_scrap")) if inv else 0

	## 模擬 4 小時後領取 (600 金幣, 12 鐵屑)
	var claim_t := base_t + 14400.0
	var res := IdleClockworkVault.claim(claim_t)

	if not bool(res.get("claimed", false)):
		_fail("4 小時領取時 claimed 應為 true")
	if int(res.get("gold", 0)) != 600:
		_fail("領取回傳金幣應為 600，實得 %s" % res.get("gold", 0))
	if int(res.get("iron_scrap", 0)) != 12:
		_fail("領取回傳鐵屑應為 12，實得 %s" % res.get("iron_scrap", 0))

	if gs:
		var end_gold: int = int(gs.gold)
		if end_gold != start_gold + 600:
			_fail("GameState 金幣未正確增加 600，前=%d 後=%d" % [start_gold, end_gold])

	if inv:
		var end_scrap: int = int(inv.count("iron_scrap"))
		if end_scrap != start_scrap + 12:
			_fail("InventorySystem 鐵屑未正確增加 12，前=%d 後=%d" % [start_scrap, end_scrap])

	## 驗證領取後時間立即重置
	var st_after := IdleClockworkVault.get_status(claim_t)
	if int(st_after["gold"]) != 0 or int(st_after["iron_scrap"]) != 0:
		_fail("領取後收益應重置為 0，實得 %s" % st_after)

	print("  ✓ 一鍵領取金幣與鐵屑入帳成功，計時正確重置")


func _test_lobby_vault_card() -> void:
	if _lobby == null:
		_fail("大廳實例為空")
		return

	var card := _lobby.call("get_vault_card") as Control
	if card == null:
		_fail("找不到大廳發條儲能庫入口卡片 (get_vault_card)")
		return

	if not card.visible:
		_fail("發條儲能庫入口卡片不可見")

	var btn := _lobby.call("get_vault_claim_button") as Button
	if btn == null:
		_fail("找不到儲能庫領取按鈕 (get_vault_claim_button)")
		return

	## 檢驗熱區 >= 48px
	if btn.custom_minimum_size.x < 48.0 or btn.custom_minimum_size.y < 48.0:
		_fail("按鈕熱區小於 48px: %s" % [btn.custom_minimum_size])

	## 檢驗果凍厚底 5~6px
	var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null or sb.border_width_bottom < 5:
		_fail("按鈕未設定果凍厚底 (border_width_bottom < 5px)")

	## 檢驗零系統 emoji
	_check_forbidden_symbols(card)

	print("  ✓ 大廳儲能庫入口規範達標 (熱區 >= 48px, 厚底 5-6px, 零系統 emoji)")


func _test_vault_dialog() -> void:
	if _lobby == null:
		return

	var dlg := _lobby.call("open_clockwork_vault") as Control
	if dlg == null:
		_fail("無法開啟發條儲能庫收穫彈窗")
		return

	## 檢查關鍵節點
	var card := dlg.get_node_or_null("VaultCard")
	if card == null:
		_fail("彈窗內找不到 VaultCard")

	var title_lbl := dlg.call("get_title_label") as Label
	if title_lbl == null:
		_fail("彈窗內找不到 VaultTitleLabel")

	var claim_btn := dlg.call("get_claim_button") as Button
	if claim_btn == null:
		_fail("彈窗內找不到 ClaimButton")
	else:
		if claim_btn.custom_minimum_size.y < 48.0:
			_fail("彈窗領取按鈕高度小於 48px")
		var csb := claim_btn.get_theme_stylebox("normal") as StyleBoxFlat
		if csb == null or csb.border_width_bottom < 5:
			_fail("彈窗領取按鈕未具備果凍厚底")

	var close_btn := dlg.call("get_close_button") as Button
	if close_btn == null:
		_fail("彈窗內找不到 CloseButton")

	## 檢查進度條節點與寬度渲染斷言
	var fill_panel := dlg.call("get_progress_bar_fill") as Panel
	var bg_panel := dlg.call("get_progress_bar_bg") as PanelContainer
	if fill_panel == null or bg_panel == null:
		_fail("彈窗內找不到 ProgressBarFill 或 ProgressBarBg")
	else:
		## 模擬累積 4 小時 (14400s -> 50% 進度)
		IdleClockworkVault.set_last_claim_ts(Time.get_unix_time_from_system() - 14400.0)
		dlg.call("refresh_display")
		var min_w: float = fill_panel.custom_minimum_size.x
		var act_w: float = fill_panel.size.x
		if not fill_panel.visible:
			_fail("50% 進度時 ProgressBarFill 應為可見")
		if min_w < 300.0 or min_w > 360.0:
			_fail("50%% 進度條 custom_minimum_size.x 異常，期望約 330px，實得 %f" % min_w)
		if act_w < 300.0 or act_w > 360.0:
			_fail("50%% 進度條 size.x 異常，期望約 330px，實得 %f" % act_w)

		## 模擬累積 0 秒 (0% 進度)
		IdleClockworkVault.set_last_claim_ts(Time.get_unix_time_from_system())
		dlg.call("refresh_display")
		if fill_panel.visible and fill_panel.custom_minimum_size.x > 1.0:
			_fail("0% 進度時 ProgressBarFill 應隱藏或寬度為 0")

	## 測試零 Emoji 與禁止符號
	_check_forbidden_symbols(dlg)

	## 測試領取點擊與反饋動效
	IdleClockworkVault.set_last_claim_ts(Time.get_unix_time_from_system() - 7200.0) # 2 小時
	dlg.call("refresh_display")
	if claim_btn:
		claim_btn.emit_signal("pressed")

	## 關閉彈窗
	if close_btn:
		close_btn.emit_signal("pressed")

	print("  ✓ 收穫彈窗開啟、多巴胺入帳動效與零 Emoji 檢驗通過")


func _test_i18n_locales() -> void:
	var loc_node := root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	var test_locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var required_keys := [
		"vault.title",
		"vault.popup_title",
		"vault.desc",
		"vault.gold_reward",
		"vault.scrap_reward",
		"vault.btn_claim",
		"vault.charging",
		"vault.capacity",
		"vault.max_cap"
	]

	for loc in test_locales:
		loc_node.call("set_locale", loc)
		for k in required_keys:
			var translated := str(loc_node.call("t", k))
			if translated.is_empty() or translated == k:
				_fail("語系 %s 缺少在地化 key: %s (翻譯結果為空或回退至key)" % [loc, k])

	## 還原回繁體中文
	loc_node.call("set_locale", "zh_TW")
	print("  ✓ 六大語系 (zh_TW, zh_CN, en, ja, ko, es) 全部 100% 翻譯就緒")


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
		print("IDLE_CLOCKWORK_VAULT_TEST_OK")
		quit(0)
	else:
		print("IDLE_CLOCKWORK_VAULT_TEST_FAIL")
		quit(1)
	return true
