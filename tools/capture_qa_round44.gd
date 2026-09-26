extends SceneTree
## 探索性 QA 第四十四輪 實機截圖腳本 (tools/capture_qa_round44.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 任務目標：
## 1. 兵器架 en / ja 各一（選定劍與弓各至少一張語系）。
## 2. 驗收十二顆流派按鈕「短名·稱號」與選定後玩法句、第一條優點跟著換。
## 3. en 不准出現單字母 S，零系統 emoji，零破圖截字。
## 4. OUT_DIR 嚴格限定為 proofs/qa_round44/ (0-QA23)。

var _out_dir: String = ""
var _crops_dir: String = ""
var _step: int = 0
var _wait: int = 0
var _main: Node = null
var _loc_node: Node = null
var _gs: Node = null
var _dialogue: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/qa_round44")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	print("=== 開始執行 QA 第四十四輪實機巡檢截圖腳本 (qa_round44) ===")
	print("OUT_DIR: ", _out_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if current_scene != null and current_scene.has_method("proof_show_paths"):
				_main = current_scene
				_loc_node = root.get_node_or_null("Loc")
				_gs = root.get_node_or_null("GameState")
				_dialogue = _main.get("_dialogue") if "_dialogue" in _main else null
				if _loc_node == null or _gs == null:
					return false
				print("  -> 主場景與 Autoload 節點就緒，開始截圖流程")
				_step = 10
				_wait = 0

		# ----------------------------------------------------
		# [EN 流程] 選定劍 (sword)，截對話框(玩法句+優點)與兵器架
		# ----------------------------------------------------
		10:
			if _wait == 1:
				print("  -> [en] 設定語系為 en，並選定劍 (sword)")
				_loc_node.call("set_locale", "en")
				_main.call("_set_path_and_back", "sword", false)
			elif _wait == 15:
				if _dialogue != null:
					# 第一句是流派確認，advance 到第二句玩法與優點
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
			elif _wait == 30:
				var path := _out_dir.path_join("proof_02_en_sword_chosen_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_02_en_sword_dialog.png")
				_save_crop(path, crop_path, Rect2i(30, 430, 1220, 270))
				print("  ✓ [en] 選定劍對話框截圖與裁切完成: ", path)
			elif _wait == 45:
				# 關閉對話框，觸發 callback 回到兵器架
				if _dialogue != null:
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
			elif _wait == 65:
				var path := _out_dir.path_join("proof_01_en_sword_rack.png")
				_save_screenshot(path)
				var crop_btns := _crops_dir.path_join("crop_01_en_sword_buttons.png")
				_save_crop(path, crop_btns, Rect2i(180, 80, 920, 560))
				var crop_hdr := _crops_dir.path_join("crop_05_en_header_status.png")
				_save_crop(path, crop_hdr, Rect2i(0, 0, 1280, 90))
				print("  ✓ [en] 兵器架全景與按鈕裁切完成: ", path)
				_step = 20
				_wait = 0

		# ----------------------------------------------------
		# [JA 流程] 選定弓 (bow)，截對話框(玩法句+優點)與兵器架
		# ----------------------------------------------------
		20:
			if _wait == 1:
				print("  -> [ja] 設定語系為 ja，並選定弓 (bow)")
				_loc_node.call("set_locale", "ja")
				_main.call("_set_path_and_back", "bow", false)
			elif _wait == 15:
				if _dialogue != null:
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
			elif _wait == 30:
				var path := _out_dir.path_join("proof_04_ja_bow_chosen_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_04_ja_bow_dialog.png")
				_save_crop(path, crop_path, Rect2i(30, 430, 1220, 270))
				print("  ✓ [ja] 選定弓對話框截圖與裁切完成: ", path)
			elif _wait == 45:
				if _dialogue != null:
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
			elif _wait == 65:
				var path := _out_dir.path_join("proof_03_ja_bow_rack.png")
				_save_screenshot(path)
				var crop_btns := _crops_dir.path_join("crop_03_ja_bow_buttons.png")
				_save_crop(path, crop_btns, Rect2i(180, 80, 920, 560))
				var crop_hdr := _crops_dir.path_join("crop_06_ja_header_status.png")
				_save_crop(path, crop_hdr, Rect2i(0, 0, 1280, 90))
				print("  ✓ [ja] 兵器架全景與按鈕裁切完成: ", path)
				_step = 30
				_wait = 0

		# ----------------------------------------------------
		# [ZH_TW 基準流程] 選定劍 (sword)，截對話框與兵器架
		# ----------------------------------------------------
		30:
			if _wait == 1:
				print("  -> [zh_TW] 設定語系為 zh_TW，並選定劍 (sword)")
				_loc_node.call("set_locale", "zh_TW")
				_main.call("_set_path_and_back", "sword", false)
			elif _wait == 15:
				if _dialogue != null:
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_finish_typing"):
						_dialogue.call("_finish_typing")
			elif _wait == 30:
				var path := _out_dir.path_join("proof_06_zh_TW_sword_chosen_dialog.png")
				_save_screenshot(path)
				var crop_path := _crops_dir.path_join("crop_08_zh_TW_dialog.png")
				_save_crop(path, crop_path, Rect2i(30, 430, 1220, 270))
				print("  ✓ [zh_TW] 選定劍對話框截圖與裁切完成: ", path)
			elif _wait == 45:
				if _dialogue != null:
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
					if _dialogue.has_method("_skip_or_advance"):
						_dialogue.call("_skip_or_advance")
			elif _wait == 65:
				var path := _out_dir.path_join("proof_05_zh_TW_sword_rack.png")
				_save_screenshot(path)
				var crop_btns := _crops_dir.path_join("crop_07_zh_TW_buttons.png")
				_save_crop(path, crop_btns, Rect2i(180, 80, 920, 560))
				print("  ✓ [zh_TW] 兵器架全景與按鈕裁切完成: ", path)
				_step = 40
				_wait = 0

		40:
			print("=== 全部 QA 第四十四輪實機截圖存證完成 ===")
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
