extends SceneTree
## 全面回歸驗收截圖存證腳本 (t_1c9863a0)
## 驗收內容：
## 1. 大廳角色頁三欄武器槽連動真實裝備、品質色階、即時切換與紙娃娃零穿模 (slot 0/1/2)
## 2. 探索寶箱消耗品與材料專有名詞 100% 玩具世界化轉譯 (zh_TW, en, ja) 零舊奇幻殘留

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const MapleInventoryScript = preload("res://scripts/ui/maple_inventory.gd")
const MapleHotbarScript = preload("res://scripts/ui/maple_hotbar.gd")

const OUT_DIRS := [
	"/opt/side/bravesoul-game/proofs/t_1c9863a0",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_1c9863a0/proofs"
]

var _stage: int = 0
var _frame: int = 0
var _lobby: Control = null
var _hotbar: Control = null
var _inv: Control = null
var _loc: Node = null
var _gs: Node = null
var _eq: Node = null
var _inv_sys: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for d in OUT_DIRS:
		DirAccess.make_dir_recursive_absolute(d)
		DirAccess.make_dir_recursive_absolute(d.path_join("crops"))

	_loc = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_inv_sys = root.get_node_or_null("InventorySystem")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 20)

	if _loc:
		_loc.call("set_locale", "zh_TW")

	_setup_weapons()
	_setup_inventory()

	_lobby = MobileLobbyScript.new()
	_lobby.size = Vector2(1280, 720)
	root.add_child(_lobby)

	print("=== 開始執行 t_1c9863a0 全面回歸實機截圖 ===")
	_stage = 0
	_frame = 0


func _setup_weapons() -> void:
	var w_sword := {
		"uid": "w_live_sword", "base_id": "sword", "name": "晨曦長劍", "line": "sword",
		"slot": "weapon", "tier": 1, "quality": "rare", "quality_label": "上品",
		"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 2.0, "crit_dmg": 5.0}
	}
	var w_spear := {
		"uid": "w_live_spear", "base_id": "spear", "name": "破浪長槍", "line": "spear",
		"slot": "weapon", "tier": 1, "quality": "uncommon", "quality_label": "良品",
		"rolled": {"atk": 12, "def": 2, "hp": 0, "crit": 1.0, "crit_dmg": 0.0}
	}
	var w_fist := {
		"uid": "w_live_fist", "base_id": "fist", "name": "熔火鐵拳", "line": "fist",
		"slot": "weapon", "tier": 1, "quality": "epic", "quality_label": "秘寶",
		"rolled": {"atk": 20, "def": 0, "hp": 10, "crit": 3.0, "crit_dmg": 10.0}
	}

	_gs.equip_worn["w_live_sword"] = w_sword
	_gs.equip_worn["w_live_spear"] = w_spear
	_gs.equip_worn["w_live_fist"] = w_fist
	_gs.weapon_loadout = ["w_live_sword", "w_live_spear", "w_live_fist"]
	_gs.weapon_loadout_active = 0
	_gs.equip_slots["weapon"] = "w_live_sword"


func _setup_inventory() -> void:
	_gs.inventory = {
		"hp_s": 15,
		"hp_m": 5,
		"bread": 20,
		"antidote": 8,
		"hunt_bone": 12,
		"hunt_hide": 16,
		"star_ore": 30,
		"wolf_fang": 10,
		"iron_scrap": 25,
		"key_rusty": 1,
		"friendship_key": 3,
		"windup_fragment": 7
	}
	if _inv_sys:
		_inv_sys.call("ensure_hotbar")
		_inv_sys.call("set_hotbar", 0, "hp_s")
		_inv_sys.call("set_hotbar", 1, "bread")
		_inv_sys.call("set_hotbar", 2, "iron_scrap")


func _save_image_and_crop(fname: String, crop_fname: String, crop_rect: Rect2i) -> void:
	var vp := root.get_viewport()
	var img := vp.get_texture().get_image()
	if img == null:
		push_error("無法獲取 viewport image: " + fname)
		return

	for dir: String in OUT_DIRS:
		var target: String = dir.path_join(fname)
		var err := img.save_png(target)
		if err == OK:
			print("  ✓ 截圖儲存成功: ", target)
		else:
			push_error("  ✗ 儲存失敗: " + target)

		if crop_fname != "":
			var crop_target: String = dir.path_join("crops").path_join(crop_fname)
			var cropped: Image = img.get_region(crop_rect)
			cropped.save_png(crop_target)
			print("  ✓ 局部裁切儲存: ", crop_target)


func _process(_delta: float) -> bool:
	_frame += 1

	match _stage:
		# ------------------------------------------------------------------
		# Stage 0: 大廳角色頁 - 首選武器 (晨曦長劍, slot 0)
		# ------------------------------------------------------------------
		0:
			if _frame == 2:
				_loc.call("set_locale", "zh_TW")
				_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
				_lobby.select_weapon_slot(0)
				_lobby.refresh_weapon_slots()
			elif _frame >= 15:
				print("\n--- [1/6] 捕捉大廳角色頁：首選武器 晨曦長劍 (Slot 0) ---")
				_save_image_and_crop(
					"proof_01_lobby_weapon_slot0_sword.png",
					"crop_01_weapon_slots_sword.png",
					Rect2i(320, 100, 640, 520)
				)
				_stage = 1
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 1: 大廳角色頁 - 切換至副手武器 (破浪長槍, slot 1)
		# ------------------------------------------------------------------
		1:
			if _frame == 2:
				_lobby.select_weapon_slot(1)
				_lobby.refresh_weapon_slots()
			elif _frame >= 15:
				print("\n--- [2/6] 捕捉大廳角色頁：副手武器 破浪長槍 (Slot 1, 暖橘選中態與零穿模) ---")
				_save_image_and_crop(
					"proof_02_lobby_weapon_slot1_spear.png",
					"crop_02_weapon_slots_spear.png",
					Rect2i(320, 100, 640, 520)
				)
				_stage = 2
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 2: 大廳角色頁 - 切換至絕技武器 (熔火鐵拳, slot 2)
		# ------------------------------------------------------------------
		2:
			if _frame == 2:
				_lobby.select_weapon_slot(2)
				_lobby.refresh_weapon_slots()
			elif _frame >= 15:
				print("\n--- [3/6] 捕捉大廳角色頁：絕技武器 熔火鐵拳 (Slot 2, 秘寶品質與零穿模) ---")
				_save_image_and_crop(
					"proof_03_lobby_weapon_slot2_fist.png",
					"crop_03_weapon_slots_fist.png",
					Rect2i(320, 100, 640, 520)
				)
				_stage = 3
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 3: 背包介面 (繁中 zh_TW) - 玩具世界化寶箱消耗品與材料
		# ------------------------------------------------------------------
		3:
			if _frame == 2:
				_lobby._switch_tab(MobileLobbyScript.Tab.VILLAGE)
				if _hotbar == null:
					_hotbar = MapleHotbarScript.new()
					_hotbar.name = "MapleHotbar"
					root.add_child(_hotbar)
				if _inv == null:
					_inv = MapleInventoryScript.new()
					_inv.name = "MapleInventory"
					root.add_child(_inv)
					_inv.call("open")
			elif _frame >= 25:
				print("\n--- [4/6] 捕捉背包介面 (繁中)：玩具世界化消耗品與材料 ---")
				_save_image_and_crop(
					"proof_04_inventory_toy_items_zh_TW.png",
					"crop_04_inventory_toy_items_zh_TW.png",
					Rect2i(250, 80, 780, 560)
				)
				_stage = 4
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 4: 背包介面 (英文 en) - 六語系同屏動態連動切換
		# ------------------------------------------------------------------
		4:
			if _frame == 2:
				_loc.call("set_locale", "en")
			elif _frame >= 25:
				print("\n--- [5/6] 捕捉背包介面 (英文)：同屏切換連動與零 CJK 殘留 ---")
				_save_image_and_crop(
					"proof_05_inventory_toy_items_en.png",
					"crop_05_inventory_toy_items_en.png",
					Rect2i(250, 80, 780, 560)
				)
				_stage = 5
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 5: 背包介面 (日文 ja) - 六語系日本常用漢字核實
		# ------------------------------------------------------------------
		5:
			if _frame == 2:
				_loc.call("set_locale", "ja")
			elif _frame >= 25:
				print("\n--- [6/6] 捕捉背包介面 (日文)：日本常用漢字道地對齊 ---")
				_save_image_and_crop(
					"proof_06_inventory_toy_items_ja.png",
					"crop_06_inventory_toy_items_ja.png",
					Rect2i(250, 80, 780, 560)
				)
				_stage = 6
				_frame = 0

		# ------------------------------------------------------------------
		# Stage 6: 完成收工
		# ------------------------------------------------------------------
		6:
			print("\n=== 全部實機截圖存證完成 (t_1c9863a0) ===")
			quit(0)

	return false
