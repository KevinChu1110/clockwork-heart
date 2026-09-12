extends SceneTree
const FlowScript := preload("res://scripts/systems/onboard/onboard_flow.gd")

func _init() -> void:
	var ok := true
	var f = FlowScript.new()
	if not f.load_bingo():
		print("ONBOARD_FAIL load")
		quit(1)
		return
	if str(f.current().get("key", "")) != "onb.n01":
		print("ONBOARD_FAIL n01")
		ok = false
	# cannot skip N05
	while str(f.current().get("node", "")) != "N05" and not f.done:
		f.advance(false)
	if f.can_skip_current():
		print("ONBOARD_FAIL N05 skippable")
		ok = false
	f.advance(false) # N06
	f.advance(false) # N07
	if not f.can_skip_current():
		print("ONBOARD_FAIL N07 not skippable")
		ok = false
	f.advance(true) # skip to N08
	if str(f.current().get("node", "")) != "N08":
		print("ONBOARD_FAIL after skip %s" % str(f.current()))
		ok = false
	f.advance(false)
	if not f.done:
		print("ONBOARD_FAIL not done")
		ok = false
	# assets
	for p in [
		"res://assets/sprites/pack_a/v2/ui/soul_result_card.png",
		"res://scenes/soul_draw/soul_draw_play.tscn",
		"res://scenes/onboard_w8/onboard_w8.tscn",
	]:
		if not FileAccess.file_exists(p) and not ResourceLoader.exists(p):
			print("ONBOARD_FAIL missing %s" % p)
			ok = false
	if ok:
		print("ONBOARD_SOULDRAW_UI_SUCCESS")
		quit(0)
	else:
		print("ONBOARD_SOULDRAW_UI_FAIL")
		quit(1)
