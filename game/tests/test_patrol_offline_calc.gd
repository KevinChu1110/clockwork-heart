extends SceneTree
## 發條自動巡邏全自動離線結算單元測試
## 驗收項目：
##   1. 10m / 1h / 8h 衰減曲線與有效秒數運算
##   2. 10m / 1h / 8h 離線結算與無感入帳 (金幣、經驗、發條碎片)
##   3. 超過 8h 封頂休眠機制 (零邊際增量，不超額累積)
##   4. 嚴禁手動收成按鈕與嚴禁彈出收成確認視窗 (無感入帳規範)
##   5. 大廳側欄沉浸式發條巡邏日誌呈現
## 執行指令：godot --path game --headless -s res://scripts/systems/test_patrol_offline_calc.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false
	print("PATROL_OFFLINE_CALC_FAIL")
	quit(1)


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var inv := root.get_node_or_null("InventorySystem")
	var patrol := root.get_node_or_null("ClockworkPatrolSystem")
	var gl := root.get_node_or_null("GameLog")

	if gs == null or inv == null or patrol == null or gl == null:
		_fail("Autoload 缺失: gs=%s inv=%s patrol=%s gl=%s" % [gs, inv, patrol, gl])
		return

	print("== [發條自動巡邏離線結算測試] 開始驗證 ==")

	## ──────────────────────────────────────────
	## 1. 驗證 10m 衰減與收益 (100% 邊際效率)
	## ──────────────────────────────────────────
	var r_10m: Dictionary = patrol.calc_offline_rewards(600.0)
	var eff_10m: float = float(r_10m.get("effective_seconds", 0.0))
	var marg_10m: float = float(r_10m.get("marginal_efficiency", 0.0))
	var avg_10m: float = float(r_10m.get("average_efficiency", 0.0))
	var gold_10m: int = int(r_10m.get("gold", 0))
	var xp_10m: int = int(r_10m.get("xp", 0))
	var frag_10m: int = int(r_10m.get("fragments", 0))

	if absf(eff_10m - 600.0) > 0.001:
		_fail("10m 有效秒數應為 600，實際為: %f" % eff_10m)
		return
	if absf(marg_10m - 1.0) > 0.001 or absf(avg_10m - 1.0) > 0.001:
		_fail("10m 邊際與平均效率應為 1.0 (100%%)，實際為 marg=%f avg=%f" % [marg_10m, avg_10m])
		return
	if gold_10m != 20 or xp_10m != 10:
		_fail("10m 產出數值不符: gold=%d xp=%d (期望 20/10)" % [gold_10m, xp_10m])
		return
	if frag_10m != 1:
		_fail("10m 發條碎片應為 1，實際為: %d" % frag_10m)
		return
	print("  ✓ 1. 10m 巡邏高效產出驗證通過 (有效秒: 600s, 效率: 100%%, 金: 20, 經驗: 10, 碎片: 1)")

	## ──────────────────────────────────────────
	## 2. 驗證 1h 衰減與收益 (10m~1h 衰減至 80% 邊際效率)
	## ──────────────────────────────────────────
	var r_1h: Dictionary = patrol.calc_offline_rewards(3600.0)
	var eff_1h: float = float(r_1h.get("effective_seconds", 0.0))
	var marg_1h: float = float(r_1h.get("marginal_efficiency", 0.0))
	var avg_1h: float = float(r_1h.get("average_efficiency", 0.0))
	var gold_1h: int = int(r_1h.get("gold", 0))
	var xp_1h: int = int(r_1h.get("xp", 0))

	# 1h: 前 10m (600s * 1.0) + 後 50m (3000s * 0.8) = 600 + 2400 = 3000s
	if absf(eff_1h - 3000.0) > 0.001:
		_fail("1h 有效秒數應為 3000，實際為: %f" % eff_1h)
		return
	if absf(marg_1h - 0.8) > 0.001:
		_fail("1h 邊際效率應衰減至 0.8 (80%%)，實際為: %f" % marg_1h)
		return
	if absf(avg_1h - (3000.0 / 3600.0)) > 0.001:
		_fail("1h 平均效率應為 0.8333，實際為: %f" % avg_1h)
		return
	if gold_1h != 100 or xp_1h != 50:
		_fail("1h 產出數值不符: gold=%d xp=%d (期望 100/50，已驗證相比未衰減 120 金存在衰減)" % [gold_1h, xp_1h])
		return
	print("  ✓ 2. 1h 巡邏衰減驗證通過 (有效秒: 3000s, 邊際: 80%%, 平均: 83.33%%, 金: 100, 經驗: 50)")

	## ──────────────────────────────────────────
	## 3. 驗證 8h 衰減與收益 (1h~8h 衰減至 50% 邊際效率)
	## ──────────────────────────────────────────
	var r_8h: Dictionary = patrol.calc_offline_rewards(28800.0)
	var eff_8h: float = float(r_8h.get("effective_seconds", 0.0))
	var marg_8h: float = float(r_8h.get("marginal_efficiency", 0.0))
	var avg_8h: float = float(r_8h.get("average_efficiency", 0.0))
	var gold_8h: int = int(r_8h.get("gold", 0))
	var xp_8h: int = int(r_8h.get("xp", 0))
	var frag_8h: int = int(r_8h.get("fragments", 0))

	# 8h: 前 1h (3000s) + 後 7h (25200s * 0.5 = 12600s) = 3000 + 12600 = 15600s
	if absf(eff_8h - 15600.0) > 0.001:
		_fail("8h 有效秒數應為 15600，實際為: %f" % eff_8h)
		return
	if absf(marg_8h - 0.5) > 0.001:
		_fail("8h 邊際效率應衰減至 0.5 (50%%)，實際為: %f" % marg_8h)
		return
	if absf(avg_8h - (15600.0 / 28800.0)) > 0.001:
		_fail("8h 平均效率應為 0.5417，實際為: %f" % avg_8h)
		return
	if gold_8h != 520 or xp_8h != 260:
		_fail("8h 產出數值不符: gold=%d xp=%d (期望 520/260)" % [gold_8h, xp_8h])
		return
	if frag_8h != 3:
		_fail("8h 發條碎片上限應為 3，實際為: %d" % frag_8h)
		return
	print("  ✓ 3. 8h 巡邏衰減驗證通過 (有效秒: 15600s, 邊際: 50%%, 平均: 54.17%%, 金: 520, 經驗: 260, 碎片: 3)")

	## ──────────────────────────────────────────
	## 4. 驗證超過 8h 封頂休眠機制 (>8h 邊際效率 0%，零增量)
	## ──────────────────────────────────────────
	var r_10h: Dictionary = patrol.calc_offline_rewards(36000.0)
	var r_24h: Dictionary = patrol.calc_offline_rewards(86400.0)

	if float(r_10h.get("effective_seconds", 0.0)) != 15600.0 or float(r_24h.get("effective_seconds", 0.0)) != 15600.0:
		_fail("超過 8h 有效秒數未被封頂在 15600s")
		return
	if float(r_10h.get("marginal_efficiency", 0.0)) != 0.0:
		_fail("超過 8h 邊際效率應為 0.0 (封頂停擺)，實際為: %f" % float(r_10h.get("marginal_efficiency", 0.0)))
		return
	if int(r_10h.get("gold", 0)) != gold_8h or int(r_24h.get("gold", 0)) != gold_8h:
		_fail("超過 8h 收益未封頂: 10h_gold=%d 24h_gold=%d 8h_gold=%d" % [int(r_10h.get("gold", 0)), int(r_24h.get("gold", 0)), gold_8h])
		return
	if not bool(r_10h.get("is_capped", false)):
		_fail("超過 8h 的 is_capped 旗標應為 true")
		return
	print("  ✓ 4. 超過 8h 封頂休眠驗證通過 (10h/24h 收益嚴格等於 8h，無溢出增量)")

	## ──────────────────────────────────────────
	## 5. 驗證登入無感入帳 (金幣/經驗/道具直接入帳，絕無確認視窗)
	## ──────────────────────────────────────────
	gs.reset_new_game()
	patrol.clear_patrol_data_for_test()

	var t_start := 1700000000.0
	# 模擬第一次登入 (初始錨點)
	var init_res: Dictionary = patrol.settle_offline_patrol(t_start)
	if not bool(init_res.get("ok", false)) or not bool(init_res.get("first_init", false)):
		_fail("首次結算錨點建立失敗: %s" % str(init_res))
		return

	var gold_before: int = gs.gold
	var xp_before: int = gs.xp
	var frag_before: int = inv.count("windup_fragment")

	# 模擬離線 1 小時後登入 (t_start + 3600s)
	var settle_res: Dictionary = patrol.settle_offline_patrol(t_start + 3600.0)
	if not bool(settle_res.get("ok", false)) or not bool(settle_res.get("settled", false)):
		_fail("離線 1 小時結算失敗: %s" % str(settle_res))
		return

	var gold_after: int = gs.gold
	var xp_after: int = gs.xp
	var frag_after: int = inv.count("windup_fragment")

	if gold_after != gold_before + 100:
		_fail("金幣未無感入帳: 期望增加 100，實際從 %d 變為 %d" % [gold_before, gold_after])
		return
	if xp_after != xp_before + 50:
		_fail("經驗未無感入帳: 期望增加 50，實際從 %d 變為 %d" % [xp_before, xp_after])
		return
	if frag_after != frag_before + 1:
		_fail("發條碎片未無感入帳: 期望增加 1，實際從 %d 變為 %d" % [frag_before, frag_after])
		return
	print("  ✓ 5. 無感自動入帳驗證通過 (金幣 +100、經驗 +50、發條碎片 +1 自動累加)")

	## ──────────────────────────────────────────
	## 6. 嚴禁手動收成按鈕與嚴禁彈窗確認驗證 (在大廳實例上檢查)
	## ──────────────────────────────────────────
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		_fail("無法載入 mobile_lobby.gd")
		return

	var lobby: Control = LobbyClass.new()
	root.add_child(lobby)
	lobby._ready()

	# 6.1 檢查畫面上是否有收成彈窗 / 確認視窗
	for c in root.get_children():
		if c is ConfirmationDialog or c is AcceptDialog:
			_fail("違規：根節點發現收成彈窗確認視窗: %s" % c.name)
			return
		if c.name.to_lower().find("harvest") >= 0 or c.name.to_lower().find("claim") >= 0:
			_fail("違規：根節點發現 harvest/claim 彈窗: %s" % c.name)
			return

	for c in lobby.get_children():
		if c is ConfirmationDialog or c is AcceptDialog:
			_fail("違規：大廳節點發現收成彈窗確認視窗: %s" % c.name)
			return

	# 6.2 檢查大廳所有按鈕，嚴禁手動收成按鈕
	var all_buttons: Array[Button] = []
	_collect_buttons(lobby, all_buttons)
	for b in all_buttons:
		var btn_t := b.text.strip_edges()
		if btn_t.find("收成") >= 0 or btn_t.find("領取巡邏") >= 0 or btn_t.find("收獲") >= 0:
			_fail("違規：大廳存在手動收成按鈕: %s (文字: %s)" % [b.name, btn_t])
			return

	print("  ✓ 6. 嚴格落實硬限制：無手動收成按鈕、零收成確認視窗")

	## ──────────────────────────────────────────
	## 7. 驗證大廳側欄沉浸式發條巡邏日誌呈現
	## ──────────────────────────────────────────
	var sidebar: PanelContainer = lobby.get_patrol_sidebar()
	var log_label: Label = lobby.get_patrol_log_label()

	if sidebar == null or not is_instance_valid(sidebar):
		_fail("大廳缺少 PatrolSidebar 側欄節點")
		return
	if log_label == null or not is_instance_valid(log_label):
		_fail("大廳缺少 PatrolLogLabel 日誌標籤節點")
		return

	var log_text := log_label.text
	if log_text.is_empty():
		_fail("巡邏日誌文字為空")
		return
	if log_text.find("【自律巡邏】") < 0 and log_text.find("巡邏") < 0:
		_fail("巡邏日誌未呈現沉浸式文案: %s" % log_text)
		return

	# 檢查 GameLog 紀錄
	var recent_logs: Array = gl.recent(10, "patrol")
	if recent_logs.is_empty():
		_fail("GameLog 中未記錄 patrol 分類條目")
		return

	print("  ✓ 7. 大廳側欄沉浸式發條巡邏日誌驗證通過: %s" % log_text)

	lobby.queue_free()
	print("== [發條自動巡邏離線結算測試] 全部項目驗證通過 ==")
	print("PATROL_OFFLINE_CALC_OK")
	quit(0)


func _collect_buttons(node: Node, list: Array[Button]) -> void:
	if node is Button:
		list.append(node as Button)
	for c in node.get_children():
		_collect_buttons(c, list)
