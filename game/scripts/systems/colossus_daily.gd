extends Node
## 《發條之心》停擺巨偶每日出征系統
## 規則：每日 3 次免費挑戰機會（上限 3 次），每日 00:00 依本機日曆重置。
## 本階段為骨架：每天看得到、次數算得出；不開戰、不扣體力、不掉機芯。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const MAX_DAILY_ENTRIES := 3

## 測試用：>0 時覆寫本地日（YYYYMMDD）。正式遊玩維持 -1。
var debug_day: int = -1

## 三隻停擺巨偶占位資料（名稱走六語系，等級 Lv12 / Lv20 / Lv28，不准自創第四隻）
const BOSSES: Array[Dictionary] = [
	{
		"id": "colossus_lion",
		"num": "巨偶-1",
		"name": "失控發條獅",
		"level": 12,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 320,
		"is_colossus": true,
		"boss_key": "colossus_lion",
	},
	{
		"id": "colossus_puppet",
		"num": "巨偶-2",
		"name": "霧鐘提線人偶",
		"level": 20,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 480,
		"is_colossus": true,
		"boss_key": "colossus_puppet",
	},
	{
		"id": "colossus_elephant",
		"num": "巨偶-3",
		"name": "黑鏽蒸氣巨象",
		"level": 28,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 650,
		"is_colossus": true,
		"boss_key": "colossus_elephant",
	},
]

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null

func today_id() -> int:
	if debug_day > 0:
		return debug_day
	var d: Dictionary = Time.get_date_dict_from_system()
	return int(d.year) * 10000 + int(d.month) * 100 + int(d.day)

func refresh() -> void:
	var gs := _gs()
	if gs == null:
		return
	var today := today_id()
	var last_day: int = int(gs.get("colossus_daily_day"))
	if last_day != today:
		gs.set("colossus_daily_day", today)
		gs.set("colossus_daily_entries", MAX_DAILY_ENTRIES)

func get_remaining_entries() -> int:
	refresh()
	var gs := _gs()
	if gs == null:
		return MAX_DAILY_ENTRIES
	return maxi(0, int(gs.get("colossus_daily_entries")))

func can_enter() -> bool:
	return get_remaining_entries() > 0

## 模擬出征嘗試：同一天呼叫 3 次成功，第 4 次被拒
func try_enter(boss_id: String = "") -> Dictionary:
	refresh()
	var gs := _gs()
	if gs == null:
		return {
			"ok": false,
			"reason": "no_game_state",
			"remaining": 0,
			"message": _t("遊戲狀態未就緒"),
		}
	var left: int = int(gs.get("colossus_daily_entries"))
	if left <= 0:
		return {
			"ok": false,
			"reason": "daily_limit_reached",
			"remaining": 0,
			"message": _t("今日挑戰次數已用盡，請明天再來！"),
		}
	left -= 1
	gs.set("colossus_daily_entries", left)
	return {
		"ok": true,
		"reason": "",
		"remaining": left,
		"boss_id": boss_id,
		"message": _t("出征就緒"),
	}

func get_bosses() -> Array[Dictionary]:
	return BOSSES

## 硬限制檢驗：嚴禁改動 ATB / 攻速 / 前搖 / 命中等時間模型常數
static func verify_time_model_locked() -> bool:
	var FormulasClass: GDScript = load("res://scripts/battle/formulas.gd")
	if FormulasClass == null:
		return false
	var atb_max: float = float(FormulasClass.atb_max())
	var strike_dur: float = float(FormulasClass.strike_duration())
	var telegraph_sec: float = float(FormulasClass.boss_telegraph_sec())
	var parry_win: float = float(FormulasClass.boss_parry_window_sec())
	var grace_sec: float = float(FormulasClass.parry_early_grace_sec())
	if absf(atb_max - 100.0) > 0.001:
		return false
	if absf(strike_dur - 0.08) > 0.001:
		return false
	if absf(telegraph_sec - 1.85) > 0.001:
		return false
	if absf(parry_win - 0.85) > 0.001:
		return false
	if absf(grace_sec - 0.35) > 0.001:
		return false
	return true
