extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = []
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始截取三件外裝（豬維京束帶／猴晨曦短襦／狐星紋斗篷）衣櫥實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var p1 := base.path_join("../proofs/costume_512_unique")
	var p2 := base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(p1)
	DirAccess.make_dir_recursive_absolute(p2)
	_out_dirs = [p1, p2]

	_run_captures()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture_frame(filename: String) -> void:
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

	for out_dir in _out_dirs:
		var p := out_dir.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ 成功存證截圖: ", p)
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

func _run_captures() -> void:
	await _wait_frames(10)
	var gs = root.get_node_or_null("GameState")

	# 1. 豬族：維京束帶 (costume_viking_harness)
	print("--- [1/3] 準備豬族維京束帶 ---")
	if gs:
		gs.player_race = "boar"
		gs.player_name = "鋼齒豬"
		gs.paperdoll_slots = {
			"race": "boar",
			"costume": "costume_viking_harness",
			"chassis": "paint_rust_iron",
			"costume_id": "costume_viking_harness",
			"paint_id": "paint_rust_iron",
			"weapon": "wpn_cog_halberd"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(15)

	_lobby.open_wardrobe()
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe != null:
		_wardrobe.call("set_race_filter", "boar")
		_select_costume_by_id("costume_viking_harness")
	await _wait_frames(30)
	print(">>> 截取豬族維京束帶畫面...")
	await _capture_frame("proof_wardrobe_boar_viking_harness.png")

	# 2. 猴族：晨曦短襦 (costume_dawn_monk_tunic)
	print("--- [2/3] 準備猴族晨曦短襦 ---")
	if gs:
		gs.player_race = "macaque"
		gs.player_name = "靈爪猴"
		gs.paperdoll_slots = {
			"race": "macaque",
			"costume": "costume_dawn_monk_tunic",
			"chassis": "paint_bamboo_bronze",
			"costume_id": "costume_dawn_monk_tunic",
			"paint_id": "paint_bamboo_bronze",
			"weapon": "wpn_spring_claws"
		}
	if _wardrobe != null:
		_wardrobe.call("set_race_filter", "macaque")
		_select_costume_by_id("costume_dawn_monk_tunic")
	await _wait_frames(30)
	print(">>> 截取猴族晨曦短襦畫面...")
	await _capture_frame("proof_wardrobe_macaque_dawn_monk_tunic.png")

	# 3. 狐族：星紋斗篷 (costume_astral_cape)
	print("--- [3/3] 準備狐族星紋斗篷 ---")
	if gs:
		gs.player_race = "fox"
		gs.player_name = "靈尾狐"
		gs.paperdoll_slots = {
			"race": "fox",
			"costume": "costume_astral_cape",
			"chassis": "paint_fox_orange",
			"costume_id": "costume_astral_cape",
			"paint_id": "paint_fox_orange",
			"weapon": "wpn_astral_staff"
		}
	if _wardrobe != null:
		_wardrobe.call("set_race_filter", "fox")
		_select_costume_by_id("costume_astral_cape")
	await _wait_frames(30)
	print(">>> 截取狐族星紋斗篷畫面...")
	await _capture_frame("proof_wardrobe_fox_astral_cape.png")

	if _wardrobe != null and is_instance_valid(_wardrobe):
		_wardrobe.call("close")
	if _lobby != null and is_instance_valid(_lobby):
		_lobby.queue_free()

	print("=== 所有截圖完成，正常結束 ===")
	quit(0)
