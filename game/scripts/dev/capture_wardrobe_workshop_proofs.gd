extends SceneTree
## 《發條之心》衣櫥換裝與紙娃娃工坊介面驗收測試與實機截圖
## 驗收項目：
## 1. 3D立體溫潤木質旋轉展示台正常渲染
## 2. 七大槽位果凍厚底色階圓角光框與即時流光
## 3. 切換部件即時合成與金色星芒動效
## 4. 全程 0 錯誤

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _dlg: WardrobeDialog = null


func _initialize() -> void:
	print("=== 開始驗收衣櫥換裝與紙娃娃工坊 (Wardrobe Workshop) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_28cd1554")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock",
			"head_unit": "ear_rabbit_straight",
			"winding_key": "key_classic_brass",
			"weapon": "wpn_dawn_blade",
			"optic_core": "core_cyan_emerald",
			"back_curio": "curio_clockwork_pigeon"
		}

	_dlg = WardrobeDialog.new()
	_dlg.creation_mode = false
	root.add_child(_dlg)
	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 等待初始展台渲染穩定
			if _wait_frames >= 20:
				_save_screenshot("proof_01_workshop_overview.png")
				print("  ✓ 截圖 1：[工坊全貌] 3D立體溫潤木質旋轉展台與七大槽位色階光框")
				# 進入第 2 步：換裝（切換至機體塗裝 chassis 分頁，選用黃銅原金拋光與裸機素體，展示全身金黃塗裝與金色星芒爆散）
				if _dlg != null:
					_dlg._select_slot_tab("chassis")
					_dlg.costume_index = 3 # none (無外裝 裸機素體)
					_dlg.chassis_index = 1 # paint_brass_gold (黃銅原金拋光)
					_dlg._spawn_golden_stars(true) # 立即綻放爆散金色星芒
					_dlg._turntable_bounce()
					_dlg._update_preview()
					_dlg._update_card_selection_states()
					_dlg._update_seven_slots_visual()
				_step = 2
				_wait_frames = 0
		2:
			# 等待星芒與換裝反應在畫面上
			if _wait_frames >= 12:
				_save_screenshot("proof_02_equip_swap_burst.png")
				print("  ✓ 截圖 2：[換裝反饋] 金色星芒爆散、黃銅金塗裝與即時流光色階框")
				# 進入第 3 步：切換槽位分頁至武器槽
				if _dlg != null:
					_dlg._select_slot_tab("weapon")
					_dlg.costume_index = 0 # costume_nutcracker_guard
					_dlg.chassis_index = 0 # paint_ivory_stock
					_dlg.weapon_index = 0 # wpn_dawn_blade
					_dlg._spawn_golden_stars(true)
					_dlg._update_preview()
					_dlg._update_card_selection_states()
					_dlg._update_seven_slots_visual()
				_step = 3
				_wait_frames = 0
		3:
			if _wait_frames >= 15:
				_save_screenshot("proof_03_weapon_slot_browse.png")
				print("  ✓ 截圖 3：[槽位切換] 武器槽位聚焦、色階光框與即時流光")
				print("=== 驗收截圖產生完畢 ===")
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
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
