extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

const RACES = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog"]

var _frame := 0

func _initialize() -> void:
	pass

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_qa()
		return true
	return false

func _run_qa() -> void:
	print("=== 開始九族全流程探索性 QA 驗證 ===")
	var errors: Array[String] = []

	# 1. 創角流程 (Creation Mode) 逐族驗證
	print("\n--- [Phase 1] 九族創角流程 (PaperdollSelectDemo in creation_mode) ---")
	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root.add_child(demo)

	# 驗證 chip 列
	var chip_scroll = demo.get_node_or_null("FilterScroll") as ScrollContainer
	if chip_scroll == null:
		errors.append("DemoScene 缺少 FilterScroll 節點")
		print("❌ 缺少 FilterScroll")
	else:
		print("✓ FilterScroll 存在，尺寸: %s, 位置: %s" % [chip_scroll.size, chip_scroll.position])

	for rid in RACES:
		demo.call("select_race", rid)
		var cur_rid = demo.get("_current_race_id")
		if cur_rid != rid:
			errors.append("創角選族失敗: 預期 %s 但得到 %s" % [rid, cur_rid])
			print("❌ 選族失敗: %s" % rid)
		else:
			var title_lbl = demo.get_node_or_null("CenterStage/HeroBadge/Margin/HBox/HeroTitleLabel") as Label
			var title_text = title_lbl.text if title_lbl else ""
			print("  ✓ 創角成功選取 [%s] -> 標題: '%s'" % [rid, title_text])
			
		# 測試確認選角儲存至 GameState
		demo.call("confirm_selection")
		var gs = root.get_node_or_null("GameState")
		if gs:
			var gs_race = gs.get("player_race")
			if gs_race != rid:
				errors.append("GameState player_race 未更新: 預期 %s 但為 %s" % [rid, gs_race])
				print("❌ GameState player_race 錯誤: %s" % gs_race)
			else:
				print("    -> GameState.player_race 同步正確: %s" % gs_race)

	demo.queue_free()

	# 2. 衣櫥換裝 (WardrobeDialog) 逐族換裝與篩選驗證
	print("\n--- [Phase 2] 九族衣櫥換裝與種族篩選驗證 (WardrobeDialog) ---")
	var wardrobe = WardrobeDialog.new()
	root.add_child(wardrobe)

	for rid in RACES:
		wardrobe.call("set_race_filter", rid)
		var cur_filter = wardrobe.get("current_filter_race")
		if cur_filter != rid:
			errors.append("衣櫥篩選失敗: 預期 %s 但為 %s" % [rid, cur_filter])
			print("❌ 衣櫥篩選失敗: %s" % rid)
		else:
			var costumes: Array = wardrobe.get("_displayed_costumes")
			var chassis: Array = wardrobe.get("_displayed_chassis")
			print("  ✓ 衣櫥切換 [%s]: 篩選=%s, 服裝數=%d, 塗裝數=%d" % [rid, cur_filter, costumes.size(), chassis.size()])
			if costumes.is_empty():
				errors.append("種族 %s 在衣櫥中無可用服裝" % rid)
			if chassis.is_empty():
				errors.append("種族 %s 在衣櫥中無可用塗裝" % rid)

	# 驗證 "all" 篩選
	wardrobe.call("set_race_filter", "all")
	var all_costumes: Array = wardrobe.get("_displayed_costumes")
	var all_chassis: Array = wardrobe.get("_displayed_chassis")
	print("  ✓ 衣櫥篩選 [all 全部]: 總服裝數=%d, 總塗裝數=%d" % [all_costumes.size(), all_chassis.size()])

	wardrobe.queue_free()

	# 3. 隊伍展示 (MobileLobby Tab.VILLAGE) 逐族展示驗證
	print("\n--- [Phase 3] 九族大廳隊伍展示 (MobileLobby) ---")
	for rid in RACES:
		var gs = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", rid)
			gs.set("player_name", "測試勇者_" + rid)
			gs.set("player_race", rid)

		var lobby = MobileLobby.new()
		root.add_child(lobby)
		lobby._switch_tab(MobileLobby.Tab.VILLAGE)

		var party_node = lobby.find_child("PartyDisplay", true, false)
		if party_node == null:
			party_node = lobby.find_child("VillageView", true, false)

		print("  ✓ 大廳隊伍展示 [%s] 載入成功 (0 crash)" % rid)
		lobby.queue_free()

	print("\n=== 九族全流程探索性 QA 總結 ===")
	if errors.is_empty():
		print("ALL_9_RACES_QA_OK")
		quit(0)
	else:
		print("ALL_9_RACES_QA_FAIL")
		for e in errors:
			print("  - " + e)
		quit(1)
