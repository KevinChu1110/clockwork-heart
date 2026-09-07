extends Node
## 「今天，誰需要上發條？」—— Product Lock §3.2 每日單一異常。
## Autoload：WindupDailySystem
## 每天本地日固定抽 1 組；錯過不懲罰；完成次數累計發里程碑。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const FRAG_ITEM := "windup_fragment"
const REWARD_GOLD := 25
const REWARD_DUST := 1
const REWARD_FRAG := 1

const FLAG_DAY := "windup.day"
const FLAG_CASE := "windup.case"
const FLAG_DONE := "windup.done"
const FLAG_COUNT := "windup.count"
const FLAG_UNLOCK := "windup.unlock."
const FLAG_MILE := "windup.milestone_"

## 測試用：>0 時覆寫本地日（YYYYMMDD）。正式遊玩維持 -1。
var debug_day: int = -1

const CASES: Array[Dictionary] = [
	{
		"id": "ding",
		"npc": "釘釘",
		"kind": "talk",
		"title": "釘釘的風箱停了",
		"desc": "鐵匠鋪風箱發條鬆了一夜。釘釘蹲在爐邊，錘提得動、風卻沒有。",
		"prompt": "釘釘：別站門口看。發條在爐左側，順時針兩圈。弄斷了你賠。",
		"choices": [
			{"id": "a", "label": "順時針兩圈"},
			{"id": "b", "label": "先擦淨再轉"},
		],
		"unlock": "釘釘把風箱蓋上，沒說謝謝。爐火重新咬住鐵。他丟來一塊碎齒輪：「別弄丟。」",
	},
	{
		"id": "weasel",
		"npc": "灰鼬",
		"kind": "talk",
		"title": "灰鼬的門栓鬆了",
		"desc": "城門栓發條一夜走完。灰鼬靠牆，不讓人進出，也不自己彎腰。",
		"prompt": "灰鼬：門栓在腳邊。上緊。別指望有人抱你。",
		"choices": [
			{"id": "a", "label": "蹲下去上緊門栓"},
			{"id": "b", "label": "問他要不要一起轉"},
		],
		"unlock": "灰鼬哼一聲，把門推開半掌。腳步聲從石板上傳回來。他沒看你。",
	},
	{
		"id": "sprout",
		"npc": "小芽",
		"kind": "talk",
		"title": "小芽的木劍轉不動",
		"desc": "小芽蹲在旗下，木劍發條卡死。她轉了三次，第三次咬嘴唇。",
		"prompt": "小芽：它昨天還會自己晃！你幫我看好不好？輕輕的。",
		"choices": [
			{"id": "a", "label": "輕輕轉回原位"},
			{"id": "b", "label": "讓她扶著、你轉"},
		],
		"unlock": "木劍又開始小小地晃。小芽把劍舉過頭頂：「我以後要當騎士！比獅子還大！」",
	},
	{
		"id": "starread",
		"npc": "星讀",
		"kind": "talk",
		"title": "星讀的觀星盤停一格",
		"desc": "聚魂殿觀星盤昨夜停了一格。星讀手指停在空位上，沒有責備盤。",
		"prompt": "星讀：缺的那格在東側。轉回去就好。別急著問為什麼停。",
		"choices": [
			{"id": "a", "label": "把東側那格轉回去"},
			{"id": "b", "label": "先聽她數一圈再轉"},
		],
		"unlock": "盤重新咬合，發出極輕的齒聲。星讀合上眼：「它記得路。我們只是幫它醒。」",
	},
	{
		"id": "lion_remnant",
		"npc": "獅子殘件",
		"kind": "talk",
		"title": "石獅像掉出發條",
		"desc": "石獅缺了一眼。另一眼望向內殿。眼窩裡一截發條掉在台座上。",
		"prompt": "發條還溫。塞回去，順毛轉半圈。石獅不說話。",
		"choices": [
			{"id": "a", "label": "把發條塞回眼窩"},
			{"id": "b", "label": "先對齊齒再轉半圈"},
		],
		"unlock": "石獅那隻完好的眼沒有眨。台座卻輕輕震了一下，像有人在裡面吸了一口氣。",
	},
	{
		"id": "fox_remnant",
		"npc": "狐狸殘件",
		"kind": "talk",
		"title": "白狐像耳後卡住",
		"desc": "白狐像閉著眼。香灰未冷。耳後一截發條卡在半途，轉不動也退不回。",
		"prompt": "卡住的是耳後那截。逆時針退一齒，再順回去。",
		"choices": [
			{"id": "a", "label": "逆時針退一齒再上"},
			{"id": "b", "label": "上香後再轉"},
		],
		"unlock": "發條咬回去時，白狐耳尖動了一下。香灰掉下一點。它仍閉眼。",
	},
]


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


func today_id() -> int:
	if debug_day > 0:
		return debug_day
	var d: Dictionary = Time.get_date_dict_from_system()
	return int(d.year) * 10000 + int(d.month) * 100 + int(d.day)


func _case_by_id(id: String) -> Dictionary:
	for c in CASES:
		if str(c.get("id", "")) == id:
			return c
	return {}


func _pick_id_for_day(day: int) -> String:
	var rng := RandomNumberGenerator.new()
	rng.seed = int(day) * 7919 + 31
	var idx := rng.randi_range(0, CASES.size() - 1)
	return str(CASES[idx].get("id", "ding"))


func refresh() -> void:
	var today := today_id()
	var last := int(GameState.get_flag(FLAG_DAY, 0))
	if last == today:
		if str(GameState.get_flag(FLAG_CASE, "")) == "":
			GameState.set_flag(FLAG_CASE, _pick_id_for_day(today))
		return
	GameState.set_flag(FLAG_DAY, today)
	GameState.set_flag(FLAG_CASE, _pick_id_for_day(today))
	GameState.set_flag(FLAG_DONE, false)


func todays_case() -> Dictionary:
	refresh()
	var c := _case_by_id(str(GameState.get_flag(FLAG_CASE, "")))
	if c.is_empty():
		c = CASES[0]
	return c


func is_done_today() -> bool:
	refresh()
	return bool(GameState.get_flag(FLAG_DONE, false))


func is_ready() -> bool:
	return not is_done_today()


func windup_count() -> int:
	return int(GameState.get_flag(FLAG_COUNT, 0))


func fragments() -> int:
	if Engine.get_main_loop() is SceneTree:
		var inv: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_method("count"):
			return int(inv.call("count", FRAG_ITEM))
	return 0


func is_case_unlocked(id: String) -> bool:
	return GameState.has_flag(FLAG_UNLOCK + id)


func milestone_hint() -> String:
	var n := windup_count()
	for t in [3, 7, 15, 28]:
		if n < t:
			return _t("上發條下一檔：累計 %d 次") % t
	return _t("上發條里程碑已達 28 次")


func panel_bbcode() -> String:
	refresh()
	var c := todays_case()
	var lines: PackedStringArray = []
	lines.append(_t("[b]今天，誰需要上發條？[/b]"))
	lines.append(_t("每天一件小事。錯過不罰，也不累積待辦。"))
	lines.append(_t("累計上發條 %d 次 · %s") % [windup_count(), milestone_hint()])
	lines.append("")
	lines.append("[b]%s[/b]  ·  %s" % [c.get("title", ""), c.get("npc", "")])
	lines.append(str(c.get("desc", "")))
	lines.append("")
	if is_done_today():
		lines.append(_t("[color=#4ED86A]今天這截發條已經上好。[/color]"))
	else:
		lines.append(str(c.get("prompt", "")))
	return "\n".join(lines)


func summary_line() -> String:
	refresh()
	var c := todays_case()
	if is_done_today():
		return _t("· 今天已替「%s」上過發條") % str(c.get("npc", ""))
	return _t("[color=#fc6]● 今天，誰需要上發條？ → %s[/color]") % str(c.get("title", ""))


func complete(choice_id: String = "") -> Dictionary:
	refresh()
	if is_done_today():
		return {"ok": false, "msg": _t("今天這截發條已經上好。明天再來看誰需要。")}
	var c := todays_case()
	var gold_n := REWARD_GOLD
	var dust_n := REWARD_DUST
	GameState.add_gold(gold_n)
	GameState.add_stardust(dust_n)
	var frag_ok := false
	if Engine.get_main_loop() is SceneTree:
		var inv: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_method("add_item"):
			frag_ok = bool(inv.call("add_item", FRAG_ITEM, REWARD_FRAG))
	var n := windup_count() + 1
	GameState.set_flag(FLAG_COUNT, n)
	GameState.set_flag(FLAG_DONE, true)
	## 累計次數與登入 streak 對齊，供舊面板／測試讀同一把尺
	GameState.set_flag("meta.daily_streak", n)

	var unlock_txt := ""
	var cid := str(c.get("id", ""))
	if cid != "" and not is_case_unlocked(cid):
		GameState.set_flag(FLAG_UNLOCK + cid, true)
		unlock_txt = str(c.get("unlock", ""))

	var bonus := _grant_milestones(n)
	var choice_note := ""
	for ch in c.get("choices", []):
		if str(ch.get("id", "")) == choice_id:
			choice_note = str(ch.get("label", ""))
			break

	if Engine.get_main_loop() is SceneTree:
		var sm: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("SaveManager")
		if sm and sm.has_method("save_game"):
			sm.call("save_game")

	var msg := _t("替「%s」上好發條：金 %d · 星屑 %d · 發條碎片 %d") % [
		c.get("npc", cid), gold_n, dust_n, (REWARD_FRAG if frag_ok else 0),
	]
	if choice_note != "":
		msg += " · " + choice_note
	if unlock_txt != "":
		msg += "\n" + unlock_txt
	if bonus != "":
		msg += bonus
	return {
		"ok": true,
		"gold": gold_n,
		"dust": dust_n,
		"frag": REWARD_FRAG if frag_ok else 0,
		"count": n,
		"case_id": cid,
		"unlocked": unlock_txt != "",
		"msg": msg,
	}


func _grant_milestones(n: int) -> String:
	var bonus := ""
	if n == 3 and not GameState.has_flag(FLAG_MILE + "3"):
		GameState.set_flag(FLAG_MILE + "3", true)
		GameState.add_gold(100)
		_energy_grant(5)
		bonus = _t(" · 累計 3 次：能量+5 · 金+100")
	elif n == 7 and not GameState.has_flag(FLAG_MILE + "7"):
		GameState.set_flag(FLAG_MILE + "7", true)
		GameState.add_stardust(5)
		_energy_grant(10)
		if Engine.get_main_loop() is SceneTree:
			var ar: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("ArenaSystem")
			if ar:
				GameState.arena_tickets = int(ar.get("TICKET_MAX")) if ar.get("TICKET_MAX") != null else 3
		bonus = _t(" · 累計 7 次：能量+10 · 挑戰狀補滿 · 星屑+5")
	elif n == 15 and not GameState.has_flag(FLAG_MILE + "15"):
		GameState.set_flag(FLAG_MILE + "15", true)
		GameState.add_gold(300)
		GameState.soul_free_draws += 10
		bonus = _t(" · 累計 15 次：免費抽魂×10 · 金+300")
	elif n == 28 and not GameState.has_flag(FLAG_MILE + "28"):
		GameState.set_flag(FLAG_MILE + "28", true)
		GameState.add_gold(400)
		_energy_grant(30)
		bonus = _t(" · 累計 28 次：能量+30 · 金+400")
	return bonus


func _energy_grant(n: int) -> void:
	if Engine.get_main_loop() is SceneTree:
		var es: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EnergySystem")
		if es and es.has_method("grant"):
			es.call("grant", n)
