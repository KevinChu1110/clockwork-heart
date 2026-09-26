extends SceneTree
## 停擺巨偶每日次數與出征入口骨架單元測試 (test_colossus_daily.gd)
## 驗證：
## 1. 停擺巨偶三張占位卡（失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏑蒸汽巨象 Lv28，無第四隻）
## 2. 每日初始次數為 3
## 3. 同一天內呼叫 3 次後第 4 次被拒
## 4. 跨日重置（改 debug_day 隔日後次數回到 3）
## 5. 硬限制：嚴禁改動 ATB / 攻速 / 前搖 / 命中等時間模型常數
## 6. 六語系鍵值與零系統 Emoji 檢查
## 7. 大廳出征分頁子模式切換與熱區 >= 48px

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FormulasClass = preload("res://scripts/battle/formulas.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _wait := 0
var _lobby: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_colossus_daily 測試 ===")
	root.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	var cds = root.get_node_or_null("ColossusDailySystem")
	if gs == null or cds == null:
		_fail("缺少必要 Autoload: GameState=%s, ColossusDailySystem=%s" % [gs, cds])
		print("TEST_COLOSSUS_DAILY_FAIL")
		quit(1)
		return

	gs.reset_new_game()
	cds.debug_day = 20260927
	cds.refresh()

	# --- 1. 檢驗三隻巨偶占位資料 ---
	print("--- 1. 檢驗三隻停擺巨偶占位資料 ---")
	var bosses: Array = cds.get_bosses()
	if bosses.size() != 3:
		_fail("巨偶數量應為 3，實際為 %d（不准自創第四隻）" % bosses.size())
	var expected_bosses := [
		{"name": "失控發條獅", "level": 12},
		{"name": "霧鐘提線人偶", "level": 20},
		{"name": "黑鏑蒸汽巨象", "level": 28},
	]
	for i in range(expected_bosses.size()):
		var b: Dictionary = bosses[i]
		if str(b.get("name", "")) != str(expected_bosses[i]["name"]):
			_fail("巨偶 %d 名稱不符：預期 %s，實際 %s" % [i, expected_bosses[i]["name"], b.get("name")])
		if int(b.get("level", 0)) != int(expected_bosses[i]["level"]):
			_fail("巨偶 %d 等級不符：預期 Lv%d，實際 Lv%d" % [i, expected_bosses[i]["level"], b.get("level")])
		if int(b.get("cost", -1)) != 0:
			_fail("巨偶 %d 本期不應消耗體力/能量（cost 應為 0）" % i)
	print("  ✓ 三隻停擺巨偶資料完全符合規範")

	# --- 2. 檢驗每日次數限制與同日第 4 次被拒 ---
	print("--- 2. 檢驗每日次數限制與同日第 4 次被拒 ---")
	gs.reset_new_game()
	cds.debug_day = 20260927
	cds.refresh()

	if cds.get_remaining_entries() != 3:
		_fail("初始剩餘次數應為 3，實際為 %d" % cds.get_remaining_entries())

	var r1 = cds.try_enter("colossus_lion")
	if not bool(r1.get("ok", false)) or int(r1.get("remaining", -1)) != 2:
		_fail("第 1 次嘗試應成功且剩餘 2，實際 %s" % str(r1))

	var r2 = cds.try_enter("colossus_puppet")
	if not bool(r2.get("ok", false)) or int(r2.get("remaining", -1)) != 1:
		_fail("第 2 次嘗試應成功且剩餘 1，實際 %s" % str(r2))

	var r3 = cds.try_enter("colossus_elephant")
	if not bool(r3.get("ok", false)) or int(r3.get("remaining", -1)) != 0:
		_fail("第 3 次嘗試應成功且剩餘 0，實際 %s" % str(r3))

	if cds.get_remaining_entries() != 0:
		_fail("3 次使用後剩餘次數應為 0，實際為 %d" % cds.get_remaining_entries())

	var r4 = cds.try_enter("colossus_lion")
	if bool(r4.get("ok", true)):
		_fail("第 4 次嘗試應被拒絕，實際回傳成功！")
	if str(r4.get("reason", "")) != "daily_limit_reached":
		_fail("第 4 次被拒理由應為 daily_limit_reached，實際為 %s" % str(r4.get("reason")))
	print("  ✓ 同日滿 3 次後第 4 次成功被拒")

	# --- 3. 檢驗換日重置 ---
	print("--- 3. 檢驗換日自動回到 3 次 ---")
	cds.debug_day = 20260928  # 模擬隔天
	cds.refresh()

	if cds.get_remaining_entries() != 3:
		_fail("換日後次數應自動回到 3，實際為 %d" % cds.get_remaining_entries())

	var r_next = cds.try_enter("colossus_lion")
	if not bool(r_next.get("ok", false)) or int(r_next.get("remaining", -1)) != 2:
		_fail("換日後應可正常入場，實際 %s" % str(r_next))
	print("  ✓ 換日自動重置至 3 次成功")

	# --- 4. 檢驗硬限制：嚴禁改動 ATB / 攻速 / 前搖 / 命中等時間模型常數 ---
	print("--- 4. 檢驗硬限制：ATB / 攻速時間模型常數鎖定 ---")
	if not cds.verify_time_model_locked():
		_fail("時間模型驗證失敗：ATB、攻速或前搖常數遭到非預期修改！")
	var atb_max: float = float(FormulasClass.atb_max())
	var strike_dur: float = float(FormulasClass.strike_duration())
	var telegraph_sec: float = float(FormulasClass.boss_telegraph_sec())
	var parry_win: float = float(FormulasClass.boss_parry_window_sec())
	var grace_sec: float = float(FormulasClass.parry_early_grace_sec())
	if absf(atb_max - 100.0) > 0.001 or absf(strike_dur - 0.08) > 0.001:
		_fail("時間模型數值偏移：atb_max=%f, strike_dur=%f" % [atb_max, strike_dur])
	if absf(telegraph_sec - 1.85) > 0.001 or absf(parry_win - 0.85) > 0.001 or absf(grace_sec - 0.35) > 0.001:
		_fail("Boss 動作時間窗口偏移：telegraph=%f, parry=%f, grace=%f" % [telegraph_sec, parry_win, grace_sec])
	print("  ✓ 硬限制常數防護驗證通過：ATB 與攻速常數 0 漂移")

	# --- 5. 檢驗六語系鍵值與零 Emoji ---
	print("--- 5. 檢驗六語系字典映射與零系統 Emoji ---")
	var check_keys := [
		"停擺巨偶",
		"失控發條獅",
		"霧鐘提線人偶",
		"黑鏑蒸汽巨象",
		"明天再來",
		"四區主線",
		"停擺巨偶 · 今日剩餘: %d/3",
		"今日挑戰次數已用盡，請明天再來！",
	]
	var loc_node: Node = root.get_node_or_null("Loc")
	for loc in LOCALES:
		if loc_node and loc_node.has_method("set_locale"):
			loc_node.call("set_locale", loc)
		for k in check_keys:
			var localized := ContentLoc.text("ui", k)
			if localized.is_empty():
				_fail("[%s] 缺少詞條翻譯：%s" % [loc, k])
			for c in localized:
				var code := c.unicode_at(0)
				if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
					_fail("[%s] 詞條含有違禁 Emoji: %s -> %s" % [loc, k, localized])
	if loc_node and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")
	print("  ✓ 六語系鍵值與零系統 Emoji 全數合格")

	# 建立 MobileLobby 等待第一影格就緒
	_lobby = MobileLobbyScn.new()
	root.add_child(_lobby)

func _process(_d: float) -> bool:
	_wait += 1
	if _wait < 3:
		return false

	print("--- 6. 檢驗大廳出征分頁巨偶入口與卡片控件 ---")
	_lobby.switch_tab(2)  # Tab.ADVENTURE = 2

	var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
	if colossus_btn == null:
		_fail("未在大廳出征分頁找到 BtnModeColossus 入口按鈕")
	else:
		if colossus_btn.custom_minimum_size.y < 48:
			_fail("BtnModeColossus 按鈕高度不足 48px: %f" % colossus_btn.custom_minimum_size.y)
		print("  ✓ 停擺巨偶入口按鈕存在且熱區 >= 48px (高度 %dpx)" % colossus_btn.custom_minimum_size.y)

		# 點擊切換至巨偶模式
		colossus_btn.emit_signal("pressed")

		var colossus_grid: GridContainer = _lobby.find_child("ColossusStagesGrid", true, false)
		if colossus_grid == null:
			_fail("切換至巨偶模式後未找到 ColossusStagesGrid")
		else:
			var cards := colossus_grid.get_children()
			if cards.size() != 3:
				_fail("巨偶模式卡片數量應為 3，實際為 %d" % cards.size())
			else:
				for i in range(cards.size()):
					var card: Control = cards[i] as Control
					var btn: Button = card.find_child("BattleButton", true, false)
					if btn == null:
						_fail("卡片 %d 缺少 BattleButton" % i)
					elif btn.custom_minimum_size.y < 48:
						_fail("卡片 %d BattleButton 高度不足 48px: %f" % [i, btn.custom_minimum_size.y])
				print("  ✓ 三張停擺巨偶卡片已成功渲染在出征分頁，按鈕熱區全數 >= 48px")

	_lobby.queue_free()

	if _ok:
		print("TEST_COLOSSUS_DAILY_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_DAILY_FAIL")
		quit(1)
	return true
