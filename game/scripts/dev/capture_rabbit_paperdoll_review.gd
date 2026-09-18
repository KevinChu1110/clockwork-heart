extends SceneTree
## 兔族紙娃娃全套實機截圖產生器 (t_0b9157b4)
## 依據任務規範逐一截取：
## 1. 大廳中央角色（村莊分頁，無外裝 / 皇家巡遊）
## 2. 角色分頁左側紙娃娃預覽（無外裝 / 皇家巡遊）
## 3. 衣櫥彈窗：4外裝 x 3塗裝 = 12 組合全截
## 4. 跨族：兔穿維京束帶、兔穿星紋斗篷
## 5. 衣櫥右側卡片縮圖特寫

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始產生兔族紙娃娃全套複檢實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/rabbit_paperdoll_review")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗（無 Viewport）: %s" % filename)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗（無 Texture）: %s" % filename)
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗（空畫面）: %s" % filename)
		return

	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ 成功截圖: %s" % filename)
	else:
		push_error("截圖儲存失敗: %s" % p)

func _select_costume_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_costume_cards")
	var displayed: Array = _wardrobe.get("_displayed_costumes")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("costume_index", i)
				_wardrobe.set("selected_costume_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false

func _select_chassis_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var cards: Array = _wardrobe.get("_chassis_cards")
	var displayed: Array = _wardrobe.get("_displayed_chassis")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			if i < cards.size():
				cards[i].emit_signal("pressed")
			else:
				_wardrobe.set("chassis_index", i)
				_wardrobe.set("selected_chassis_id", target_id)
				_wardrobe.call("_update_card_selection_states")
				_wardrobe.call("_update_preview")
				_wardrobe.call("_update_ui_texts")
			return true
	return false

func _run() -> void:
	await _wait_frames(5)
	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.reset_new_game()
		_gs.player_race = "rabbit"
		_gs.player_name = "白金兔"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	await _wait_frames(20)

	# --- 1. 大廳中央角色（村莊分頁） ---
	print(">>> [1/5] 大廳中央角色（村莊分頁）...")
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	_lobby._apply_hero_idle_visual()
	await _wait_frames(15)
	await _capture("01_lobby_village_rabbit_bare.png")

	# 換上皇家巡遊
	if _gs:
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_royal_parade",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_royal_parade",
			"paint_id": "paint_ivory_stock",
			"weapon": "wpn_dawn_blade"
		}
	_lobby._load_hero_poses()
	_lobby._apply_hero_idle_visual()
	await _wait_frames(15)
	await _capture("02_lobby_village_rabbit_royal.png")

	# --- 2. 角色分頁左側紙娃娃預覽 ---
	print(">>> [2/5] 角色分頁左側紙娃娃預覽...")
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(15)
	await _capture("03_lobby_char_tab_rabbit_royal.png")

	# 切回無外裝
	if _gs:
		_gs.paperdoll_slots = {}
	_lobby._load_hero_poses()
	_lobby._apply_hero_idle_visual()
	await _wait_frames(15)
	await _capture("04_lobby_char_tab_rabbit_bare.png")

	# --- 3. 打開衣櫥彈窗進行 12 組合截圖 ---
	print(">>> [3/5] 衣櫥彈窗 12 組合截圖...")
	_lobby.open_wardrobe()
	await _wait_frames(15)
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe == null:
		push_error("無法找到 WardrobeDialog 節點！")
		quit(1)
		return

	_wardrobe.call("set_race_filter", "rabbit")
	await _wait_frames(10)

	var costumes := [
		{"id": "none", "name": "none"},
		{"id": "costume_nutcracker_guard", "name": "nutcracker"},
		{"id": "costume_steam_artisan", "name": "steam"},
		{"id": "costume_royal_parade", "name": "royal"}
	]
	var paints := [
		{"id": "paint_ivory_stock", "name": "ivory"},
		{"id": "paint_brass_gold", "name": "brass"},
		{"id": "paint_midnight_navy", "name": "midnight"}
	]

	for c in costumes:
		_select_costume_by_id(c["id"])
		for p in paints:
			_select_chassis_by_id(p["id"])
			await _wait_frames(8)
			var fname := "05_wardrobe_%s_%s.png" % [c["name"], p["name"]]
			await _capture(fname)

	# --- 4. 跨族：兔穿維京束帶、兔穿星紋斗篷 ---
	print(">>> [4/5] 跨族外裝截圖...")
	# 切換篩選到 "all" 以便載入跨族裝備卡片
	_wardrobe.call("set_race_filter", "all")
	await _wait_frames(10)

	# 兔穿維京束帶 (costume_viking_harness)
	_select_chassis_by_id("paint_ivory_stock")
	_select_costume_by_id("costume_viking_harness")
	await _wait_frames(10)
	await _capture("06_cross_rabbit_viking_harness.png")

	# 兔穿星紋斗篷 (costume_astral_cape)
	_select_costume_by_id("costume_astral_cape")
	await _wait_frames(10)
	await _capture("07_cross_rabbit_astral_cape.png")

	print("=== 所有截圖產生完畢 ===")
	quit(0)
