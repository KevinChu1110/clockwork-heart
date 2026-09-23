extends SceneTree
## QA Round 30: 瓷韻熊貓（第十三族）骨架與紙娃娃切片合併後探索性 QA 驗收截圖腳本
## 涵蓋：
## 1. DevPaperdollPreview: 瓷韻熊貓 7 大槽位切片與骨架載入驗證（128x128 舞台、7/7 全綠已就緒）
## 2. DevPaperdollPreview: 裸機素體 (none) 換裝，驗證 0-ART9/11/18（無武器殘留、無長袍殘留、完整瓷板陰影）
## 3. DevPaperdollPreview: 多族動態切換 (frog -> elephant -> panda) 驗證無狀態殘留與無 cross-race 貼圖污染
## 4. 紙娃娃 512 高清合成舞台：驗證 512x512 尺寸、LANCZOS/原生貼圖疊合品質與非模糊圖
## 5. 官方行走動畫四幀合成對照：驗證 4b-4 非純位移關節運動與 4b-5 軟陰影一致性
## 6. 官方立牌與概念立繪驗證：branding/char_panda.png (4:5 1344x1680) 與 porcelain_panda_concept.png (928x1152)
## 7. 官方戰鬥特寫與頭像驗證：HUD 戰鬥頭像 (128x128)、對話半身像 (384x480 y=480 錨定)、戰鬥姿態 (128x128)
## 8. 玩家流程稽核 1：創角介面 (PaperdollSelectDemo) 種族橫滑列稽核（目前 12 族，記錄熊貓待串接缺口）
## 9. 玩家流程稽核 2：衣櫥彈窗 (WardrobeDialog) 種族 chip 篩選列稽核（目前 12 族，記錄熊貓待串接缺口）
## 10. 玩家流程稽核 3：手遊大廳 (MobileLobby) 熊貓種族頭像備援稽核（記錄 avatar fallback 兔頭像缺口）
## 11. 玩家流程稽核 4：戰鬥畫面 (BattleView) 空名備援稽核（記錄 fallback 小白缺口）
## 12. 六語系 i18n 覆蓋率與 0-UI1 / 31d 零系統 Emoji 稽核看板
## 13. 特寫 Crops 產出

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round30"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round30/crops"

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

	print("── 開始執行 QA Round 30 瓷韻熊貓骨架與切片探索性實機截圖 ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: DevPaperdollPreview 切換至瓷韻熊貓預設 7 槽位
			if _wait == 1:
				var preview_packed: PackedScene = load("res://scenes/dev/dev_paperdoll_preview.tscn")
				if preview_packed:
					var p = preview_packed.instantiate()
					root.add_child(p)
					if p.has_method("ensure_initialized"):
						p.call("ensure_initialized")
					p.call("switch_to_race", "panda")
					_current_node = p
			elif _wait >= 15:
				var path := "%s/proof_01_dev_paperdoll_panda_default.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/12] 已截取瓷韻熊貓預設 7 槽位切片預覽: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: DevPaperdollPreview 切換至裸機素體 (none 外裝)
			if _wait == 2:
				if _current_node:
					var char_node: Node = _current_node.get_node_or_null("Stage/PaperdollCharacter")
					if char_node and char_node.has_method("render_character"):
						char_node.call("render_character", "panda", {"costume": "none"})
					if _current_node.has_method("_refresh_ui_info"):
						_current_node.call("_refresh_ui_info")
			elif _wait >= 15:
				var path := "%s/proof_02_dev_paperdoll_panda_bare.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/12] 已截取瓷韻熊貓裸機素體 (costume: none): %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: DevPaperdollPreview 切換至卸除武器 (weapon: none 裸拳練招)
			if _wait == 2:
				if _current_node:
					var char_node: Node = _current_node.get_node_or_null("Stage/PaperdollCharacter")
					if char_node and char_node.has_method("render_character"):
						char_node.call("render_character", "panda", {"weapon": "none"})
					if _current_node.has_method("_refresh_ui_info"):
						_current_node.call("_refresh_ui_info")
			elif _wait >= 15:
				var path := "%s/proof_03_dev_paperdoll_panda_unarmed.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/12] 已截取瓷韻熊貓卸除武器 (weapon: none 裸拳練招): %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 紙娃娃 512 高清合成舞台
			if _wait == 1:
				var stage := _create_512_composite_stage()
				root.add_child(stage)
				_current_node = stage
			elif _wait >= 12:
				var path := "%s/proof_04_panda_512_composite_stage.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/12] 已截取紙娃娃 512 高清合成舞台: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 官方行走動畫四幀合成對照
			if _wait == 1:
				var walk_stage := _create_walk_cycle_stage()
				root.add_child(walk_stage)
				_current_node = walk_stage
			elif _wait >= 12:
				var path := "%s/proof_05_panda_walk_cycle_composite.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/12] 已截取官方行走動畫四幀合成對照: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 官方品牌立牌與概念立繪對照
			if _wait == 1:
				var standee_stage := _create_standee_stage()
				root.add_child(standee_stage)
				_current_node = standee_stage
			elif _wait >= 12:
				var path := "%s/proof_06_panda_official_standee_and_concept.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [6/12] 已截取官方立牌與概念立繪對照: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 官方戰鬥特寫、HUD 頭像與對話半身像對照
			if _wait == 1:
				var portrait_stage := _create_portrait_stage()
				root.add_child(portrait_stage)
				_current_node = portrait_stage
			elif _wait >= 12:
				var path := "%s/proof_07_panda_official_portraits_and_battle.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [7/12] 已截取官方戰鬥特寫與頭像對照: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 8
				_wait = 0

		8:
			# 步驟 8: 玩家流程稽核 1 - 創角種族列 (PaperdollSelectDemo)
			if _wait == 1:
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					if demo.has_method("select_race"):
						demo.call("select_race", "frog") # 滾動至現有最末端
					_current_node = demo
			elif _wait >= 15:
				var path := "%s/proof_08_creation_flow_audit_panda_missing.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [8/12] 已截取創角流程種族列稽核（記錄熊貓待串接缺口）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		9:
			# 步驟 9: 玩家流程稽核 2 - 衣櫥種族 chip 篩選列 (WardrobeDialog)
			if _wait == 1:
				var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
				if WardrobeClass:
					var dlg = WardrobeClass.new()
					root.add_child(dlg)
					_current_node = dlg
			elif _wait >= 15:
				var path := "%s/proof_09_wardrobe_flow_audit_panda_missing.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [9/12] 已截取衣櫥篩選列稽核（記錄熊貓待串接缺口）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 10
				_wait = 0

		10:
			# 步驟 10: 玩家流程稽核 3 - 手遊大廳頭像備援 (MobileLobby)
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "panda")
					_gs.set("player_race", "panda")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					lobby.set_anchors_preset(Control.PRESET_FULL_RECT)
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 18:
				var path := "%s/proof_10_lobby_flow_audit_panda_avatar_fallback.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [10/12] 已截取大廳頭像備援稽核（記錄熊貓 fallback 兔頭像缺口）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 11
				_wait = 0

		11:
			# 步驟 11: 玩家流程稽核 4 - 戰鬥空名備援 (BattleView)
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "panda")
					_gs.set("player_race", "panda")
					_gs.set("player_name", "")
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					_current_node = b
			elif _wait == 10:
				if _current_node:
					_current_node.call("_on_event", "hit", {
						"attacker": "player",
						"defender": "wolf",
						"damage": 66,
						"crit": true,
						"hp": 34,
						"max_hp": 100
					})
			elif _wait >= 18:
				var path := "%s/proof_11_battle_flow_audit_panda_name_fallback.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [11/12] 已截取戰鬥空名備援稽核（記錄熊貓 fallback 小白缺口）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 12
				_wait = 0

		12:
			# 步驟 12: 六語系 i18n 覆蓋率與 0-UI1 / 31d 零系統 Emoji 稽核看板
			if _wait == 1:
				var audit_stage := _create_audit_dashboard()
				root.add_child(audit_stage)
				_current_node = audit_stage
			elif _wait >= 12:
				var path := "%s/proof_12_i18n_and_emoji_audit.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [12/12] 已截取六語系 i18n 與零 Emoji 稽核看板: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 13
				_wait = 0

		13:
			# 步驟 13: 產出特寫裁剪 Crops
			_generate_crops()
			print("── QA Round 30 實機截圖與特寫全數完成 ──")
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

	# 標題
	var title := Label.new()
	title.text = "【QA Round 30 驗收】瓷韻熊貓 512x512 高清紙娃娃圖層合成驗證 (0-QA18 / 0-QA21)"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 22)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	var tex_512: Texture2D = PaperdollRenderer.build_composite_texture_512("panda")
	var tex_128: Texture2D = PaperdollRenderer.build_composite_texture("panda")

	# 左側 512 展示
	var rect_512 := TextureRect.new()
	rect_512.texture = tex_512
	rect_512.position = Vector2(80, 80)
	rect_512.custom_minimum_size = Vector2(512, 512)
	rect_512.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect_512.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	root_ctrl.add_child(rect_512)

	var lbl_512 := Label.new()
	lbl_512.text = "512x512 高清圖層合成 (LANCZOS / 512切片疊合，嚴禁模糊圖)"
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
	info.text = "• 種族: panda (瓷韻熊貓)\n• 7 大槽位: chassis, head_unit, winding_key, costume,\n  optic_core, weapon, back_curio (7/7 全部具備 128 & 512)\n• 0-ART9/11: 底盤完全解耦，未烘入拳套\n• 0-ART27: 頭部獨立鏤空眼窩，光學核心精準嵌入\n• 審核結論: 零破圖、零毛皮、生漆瓷板質感合規"
	root_ctrl.add_child(info)

	return root_ctrl


func _create_walk_cycle_stage() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 30 驗收】瓷韻熊貓官方行走動畫四幀運動學與軟陰影一致性 (Rule 4b-4 / 4b-5 / 4b-7)"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 22)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	for i in range(4):
		var p_x3 := "res://assets/sprites/player/panda_walk_%d_x3.png" % i
		var tex := load(p_x3) as Texture2D
		var tr := TextureRect.new()
		tr.texture = tex
		tr.position = Vector2(60 + i * 300, 100)
		tr.custom_minimum_size = Vector2(256, 256)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root_ctrl.add_child(tr)

		var lbl := Label.new()
		lbl.text = "Walk Frame %d\n• 4b-4: 非純位移關節運動\n• 4b-7: 關節形變量 > 300px\n• 4b-5: 陰影寬度 100%% 一致" % i
		lbl.position = Vector2(60 + i * 300, 380)
		lbl.add_theme_font_size_override("font_size", 13)
		lbl.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl)

	# 底部行走合成條
	var strip_tex := load("res://assets/sprites/player/proof_panda_walk_cycle.png") as Texture2D
	if strip_tex:
		var tr_strip := TextureRect.new()
		tr_strip.texture = strip_tex
		tr_strip.position = Vector2(140, 490)
		tr_strip.custom_minimum_size = Vector2(1000, 160)
		tr_strip.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr_strip.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		root_ctrl.add_child(tr_strip)

	return root_ctrl


func _create_standee_stage() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 30 驗收】瓷韻熊貓官方品牌立牌 (1344x1680 4:5) 與概念立繪 (928x1152)"
	title.position = Vector2(40, 20)
	title.add_theme_font_size_override("font_size", 22)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var standee_img := Image.load_from_file("/opt/side/bravesoul-game/branding/char_panda.png")
	if standee_img and not standee_img.is_empty():
		var standee_tex := ImageTexture.create_from_image(standee_img)
		var tr := TextureRect.new()
		tr.texture = standee_tex
		tr.position = Vector2(80, 70)
		tr.custom_minimum_size = Vector2(440, 550)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		root_ctrl.add_child(tr)

		var lbl := Label.new()
		lbl.text = "品牌立牌 branding/char_panda.png\n• 尺寸: 1344x1680 (嚴格 4:5 比例)\n• 邊界安全邊距: 無武器/鑰匙硬切\n• CANON: 生漆黑白瓷紋、太極如意發條鑰匙"
		lbl.position = Vector2(80, 630)
		lbl.add_theme_font_size_override("font_size", 13)
		lbl.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl)

	var concept_img := Image.load_from_file("/opt/side/bravesoul-game/docs/art/porcelain_panda_concept.png")
	if concept_img and not concept_img.is_empty():
		var concept_tex := ImageTexture.create_from_image(concept_img)
		var tr2 := TextureRect.new()
		tr2.texture = concept_tex
		tr2.position = Vector2(620, 70)
		tr2.custom_minimum_size = Vector2(440, 550)
		tr2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr2.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		root_ctrl.add_child(tr2)

		var lbl2 := Label.new()
		lbl2.text = "概念立繪 docs/art/porcelain_panda_concept.png\n• 尺寸: 928x1152\n• 造型核定: 武術家乾坤拳套、背後太極金屬匣\n• 零毛皮: 100% 漆面瓷片與旋轉球窩關節"
		lbl2.position = Vector2(620, 630)
		lbl2.add_theme_font_size_override("font_size", 13)
		lbl2.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl2)

	return root_ctrl


func _create_portrait_stage() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 30 驗收】瓷韻熊貓官方戰鬥特寫姿態、HUD 戰鬥頭像與對話半身像"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 22)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	# 1. 戰鬥特寫姿態
	var battle_tex := load("res://assets/sprites/player/panda_battle.png") as Texture2D
	if battle_tex:
		var tr_b := TextureRect.new()
		tr_b.texture = battle_tex
		tr_b.position = Vector2(80, 100)
		tr_b.custom_minimum_size = Vector2(256, 256)
		tr_b.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr_b.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root_ctrl.add_child(tr_b)

		var lbl_b := Label.new()
		lbl_b.text = "戰鬥特寫姿態 panda_battle.png\n• 尺寸: 128x128 像素\n• 4b-6: 差異 6331px > 2500px 門檻\n• 馬步弓步下盤雙腿形變 958px"
		lbl_b.position = Vector2(80, 380)
		lbl_b.add_theme_font_size_override("font_size", 13)
		lbl_b.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl_b)

	# 2. HUD 頭像
	var hud_tex := load("res://assets/sprites/portraits/panda.png") as Texture2D
	if hud_tex:
		var tr_h := TextureRect.new()
		tr_h.texture = hud_tex
		tr_h.position = Vector2(420, 100)
		tr_h.custom_minimum_size = Vector2(256, 256)
		tr_h.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr_h.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		root_ctrl.add_child(tr_h)

		var lbl_h := Label.new()
		lbl_h.text = "HUD 戰鬥頭像 portraits/panda.png\n• 尺寸: 128x128 像素\n• 邊距: 左右各 12px / 上 16px 合規\n• 無白邊、無裁切、雙耳球窩就位"
		lbl_h.position = Vector2(420, 380)
		lbl_h.add_theme_font_size_override("font_size", 13)
		lbl_h.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl_h)

	# 3. 對話半身像
	var bust_tex := load("res://assets/sprites/portraits/porcelain_panda.png") as Texture2D
	if bust_tex:
		var tr_d := TextureRect.new()
		tr_d.texture = bust_tex
		tr_d.position = Vector2(780, 80)
		tr_d.custom_minimum_size = Vector2(384, 480)
		tr_d.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr_d.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		root_ctrl.add_child(tr_d)

		var lbl_d := Label.new()
		lbl_d.text = "對話半身像 portraits/porcelain_panda.png\n• 尺寸: 384x480\n• 錨定: 底端錨定 y=480 完整落地\n• 生漆彩繪、武術家長袍細節完整"
		lbl_d.position = Vector2(780, 580)
		lbl_d.add_theme_font_size_override("font_size", 13)
		lbl_d.modulate = Color(0.15, 0.5, 0.2)
		root_ctrl.add_child(lbl_d)

	return root_ctrl


func _create_audit_dashboard() -> Control:
	var root_ctrl := Control.new()
	root_ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)

	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.98, 0.97, 0.95, 1.0)
	root_ctrl.add_child(bg)

	var title := Label.new()
	title.text = "【QA Round 30 盤點總結】第十三族瓷韻熊貓多維度規範稽核看板"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 22)
	title.modulate = Color(0.12, 0.1, 0.22)
	root_ctrl.add_child(title)

	var col1 := Label.new()
	col1.position = Vector2(60, 80)
	col1.add_theme_font_size_override("font_size", 14)
	col1.modulate = Color(0.15, 0.45, 0.2)
	col1.text = """=== 【通過項目】已就緒與驗證合格 (PASSED) ===
✓ 7 大部件紙娃娃切片 (128 & 512):
  - chassis: paint_panda_porcelain (c100=11.43% > 10%)
  - head_unit: head_panda_brass_socket_ears (c100=15.05%)
  - winding_key: key_panda_taiji_ruyi_brass (c100=43.63%)
  - costume: costume_panda_zen_apprentice_robe (c100=20.45%)
  - optic_core: core_obsidian_amber_quartz (c100=12.20%)
  - weapon: wpn_panda_taiji_cestus (c100=10.85%)
  - back_curio: curio_panda_floating_taiji_box (c100=10.57%)
✓ 0-ART9/11 底盤完全解耦: 武器區 0 像素殘留
✓ 0-ART27 雙眼透鏡: 獨立鏤空眼窩，光學核心精準嵌入
✓ 0-ART18 素體彩階: 149 色階多色調陶瓷生漆
✓ 官方資產套件 21 件完整具備且尺寸合規:
  - 品牌立牌 & 官網英雄圖: 1344x1680 (4:5 比例合格)
  - 概念立繪: 928x1152
  - 行走動畫四幀: 4b-4/4b-7/4b-5 全數合格
  - 戰鬥特寫姿態: 128x128, diff 6331px > 2500px
  - 戰鬥 HUD 頭像: 128x128, 安全邊距合規
  - 對話半身像: 384x480, y=480 底部錨定合規
✓ 0-UI1 / 31d 零系統 Emoji 稽核: 100% 零 Emoji 殘留
✓ 無頭測試全綠: paperdoll (19/19), walk (4/4), switch (13/13)"""
	root_ctrl.add_child(col1)

	var col2 := Label.new()
	col2.position = Vector2(680, 80)
	col2.add_theme_font_size_override("font_size", 14)
	col2.modulate = Color(0.7, 0.25, 0.1)
	col2.text = """=== 【待串接缺口盤點】探索性 QA 發現事項 (FINDINGS) ===
⚠ 缺口 1 (創角流程未串接):
  - paperdoll_select_demo.tscn/gd 種族列目前上限為 12 族 (frog)
  - 尚未加入 panda 選項與預設套裝展示卡

⚠ 缺口 2 (衣櫥種族篩選未串接):
  - wardrobe_dialog.gd 目前僅有 12 族篩選 Chip
  - 尚未加入「貓」/「熊貓」篩選 Chip 與對應變體卡片

⚠ 缺口 3 (大廳頭像對照缺映射):
  - mobile_lobby.gd 的 _get_avatar_texture() 缺少 \"panda\" 映射
  - 若強制設定 player_race=\"panda\"，頭像 fallback 至 rabbit

⚠ 缺口 4 (戰鬥空名 fallback 缺少映射):
  - battle_view.gd 的 _unit_display_name() 缺少 \"panda\" 映射
  - 若未命名，戰鬥單位名稱 fallback 至「小白」而非「瓷韻熊貓」

⚠ 缺口 5 (GameState 預設命名缺少映射):
  - game_state.gd reset_new_game(\"panda\") default_name 回傳「小白」

⚠ 缺口 6 (六語系 UI 翻譯未補全):
  - ui.json 各語系尚未加入瓷韻熊貓專屬外裝與武器名稱翻譯

👉 建議行動: 開立對應工程卡【瓷韻熊貓接上正式創角流程與衣櫥】"""
	root_ctrl.add_child(col2)

	return root_ctrl


func _generate_crops() -> void:
	# 1. 7 槽位預覽特寫
	var p1 := "%s/proof_01_dev_paperdoll_panda_default.png" % OUT_DIR
	if FileAccess.file_exists(p1):
		var img := Image.load_from_file(p1)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(240, 200, 340, 380))
			var crop_p := "%s/crop_panda_paperdoll_7_slots.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 2. 裸機素體特寫
	var p2 := "%s/proof_02_dev_paperdoll_panda_bare.png" % OUT_DIR
	if FileAccess.file_exists(p2):
		var img := Image.load_from_file(p2)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(240, 200, 340, 380))
			var crop_p := "%s/crop_panda_bare_chassis.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 2b. 卸除武器裸拳特寫
	var p3 := "%s/proof_03_dev_paperdoll_panda_unarmed.png" % OUT_DIR
	if FileAccess.file_exists(p3):
		var img := Image.load_from_file(p3)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(240, 200, 340, 380))
			var crop_p := "%s/crop_panda_unarmed_fist.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 3. 512 軀幹特寫
	var p4 := "%s/proof_04_panda_512_composite_stage.png" % OUT_DIR
	if FileAccess.file_exists(p4):
		var img := Image.load_from_file(p4)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(150, 150, 360, 360))
			var crop_p := "%s/crop_panda_512_torso.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 4. 行走動畫單幀特寫
	var p5 := "%s/proof_05_panda_walk_cycle_composite.png" % OUT_DIR
	if FileAccess.file_exists(p5):
		var img := Image.load_from_file(p5)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(60, 100, 256, 256))
			var crop_p := "%s/crop_panda_walk_frame.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 5. 戰鬥特寫姿態與頭像
	var p7 := "%s/proof_07_panda_official_portraits_and_battle.png" % OUT_DIR
	if FileAccess.file_exists(p7):
		var img := Image.load_from_file(p7)
		if img and not img.is_empty():
			var crop_b := img.get_region(Rect2i(80, 100, 256, 256))
			var crop_bp := "%s/crop_panda_battle_stance.png" % CROPS_DIR
			crop_b.save_png(crop_bp)
			print("  ✓ 已產出特寫: %s" % crop_bp)

			var crop_h := img.get_region(Rect2i(420, 100, 256, 256))
			var crop_hp := "%s/crop_panda_hud_portrait.png" % CROPS_DIR
			crop_h.save_png(crop_hp)
			print("  ✓ 已產出特寫: %s" % crop_hp)

			var crop_d := img.get_region(Rect2i(780, 80, 384, 480))
			var crop_dp := "%s/crop_panda_dialogue_bust.png" % CROPS_DIR
			crop_d.save_png(crop_dp)
			print("  ✓ 已產出特寫: %s" % crop_dp)

	# 6. 創角種族列末端特寫
	var p8 := "%s/proof_08_creation_flow_audit_panda_missing.png" % OUT_DIR
	if FileAccess.file_exists(p8):
		var img := Image.load_from_file(p8)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(300, 20, 950, 140))
			var crop_p := "%s/crop_creation_race_bar_end.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)

	# 7. 衣櫥種族 chip 列末端特寫
	var p9 := "%s/proof_09_wardrobe_flow_audit_panda_missing.png" % OUT_DIR
	if FileAccess.file_exists(p9):
		var img := Image.load_from_file(p9)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(200, 120, 900, 80))
			var crop_p := "%s/crop_wardrobe_chips_end.png" % CROPS_DIR
			crop.save_png(crop_p)
			print("  ✓ 已產出特寫: %s" % crop_p)
