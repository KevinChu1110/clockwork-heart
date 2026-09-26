extends SceneTree
## 新手引導觸控化與六語系實機截圖腳本 (onboard-touch-hints)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 觸控模式（force_touch_mode = true）下 en / ja / zh_TW 新手引導全景實機截圖。
## 2. 畫面上底列提示清楚呈現「點一下繼續」/「Tap to continue」/「タップで進む」，無空白鍵/Space/スペース。
## 3. 零系統 emoji、零破圖、零文字截斷。
## 4. OUT_DIR 獨立設定為 proofs/onboard-touch-hints/ (0-QA23)。

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _current_view: Control = null
var _loc_node: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_onboard_touch_en.png"},
	{"loc": "ja", "file": "proof_onboard_touch_ja.png"},
	{"loc": "zh_TW", "file": "proof_onboard_touch_zh_TW.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/onboard-touch-hints")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	print("── 開始執行新手引導觸控化實機截圖腳本 (onboard-touch-hints) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])

		if _wait == 1:
			if _loc_node:
				_loc_node.call("set_locale", code)

			var OnboardScene: PackedScene = load("res://scenes/onboard_w8/onboard_w8.tscn")
			if OnboardScene:
				_current_view = OnboardScene.instantiate() as Control
				# 強制設定為觸控模式
				_current_view.set("force_touch_mode", true)
				root.add_child(_current_view)

				# 切換至 N07（含下一步、稍後再說兩顆按鈕與結果卡）
				var flow = _current_view.get("flow")
				while flow != null and str(flow.current().get("node", "")) != "N07" and not flow.done:
					_current_view.call("_advance", false)
				print("  [流程] [%s] 已推進至 N07 節點: %s" % [code, str(flow.current().get("node", ""))])

		elif _wait >= 25:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 新手引導觸控模式 [%s] 實機截圖完成: %s" % [_step + 1, TASKS.size(), code, path])

			_cleanup_nodes()
			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		print("── 新手引導觸控化 3 張全景截圖全數完成 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_view and is_instance_valid(_current_view):
		_current_view.queue_free()
		_current_view = null


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img:
		if img.get_size() != Vector2i(1280, 720):
			img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
		img.save_png(abs_path)
