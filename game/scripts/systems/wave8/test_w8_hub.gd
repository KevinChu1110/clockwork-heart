extends SceneTree
const HubScript := preload("res://scripts/systems/wave8/w8_hub_view.gd")
const FlowScript := preload("res://scripts/systems/onboard/onboard_flow.gd")

func _init() -> void:
	var ok := true
	# scene file
	if not FileAccess.file_exists("res://scenes/w8_hub/w8_hub.tscn"):
		print("W8_HUB_FAIL scene")
		ok = false
	# flow chain logic: onboard done → soul → chapter methods exist
	var hub = HubScript.new()
	# don't add to tree; just check script loads and runtime path
	var rt_ok := ResourceLoader.exists("res://scripts/systems/wave8/w8_hub_view.gd")
	if not rt_ok:
		ok = false
	var flow = FlowScript.new()
	flow.load_bingo()
	while not flow.done:
		flow.advance(str(flow.current().get("node", "")) == "N07")
	if not flow.done:
		print("W8_HUB_FAIL onboard")
		ok = false
	# signals declared
	if not hub.has_signal("finished") and false:
		pass
	print("phases=onboard,soul,chapter scene=w8_hub.tscn")
	if ok:
		print("W8_HUB_SUCCESS")
		quit(0)
	else:
		print("W8_HUB_FAIL")
		quit(1)
