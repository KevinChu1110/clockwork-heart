extends SceneTree
## 《發條之心》九族全數補齊第二套外裝後的全域回歸驗收截圖腳本 (Xvfb + OpenGL3)
## 覆蓋九族：兔、狐、獅、豬、猴、虎、鶴、熊、企鵝
## 每族截取：
## 1. 大廳待機 (MobileLobby Tab.VILLAGE)
## 2. 衣櫥換裝彈窗 (WardrobeDialog) 第二套外裝與塗裝展示
## 3. 角色高解析對照裁切 (Char Zoom 256x256) 供 vision 0-ART9 / CANON 驗收
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_nine_race_regression.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

var _proofs_dir: String = ""
var _wait_frames: int = 0
var _current_race_idx: int = 0
var _current_substep: int = 0 # 0: setup lobby, 1: wait & capture lobby, 2: setup wardrobe, 3: wait & capture wardrobe

var _lobby: MobileLobby = null
var _wardrobe: Control = null

const RACES_ORDER: Array[Dictionary] = [
	{
		"race": "rabbit",
		"name": "小白",
		"costume": "costume_steam_artisan",
		"costume_name": "蒸氣工匠吊帶工作裝",
		"chassis": "paint_brass_gold",
		"chassis_name": "黃銅原金拋光",
		"weapon": "wpn_dawn_blade"
	},
	{
		"race": "fox",
		"name": "靈尾狐",
		"costume": "costume_astral_observer",
		"costume_name": "星象觀測者金屬儀裝",
		"chassis": "paint_emerald_glaze",
		"chassis_name": "翡翠螢光釉面",
		"weapon": "wpn_astral_staff"
	},
	{
		"race": "lion",
		"name": "烈鬃獅",
		"costume": "costume_steam_artisan",
		"costume_name": "蒸氣工匠吊帶工作裝",
		"chassis": "paint_midnight_navy",
		"chassis_name": "午夜深藍烤漆",
		"weapon": "wpn_knight_lance"
	},
	{
		"race": "boar",
		"name": "鋼牙豕",
		"costume": "costume_viking_ironclad",
		"costume_name": "維京重裝鍛鐵板甲",
		"chassis": "paint_molten_crimson",
		"chassis_name": "赤焰熔爐烤漆",
		"weapon": "wpn_anvil_greathammer"
	},
	{
		"race": "macaque",
		"name": "靈爪猴",
		"costume": "costume_zen_striker",
		"costume_name": "天元演武者機關甲",
		"chassis": "paint_bamboo_bronze",
		"chassis_name": "天元青古銅烤漆",
		"weapon": "wpn_spring_claws"
	},
	{
		"race": "tiger",
		"name": "烈焰虎",
		"costume": "costume_ash_ninja_garb",
		"costume_name": "灰燼夜行機關裝",
		"chassis": "paint_volcano_black",
		"chassis_name": "鍛爐淬火曜黑烤漆",
		"weapon": "wpn_twin_ember_sabers"
	},
	{
		"race": "crane",
		"name": "雲嵐鶴",
		"costume": "costume_sky_hunter_mail",
		"costume_name": "晴空巡獵機關羽甲",
		"chassis": "paint_zephyr_azure",
		"chassis_name": "晴空凌雲湛藍",
		"weapon": "wpn_zephyr_wing_bow"
	},
	{
		"race": "bear",
		"name": "玄軸熊",
		"costume": "costume_berserker_cuirass",
		"costume_name": "狂戰破陣機關戰鎧",
		"chassis": "paint_iron_quarry",
		"chassis_name": "重裝礦山玄鐵灰",
		"weapon": "wpn_eccentric_gyro_sledge"
	},
	{
		"race": "penguin",
		"name": "蒸氣企鵝",
		"costume": "costume_abyssal_diver_cuirass",
		"costume_name": "淵海深潛耐壓機關鎧",
		"chassis": "paint_polar_frost",
		"chassis_name": "極光冰川銀白",
		"weapon": "wpn_twin_harpoon_gun"
	}
]


func _initialize() -> void:
	print("=== 開始九族全域回歸實機截圖 (Xvfb + OpenGL3) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proofs_dir = base.path_join("../proofs/nine_race_regression")
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	_current_race_idx = 0
	_current_substep = 0
	_wait_frames = 0
	_setup_lobby_for_current_race()


func _setup_lobby_for_current_race() -> void:
	var info: Dictionary = RACES_ORDER[_current_race_idx]
	var r: String = str(info["race"])
	var r_name: String = str(info["name"])
	print("\n--- [%d/9] 設定種族: %s (%s) ---" % [_current_race_idx + 1, r, r_name])

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", r)
		gs.set("player_race", r)
		gs.set("player_name", r_name)
		gs.set("paperdoll_slots", {
			"race": r,
			"costume": info["costume"],
			"chassis": info["chassis"],
			"costume_id": info["costume"],
			"paint_id": info["chassis"],
			"weapon": info["weapon"]
		})

	# 實例化大廳
	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	_current_substep = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1
	var info: Dictionary = RACES_ORDER[_current_race_idx]
	var r: String = str(info["race"])
	var idx_str := "%02d_%s" % [_current_race_idx + 1, r]

	match _current_substep:
		1: # Wait and capture lobby
			if _wait_frames >= 30:
				var lobby_fn := "proof_%s_lobby.png" % idx_str
				_save_screenshot(lobby_fn)
				print("  ✓ [%s] 大廳待機截圖完成 -> %s" % [r, lobby_fn])

				# 另存高解析獨立合成裁切圖供 0-ART9 嚴查
				_save_character_composite_zoom(idx_str, info)

				# 開啟衣櫥
				_lobby.open_wardrobe()
				_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
				if _wardrobe:
					_wardrobe.set_race_filter(r)
					# 選定第二套外裝與塗裝變體
					var costumes: Array = _wardrobe.get("_displayed_costumes")
					for i in range(costumes.size()):
						if str(costumes[i].get("id", "")) == info["costume"]:
							_wardrobe.set("costume_index", i)
							_wardrobe.set("selected_costume_id", str(info["costume"]))
							break
					var chassis_list: Array = _wardrobe.get("_displayed_chassis")
					for i in range(chassis_list.size()):
						if str(chassis_list[i].get("id", "")) == info["chassis"]:
							_wardrobe.set("chassis_index", i)
							_wardrobe.set("selected_chassis_id", str(info["chassis"]))
							break
					if _wardrobe.has_method("_update_card_selection_states"):
						_wardrobe.call("_update_card_selection_states")
					if _wardrobe.has_method("_update_preview"):
						_wardrobe.call("_update_preview")
					if _wardrobe.has_method("_update_ui_texts"):
						_wardrobe.call("_update_ui_texts")
					print("  [Wardrobe] 已選中外裝: %s, 塗裝: %s" % [info["costume_name"], info["chassis_name"]])

				_current_substep = 3
				_wait_frames = 0

		3: # Wait and capture wardrobe
			if _wait_frames >= 35:
				var wardrobe_fn := "proof_%s_wardrobe.png" % idx_str
				_save_screenshot(wardrobe_fn)
				print("  ✓ [%s] 衣櫥第二套外裝截圖完成 -> %s" % [r, wardrobe_fn])

				# 關閉衣櫥並釋放大廳
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				# 進入下一族或結束
				_current_race_idx += 1
				if _current_race_idx < RACES_ORDER.size():
					_current_substep = 0
					_wait_frames = 0
					_setup_lobby_for_current_race()
				else:
					print("\n=== 全部九族（18 張實機截圖 ＋ 9 張高解析角色特寫）截圖完畢！ ===")
					quit(0)
					return true

	return false


func _save_character_composite_zoom(idx_str: String, info: Dictionary) -> void:
	var r: String = str(info["race"])
	var sel := {
		"race": r,
		"costume": info["costume"],
		"chassis": info["chassis"],
		"costume_id": info["costume"],
		"paint_id": info["chassis"],
		"weapon": info["weapon"]
	}
	var img := PaperdollRenderer.build_composite_image(r, sel)
	if img != null and not img.is_empty():
		var zoom := img.duplicate()
		zoom.resize(384, 384, Image.INTERPOLATE_NEAREST)
		var zoom_fn := "proof_%s_char_zoom_384px.png" % idx_str
		var p := _proofs_dir.path_join(zoom_fn)
		zoom.save_png(p)
		print("  ✓ [%s] 角色特寫 (384x384) 存檔 -> %s" % [r, zoom_fn])


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("無法取得 Viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("無法取得 ViewportTexture")
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("無法取得 Image")
		return

	var file_path := _proofs_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [儲存成功] %s (%dx%d)" % [file_path, img.get_width(), img.get_height()])
	else:
		push_error("儲存失敗: %s (err=%d)" % [file_path, err])
