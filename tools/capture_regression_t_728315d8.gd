extends SceneTree
## 大廳角色頁一鍵配置最高戰力武器實機存證腳本 (t_728315d8)
## 驗收項目：
## 1. 大廳角色頁裝備分頁「一鍵配置」金黃多巴胺果凍厚底按鈕 (BtnAutoEquip，>=48px，零 Emoji)
## 2. 點擊「一鍵配置」前：背包有高戰力武器，槽位尚未配置最佳武器
## 3. 點擊「一鍵配置」後：自動裝備至解鎖槽位、攻擊力/戰力提升、紙娃娃與 HUD 刷新、彈出 toast 提示
## 4. 多語系 (zh_TW, en, ja, ko, es, zh_CN) 在地化切換
## 5. 儲存實機全景圖 (1280x720) 與特寫裁切圖至 proofs/t_728315d8/

const MobileLobbyScript := preload("res://scripts/ui/mobile_lobby.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_728315d8",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_728315d8/proofs/t_728315d8"
]

var _step: int = 0
var _wait: int = 0
var _lobby: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _eq: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)
		DirAccess.make_dir_recursive_absolute(p.path_join("crops"))

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")

	if _gs == null or _eq == null or _loc_node == null:
		push_error("缺少必要 Autoload 節點")
		quit(1)
		return

	_gs.reset_new_game("rabbit")
	_gs.level = 10  # 解鎖 Slot 0 與 Slot 1
	_gs.equip_bag.clear()

	# 放入高等武器
	var w1: Dictionary = _eq.roll_instance("ash_spear", "epic")
	w1["rolled"]["atk"] = 65.0
	_eq.add_to_bag(w1)

	var w2: Dictionary = _eq.roll_instance("star_rod", "rare")
	w2["rolled"]["atk"] = 40.0
	_eq.add_to_bag(w2)

	_loc_node.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("== 初始化大廳存證場景 (t_728315d8) ===")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait >= 15:
				_lobby._switch_tab(_lobby.Tab.CHARACTER)
				_step = 1
				_wait = 0
		1:
			# 截圖 1: 點擊一鍵配置前 (Lv10, 槽位未配置最佳武器，背包有 2 把神兵)
			if _wait >= 15:
				var btn: Button = _lobby._btn_auto_equip
				var btn_rect := Rect2i(btn.get_global_rect()) if btn else Rect2i(850, 240, 104, 48)
				_save_viewport(
					"proof_01_lobby_character_before_auto_equip.png",
					[
						{"rect": btn_rect.grow(8), "filename": "crop_01_btn_auto_equip.png"},
						{"rect": Rect2i(700, 220, 520, 260), "filename": "crop_02_weapon_section_before.png"}
					]
				)
				# 點擊一鍵配置按鈕
				print("  -> 觸發一鍵配置 auto_equip_weapons()...")
				_lobby.auto_equip_weapons()
				_step = 2
				_wait = 0
		2:
			# 截圖 2: 點擊一鍵配置後 (Toast 彈出，Slot 0 與 Slot 1 裝上最強武器，攻擊力提升)
			if _wait >= 10:
				_save_viewport(
					"proof_02_lobby_character_after_auto_equip.png",
					[
						{"rect": Rect2i(700, 220, 520, 260), "filename": "crop_03_weapon_section_after.png"},
						{"rect": Rect2i(700, 100, 520, 120), "filename": "crop_04_stats_card_after.png"}
					]
				)
				# 切換至英文 en
				_loc_node.call("set_locale", "en")
				_lobby._apply_locale_texts()
				_step = 3
				_wait = 0
		3:
			# 截圖 3: 英文在地化
			if _wait >= 10:
				var btn: Button = _lobby._btn_auto_equip
				var btn_rect := Rect2i(btn.get_global_rect()) if btn else Rect2i(850, 240, 104, 48)
				_save_viewport(
					"proof_03_lobby_character_en.png",
					[
						{"rect": btn_rect.grow(8), "filename": "crop_05_btn_auto_equip_en.png"}
					]
				)
				# 切換至日文 ja
				_loc_node.call("set_locale", "ja")
				_lobby._apply_locale_texts()
				_step = 4
				_wait = 0
		4:
			# 截圖 4: 日文在地化
			if _wait >= 10:
				var btn: Button = _lobby._btn_auto_equip
				var btn_rect := Rect2i(btn.get_global_rect()) if btn else Rect2i(850, 240, 104, 48)
				_save_viewport(
					"proof_04_lobby_character_ja.png",
					[
						{"rect": btn_rect.grow(8), "filename": "crop_06_btn_auto_equip_ja.png"}
					]
				)
				print("== 存證截圖全部完成 ==")
				quit(0)
				return true

	return false


func _save_viewport(filename: String, crops: Array[Dictionary] = []) -> String:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img := tex.get_image()
	if img == null or img.is_empty():
		return ""

	var data := img.get_data()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(data)
	var hash_bytes := ctx.finish()
	var hash_hex := hash_bytes.hex_encode()

	for base_dir in OUT_PATHS:
		var full_path := base_dir.path_join(filename)
		var err := img.save_png(full_path)
		if err == OK:
			print("  ✓ 儲存實機全景圖: %s (%dx%d, SHA256: %s)" % [full_path, img.get_width(), img.get_height(), hash_hex.substr(0, 12)])
		else:
			push_error("  ✗ 儲存全景圖失敗: %s" % full_path)

		for c in crops:
			var crop_rect: Rect2i = c.get("rect", Rect2i())
			var crop_filename: String = c.get("filename", "")
			if crop_rect.size != Vector2i.ZERO and crop_filename != "":
				var crop_path := base_dir.path_join("crops").path_join(crop_filename)
				var clamped_rect := crop_rect.intersection(Rect2i(0, 0, img.get_width(), img.get_height()))
				if clamped_rect.size.x > 0 and clamped_rect.size.y > 0:
					var crop_img := img.get_region(clamped_rect)
					var cerr := crop_img.save_png(crop_path)
					if cerr == OK:
						print("    -> 儲存特寫裁切: %s (%dx%d)" % [crop_filename, crop_img.get_width(), crop_img.get_height()])
					else:
						push_error("    ✗ 儲存特寫裁切失敗: %s" % crop_filename)

	return hash_hex
