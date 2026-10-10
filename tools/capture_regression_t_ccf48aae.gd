extends SceneTree
## 《發條之心》四大背包與工坊閉環功能合併後全回歸驗收存證腳本 (t_ccf48aae)
## 覆蓋四大核心功能：
## 1. 背包Tab武器裝備拆解回收 (BtnBagDismantle)
## 2. 背包Tab裝備詳情顯示已鑲寶石與拆解返還
## 3. 天宮鐵匠與手藝工坊雙向直通快捷按鈕 (BtnGoWorkshop / BtnGoForge)
## 4. 背包Tab寶石素材與裝備直達工坊按鈕 (BtnBagGoWorkshop)

const MobileLobbyScript := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const OUT_DIRS: Array[String] = [
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ccf48aae/proofs/t_ccf48aae",
	"/opt/side/bravesoul-game/proofs/t_ccf48aae"
]

var _frame: int = 0
var _step: int = 0
var _wait: int = 0
var _ok: bool = true

var _lobby: Control = null
var _gs: Node = null
var _loc: Node = null
var _inv: Node = null
var _eq: Node = null
var _gem: Node = null

var _plain_weapon_uid: String = ""
var _gem_weapon_uid: String = ""
var _proof_hashes: Array[String] = []


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _init() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for d in OUT_DIRS:
		DirAccess.make_dir_recursive_absolute(d)

	change_scene_to_file("res://scenes/main.tscn")


func _setup_lobby_and_data() -> void:
	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")
	_eq = root.get_node_or_null("EquipmentSystem")
	_gem = root.get_node_or_null("GemSystem")

	if _gs == null or _loc == null or _inv == null or _eq == null or _gem == null:
		_fail("Autoload 節點初始化失敗")
		quit(1)
		return

	_gs.call("reset_new_game", "rabbit")
	_loc.call("set_locale", "zh_TW")
	ContentLoc.reload()

	# 物品準備
	_inv.call("add_item", "hp_s", 5)
	_inv.call("add_item", "iron_scrap", 15)
	_inv.call("add_item", "dust_crumb", 5)
	_inv.call("add_item", "gem_red", 2)
	_inv.call("add_item", "gem_blue", 1)

	# 建立 1: 可拆解普通裝備 (rusty_blade)
	var w_plain: Dictionary = _eq.call("roll_instance", "rusty_blade", "rare")
	_plain_weapon_uid = str(w_plain.get("uid", "proof_plain_w"))
	w_plain["uid"] = _plain_weapon_uid
	_eq.call("add_to_bag", w_plain)

	# 建立 2: 鑲嵌 1星紅寶石裝備 (dawn_blade)
	var w_gem: Dictionary = _eq.call("roll_instance", "dawn_blade", "epic")
	w_gem["gem"] = {"color": "red", "level": 1}
	_gem_weapon_uid = str(w_gem.get("uid", "proof_gem_w"))
	w_gem["uid"] = _gem_weapon_uid
	_eq.call("add_to_bag", w_gem)

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ✓ MobileLobby 初始化完成")


func _capture_and_save(file_name: String) -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("Viewport 為空")
		return ""
	var tex := vp.get_texture()
	if tex == null:
		_fail("Texture 為空")
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		_fail("Image 為空")
		return ""

	var primary_path := OUT_DIRS[0].path_join(file_name)
	var err := img.save_png(primary_path)
	if err != OK:
		_fail("儲存截圖失敗: %s" % primary_path)
		return ""

	var f := FileAccess.open(primary_path, FileAccess.READ)
	if f == null:
		_fail("讀取截圖失敗: %s" % primary_path)
		return ""
	var hash := f.get_buffer(f.get_length()).hex_encode().sha256_text()
	f.close()

	# 鏡像儲存至主 repo 存證目錄
	if OUT_DIRS.size() > 1:
		var secondary_path := OUT_DIRS[1].path_join(file_name)
		img.save_png(secondary_path)

	if _proof_hashes.has(hash):
		_fail("截圖 SHA256 重複: %s" % file_name)
	else:
		_proof_hashes.append(hash)

	print("  [PROOF SAVED] %s (1280x720, SHA256: %s)" % [file_name, hash.substr(0, 12)])
	return hash


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 15:
		return false

	if _frame == 15:
		_setup_lobby_and_data()
		return false

	match _step:
		0:
			# 截圖 1: 背包Tab選中武器裝備，右側顯示多巴胺珊瑚粉『拆解回收』按鈕 (BtnBagDismantle)
			_lobby.call("_switch_tab", 4) # Tab.BAG
			_lobby.set("_selected_bag_item", _plain_weapon_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save("proof_01_bag_dismantle_btn_visible.png")
			_wait = 0
			_step = 1

		1:
			# 截圖 2: 背包Tab選中鑲寶石武器，詳情面板顯示已鑲寶石資訊、星級加成與安全返還
			_lobby.set("_selected_bag_item", _gem_weapon_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save("proof_02_bag_gem_detail_and_refund.png")
			_wait = 0
			_step = 2

		2:
			# 截圖 3: 天宮鐵匠彈窗 ForgeDialog，顯示薄荷綠『前往工坊』直通按鈕 (BtnGoWorkshop)
			_lobby.call("open_forge", _gem_weapon_uid)
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save("proof_03_forge_workshop_bidirectional_link.png")
			var forge_dlg = _lobby.get_node_or_null("ForgeDialog")
			if forge_dlg:
				forge_dlg.queue_free()
			_wait = 0
			_step = 3

		3:
			# 截圖 4: 背包Tab選中星屑素材時，右側詳情面板顯示多巴胺薄荷綠『前往工坊』按鈕 (BtnBagGoWorkshop)
			_lobby.call("_switch_tab", 4) # Tab.BAG
			_lobby.set("_selected_bag_item", "dust_crumb")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save("proof_04_bag_workshop_shortcut_btn.png")
			_wait = 0
			_step = 4

		4:
			if _ok and _proof_hashes.size() == 4:
				print("\n=======================================================")
				print("ALL_REGRESSION_PROOFS_OK (4/4 獨立存證完成)")
				print("=======================================================")
				quit(0)
			else:
				push_error("REGRESSION_PROOFS_FAILED")
				quit(1)
			return true

	return false
