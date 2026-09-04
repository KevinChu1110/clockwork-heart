extends SceneTree

var _frame: int = 0
var _lobby: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = "/opt/side/bravesoul-game/screenshots"
	if not DirAccess.dir_exists_absolute(_out_dir):
		DirAccess.make_dir_recursive_absolute(_out_dir)

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1

	if _frame == 8:
		# 1. 截取繽紛慶典大廳全景 (彩旗 + 陽光粒子 + 奶油卡片)
		var img1 := root.get_texture().get_image()
		var p1 := _out_dir.path_join("proof_bravesoul_village.png")
		img1.save_png(p1)
		print("SAVED_VILLAGE: ", p1)

		# 2. 模擬點擊主角觸發互動 (揮劍姿態 + 彩色星芒粒子 + 對話氣泡)
		_lobby._on_hero_clicked()

	elif _frame == 14:
		# 3. 截取主角互動當下 (揮劍動作 + 氣泡 + 噴散彩色星芒粒子)
		var img_act := root.get_texture().get_image()
		var p_act := _out_dir.path_join("proof_bravesoul_hero_interact.png")
		img_act.save_png(p_act)
		print("SAVED_HERO_INTERACT: ", p_act)

		# 切換到冒險分頁
		_lobby._switch_tab(_lobby.Tab.ADVENTURE)

	elif _frame == 20:
		var img2 := root.get_texture().get_image()
		var p2 := _out_dir.path_join("proof_bravesoul_adventure.png")
		img2.save_png(p2)
		print("SAVED_ADVENTURE: ", p2)

		_lobby._switch_tab(_lobby.Tab.SOUL_HALL)

	elif _frame == 26:
		var img3 := root.get_texture().get_image()
		var p3 := _out_dir.path_join("proof_bravesoul_gourds.png")
		img3.save_png(p3)
		print("SAVED_GOURDS: ", p3)
		print("BRAVESOUL_CAPTURE_OK")
		quit(0)
		return true

	return false
