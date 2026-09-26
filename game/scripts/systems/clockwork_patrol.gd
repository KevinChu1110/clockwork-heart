extends Node
## 發條自動巡邏全自動離線結算系統 (Clockwork Patrol System)
## Autoload: ClockworkPatrolSystem
##
## 核心規約：
## 1. 玩家離線依時間戳差累積巡邏收益（純前後差運算，不改時間模型、不加背景常駐服務）。
## 2. 登入或進入大廳時無感自動入帳（拔除手動收成按鈕，嚴禁任何收成確認視窗與彈窗）。
## 3. 大廳側欄寫入沉浸式發條巡邏日誌。
## 4. 收益具備 10m / 1h / 8h 階梯式衰減，8h 封頂休眠。

signal patrol_settled(result: Dictionary)
signal patrol_logs_updated()

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

## 衰減門檻（秒）
const TIER_1_SEC := 600.0       ## 10 分鐘：高能巡邏期 (100%)
const TIER_2_SEC := 3600.0      ## 1 小時：穩定釋放期 (80%)
const TIER_3_SEC := 28800.0     ## 8 小時：低耗巡邏期 (50%)，之後停擺封頂 (0%)

## 邊際產出效率
const EFFICIENCY_TIER_1 := 1.0  ## 0 ~ 10m: 100%
const EFFICIENCY_TIER_2 := 0.8  ## 10m ~ 1h: 80%
const EFFICIENCY_TIER_3 := 0.5  ## 1h ~ 8h: 50%
const EFFICIENCY_TIER_4 := 0.0  ## >8h: 0% (封頂無增量)

## 基準時薪產出（每 3600 有效秒）
const BASE_GOLD_PER_HOUR := 120
const BASE_XP_PER_HOUR := 60

## 存檔旗標
const FLAG_PATROL_TS := "patrol.last_ts"
const FLAG_PATROL_LOGS := "patrol.logs"
const MAX_LOGS := 30

var _cached_logs: Array[Dictionary] = []


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


func _get_game_state() -> Node:
	if Engine.get_main_loop() is SceneTree:
		var st := Engine.get_main_loop() as SceneTree
		if st.root:
			return st.root.get_node_or_null("GameState")
	return null


func _get_inv_sys() -> Node:
	if Engine.get_main_loop() is SceneTree:
		var st := Engine.get_main_loop() as SceneTree
		if st.root:
			return st.root.get_node_or_null("InventorySystem")
	return null


func _get_game_log() -> Node:
	if Engine.get_main_loop() is SceneTree:
		var st := Engine.get_main_loop() as SceneTree
		if st.root:
			return st.root.get_node_or_null("GameLog")
	return null


func _ready() -> void:
	# 遊戲啟動時嘗試讀取快取日誌
	get_patrol_logs()


## 計算有效秒數 (帶分段衰減與 8h 封頂)
func calculate_effective_seconds(elapsed_sec: float) -> float:
	var t := maxf(0.0, elapsed_sec)
	var t1 := minf(t, TIER_1_SEC)
	var t2 := maxf(0.0, minf(t - TIER_1_SEC, TIER_2_SEC - TIER_1_SEC))
	var t3 := maxf(0.0, minf(t - TIER_2_SEC, TIER_3_SEC - TIER_2_SEC))
	return (t1 * EFFICIENCY_TIER_1) + (t2 * EFFICIENCY_TIER_2) + (t3 * EFFICIENCY_TIER_3)


## 當前時間點的邊際產能效率 (用於驗收 10m/1h/8h 衰減狀態)
func get_marginal_efficiency(elapsed_sec: float) -> float:
	var t := maxf(0.0, elapsed_sec)
	if t <= TIER_1_SEC:
		return EFFICIENCY_TIER_1
	elif t <= TIER_2_SEC:
		return EFFICIENCY_TIER_2
	elif t <= TIER_3_SEC:
		return EFFICIENCY_TIER_3
	else:
		return EFFICIENCY_TIER_4


## 離線全段平均產能效率
func get_average_efficiency(elapsed_sec: float) -> float:
	var t := maxf(0.0, elapsed_sec)
	if t <= 0.0:
		return EFFICIENCY_TIER_1
	return calculate_effective_seconds(t) / t


## 依離線秒數計算巡邏收益
func calc_offline_rewards(elapsed_sec: float) -> Dictionary:
	var t := maxf(0.0, elapsed_sec)
	var eff := calculate_effective_seconds(t)
	var gold := int(floor(eff * float(BASE_GOLD_PER_HOUR) / 3600.0))
	var xp := int(floor(eff * float(BASE_XP_PER_HOUR) / 3600.0))
	
	var fragments := 0
	if eff >= 10000.0:
		fragments = 3
	elif eff >= 3600.0:
		fragments = 2
	elif eff >= 600.0:
		fragments = 1
	
	var tier_desc := ""
	if t <= TIER_1_SEC:
		tier_desc = "高效巡邏期"
	elif t <= TIER_2_SEC:
		tier_desc = "穩定釋放期"
	elif t <= TIER_3_SEC:
		tier_desc = "低耗運轉期"
	else:
		tier_desc = "動能耗盡休眠"

	return {
		"elapsed_seconds": t,
		"effective_seconds": eff,
		"gold": gold,
		"xp": xp,
		"fragments": fragments,
		"marginal_efficiency": get_marginal_efficiency(t),
		"average_efficiency": get_average_efficiency(t),
		"is_capped": t >= TIER_3_SEC,
		"tier_desc": tier_desc,
	}


## 全自動離線結算：無感入帳，嚴禁彈窗，拔除手動領取按鈕
func settle_offline_patrol(now_ts: float = -1.0) -> Dictionary:
	var gs := _get_game_state()
	if gs == null:
		return {"ok": false, "error": "missing_game_state"}
	
	if now_ts < 0.0:
		now_ts = Time.get_unix_time_from_system()
	
	var last_ts: float = float(gs.get_flag(FLAG_PATROL_TS, 0.0))
	if last_ts <= 0.0:
		# 首次初始化巡邏錨點
		gs.set_flag(FLAG_PATROL_TS, now_ts)
		var init_entry := {
			"t": Time.get_datetime_string_from_system(true),
			"unix": now_ts,
			"msg": "【自律巡邏】背後發條首次上緊，自律守護機制已啟動。",
			"gold": 0,
			"xp": 0,
			"fragments": 0,
			"elapsed": 0.0,
		}
		_append_patrol_log(init_entry)
		return {"ok": true, "settled": false, "first_init": true, "now_ts": now_ts}
	
	var elapsed := now_ts - last_ts
	if elapsed < 60.0:
		# 少於 1 分鐘，維持時間戳，避免極短重複計算
		return {"ok": true, "settled": false, "reason": "too_short", "elapsed": elapsed}
	
	var rewards := calc_offline_rewards(elapsed)
	
	# 無感自動入帳：直接進 GameState 與背包，絕不彈出收成確認視窗
	if rewards.gold > 0:
		gs.gold += rewards.gold
		if gs.has_signal("gold_changed"):
			gs.gold_changed.emit(gs.gold)
	
	if rewards.xp > 0:
		if gs.has_method("add_xp"):
			gs.add_xp(rewards.xp)
		else:
			gs.xp += rewards.xp
	
	if rewards.fragments > 0:
		var inv := _get_inv_sys()
		if inv and inv.has_method("add_item"):
			inv.add_item("windup_fragment", rewards.fragments)
	
	# 更新最後巡邏結算時間戳
	gs.set_flag(FLAG_PATROL_TS, now_ts)
	
	# 沉浸式發條巡邏日誌
	var duration_str := _format_duration(elapsed)
	var log_msg := "【自律巡邏】離線巡邏 %s，無感入帳：%d 金幣 · %d 經驗 · %d 發條碎片（%s）。" % [
		duration_str, rewards.gold, rewards.xp, rewards.fragments, rewards.tier_desc
	]
	
	var entry := {
		"t": Time.get_datetime_string_from_system(true),
		"unix": now_ts,
		"msg": log_msg,
		"gold": rewards.gold,
		"xp": rewards.xp,
		"fragments": rewards.fragments,
		"elapsed": elapsed,
	}
	_append_patrol_log(entry)
	
	var gl := _get_game_log()
	if gl and gl.has_method("append"):
		gl.append("patrol", log_msg, rewards)
	
	patrol_settled.emit(rewards)
	return {"ok": true, "settled": true, "rewards": rewards, "entry": entry}


func _format_duration(sec: float) -> String:
	var total_sec := int(sec)
	var h := total_sec / 3600
	var m := (total_sec % 3600) / 60
	var s := total_sec % 60
	if h > 0:
		if m > 0:
			return "%d 小時 %d 分" % [h, m]
		else:
			return "%d 小時" % h
	elif m > 0:
		return "%d 分鐘" % m
	else:
		return "%d 秒" % s


func _append_patrol_log(entry: Dictionary) -> void:
	_cached_logs.append(entry)
	while _cached_logs.size() > MAX_LOGS:
		_cached_logs.pop_front()
	var gs := _get_game_state()
	if gs:
		gs.set_flag(FLAG_PATROL_LOGS, _cached_logs)
	patrol_logs_updated.emit()


func get_patrol_logs() -> Array[Dictionary]:
	var gs := _get_game_state()
	if gs:
		var saved = gs.get_flag(FLAG_PATROL_LOGS, null)
		if saved is Array:
			_cached_logs.clear()
			for item in saved:
				if item is Dictionary:
					_cached_logs.append(item)
	return _cached_logs


func get_latest_patrol_log_text() -> String:
	var logs := get_patrol_logs()
	if logs.is_empty():
		return "【自律巡邏】背後發條依動能持續運轉中，巡邏已解鎖地圖區域……"
	return str(logs[logs.size() - 1].get("msg", ""))


func clear_patrol_data_for_test() -> void:
	_cached_logs.clear()
	var gs := _get_game_state()
	if gs:
		gs.set_flag(FLAG_PATROL_TS, 0.0)
		gs.set_flag(FLAG_PATROL_LOGS, [])
