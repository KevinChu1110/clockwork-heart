extends SceneTree
## 《發條之心》ShopDialog 商城彈窗新增前往聚魂與前往鍛造快捷果凍按鈕單元與整合測試
## (test_shop_shortcuts.gd)
##
## 驗證項目：
## 1. 按鈕規格與多巴胺高飽和色盤：
##    - BtnGoInventory：薄荷綠 #4ED86A，深藍紫描邊與文字 #1F1A3A，果凍厚底 5px，圓角 18px，熱區高度 52px (>= 50px)，寬度 160px，字級 17px (>= 16px)，零系統 Emoji。
##    - BtnGoSoulHall：珊瑚粉 #FF5E8A，深藍紫描邊與文字 #1F1A3A，果凍厚底 5px，圓角 18px，熱區高度 52px (>= 50px)，寬度 160px，字級 17px (>= 16px)，零系統 Emoji。
##    - BtnGoForge：金黃 #FFD028，深藍紫描邊與文字 #1F1A3A，果凍厚底 5px，圓角 18px，熱區高度 52px (>= 50px)，寬度 160px，字級 17px (>= 16px)，零系統 Emoji。
##    - FooterBar：包含三按鈕，居中並列 (BoxContainer.ALIGNMENT_CENTER)。
## 2. 存取器定義：
##    - ShopDialog 提供 get_go_inventory_button(), get_go_soul_hall_button(), get_go_forge_button()。
## 3. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、歐美語系零 CJK 殘留、全語系零系統 Emoji。
## 4. 點擊連動：
##    - 點擊 BtnGoSoulHall 發射 go_soul_hall / soul_hall_requested 訊號，關閉商城彈窗，大廳開啟聚魂殿堂 (open_soul_hall)。
##    - 點擊 BtnGoForge 發射 go_forge / forge_requested 訊號，關閉商城彈窗，大廳開啟天宮鐵匠 (open_forge)。
## 5. 實機渲染存證：在非 headless (xvfb) 下擷取 8 張真實截圖存證至 proofs/t_29493bde/，驗證 SHA256 獨立不重複。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ShopDialogScn = preload("res://scripts/ui/shop_dialog.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": {
		"inv": "前往背包",
		"soul": "前往聚魂",
		"forge": "前往鍛造"
	},
	"zh_CN": {
		"inv": "前往背包",
		"soul": "前往聚魂",
		"forge": "前往锻造"
	},
	"en": {
		"inv": "Go to Inventory",
		"soul": "Go to Soul Hall",
		"forge": "Go to Forge"
	},
	"ja": {
		"inv": "インベントリへ進む",
		"soul": "聚魂殿へ進む",
		"forge": "鍛冶屋へ進む"
	},
	"ko": {
		"inv": "인벤토리로 이동",
		"soul": "혼령전으로 이동",
		"forge": "대장간으로 이동"
	},
	"es": {
		"inv": "Ir al Inventario",
		"soul": "Ir a Sala de Almas",
		"forge": "Ir a la Forja"
	}
}

var _lobby: Control = null
var _dlg: Control = null
var _btn_inv: Button = null
var _btn_soul: Button = null
var _btn_forge: Button = null
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
	_out_dir = base_dir.path_join("../proofs/t_29493bde")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs != null and gs.has_method("reset_new_game"):
		gs.reset_new_game()

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TEST_SHOP_SHORTCUTS_FAIL: ", msg)
	quit(1)
	return true


func _has_cjk(text: String) -> bool:
	for c in text:
		var cp := c.unicode_at(0)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	var forbidden := ["🎒", "👜", "📦", "🛒", "💎", "⚡", "✨", "🎁", "⚙", "🔮", "🔨", "🗡", "⚔", "🛡"]
	for s in forbidden:
		if text.contains(s):
			return true
	for c in text:
		var cp := c.unicode_at(0)
		if (cp >= 0x1F300 and cp <= 0x1F9FF) or (cp >= 0x2600 and cp <= 0x27BF):
			return true
	return false


func _check_button_spec(btn: Button, btn_name: String, exp_color: Color, exp_text: String) -> bool:
	if btn == null or not is_instance_valid(btn):
		return _fail("找不到按鈕: %s" % btn_name)
	if btn.name != btn_name:
		return _fail("按鈕名稱不符，期望 %s，實得: %s" % [btn_name, btn.name])
	if btn.custom_minimum_size.y < 50.0:
		return _fail("%s 高度小於 50px 觸控熱區規範，實得: %f" % [btn_name, btn.custom_minimum_size.y])
	if btn.custom_minimum_size.x < 150.0 or btn.custom_minimum_size.x > 165.0:
		return _fail("%s 寬度不符 150~160px 規範，實得: %f" % [btn_name, btn.custom_minimum_size.x])

	var font_size: int = btn.get_theme_font_size("font_size")
	if font_size < 16:
		return _fail("%s 字級小於 16px 規範，實得: %d" % [btn_name, font_size])

	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if not (sb is StyleBoxFlat):
		return _fail("%s normal 樣式應為 StyleBoxFlat" % btn_name)
	var sbf := sb as StyleBoxFlat

	if sbf.bg_color.to_html(false).to_upper() != exp_color.to_html(false).to_upper():
		return _fail("%s 背景色不符 #%s，實得: #%s" % [btn_name, exp_color.to_html(false), sbf.bg_color.to_html(false)])

	var exp_border := Color("#1F1A3A")
	if sbf.border_color.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
		return _fail("%s 描邊色不符深藍紫 #1F1A3A，實得: #%s" % [btn_name, sbf.border_color.to_html(false)])

	if sbf.border_width_bottom < 4 or sbf.border_width_bottom > 6:
		return _fail("%s 果凍厚底不符 5px，實得: %d" % [btn_name, sbf.border_width_bottom])

	if sbf.corner_radius_top_left < 16:
		return _fail("%s 圓角小於 16px，實得: %d" % [btn_name, sbf.corner_radius_top_left])

	var fc: Color = btn.get_theme_color("font_color")
	if fc.to_html(false).to_upper() != exp_border.to_html(false).to_upper():
		return _fail("%s 文字顏色不符深藍紫 #1F1A3A，實得: #%s" % [btn_name, fc.to_html(false)])

	if btn.text != exp_text:
		return _fail("%s 初始文案不符，期望 '%s'，實得: '%s'" % [btn_name, exp_text, btn.text])

	if _has_emoji(btn.text):
		return _fail("%s 殘留 Emoji: '%s'" % [btn_name, btn.text])

	print("  ok %s 規格完全合規 (尺寸: %.0fx%.0f, 色盤: #%s, 字級: %dpx, 圓角: %dpx, 厚底: %dpx, 文案: '%s', 零 Emoji)" % [
		btn_name, btn.custom_minimum_size.x, btn.custom_minimum_size.y,
		exp_color.to_html(false), font_size, sbf.corner_radius_top_left, sbf.border_width_bottom, btn.text
	])
	return true


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 3:
				return false
			print("\n--- 1. 開啟 ShopDialog 並檢驗三按鈕規格與佈局 ---")
			_dlg = _lobby.call("open_shop") as Control
			if _dlg == null or not is_instance_valid(_dlg):
				return _fail("無法開啟 ShopDialog")

			_btn_inv = _dlg.call("get_go_inventory_button") as Button
			if _btn_inv == null:
				_btn_inv = _dlg.find_child("BtnGoInventory", true, false) as Button

			_btn_soul = _dlg.call("get_go_soul_hall_button") as Button
			if _btn_soul == null:
				_btn_soul = _dlg.find_child("BtnGoSoulHall", true, false) as Button

			_btn_forge = _dlg.call("get_go_forge_button") as Button
			if _btn_forge == null:
				_btn_forge = _dlg.find_child("BtnGoForge", true, false) as Button

			# 驗證按鈕規格
			if not _check_button_spec(_btn_inv, "BtnGoInventory", Color("#4ED86A"), "前往背包"):
				return false
			if not _check_button_spec(_btn_soul, "BtnGoSoulHall", Color("#FF5E8A"), "前往聚魂"):
				return false
			if not _check_button_spec(_btn_forge, "BtnGoForge", Color("#FFD028"), "前往鍛造"):
				return false

			# 驗證 FooterBar 容器排版
			var foot: Node = _btn_inv.get_parent()
			if foot == null or foot.name != "FooterBar":
				return _fail("BtnGoInventory 應安置於 FooterBar")
			if _btn_soul.get_parent() != foot:
				return _fail("BtnGoSoulHall 應安置於 FooterBar")
			if _btn_forge.get_parent() != foot:
				return _fail("BtnGoForge 應安置於 FooterBar")

			if foot is BoxContainer and (foot as BoxContainer).alignment != BoxContainer.ALIGNMENT_CENTER:
				return _fail("FooterBar alignment 應為 ALIGNMENT_CENTER")

			print("  ok FooterBar 居中並列三按鈕排版合規")

			_step = 1
			_wait = 0

		1:
			if _wait < 5:
				return false
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_shop_three_shortcuts_zh_TW.png"))

			print("\n--- 2. 驗證六語系即時切換與零 CJK/Emoji ---")
			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "en")
			_dlg.call("_apply_locale_texts")
			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return false
			var exp_en: Dictionary = EXPECTED_TEXTS["en"]
			if _btn_inv.text != exp_en["inv"] or _btn_soul.text != exp_en["soul"] or _btn_forge.text != exp_en["forge"]:
				return _fail("語系 [en] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			if _has_cjk(_btn_inv.text) or _has_cjk(_btn_soul.text) or _has_cjk(_btn_forge.text):
				return _fail("語系 [en] 殘留 CJK")
			if _has_emoji(_btn_inv.text) or _has_emoji(_btn_soul.text) or _has_emoji(_btn_forge.text):
				return _fail("語系 [en] 殘留 Emoji")
			print("  ok 語系 [en]: inv='%s', soul='%s', forge='%s' 通過 (零 CJK, 零 Emoji)" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_shop_shortcuts_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ja")
			_dlg.call("_apply_locale_texts")
			_step = 3
			_wait = 0

		3:
			if _wait < 5:
				return false
			var exp_ja: Dictionary = EXPECTED_TEXTS["ja"]
			if _btn_inv.text != exp_ja["inv"] or _btn_soul.text != exp_ja["soul"] or _btn_forge.text != exp_ja["forge"]:
				return _fail("語系 [ja] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			if _has_emoji(_btn_inv.text) or _has_emoji(_btn_soul.text) or _has_emoji(_btn_forge.text):
				return _fail("語系 [ja] 殘留 Emoji")
			print("  ok 語系 [ja]: inv='%s', soul='%s', forge='%s' 通過 (零 Emoji)" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_shop_shortcuts_ja.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "ko")
			_dlg.call("_apply_locale_texts")
			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			var exp_ko: Dictionary = EXPECTED_TEXTS["ko"]
			if _btn_inv.text != exp_ko["inv"] or _btn_soul.text != exp_ko["soul"] or _btn_forge.text != exp_ko["forge"]:
				return _fail("語系 [ko] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			if _has_emoji(_btn_inv.text) or _has_emoji(_btn_soul.text) or _has_emoji(_btn_forge.text):
				return _fail("語系 [ko] 殘留 Emoji")
			print("  ok 語系 [ko]: inv='%s', soul='%s', forge='%s' 通過 (零 Emoji)" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_shop_shortcuts_ko.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "es")
			_dlg.call("_apply_locale_texts")
			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			var exp_es: Dictionary = EXPECTED_TEXTS["es"]
			if _btn_inv.text != exp_es["inv"] or _btn_soul.text != exp_es["soul"] or _btn_forge.text != exp_es["forge"]:
				return _fail("語系 [es] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			if _has_cjk(_btn_inv.text) or _has_cjk(_btn_soul.text) or _has_cjk(_btn_forge.text):
				return _fail("語系 [es] 殘留 CJK")
			if _has_emoji(_btn_inv.text) or _has_emoji(_btn_soul.text) or _has_emoji(_btn_forge.text):
				return _fail("語系 [es] 殘留 Emoji")
			print("  ok 語系 [es]: inv='%s', soul='%s', forge='%s' 通過 (零 CJK, 零 Emoji)" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_shop_shortcuts_es.png"))

			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_CN")
			_dlg.call("_apply_locale_texts")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			var exp_cn: Dictionary = EXPECTED_TEXTS["zh_CN"]
			if _btn_inv.text != exp_cn["inv"] or _btn_soul.text != exp_cn["soul"] or _btn_forge.text != exp_cn["forge"]:
				return _fail("語系 [zh_CN] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			if _has_emoji(_btn_inv.text) or _has_emoji(_btn_soul.text) or _has_emoji(_btn_forge.text):
				return _fail("語系 [zh_CN] 殘留 Emoji")
			print("  ok 語系 [zh_CN]: inv='%s', soul='%s', forge='%s' 通過" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_shop_shortcuts_zh_CN.png"))

			# 切回繁體中文
			var loc: Node = root.get_node_or_null("Loc")
			if loc != null:
				loc.call("set_locale", "zh_TW")
			_dlg.call("_apply_locale_texts")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			var exp_tw: Dictionary = EXPECTED_TEXTS["zh_TW"]
			if _btn_inv.text != exp_tw["inv"] or _btn_soul.text != exp_tw["soul"] or _btn_forge.text != exp_tw["forge"]:
				return _fail("語系 [zh_TW] 文案不符: inv='%s', soul='%s', forge='%s'" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])
			print("  ok 語系 [zh_TW]: inv='%s', soul='%s', forge='%s' 通過" % [_btn_inv.text, _btn_soul.text, _btn_forge.text])

			print("\n--- 3. 驗證點擊 BtnGoSoulHall 發射訊號、關閉商城並直達聚魂殿堂 ---")
			var signals_fired: Dictionary = {"go_soul_hall": false, "soul_hall_requested": false}
			_dlg.connect("go_soul_hall", func():
				signals_fired["go_soul_hall"] = true
			)
			_dlg.connect("soul_hall_requested", func():
				signals_fired["soul_hall_requested"] = true
			)

			_btn_soul.pressed.emit()

			if not signals_fired["go_soul_hall"]:
				return _fail("點擊 BtnGoSoulHall 未發射 go_soul_hall 訊號")
			if not signals_fired["soul_hall_requested"]:
				return _fail("點擊 BtnGoSoulHall 未發射 soul_hall_requested 訊號")
			print("  ok 成功接收 go_soul_hall 與 soul_hall_requested 訊號")

			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			var shop_node = _lobby.get_node_or_null("ShopDialog")
			if shop_node != null and not shop_node.is_queued_for_deletion():
				return _fail("點擊 BtnGoSoulHall 後 ShopDialog 未正常關閉")
			print("  ok ShopDialog 成功關閉")

			# 驗證聚魂殿堂開啟 (Tab.SOUL_HALL)
			var cur_tab: int = int(_lobby.get("_current_tab"))
			if cur_tab != int(MobileLobbyScn.Tab.SOUL_HALL):
				return _fail("大廳當前分頁應為 SOUL_HALL (%d)，實得: %d" % [int(MobileLobbyScn.Tab.SOUL_HALL), cur_tab])
			print("  ok 大廳即時切換至聚魂殿堂 (Tab.SOUL_HALL)，動線閉環！")

			_proof_hashes["proof_07"] = _capture_save(_out_dir.path_join("proof_07_click_go_soul_hall_opens_soul_hall.png"))

			print("\n--- 4. 驗證點擊 BtnGoForge 發射訊號、關閉商城並直達天宮鐵匠 ---")
			# 重新開啟商城彈窗
			_dlg = _lobby.call("open_shop") as Control
			if _dlg == null or not is_instance_valid(_dlg):
				return _fail("無法重新開啟 ShopDialog 進行鍛造連動測試")

			_btn_forge = _dlg.call("get_go_forge_button") as Button
			if _btn_forge == null:
				_btn_forge = _dlg.find_child("BtnGoForge", true, false) as Button

			var forge_signals_fired: Dictionary = {"go_forge": false, "forge_requested": false}
			_dlg.connect("go_forge", func():
				forge_signals_fired["go_forge"] = true
			)
			_dlg.connect("forge_requested", func():
				forge_signals_fired["forge_requested"] = true
			)

			_btn_forge.pressed.emit()

			if not forge_signals_fired["go_forge"]:
				return _fail("點擊 BtnGoForge 未發射 go_forge 訊號")
			if not forge_signals_fired["forge_requested"]:
				return _fail("點擊 BtnGoForge 未發射 forge_requested 訊號")
			print("  ok 成功接收 go_forge 與 forge_requested 訊號")

			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			var shop_node2 = _lobby.get_node_or_null("ShopDialog")
			if shop_node2 != null and not shop_node2.is_queued_for_deletion():
				return _fail("點擊 BtnGoForge 後 ShopDialog 未正常關閉")
			print("  ok ShopDialog 成功關閉")

			# 驗證天宮鐵匠彈窗開啟 (ForgeDialog)
			var forge_dlg: Control = _lobby.get_node_or_null("ForgeDialog") as Control
			if forge_dlg == null or not is_instance_valid(forge_dlg):
				return _fail("點擊前往鍛造後大廳未開啟 ForgeDialog (天宮鐵匠)")
			if not forge_dlg.visible:
				return _fail("ForgeDialog 應為可見 (visible=true)")
			print("  ok 大廳即時開啟天宮鐵匠 (ForgeDialog)，強化鍛造動線閉環！")

			_proof_hashes["proof_08"] = _capture_save(_out_dir.path_join("proof_08_click_go_forge_opens_forge_dialog.png"))

			_step = 10
			_wait = 0

		10:
			if _wait < 3:
				return false
			print("\n--- 5. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var keys := [
					"proof_01", "proof_02", "proof_03", "proof_04",
					"proof_05", "proof_06", "proof_07", "proof_08"
				]
				var seen_hashes: Dictionary = {}
				for k in keys:
					var h: String = _proof_hashes.get(k, "")
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 8 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 ShopDialog 前往聚魂與前往鍛造快捷按鈕測試全數通過！")
			print("TEST_SHOP_SHORTCUTS_OK")
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
	return sha
