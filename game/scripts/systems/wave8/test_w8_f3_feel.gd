extends SceneTree
const FlowScript := preload("res://scripts/systems/onboard/onboard_flow.gd")
const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const LoadoutScript := preload("res://scripts/systems/paper_doll_v2/character_loadout.gd")
const RuntimeScript := preload("res://scripts/systems/wave8/w8_runtime.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")

func _init() -> void:
	var notes: Array = []
	var ok := true
	# 1) onboard → N07 pull cue → N08
	var flow = FlowScript.new()
	flow.load_bingo()
	while not flow.done and str(flow.current().get("node","")) != "N07":
		flow.advance(false)
	if str(flow.current().get("node","")) != "N07":
		notes.append("FAIL onboard never reached N07")
		ok = false
	else:
		notes.append("PASS onboard to N07 cue=%s key=%s" % [str(flow.current().get("cue","")), str(flow.current().get("key",""))])
	# first pull + result card keys
	var pool = PoolScript.new()
	pool.setup(null, 99)
	var loadout = LoadoutScript.new()
	loadout.setup()
	var drop: Dictionary = pool.pull()
	loadout.apply_soul_drop(drop)
	var toast: String = str(drop.get("toastKey",""))
	if toast.find("soul.pull_") != 0 and toast.find("soul.pity_") != 0:
		notes.append("FAIL toastKey %s" % toast)
		ok = false
	else:
		notes.append("PASS first pull DropId=%s kind=%s toast=%s" % [str(drop.get("DropId","")), str(drop.get("kind","")), toast])
	# card asset
	if not FileAccess.file_exists("res://assets/sprites/pack_a/v2/ui/soul_result_card.png"):
		notes.append("FAIL result card art missing")
		ok = false
	else:
		notes.append("PASS result card art present")
	# 2) C0 first clear + sweep
	var rt = RuntimeScript.new()
	rt.setup()
	rt.daily.wind = 15
	rt.econ.soul_tickets = 5
	var fc: Dictionary = rt.do_first_clear("C0_S8")
	if not bool(fc.get("ok", false)):
		notes.append("FAIL C0 first clear %s" % str(fc))
		ok = false
	else:
		notes.append("PASS C0 first clear toast=%s gold=%s wind=%s" % [str(fc.get("toastKey","")), str(rt.econ.gold), str(fc.get("wind",""))])
	rt.daily.wind = 15
	rt.econ.gold = max(rt.econ.gold, 100)
	var sw: Dictionary = rt.do_sweep("C0_S8")
	if not bool(sw.get("ok", false)):
		notes.append("FAIL C0 sweep %s" % str(sw))
		ok = false
	else:
		notes.append("PASS C0 sweep toast=%s" % str(sw.get("toastKey","")))
	# 3) stamina regen perceptible
	rt.daily.wind = 5
	rt.daily.last_regen_unix = Time.get_unix_time_from_system() - 8 * 60 * 3
	var before: int = rt.daily.wind
	var gained: int = rt.daily.tick_regen()
	var after: int = rt.daily.wind
	if gained < 3 or after < before + 3:
		notes.append("FAIL regen gained=%d %d→%d" % [gained, before, after])
		ok = false
	else:
		notes.append("PASS regen +%d (%d→%d) at 8min/tick" % [gained, before, after])
	# scenes exist
	for p in ["res://scenes/onboard_w8/onboard_w8.tscn", "res://scenes/soul_draw/soul_draw_play.tscn", "res://scenes/s8_smoke/s8_smoke.tscn"]:
		if not FileAccess.file_exists(p) and not ResourceLoader.exists(p):
			notes.append("FAIL scene %s" % p)
			ok = false
	for n in notes:
		print(n)
	if ok:
		print("W8_F3_FEEL_SUCCESS")
		quit(0)
	else:
		print("W8_F3_FEEL_FAIL")
		quit(1)
