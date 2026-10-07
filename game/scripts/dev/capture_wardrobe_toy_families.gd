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
var _saved_imgs: Array = []
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
		_saved_imgs.append(img.duplicate())
		_idx += 1
	if _idx >= _shots.size():
		_save_composite()
		print("WARDROBE_TOY_FAMILIES_CAPTURE_OK ", _out_dir)
		quit(0)
	return false


func _save_composite() -> void:
	if _saved_imgs.size() < 4:
		return
	var w: int = 1280
	var h: int = 720
	var comp := Image.create(w, h, false, Image.FORMAT_RGBA8)
	var half_w := w / 2
	var half_h := h / 2
	var positions := [
		Vector2i(0, 0),
		Vector2i(half_w, 0),
		Vector2i(0, half_h),
		Vector2i(half_w, half_h)
	]
	for i in range(4):
		var sm: Image = _saved_imgs[i].duplicate()
		sm.resize(half_w, half_h, Image.INTERPOLATE_LANCZOS)
		comp.blend_rect(sm, Rect2i(0, 0, half_w, half_h), positions[i])
	comp.save_png(_out_dir.path_join("proof_wardrobe_toy_families.png"))
	var root_path := ProjectSettings.globalize_path("res://").path_join("../proof_wardrobe_toy_families.png")
	comp.save_png(root_path)

