extends SceneTree
## 側案測試 (sideqa) - 探索性 QA：幻彩變色龍與星盤靈羊創角與衣櫥實機截圖產生器
## 執行方式：
## Xvfb :99 -screen 0 1280x720x24 &
## DISPLAY=:99 godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_ram_chameleon_qa.gd

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0

var _demo: Node = null
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始執行幻彩變色龍與星盤靈羊 創角與衣櫥實機截圖驗證 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proofs_dir = base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	# 步驟 1: 進入創角展示
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)

	_step = 1
	_wait_frames = 0

func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 創角舞台: 選取星盤靈羊 (ram)
			if _wait_frames == 10:
				print("\n>>> [創角 1/2] 選取星盤靈羊 (ram)...")
				_demo.call("select_race", "ram")
				_demo.call("reset_to_default")
			elif _wait_frames >= 30:
				_save_screenshot("creation_ram_stage.png")
				print("  ✓ 成功截取 [創角舞台] 星盤靈羊 (ram)")
				_step = 2
				_wait_frames = 0

		2:
			# 創角舞台: 選取幻彩變色龍 (chameleon)
			if _wait_frames == 10:
				print("\n>>> [創角 2/2] 選取幻彩變色龍 (chameleon)...")
				_demo.call("select_race", "chameleon")
				_demo.call("reset_to_default")
			elif _wait_frames >= 30:
				_save_screenshot("creation_chameleon_stage.png")
				print("  ✓ 成功截取 [創角舞台] 幻彩變色龍 (chameleon)")
				# 清理創角舞台
				_demo.queue_free()
				_demo = null
				_step = 3
				_wait_frames = 0

		3:
			# 準備大廳與更衣室
			if _wait_frames == 10:
				print("\n>>> [衣櫥 1/2] 初始化大廳並切換至星盤靈羊 (ram)...")
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "ram"
					gs.player_name = "星盤遊俠"
					gs.paperdoll_slots = {"race": "ram"}
				_lobby = MobileLobby.new()
				root.add_child(_lobby)
				_lobby._ready()
				_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
			elif _wait_frames == 25:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
			elif _wait_frames >= 50:
				_save_screenshot("wardrobe_ram_dialog.png")
				print("  ✓ 成功截取 [衣櫥彈窗] 星盤靈羊 (ram)")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				_step = 4
				_wait_frames = 0

		4:
			# 衣櫥: 切換至幻彩變色龍 (chameleon)
			if _wait_frames == 10:
				print("\n>>> [衣櫥 2/2] 大廳切換至幻彩變色龍 (chameleon)...")
				var gs = root.get_node_or_null("GameState")
				if gs:
					gs.player_race = "chameleon"
					gs.player_name = "幻彩獵手"
					gs.paperdoll_slots = {"race": "chameleon"}
				if _lobby != null:
					_lobby.refresh_character()
			elif _wait_frames == 25:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
			elif _wait_frames >= 50:
				_save_screenshot("wardrobe_chameleon_dialog.png")
				print("  ✓ 成功截取 [衣櫥彈窗] 幻彩變色龍 (chameleon)")
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				print("\n🎉 創角與衣櫥兩族實機截圖存證完成！")
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
	var proof_path := _proofs_dir.path_join(filename)
	img.save_png(file_path)
	img.save_png(proof_path)
	print("  [截圖成功] -> %s & %s" % [file_path, proof_path])
