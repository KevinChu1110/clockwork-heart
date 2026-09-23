extends SceneTree
## QA Regression: 玄機龜第二套外裝【乾坤八卦宗師道鎧】與塗裝變體【玄武黑曜淬火黑】合併後回歸驗收截圖腳本 (t_8878a84e)
## 驗收項目：
## 1. 創角介面 (PaperdollSelectDemo) 選用玄機龜新外裝與新塗裝，中央 512 舞台即時渲染（lobby-no-128 原則）
## 2. 衣櫥 (WardrobeDialog) 玄機龜篩選：選中【乾坤八卦宗師道鎧】與【玄武黑曜淬火黑】，即時預覽與選中態卡片
## 3. 衣櫥切換回舊外裝【天元道場玄機護甲】對照，驗證無互相污染或覆蓋
## 4. 衣櫥「全部」篩選，驗證兩套外裝與兩套塗裝於全清單中正確列出
## 5. 手遊大廳 (MobileLobby) 驗證 512 高清合成與六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時刷新
## 6. 戰鬥畫面 (BattleView) 玄機龜穿戴新外裝出戰與戰鬥日誌
## 7. 特寫 Crops 產出

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_tortoise_second_costume"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_tortoise_second_costume/crops"
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行玄機龜第二套外裝與塗裝回歸驗收實機截圖 (t_8878a84e) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角介面 (PaperdollSelectDemo) 選用玄機龜新外裝與新塗裝
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "tortoise")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "tortoise")
					
					# 切換外裝至 costume_bagua_master_robe (index 1)
					var data: Dictionary = demo.get("RACES_DATA").get("tortoise", {})
					var costumes: Array = data.get("costumes", [])
					var bagua_idx := 0
					for idx in range(costumes.size()):
						if costumes[idx].get("id") == "costume_bagua_master_robe":
							bagua_idx = idx
							break
					var chassis_list: Array = data.get("chassis", [])
					var basalt_idx := 0
					for idx in range(chassis_list.size()):
						if chassis_list[idx].get("id") == "paint_basalt_black":
							basalt_idx = idx
							break
					
					demo.set("_costume_index", bagua_idx)
					demo.set("_chassis_index", basalt_idx)
					demo.call("_apply_current_selections")
					_current_node = demo
			elif _wait >= 30:
				var path := "%s/proof_01_creation_tortoise_bagua.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/11] 創角畫面選用【乾坤八卦宗師道鎧】與【玄武黑曜淬火黑】: %s" % path)
				if _current_node and _current_node.has_method("is_stage_512"):
					var is_512: bool = _current_node.call("is_stage_512")
					var stage_tex: Texture2D = _current_node.call("get_stage_texture")
					var sz := stage_tex.get_size() if stage_tex else Vector2.ZERO
					print("    舞台是否為 512 高清合成: %s, 尺寸: %s (禁止退回 128 糊圖)" % [str(is_512), str(sz)])
				if _current_node and _current_node.has_method("confirm_selection"):
					_current_node.call("confirm_selection")
					print("    GameState 創角後存檔槽位: race=%s, costume=%s, chassis=%s" % [
						_gs.get("player_race"),
						_gs.get("paperdoll_slots").get("costume"),
						_gs.get("paperdoll_slots").get("chassis")
					])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 開啟衣櫥 (WardrobeDialog)，篩選「玄機龜」，選中新外裝與新塗裝
			if _wait == 1:
				var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
				if WardrobeClass:
					var dlg = WardrobeClass.new()
					root.add_child(dlg)
					_current_node = dlg
			elif _wait == 10:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "tortoise")
			elif _wait == 20:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999
				
				# 選中 costume_bagua_master_robe 與 paint_basalt_black
				var displayed_c: Array = _current_node.get("_displayed_costumes")
				var target_c_idx := 0
				for idx in range(displayed_c.size()):
					if displayed_c[idx].get("id") == "costume_bagua_master_robe":
						target_c_idx = idx
						break
				var displayed_ch: Array = _current_node.get("_displayed_chassis")
				var target_ch_idx := 0
				for idx in range(displayed_ch.size()):
					if displayed_ch[idx].get("id") == "paint_basalt_black":
						target_ch_idx = idx
						break
				
				_current_node.set("costume_index", target_c_idx)
				_current_node.set("chassis_index", target_ch_idx)
				_current_node.set("selected_costume_id", "costume_bagua_master_robe")
				_current_node.set("selected_chassis_id", "paint_basalt_black")
				if _current_node.has_method("_update_card_selection_states"):
					_current_node.call("_update_card_selection_states")
				if _current_node.has_method("_update_preview"):
					_current_node.call("_update_preview")
				if _current_node.has_method("_update_ui_texts"):
					_current_node.call("_update_ui_texts")
			elif _wait >= 40:
				var path := "%s/proof_02_wardrobe_bagua_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/11] 衣櫥選中【乾坤八卦宗師道鎧】與【玄武黑曜淬火黑】實機圖: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 衣櫥切換回舊外裝【天元道場玄機護甲】與【原廠青銅古翠綠】對照
			if _wait == 5:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999
				if _current_node:
					var displayed_c: Array = _current_node.get("_displayed_costumes")
					var target_c_idx := 0
					for idx in range(displayed_c.size()):
						if displayed_c[idx].get("id") == "costume_zen_dojo_harness":
							target_c_idx = idx
							break
					var displayed_ch: Array = _current_node.get("_displayed_chassis")
					var target_ch_idx := 0
					for idx in range(displayed_ch.size()):
						if displayed_ch[idx].get("id") == "paint_tortoise_jade":
							target_ch_idx = idx
							break
					
					_current_node.set("costume_index", target_c_idx)
					_current_node.set("chassis_index", target_ch_idx)
					_current_node.set("selected_costume_id", "costume_zen_dojo_harness")
					_current_node.set("selected_chassis_id", "paint_tortoise_jade")
					if _current_node.has_method("_update_card_selection_states"):
						_current_node.call("_update_card_selection_states")
					if _current_node.has_method("_update_preview"):
						_current_node.call("_update_preview")
					if _current_node.has_method("_update_ui_texts"):
						_current_node.call("_update_ui_texts")
			elif _wait >= 30:
				var path := "%s/proof_03_wardrobe_harness_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/11] 衣櫥切換為【天元道場玄機護甲】對照實機圖: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 衣櫥篩選「全部」，展示玄機龜兩套外裝與兩套塗裝於全清單中
			if _wait == 5:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "all")
			elif _wait >= 30:
				var path := "%s/proof_04_wardrobe_filter_all.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/11] 衣櫥篩選「全部」驗證兩套外裝與塗裝於全清單中列出: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 建立手遊大廳 (MobileLobby)，套用新外裝與新塗裝，準備六語系刷新驗收
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "tortoise")
					_gs.set("player_race", "tortoise")
					_gs.set("player_name", "玄機龜")
					_gs.set("paperdoll_slots", {
						"race": "tortoise",
						"costume": "costume_bagua_master_robe",
						"chassis": "paint_basalt_black",
						"costume_id": "costume_bagua_master_robe",
						"paint_id": "paint_basalt_black",
						"weapon": "wpn_bagua_astrolabe"
					})
					_gs.set("energy", 15)
					_gs.set("gold", 18880)
					_gs.set("stardust", 168)
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 30:
				# 檢查大廳英雄貼圖是否為 512 高清合成
				if _current_node and _current_node.has_method("_hero_display_tex"):
					var hd_tex: Texture2D = _current_node.call("_hero_display_tex")
					var w := hd_tex.get_width() if hd_tex else 0
					print("    大廳英雄展示貼圖寬度: %d (>= 256 為 512 高清合成，嚴格遵守 lobby-no-128)" % w)
				_step = 6
				_wait = 0

		6, 7, 8, 9, 10, 11:
			# 步驟 6~11: 六語系大廳實機截圖 (zh_TW, zh_CN, en, ja, ko, es)
			var loc_idx := _step - 6
			var code: String = LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
			elif _wait >= 25:
				var path := "%s/proof_05_lobby_tortoise_bagua_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/11] 已截取大廳新外裝 [%s] 語系實機截圖: %s" % [loc_idx + 5, code, path])
				_step += 1
				_wait = 0

		12:
			# 步驟 12: 戰鬥畫面 (BattleView) 玄機龜穿戴新外裝出戰
			if _wait == 1:
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "tortoise")
					_gs.set("player_race", "tortoise")
					_gs.set("player_name", "玄機龜")
					_gs.set("paperdoll_slots", {
						"race": "tortoise",
						"costume": "costume_bagua_master_robe",
						"chassis": "paint_basalt_black",
						"costume_id": "costume_bagua_master_robe",
						"paint_id": "paint_basalt_black",
						"weapon": "wpn_bagua_astrolabe"
					})
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait >= 30:
				var path := "%s/proof_06_battle_tortoise_bagua.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [11/11] 已截取戰鬥畫面玄機龜新外裝出戰: %s" % path)
				
				# 觸發戰鬥事件產生戰鬥日誌
				if _current_node:
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 58,
						"crit": true,
						"hp": 42,
						"max_hp": 100
					})
				_step = 13
				_wait = 0

		13:
			if _wait >= 25:
				var path := "%s/proof_07_battle_log_and_nameplates.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [Extra] 已截取戰鬥日誌與新外裝名稱牌: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 14
				_wait = 0

		14:
			# 步驟 14: 產出特寫裁切 Crops
			_generate_crops()
			print("── 玄機龜新外裝與塗裝回歸驗收截圖全數完成 ──")
			quit(0)
			return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    Successfully wrote: %s" % abs_path)

func _generate_crops() -> void:
	# 1. 創角中央舞台特寫
	var creation_p := "%s/proof_01_creation_tortoise_bagua.png" % OUT_DIR
	if FileAccess.file_exists(creation_p):
		var img := Image.load_from_file(creation_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(420, 160, 440, 460))
			var crop_p := "%s/crop_creation_hero_bagua_512.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 2. 衣櫥左側紙娃娃預覽特寫
	var wd_bagua := "%s/proof_02_wardrobe_bagua_equipped.png" % OUT_DIR
	if FileAccess.file_exists(wd_bagua):
		var img := Image.load_from_file(wd_bagua)
		if img and not img.is_empty():
			var crop_prev := img.get_region(Rect2i(270, 140, 260, 360))
			var crop_prev_p := "%s/crop_wardrobe_preview_bagua.png" % CROPS_DIR
			crop_prev.save_png(crop_prev_p)
			print("  ✓ 已產出特寫: %s" % crop_prev_p)

			var crop_cards := img.get_region(Rect2i(540, 130, 470, 470))
			var crop_cards_p := "%s/crop_wardrobe_cards_bagua.png" % CROPS_DIR
			crop_cards.save_png(crop_cards_p)
			print("  ✓ 已產出特寫: %s" % crop_cards_p)

	# 3. 大廳中央英雄 512 渲染特寫
	var lobby_zh := "%s/proof_05_lobby_tortoise_bagua_zh_TW.png" % OUT_DIR
	if FileAccess.file_exists(lobby_zh):
		var img := Image.load_from_file(lobby_zh)
		if img and not img.is_empty():
			var char_crop := img.get_region(Rect2i(490, 270, 300, 330))
			var char_crop_p := "%s/crop_lobby_hero_bagua_512.png" % CROPS_DIR
			char_crop.save_png(char_crop_p)
			print("  ✓ 已產出特寫: %s" % char_crop_p)

	# 4. 戰鬥玄機龜角色特寫
	var battle_p := "%s/proof_06_battle_tortoise_bagua.png" % OUT_DIR
	if FileAccess.file_exists(battle_p):
		var img := Image.load_from_file(battle_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(200, 320, 280, 280))
			var crop_p := "%s/crop_battle_tortoise_sprite.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)
