extends SceneTree
## QA Round 32 探索性驗證實機截圖腳本
## 涵蓋：
## 1. 創角首發頁（五卡一屏）
## 2. 創角擴充頁（含瓷韻熊貓）
## 3. 點熊貓後中央預覽（512 舞台、外裝與塗裝）
## 4. 創角擴充頁向右滾動至翠角鹿卡片檢查
## 5. 創角點選翠角鹿後預覽檢查（檢查空卡／色塊／128 糊圖）
## 6. 熊貓戰鬥待機 (idle 512)
## 7. 熊貓戰鬥攻擊 (attack 512)
## 8. 熊貓戰鬥受擊 (hit 512)
## 9. 衣櫥抽查熊貓（篩選「貓」，選用禪道學徒長袍＋白瓷塗裝）
## 10. 衣櫥抽查翠角鹿（篩選「鹿」，檢查空卡／占位色塊）
## 11. 衣櫥篩選「全部」並滾動至翠角鹿部件

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round32"
const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _step := 0
var _wait := 0
var _current_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	_gs = root.get_node_or_null("GameState")

	print("=== 開始執行 QA Round 32 探索性實機截圖流程 ===")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角首發頁（五卡一屏）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "launch")
					demo.call("select_race", "rabbit")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 30:
				var path := "%s/proof_01_creation_launch.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/11] 創角首發頁（五卡一屏）: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 創角擴充頁（含瓷韻熊貓）
			if _wait == 1:
				if _current_node:
					_current_node.call("switch_tab", "expansion")
			elif _wait >= 30:
				var path := "%s/proof_02_creation_expansion.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/11] 創角擴充頁（含瓷韻熊貓）: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 點熊貓後中央預覽（512 舞台）
			if _wait == 1:
				if _current_node:
					_current_node.call("select_race", "panda")
					_current_node.call("reset_to_default")
			elif _wait >= 30:
				var path := "%s/proof_03_creation_panda_selected.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/11] 點熊貓後中央預覽: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 創角擴充頁向右滾動至翠角鹿卡片檢查
			if _wait == 1:
				if _current_node:
					var scroll := _current_node.get_node_or_null("TopRaceBar") as ScrollContainer
					if scroll:
						var hbar := scroll.get_h_scroll_bar()
						scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999
			elif _wait >= 30:
				var path := "%s/proof_04_creation_fawn_check.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/11] 創角擴充頁右滾動翠角鹿卡片: %s" % path)
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 點選翠角鹿檢查中央預覽與舞台狀態
			if _wait == 1:
				if _current_node:
					_current_node.call("select_race", "fawn")
			elif _wait >= 30:
				var path := "%s/proof_05_creation_fawn_selected.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/11] 創角選取翠角鹿中央預覽檢查: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 熊貓戰鬥待機
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "panda")
					_gs.set("player_race", "panda")
					_gs.set("player_name", "瓷韻熊貓")
					_gs.set("gold", 3000)
					_gs.set("weapon_tier", 3)
					_gs.set("weapon_atk", 50)
					_gs.call("set_flag", "c1_forged", true)
					_gs.call("set_flag", "tut_done", true)
				var battle_packed: PackedScene = load("res://scenes/battle/battle.tscn")
				if battle_packed:
					var b = battle_packed.instantiate()
					root.add_child(b)
					if b.has_method("setup"):
						b.call("setup", "wolf")
					b.set_process(false) # 停止戰鬥自動模擬，保持姿態不被計時器覆蓋
					_current_node = b
			elif _wait == 5:
				var p_body: TextureRect = _current_node.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
				if p_body:
					var idle_tex: Texture2D = SpriteDB.player_pose("idle", "panda")
					if idle_tex:
						p_body.texture = idle_tex
						p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			elif _wait >= 20:
				var path := "%s/proof_06_battle_panda_idle.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [6/11] 熊貓戰鬥待機: %s" % path)
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 熊貓戰鬥攻擊
			if _wait == 1:
				var p_body: TextureRect = _current_node.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
				if p_body:
					var atk_tex: Texture2D = SpriteDB.player_pose("attack", "panda")
					if atk_tex:
						p_body.texture = atk_tex
						p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				if _current_node.has_method("_layout_foot_shadow"):
					_current_node.call("_layout_foot_shadow", p_body)
			elif _wait >= 20:
				var path := "%s/proof_07_battle_panda_attack.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [7/11] 熊貓戰鬥攻擊: %s" % path)
				_step = 8
				_wait = 0

		8:
			# 步驟 8: 熊貓戰鬥受擊
			if _wait == 1:
				var p_body: TextureRect = _current_node.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
				if p_body:
					var hit_tex: Texture2D = SpriteDB.player_pose("hit", "panda")
					if hit_tex:
						p_body.texture = hit_tex
						p_body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				if _current_node.has_method("_layout_foot_shadow"):
					_current_node.call("_layout_foot_shadow", p_body)
			elif _wait >= 20:
				var path := "%s/proof_08_battle_panda_hit.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [8/11] 熊貓戰鬥受擊: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		9:
			# 步驟 9: 衣櫥抽查熊貓（篩選「貓」，選用禪道學徒生漆長袍＋羊脂白瓷生漆塗裝）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "panda")
					_gs.set("player_race", "panda")
				var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
				if WardrobeClass:
					var dlg = WardrobeClass.new()
					root.add_child(dlg)
					_current_node = dlg
			elif _wait == 10:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "panda")
			elif _wait == 18:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999

				var displayed_c: Array = _current_node.get("_displayed_costumes")
				var target_c_idx := 0
				for idx in range(displayed_c.size()):
					if displayed_c[idx].get("id") == "costume_panda_zen_apprentice_robe":
						target_c_idx = idx
						break
				var displayed_ch: Array = _current_node.get("_displayed_chassis")
				var target_ch_idx := 0
				for idx in range(displayed_ch.size()):
					if displayed_ch[idx].get("id") == "paint_panda_porcelain":
						target_ch_idx = idx
						break

				_current_node.set("costume_index", target_c_idx)
				_current_node.set("chassis_index", target_ch_idx)
				_current_node.set("selected_costume_id", "costume_panda_zen_apprentice_robe")
				_current_node.set("selected_chassis_id", "paint_panda_porcelain")
				if _current_node.has_method("_update_card_selection_states"):
					_current_node.call("_update_card_selection_states")
				if _current_node.has_method("_update_preview"):
					_current_node.call("_update_preview")
				if _current_node.has_method("_update_ui_texts"):
					_current_node.call("_update_ui_texts")
			elif _wait >= 40:
				var path := "%s/proof_09_wardrobe_panda.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [9/11] 衣櫥抽查熊貓: %s" % path)
				_step = 10
				_wait = 0

		10:
			# 步驟 10: 衣櫥抽查翠角鹿（篩選「鹿」）
			if _wait == 5:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "fawn")
			elif _wait == 15:
				var scroll: ScrollContainer = _current_node.find_child("FilterScroll", true, false) as ScrollContainer
				if scroll:
					var hbar := scroll.get_h_scroll_bar()
					scroll.scroll_horizontal = int(hbar.max_value) if hbar else 9999
			elif _wait >= 35:
				var path := "%s/proof_10_wardrobe_fawn_filter.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [10/11] 衣櫥抽查翠角鹿篩選: %s" % path)
				_step = 11
				_wait = 0

		11:
			# 步驟 11: 衣櫥篩選「全部」並滾動至最底部翠角鹿卡片
			if _wait == 5:
				if _current_node and _current_node.has_method("set_race_filter"):
					_current_node.call("set_race_filter", "all")
			elif _wait == 15:
				# 滾動卡片列表以觀察最下方的翠角鹿卡片
				var c_grid = _current_node.get("_costume_grid")
				if c_grid and c_grid.get_parent() and c_grid.get_parent().get_parent():
					var c_scroll = c_grid.get_parent().get_parent() as ScrollContainer
					if c_scroll:
						var vbar := c_scroll.get_v_scroll_bar()
						c_scroll.scroll_vertical = int(vbar.max_value) if vbar else 9999
				var ch_grid = _current_node.get("_chassis_grid")
				if ch_grid and ch_grid.get_parent() and ch_grid.get_parent().get_parent():
					var ch_scroll = ch_grid.get_parent().get_parent() as ScrollContainer
					if ch_scroll:
						var vbar := ch_scroll.get_v_scroll_bar()
						ch_scroll.scroll_vertical = int(vbar.max_value) if vbar else 9999
			elif _wait >= 35:
				var path := "%s/proof_11_wardrobe_all_fawn.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [11/11] 衣櫥篩選全部 (翠角鹿卡片): %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				print("=== QA Round 32 全部截圖產生完成 ===")
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
		print("    成功寫入截圖: %s" % abs_path)
