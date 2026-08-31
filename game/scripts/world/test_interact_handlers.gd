extends SceneTree
## 探索互動 id 的把關測試：godot --headless -s res://scripts/world/test_interact_handlers.gd
##
## AGENTS.md 硬規則：「改探索實體後務必測互動 id 是否在 main.gd 有 handler」。
## 這支把那件事自動化。守三件事：
##   1. WorldTravel.links() 的每個目標地圖都建得出來、need_flag 都有人立
##   2. 每張地圖的路標（id 以 to_／back_／exit_／path_ 開頭，或標籤以「往」開頭）
##      都在 WorldTravel 表裡或 main.gd 有明確 handler —— 路標沒接就是死路
##   3. 秘境小 Boss 的 need_flag 都有人立
##
## 其餘物件沒 handler 會落到 main.gd 的檢視句（inspect_object），不算錯；
## 但那句原本用「標籤開頭是往／回／通」猜路標而直接閉嘴，
## 「回音壁」「回音階」點了完全沒反應 —— 這裡順便守住「非路標一定有話」。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _is_signpost(id: String, label: String) -> bool:
	for p in ["to_", "back_", "exit_", "path_"]:
		if id.begins_with(p):
			return true
	return label.begins_with("往")


func _initialize() -> void:
	var MapCatalogC = load("res://scripts/world/map_catalog.gd")
	var WorldTravelC = load("res://scripts/world/world_travel.gd")
	var WorldContentC = load("res://scripts/world/world_content.gd")
	var main_src: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	if main_src == "":
		_fail("讀不到 main.gd")
		return _finish()
	var links: Dictionary = WorldTravelC.links()
	var bosses: Dictionary = WorldContentC.minibosses()
	var chests: Dictionary = WorldContentC.chests()
	var sk: Dictionary = WorldContentC.skirmishes()
	var maps: PackedStringArray = WorldTravelC.list_map_ids()

	## main.gd 裡立過的旗
	var setters := {}
	var re := RegEx.new()
	re.compile("set_flag\\(\"([^\"]+)\"")
	for m in re.search_all(main_src):
		setters[m.get_string(1)] = true

	## 1) 路標表
	for lid in links:
		var l: Dictionary = links[lid]
		var target := str(l.get("map", ""))
		if not (target in maps):
			_fail("路標 %s 指向 %s，但 list_map_ids 沒有這張圖" % [lid, target])
		var mm: Dictionary = MapCatalogC.build(target)
		if mm.is_empty() or (mm.get("entities", []) as Array).is_empty():
			_fail("路標 %s 指向 %s，但 MapCatalog 建不出來" % [lid, target])
		var need := str(l.get("need_flag", ""))
		if need != "" and not setters.has(need):
			_fail("路標 %s 要旗 %s，但 main.gd 從沒立過 —— 永遠走不過去" % [lid, need])
	print("  ok %d 條路標目標地圖都在、旗都拿得到" % links.size())

	## 3) 秘境小 Boss
	for bid in bosses:
		var need := str((bosses[bid] as Dictionary).get("need_flag", ""))
		if need != "" and not setters.has(need):
			_fail("秘境 %s 要旗 %s，但 main.gd 從沒立過" % [bid, need])

	## 2) 每張圖的實體
	var total := 0
	var signposts := 0
	var main_flavor_ok := main_src.find("WorldTravel.links().has(id)") >= 0
	if not main_flavor_ok:
		_fail("main.gd 的檢視句退回不再以 WorldTravel 表判斷路標 —— 「回音壁」那類物件會點了沒反應")
	for mid in maps:
		var m: Dictionary = MapCatalogC.build(mid)
		if m.is_empty():
			_fail("MapCatalog 建不出 %s" % mid)
			continue
		for e in m.get("entities", []):
			var id := str(e.get("id", ""))
			var label := str(e.get("label", ""))
			if id == "" or (bool(e.get("solid", false)) and label == ""):
				continue
			total += 1
			var handled := links.has(id) or bosses.has(id) or chests.has(id) or sk.has(id) \
				or id.begins_with("mb_") or id.begins_with("hunt_") or id.begins_with("smob_") \
				or main_src.find("\"%s\"" % id) >= 0
			if _is_signpost(id, label):
				signposts += 1
				if not handled:
					_fail("%s／%s「%s」是路標卻沒有任何 handler —— 死路" % [mid, id, label])
			elif label == "":
				_fail("%s／%s 沒有標籤，落到檢視句會是空話" % [mid, id])
	print("  ok %d 張圖 %d 個實體、%d 個路標全部有接" % [maps.size(), total, signposts])
	_finish()


func _finish() -> void:
	if _ok:
		print("INTERACT_HANDLERS_OK")
		quit(0)
	else:
		print("INTERACT_HANDLERS_FAIL")
		quit(1)
