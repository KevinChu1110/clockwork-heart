## 發條之心 (Clockwork Heart) - 發條儲能庫放置收益系統 (Idle Clockwork Vault)
## 依據 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點二
## 放置規則：離線/待機每小時產出基礎金幣 150 與鐵屑 3（上限 8 小時）
## 刻意不加 class_name，避免無頭測試模式下缺少 class cache 導致報錯。

const MAX_HOURS: float = 8.0
const MAX_SECONDS: float = 28800.0  ## 8.0 * 3600.0
const GOLD_PER_HOUR: int = 150
const IRON_SCRAP_PER_HOUR: int = 3
const FLAG_LAST_TS: String = "idle_vault_last_ts"


## 取得上次領取時間戳記（若未曾設定，初始化為當前時間並寫入）
static func get_last_claim_ts() -> float:
	var gs = Engine.get_main_loop().root.get_node_or_null("GameState")
	if gs == null:
		return 0.0
	if not gs.flags.has(FLAG_LAST_TS):
		var now_t := Time.get_unix_time_from_system()
		gs.flags[FLAG_LAST_TS] = now_t
		return now_t
	return float(gs.flags[FLAG_LAST_TS])


## 設定上次領取時間戳記
static func set_last_claim_ts(ts: float) -> void:
	var gs = Engine.get_main_loop().root.get_node_or_null("GameState")
	if gs != null:
		gs.flags[FLAG_LAST_TS] = ts


## 取得當前累積秒數（已限制在 0 ~ MAX_SECONDS）
static func get_elapsed_seconds(now_ts: float = -1.0) -> float:
	var current_now := now_ts if now_ts >= 0.0 else Time.get_unix_time_from_system()
	var last_ts := get_last_claim_ts()
	if last_ts <= 0.0:
		set_last_claim_ts(current_now)
		return 0.0
	var elapsed := current_now - last_ts
	if elapsed < 0.0:
		return 0.0
	return minf(elapsed, MAX_SECONDS)


## 取得累積進度比例（0.0 ~ 1.0）
static func get_progress_ratio(now_ts: float = -1.0) -> float:
	var sec := get_elapsed_seconds(now_ts)
	if MAX_SECONDS <= 0.0:
		return 0.0
	return clampf(sec / MAX_SECONDS, 0.0, 1.0)


## 是否已達 8 小時上限
static func is_vault_full(now_ts: float = -1.0) -> bool:
	return get_elapsed_seconds(now_ts) >= MAX_SECONDS


## 取得累積金幣（每小時 GOLD_PER_HOUR，依時間比例累積）
static func get_accumulated_gold(now_ts: float = -1.0) -> int:
	var sec := get_elapsed_seconds(now_ts)
	var hrs := sec / 3600.0
	return int(hrs * float(GOLD_PER_HOUR))


## 取得累積鐵屑（每小時 IRON_SCRAP_PER_HOUR，依時間比例累積）
static func get_accumulated_iron_scrap(now_ts: float = -1.0) -> int:
	var sec := get_elapsed_seconds(now_ts)
	var hrs := sec / 3600.0
	return int(hrs * float(IRON_SCRAP_PER_HOUR))


## 取得當前儲能庫狀態字典
static func get_status(now_ts: float = -1.0) -> Dictionary:
	var sec := get_elapsed_seconds(now_ts)
	var hrs := sec / 3600.0
	var g := get_accumulated_gold(now_ts)
	var s := get_accumulated_iron_scrap(now_ts)
	var ratio := get_progress_ratio(now_ts)
	var full := is_vault_full(now_ts)
	return {
		"elapsed_seconds": sec,
		"accumulated_hours": hrs,
		"gold": g,
		"iron_scrap": s,
		"progress_ratio": ratio,
		"is_full": full,
		"max_hours": MAX_HOURS
	}


## 一鍵領取收益並重置計時
static func claim(now_ts: float = -1.0) -> Dictionary:
	var current_now := now_ts if now_ts >= 0.0 else Time.get_unix_time_from_system()
	var g := get_accumulated_gold(current_now)
	var s := get_accumulated_iron_scrap(current_now)
	var sec := get_elapsed_seconds(current_now)
	var hrs := sec / 3600.0
	var claimed := (g > 0 or s > 0)

	var gs = Engine.get_main_loop().root.get_node_or_null("GameState")
	var inv = Engine.get_main_loop().root.get_node_or_null("InventorySystem")

	if claimed:
		if gs != null and g > 0:
			gs.add_gold(g)
		if inv != null and s > 0:
			inv.add_item("iron_scrap", s)

	## 重置領取時間為當前時間
	set_last_claim_ts(current_now)

	return {
		"claimed": claimed,
		"gold": g,
		"iron_scrap": s,
		"elapsed_seconds": sec,
		"hours": hrs,
		"reset_ts": current_now
	}


## 重置儲能庫計時
static func reset(now_ts: float = -1.0) -> void:
	var current_now := now_ts if now_ts >= 0.0 else Time.get_unix_time_from_system()
	set_last_claim_ts(current_now)
