extends SceneTree
## Headless：W8-K1 日循環／養成／經濟／關卡

const RuntimeScript := preload("res://scripts/systems/wave8/w8_runtime.gd")


func _init() -> void:
	var ok := true
	var rt = RuntimeScript.new()
	if not rt.setup():
		print("W8_K1_FAIL setup")
		quit(1)
		return
	# regen: set wind low and advance time
	rt.daily.wind = 10
	rt.daily.last_regen_unix = Time.get_unix_time_from_system() - 8 * 60 * 2
	var gained: int = rt.daily.tick_regen()
	if gained < 2 or rt.daily.wind < 12:
		print("W8_K1_FAIL regen gained=%d wind=%d" % [gained, rt.daily.wind])
		ok = false
	# first clear C0
	rt.daily.wind = 15
	var fc: Dictionary = rt.do_first_clear("C0_S8")
	if not bool(fc.get("ok", false)):
		print("W8_K1_FAIL first clear %s" % str(fc))
		ok = false
	if rt.econ.gold < 200:
		print("W8_K1_FAIL gold after clear")
		ok = false
	# enhance
	rt.inventory_parts["drop_brass_gear"] = 5
	var en: Dictionary = rt.do_enhance("weapon_main")
	if not bool(en.get("ok", false)):
		print("W8_K1_FAIL enhance %s" % str(en))
		ok = false
	# sweep
	rt.daily.wind = 15
	rt.econ.gold = max(rt.econ.gold, 100)
	var sw: Dictionary = rt.do_sweep("C0_S8")
	if not bool(sw.get("ok", false)):
		print("W8_K1_FAIL sweep %s" % str(sw))
		ok = false
	# caps
	if not rt.daily.can_soul_pull():
		print("W8_K1_FAIL soul pull gate")
		ok = false
	# formula
	var dmg: int = rt.chapters.final_damage(10, 2, 5)
	if dmg != 7:
		print("W8_K1_FAIL dmg %d" % dmg)
		ok = false
	print(JSON.stringify(rt.summary()))
	if ok:
		print("W8_K1_SUCCESS")
		quit(0)
	else:
		print("W8_K1_FAIL")
		quit(1)
