extends SceneTree
## 驗證：兔／狐穿同一件維京束帶外裝，身體仍是各族本體、衣服共用同一切片
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_paperdoll_costume_reuse_proof.gd

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _dlg: WardrobeDialog = null
var _gs = null


func _initialize() -> void:
	print("=== 開始產生兔/狐共用維京外裝驗證截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/costume_reuse")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	_set_race_costume("rabbit", "costume_viking_harness")

	_dlg = WardrobeDialog.new()
	root.add_child(_dlg)
	_step = 1
	_wait_frames = 0


func _set_race_costume(race: String, costume_id: String) -> void:
	if _gs:
		_gs.player_race = race
		_gs.player_name = "小白"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": race,
			"costume": costume_id,
			"costume_id": costume_id,
		}


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames >= 30:
				_save_screenshot("proof_rabbit_viking_harness.png")
				print("  ✓ 步驟1：兔穿維京束帶截圖完成")
				_step = 2
				_wait_frames = 0
				root.remove_child(_dlg)
				_dlg.queue_free()
				_set_race_costume("fox", "costume_viking_harness")
				_dlg = WardrobeDialog.new()
				root.add_child(_dlg)
		2:
			if _wait_frames >= 30:
				_save_screenshot("proof_fox_viking_harness.png")
				print("  ✓ 步驟2：狐穿維京束帶截圖完成")
				_step = 3
				_wait_frames = 0
		3:
			print("=== 完成 ===")
			quit(0)
			return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var full_path := _out_dir.path_join(filename)
				var err := img.save_png(full_path)
				if err == OK:
					print("  [截圖存檔] %s" % full_path)
				else:
					push_error("截圖儲存失敗: %d" % err)
