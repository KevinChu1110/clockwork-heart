extends RefCounted
## 經濟：金幣／SoulTicket 產銷＋日上限防通脹。

var config
var gold: int = 0
var soul_tickets: int = 0
var daily_gold_gained: int = 0
var daily_ticket_gained: int = 0
var day_key: String = ""


func setup(cfg, start_gold: int = 100, start_tickets: int = 1) -> void:
	config = cfg
	gold = start_gold
	soul_tickets = start_tickets
	daily_gold_gained = 0
	daily_ticket_gained = 0


func _caps() -> Dictionary:
	return config.economy.get("inflationGuard", {}) as Dictionary


func _apply_gain(g: int, t: int) -> Dictionary:
	var caps: Dictionary = _caps()
	var g_cap: int = int(caps.get("dailyGoldCap", 5000))
	var t_cap: int = int(caps.get("dailyTicketCap", 40))
	var g_room: int = max(0, g_cap - daily_gold_gained)
	var t_room: int = max(0, t_cap - daily_ticket_gained)
	var g_add: int = mini(g, g_room) if g > 0 else g
	var t_add: int = mini(t, t_room) if t > 0 else t
	if g_add > 0:
		gold += g_add
		daily_gold_gained += g_add
	elif g_add < 0:
		gold = max(0, gold + g_add)
	if t_add > 0:
		soul_tickets += t_add
		daily_ticket_gained += t_add
	elif t_add < 0:
		soul_tickets = max(0, soul_tickets + t_add)
	return {"goldAdded": g_add, "ticketAdded": t_add, "gold": gold, "soulTickets": soul_tickets}


func grant_source(source_id: String) -> Dictionary:
	var sources: Dictionary = config.economy.get("sources", {}) as Dictionary
	if not sources.has(source_id):
		return {"ok": false, "error": "unknown_source"}
	var row: Dictionary = sources[source_id] as Dictionary
	var r: Dictionary = _apply_gain(int(row.get("Gold", 0)), int(row.get("SoulTicket", 0)))
	r["ok"] = true
	r["exp"] = int(row.get("exp", 0))
	r["source"] = source_id
	return r


func spend_soul_pull() -> bool:
	var sinks: Dictionary = config.economy.get("sinks", {}) as Dictionary
	var need: int = int((sinks.get("soulPull", {}) as Dictionary).get("SoulTicket", 1))
	if soul_tickets < need:
		return false
	soul_tickets -= need
	return true


func spend_gold(amount: int) -> bool:
	if amount <= 0:
		return true
	if gold < amount:
		return false
	gold -= amount
	return true


func spend_sweep() -> bool:
	var sinks: Dictionary = config.economy.get("sinks", {}) as Dictionary
	var need: int = int((sinks.get("sweep", {}) as Dictionary).get("Gold", 20))
	return spend_gold(need)


func toast_for_source(source_id: String) -> String:
	match source_id:
		"dailyLogin":
			return "reward.daily_login"
		"firstClear":
			return "reward.first_clear"
		"sweep":
			return "reward.sweep"
		"partBreak":
			return "reward.part_break_gold"
		_:
			return "reward.daily_event"
