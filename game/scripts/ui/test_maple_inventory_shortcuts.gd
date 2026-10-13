extends SceneTree
## 《發條之心》MapleInventory 探索背包前往鍛造與前往工坊快捷跳轉單元測試 (test_maple_inventory_shortcuts.gd)
##
## 驗證項目：
## 1. 按鈕規格與多巴胺亮色盤樣式：
##    - BtnGoForge (前往鍛造)：暖橘果凍厚底按鈕 (COLOR_ORANGE #FFA010)，熱區高度 >= 50px，立體厚底 5px，圓角 18px，字級 18px (>= 18px)，零系統 Emoji。
##    - BtnGoWorkshop (前往工坊)：薄荷綠果凍厚底按鈕 (COLOR_MINT #4ED86A)，熱區高度 >= 50px，立體厚底 5px，圓角 18px，字級 18px (>= 18px)，零系統 Emoji。
## 2. 狀態切換覆蓋：
##    - 未選取物品 (_selected == "")：BtnGoForge 與 BtnGoWorkshop 均隱藏 (visible=false)。
##    - 選取裝備 (rusty_blade / ash_mail)：BtnGoForge 顯示 (visible=true)，BtnGoWorkshop 隱藏 (visible=false)。
##    - 選取素材或寶石 (iron_scrap / gem_red_1)：BtnGoWorkshop 顯示 (visible=true)，BtnGoForge 隱藏 (visible=false)。
##    - 選取消耗品 (hp_s) 或重要道具 (key_rusty)：BtnGoForge 與 BtnGoWorkshop 均隱藏 (visible=false)。
## 3. 訊號發送與跳轉連動：
##    - 點擊 BtnGoForge 發射 forge_requested 訊號並支援 open_forge() 直通開啟 ForgeDialog (天宮鐵匠)。
##    - 點擊 BtnGoWorkshop 發射 workshop_requested 訊號並支援 open_gem_workshop() 直通開啟 GemWorkshopDialog (手藝工坊)。
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji。
## 5. 實機渲染存證：在非 headless (xvfb) 下擷取真實截圖存證至 proofs/t_31190d69/，驗證 SHA256 獨立不重複。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_FORGE_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}
const EXPECTED_WORKSHOP_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "Go to Workshop",
	"ja": "工房へ進む",
	"ko": "공방으로 이동",
	"es": "Ir al Taller"
}

var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _forge_signal_emitted: bool = false
var _workshop_signal_emitted: bool = false
var _created_dialog: Control = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_31190d69")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_SHORTCUTS_FAIL: ", msg)
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
			_inv.open()
			_step = 1
			_wait = 0

		1:
			if _wait < 3:
				return false

			print("--- 1. 初始化測試環境道具與裝備資料 ---")
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
			inv_sys.call("register_item", "gem_red_1", {
				"name": "赤紅寶石",
				"kind": "gem",
				"desc": "蘊含火之力量的寶石結晶，可前往工坊合成與鑲嵌。",
				"stack": 99,
				"glyph": "寶"
			})

			inv_sys.call("add_item", "rusty_blade", 1)   # 武器 (裝備)
			inv_sys.call("add_item", "ash_mail", 1)      # 防具 (裝備)
			inv_sys.call("add_item", "iron_scrap", 10)   # 素材
			inv_sys.call("add_item", "gem_red_1", 3)     # 寶石
			inv_sys.call("add_item", "hp_s", 5)          # 消耗品
			inv_sys.call("add_item", "key_rusty", 1)     # 重要道具

			_inv.refresh()
			print("  ok 道具初始化完成 (rusty_blade, ash_mail, iron_scrap, gem_red_1, hp_s, key_rusty)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證快捷按鈕節點存在性與多巴胺果凍樣式規格 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			if btn_forge == null or not is_instance_valid(btn_forge):
				return _fail("找不到前往鍛造按鈕 (get_go_forge_button / BtnGoForge)")
			if btn_workshop == null or not is_instance_valid(btn_workshop):
				return _fail("找不到前往工坊按鈕 (get_go_workshop_button / BtnGoWorkshop)")

			# 驗證名稱
			if btn_forge.name != "BtnGoForge":
				return _fail("前往鍛造按鈕名稱應為 BtnGoForge，實得: %s" % btn_forge.name)
			if btn_workshop.name != "BtnGoWorkshop":
				return _fail("前往工坊按鈕名稱應為 BtnGoWorkshop，實得: %s" % btn_workshop.name)

			# 驗證高度 >= 50px (熱區 >= 48px)
			if btn_forge.custom_minimum_size.y < 50.0:
				return _fail("BtnGoForge 高度小於 50px，實得: %f" % btn_forge.custom_minimum_size.y)
			if btn_workshop.custom_minimum_size.y < 50.0:
				return _fail("BtnGoWorkshop 高度小於 50px，實得: %f" % btn_workshop.custom_minimum_size.y)
			print("  ok 按鈕尺寸與熱區符合規範: BtnGoForge=%.1fpx, BtnGoWorkshop=%.1fpx (>= 50px)" % [btn_forge.custom_minimum_size.y, btn_workshop.custom_minimum_size.y])

			# 驗證字級 >= 18px
			var font_size_f: int = btn_forge.get_theme_font_size("font_size")
			var font_size_w: int = btn_workshop.get_theme_font_size("font_size")
			if font_size_f < 18:
				return _fail("BtnGoForge 字級小於 18px，實得: %d" % font_size_f)
			if font_size_w < 18:
				return _fail("BtnGoWorkshop 字級小於 18px，實得: %d" % font_size_w)
			print("  ok 按鈕字級符合規範: BtnGoForge=%dpx, BtnGoWorkshop=%dpx (>= 18px)" % [font_size_f, font_size_w])

			# 驗證樣式 (StyleBoxFlat: 果凍厚底 5px, 圓角 18px)
			var sb_f = btn_forge.get_theme_stylebox("normal") as StyleBoxFlat
			var sb_w = btn_workshop.get_theme_stylebox("normal") as StyleBoxFlat
			if sb_f == null or sb_w == null:
				return _fail("快捷按鈕 normal 樣式非 StyleBoxFlat")

			if sb_f.border_width_bottom != 5 or sb_f.corner_radius_top_left != 18:
				return _fail("BtnGoForge 果凍厚底 (5px) 或圓角 (18px) 不符，實得: bottom=%d, radius=%d" % [sb_f.border_width_bottom, sb_f.corner_radius_top_left])
			if sb_w.border_width_bottom != 5 or sb_w.corner_radius_top_left != 18:
				return _fail("BtnGoWorkshop 果凍厚底 (5px) 或圓角 (18px) 不符，實得: bottom=%d, radius=%d" % [sb_w.border_width_bottom, sb_w.corner_radius_top_left])

			# 驗證配色：BtnGoForge 為暖橘 (COLOR_ORANGE #FFA010)，BtnGoWorkshop 為薄荷綠 (COLOR_MINT #4ED86A)
			if sb_f.bg_color != Color("#FFA010"):
				return _fail("BtnGoForge 底色非多巴胺暖橘 (#FFA010)，實得: %s" % sb_f.bg_color.to_html())
			if sb_w.bg_color != Color("#4ED86A"):
				return _fail("BtnGoWorkshop 底色非多巴胺薄荷綠 (#4ED86A)，實得: %s" % sb_w.bg_color.to_html())
			print("  ok 按鈕多巴胺亮色盤樣式完全合規 (暖橘 #FFA010 / 薄荷綠 #4ED86A, 果凍厚底 5px, 圓角 18px)")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 驗證未選取道具時快捷按鈕隱藏 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			_inv.set("_selected", "")
			_inv.refresh()

			if btn_forge.visible:
				return _fail("未選取道具時 BtnGoForge 應為隱藏 (visible=false)")
			if btn_workshop.visible:
				return _fail("未選取道具時 BtnGoWorkshop 應為隱藏 (visible=false)")
			print("  ok 未選取狀態下 BtnGoForge 與 BtnGoWorkshop 嚴格隱藏")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證選取裝備類物品 (rusty_blade / ash_mail) 時切換 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			# 4.1 武器 (rusty_blade)
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if not btn_forge.visible:
				return _fail("選取武器 (rusty_blade) 時 BtnGoForge 應為可見 (visible=true)")
			if btn_workshop.visible:
				return _fail("選取武器 (rusty_blade) 時 BtnGoWorkshop 應隱藏 (visible=false)")
			if btn_forge.text != "前往鍛造":
				return _fail("BtnGoForge 繁中文案不符，期望 '前往鍛造'，實得: '%s'" % btn_forge.text)
			print("  ok 選取武器 (rusty_blade) 顯示『前往鍛造』(BtnGoForge)，隱藏『前往工坊』")

			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return false
			# 截圖 1: 選取裝備顯示前往鍛造
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_maple_inv_weapon_selected_forge_btn.png"))

			# 4.2 防具 (ash_mail)
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			if not btn_forge.visible:
				return _fail("選取防具 (ash_mail) 時 BtnGoForge 應為可見 (visible=true)")
			if btn_workshop.visible:
				return _fail("選取防具 (ash_mail) 時 BtnGoWorkshop 應隱藏 (visible=false)")
			print("  ok 選取防具 (ash_mail) 同樣顯示『前往鍛造』(BtnGoForge)")

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			print("\n--- 5. 驗證選取素材與寶石 (iron_scrap / gem_red_1) 時切換 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			# 5.1 素材 (iron_scrap)
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if btn_forge.visible:
				return _fail("選取素材 (iron_scrap) 時 BtnGoForge 應隱藏 (visible=false)")
			if not btn_workshop.visible:
				return _fail("選取素材 (iron_scrap) 時 BtnGoWorkshop 應為可見 (visible=true)")
			if btn_workshop.text != "前往工坊":
				return _fail("BtnGoWorkshop 繁中文案不符，期望 '前往工坊'，實得: '%s'" % btn_workshop.text)
			print("  ok 選取素材 (iron_scrap) 顯示『前往工坊』(BtnGoWorkshop)，隱藏『前往鍛造』")

			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			# 截圖 2: 選取素材顯示前往工坊
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_maple_inv_material_selected_workshop_btn.png"))

			# 5.2 寶石 (gem_red_1)
			_inv.set("_selected", "gem_red_1")
			_inv.refresh()
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			if btn_forge.visible:
				return _fail("選取寶石 (gem_red_1) 時 BtnGoForge 應隱藏 (visible=false)")
			if not btn_workshop.visible:
				return _fail("選取寶石 (gem_red_1) 時 BtnGoWorkshop 應為可見 (visible=true)")
			print("  ok 選取寶石 (gem_red_1) 同樣顯示『前往工坊』(BtnGoWorkshop)")

			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證選取消耗品與重要道具時兩按鈕均隱藏 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			# 6.1 消耗品 (hp_s)
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if btn_forge.visible or btn_workshop.visible:
				return _fail("選取消耗品 (hp_s) 時兩快捷按鈕均應隱藏")
			print("  ok 選取消耗品 (hp_s) 時 BtnGoForge 與 BtnGoWorkshop 均隱藏")

			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return false
			# 截圖 3: 選取消耗品快捷按鈕嚴格隱藏
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_maple_inv_consumable_hidden_shortcuts.png"))

			# 6.2 重要道具 (key_rusty)
			_inv.set("_selected", "key_rusty")
			_inv.refresh()
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			if btn_forge.visible or btn_workshop.visible:
				return _fail("選取重要道具 (key_rusty) 時兩快捷按鈕均應隱藏")
			print("  ok 選取重要道具 (key_rusty) 時 BtnGoForge 與 BtnGoWorkshop 均隱藏")

			_step = 10
			_wait = 0

		10:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證點擊發射訊號與連動開啟 ForgeDialog / GemWorkshopDialog ---")
			# 7.1 點擊 BtnGoForge 發射 forge_requested 訊號
			_forge_signal_emitted = false
			_inv.forge_requested.connect(func():
				_forge_signal_emitted = true
			, CONNECT_ONE_SHOT)

			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			var btn_forge: Button = _inv.call("get_go_forge_button")
			btn_forge.pressed.emit()

			if not _forge_signal_emitted:
				return _fail("點擊 BtnGoForge 未能發射 forge_requested 訊號")
			print("  ok 點擊 BtnGoForge 成功發射 forge_requested 訊號")

			_step = 11
			_wait = 0

		11:
			if _wait < 5:
				return false
			# 驗證 open_forge 連動開啟 ForgeDialog 且背包關閉
			var forge_dlg: Control = root.get_node_or_null("ForgeDialog")
			if forge_dlg == null:
				return _fail("點擊 BtnGoForge 未能成功開啟 ForgeDialog")
			if _inv.visible:
				return _fail("開啟 ForgeDialog 後背包應自動關閉 (visible=false)")
			print("  ok 成功直通連動開啟 ForgeDialog，背包自動關閉")

			# 截圖 4: ForgeDialog 開啟存證
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_maple_inv_forge_dialog_opened.png"))
			forge_dlg.queue_free()

			_step = 12
			_wait = 0

		12:
			if _wait < 3:
				return false
			# 重新開啟背包，測試 BtnGoWorkshop
			_inv.open()
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()

			_workshop_signal_emitted = false
			_inv.workshop_requested.connect(func():
				_workshop_signal_emitted = true
			, CONNECT_ONE_SHOT)

			var btn_workshop: Button = _inv.call("get_go_workshop_button")
			btn_workshop.pressed.emit()

			if not _workshop_signal_emitted:
				return _fail("點擊 BtnGoWorkshop 未能發射 workshop_requested 訊號")
			print("  ok 點擊 BtnGoWorkshop 成功發射 workshop_requested 訊號")

			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			# 驗證 open_gem_workshop 連動開啟 GemWorkshopDialog 且背包關閉
			var gem_dlg: Control = root.get_node_or_null("GemWorkshopDialog")
			if gem_dlg == null:
				return _fail("點擊 BtnGoWorkshop 未能成功開啟 GemWorkshopDialog")
			if _inv.visible:
				return _fail("開啟 GemWorkshopDialog 後背包應自動關閉 (visible=false)")
			print("  ok 成功直通連動開啟 GemWorkshopDialog，背包自動關閉")

			# 截圖 5: GemWorkshopDialog 開啟存證
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_maple_inv_gem_workshop_opened.png"))
			gem_dlg.queue_free()

			_step = 14
			_wait = 0

		14:
			if _wait < 3:
				return false
			_inv.open()

			print("\n--- 8. 驗證六語系即時切換與在地化字典 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			for l: String in LOCALES:
				loc.call("set_locale", l)
				_inv.set("_selected", "rusty_blade")
				_inv.refresh()

				var exp_forge: String = EXPECTED_FORGE_TEXTS[l]
				if btn_forge.text != exp_forge:
					return _fail("[%s] 前往鍛造文案不符，期望: '%s'，實得: '%s'" % [l, exp_forge, btn_forge.text])

				_inv.set("_selected", "iron_scrap")
				_inv.refresh()

				var exp_workshop: String = EXPECTED_WORKSHOP_TEXTS[l]
				if btn_workshop.text != exp_workshop:
					return _fail("[%s] 前往工坊文案不符，期望: '%s'，實得: '%s'" % [l, exp_workshop, btn_workshop.text])

				# 歐美語系 (en, es) 零 CJK 檢查
				if l in ["en", "es"]:
					if _has_cjk(btn_forge.text):
						return _fail("[%s] BtnGoForge 殘留 CJK 字元: %s" % [l, btn_forge.text])
					if _has_cjk(btn_workshop.text):
						return _fail("[%s] BtnGoWorkshop 殘留 CJK 字元: %s" % [l, btn_workshop.text])

				print("  ok [%s] 雙快捷按鈕語系文案完全對齊: Forge='%s', Workshop='%s'" % [l, exp_forge, exp_workshop])

			# 在英文語系存證截圖
			loc.call("set_locale", "en")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			_step = 15
			_wait = 0

		15:
			if _wait < 5:
				return false
			# 截圖 6: 英文語系存證
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_maple_inv_shortcuts_i18n_locales.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			_step = 16
			_wait = 0

		16:
			if _wait < 3:
				return false

			print("\n--- 9. 零系統 Emoji 嚴格檢查 ---")
			var btn_forge: Button = _inv.call("get_go_forge_button")
			var btn_workshop: Button = _inv.call("get_go_workshop_button")

			if _has_emoji(btn_forge.text):
				return _fail("BtnGoForge 包含違規系統 Emoji: %s" % btn_forge.text)
			if _has_emoji(btn_workshop.text):
				return _fail("BtnGoWorkshop 包含違規系統 Emoji: %s" % btn_workshop.text)
			print("  ok 零系統 Emoji 檢查通過 (100% 純文字與手繪質感)")

			_step = 17
			_wait = 0

		17:
			if _wait < 3:
				return false

			print("\n--- 10. 實機截圖 SHA256 獨立性驗證 ---")
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
			print("🎉 全部 MapleInventory 裝備與素材快捷跳轉單元測試通過！")
			print("MAPLE_INVENTORY_SHORTCUTS_OK")
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
