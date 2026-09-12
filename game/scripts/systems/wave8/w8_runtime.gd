extends RefCounted
## Wave-8 執行時組裝：日循環＋養成＋經濟＋關卡（單池抽魂，不開第二轉蛋）。

const ConfigScript := preload("res://scripts/systems/wave8/w8_k1_config.gd")
const DailyScript := preload("res://scripts/systems/wave8/w8_daily_cycle.gd")
const GrowthScript := preload("res://scripts/systems/wave8/w8_growth.gd")
const EconScript := preload("res://scripts/systems/wave8/w8_economy.gd")
const ChaptersScript := preload("res://scripts/systems/wave8/w8_chapters.gd")
const W8StateScript := preload("res://scripts/systems/wave8/w8_game_state.gd")
const DailyEventsScript := preload("res://scripts/systems/wave8/w8_daily_events.gd")

var config
var daily
var growth
var econ
var chapters
var meta  ## onboard／daily events
var daily_events
var inventory_parts: Dictionary = {"drop_brass_gear": 0, "drop_spring_coil": 0, "drop_core_shard": 0}
var last_error: String = ""


func setup() -> bool:
	config = ConfigScript.new()
	if not config.load_from():
		last_error = "k1_config"
		return false
	daily = DailyScript.new()
	daily.setup(config)
	growth = GrowthScript.new()
	growth.setup(config)
	econ = EconScript.new()
	econ.setup(config, 100, 1)
	chapters = ChaptersScript.new()
	chapters.setup(config)
	meta = W8StateScript.new()
	meta.load_bingo()
	meta.grant_tutorial_ticket()
	daily_events = DailyEventsScript.new()
	if not daily_events.load_from():
		last_error = "k2_daily_events"
		return false
	# sync tutorial ticket into econ
	econ.soul_tickets = max(econ.soul_tickets, meta.soul_tickets)
	return true


func do_first_clear(chapter_id: String) -> Dictionary:
	daily.tick_regen()
	var ch: Dictionary = config.chapter_def(chapter_id)
	if ch.is_empty():
		return {"ok": false, "error": "no_chapter"}
	var cost: int = int(ch.get("staminaEnter", 0))
	if not daily.spend(cost):
		return {"ok": false, "error": "stamina"}
	var enemy: Dictionary = ch.get("enemy", {}) as Dictionary
	var base: Dictionary = growth.base_stats()
	var enh: Dictionary = growth.enhance_bonus()
	var dmg: int = chapters.final_damage(10 + int(base.ATK), int(enh.ATK), int(enemy.get("DEF", 0)))
	if dmg <= 0:
		return {"ok": false, "error": "no_damage"}
	var already: bool = chapters.is_cleared(chapter_id)
	chapters.mark_cleared(chapter_id)
	var reward: Dictionary = chapters.first_clear_reward(chapter_id) if not already else chapters.sweep_reward(chapter_id)
	# first clear uses firstClear table only once
	if already:
		return {"ok": false, "error": "already_cleared_use_sweep"}
	var g: int = int(reward.get("Gold", 0))
	var t: int = int(reward.get("SoulTicket", 0))
	var exp_n: int = int(reward.get("exp", 0))
	var gain: Dictionary = econ._apply_gain(g, t)
	var lv: Dictionary = growth.add_exp(exp_n)
	var drop_id: String = str(reward.get("DropId", ""))
	if drop_id != "":
		inventory_parts[drop_id] = int(inventory_parts.get(drop_id, 0)) + 1
	return {
		"ok": true,
		"chapterId": chapter_id,
		"damage": dmg,
		"reward": reward,
		"gain": gain,
		"level": lv,
		"wind": daily.wind,
		"toastKey": "reward.first_clear",
	}


func do_sweep(chapter_id: String) -> Dictionary:
	daily.tick_regen()
	if not daily.can_sweep():
		return {"ok": false, "error": "daily_sweep_cap", "toastKey": "err.daily_cap_sweep"}
	var ch: Dictionary = config.chapter_def(chapter_id)
	if not chapters.can_sweep(chapter_id, daily.wind, true):
		return {"ok": false, "error": "cannot_sweep"}
	var cost: int = int(ch.get("staminaEnter", 0))
	if not daily.spend(cost):
		return {"ok": false, "error": "stamina"}
	if not econ.spend_sweep():
		daily.wind += cost  # refund stamina if gold fail
		return {"ok": false, "error": "gold"}
	daily.note_sweep()
	var reward: Dictionary = chapters.sweep_reward(chapter_id)
	var gain: Dictionary = econ._apply_gain(int(reward.get("Gold", 0)), 0)
	var lv: Dictionary = growth.add_exp(int(reward.get("exp", 0)))
	var drop_id: String = str(reward.get("DropId", ""))
	var drop_pct: int = int(reward.get("dropPct", 0))
	var dropped := false
	if drop_id != "" and drop_pct > 0:
		# deterministic-ish: always drop in tests via pct check with fixed rule — use >= 100 or roll
		dropped = drop_pct >= 100
		if not dropped:
			dropped = (randi() % 100) < drop_pct
		if dropped:
			inventory_parts[drop_id] = int(inventory_parts.get(drop_id, 0)) + 1
	return {"ok": true, "reward": reward, "gain": gain, "level": lv, "dropped": dropped, "wind": daily.wind, "toastKey": "reward.sweep"}


func do_enhance(slot: String) -> Dictionary:
	var brass: int = int(inventory_parts.get("drop_brass_gear", 0))
	var res: Dictionary = growth.try_enhance(slot, econ.gold, brass)
	if not bool(res.get("ok", false)):
		return res
	if not econ.spend_gold(int(res.get("costGold", 0))):
		# rollback enhance
		growth.enhance[slot] = int(growth.enhance.get(slot, 1)) - 1
		return {"ok": false, "error": "gold"}
	var cp: int = int(res.get("costPart", 0))
	if cp > 0:
		inventory_parts["drop_brass_gear"] = brass - cp
	return res


func calendar_day_index(now_unix: float = -1.0) -> int:
	## Mon=1 … Sun=7 → DayId D1…D7（D7 週末）
	if now_unix < 0.0:
		now_unix = Time.get_unix_time_from_system()
	daily.tick_regen(now_unix)
	var dt := Time.get_datetime_dict_from_unix_time(int(now_unix))
	var wd: int = int(dt.get("weekday", 0))  # 0=Sun … 6=Sat
	if wd == 0:
		return 7
	return wd

func do_daily_event_pick(choice_id: String) -> Dictionary:
	daily.tick_regen()
	var day_key: String = daily.day_key
	var idx: int = calendar_day_index()
	return daily_events.pick(day_key, idx, choice_id, self)

func today_daily_event() -> Dictionary:
	daily.tick_regen()
	var idx: int = calendar_day_index()
	var ev: Dictionary = daily_events.todays_event(idx)
	var day_key: String = daily.day_key
	return {
		"event": ev,
		"dayKey": day_key,
		"dayIndex": idx,
		"picked": daily_events.has_picked(day_key),
		"pickedChoice": str(daily_events.picked_by_day.get(day_key, "")),
	}

func summary() -> Dictionary:
	return {
		"wind": daily.wind,
		"level": growth.level,
		"gold": econ.gold,
		"soulTickets": econ.soul_tickets,
		"cleared": chapters.cleared.keys(),
		"enhance": growth.enhance,
		"parts": inventory_parts,
		"noSecondGacha": true,
	}
