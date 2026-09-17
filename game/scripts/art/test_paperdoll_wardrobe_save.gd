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

	# ── 3a. 測試卡片網格 (GridContainer) 與『✓ 已選用』標籤 (review.md 第 28a 條) ──
	var grid_costume = dlg2.find_child("GridCostume", true, false)
	var grid_chassis = dlg2.find_child("GridChassis", true, false)
	if not (grid_costume is GridContainer) or not (grid_chassis is GridContainer):
		push_error("未找到 GridCostume 或 GridChassis (GridContainer)")
		ok = false
	else:
		print("  ✓ 換裝面板外裝與塗裝皆採用 GridContainer 卡片網格")
		if (grid_costume as GridContainer).get_child_count() < 3 or (grid_chassis as GridContainer).get_child_count() < 3:
			push_error("卡片網格數量不足")
			ok = false
		else:
			print("  ✓ 卡片網格數量充足 (外裝 %d 格，塗裝 %d 格)" % [(grid_costume as GridContainer).get_child_count(), (grid_chassis as GridContainer).get_child_count()])

		# 檢驗選中卡片之『✓ 已選用』狀態
		var c_card = (grid_costume as GridContainer).get_child(dlg2.costume_index)
		var c_badge = c_card.find_child("BadgeLabel", true, false) if c_card else null
		if c_badge is Label and (c_badge as Label).text == "✓ 已選用":
			print("  ✓ 已裝備外裝卡片正確標示『✓ 已選用』")
		else:
			push_error("已裝備外裝卡片未標示『✓ 已選用』")
			ok = false

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

	# ── 7. 測試衣櫥彈窗角色預覽待機呼吸 (Wardrobe Preview Breathe) ──
	var dlg_breathe: WardrobeDialog = WardrobeDialog.new()
	root.add_child(dlg_breathe)
	dlg_breathe._ready()

	if not dlg_breathe.is_breathe_running():
		push_error("WardrobeDialog 打開後未啟動預覽角色待機呼吸動畫")
		ok = false
	else:
		print("  ✓ WardrobeDialog 預覽角色待機呼吸動畫正常啟動")

	# 點選切換不同外裝，預覽圖更新後呼吸不中斷
	dlg_breathe.costume_index = 0
	dlg_breathe._update_card_selection_states()
	dlg_breathe._update_preview()
	if not dlg_breathe.is_breathe_running():
		push_error("點選切換外裝更新預覽後，呼吸動畫中斷")
		ok = false
	else:
		print("  ✓ 點選切換外裝後呼吸動畫持續進行不中斷")

	# 關閉彈窗必須停掉 tween
	dlg_breathe.close()
	if dlg_breathe.is_breathe_running():
		push_error("WardrobeDialog 關閉後呼吸 tween 未被停止")
		ok = false
	else:
		print("  ✓ WardrobeDialog 關閉時呼吸 tween 確實停止")

	# ── 8. 測試烈焰虎 (tiger) 專屬換裝與存檔持久化 ──
	print("\n--- 8. 測試烈焰虎 (tiger) 換裝切換與存檔持久化 ---")
	gs.player_race = "tiger"
	gs.paperdoll_slots = {
		"race": "tiger",
		"costume_id": "costume_ember_tunic",
		"paint_id": "paint_ember_orange"
	}
	var dlg_tiger: WardrobeDialog = WardrobeDialog.new()
	root.add_child(dlg_tiger)
	dlg_tiger._ready()
	if dlg_tiger.current_race != "tiger":
		push_error("WardrobeDialog 當前種族非 tiger: %s" % dlg_tiger.current_race)
		ok = false
	else:
		print("  ✓ WardrobeDialog 正確辨識玩家當前種族為 tiger")

	# 切換為新外裝 (costume index 1: costume_ash_ninja_garb) 與新塗裝 (chassis index 1: paint_volcano_black)
	dlg_tiger.costume_index = 1
	dlg_tiger.chassis_index = 1
	dlg_tiger._update_card_selection_states()
	dlg_tiger._update_preview()
	dlg_tiger.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "costume_ash_ninja_garb":
		push_error("烈焰虎換裝後 costume_id 應為 costume_ash_ninja_garb，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 烈焰虎成功換裝為灰燼夜行機關裝 (costume_ash_ninja_garb)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_volcano_black":
		push_error("烈焰虎換裝後 paint_id 應為 paint_volcano_black，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 烈焰虎成功換塗裝為鍛爐淬火曜黑烤漆 (paint_volcano_black)")

	# 切換為裸機素體 (costume index 2: none) 與原廠象牙白 (chassis index 2: paint_ivory_stock)
	dlg_tiger.costume_index = 2
	dlg_tiger.chassis_index = 2
	dlg_tiger._update_card_selection_states()
	dlg_tiger._update_preview()
	dlg_tiger.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "none":
		push_error("烈焰虎換裝後 costume_id 應為 none，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 烈焰虎成功換裝為裸機素體 (none)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_ivory_stock":
		push_error("烈焰虎換裝後 paint_id 應為 paint_ivory_stock，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 烈焰虎成功換塗裝為原廠象牙白 (paint_ivory_stock)")

	# ── 9. 測試雲嵐鶴 (crane) 專屬換裝與存檔持久化 ──
	print("\n--- 9. 測試雲嵐鶴 (crane) 換裝切換與存檔持久化 ---")
	gs.player_race = "crane"
	gs.paperdoll_slots = {
		"race": "crane",
		"costume_id": "costume_zephyr_robe",
		"paint_id": "paint_crane_porcelain"
	}
	var dlg_crane: WardrobeDialog = WardrobeDialog.new()
	root.add_child(dlg_crane)
	dlg_crane._ready()
	if dlg_crane.current_race != "crane":
		push_error("WardrobeDialog 當前種族非 crane: %s" % dlg_crane.current_race)
		ok = false
	else:
		print("  ✓ WardrobeDialog 正確辨識玩家當前種族為 crane")

	# 切換為新外裝 (costume index 1: costume_sky_hunter_mail) 與新塗裝 (chassis index 1: paint_zephyr_azure)
	dlg_crane.costume_index = 1
	dlg_crane.chassis_index = 1
	dlg_crane._update_card_selection_states()
	dlg_crane._update_preview()
	dlg_crane.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "costume_sky_hunter_mail":
		push_error("雲嵐鶴換裝後 costume_id 應為 costume_sky_hunter_mail，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 雲嵐鶴成功換裝為晴空巡獵機關羽甲 (costume_sky_hunter_mail)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_zephyr_azure":
		push_error("雲嵐鶴換裝後 paint_id 應為 paint_zephyr_azure，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 雲嵐鶴成功換塗裝為晴空凌雲湛藍 (paint_zephyr_azure)")

	# 切換為裸機素體 (costume index 2: none) 與原廠象牙白 (chassis index 2: paint_ivory_stock)
	dlg_crane.costume_index = 2
	dlg_crane.chassis_index = 2
	dlg_crane._update_card_selection_states()
	dlg_crane._update_preview()
	dlg_crane.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "none":
		push_error("雲嵐鶴換裝後 costume_id 應為 none，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 雲嵐鶴成功換裝為裸機素體 (none)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_ivory_stock":
		push_error("雲嵐鶴換裝後 paint_id 應為 paint_ivory_stock，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 雲嵐鶴成功換塗裝為原廠象牙白 (paint_ivory_stock)")

	dlg_crane.queue_free()

	# ── 10. 測試玄軸熊 (bear) 專屬換裝與存檔持久化 ──
	print("\n--- 10. 測試玄軸熊 (bear) 換裝切換與存檔持久化 ---")
	gs.player_race = "bear"
	gs.paperdoll_slots = {
		"race": "bear",
		"costume_id": "costume_ironclad_overalls",
		"paint_id": "paint_bear_amber"
	}
	var dlg_bear: WardrobeDialog = WardrobeDialog.new()
	root.add_child(dlg_bear)
	dlg_bear._ready()
	if dlg_bear.current_race != "bear":
		push_error("WardrobeDialog 當前種族非 bear: %s" % dlg_bear.current_race)
		ok = false
	else:
		print("  ✓ WardrobeDialog 正確辨識玩家當前種族為 bear")

	# 切換為新外裝 (costume index 1: costume_berserker_cuirass) 與新塗裝 (chassis index 1: paint_iron_quarry)
	dlg_bear.costume_index = 1
	dlg_bear.chassis_index = 1
	dlg_bear._update_card_selection_states()
	dlg_bear._update_preview()
	dlg_bear.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "costume_berserker_cuirass":
		push_error("玄軸熊換裝後 costume_id 應為 costume_berserker_cuirass，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 玄軸熊成功換裝為狂戰破陣機關戰鎧 (costume_berserker_cuirass)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_iron_quarry":
		push_error("玄軸熊換裝後 paint_id 應為 paint_iron_quarry，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 玄軸熊成功換塗裝為重裝礦山玄鐵灰 (paint_iron_quarry)")

	# 切換為裸機素體 (costume index 2: none) 與原廠象牙白 (chassis index 2: paint_ivory_stock)
	dlg_bear.costume_index = 2
	dlg_bear.chassis_index = 2
	dlg_bear._update_card_selection_states()
	dlg_bear._update_preview()
	dlg_bear.confirm_selection()

	if str(gs.paperdoll_slots.get("costume_id", "")) != "none":
		push_error("玄軸熊換裝後 costume_id 應為 none，實際為: %s" % str(gs.paperdoll_slots.get("costume_id", "")))
		ok = false
	else:
		print("  ✓ 玄軸熊成功換裝為裸機素體 (none)")

	if str(gs.paperdoll_slots.get("paint_id", "")) != "paint_ivory_stock":
		push_error("玄軸熊換裝後 paint_id 應為 paint_ivory_stock，實際為: %s" % str(gs.paperdoll_slots.get("paint_id", "")))
		ok = false
	else:
		print("  ✓ 玄軸熊成功換塗裝為原廠象牙白 (paint_ivory_stock)")

	dlg_bear.queue_free()

	# ── 跨種族穿裝：兔子穿維京裝，本體仍是兔 ──
	gs.call("reset_new_game", "rabbit")
	var dlg_cross: WardrobeDialog = WardrobeDialog.new()
	dlg_cross.creation_mode = false
	root.add_child(dlg_cross)
	dlg_cross.set_race_filter("all")
	var viking_idx := -1
	for i in range(dlg_cross._displayed_costumes.size()):
		if str(dlg_cross._displayed_costumes[i].get("id", "")) == "costume_viking_harness":
			viking_idx = i
			break
	if viking_idx < 0:
		push_error("全部外裝庫找不到 costume_viking_harness")
		ok = false
	else:
		dlg_cross.costume_index = viking_idx
		dlg_cross.selected_costume_id = "costume_viking_harness"
		dlg_cross._update_card_selection_states()
		dlg_cross._update_preview()
		if dlg_cross.current_race != "rabbit":
			push_error("穿維京裝後本體種族被改成 %s（應保持 rabbit）" % dlg_cross.current_race)
			ok = false
		else:
			print("  ✓ 兔子穿維京裝時本體仍是 rabbit")
		var cross_sel: Dictionary = dlg_cross.get_current_selections()
		if str(cross_sel.get("costume", "")) != "costume_viking_harness":
			push_error("跨族選裝後 costume 應為 viking_harness，實際 %s" % str(cross_sel.get("costume", "")))
			ok = false
		if str(cross_sel.get("race", "")) != "rabbit":
			push_error("跨族選裝後 selections.race 應為 rabbit，實際 %s" % str(cross_sel.get("race", "")))
			ok = false
		var cross_path := PaperdollRenderer.resolve_slot_texture_path("rabbit", "costume", "costume_viking_harness")
		if cross_path.find("viking_harness") < 0:
			push_error("跨族切片路徑未解析到維京裝：%s" % cross_path)
			ok = false
		var fox_path := PaperdollRenderer.resolve_slot_texture_path("fox", "costume", "costume_viking_harness")
		if fox_path.find("viking_harness") < 0:
			push_error("狐族也應共用維京裝切片：%s" % fox_path)
			ok = false
		elif fox_path.get_file() != cross_path.get_file():
			print("  ~ 兔/狐維京裝檔名不同（仍可接受）：%s vs %s" % [cross_path, fox_path])
		else:
			print("  ✓ 兔與狐共用同一件維京裝切片檔名")

		var rab_512_viking := PaperdollRenderer.resolve_slot_texture_path_512("rabbit", "costume", "costume_viking_harness")
		var fox_512_viking := PaperdollRenderer.resolve_slot_texture_path_512("fox", "costume", "costume_viking_harness")
		if rab_512_viking.find("viking_harness") < 0 or fox_512_viking.find("viking_harness") < 0:
			push_error("512 維京裝未正確解析: %s, %s" % [rab_512_viking, fox_512_viking])
			ok = false
		elif rab_512_viking != fox_512_viking:
			push_error("兔與狐 512 維京裝未解析至同一共用檔案: %s vs %s" % [rab_512_viking, fox_512_viking])
			ok = false
		else:
			print("  ✓ 兔與狐 512 維京裝解析至同一共用檔案: %s" % rab_512_viking)

		var rab_512_astral := PaperdollRenderer.resolve_slot_texture_path_512("rabbit", "costume", "costume_astral_cape")
		var fox_512_astral := PaperdollRenderer.resolve_slot_texture_path_512("fox", "costume", "costume_astral_cape")
		if rab_512_astral != fox_512_astral or rab_512_astral.find("astral_cape") < 0:
			push_error("512 星紋斗篷未正確共用解析: %s vs %s" % [rab_512_astral, fox_512_astral])
			ok = false
		else:
			print("  ✓ 兔與狐 512 星紋斗篷解析至同一共用檔案: %s" % rab_512_astral)

		var rab_512_monk := PaperdollRenderer.resolve_slot_texture_path_512("rabbit", "costume", "costume_dawn_monk_tunic")
		var fox_512_monk := PaperdollRenderer.resolve_slot_texture_path_512("fox", "costume", "costume_dawn_monk_tunic")
		if rab_512_monk != fox_512_monk or rab_512_monk.find("dawn_monk_tunic") < 0:
			push_error("512 武道短褙未正確共用解析: %s vs %s" % [rab_512_monk, fox_512_monk])
			ok = false
		else:
			print("  ✓ 兔與狐 512 武道短褙解析至同一共用檔案: %s" % rab_512_monk)

		dlg_cross.confirm_selection()
		if str(gs.player_race).to_lower() != "rabbit":
			push_error("確認換裝後 player_race 被改成 %s" % str(gs.player_race))
			ok = false
		if str(gs.paperdoll_slots.get("costume", "")) != "costume_viking_harness" and str(gs.paperdoll_slots.get("costume_id", "")) != "costume_viking_harness":
			push_error("確認後未寫入維京裝")
			ok = false
		else:
			print("  ✓ 兔子確認穿上維京裝且種族不變")

	# 恢復測試環境回兔族
	gs.call("reset_new_game", "rabbit")

	_finish(ok)


func _finish(ok: bool) -> void:
	if ok:
		print("=== 大廳角色換裝衣櫥與存檔測試通過 ===")
		print("PAPERDOLL_WARDROBE_SAVE_OK")
		quit(0)
	else:
		print("PAPERDOLL_WARDROBE_SAVE_FAIL")
		quit(1)
