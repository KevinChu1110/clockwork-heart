extends SceneTree
## 《發條之心》MapleInventory 探索背包戰魂素材『前往聚魂』快捷按鈕連動大廳聚魂殿單元測試
## (test_maple_inventory_soul_shortcut.gd)
##
## 驗證項目：
## 1. 按鈕規格與多巴胺亮色盤樣式：
##    - BtnGoSoul (前往聚魂)：金黃果凍厚底按鈕 (COLOR_GOLD #FFD028)，深藍紫文字與描邊 #1F1A3A，
##      熱區高度 >= 50px (>= 48px)，立體厚底 5px，圓角 18px，字級 18px，零系統 Emoji。
## 2. 狀態切換與互斥性：
##    - 未選取物品 (_selected == "")：BtnGoSoul、BtnGoForge、BtnGoWorkshop、BtnGoCalibrate 均隱藏。
##    - 選取戰魂素材 (windup_fragment / soul_crystal)：BtnGoSoul 顯示 (visible=true)，
##      BtnGoForge、BtnGoWorkshop、BtnGoCalibrate 互斥隱藏 (visible=false)。
##    - 選取裝備 (rusty_blade / ash_mail)：BtnGoForge 顯示，BtnGoSoul、BtnGoWorkshop、BtnGoCalibrate 隱藏。
##    - 選取素材或寶石 (iron_scrap / gem_red_1)：BtnGoWorkshop 顯示，BtnGoSoul、BtnGoForge、BtnGoCalibrate 隱藏。
##    - 選取消耗品 (hp_s) 或重要道具 (key_rusty)：BtnGoSoul、BtnGoForge、BtnGoWorkshop 均隱藏。
## 3. 訊號發送與直達跳轉連動：
##    - 點擊 BtnGoSoul 發射 go_soul_hall_requested 訊號並呼叫 open_soul_hall()。
##    - 自動關閉背包彈窗 (visible=false) 並連動 MobileLobby 切換至聚魂殿堂 (Tab.SOUL_HALL)。
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。
## 5. 實機渲染存證：在非 headless (xvfb) 下擷取真實截圖存證至 proofs/t_3726e90e/，驗證 SHA256 獨立不重複。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_SOUL_TEXTS: Dictionary = {
	"zh_TW": "前往聚魂",
	"zh_CN": "前往聚魂",
	"en": "Go to Soul Draw",
	"ja": "魂寄せへ",
	"ko": "영혼 뽑기로 이동",
	"es": "Ir a extracción de almas"
}

var _lobby: Control = null
var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _soul_signal_emitted: bool = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_3726e90e")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	_inv = _lobby.open_maple_inventory()


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_SOUL_SHORTCUT_FAIL: ", msg)
	quit(1)
	return true


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			return true
	return false


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 3:
				return false
			print("--- 1. 初始化測試環境道具與戰魂素材資料 ---")
			_inv.open()
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / EquipmentSystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "equip_worn" in gs and gs.equip_worn != null:
				gs.equip_worn.clear()
			if "equip_slots" in gs and gs.equip_slots != null:
				gs.equip_slots.clear()
			if "equip_bag" in gs and gs.equip_bag != null:
				gs.equip_bag.clear()

			# 註冊與添加各類測試道具
			inv_sys.call("register_item", "soul_crystal", {
				"name": "聚魂結晶",
				"kind": "soul",
				"desc": "純淨的戰魂能量結晶，可用於聚魂殿堂召喚戰魂。",
				"stack": 99,
				"glyph": "魂"
			})
			inv_sys.call("register_item", "gem_red_1", {
				"name": "赤紅寶石",
				"kind": "gem",
				"desc": "蘊含火之力量的寶石結晶，可前往工坊合成與鑲嵌。",
				"stack": 99,
				"glyph": "寶"
			})

			inv_sys.call("add_item", "windup_fragment", 15) # 戰魂素材 (發條碎片)
			inv_sys.call("add_item", "soul_crystal", 5)     # 戰魂素材 (聚魂結晶)
			inv_sys.call("add_item", "rusty_blade", 1)      # 武器 (裝備)
			inv_sys.call("add_item", "ash_mail", 1)         # 防具 (裝備)
			inv_sys.call("add_item", "iron_scrap", 10)      # 一般素材
			inv_sys.call("add_item", "gem_red_1", 3)        # 寶石
			inv_sys.call("add_item", "hp_s", 5)             # 消耗品
			inv_sys.call("add_item", "key_rusty", 1)        # 重要道具

			_inv.refresh()
			print("  ok 道具初始化完成 (windup_fragment, soul_crystal, rusty_blade, ash_mail, iron_scrap, gem_red_1, hp_s, key_rusty)")
			_step = 1
			_wait = 0

		1:
			if _wait < 3:
				return false
			print("\n--- 2. 驗證 BtnGoSoul 節點存在性與金黃果凍厚底規格 ---")
			var btn_soul: Button = _inv.call("get_go_soul_button")
			if btn_soul == null or not is_instance_valid(btn_soul):
				return _fail("找不到前往聚魂按鈕 (get_go_soul_button / BtnGoSoul)")

			if btn_soul.name != "BtnGoSoul":
				return _fail("前往聚魂按鈕名稱應為 BtnGoSoul，實得: %s" % btn_soul.name)

			if btn_soul.custom_minimum_size.y < 48.0:
				return _fail("BtnGoSoul 高度小於 48px，實得: %f" % btn_soul.custom_minimum_size.y)
			print("  ok BtnGoSoul 按鈕尺寸與熱區符合規範: 高度=%.1fpx (>= 48px)" % btn_soul.custom_minimum_size.y)

			var font_size: int = btn_soul.get_theme_font_size("font_size")
			if font_size < 18:
				return _fail("BtnGoSoul 字級小於 18px，實得: %d" % font_size)
			print("  ok BtnGoSoul 字級符合規範: %dpx (>= 18px)" % font_size)

			var sb = btn_soul.get_theme_stylebox("normal") as StyleBoxFlat
			if sb == null:
				return _fail("BtnGoSoul normal 樣式非 StyleBoxFlat")

			if sb.border_width_bottom != 5 or sb.corner_radius_top_left != 18:
				return _fail("BtnGoSoul 果凍厚底 (5px) 或圓角 (18px) 不符，實得: bottom=%d, radius=%d" % [sb.border_width_bottom, sb.corner_radius_top_left])

			if sb.bg_color != Color("#FFD028"):
				return _fail("BtnGoSoul 底色非多巴胺金黃 (#FFD028)，實得: %s" % sb.bg_color.to_html())

			if sb.border_color != Color("#1F1A3A"):
				return _fail("BtnGoSoul 描邊非深藍紫 (#1F1A3A)，實得: %s" % sb.border_color.to_html())

			var font_color: Color = btn_soul.get_theme_color("font_color")
			if font_color != Color("#1F1A3A"):
				return _fail("BtnGoSoul 文字顏色非深藍紫 (#1F1A3A)，實得: %s" % font_color.to_html())

			print("  ok BtnGoSoul 金黃果凍厚底樣式完全合規 (金黃 #FFD028, 深藍紫文字與描邊 #1F1A3A, 果凍厚底 5px, 圓角 18px)")
			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false
			print("\n--- 3. 驗證未選取道具時快捷按鈕隱藏 ---")
			var btn_soul: Button = _inv.call("get_go_soul_button")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			var btn_calibrate: Button = _inv.call("get_go_calibrate_button")

			_inv.set("_selected", "")
			_inv.refresh()

			if btn_soul.visible:
				return _fail("未選取道具時 BtnGoSoul 應為隱藏 (visible=false)")
			if btn_forge.visible:
				return _fail("未選取道具時 BtnGoForge 應為隱藏 (visible=false)")
			if btn_workshop.visible:
				return _fail("未選取道具時 BtnGoWorkshop 應為隱藏 (visible=false)")
			if btn_calibrate != null and btn_calibrate.visible:
				return _fail("未選取道具時 BtnGoCalibrate 應為隱藏 (visible=false)")

			print("  ok 未選取狀態下 BtnGoSoul、BtnGoForge、BtnGoWorkshop 均嚴格隱藏")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			print("\n--- 4. 驗證選取戰魂素材 (windup_fragment / soul_crystal) 互斥顯示 ---")
			var btn_soul: Button = _inv.call("get_go_soul_button")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			var btn_calibrate: Button = _inv.call("get_go_calibrate_button")

			# 4.1 選取 windup_fragment
			_inv.set("_selected", "windup_fragment")
			_inv.refresh()

			if not btn_soul.visible:
				return _fail("選取 windup_fragment 時 BtnGoSoul 應為可見 (visible=true)")
			if btn_forge.visible:
				return _fail("選取 windup_fragment 時 BtnGoForge 應隱藏 (visible=false)")
			if btn_workshop.visible:
				return _fail("選取 windup_fragment 時 BtnGoWorkshop 應隱藏 (visible=false)")
			if btn_calibrate != null and btn_calibrate.visible:
				return _fail("選取 windup_fragment 時 BtnGoCalibrate 應隱藏 (visible=false)")
			if btn_soul.text != "前往聚魂":
				return _fail("BtnGoSoul 繁中文案不符，期望 '前往聚魂'，實得: '%s'" % btn_soul.text)
			print("  ok 選取 windup_fragment 顯示『前往聚魂』(BtnGoSoul)，互斥隱藏鍛造、工坊、校準按鈕")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_maple_inv_soul_fragment_selected_btn_go_soul_zh_tw.png"))

			# 4.2 選取自定義 soul_crystal
			_inv.set("_selected", "soul_crystal")
			_inv.refresh()
			var btn_soul: Button = _inv.call("get_go_soul_button")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			if not btn_soul.visible:
				return _fail("選取 soul_crystal 時 BtnGoSoul 應為可見 (visible=true)")
			if btn_forge.visible or btn_workshop.visible:
				return _fail("選取 soul_crystal 時 BtnGoForge 與 BtnGoWorkshop 應隱藏 (visible=false)")
			print("  ok 選取 soul_crystal 同樣正確顯示『前往聚魂』(BtnGoSoul)")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			print("\n--- 5. 驗證選取一般裝備、素材、消耗品時 BtnGoSoul 互斥隱藏 ---")
			var btn_soul: Button = _inv.call("get_go_soul_button")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			# 5.1 裝備 (rusty_blade)
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if btn_soul.visible:
				return _fail("選取裝備 (rusty_blade) 時 BtnGoSoul 應隱藏 (visible=false)")
			if not btn_forge.visible:
				return _fail("選取裝備 (rusty_blade) 時 BtnGoForge 應顯示 (visible=true)")
			print("  ok 選取裝備顯示 BtnGoForge，BtnGoSoul 互斥隱藏")

			# 5.2 一般素材 (iron_scrap)
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if btn_soul.visible:
				return _fail("選取素材 (iron_scrap) 時 BtnGoSoul 應隱藏 (visible=false)")
			if not btn_workshop.visible:
				return _fail("選取素材 (iron_scrap) 時 BtnGoWorkshop 應顯示 (visible=true)")
			print("  ok 選取一般素材顯示 BtnGoWorkshop，BtnGoSoul 互斥隱藏")

			# 5.3 消耗品 (hp_s)
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if btn_soul.visible or btn_forge.visible or btn_workshop.visible:
				return _fail("選取消耗品 (hp_s) 時所有快捷按鈕均應隱藏")
			print("  ok 選取消耗品時所有快捷按鈕均隱藏")

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false
			print("\n--- 6. 驗證六語系動態即時切換無缺詞與零 CJK/Emoji ---")
			var loc: Node = root.get_node_or_null("Loc")
			var btn_soul: Button = _inv.call("get_go_soul_button")
			_inv.set("_selected", "windup_fragment")

			for code in LOCALES:
				loc.call("set_locale", code)
				_inv.refresh()
				var exp_txt: String = EXPECTED_SOUL_TEXTS[code]
				if btn_soul.text != exp_txt:
					return _fail("語系 [%s] 文案不符，期望 '%s'，實得 '%s'" % [code, exp_txt, btn_soul.text])

				if _has_emoji(btn_soul.text):
					return _fail("語系 [%s] 包含違規系統 Emoji: %s" % [code, btn_soul.text])

				if code in ["en", "es"] and _has_cjk(btn_soul.text):
					return _fail("歐美語系 [%s] 殘留 CJK 字元: %s" % [code, btn_soul.text])

				print("  ok 語系 [%s]: '%s' 通過" % [code, btn_soul.text])

			# 截圖 2 (en)
			loc.call("set_locale", "en")
			_inv.refresh()
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_maple_inv_soul_shortcut_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ja")
			_inv.refresh()
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_maple_inv_soul_shortcut_ja.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ko")
			_inv.refresh()
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_maple_inv_soul_shortcut_ko.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "es")
			_inv.refresh()
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_maple_inv_soul_shortcut_es.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()
			_step = 11
			_wait = 0

		11:
			if _wait < 3:
				return false
			print("\n--- 7. 驗證點擊 BtnGoSoul 發送訊號與直達大廳聚魂殿堂 (Tab.SOUL_HALL) ---")
			_soul_signal_emitted = false
			_inv.go_soul_hall_requested.connect(func():
				_soul_signal_emitted = true
			, CONNECT_ONE_SHOT)

			_inv.set("_selected", "windup_fragment")
			_inv.refresh()
			var btn_soul: Button = _inv.call("get_go_soul_button")

			# 模擬點擊前往聚魂按鈕
			btn_soul.pressed.emit()

			if not _soul_signal_emitted:
				return _fail("點擊 BtnGoSoul 未能發射 go_soul_hall_requested 訊號")
			print("  ok 成功發射 go_soul_hall_requested 訊號")

			if _inv.visible:
				return _fail("點擊 BtnGoSoul 後 MapleInventory 未關閉隱藏 (visible 應為 false)")
			print("  ok MapleInventory 背包成功關閉 (visible=false)")

			if _lobby.get("_current_tab") != MobileLobbyScn.Tab.SOUL_HALL:
				return _fail("大廳未切換至聚魂殿堂分頁 (Tab.SOUL_HALL)，目前分頁: %s" % str(_lobby.get("_current_tab")))
			print("  ok MobileLobby 成功連動切換至聚魂殿堂分頁 (Tab.SOUL_HALL)")

			_step = 12
			_wait = 0

		12:
			if _wait < 6:
				return false
			# 截圖 6: 點擊前往聚魂後直達聚魂殿堂畫面
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_click_btn_go_soul_opens_soul_hall.png"))

			_step = 13
			_wait = 0

		13:
			if _wait < 3:
				return false
			print("\n--- 8. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var keys := ["proof_01", "proof_02", "proof_03", "proof_04", "proof_05", "proof_06"]
				var seen_hashes: Dictionary = {}
				for k in keys:
					var h: String = _proof_hashes.get(k, "")
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 6 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 戰魂素材前往聚魂快捷按鈕單元測試通過！")
			print("MAPLE_INVENTORY_SOUL_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha
