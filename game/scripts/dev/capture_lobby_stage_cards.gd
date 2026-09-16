extends SceneTree
## 冒險分頁四地區關卡卡片與標籤完整性實機截圖存證（t_c4269b45 複驗）
## 執行：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_stage_cards.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _main: Node = null

func _initialize() -> void:
	print("=== 開始產生冒險分頁四地區關卡卡片實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_stage_cards")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	change_scene_to_file("res://scenes/main.tscn")
	_run_flow()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _run_flow() -> void:
	await _wait_frames(10)
	while current_scene == null or not current_scene.has_method("_go_mobile_lobby"):
		await _wait_frames(2)

	_main = current_scene
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_name", "小白")
		gs.set("player_race", "rabbit")
		gs.set("level", 20)
		gs.set("hp", 400)
		gs.set("max_hp", 400)
		gs.set("energy", 15)
		gs.set("energy_ts", Time.get_unix_time_from_system())

	var tut: Node = root.get_node_or_null("TutorialSystem")
	if tut:
		tut.call("mark", "battle_auto")
		tut.call("mark", "battle_parry")
		tut.call("mark", "battle_fog")
		tut.call("mark", "explore")

	print("進入大廳...")
	_main.call("_go_mobile_lobby")
	await _wait_frames(8)

	var lobby: MobileLobby = _find_lobby(_main)
	if lobby == null:
		push_error("無法找到 MobileLobby 節點")
		quit(1)
		return

	print("切換至四區出征分頁 (Tab.ADVENTURE)...")
	lobby._switch_tab(MobileLobby.Tab.ADVENTURE)
	await _wait_frames(8)

	var regions: Array[Dictionary] = [
		{"idx": 0, "name": "第一地區 · 閣樓與堡壘", "file": "proof_stage_cards_region_1_attic.png"},
		{"idx": 1, "name": "第二地區 · 白霧之地", "file": "proof_stage_cards_region_2_mist.png"},
		{"idx": 2, "name": "第三地區 · 道場與西林", "file": "proof_stage_cards_region_3_dojo.png"},
		{"idx": 3, "name": "第四地區 · 潮岸與終境", "file": "proof_stage_cards_region_4_tide.png"}
	]

	for r in regions:
		print("\n>>> 選擇 %s (索引 %d)..." % [r["name"], r["idx"]])
		lobby._select_region(int(r["idx"]))
		await _wait_frames(10)
		await RenderingServer.frame_post_draw
		_capture_screenshot(str(r["file"]))

	print("\n=== 四個地區分頁截圖皆已成功產出！===")
	quit(0)

func _capture_screenshot(out_filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img != null and not img.is_empty():
		var p := _out_dir.path_join(out_filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ 截圖已儲存至: %s" % p)
		else:
			push_error("截圖存檔失敗: %d" % err)
			quit(1)
	else:
		push_error("截圖為空")
		quit(1)

func _find_lobby(node: Node) -> MobileLobby:
	if node is MobileLobby:
		return node as MobileLobby
	for child in node.get_children():
		var res := _find_lobby(child)
		if res != null:
			return res
	return null
