extends Node
## 《發條之心》停擺巨偶每日出征系統
## 規則：每日 3 次免費挑戰機會（上限 3 次），每日 00:00 依本機日曆重置。
## 本階段為骨架：每天看得到、次數算得出；不開戰、不扣體力、不掉機芯。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const MAX_DAILY_ENTRIES := 3
const LEVEL_GATE_OFFSET := 10

## 測試用：>0 時覆寫本地日（YYYYMMDD）。正式遊玩維持 -1。
var debug_day: int = -1

## 三隻停擺巨偶占位資料（名稱走六語系，等級 Lv12 / Lv20 / Lv28，不准自創第四隻）
const BOSSES: Array[Dictionary] = [
	{
		"id": "colossus_lion",
		"num": "巨偶-1",
		"name": "失控發條獅",
		"level": 12,
		"req_level": 2,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 610,
		"is_colossus": true,
		"boss_key": "colossus_lion",
		"blurb": "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。",
	},
	{
		"id": "colossus_puppet",
		"num": "巨偶-2",
		"name": "霧鐘提線人偶",
		"level": 20,
		"req_level": 10,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 800,
		"is_colossus": true,
		"boss_key": "colossus_puppet",
		"blurb": "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。",
	},
	{
		"id": "colossus_elephant",
		"num": "巨偶-3",
		"name": "黑鏽蒸氣巨象",
		"level": 28,
		"req_level": 18,
		"type": "停擺巨偶",
		"cost": 0,
		"power": 1320,
		"is_colossus": true,
		"boss_key": "colossus_elephant",
		"blurb": "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。",
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

static func get_req_level(boss_level: int) -> int:
	return boss_level - LEVEL_GATE_OFFSET

func get_boss_by_id(boss_id: String) -> Dictionary:
	for b in BOSSES:
		if b.get("id") == boss_id or b.get("boss_key") == boss_id:
			return b
	return {}

func get_required_level(boss_id: String) -> int:
	var b := get_boss_by_id(boss_id)
	if not b.is_empty():
		return int(b.get("req_level", int(b.get("level", 10)) - LEVEL_GATE_OFFSET))
	return 1

## 檢驗特定巨偶是否達到入場門檻（王等級 - 10 級）
func can_enter_boss(boss_id: String, player_lv: int = -1) -> bool:
	if not can_enter():
		return false
	var plv := player_lv
	if plv < 0:
		var gs := _gs()
		if gs and "level" in gs:
			plv = int(gs.get("level"))
		else:
			plv = 1
	var req := get_required_level(boss_id)
	return plv >= req

## 模擬出征嘗試：同一天呼叫 3 次成功，第 4 次被拒；若等級低於門檻則被拒
func try_enter(boss_id: String = "", player_lv: int = -1) -> Dictionary:
	refresh()
	var gs := _gs()
	if gs == null:
		return {
			"ok": false,
			"reason": "no_game_state",
			"remaining": 0,
			"message": _t("遊戲狀態未就緒"),
		}
	var check_lv: int = player_lv
	if check_lv >= 0 and not boss_id.is_empty():
		var req := get_required_level(boss_id)
		if check_lv < req:
			return {
				"ok": false,
				"reason": "level_too_low",
				"required_level": req,
				"remaining": int(gs.get("colossus_daily_entries")),
				"message": _t("等級未達 Lv.%d，低於推薦等級 10 級以上不可出征") % req,
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

func try_enter_boss(boss_id: String, player_lv: int = -1) -> Dictionary:
	var plv := player_lv
	if plv < 0:
		var gs := _gs()
		if gs and "level" in gs:
			plv = int(gs.get("level"))
		else:
			plv = 1
	return try_enter(boss_id, plv)

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
