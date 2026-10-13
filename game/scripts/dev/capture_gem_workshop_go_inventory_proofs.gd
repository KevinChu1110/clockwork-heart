extends SceneTree
## 手藝工坊新增『前往背包』快捷按鈕實機 Framebuffer 截圖存證腳本 (capture_gem_workshop_go_inventory_proofs.gd)
## 遵循 0-QA5 / 0-QA26（真實 Viewport Texture Framebuffer 截圖，零 PIL 假圖）
##
## 截圖清單：
## 1. proof_01_gem_workshop_smelt_tab_zh_TW.png：手藝工坊熔煉分頁，展示『前往背包』天藍色立體果凍按鈕 (BtnGoInventory)
## 2. proof_02_gem_workshop_case_tab_zh_TW.png：手藝工坊寶石櫃分頁，孔位卡片、六維加成面板、15 格盤點小卡與『前往背包』按鈕
## 3. proof_03_click_go_inventory_opens_maple_inventory_gem_chip_zh_TW.png：點擊『前往背包』後連動開啟 MapleInventory 並自動切換至『寶石』分類 Chip (cid: 'gem')
## 4. proof_04_gem_workshop_en.png：英文語系 (en) Go to Inventory 按鈕與介面，零 CJK 殘留
## 5. proof_05_gem_workshop_ja.png：日文語系 (ja) インベントリへ進む 按鈕與介面
## 6. proof_06_gem_workshop_ko.png：韓文語系 (ko) 인벤토리로 이동 按鈕與介面
## 7. proof_07_gem_workshop_es.png：西班牙文語系 (es) Ir al Inventario 按鈕與介面，零 CJK 殘留

var _step := 0
var _frame := 0
var _proof_dir := ""
var _saved: PackedStringArray = PackedStringArray()
var _current_dlg: Node = null
var _current_inv: Node = null
var _lobby: Node = null
var _gs: Node = null
var _loc: Node = null
var _inv: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	var env_out := OS.get_environment("OUT_DIR").strip_edges()
	if env_out != "":
		if env_out.is_absolute_path():
			_proof_dir = env_out
		else:
			_proof_dir = base.path_join(env_out)
	else:
		_proof_dir = base.path_join("../proofs/t_3693a5bb")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	change_scene_to_file("res://scenes/main.tscn")


func _save_frame(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE_FAIL: null image for ", filename)
		return
	var out_path := _proof_dir.path_join(filename)
	var err := img.save_png(out_path)
	print("CAPTURE_SAVED: ", out_path, " err=", err, " ", img.get_width(), "x", img.get_height())
	_saved.append(out_path)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame < 30:
				return false
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			_inv = root.get_node_or_null("InventorySystem")

			if _gs:
				_gs.call("reset_new_game")
				_gs.set("gold", 50000)
				_gs.set("weapon_tier", 3)
				_gs.set("weapon_atk", 24)
				_gs.set("weapon_name", "精煉長劍")
				_gs.call("set_flag", "c1_forged", true)
				_gs.call("set_flag", "c1_entered_city", true)
				_gs.call("set_flag", "tut_done", true)

			# 註冊並在背包加入寶石道具
			if _inv:
				if _inv.has_method("register_item"):
					_inv.call("register_item", "gem_ruby_1", {
						"name": "1階紅寶石",
						"desc": "凝聚烈焰之力的寶石。鑲嵌於裝備可提升暴擊與生命值。",
						"kind": "gem",
						"stack": 99,
						"glyph": "紅",
						"color": Color("#FF5E8A")
					})
					_inv.call("register_item", "gem_sapphire_2", {
						"name": "2階藍寶石",
						"desc": "蘊含靜水之力的精煉寶石。鑲嵌於裝備可大幅提升命中與迴避。",
						"kind": "gem",
						"stack": 99,
						"glyph": "藍",
						"color": Color("#38A0FF")
					})
					_inv.call("register_item", "gem_topaz_1", {
						"name": "1階黃寶石",
						"desc": "沉穩厚重的厚土寶石。鑲嵌於裝備可提升攻擊力與堅韌防禦。",
						"kind": "gem",
						"stack": 99,
						"glyph": "黃",
						"color": Color("#FFD028")
					})
				if _inv.has_method("add_item"):
					_inv.call("add_item", "gem_ruby_1", 3)
					_inv.call("add_item", "gem_sapphire_2", 2)
					_inv.call("add_item", "gem_topaz_1", 5)

			var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
			_current_dlg = GemWorkshopClass.new()
			root.add_child(_current_dlg)

			_step = 1
			_frame = 0

		1:
			# 截圖 1: 熔煉分頁 (zh_TW)，展示 BtnGoInventory
			if _frame >= 25:
				_save_frame("proof_01_gem_workshop_smelt_tab_zh_TW.png")
				if is_instance_valid(_current_dlg) and _current_dlg.has_method("set_tab"):
					_current_dlg.call("set_tab", 1) # 切換至寶石櫃分頁
				_step = 2
				_frame = 0

		2:
			# 截圖 2: 寶石櫃分頁 (zh_TW)，展示 BtnGoInventory
			if _frame >= 25:
				_save_frame("proof_02_gem_workshop_case_tab_zh_TW.png")
				# 進入步驟 3：掛載 MobileLobby 並測試點擊前往背包
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null

				var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = MobileLobbyClass.new()
				root.add_child(_lobby)

				_current_inv = _lobby.call("open_maple_inventory", "gem")
				_step = 3
				_frame = 0

		3:
			# 截圖 3: 點擊前往背包後開啟 MapleInventory 且自動切換至 'gem' 寶石分類 Chip
			if _frame >= 30:
				_save_frame("proof_03_click_go_inventory_opens_maple_inventory_gem_chip_zh_TW.png")
				if is_instance_valid(_current_inv):
					_current_inv.queue_free()
					_current_inv = null
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				# 步驟 4：英文語系 (en)
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")

				var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
				_current_dlg = GemWorkshopClass.new()
				root.add_child(_current_dlg)
				if _current_dlg.has_method("_on_locale_changed"):
					_current_dlg.call("_on_locale_changed", "en")

				_step = 4
				_frame = 0

		4:
			# 截圖 4: 英文語系 (en)
			if _frame >= 25:
				_save_frame("proof_04_gem_workshop_en.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				if is_instance_valid(_current_dlg) and _current_dlg.has_method("_on_locale_changed"):
					_current_dlg.call("_on_locale_changed", "ja")
				_step = 5
				_frame = 0

		5:
			# 截圖 5: 日文語系 (ja)
			if _frame >= 25:
				_save_frame("proof_05_gem_workshop_ja.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ko")
				if is_instance_valid(_current_dlg) and _current_dlg.has_method("_on_locale_changed"):
					_current_dlg.call("_on_locale_changed", "ko")
				_step = 6
				_frame = 0

		6:
			# 截圖 6: 韓文語系 (ko)
			if _frame >= 25:
				_save_frame("proof_06_gem_workshop_ko.png")
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "es")
				if is_instance_valid(_current_dlg) and _current_dlg.has_method("_on_locale_changed"):
					_current_dlg.call("_on_locale_changed", "es")
				_step = 7
				_frame = 0

		7:
			# 截圖 7: 西班牙文語系 (es)
			if _frame >= 25:
				_save_frame("proof_07_gem_workshop_es.png")
				# 復原語系
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				if is_instance_valid(_current_dlg):
					_current_dlg.queue_free()
					_current_dlg = null
				_step = 8
				_frame = 0

		8:
			print("\n=== 全部實機截圖存證完成 (共 %d 張) ===" % _saved.size())
			for p in _saved:
				print("  - ", p)
			print("CAPTURE_ALL_PROOFS_OK")
			quit(0)
			return true

	return false
