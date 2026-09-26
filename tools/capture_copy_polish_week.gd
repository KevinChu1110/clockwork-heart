extends SceneTree
## 本週文案微調批次實機截圖腳本 (tools/capture_copy_polish_week.gd)
## 依據規範：review.md 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 0-QA23: OUT_DIR 嚴格限定為 proofs/copy-polish-week/
## 2. 驗證 1：武術館選定流派確認對話（en、ja、zh_TW）字串不再含 .. 或 。。
## 3. 驗證 2：職業名「武鬥」在 en (Monk)、ja (武闘) 實機兵器架拳/爪職稱不再露繁中「武鬥」

var _out_dir: String = ""
var _crops_dir: String = ""
var _step: int = 0
var _wait: int = 0
var _main: Node = null
var _loc_node: Node = null
var _gs: Node = null

enum Phase {
	INIT,
	EN_RACK_SHOW,
	EN_RACK_SNAP,
	JA_RACK_SHOW,
	JA_RACK_SNAP,
	EN_DIALOG_SHOW,
	EN_DIALOG_SNAP,
	JA_DIALOG_SHOW,
	JA_DIALOG_SNAP,
	ZH_DIALOG_SHOW,
	ZH_DIALOG_SNAP,
	DONE
}

var _phase: Phase = Phase.INIT

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/copy-polish-week")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	print("=== 開始執行 copy-polish-week 實機截圖 ===")
	print("OUT_DIR: ", _out_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _advance_to_playstyle(diag: Control) -> void:
	if diag == null:
		return
	# 如果還在第 0 句，跳過打字並進到第 1 句
	while int(diag.get("_index")) < 1:
		diag.call("_skip_or_advance")
	# 立即完成第 1 句打字（玩法/playstyle）
	diag.call("_finish_typing")

func _process(_delta: float) -> bool:
	match _phase:
		Phase.INIT:
			if current_scene != null and current_scene.has_method("proof_show_paths"):
				_main = current_scene
				_loc_node = root.get_node_or_null("Loc")
				_gs = root.get_node_or_null("GameState")
				if _loc_node == null:
					return false
				_phase = Phase.EN_RACK_SHOW
				_wait = 0

		Phase.EN_RACK_SHOW:
			print("  [1/5] 設定 en 語系，展示兵器架...")
			_loc_node.call("set_locale", "en")
			_main.call("proof_show_paths")
			_phase = Phase.EN_RACK_SNAP
			_wait = 0

		Phase.EN_RACK_SNAP:
			_wait += 1
			if _wait >= 30:
				var path := _out_dir.path_join("proof_01_en_rack.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_01_en_rack.png")
				_save_crop(path, crop_path, Rect2i(180, 100, 920, 520))
				print("  ✓ proof_01_en_rack 完成: ", path)
				_phase = Phase.JA_RACK_SHOW
				_wait = 0

		Phase.JA_RACK_SHOW:
			print("  [2/5] 設定 ja 語系，展示兵器架...")
			_loc_node.call("set_locale", "ja")
			_main.call("proof_show_paths")
			_phase = Phase.JA_RACK_SNAP
			_wait = 0

		Phase.JA_RACK_SNAP:
			_wait += 1
			if _wait >= 30:
				var path := _out_dir.path_join("proof_02_ja_rack.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_02_ja_rack.png")
				_save_crop(path, crop_path, Rect2i(180, 100, 920, 520))
				print("  ✓ proof_02_ja_rack 完成: ", path)
				_phase = Phase.EN_DIALOG_SHOW
				_wait = 0

		Phase.EN_DIALOG_SHOW:
			print("  [3/5] 設定 en 語系，觸發選定流派對話 (sword)...")
			_loc_node.call("set_locale", "en")
			_main.call("proof_show_paths")
			_main.call("_set_path_and_back", "sword", false)
			_phase = Phase.EN_DIALOG_SNAP
			_wait = 0

		Phase.EN_DIALOG_SNAP:
			_wait += 1
			var diag: Control = _main.get("_dialogue")
			if diag and _wait == 10:
				_advance_to_playstyle(diag)
			elif _wait >= 25:
				var path := _out_dir.path_join("proof_03_en_sword_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_03_en_sword_dialog.png")
				_save_crop(path, crop_path, Rect2i(32, 440, 1216, 260))
				print("  ✓ proof_03_en_sword_dialog 完成: ", path)
				if diag:
					diag.call("_skip_or_advance")
					diag.call("_skip_or_advance")
				_phase = Phase.JA_DIALOG_SHOW
				_wait = 0

		Phase.JA_DIALOG_SHOW:
			print("  [4/5] 設定 ja 語系，觸發選定流派對話 (bow)...")
			_loc_node.call("set_locale", "ja")
			_main.call("proof_show_paths")
			_main.call("_set_path_and_back", "bow", false)
			_phase = Phase.JA_DIALOG_SNAP
			_wait = 0

		Phase.JA_DIALOG_SNAP:
			_wait += 1
			var diag: Control = _main.get("_dialogue")
			if diag and _wait == 10:
				_advance_to_playstyle(diag)
			elif _wait >= 25:
				var path := _out_dir.path_join("proof_04_ja_bow_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_04_ja_bow_dialog.png")
				_save_crop(path, crop_path, Rect2i(32, 440, 1216, 260))
				print("  ✓ proof_04_ja_bow_dialog 完成: ", path)
				if diag:
					diag.call("_skip_or_advance")
					diag.call("_skip_or_advance")
				_phase = Phase.ZH_DIALOG_SHOW
				_wait = 0

		Phase.ZH_DIALOG_SHOW:
			print("  [5/5] 設定 zh_TW 語系，觸發選定流派對話 (sword)...")
			_loc_node.call("set_locale", "zh_TW")
			_main.call("proof_show_paths")
			_main.call("_set_path_and_back", "sword", false)
			_phase = Phase.ZH_DIALOG_SNAP
			_wait = 0

		Phase.ZH_DIALOG_SNAP:
			_wait += 1
			var diag: Control = _main.get("_dialogue")
			if diag and _wait == 10:
				_advance_to_playstyle(diag)
			elif _wait >= 25:
				var path := _out_dir.path_join("proof_05_zh_TW_sword_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_05_zh_TW_sword_dialog.png")
				_save_crop(path, crop_path, Rect2i(32, 440, 1216, 260))
				print("  ✓ proof_05_zh_TW_sword_dialog 完成: ", path)
				if diag:
					diag.call("_skip_or_advance")
					diag.call("_skip_or_advance")
				_phase = Phase.DONE
				_wait = 0

		Phase.DONE:
			print("=== 全部 copy-polish-week 實機截圖完成 ===")
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
