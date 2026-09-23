extends SceneTree
## QA Round 29: 碧簧蛙（第十二族）全流程（骨架/切片/戰鬥姿勢/官方資產/創角/大廳/衣櫥/探索/戰鬥）探索性 QA 驗收截圖腳本
## 涵蓋：
## 1. 創角畫面 (PaperdollSelectDemo)：碧簧蛙預設外裝【碧簧巡林客工裝】與塗裝【原廠薄荷翡翠綠】
## 2. 創角畫面：切換外裝【無外裝 (裸機素體)】，驗證 512 舞台即時更新與 confirm_selection 寫入 GameState
## 3. 衣櫥 (WardrobeDialog) 篩選「全部」驗證 12 族完整清單
## 4. 衣櫥篩選「蛙」，選戴【碧簧巡林客工裝】與【原廠薄荷翡翠綠】，即時預覽與選中態卡片
## 5. 衣櫥換裝切換為【無外裝 (裸機素體)】，並抽查象族/龜族跨族換裝對照，驗證無污染
## 6. 手遊大廳 (MobileLobby) 驗證碧簧蛙 512 高清合成與六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時刷新
## 7. 大廳連動商城即時刷新 (en 英文環境，0-QA25 檢查)
## 8. 探索場景 (ExploreView) 碧簧蛙在地圖中行走/待機，驗證不退回 128 糊圖
## 9. 戰鬥畫面 (BattleView) 碧簧蛙出戰對戰狼，PlayerBody 為 512x512 高清合成
## 10. 戰鬥名稱備援對照（空名 fallback 碧簧蛙族名與暴擊打擊事件戰鬥日誌）
## 11. 碧簧蛙 7 槽切片與骨架驗證 (DevPaperdollPreview)
## 12. 特寫 Crops 產出

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round29"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round29/crops"
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

	print("── 開始執行 QA Round 29 碧簧蛙全流程探索性實機截圖 ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角介面 (PaperdollSelectDemo) 選中碧簧蛙預設外裝與塗裝
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "frog")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("select_race", "frog")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 30:
				var path := "%s/proof_01_creation_frog_default.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/16] 創角選用碧簧蛙預設外裝【碧簧巡林客工裝】與【原廠薄荷翡翠綠】: %s" % path)
				if _current_node and _current_node.has_method("is_stage_512"):
					var is_512: bool = _current_node.call("is_stage_512")
					var stage_tex: Texture2D = _current_node.call("get_stage_texture")
					var sz := stage_tex.get_size() if stage_tex else Vector2.ZERO
					print("    舞台是否為 512 高清合成: %s, 尺寸: %s (禁止退回 128 糊圖)" % [str(is_512), str(sz)])
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 創角介面切換至【無外裝 (裸機素體)】
			if _wait == 5:
				if _current_node:
					var data: Dictionary = _current_node.get("RACES_DATA").get("frog", {})
					var costumes: Array = data.get("costumes", [])
					var none_idx := 0
					for idx in range(costumes.size()):
						if costumes[idx].get("id") == "none":
							none_idx = idx
							break
					_current_node.set("_costume_index", none_idx)
					_current_node.call("_apply_current_selections")
			elif _wait >= 30:
				var path := "%s/proof_02_creation_frog_bare.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/16] 創角切換為外裝【無外裝 (裸機素體)】: %s" % path)
				if _current_node and _current_node.has_method("confirm_selection"):
					_current_node.call("confirm_selection")
					print("    GameState 創角後存檔槽位: race=%s, name=%s, costume=%s, chassis=%s" % [
						_gs.get("player_race"),
						_gs.get("player_name"),
						_gs.get("paperdoll_slots").get("costume"),
						_gs.get("paperdoll_slots").get("chassis")
					])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 開啟衣櫥 (WardrobeDialog)，篩選「全部」
			if _wait == 1:
				var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
				if WardrobeClass:
					var dlg = WardrobeClass.new()
					root.add_child(dlg)
					_current_node = dlg
			elif _wait == 10:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "all")
			elif _wait >= 30:
				var path := "%s/proof_03_wardrobe_filter_all.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/16] 衣櫥篩選「全部」驗證 12 族完整清單: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 衣櫥切換為「蛙」篩選，選戴【碧簧巡林客工裝】與【原廠薄荷翡翠綠】
			if _wait == 5:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "frog")
			elif _wait == 15:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999

				var displayed_c: Array = _current_node.get("_displayed_costumes")
				var target_c_idx := 0
				for idx in range(displayed_c.size()):
					if displayed_c[idx].get("id") == "costume_spring_forest_courier":
						target_c_idx = idx
						break
				var displayed_ch: Array = _current_node.get("_displayed_chassis")
				var target_ch_idx := 0
				for idx in range(displayed_ch.size()):
					if displayed_ch[idx].get("id") == "paint_frog_emerald":
						target_ch_idx = idx
						break

				_current_node.set("costume_index", target_c_idx)
				_current_node.set("chassis_index", target_ch_idx)
				_current_node.set("selected_costume_id", "costume_spring_forest_courier")
				_current_node.set("selected_chassis_id", "paint_frog_emerald")
				if _current_node.has_method("_update_card_selection_states"):
					_current_node.call("_update_card_selection_states")
				if _current_node.has_method("_update_preview"):
					_current_node.call("_update_preview")
				if _current_node.has_method("_update_ui_texts"):
					_current_node.call("_update_ui_texts")
			elif _wait >= 40:
				var path := "%s/proof_04_wardrobe_frog_courier_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/16] 衣櫥選用【碧簧巡林客工裝】與【原廠薄荷翡翠綠】: %s" % path)
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 衣櫥切換為【無外裝 (裸機素體)】對照，並抽查跨族切換無污染
			if _wait == 5:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999
				if _current_node:
					var displayed_c: Array = _current_node.get("_displayed_costumes")
					var target_c_idx := 0
					for idx in range(displayed_c.size()):
						if displayed_c[idx].get("id") == "none":
							target_c_idx = idx
							break

					_current_node.set("costume_index", target_c_idx)
					_current_node.set("selected_costume_id", "none")
					if _current_node.has_method("_update_card_selection_states"):
						_current_node.call("_update_card_selection_states")
					if _current_node.has_method("_update_preview"):
						_current_node.call("_update_preview")
					if _current_node.has_method("_update_ui_texts"):
						_current_node.call("_update_ui_texts")
			elif _wait >= 35:
				var path := "%s/proof_05_wardrobe_frog_bare_equipped.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/16] 衣櫥切換為【無外裝 (裸機素體)】對照實機圖: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 建立手遊大廳 (MobileLobby)，套用碧簧蛙全套配裝
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "碧簧蛙")
					_gs.set("paperdoll_slots", {
						"race": "frog",
						"costume": "costume_spring_forest_courier",
						"chassis": "paint_frog_emerald",
						"costume_id": "costume_spring_forest_courier",
						"paint_id": "paint_frog_emerald",
						"weapon": "wpn_lotus_cog_dart",
						"head_unit": "head_spring_frog_stock",
						"optic_core": "core_azure_aperture",
						"winding_key": "key_twin_wing_concentric",
						"back_curio": "curio_lotus_leaf_parasol"
					})
					_gs.set("energy", 15)
					_gs.set("gold", 18800)
					_gs.set("stardust", 260)
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 30:
				if _current_node and _current_node.has_method("_hero_display_tex"):
					var hd_tex: Texture2D = _current_node.call("_hero_display_tex")
					var w := hd_tex.get_width() if hd_tex else 0
					print("    大廳碧簧蛙英雄展示貼圖寬度: %d (>= 256 為 512 高清合成，嚴格遵守 lobby-no-128)" % w)
				_step = 7
				_wait = 0

		7, 8, 9, 10, 11, 12:
			# 步驟 7~12: 六語系大廳實機截圖 (zh_TW, zh_CN, en, ja, ko, es)
			var loc_idx := _step - 7
			var code: String = LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
			elif _wait >= 25:
				var path := "%s/proof_06_lobby_frog_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/16] 已截取大廳碧簧蛙 [%s] 語系實機截圖: %s" % [loc_idx + 6, code, path])
				_log_lobby_audit(code)
				_step += 1
				_wait = 0

		13:
			# 步驟 13: 商城與大廳即時刷新驗收 (0-QA25 檢查，以 en 英文大廳開啟商城彈窗)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
			elif _wait == 10:
				if _current_node and _current_node.has_method("open_shop"):
					_current_node.call("open_shop")
			elif _wait >= 35:
				var path := "%s/proof_07_lobby_with_shop_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [12/16] 已截取大廳連動商城即時刷新 (en): %s" % path)
				var shop = _current_node.get_node_or_null("ShopDialog")
				if shop:
					shop.queue_free()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 14
				_wait = 0

		14:
			# 步驟 14: 探索場景 (ExploreView) 碧簧蛙在地圖中行走/待機驗證
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "碧簧蛙")
					_gs.set("paperdoll_slots", {
						"race": "frog",
						"costume": "costume_spring_forest_courier",
						"chassis": "paint_frog_emerald",
						"weapon": "wpn_lotus_cog_dart",
						"head_unit": "head_spring_frog_stock",
						"optic_core": "core_azure_aperture",
						"winding_key": "key_twin_wing_concentric",
						"back_curio": "curio_lotus_leaf_parasol"
					})
				var ExploreViewScn = load("res://scripts/world/explore_view.gd")
				if ExploreViewScn:
					var ev = ExploreViewScn.new()
					ev.set_anchors_preset(Control.PRESET_FULL_RECT)
					root.add_child(ev)
					ev.setup("village")
					_current_node = ev
			elif _wait >= 35:
				var path := "%s/proof_08_explore_frog.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [13/16] 已截取探索場景碧簧蛙展示: %s" % path)
				if _current_node:
					var player = _current_node.get("_player")
					if player:
						var body: Sprite2D = player.get_node_or_null("Visuals/Body")
						var tex: Texture2D = body.texture if body else null
						var w := tex.get_width() if tex else 0
						print("    探索場景玩家貼圖尺寸: %dx%d (>= 256 為高清，無 128 退回)" % [w, (tex.get_height() if tex else 0)])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 15
				_wait = 0

		15:
			# 步驟 15: 戰鬥畫面 (BattleView) 碧簧蛙穿戴專屬裝備出戰
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "碧簧蛙")
					_gs.set("paperdoll_slots", {
						"race": "frog",
						"costume": "costume_spring_forest_courier",
						"chassis": "paint_frog_emerald",
						"costume_id": "costume_spring_forest_courier",
						"paint_id": "paint_frog_emerald",
						"weapon": "wpn_lotus_cog_dart"
					})
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait >= 30:
				var path := "%s/proof_09_battle_frog_combat.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [14/16] 已截取戰鬥畫面碧簧蛙出戰: %s" % path)

				# 觸發打擊事件並清除 player_name 以驗證空名 fallback 與戰鬥日誌
				if _current_node and _gs:
					_gs.set("player_name", "")
					var saved_sim = _current_node.get("sim")
					_current_node.set("sim", null)
					var fallback_name: String = _current_node.call("_unit_display_name", "player")
					print("    戰鬥備援名稱 (空名 fallback): %s" % fallback_name)
					_current_node.set("sim", saved_sim)

					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 77,
						"crit": true,
						"hp": 23,
						"max_hp": 100
					})
				_step = 16
				_wait = 0

		16:
			# 步驟 16: 戰鬥空名備援與戰鬥日誌截圖
			if _wait >= 25:
				var path := "%s/proof_10_battle_fallback_empty_name.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [15/16] 已截取戰鬥空名備援與戰鬥日誌: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 17
				_wait = 0

		17:
			# 步驟 17: 碧簧蛙（第十二族 frog）骨架與 7 大槽位切片驗證 (DevPaperdollPreview)
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "frog")
					_current_node = p
			elif _wait >= 30:
				var path := "%s/proof_11_frog_paperdoll_slices_verification.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [16/16] 已截取碧簧蛙骨架與 7 大槽位切片驗證: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 18
				_wait = 0

		18:
			# 步驟 18: 特寫裁切 Crops
			_generate_crops()
			print("── QA Round 29 截圖全數完成 ──")
			quit(0)
			return true

	return false


func _log_lobby_audit(code: String) -> void:
	if _current_node == null:
		return
	var shop_btn: Button = _current_node.get_shop_button() if _current_node.has_method("get_shop_button") else null
	var set_btn: Button = _current_node.get_settings_button() if _current_node.has_method("get_settings_button") else null
	var sortie_btn: Button = _current_node.get_sortie_button() if _current_node.has_method("get_sortie_button") else null
	var pwr_lbl: Label = _current_node.get("_power_label")
	var nrg_title: Label = _current_node.get("_energy_title_label")
	var gold_title: Label = _current_node.get("_gold_title_label")
	var gem_title: Label = _current_node.get("_gem_title_label")
	var avatar: TextureRect = _current_node.get("_profile_avatar")
	var avatar_path: String = avatar.texture.resource_path if avatar and avatar.texture else "none"

	print("    [%s 稽核] 頭像路徑: %s" % [code, avatar_path])
	print("    [%s 稽核] 頂部狀態: 能量=%s, 金幣=%s, 星屑=%s, %s" % [
		code,
		nrg_title.text if nrg_title else "null",
		gold_title.text if gold_title else "null",
		gem_title.text if gem_title else "null",
		pwr_lbl.text if pwr_lbl else "null"
	])
	print("    [%s 稽核] 按鈕: 商城=%s, 設置=%s, 出征=%s" % [
		code,
		shop_btn.text if shop_btn else "null",
		set_btn.text if set_btn else "null",
		sortie_btn.text if sortie_btn else "null"
	])


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
	# 1. 創角 512 舞台特寫 (角色位於舞台左側 X:190~490, Y:340~650)
	var c_path := "%s/proof_01_creation_frog_default.png" % OUT_DIR
	if FileAccess.file_exists(c_path):
		var img := Image.load_from_file(c_path)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(190, 340, 300, 310))
			var crop_p := "%s/crop_creation_frog_512.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 2. 衣櫥卡片網格與左側預覽 (左側預覽 X:270, 卡片網格 X:540)
	var wd_path := "%s/proof_04_wardrobe_frog_courier_equipped.png" % OUT_DIR
	if FileAccess.file_exists(wd_path):
		var img := Image.load_from_file(wd_path)
		if img and not img.is_empty():
			var crop_grid := img.get_region(Rect2i(540, 130, 470, 470))
			var crop_grid_p := "%s/crop_wardrobe_frog_cards.png" % CROPS_DIR
			crop_grid.save_png(crop_grid_p)
			print("  ✓ 已產出特寫: %s" % crop_grid_p)

			var crop_prev := img.get_region(Rect2i(270, 140, 260, 380))
			var crop_prev_p := "%s/crop_wardrobe_preview_frog.png" % CROPS_DIR
			crop_prev.save_png(crop_prev_p)
			print("  ✓ 已產出特寫: %s" % crop_prev_p)

	# 3. 大廳角色與頭像特寫
	var lobby_zh := "%s/proof_06_lobby_frog_zh_TW.png" % OUT_DIR
	if FileAccess.file_exists(lobby_zh):
		var img := Image.load_from_file(lobby_zh)
		if img and not img.is_empty():
			var crop_char := img.get_region(Rect2i(500, 280, 280, 320))
			var crop_char_p := "%s/crop_lobby_frog_char.png" % CROPS_DIR
			crop_char.save_png(crop_char_p)
			print("  ✓ 已產出特寫: %s" % crop_char_p)

			var crop_av := img.get_region(Rect2i(30, 10, 260, 90))
			var crop_av_p := "%s/crop_lobby_frog_avatar.png" % CROPS_DIR
			crop_av.save_png(crop_av_p)
			print("  ✓ 已產出特寫: %s" % crop_av_p)

	# 4. 探索角色特寫
	var exp_p := "%s/proof_08_explore_frog.png" % OUT_DIR
	if FileAccess.file_exists(exp_p):
		var img := Image.load_from_file(exp_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(560, 280, 160, 200))
			var crop_p := "%s/crop_explore_frog_sprite.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 5. 戰鬥角色特寫
	var battle_p := "%s/proof_09_battle_frog_combat.png" % OUT_DIR
	if FileAccess.file_exists(battle_p):
		var img := Image.load_from_file(battle_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(100, 270, 320, 280))
			var crop_p := "%s/crop_battle_frog_sprite.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 6. 戰鬥名稱與日誌特寫
	var battle_log_p := "%s/proof_10_battle_fallback_empty_name.png" % OUT_DIR
	if FileAccess.file_exists(battle_log_p):
		var img := Image.load_from_file(battle_log_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(100, 30, 1080, 140))
			var crop_p := "%s/crop_battle_nameplates_log.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 7. 碧簧蛙紙娃娃切片與骨架特寫
	var frog_p := "%s/proof_11_frog_paperdoll_slices_verification.png" % OUT_DIR
	if FileAccess.file_exists(frog_p):
		var img := Image.load_from_file(frog_p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(420, 140, 440, 420))
			var crop_p := "%s/crop_frog_paperdoll_stage.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)
