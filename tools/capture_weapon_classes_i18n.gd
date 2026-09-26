extends SceneTree
## 武術館兵器架十二流派名稱與說明六語系實機全景截圖腳本 (tools/capture_weapon_classes_i18n.gd)
## 遵循規範：review.md 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja 各一張全景實機截圖（1280x720），呈現 0-QA25 彈窗 chrome、背景與兵器架按鈕同語系連動。
## 2. 兵器架十二流派按鈕顯示該語言的「短名·稱號」，不再出現繁中或單字母 S。
## 3. OUT_DIR 嚴格限定為 proofs/weapon-classes-i18n/ (0-QA23)。

var _out_dir: String = ""
var _crops_dir: String = ""
var _step: int = 0
var _wait: int = 0
var _main: Node = null
var _loc_node: Node = null
var _gs: Node = null

const SHOTS := [
	{"loc": "en", "file": "proof_01_weapon_classes_en.png", "crop": "crops/crop_01_weapon_classes_en.png"},
	{"loc": "ja", "file": "proof_02_weapon_classes_ja.png", "crop": "crops/crop_02_weapon_classes_ja.png"}
]
var _shot_idx: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/weapon-classes-i18n")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	print("=== 開始執行武術館兵器架十二流派實機截圖 (weapon-classes-i18n) ===")
	print("OUT_DIR: ", _out_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	match _step:
		0:
			if current_scene != null and current_scene.has_method("proof_show_paths"):
				_main = current_scene
				_loc_node = root.get_node_or_null("Loc")
				_gs = root.get_node_or_null("GameState")
				if _loc_node == null:
					return false

				var cfg: Dictionary = SHOTS[_shot_idx]
				var code: String = str(cfg["loc"])
				print("  -> 設定語系為: ", code)
				_loc_node.call("set_locale", code)

				# 開啟兵器架面板
				_main.call("proof_show_paths")
				_step = 1
				_wait = 0
		1:
			_wait += 1
			if _wait >= 40:
				var cfg: Dictionary = SHOTS[_shot_idx]
				var fname: String = str(cfg["file"])
				var cname: String = str(cfg["crop"])
				var path := _out_dir.path_join(fname)
				
				_save_screenshot(path)
				print("  ✓ 全景截圖完成 [%s]: %s" % [cfg["loc"], path])

				# 局部裁切兵器架十二顆按鈕與標題區域
				var crop_path := _out_dir.path_join(cname)
				_save_crop(path, crop_path, Rect2i(180, 100, 920, 520))
				print("  ✓ 局部特寫裁切完成 [%s]: %s" % [cfg["loc"], crop_path])

				_shot_idx += 1
				if _shot_idx < SHOTS.size():
					_step = 0
					_wait = 0
				else:
					print("=== 全部實機截圖完成 ===")
					if _loc_node:
						_loc_node.call("set_locale", "zh_TW")
					quit(0)
					return true
	return false

func _save_screenshot(target_path: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img != null:
		img.save_png(target_path)

func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null:
		return
	var cropped := img.get_region(rect)
	cropped.save_png(crop_path)
