extends SceneTree
## 六族頭部塗裝同步實機換裝截圖產生器 (t_d11b0432 / 0-ART28h)
## 獅、狐、豬、猴、虎、鶴

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _gs: Node = null
var _out_dir: String = ""

const TARGETS: Array[Dictionary] = [
	# 1. 烈鬃獅
	{"race": "lion", "chassis": "paint_midnight_navy", "full": "proof_wardrobe_lion_midnight.png", "comp": "composite_512_lion_midnight.png"},
	{"race": "lion", "chassis": "paint_ivory_stock", "full": "proof_wardrobe_lion_ivory.png", "comp": "composite_512_lion_ivory.png"},
	
	# 2. 靈尾狐
	{"race": "fox", "chassis": "paint_emerald_glaze", "full": "proof_wardrobe_fox_emerald.png", "comp": "composite_512_fox_emerald.png"},
	{"race": "fox", "chassis": "paint_ivory_stock", "full": "proof_wardrobe_fox_ivory.png", "comp": "composite_512_fox_ivory.png"},
	
	# 3. 鋼牙豕
	{"race": "boar", "chassis": "paint_molten_crimson", "full": "proof_wardrobe_boar_crimson.png", "comp": "composite_512_boar_crimson.png"},
	{"race": "boar", "chassis": "paint_brass_gold", "full": "proof_wardrobe_boar_brass.png", "comp": "composite_512_boar_brass.png"},
	
	# 4. 靈爪猴
	{"race": "macaque", "chassis": "paint_bamboo_bronze", "full": "proof_wardrobe_macaque_bronze.png", "comp": "composite_512_macaque_bronze.png"},
	
	# 5. 烈焰虎
	{"race": "tiger", "chassis": "paint_volcano_black", "full": "proof_wardrobe_tiger_volcano.png", "comp": "composite_512_tiger_volcano.png"},
	{"race": "tiger", "chassis": "paint_ivory_stock", "full": "proof_wardrobe_tiger_ivory.png", "comp": "composite_512_tiger_ivory.png"},
	
	# 6. 雲嵐鶴
	{"race": "crane", "chassis": "paint_zephyr_azure", "full": "proof_wardrobe_crane_azure.png", "comp": "composite_512_crane_azure.png"},
	{"race": "crane", "chassis": "paint_ivory_stock", "full": "proof_wardrobe_crane_ivory.png", "comp": "composite_512_crane_ivory.png"}
]

func _initialize() -> void:
	print("=== 開始執行六族頭部塗裝同步實機換裝截圖 (t_d11b0432) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/head_sync_proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run()

func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _capture(full_fn: String, comp_fn: String = "") -> void:
	await _wait_frames(3)
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		push_error("截圖失敗: 無 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("截圖失敗: 無 Texture")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗: 空畫面")
		return

	var full_p := _out_dir.path_join(full_fn)
	img.save_png(full_p)
	print("  ✓ 實機全景截圖: %s" % full_p)

	if not comp_fn.is_empty() and _wardrobe != null:
		var pr_rect: TextureRect = _wardrobe.get("_preview_rect")
		if pr_rect and pr_rect.texture:
			var comp_img := pr_rect.texture.get_image()
			if comp_img and not comp_img.is_empty():
				var comp_p := _out_dir.path_join(comp_fn)
				comp_img.save_png(comp_p)
				print("  ✓ 512高清合成角色存證: %s" % comp_p)

func _select_costume_by_id(target_id: String) -> bool:
	if _wardrobe == null or not is_instance_valid(_wardrobe):
		return false
	var displayed: Array = _wardrobe.get("_displayed_costumes")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
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
	var displayed: Array = _wardrobe.get("_displayed_chassis")
	for i in range(displayed.size()):
		var item: Dictionary = displayed[i]
		if str(item.get("id", "")) == target_id:
			_wardrobe.set("chassis_index", i)
			_wardrobe.set("selected_chassis_id", target_id)
			_wardrobe.call("_update_card_selection_states")
			_wardrobe.call("_update_preview")
			_wardrobe.call("_update_ui_texts")
			return true
	return false

func _run() -> void:
	await _wait_frames(10)
	_gs = root.get_node_or_null("GameState")

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	await _wait_frames(25)

	_lobby.open_wardrobe()
	await _wait_frames(20)
	_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
	if _wardrobe == null:
		push_error("無法找到 WardrobeDialog 節點！")
		quit(1)
		return

	var curr_race := ""
	for tgt in TARGETS:
		var r: String = tgt["race"]
		var ch: String = tgt["chassis"]
		var full_fn: String = tgt["full"]
		var comp_fn: String = tgt["comp"]
		
		if r != curr_race:
			curr_race = r
			print("\n--- 切換種族: %s ---" % r)
			if _gs:
				_gs.set("player_race", r)
				_gs.set("paperdoll_slots", {})
			SpriteDB.clear_equipped_cache()
			_wardrobe.call("set_race_filter", r)
			await _wait_frames(15)
			_select_costume_by_id("none")
			await _wait_frames(5)
			
		print("  -> 選擇塗裝: %s" % ch)
		_select_chassis_by_id(ch)
		await _wait_frames(10)
		await _capture(full_fn, comp_fn)

	print("\n=== 全部六族實機截圖完成 ===")
	quit(0)
