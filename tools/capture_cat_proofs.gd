extends SceneTree
## 《發條之心》幽影貓 (cat) 7 大部件紙娃娃實機截圖存證腳本
## 對應任務：t_5ff42afe

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_5ff42afe"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行幽影貓實機截圖腳本 (t_5ff42afe) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角介面 (PaperdollSelectDemo) 擴充分頁選幽影貓 (cat)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "cat")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "expansion")
					demo.call("select_race", "cat")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 35:
				var path := "%s/proof_01_creation_cat_selected.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/3] 創角介面選取幽影貓截圖完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 創角介面卸除外裝 (裸機素體模式)
			if _wait == 1:
				if _current_node and _current_node.has_method("_on_costume_next_pressed"):
					_current_node.call("_on_costume_next_pressed")
			elif _wait >= 30:
				var path := "%s/proof_02_creation_cat_bare_chassis.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/3] 創角介面卸除外裝 (裸機素體) 截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 大廳開啟衣櫥 (WardrobeDialog)，篩選「貓」
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "cat")
					_gs.set("player_name", "幽影貓")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 10:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
			elif _wait == 25:
				var dlg: Node = _current_node.get_node_or_null("WardrobeDialog") if _current_node else null
				if dlg and dlg.has_method("set_race_filter"):
					dlg.call("set_race_filter", "cat")
			elif _wait == 35:
				var dlg: Node = _current_node.get_node_or_null("WardrobeDialog") if _current_node else null
				if dlg:
					var f_scroll: ScrollContainer = dlg.find_child("FilterScroll", true, false) as ScrollContainer
					if f_scroll:
						var hbar := f_scroll.get_h_scroll_bar()
						f_scroll.scroll_horizontal = int(hbar.max_value) if hbar else 908
			elif _wait >= 55:
				var path := "%s/proof_03_wardrobe_cat.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/3] 衣櫥介面篩選幽影貓截圖完成: %s" % path)
				_finish_all()
				return true

	return false


func _save_screenshot(path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null and not img.is_empty():
		img.save_png(path)
	else:
		push_error("無法取得視窗截圖！")


func _finish_all() -> void:
	print("── 幽影貓實機截圖存證完成 ──")
	quit(0)
