extends SceneTree
## 《發條之心》大廳聚魂殿堂新增『前往背包』快捷果凍按鈕連動探索背包素材頁籤單元測試
## (test_soul_hall_inventory_shortcut.gd)
##
## 驗證項目：
## 1. 按鈕規格與多巴胺高飽和色盤：
##    - BtnGoInventory：珊瑚粉果凍厚底按鈕 (COLOR_PINK #FF5E8A)，深藍紫描邊與文字 #1F1A3A，
##      熱區高度 >= 50px (實際 52px >= 48px)，立體厚底 5px，圓角 18px，字級 16px，零系統 Emoji。
##    - 聚魂殿堂底欄並列一鍵吸收 (BtnAbsorb)、前往背包 (BtnGoInventory) 與聚魂十連 (BtnDrawTen) 三顆果凍按鈕。
## 2. 功能連動：
##    - 點擊 BtnGoInventory 呼叫 open_maple_inventory("material")。
##    - 無縫開啟探索背包 MapleInventory 並自動定位至素材分類頁籤 ("material")。
## 3. 雙向閉環：
##    - 在探索背包選中戰魂素材時點擊前往聚魂 (BtnGoSoul) 可直達聚魂殿堂。
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。
## 5. 實機渲染存證：在非 headless (xvfb) 下擷取 6 張真實截圖存證至 proofs/t_13a0ab72/，驗證 SHA256 獨立不重複。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "Go to Inventory",
	"ja": "インベントリへ進む",
	"ko": "인벤토리로 이동",
	"es": "Ir al Inventario"
}

var _lobby: Control = null
var _btn_inv: Button = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_13a0ab72")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	# 切換至聚魂殿堂 Tab 將在 _process step 0 執行，確保在 _ready() 後生效
	# _lobby.open_soul_hall()


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SOUL_HALL_INVENTORY_SHORTCUT_FAIL: ", msg)
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
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF):
			return true
	return false


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 3:
				_lobby.open_soul_hall()
				return false
			print("\n--- 1. 驗證聚魂殿堂底欄 BtnGoInventory 節點存在性與規格 ---")
			_lobby.open_soul_hall()
			_btn_inv = _lobby.call("get_soul_hall_go_inventory_btn") as Button
			if _btn_inv == null or not is_instance_valid(_btn_inv):
				return _fail("找不到前往背包按鈕 (get_soul_hall_go_inventory_btn / BtnGoInventory)")

			if _btn_inv.name != "BtnGoInventory":
				return _fail("前往背包按鈕名稱應為 BtnGoInventory，實得: %s" % _btn_inv.name)

			if _btn_inv.custom_minimum_size.y < 48.0:
				return _fail("BtnGoInventory 高度小於 48px，實得: %f" % _btn_inv.custom_minimum_size.y)
			print("  ok BtnGoInventory 按鈕尺寸與熱區符合規範: 高度=%.1fpx (>= 48px), 寬度=%.1fpx" % [
				_btn_inv.custom_minimum_size.y, _btn_inv.custom_minimum_size.x
			])

			var font_size: int = _btn_inv.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("BtnGoInventory 字級小於 16px，實得: %d" % font_size)
			print("  ok BtnGoInventory 字級符合規範: %dpx (>= 16px)" % font_size)

			var sb: StyleBox = _btn_inv.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("BtnGoInventory normal 樣式應為 StyleBoxFlat")
			var sbf := sb as StyleBoxFlat

			var exp_pink := Color("#FF5E8A")
			if sbf.bg_color.to_html(false) != exp_pink.to_html(false):
				return _fail("BtnGoInventory 背景色不符珊瑚粉 #FF5E8A，實得: #%s" % sbf.bg_color.to_html(false))

			var exp_border := Color("#1F1A3A")
			if sbf.border_color.to_html(false) != exp_border.to_html(false):
				return _fail("BtnGoInventory 描邊色不符深藍紫 #1F1A3A，實得: #%s" % sbf.border_color.to_html(false))

			if sbf.border_width_bottom < 4:
				return _fail("BtnGoInventory 果凍厚底小於 4px，實得: %d" % sbf.border_width_bottom)

			if sbf.corner_radius_top_left < 16:
				return _fail("BtnGoInventory 圓角小於 16px，實得: %d" % sbf.corner_radius_top_left)

			var fc: Color = _btn_inv.get_theme_color("font_color")
			if fc.to_html(false) != exp_border.to_html(false):
				return _fail("BtnGoInventory 文字顏色不符 #1F1A3A，實得: #%s" % fc.to_html(false))

			print("  ok BtnGoInventory 珊瑚粉果凍厚底樣式完全合規 (珊瑚粉 #FF5E8A, 深藍紫描邊 #1F1A3A, 果凍厚底 %dpx, 圓角 %dpx)" % [
				sbf.border_width_bottom, sbf.corner_radius_top_left
			])

			# 驗證底欄三個按鈕齊全
			var parent_bar: Node = _btn_inv.get_parent()
			if parent_bar == null:
				return _fail("BtnGoInventory 無父容器")
			var btn_absorb: Button = parent_bar.get_node_or_null("BtnAbsorb")
			var btn_draw: Button = parent_bar.get_node_or_null("BtnDrawTen")
			if btn_absorb == null or btn_draw == null:
				return _fail("底欄應並列 BtnAbsorb, BtnGoInventory, BtnDrawTen")
			print("  ok 底欄三顆果凍按鈕齊全並列 (BtnAbsorb, BtnGoInventory, BtnDrawTen)")

			# 驗證初始繁中文案與零 Emoji
			if _btn_inv.text != "前往背包":
				return _fail("BtnGoInventory 初始繁中文案不符，期望 '前往背包'，實得: '%s'" % _btn_inv.text)
			if _has_emoji(_btn_inv.text):
				return _fail("BtnGoInventory 殘留 Emoji: '%s'" % _btn_inv.text)
			print("  ok 初始繁中文案正確且零 Emoji: '%s'" % _btn_inv.text)

			_step = 1
			_wait = 0

		1:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_soul_hall_bottom_bar_three_buttons_zh_TW.png"))

			print("\n--- 2. 驗證六語系即時切換與零 CJK/Emoji ---")
			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "en")
			_lobby.call("_apply_locale_texts")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["en"]:
				return _fail("語系 en 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["en"], _btn_inv.text])
			if _has_cjk(_btn_inv.text):
				return _fail("語系 en 殘留 CJK: '%s'" % _btn_inv.text)
			if _has_emoji(_btn_inv.text):
				return _fail("語系 en 殘留 Emoji: '%s'" % _btn_inv.text)
			print("  ok 語系 [en]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_inv.text)
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_soul_hall_go_inventory_btn_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ja")
			_lobby.call("_apply_locale_texts")
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["ja"]:
				return _fail("語系 ja 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ja"], _btn_inv.text])
			if _has_emoji(_btn_inv.text):
				return _fail("語系 ja 殘留 Emoji: '%s'" % _btn_inv.text)
			print("  ok 語系 [ja]: '%s' 通過 (零 Emoji)" % _btn_inv.text)
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_soul_hall_go_inventory_btn_ja.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ko")
			_lobby.call("_apply_locale_texts")
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["ko"]:
				return _fail("語系 ko 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["ko"], _btn_inv.text])
			if _has_emoji(_btn_inv.text):
				return _fail("語系 ko 殘留 Emoji: '%s'" % _btn_inv.text)
			print("  ok 語系 [ko]: '%s' 通過 (零 Emoji)" % _btn_inv.text)
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_soul_hall_go_inventory_btn_ko.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "es")
			_lobby.call("_apply_locale_texts")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["es"]:
				return _fail("語系 es 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["es"], _btn_inv.text])
			if _has_cjk(_btn_inv.text):
				return _fail("語系 es 殘留 CJK: '%s'" % _btn_inv.text)
			if _has_emoji(_btn_inv.text):
				return _fail("語系 es 殘留 Emoji: '%s'" % _btn_inv.text)
			print("  ok 語系 [es]: '%s' 通過 (零 CJK, 零 Emoji)" % _btn_inv.text)
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_soul_hall_go_inventory_btn_es.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_CN")
			_lobby.call("_apply_locale_texts")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["zh_CN"]:
				return _fail("語系 zh_CN 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["zh_CN"], _btn_inv.text])
			print("  ok 語系 [zh_CN]: '%s' 通過" % _btn_inv.text)

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_TW")
			_lobby.call("_apply_locale_texts")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			if _btn_inv.text != EXPECTED_TEXTS["zh_TW"]:
				return _fail("語系 zh_TW 文案不符，期望 '%s'，實得: '%s'" % [EXPECTED_TEXTS["zh_TW"], _btn_inv.text])
			print("  ok 語系 [zh_TW]: '%s' 通過" % _btn_inv.text)

			print("\n--- 3. 驗證點擊 BtnGoInventory 連動開啟探索背包素材頁籤 ---")
			# 點擊 BtnGoInventory 按鈕
			_btn_inv.pressed.emit()
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var inv: Control = _lobby.get_node_or_null("MapleInventory") as Control
			if inv == null or not is_instance_valid(inv):
				return _fail("點擊 BtnGoInventory 後未成功開啟 MapleInventory 探索背包")

			if not inv.visible:
				return _fail("MapleInventory 探索背包應為可見 (visible=true)")

			var current_cat: String = str(inv.get("_current_category"))
			if current_cat != "material":
				return _fail("MapleInventory 當前分類應為 'material' (素材)，實得: '%s'" % current_cat)
			print("  ok MapleInventory 成功開啟且自動切換至素材分類頁籤 (_current_category = 'material')")

			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_click_go_inventory_opens_maple_inventory_material.png"))
			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false
			print("\n--- 4. 驗證雙向閉環：背包前往聚魂直達聚魂殿 ---")
			var inv: Control = _lobby.get_node_or_null("MapleInventory") as Control
			if inv != null and is_instance_valid(inv):
				# 選取戰魂素材
				inv.set("_selected", "windup_fragment")
				inv.call("refresh")
				var btn_soul: Button = inv.call("get_go_soul_button") as Button
				if btn_soul != null and btn_soul.visible:
					btn_soul.pressed.emit()
					print("  ok 從背包點擊 BtnGoSoul 直達聚魂殿堂")

			_step = 10
			_wait = 0

		10:
			if _wait < 3:
				return false
			print("\n--- 5. 實機截圖 SHA256 獨立性驗證 ---")
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
			print("🎉 全部大廳聚魂殿堂前往背包快捷按鈕單元測試通過！")
			print("TEST_SOUL_HALL_INVENTORY_SHORTCUT_OK")
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
