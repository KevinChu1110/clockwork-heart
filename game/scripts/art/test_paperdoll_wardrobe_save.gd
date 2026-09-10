extends SceneTree
## 《發條之心》大廳角色換裝衣櫥與存檔持續性測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_wardrobe_save.gd

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")


func _initialize() -> void:
	print("=== 開始大廳角色換裝衣櫥 (WardrobeDialog) 與存檔測試 ===")
	var ok := true

	# ── 1. 取得全域 GameState 與 SaveManager ──
	var gs = root.get_node_or_null("GameState")
	var sm = root.get_node_or_null("SaveManager")

	if gs == null:
		push_error("無法取得 GameState 單例")
		_finish(false)
		return
	if sm == null:
		push_error("無法取得 SaveManager 單例")
		_finish(false)
		return

	# ── 2. 測試 WardrobeDialog 實例化與手遊人體工學規格 (review.md) ──
	var dlg: WardrobeDialog = WardrobeDialog.new()
	dlg.creation_mode = false
	root.add_child(dlg)

	if not is_instance_valid(dlg):
		push_error("無法實例化 WardrobeDialog")
		_finish(false)
		return
	print("  ✓ 成功實例化 WardrobeDialog 並掛載至場景樹")

	# 檢驗彈窗寬度：橫屏彈窗 740~760px
	var card_node = dlg.get_node_or_null("DialogCard")
	if card_node is Control:
		var w: float = (card_node as Control).custom_minimum_size.x
		if w < 740.0 or w > 760.0:
			push_error("WardrobeDialog 寬度 %f 不符合 740~760px 規範" % w)
			ok = false
		else:
			print("  ✓ WardrobeDialog 彈窗寬度符合規範：%f px" % w)
	else:
		push_error("找不到 DialogCard 容器節點")
		ok = false

	# 檢驗右上關閉按鈕尺寸 >= 50px
	var close_btn = card_node.find_child("CloseBtn", true, false)
	if close_btn is Button:
		var btn_size: Vector2 = (close_btn as Button).custom_minimum_size
		if btn_size.x < 50.0 or btn_size.y < 50.0:
			push_error("關閉按鈕熱區小於 50px: %s" % str(btn_size))
			ok = false
		else:
			print("  ✓ 右上角關閉按鈕熱區符合規範：(%f, %f)" % [btn_size.x, btn_size.y])
	else:
		push_error("找不到 CloseBtn 按鈕節點")
		ok = false

	dlg.queue_free()

	# ── 3. 測試打開衣櫥時自動讀取已裝備部件 (不強制從 0 開始重置) ──
	gs.player_race = "rabbit"
	gs.chapter = "c0"
	gs.paperdoll_slots = {
		"race": "rabbit",
		"costume_id": "costume_royal_parade",
		"paint_id": "paint_midnight_navy",
		"costume": "costume_royal_parade",
		"chassis": "paint_midnight_navy"
	}

	var dlg2: WardrobeDialog = WardrobeDialog.new()
	dlg2.creation_mode = false
	root.add_child(dlg2)

	# 兔族 costumes 中 costume_royal_parade 為第 3 套 (index 2)
	# chassis 中 paint_midnight_navy 為第 3 套 (index 2)
	if dlg2.costume_index != 2:
		push_error("costume_index 未對應已裝備部件：實際 %d，預期 2" % dlg2.costume_index)
		ok = false
	else:
		print("  ✓ 打開衣櫥時正確定位已裝備外裝索引：costume_index = %d" % dlg2.costume_index)

	if dlg2.chassis_index != 2:
		push_error("chassis_index 未對應已裝備塗裝：實際 %d，預期 2" % dlg2.chassis_index)
		ok = false
	else:
		print("  ✓ 打開衣櫥時正確定位已裝備塗裝索引：chassis_index = %d" % dlg2.chassis_index)

	# ── 4. 測試換裝並確認寫回 GameState ──
	# 切換為蒸氣工匠工作裝 (index 1: costume_steam_artisan) 與黃銅原金 (index 1: paint_brass_gold)
	dlg2.costume_index = 1
	dlg2.chassis_index = 1
	dlg2.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "costume_steam_artisan":
		push_error("GameState.paperdoll_slots.costume_id 未更新為 costume_steam_artisan")
		ok = false
	else:
		print("  ✓ GameState costume_id 正確更新為 costume_steam_artisan")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_brass_gold":
		push_error("GameState.paperdoll_slots.paint_id 未更新為 paint_brass_gold")
		ok = false
	else:
		print("  ✓ GameState paint_id 正確更新為 paint_brass_gold")

	# ── 5. 測試存檔與讀檔持久化 (Save / Load Round-trip) ──
	var save_err = sm.save_game(1)
	if save_err != OK:
		push_error("SaveManager.save_game(1) 失敗，錯誤碼：%d" % save_err)
		ok = false
	else:
		print("  ✓ 換裝結果成功寫入存檔 slot 1")

	# 清空 GameState 記憶體中的 paperdoll_slots
	gs.paperdoll_slots = {}
	if not gs.paperdoll_slots.is_empty():
		push_error("無法清空記憶體中的 paperdoll_slots 進行讀檔驗證")
		ok = false

	# 重新載入存檔
	var load_err = sm.load_game(1)
	if load_err != OK:
		push_error("SaveManager.load_game(1) 失敗，錯誤碼：%d" % load_err)
		ok = false
	else:
		print("  ✓ 成功從存檔 slot 1 重新載入 GameState")

	# 斷言存檔載入後，裝備與部件完好保留
	var reloaded_costume = str(gs.paperdoll_slots.get("costume_id", gs.paperdoll_slots.get("costume", "")))
	var reloaded_paint = str(gs.paperdoll_slots.get("paint_id", gs.paperdoll_slots.get("chassis", "")))

	if reloaded_costume != "costume_steam_artisan":
		push_error("重新載入存檔後 costume_id 遺失或不符：實際 %s" % reloaded_costume)
		ok = false
	else:
		print("  ✓ 重新載入存檔後 costume_id 完好保留：%s" % reloaded_costume)

	if reloaded_paint != "paint_brass_gold":
		push_error("重新載入存檔後 paint_id 遺失或不符：實際 %s" % reloaded_paint)
		ok = false
	else:
		print("  ✓ 重新載入存檔後 paint_id 完好保留：%s" % reloaded_paint)

	# ── 6. 測試 MobileLobby 角色分頁中的更衣入口 ──
	var lobby := MobileLobby.new()
	root.add_child(lobby)
	lobby._ready()

	var btn_wardrobe = lobby.find_child("BtnWardrobe", true, false)
	if btn_wardrobe is Button:
		var btn: Button = btn_wardrobe as Button
		if btn.custom_minimum_size.y < 50.0:
			push_error("大廳更衣按鈕高度小於 50px: %f" % btn.custom_minimum_size.y)
			ok = false
		else:
			print("  ✓ 大廳角色分頁 BtnWardrobe 存在且熱區高度符合規範：%f px" % btn.custom_minimum_size.y)
	else:
		push_error("在大廳角色分頁中找不到 BtnWardrobe 按鈕")
		ok = false

	# 測試點擊 open_wardrobe() 能呼叫出 WardrobeDialog
	lobby.open_wardrobe()
	var spawned_dlg = lobby.get_node_or_null("WardrobeDialog")
	if spawned_dlg != null and spawned_dlg is WardrobeDialog:
		if bool(spawned_dlg.creation_mode) != false:
			push_error("在大廳中開啟的 WardrobeDialog 的 creation_mode 不為 false！")
			ok = false
		else:
			print("  ✓ 大廳成功開啟 WardrobeDialog 且 creation_mode 為 false (非開局選角，可重複開合)")
	else:
		push_error("open_wardrobe() 未在大廳中生成 WardrobeDialog 節點")
		ok = false

	lobby.queue_free()

	_finish(ok)


func _finish(ok: bool) -> void:
	if ok:
		print("=== 大廳角色換裝衣櫥與存檔測試通過 ===")
		print("PAPERDOLL_WARDROBE_SAVE_OK")
		quit(0)
	else:
		print("PAPERDOLL_WARDROBE_SAVE_FAIL")
		quit(1)
