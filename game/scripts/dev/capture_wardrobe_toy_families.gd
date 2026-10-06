extends SceneTree
## 衣櫥玩具家族分頁實機截圖 + 背後發條 8 格橫條
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_toy_families.gd

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const ToyFamily = preload("res://scripts/art/toy_family.gd")
const WindingKeyAnim = preload("res://scripts/art/winding_key_anim.gd")

var _out_dir := ""
var _dlg: Control = null
var _frame := 0
var _shots: Array = ["nutcracker_rabbit", "tin_soldier", "music_box", "carousel"]
var _idx := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/wardrobe_toy_families")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.paperdoll_slots = {"race": "rabbit", "costume_id": "costume_nutcracker_guard", "paint_id": "paint_ivory_stock"}
	_save_key_strip()
	_dlg = WardrobeDialog.new()
	root.add_child(_dlg)


func _save_key_strip() -> void:
	var frames := WindingKeyAnim.build_idle_key_frames_512("rabbit", {"costume": "costume_nutcracker_guard", "chassis": "paint_ivory_stock"})
	if frames.size() != WindingKeyAnim.STEPS_PER_TURN:
		return
	var crop := Rect2i(112, 208, 160, 160)
	var strip := Image.create(crop.size.x * frames.size(), crop.size.y, false, Image.FORMAT_RGBA8)
	strip.fill(Color(0.93, 0.89, 0.80, 1))
	for i in range(frames.size()):
		strip.blend_rect(frames[i].get_image(), crop, Vector2i(i * crop.size.x, 0))
	strip.save_png(_out_dir.path_join("proof_winding_key_8steps.png"))


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame % 20 == 5 and _idx < _shots.size():
		_dlg.call("set_family", _shots[_idx])
	if _frame % 20 == 15 and _idx < _shots.size():
		var img := root.get_texture().get_image()
		img.save_png(_out_dir.path_join("proof_wardrobe_%d_%s.png" % [_idx + 1, _shots[_idx]]))
		_idx += 1
	if _idx >= _shots.size():
		print("WARDROBE_TOY_FAMILIES_CAPTURE_OK ", _out_dir)
		quit(0)
	return false
