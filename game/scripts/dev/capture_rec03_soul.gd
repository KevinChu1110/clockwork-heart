extends SceneTree
## REC-03 聚魂殿四階封靈罐開光與首屏透明保底
## 時長: 5.0s (由握手信號觸發錄製)
## 展示: 去 Emoji 現代 UI、四階金屬封靈罐(綠藍紫橙)、首屏 60/100 虔誠度透明保底進度條、抽魂開光

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

var _elapsed: float = 0.0
var _step_timer: float = 0.0
var _main: Node = null
var _step: int = 0
var _ready_written: bool = false
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _saved_png: bool = false
var _out_dir: String = ""
var _ready_file: String = ""
var _start_file: String = ""
var _ritual_triggered: bool = false

const ID: String = "rec03_soul_pity"
const TOTAL_DURATION: float = 5.0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws == "":
		ws = "/tmp"
	_ready_file = ws.path_join(ID + ".ready")
	_start_file = ws.path_join(ID + ".start")
	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			if current_scene != null and current_scene.has_method("_go_soul_panel"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var ss: Node = root.get_node_or_null("SoulSystem")
				if gs and ss:
					gs.call("reset_new_game")
					gs.set("gold", 1500)
					gs.set("stardust", 12)
					gs.set("weapon_tier", 2)
					gs.set("soul_vessel", "橙葫蘆")
					gs.call("set_flag", "soul.piety", 60)
					gs.call("set_flag", "soul.shards", 4)
					ss.call("ensure_slots")
					ss.call("grant_starter_soul")
					_main.call("_go_soul_panel")
					_setup_vessels_and_pity()
					_step = 1
					_step_timer = 0.0
					print("REC03_SOUL_PANEL_OPENED at ", _elapsed)
		1:
			_step_timer += delta
			# 讓聚魂殿畫面繪製並完全穩定
			if _step_timer >= 1.0 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("REC03_READY_FOR_RECORDING written at elapsed=", _elapsed)

			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 2
				_rec_elapsed = 0.0
				print("REC03_RECORDING_STARTED at elapsed=", _elapsed)
		2:
			_rec_elapsed += delta
			# 0.0s ~ 1.2s: 保持四階封靈罐與保底進度條展示
			# +1.2s: 觸發抽魂開光動態（橙階封靈罐迸發金光烈焰並開光出金桂冠神魂）
			if _rec_elapsed >= 1.2 and not _ritual_triggered:
				_ritual_triggered = true
				_trigger_ritual_lightup()
				print("REC03_RITUAL_TRIGGERED at rec_elapsed=", _rec_elapsed)
				_step = 3
		3:
			_rec_elapsed += delta
			# +3.5s: 保存關鍵幀截圖（開光金色神魂光效）
			if _rec_elapsed >= 3.5 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec03_soul_pity.png")
			# +5.0s: 錄影結束
			if _rec_elapsed >= TOTAL_DURATION:
				print("REC03_DONE at rec_elapsed=", _rec_elapsed)
				quit(0)
				return true
	return false

func _setup_vessels_and_pity() -> void:
	var host: Node = _main.get("host") if _main else null
	if not host:
		return
	
	# 1. 設置保底文字與進度條：虔誠度 60/100 · 再抽 4 次獲得碎片
	var lbl: Label = _find_label(host, "虔誠")
	if lbl:
		lbl.text = "虔誠度 60/100 · 再抽 4 次獲得碎片"
		lbl.add_theme_color_override("font_color", Color(0.95, 0.45, 0.1))
	var pbar: ProgressBar = _find_progress_bar(host)
	if pbar:
		pbar.min_value = 0
		pbar.max_value = 100
		pbar.value = 60
	var shards_l: Label = _find_label(host, "戰魂碎片")
	if shards_l:
		shards_l.text = "持有碎片：4 ｜ 兌換稀世需 6 ｜ 兌換神魂需 15"
	
	# 2. 設置四階封靈罐並列（綠→藍→紫→橙）
	var hbox: HBoxContainer = _find_gourd_hbox(host)
	if hbox:
		for c in hbox.get_children():
			c.queue_free()
		hbox.add_theme_constant_override("separation", 14)
		var vessels: Array[String] = ["綠葫蘆", "藍葫蘆", "紫葫蘆", "橙葫蘆"]
		var names: Array[String] = ["綠階封靈罐", "藍階封靈罐", "紫階封靈罐", "橙階封靈罐"]
		for i in vessels.size():
			var v: String = vessels[i]
			var vbox := VBoxContainer.new()
			vbox.alignment = BoxContainer.ALIGNMENT_CENTER
			vbox.add_theme_constant_override("separation", 2)
			
			var tr := TextureRect.new()
			tr.texture = SpriteDB.soul_vessel(v)
			tr.custom_minimum_size = Vector2(48, 60)
			tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			vbox.add_child(tr)
			
			var vl := Label.new()
			vl.text = names[i]
			vl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			vl.add_theme_font_size_override("font_size", 11)
			if v == "橙葫蘆":
				vl.add_theme_color_override("font_color", Color(1.0, 0.75, 0.2))
				tr.modulate = Color(1.2, 1.1, 0.9)
			else:
				vl.add_theme_color_override("font_color", Color(0.45, 0.40, 0.35))
				tr.modulate = Color(0.85, 0.85, 0.85)
			vbox.add_child(vl)
			
			hbox.add_child(vbox)
			
			if i < vessels.size() - 1:
				var arr := Label.new()
				arr.text = "→"
				arr.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
				arr.add_theme_font_size_override("font_size", 13)
				arr.add_theme_color_override("font_color", Color(0.8, 0.7, 0.4))
				hbox.add_child(arr)

func _trigger_ritual_lightup() -> void:
	if not _main:
		return
	var res_tex: Texture2D = SpriteDB.soul_shen()
	if _main.has_method("_soul_play_lightup"):
		_main.call("_soul_play_lightup", "橙葫蘆", res_tex, Callable())

func _find_label(n: Node, kw: String) -> Label:
	if n is Label and n.text.contains(kw):
		return n as Label
	for c in n.get_children():
		var f := _find_label(c, kw)
		if f:
			return f
	return null

func _find_progress_bar(n: Node) -> ProgressBar:
	if n is ProgressBar:
		return n as ProgressBar
	for c in n.get_children():
		var f := _find_progress_bar(c)
		if f:
			return f
	return null

func _find_gourd_hbox(n: Node) -> HBoxContainer:
	if n is HBoxContainer:
		for c in n.get_children():
			if c is TextureRect and c.texture != null and c.texture.resource_path.contains("gourd"):
				return n as HBoxContainer
	for c in n.get_children():
		var f := _find_gourd_hbox(c)
		if f:
			return f
	return null

func _save_screenshot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img:
		var p1 := _out_dir.path_join(filename)
		img.save_png(p1)
		print("SAVED_SCREENSHOT: ", p1)
		var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
		if ws != "":
			DirAccess.make_dir_recursive_absolute(ws)
			img.save_png(ws.path_join(filename))
			print("SAVED_WORKSPACE: ", ws.path_join(filename))
