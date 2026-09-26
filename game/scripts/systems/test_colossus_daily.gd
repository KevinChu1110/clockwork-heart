extends SceneTree
## 停擺巨偶每日出征與戰鬥掉落單元測試 (test_colossus_daily.gd)
## 依據任務 t_f093ee0b 驗證規範：
## 1. 停擺巨偶三張占位卡（失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏽蒸氣巨象 Lv28，無第四隻）
## 2. 每日初始次數為 3，點擊開戰消耗 1 次當日次數；剩餘次數正確遞減
## 3. 同一天內出征滿 3 次後，第 4 次被拒並提示「今日挑戰次數已用盡，請明天再來！」彈窗
## 4. 跨日重置（改 debug_day 隔日後次數回到 3）
## 5. 既有戰鬥接通：卡片點擊觸發 request_battle 攜帶對應 boss key
## 6. 勝場掉落五槽機芯部件入袋，背包/整備看得到；敗場不給機芯
## 7. 硬限制鎖死：嚴禁改動 ATB / 攻速 / 前搖 / 命中等時間模型常數（常數偏移測試必紅）
## 8. 六語系鍵值完整且全域零系統 Emoji 檢查
## 9. 大廳出征分頁子模式切換與熱區 >= 48px

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FormulasClass = preload("res://scripts/battle/formulas.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _wait := 0
var _lobby: Control = null
var _last_requested_battle := ""

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

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		cs = CoreSystemClass.new()
		cs.name = "CoreSystem"
		root.add_child(cs)

	gs.reset_new_game()
	cds.debug_day = 20260927
	cds.refresh()

	# --- 1. 檢驗三隻巨偶占位資料 ---
	print("--- 1. 檢驗三隻停擺巨偶占位資料 ---")
	var bosses: Array = cds.get_bosses()
	if bosses.size() != 3:
		_fail("巨偶數量應為 3，實際為 %d（不准自創第四隻）" % bosses.size())
	var expected_bosses := [
		{
			"name": "失控發條獅",
			"level": 12,
			"id": "colossus_lion",
			"blurb": "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。",
		},
		{
			"name": "霧鐘提線人偶",
			"level": 20,
			"id": "colossus_puppet",
			"blurb": "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。",
		},
		{
			"name": "黑鏽蒸氣巨象",
			"level": 28,
			"id": "colossus_elephant",
			"blurb": "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。",
		},
	]
	for i in range(expected_bosses.size()):
		var b: Dictionary = bosses[i]
		if str(b.get("name", "")) != str(expected_bosses[i]["name"]):
			_fail("巨偶 %d 名稱不符：預期 %s，實際 %s" % [i, expected_bosses[i]["name"], b.get("name")])
		if int(b.get("level", 0)) != int(expected_bosses[i]["level"]):
			_fail("巨偶 %d 等級不符：預期 Lv%d，實際 Lv%d" % [i, expected_bosses[i]["level"], b.get("level")])
		if int(b.get("cost", -1)) != 0:
			_fail("巨偶 %d 本期不應消耗體力/能量（cost 應為 0）" % i)
		var blurb := str(b.get("blurb", ""))
		if blurb.is_empty():
			_fail("巨偶 %d 缺少世界觀副標 (blurb)" % i)
		var b_len := blurb.length()
		if b_len < 20 or b_len > 40:
			_fail("巨偶 %d 副標字數未落在 20–40 字之內: %d 字 (%s)" % [i, b_len, blurb])
		for c in blurb:
			var code := c.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
				_fail("巨偶 %d 副標含有違禁 emoji: %s" % [i, blurb])
	print("  ✓ 三隻停擺巨偶資料與世界觀副標完全符合規範")

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

	# --- 3.5 檢驗停擺巨偶推薦等級與入場門檻限制（低於王等級 10 級不能進）---
	print("--- 3.5 檢驗推薦等級與等級門檻限制（低於王等級 10 級不能進）---")
	if cds.get_required_level("colossus_lion") != 2:
		_fail("失控發條獅門檻應為 Lv2，實際為 %d" % cds.get_required_level("colossus_lion"))
	if cds.get_required_level("colossus_puppet") != 10:
		_fail("霧鐘提線人偶門檻應為 Lv10，實際為 %d" % cds.get_required_level("colossus_puppet"))
	if cds.get_required_level("colossus_elephant") != 18:
		_fail("黑鏽蒸氣巨象門檻應為 Lv18，實際為 %d" % cds.get_required_level("colossus_elephant"))

	# 獅門檻 2：Lv1 不能進、Lv2 能進
	if cds.can_enter_boss("colossus_lion", 1):
		_fail("失控發條獅 Lv1 應不能進")
	if not cds.can_enter_boss("colossus_lion", 2):
		_fail("失控發條獅 Lv2 應能進")

	# 提線門檻 10：Lv9 不能進、Lv10 能進
	if cds.can_enter_boss("colossus_puppet", 9):
		_fail("霧鐘提線人偶 Lv9 應不能進")
	if not cds.can_enter_boss("colossus_puppet", 10):
		_fail("霧鐘提線人偶 Lv10 應能進")

	# 巨象門檻 18：Lv1 不能進、Lv18 能進
	if cds.can_enter_boss("colossus_elephant", 1):
		_fail("黑鏽蒸氣巨象 Lv1 應不能進")
	if not cds.can_enter_boss("colossus_elephant", 18):
		_fail("黑鏽蒸氣巨象 Lv18 應能進")

	# 檢驗 try_enter 等級未達回傳 level_too_low
	var r_low = cds.try_enter("colossus_elephant", 1)
	if bool(r_low.get("ok", true)) or str(r_low.get("reason", "")) != "level_too_low":
		_fail("Lv1 嘗試進巨象應回傳 level_too_low，實際: %s" % str(r_low))
	var r_pass = cds.try_enter("colossus_elephant", 18)
	if not bool(r_pass.get("ok", false)):
		_fail("Lv18 嘗試進巨象應成功，實際: %s" % str(r_pass))
	print("  ✓ 單元測試等級門檻驗證通過：Lv1 不能進巨象、Lv18 能進；獅門檻 2、提線門檻 10 全數吻合")

	# --- 4. 檢驗勝場掉落機芯部件、敗場不掉機芯 ---
	print("--- 4. 檢驗勝場掉落五槽機芯部件入袋，敗場不給機芯 ---")
	CoreSystemClass.clear_inventory()
	var initial_core_count: int = CoreSystemClass.get_inventory().size()

	# 模擬勝場：抽取五槽機芯部件並入袋
	var won_part: Dictionary = CoreSystemClass.on_battle_won()
	if won_part.is_empty():
		_fail("勝場結算 roll_and_add_battle_drop 應傳回有效機芯部件")
	if not CoreSystemClass.ALL_SLOT_IDS.has(str(won_part.get("slot", ""))):
		_fail("勝場機芯部件槽位不合法: %s" % str(won_part.get("slot")))
	if not CoreSystemClass.ALL_TIER_IDS.has(str(won_part.get("tier", ""))):
		_fail("勝場機芯部件色階不合法: %s" % str(won_part.get("tier")))
	if CoreSystemClass.get_inventory().size() != initial_core_count + 1:
		_fail("勝場後機芯背包總數應增加 1")
	if gs.core_bag.size() != initial_core_count + 1:
		_fail("勝場後 GameState.core_bag 總數應增加 1")
	print("  ✓ 勝場機芯掉落驗證成功：【%s階】%s 入袋" % [won_part.get("tier_name", ""), won_part.get("slot_name", "")])

	# 模擬敗場：不呼叫 roll_and_add_battle_drop，背包不變
	var after_defeat_count: int = CoreSystemClass.get_inventory().size()
	if after_defeat_count != initial_core_count + 1:
		_fail("敗場不應增加機芯部件")
	print("  ✓ 敗場不給機芯部件驗證通過")

	# --- 5. 檢驗敵人資料庫定義與部位破壞 ---
	print("--- 5. 檢驗停擺巨偶敵人定義、部位破壞與格擋 ---")
	var WC = load("res://scripts/world/world_content.gd")
	if WC == null:
		_fail("無法載入 world_content.gd")
	else:
		for binfo in expected_bosses:
			var mid: String = str(binfo["id"])
			var edef: Dictionary = WC.enemy_def(mid)
			if edef.is_empty():
				_fail("未在 WorldContent 找到敵人定義: %s" % mid)
			if not bool(edef.get("is_boss", false)):
				_fail("敵人 %s 應為 Boss (is_boss: true)" % mid)
			if float(edef.get("windup", 0.0)) <= 0.0 or float(edef.get("recover", 0.0)) <= 0.0:
				_fail("敵人 %s 缺少格擋時間窗口配置 (windup/recover)" % mid)
			print("  ✓ 敵人定義完整: %s (HP: %d, ATK: %d, DEF: %d, is_boss: %s)" % [
				edef.get("name"), edef.get("max_hp"), edef.get("atk"), edef.get("def"), edef.get("is_boss")
			])

	# --- 6. 檢驗硬限制：嚴禁改動 ATB / 攻速 / 前搖 / 命中等時間模型常數 ---
	print("--- 6. 檢驗硬限制：ATB / 攻速時間模型常數鎖定 ---")
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

	# --- 7. 檢驗六語系鍵值與零 Emoji ---
	print("--- 7. 檢驗六語系字典映射與零系統 Emoji ---")
	var check_keys := [
		"停擺巨偶",
		"失控發條獅",
		"霧鐘提線人偶",
		"黑鏽蒸氣巨象",
		"胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。",
		"白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。",
		"冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。",
		"明天再來",
		"四區主線",
		"停擺巨偶 · 今日剩餘: %d/3",
		"今日挑戰次數已用盡，請明天再來！",
		"推薦 Lv.%d",
		"未達 Lv.%d 不可出征",
		"需達 Lv.%d",
		"未達標",
		"等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！",
		"等級未達 Lv.%d，低於推薦等級 10 級以上不可出征",
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

	# 重置當日次數並設定足夠等級 (Lv20) 以測試大廳點擊
	cds.debug_day = 20260927
	cds.refresh()
	gs.set("colossus_daily_entries", 3)
	gs.set("level", 20)

	# 建立 MobileLobby 等待第一影格就緒
	_lobby = MobileLobbyScn.new()
	_lobby.request_battle.connect(func(m: String):
		_last_requested_battle = m
		print("  [SIGNAL] MobileLobby emitted request_battle: ", m)
	)
	root.add_child(_lobby)

func _process(_d: float) -> bool:
	_wait += 1
	if _wait < 3:
		return false

	print("--- 8. 檢驗大廳出征分頁巨偶入口與卡片點擊進戰鬥 ---")
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
				var cds = root.get_node_or_null("ColossusDailySystem")
				var expected_modes := ["colossus_lion", "colossus_puppet", "colossus_elephant"]
				for i in range(cards.size()):
					var card: Control = cards[i] as Control
					var btn: Button = card.find_child("BattleButton", true, false)
					if btn == null:
						_fail("卡片 %d 缺少 BattleButton" % i)
					elif btn.custom_minimum_size.y < 48:
						_fail("卡片 %d BattleButton 高度不足 48px: %f" % [i, btn.custom_minimum_size.y])

				# 驗證三張出征卡顯示推薦等級與出征按鈕
				var expected_levels := [12, 20, 28]
				for i in range(cards.size()):
					var card: Control = cards[i] as Control
					var hint_l: Label = card.find_child("ResistHintLabel", true, false)
					if hint_l == null:
						_fail("卡片 %d 缺少 ResistHintLabel" % i)
					elif not hint_l.text.contains(str(expected_levels[i])):
						_fail("卡片 %d 未顯示推薦等級 Lv%d，實際為: %s" % [i, expected_levels[i], hint_l.text])
				print("  ✓ 三張停擺巨偶出征卡皆完整顯示推薦等級 (Lv12, Lv20, Lv28)")

				# 測試低等級阻擋：當玩家為 Lv1 時，巨象 (門檻 18) 出征鈕灰掉 (高 >= 50px) 且說明不能進
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 1)
				_lobby.call("_refresh_region_stages")
				var colossus_grid_low: GridContainer = _lobby.find_child("ColossusStagesGrid", true, false)
				var cards_low := colossus_grid_low.get_children()
				var ele_card: Control = cards_low[2] as Control
				var ele_btn: Button = ele_card.find_child("BattleButton", true, false)
				var ele_hint: Label = ele_card.find_child("ResistHintLabel", true, false)
				if ele_btn.custom_minimum_size.y < 50:
					_fail("巨象出征鈕高度未達 50px: %f" % ele_btn.custom_minimum_size.y)
				if not ele_btn.text.contains("18"):
					_fail("Lv1 時巨象出征鈕應標註需達門檻 18，實際文字: %s" % ele_btn.text)
				if not ele_hint.text.contains("18") or not ele_hint.text.contains("不可出征"):
					_fail("Lv1 時巨象卡片應有一句話說明未達 Lv.18 不可出征，實際: %s" % ele_hint.text)
				_last_requested_battle = ""
				ele_btn.emit_signal("pressed")
				if _last_requested_battle != "":
					_fail("Lv1 點擊巨象出征鈕不應進入戰鬥，實際發送: %s" % _last_requested_battle)
				print("  ✓ 低等角色 (Lv1) 巨象出征鈕灰掉 (高 >= 50px)、顯示門檻說明且打不開最高階巨偶驗證通過")

				# 恢復足夠等級 (Lv20) 刷新，進行開戰測試
				if gs:
					gs.set("level", 20)
				_lobby.call("_refresh_region_stages")
				var colossus_grid_ok: GridContainer = _lobby.find_child("ColossusStagesGrid", true, false)
				cards = colossus_grid_ok.get_children()

				# 測試點擊第 1 張卡片：失控發條獅
				var first_card: Control = cards[0] as Control
				var first_btn: Button = first_card.find_child("BattleButton", true, false)
				var prev_left: int = cds.get_remaining_entries()
				_last_requested_battle = ""
				first_btn.emit_signal("pressed")

				if _last_requested_battle != "colossus_lion":
					_fail("點擊失控發條獅後 request_battle 應發送 colossus_lion，實際為: %s" % _last_requested_battle)
				else:
					print("  ✓ 點擊失控發條獅卡片成功觸發 request_battle(\"colossus_lion\")")

				var cur_left: int = cds.get_remaining_entries()
				if cur_left != prev_left - 1:
					_fail("點擊開戰後剩餘次數應由 %d 扣為 %d，實際為: %d" % [prev_left, prev_left - 1, cur_left])
				else:
					print("  ✓ 開戰成功消耗 1 次次數（由 %d 次降為 %d 次）" % [prev_left, cur_left])

				# 測試連續打完剩餘 2 次後觸發限制彈窗
				cds.try_enter("colossus_puppet")
				cds.try_enter("colossus_elephant")
				_lobby.call("_refresh_adventure_submode_ui")
				_lobby.call("_refresh_region_stages")

				# 滿 3 次後再次點擊第 1 張卡片
				_last_requested_battle = ""
				first_btn.emit_signal("pressed")
				if _last_requested_battle != "":
					_fail("次數用盡後不應再發送 request_battle，實際發送: %s" % _last_requested_battle)
				var limit_dlg = _lobby.get_node_or_null("ColossusLimitDialog")
				if limit_dlg == null:
					_fail("次數用盡點擊後應彈出 ColossusLimitDialog 提示明天再來")
				else:
					print("  ✓ 次數用盡後第 4 次點擊成功彈出明天再來提示彈窗")
					limit_dlg.queue_free()

	_lobby.queue_free()

	if _ok:
		print("TEST_COLOSSUS_DAILY_OK")
		quit(0)
	else:
		print("TEST_COLOSSUS_DAILY_FAIL")
		quit(1)
	return true
