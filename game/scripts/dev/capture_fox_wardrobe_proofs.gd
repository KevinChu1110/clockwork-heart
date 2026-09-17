extends SceneTree
## 產生狐族衣櫥換裝實機截圖（裸機 vs 套頭套）
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_fox_wardrobe_proofs.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生狐族衣櫥換裝實機截圖 (裸機 vs 套頭套) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "fox"
		gs.player_name = "靈尾狐"
		gs.paperdoll_slots = {
			"race": "fox",
			"costume": "none",
			"chassis": "paint_fox_orange",
			"costume_id": "none",
			"paint_id": "paint_fox_orange",
			"weapon": "wpn_astral_staff"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)

	_step = 1
	_wait_frames = 0

func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames == 10:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
					if _wardrobe != null:
						# 篩選狐族
						if _wardrobe.has_method("_on_race_chip_selected"):
							_wardrobe.call("_on_race_chip_selected", "fox")
						# 選中第 2 張卡片：無外裝 (裸機素體)
						var cards: Array = _wardrobe.get("_costume_cards")
						if cards.size() > 2:
							cards[2].emit_signal("pressed")
						else:
							_wardrobe.set("costume_index", 2)
							_wardrobe.set("selected_costume_id", "none")
							_wardrobe.call("_update_card_selection_states")
							_wardrobe.call("_update_preview")
							_wardrobe.call("_update_ui_texts")
						print("  [Wardrobe] 已開啟衣櫥並選中【無外裝 (裸機素體)】與【靈狐曜橙烤漆】")
			if _wait_frames >= 40:
				var fn := "proof_wardrobe_fox_bare.png"
				_save_screenshot(fn)
				print("  ✓ [1/2] 狐族裸機素體衣櫥彈窗截圖完成 -> %s" % fn)

				# 切換至第 0 張卡片：【星紋見習占星斗篷】(套頭套/外裝)
				if _wardrobe != null and is_instance_valid(_wardrobe):
					var cards: Array = _wardrobe.get("_costume_cards")
					if cards.size() > 0:
						cards[0].emit_signal("pressed")
					else:
						_wardrobe.set("costume_index", 0)
						_wardrobe.set("selected_costume_id", "costume_astral_cape")
						_wardrobe.call("_update_card_selection_states")
						_wardrobe.call("_update_preview")
						_wardrobe.call("_update_ui_texts")
					print("  [Wardrobe] 已切換至第 0 張卡片【星紋見習占星斗篷】(套頭套)")
				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 40:
				var fn2 := "proof_wardrobe_fox_equipped.png"
				_save_screenshot(fn2)
				print("  ✓ [2/2] 狐族套頭套外裝衣櫥彈窗截圖完成 -> %s" % fn2)
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				quit(0)
				return true

	return false

func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
