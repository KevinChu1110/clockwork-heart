extends SceneTree
## 每日委託進度來源的把關測試：godot --headless -s res://scripts/systems/test_daily_tracks.gd
##
## 守一件事：**每一種委託都有地方能推進度。**
##
## 委託池每天抽四筆；一筆的 track 沒有任何程式碼呼叫 track_day，
## 那筆就是一張永遠 0／N 的委託 —— 不報錯，玩家只會覺得「我明明做了」。
## 實際踩過：「材料回收：賣出材料累計 5 件」只有琥珀一鍵賣出會算，
## 獵場的溢物回收（玩家最常賣材料的地方）賣一整輪還是 0／5。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var qs := root.get_node_or_null("QuestSystem")
	var inv := root.get_node_or_null("InventorySystem")
	var hunt := root.get_node_or_null("HuntSystem")
	if gs == null or qs == null or inv == null or hunt == null:
		_fail("GameState／QuestSystem／InventorySystem／HuntSystem autoload missing")
		return _finish()
	gs.reset_new_game()
	qs.refresh_daily()

	## 1) 靜態：委託池每個 track 都有人呼叫 track_day("<track>"
	var srcs: PackedStringArray = []
	for path in ["res://scripts/main.gd", "res://scripts/systems/hunt_system.gd",
			"res://scripts/systems/arena_system.gd", "res://scripts/systems/inventory_system.gd",
			"res://scripts/systems/equipment_system.gd"]:
		srcs.append(FileAccess.get_file_as_string(path))
	var all_src := "\n".join(srcs)
	var tracks := {}
	for c in qs.COMMISSION_POOL:
		tracks[str(c.get("track", ""))] = str(c.get("name", ""))
	for t in tracks.keys():
		var needle := "\"%s\"" % t
		var hit := all_src.find("track_day(%s" % needle) >= 0 or all_src.find("\"track_day\", %s" % needle) >= 0
		if not hit:
			_fail("委託「%s」的 track「%s」沒有任何程式碼會推進 —— 那是一張永遠做不完的委託" % [tracks[t], t])
	print("  ok 委託池 %d 種 track 都有推進點" % tracks.size())

	## 2) 動態：溢物回收要算「賣出材料」
	inv.add_item("hunt_hide", 2)
	var before := int(qs.day_count("sell"))
	var r: Dictionary = hunt.recycle_one("hunt_hide")
	if not bool(r.get("ok", false)):
		_fail("回收溢皮失敗：%s" % str(r.get("msg", "")))
	elif int(qs.day_count("sell")) != before + 1:
		_fail("回收 1 件溢皮後「賣出材料」進度 %d → %d，應 +1" % [before, int(qs.day_count("sell"))])
	else:
		print("  ok 溢物回收 1 件 → 賣出材料 %d" % int(qs.day_count("sell")))

	## 3) 動態：琥珀一鍵賣出照樣算
	inv.add_item("wolf_fang", 3)
	before = int(qs.day_count("sell"))
	var r2: Dictionary = inv.sell_all_materials()
	if not bool(r2.get("ok", false)):
		_fail("一鍵賣出失敗：%s" % str(r2.get("msg", "")))
	elif int(qs.day_count("sell")) < before + 3:
		_fail("一鍵賣出 3 件後「賣出材料」進度 %d → %d，應至少 +3" % [before, int(qs.day_count("sell"))])
	else:
		print("  ok 一鍵賣出 %d 件 → 賣出材料 %d" % [int(r2.get("count", 0)), int(qs.day_count("sell"))])
	_finish()


func _finish() -> void:
	if _ok:
		print("DAILY_TRACKS_OK")
		quit(0)
	else:
		print("DAILY_TRACKS_FAIL")
		quit(1)
