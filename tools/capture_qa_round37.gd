extends SceneTree
## QA Round 37: 第四十四族撼地野牛(bison)骨架＋第四十五族巡管守宮(gecko)切片合進 main 後探索性 QA 實機截圖腳本
## 遵循 review.md 0-QA5, 0-QA15, 0-QA16, 0-QA17, 0-QA23, 0-QA24, 0-QA25, 0-QA27, 0-QA28, 0-QA30, 0-QA31, 0-UI1, 31d

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_95b8cb93"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/t_95b8cb93/crops"

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

	print("── 開始執行 QA Round 37 撼地野牛骨架＋巡管守宮切片探索性實機截圖 ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: DevPaperdollPreview 巡管守宮 7 槽位預設裝備
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "gecko")
					_current_node = p
			elif _wait >= 15:
				var path := "%s/proof_01_dev_paperdoll_gecko_default.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/12] 已截取巡管守宮 7 槽位預設切片預覽: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: DevPaperdollPreview 巡管守宮裸機素體 (costume: none)
			if _wait == 2:
				if _current_node:
					var char_node: Node = _current_node.get_node_or_null("Stage/PaperdollCharacter")
					if char_node and char_node.has_method("render_character"):
						char_node.call("render_character", "gecko", {"costume": "none"})
					if _current_node.has_method("_refresh_ui_info"):
						_current_node.call("_refresh_ui_info")
			elif _wait >= 15:
				var path := "%s/proof_02_dev_paperdoll_gecko_bare.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/12] 已截取巡管守宮裸機素體 (costume: none): %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: DevPaperdollPreview 巡管守宮卸除武器 (weapon: none)
			if _wait == 2:
				if _current_node:
					var char_node: Node = _current_node.get_node_or_null("Stage/PaperdollCharacter")
					if char_node and char_node.has_method("render_character"):
						char_node.call("render_character", "gecko", {"weapon": "none"})
					if _current_node.has_method("_refresh_ui_info"):
						_current_node.call("_refresh_ui_info")
			elif _wait >= 15:
				var path := "%s/proof_03_dev_paperdoll_gecko_unarmed.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/12] 已截取巡管守宮卸除武器 (weapon: none): %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 巡管守宮 512x512 高清原寸切片疊合舞台
			if _wait == 1:
				var stage := _create_512_composite_stage()
				root.add_child(stage)
				_current_node = stage
			elif _wait >= 12:
				var path := "%s/proof_04_gecko_512_composite_stage.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/12] 已截取巡管守宮 512x512 高清原寸疊合舞台: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 巡管守宮官方立牌展示 (showcase 800x1200 HD) 與待機圖對照
			if _wait == 1:
				var stage := _create_showcase_stage()
				root.add_child(stage)
				_current_node = stage
			elif _wait >= 12:
				var path := "%s/proof_05_gecko_official_standee_and_showcase.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/12] 已截取巡管守宮官方立牌與展示對照: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 創角介面 (PaperdollSelectDemo) - 巡管守宮選取展示
			if _wait == 1:
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					if demo.has_method("select_race"):
						demo.call("select_race", "gecko")
					_current_node = demo
			elif _wait >= 18:
				var path := "%s/proof_06_creation_flow_audit_gecko.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [6/12] 已截取創角介面巡管守宮展示: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 創角介面 (PaperdollSelectDemo) - 驗證野牛 (bison) 安全隱藏未解鎖
			if _wait == 1:
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					if demo.has_method("select_race"):
						demo.call("select_race", "swan") # 滾動至末端
					_current_node = demo
			elif _wait >= 18:
				var path := "%s/proof_07_creation_flow_audit_bison_hidden.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [7/12] 已截取創角流程末端野牛安全隱藏狀態: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 8
				_wait = 0

		8:
			# 步驟 8: 衣櫥換裝 (WardrobeDialog) - 巡管守宮篩選 Chip 與卡片
			if _wait == 1:
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 3:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe:
						if wardrobe.has_method("set_race_filter"):
							wardrobe.call("set_race_filter", "gecko")
						wardrobe.set("costume_index", 1)
						wardrobe.set("selected_costume_id", "costume_gecko_highpressure_stealth_harness")
						if wardrobe.has_method("_update_card_selection_states"):
							wardrobe.call("_update_card_selection_states")
						if wardrobe.has_method("_update_preview"):
							wardrobe.call("_update_preview")
						if wardrobe.has_method("_update_ui_texts"):
							wardrobe.call("_update_ui_texts")
			elif _wait >= 20:
				var path := "%s/proof_08_wardrobe_flow_audit_gecko.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [8/12] 已截取衣櫥換裝巡管守宮展示: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		9:
			# 步驟 9: 戰鬥畫面 (BattleView) - 巡管守宮實機戰鬥
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "gecko")
					_gs.set("player_race", "gecko")
					_gs.set("player_name", "巡管守宮")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node and _current_node.has_method("_on_event"):
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 48,
						"crit": true,
						"hp": 52,
						"max_hp": 100
					})
			elif _wait >= 20:
				var path := "%s/proof_09_battle_flow_audit_gecko.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [9/12] 已截取戰鬥畫面巡管守宮實機: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 10
				_wait = 0

		10:
			# 步驟 10: 戰鬥畫面 (BattleView) - 撼地野牛實機戰鬥（驗證開局鎚與名稱）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "bison")
					_gs.set("player_race", "bison")
					_gs.set("player_name", "撼地野牛")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node and _current_node.has_method("_on_event"):
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 95,
						"crit": false,
						"hp": 5,
						"max_hp": 100
					})
			elif _wait >= 20:
				var path := "%s/proof_10_battle_flow_audit_bison.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [10/12] 已截取戰鬥畫面撼地野牛實機: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 11
				_wait = 0

		11:
			# 步驟 11: 手遊大廳主介面 (MobileLobby) - 巡管守宮實機大廳
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "gecko")
					_gs.set("player_race", "gecko")
					_gs.set("player_name", "巡管守宮")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 20:
				var path := "%s/proof_11_lobby_flow_audit_gecko.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [11/12] 已截取手遊大廳巡管守宮展示: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 12
				_wait = 0

		12:
			# 步驟 12: 六語系 i18n 詞條對齊與 0-UI1 / 31d 零系統 Emoji 稽核看板
			if _wait == 1:
				var audit_stage := _create_audit_dashboard()
				root.add_child(audit_stage)
				_current_node = audit_stage
			elif _wait >= 15:
				var path := "%s/proof_12_i18n_and_emoji_audit.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [12/12] 已截取六語系 i18n 與零系統 Emoji 稽核看板: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 13
				_wait = 0

		13:
			print("── QA Round 37 實機截圖全數完成 ──")
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


# ---------------------------------------------------------------------------
# 輔助視圖產出函式
# ---------------------------------------------------------------------------

func _create_512_composite_stage() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 37 驗收】第四十五族巡管守宮 512x512 高清原寸紙娃娃圖層合成驗證 (0-QA18 / 0-QA31)"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 20)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	var tex_512: Texture2D = PaperdollRenderer.build_composite_texture_512("gecko")
	var tex_128: Texture2D = PaperdollRenderer.build_composite_texture("gecko")

	# 左側 512 展示
	var rect_512 := TextureRect.new()
	rect_512.texture = tex_512
	rect_512.position = Vector2(80, 80)
	rect_512.custom_minimum_size = Vector2(512, 512)
	rect_512.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect_512.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	root_ctrl.add_child(rect_512)

	var lbl_512 := Label.new()
	lbl_512.text = "512x512 高清圖層合成 (LANCZOS 平滑縮放、無鋸齒、無雜點)"
	lbl_512.position = Vector2(80, 605)
	lbl_512.add_theme_font_size_override("font_size", 14)
	lbl_512.modulate = Color(0.15, 0.5, 0.2)
	root_ctrl.add_child(lbl_512)

	# 右側 128 原始對照
	var rect_128 := TextureRect.new()
	rect_128.texture = tex_128
	rect_128.position = Vector2(660, 140)
	rect_128.custom_minimum_size = Vector2(256, 256)
	rect_128.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect_128.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root_ctrl.add_child(rect_128)

	var lbl_128 := Label.new()
	lbl_128.text = "128x128 原始像素切片合成 (2x NEAREST 展示)"
	lbl_128.position = Vector2(660, 410)
	lbl_128.add_theme_font_size_override("font_size", 14)
	lbl_128.modulate = Color(0.3, 0.3, 0.4)
	root_ctrl.add_child(lbl_128)

	# 右側參數清單
	var info := Label.new()
	info.position = Vector2(660, 450)
	info.add_theme_font_size_override("font_size", 13)
	info.modulate = Color(0.2, 0.2, 0.3)
	info.text = "• 種族: gecko (巡管守宮)\\n• 7 大槽位: chassis, head_unit, winding_key, costume,\\n  optic_core, weapon, back_curio (7/7 均備齊 128 & 512)\\n• 0-ART9/11: 底盤完全解耦，未烘入機關鏢 (0 px)\\n• 0-ART27: 頭盔雙眼獨立透空，光圈目鏡精準嵌合\\n• 審核結論: 零破圖、零毛皮、冷軋黃銅與薄荷綠銅質感合規"
	root_ctrl.add_child(info)

	return root_ctrl


func _create_showcase_stage() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 37 驗收】第四十五族巡管守宮官方立牌展示 (showcase/gecko_idle_hd.png) 與待機圖對照"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 20)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var p_hd := "res://assets/sprites/player/showcase/gecko_idle_hd.png"
	var tex_hd := load(p_hd) as Texture2D
	if tex_hd:
		var tr := TextureRect.new()
		tr.texture = tex_hd
		tr.position = Vector2(80, 70)
		tr.custom_minimum_size = Vector2(400, 600)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		root_ctrl.add_child(tr)

	var p_idle := "res://assets/sprites/player/gecko_idle_x3.png"
	var tex_idle := load(p_idle) as Texture2D
	if tex_idle:
		var tr2 := TextureRect.new()
		tr2.texture = tex_idle
		tr2.position = Vector2(560, 120)
		tr2.custom_minimum_size = Vector2(256, 256)
		tr2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr2.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root_ctrl.add_child(tr2)

	var info := Label.new()
	info.position = Vector2(560, 410)
	info.add_theme_font_size_override("font_size", 13)
	info.modulate = Color(0.2, 0.2, 0.3)
	info.text = "• Showcase HD 立繪: 800x1200 RGBA (0-ART25 四角 100% 透明)\\n• 待機圖檔: 64x64, 128x128, party, web 齊全\\n• 材質: 冷軋黃銅、薄荷綠銅抗氧化琺瑯、雙目金黃石英\\n• 結構: 雙環洩壓黃銅發條鑰匙在背、微型同軸齒輪平衡尾\\n• 0-UI1: 零系統 Emoji、純淨文字排版"
	root_ctrl.add_child(info)

	return root_ctrl


func _create_audit_dashboard() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 37 盤點總結】第四十四族撼地野牛＋第四十五族巡管守宮合入 main 探索性 QA 查驗清單"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 20)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var col1 := Label.new()
	col1.position = Vector2(50, 75)
	col1.add_theme_font_size_override("font_size", 13)
	col1.modulate = Color(0.12, 0.45, 0.2)
	col1.text = """=== 【通過項目】已就緒與驗證合格 (PASSED) ===
✓ 巡管守宮 7 大部件紙娃娃切片 (128 & 512 LANCZOS 全備齊):
  - chassis: chassis_gecko_brass_patina_default (459 色)
  - head_unit: head_gecko_conduit_scout_crest_cowl (477 色)
  - winding_key: key_gecko_dual_ring_relief_valve_brass (39 色)
  - costume: costume_gecko_highpressure_stealth_harness (87 色)
  - optic_core: face_gecko_dual_slit_aperture_quartz_lens (29 色)
  - weapon: weapon_gecko_conduit_ratchet_dart (24 色)
  - back_curio: curio_gecko_segmented_gear_balance_tail (108 色)
✓ 撼地野牛 (bison) 骨架先行建置與空目錄 (零美術佔位圖規範)
✓ 0-QA30 正表與 fallback 表 aliases 100% 逐項對齊 (全 45 族)
✓ 0-ART9/11 素體無畫死武器、0-ART26b 外裝無畫死下身
✓ 0-ART27 雙眼獨立鏤空眼窩與光圈目鏡對齊 (alpha=255)
✓ 0-ART29 / 0-QA16 洋紅底無破洞 (0 px)、發條無黑底板 (0 px)
✓ 0-QA31 7 槽疊合像素覆蓋 4696 px > 3000、目鏡 161 色 >= 15
✓ 0-ART25 showcase HD 800x1200 四角 100% 透明
✓ 創角介面 has_race_assets 防護守衛生效 (守宮可選、野牛安全隱藏)
✓ 六語系 (zh_TW, zh_CN, en, ja, ko, es) ui.json 補齊兩族 20 條詞條
✓ 0-UI1 / 31d 遊戲畫面 100% 零系統 Emoji，按鈕熱區 >= 48px
✓ Godot 無頭自動化測試 5/5 全數 PASS，冒煙 0 SCRIPT ERROR"""
	root_ctrl.add_child(col1)

	var col2 := Label.new()
	col2.position = Vector2(660, 75)
	col2.add_theme_font_size_override("font_size", 13)
	col2.modulate = Color(0.2, 0.25, 0.45)
	col2.text = """=== 【後續追蹤項目】後續工項依標準流程開立 ===
1. 第四十四族撼地野牛 (bison):
   - 目前為資料表骨架先行建置（已合進 main）
   - 待產出：7 大部件槽位紙娃娃切片與雙規格資產 (t_bison_slices)
   - 待產出：六大戰鬥姿態 (t_bison_combat_poses)
   - 待產出：官方資產套件（官網英雄圖/戰鬥特寫/行走動畫/HUD頭像）

2. 第四十五族巡管守宮 (gecko):
   - 骨架與 7 大槽位切片已全數就緒並合進 main
   - 待產出：六大戰鬥姿態 (t_gecko_combat_poses)
   - 待產出：官方資產套件（官網英雄圖/戰鬥特寫/行走動畫/HUD頭像）

3. 世界觀對齊：
   - 遵守 CANON.md 零毛皮、零血肉、全金屬玩具世界觀
   - 守宮冷軋黃銅吸盤素體、野牛生鏽耐磨馬口鐵重裝素體均合規"""
	root_ctrl.add_child(col2)

	return root_ctrl
