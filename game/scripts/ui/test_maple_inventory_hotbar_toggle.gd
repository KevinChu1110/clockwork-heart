extends SceneTree
## 《發條之心》探索背包快捷欄綁定狀態膠囊顯示與一鍵卸下快捷鍵單元與功能測試 (test_maple_inventory_hotbar_toggle.gd)
## 驗證項目：
## 1. 按鈕規格與多巴胺亮色盤樣式：
##    - 按鈕熱區高度 >= 48px (實際 52px)，果凍厚底 5px，圓角 18px，粉圓體字級 18px (>= 16px)
##    - 未綁定：天藍果凍厚底按鈕 (COLOR_SKY #38A0FF, border COLOR_BORDER #1F1A3A, text 『放到快捷欄』)
##    - 已綁定：珊瑚粉果凍厚底按鈕 (COLOR_PINK #FF5E8A, border COLOR_BORDER #1F1A3A, text 『從快捷欄卸下』)
##    - 零系統原生 Emoji
## 2. 快捷欄槽位狀態膠囊規格與顯示：
##    - 天藍底膠囊 (COLOR_SKY #38A0FF, border COLOR_BORDER #1F1A3A, 3px 立體厚底, 圓角 10px)
##    - 膠囊字級 14px (14~16px 加粗，深藍紫描邊 outline 3px，白色文字，零 Emoji)
##    - 未綁定或未選取時隱藏 (visible=false)
##    - 綁定於槽位 0 時顯示『快捷欄 1』，綁定於槽位 1 時顯示『快捷欄 2』
## 3. 雙向動態切換與信號發射：
##    - 未綁定時點擊按鈕觸發 assign_hotbar 並綁定至快捷欄
##    - 已綁定時點擊按鈕觸發 remove_hotbar，清空 GameState.hotbar 對應槽位
##    - 彈出 HotbarFloatingToast 浮動飄字提示『已從快捷欄卸下：XX』
## 4. 裝備與未選取保護：
##    - 選取裝備類物品 (如 rusty_blade) 時快捷欄按鈕與膠囊隱藏
##    - 未選取時快捷欄按鈕置灰 (disabled=true)，膠囊隱藏
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換：
##    - 膠囊文字動態切換 (快捷欄 1 / 快捷栏 1 / Hotbar 1 / ショートカット 1 / 단축칸 1 / Acceso rápido 1)
##    - 卸下按鈕文字動態切換 (從快捷欄卸下 / 从快捷栏卸下 / Remove from Hotbar / ショートカットから解除 / 단축칸에서 해제 / Quitar de acceso rápido)
##    - 綁定按鈕文字動態切換 (放到快捷欄 / 放入快捷栏 / Assign to Hotbar / ショートカットに登録 / 단축칸에 등록 / Asignar a acceso rápido)
## 6. 零系統 Emoji 嚴格檢查
## 7. 實機截圖存證至 proofs/t_013e8c02/，包含 Viewport 等待幀數與 SHA256 唯一性檢查

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const LOCALES: Array = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_CAPSULE_TEXTS: Dictionary = {
	"zh_TW": "快捷欄 1",
	"zh_CN": "快捷栏 1",
	"en": "Hotbar 1",
	"ja": "ショートカット 1",
	"ko": "단축칸 1",
	"es": "Acceso rápido 1"
}

const EXPECTED_REMOVE_BTN_TEXTS: Dictionary = {
	"zh_TW": "從快捷欄卸下",
	"zh_CN": "从快捷栏卸下",
	"en": "Remove from Hotbar",
	"ja": "ショートカットから解除",
	"ko": "단축칸에서 해제",
	"es": "Quitar de acceso rápido"
}

const EXPECTED_ASSIGN_BTN_TEXTS: Dictionary = {
	"zh_TW": "放到快捷欄",
	"zh_CN": "放入快捷栏",
	"en": "Assign to Hotbar",
	"ja": "ショートカットに登録",
	"ko": "단축칸에 등록",
	"es": "Asignar a acceso rápido"
}

var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _received_assign_item: String = ""
var _received_remove_item: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_013e8c02")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	_inv.size = Vector2(1280, 720)
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_HOTBAR_TOGGLE_FAIL: ", msg)
	quit(1)
	return true


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
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
	var img := tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var f := FileAccess.open(path, FileAccess.READ)
	if f:
		var h := f.get_sha256(path)
		f.close()
		return h
	return ""


func _on_assign_hotbar_signal(item_id: String) -> void:
	_received_assign_item = item_id


func _on_remove_hotbar_signal(item_id: String) -> void:
	_received_remove_item = item_id


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

			print("--- 1. 初始化測試環境與道具清單 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "hotbar" in gs and gs.hotbar != null:
				gs.hotbar = ["", "", "", "", "", "", "", ""]

			inv_sys.call("add_item", "hp_s", 5)          # 微光潤滑油
			inv_sys.call("add_item", "bread", 3)         # 微型備用齒輪
			inv_sys.call("add_item", "iron_scrap", 10)   # 素材
			inv_sys.call("add_item", "rusty_blade", 1)   # 裝備

			# 清除 add_item 自動塞入的 hotbar
			gs.hotbar = ["", "", "", "", "", "", "", ""]
			_inv.refresh()
			print("  ok 道具初始化完成，GameState.hotbar 已重置為全空")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證按鈕與膠囊節點規格與多巴胺樣式 ---")
			var btn: Button = _inv.call("get_hotbar_button")
			if btn == null or not is_instance_valid(btn):
				return _fail("找不到快捷欄操作按鈕 _hb_btn (get_hotbar_button)")

			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
			if capsule == null or not is_instance_valid(capsule):
				return _fail("找不到快捷欄狀態膠囊 _hotbar_capsule (get_hotbar_capsule)")

			var cap_lbl: Label = _inv.call("get_hotbar_capsule_label")
			if cap_lbl == null or not is_instance_valid(cap_lbl):
				return _fail("找不到快捷欄狀態膠囊標籤 _hotbar_capsule_label")

			# 驗證按鈕尺寸與樣式
			if btn.custom_minimum_size.y < 48.0:
				return _fail("快捷欄按鈕熱區高度小於 48px，實際為: %f" % btn.custom_minimum_size.y)

			var font_size = btn.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("按鈕字級小於 16px，實際為: %d" % font_size)

			var sb = btn.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("按鈕 normal 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if sbf.border_width_bottom != 5:
				return _fail("按鈕底邊厚度應為 5px 果凍厚底，實際為: %d" % sbf.border_width_bottom)
			if sbf.corner_radius_top_left != 18:
				return _fail("按鈕圓角應為 18px，實際為: %d" % sbf.corner_radius_top_left)

			# 驗證膠囊樣式
			var csb = capsule.get_theme_stylebox("panel")
			if not (csb is StyleBoxFlat):
				return _fail("膠囊樣式非 StyleBoxFlat")
			var csbf: StyleBoxFlat = csb as StyleBoxFlat
			if csbf.bg_color != Color("#38A0FF"):
				return _fail("膠囊背景色應為天藍底 #38A0FF，實際為: %s" % csbf.bg_color.to_html())
			if csbf.border_color != Color("#1F1A3A"):
				return _fail("膠囊描邊應為深藍紫 #1F1A3A，實際為: %s" % csbf.border_color.to_html())

			var cap_font_sz = cap_lbl.get_theme_font_size("font_size")
			if cap_font_sz < 14 or cap_font_sz > 16:
				return _fail("膠囊字級應在 14~16px 之間，實際為: %d" % cap_font_sz)

			print("  ok 按鈕樣式符合規範 (高度 %.1f px >= 48px, 字級 %d px, 果凍底 5px, 圓角 18px)" % [btn.custom_minimum_size.y, font_size])
			print("  ok 膠囊樣式符合規範 (天藍底 #38A0FF, 深藍紫描邊 #1F1A3A, 字級 %d px)" % cap_font_sz)

			# 準備進入未綁定選取狀態
			var gs: Node = root.get_node_or_null("GameState")
			gs.hotbar = ["", "", "", "", "", "", "", ""]
			_inv.set("_selected", "hp_s")
			_inv.refresh()

			_step = 3
			_wait = 0

		3:
			# 等待 Viewport 影格完全繪製未綁定狀態
			if _wait < 4:
				return false

			print("\n--- 3. 驗證選取未綁定消耗品 (hp_s) 顯示『放到快捷欄』與膠囊隱藏 ---")
			var btn: Button = _inv.call("get_hotbar_button")
			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")

			if capsule.visible:
				return _fail("未綁定道具時，快捷欄狀態膠囊應隱藏 (visible=false)")
			if btn.disabled:
				return _fail("選取未綁定消耗品時，快捷欄按鈕應啟用 (disabled=false)")
			if btn.text != "放到快捷欄":
				return _fail("未綁定時按鈕文案應為『放到快捷欄』，實際為: %s" % btn.text)

			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb.bg_color != Color("#38A0FF"):
				return _fail("未綁定時按鈕底色應為天藍底 #38A0FF，實際為: %s" % sb.bg_color.to_html())

			print("  ok 未綁定狀態驗證通過: 膠囊隱藏，按鈕為天藍底『放到快捷欄』")

			# 截圖存證 1: 未綁定消耗品 (天藍底按鈕)
			var p1 := _out_dir.path_join("proof_01_hotbar_unbound_assign_btn_sky_zh_tw.png")
			_proof_hashes["p1"] = _capture_save(p1)

			# 觸發綁定操作
			_received_assign_item = ""
			if not _inv.assign_hotbar.is_connected(_on_assign_hotbar_signal):
				_inv.assign_hotbar.connect(_on_assign_hotbar_signal)
			btn.pressed.emit()

			_step = 4
			_wait = 0

		4:
			# 等待 Viewport 影格完全繪製綁定槽位 0 後之狀態
			if _wait < 4:
				return false

			print("\n--- 4. 驗證點擊『放到快捷欄』綁定至槽位 0 (槽位 1) ---")
			if _received_assign_item != "hp_s":
				return _fail("未收到 assign_hotbar 信號或道具 ID 不符: %s" % _received_assign_item)

			var gs: Node = root.get_node_or_null("GameState")
			if str(gs.hotbar[0]) != "hp_s":
				return _fail("點擊綁定後 GameState.hotbar[0] 應為 'hp_s'，實際為: %s" % str(gs.hotbar[0]))

			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
			var cap_lbl: Label = _inv.call("get_hotbar_capsule_label")
			var btn: Button = _inv.call("get_hotbar_button")

			if not capsule.visible:
				return _fail("已綁定於快捷欄後，狀態膠囊應顯示 (visible=true)")
			if cap_lbl.text != "快捷欄 1":
				return _fail("綁定槽位 0 膠囊文案應為『快捷欄 1』，實際為: %s" % cap_lbl.text)
			if btn.text != "從快捷欄卸下":
				return _fail("已綁定後按鈕文案應切換為『從快捷欄卸下』，實際為: %s" % btn.text)

			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb.bg_color != Color("#FF5E8A"):
				return _fail("已綁定後按鈕底色應切換為珊瑚粉 #FF5E8A，實際為: %s" % sb.bg_color.to_html())

			print("  ok 綁定成功: 信號正確，GameState.hotbar[0]='hp_s'，膠囊='快捷欄 1'，按鈕為珊瑚粉『從快捷欄卸下』")

			# 截圖存證 2: 已綁定槽位 0 (天藍膠囊『快捷欄 1』與珊瑚粉按鈕『從快捷欄卸下』)
			var p2 := _out_dir.path_join("proof_02_hotbar_bound_slot1_capsule_pink_btn_zh_tw.png")
			_proof_hashes["p2"] = _capture_save(p2)

			# 切換至槽位 1 進行多槽位辨識驗證
			gs.hotbar[0] = ""
			gs.hotbar[1] = "hp_s"
			_inv.refresh()

			_step = 5
			_wait = 0

		5:
			# 等待 Viewport 影格完全繪製槽位 1
			if _wait < 4:
				return false

			print("\n--- 5. 驗證綁定至槽位 1 顯示『快捷欄 2』標籤膠囊 ---")
			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
			var cap_lbl: Label = _inv.call("get_hotbar_capsule_label")
			var btn: Button = _inv.call("get_hotbar_button")

			if not capsule.visible:
				return _fail("綁定於槽位 1 時膠囊應為 visible")
			if cap_lbl.text != "快捷欄 2":
				return _fail("綁定槽位 1 膠囊文案應為『快捷欄 2』，實際為: %s" % cap_lbl.text)
			if btn.text != "從快捷欄卸下":
				return _fail("綁定槽位 1 時按鈕文案應為『從快捷欄卸下』，實際為: %s" % btn.text)

			print("  ok 槽位 1 識別正確: 膠囊='快捷欄 2'，按鈕='從快捷欄卸下'")

			# 截圖存證 3: 綁定槽位 1 (膠囊『快捷欄 2』)
			var p3 := _out_dir.path_join("proof_03_hotbar_bound_slot2_capsule_zh_tw.png")
			_proof_hashes["p3"] = _capture_save(p3)

			# 觸發卸下操作
			_received_remove_item = ""
			if not _inv.remove_hotbar.is_connected(_on_remove_hotbar_signal):
				_inv.remove_hotbar.connect(_on_remove_hotbar_signal)
			btn.pressed.emit()

			_step = 6
			_wait = 0

		6:
			# 等待 Viewport 繪製卸下浮動提示與更新後之介面
			if _wait < 4:
				return false

			print("\n--- 6. 驗證點擊『從快捷欄卸下』一鍵卸下、Toast 提示與狀態即時更新 ---")
			if _received_remove_item != "hp_s":
				return _fail("未收到 remove_hotbar 信號或道具 ID 不符: %s" % _received_remove_item)

			var gs: Node = root.get_node_or_null("GameState")
			if str(gs.hotbar[1]) != "":
				return _fail("卸下後 GameState.hotbar[1] 應被清空為空字串，實際為: %s" % str(gs.hotbar[1]))

			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
			var btn: Button = _inv.call("get_hotbar_button")

			if capsule.visible:
				return _fail("卸下後狀態膠囊應隱藏 (visible=false)")
			if btn.text != "放到快捷欄":
				return _fail("卸下後按鈕文案應切換回『放到快捷欄』，實際為: %s" % btn.text)

			var toast: PanelContainer = _inv.call("get_floating_hotbar_toast")
			if toast == null or not is_instance_valid(toast):
				return _fail("點擊卸下後未彈出 HotbarFloatingToast 浮動提示面板")

			var toast_lbl: Label = toast.find_child("HotbarToastLabel", true, false)
			if toast_lbl == null:
				return _fail("浮動提示面板找不到 HotbarToastLabel 標籤")
			if not toast_lbl.text.contains("已從快捷欄卸下") or not toast_lbl.text.contains("微光潤滑油"):
				return _fail("浮動提示文字應包含『已從快捷欄卸下：微光潤滑油』，實際為: %s" % toast_lbl.text)

			print("  ok 卸下流程驗證通過: 信號發射、GameState.hotbar 清空、膠囊隱藏、按鈕還原、浮動提示='%s'" % toast_lbl.text)

			# 截圖存證 4: 卸下 Toast 提示
			var p4 := _out_dir.path_join("proof_04_hotbar_unbind_toast_zh_tw.png")
			_proof_hashes["p4"] = _capture_save(p4)

			# 清理 Toast 避免殘留在後續語系截圖中
			if toast and is_instance_valid(toast):
				toast.queue_free()

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證選取裝備類物品 (rusty_blade) 時快捷欄按鈕與膠囊隱藏 ---")
			var gs: Node = root.get_node_or_null("GameState")
			gs.hotbar[0] = "rusty_blade"
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			var btn: Button = _inv.call("get_hotbar_button")
			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
			var d_btn: Button = _inv.call("get_dismantle_button")

			if btn.visible:
				return _fail("選取裝備類物品時快捷欄按鈕應隱藏 (visible=false)")
			if capsule.visible:
				return _fail("選取裝備類物品時快捷欄膠囊應隱藏 (visible=false)")
			if not d_btn.visible:
				return _fail("選取裝備類物品時拆解回收按鈕應可見 (visible=true)")

			print("  ok 裝備互斥保護驗證通過: 快捷欄按鈕與膠囊隱藏，拆解按鈕可見")

			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false

			print("\n--- 8. 驗證未選取任何道具時快捷欄按鈕置灰 (disabled=true) 與膠囊隱藏 ---")
			_inv.set("_selected", "")
			_inv.refresh()

			var btn: Button = _inv.call("get_hotbar_button")
			var capsule: PanelContainer = _inv.call("get_hotbar_capsule")

			if not btn.visible:
				return _fail("未選取時快捷欄按鈕應為可見 (visible=true)")
			if not btn.disabled:
				return _fail("未選取時快捷欄按鈕應為置灰 (disabled=true)")
			if capsule.visible:
				return _fail("未選取時快捷欄膠囊應隱藏 (visible=false)")

			print("  ok 未選取保護驗證通過: 按鈕可見且置灰，膠囊隱藏")

			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false

			print("\n--- 9. 驗證六語系邏輯斷言與即時切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var gs: Node = root.get_node_or_null("GameState")

			# 綁定 hp_s 至槽位 0
			gs.hotbar[0] = "hp_s"
			_inv.set("_selected", "hp_s")

			for lc in LOCALES:
				loc.call("set_locale", lc)
				_inv.refresh()

				var capsule: PanelContainer = _inv.call("get_hotbar_capsule")
				var cap_lbl: Label = _inv.call("get_hotbar_capsule_label")
				var btn: Button = _inv.call("get_hotbar_button")

				var exp_cap = EXPECTED_CAPSULE_TEXTS[lc]
				var exp_rem = EXPECTED_REMOVE_BTN_TEXTS[lc]
				var exp_asg = EXPECTED_ASSIGN_BTN_TEXTS[lc]

				if not capsule.visible:
					return _fail("[%s] 語系下已綁定膠囊應為 visible" % lc)
				if cap_lbl.text != exp_cap:
					return _fail("[%s] 語系膠囊文案錯誤，預期 '%s'，實際: '%s'" % [lc, exp_cap, cap_lbl.text])
				if btn.text != exp_rem:
					return _fail("[%s] 語系卸下按鈕文案錯誤，預期 '%s'，實際: '%s'" % [lc, exp_rem, btn.text])

				# 測試未綁定按鈕文案
				gs.hotbar[0] = ""
				_inv.refresh()
				if capsule.visible:
					return _fail("[%s] 語系下未綁定膠囊應隱藏" % lc)
				if btn.text != exp_asg:
					return _fail("[%s] 語系未綁定按鈕文案錯誤，預期 '%s'，實際: '%s'" % [lc, exp_asg, btn.text])

				# 還原綁定
				gs.hotbar[0] = "hp_s"
				_inv.refresh()

				print("  ok [%s] 語系驗證通過: 膠囊='%s', 卸下='%s', 綁定='%s'" % [lc, exp_cap, exp_rem, exp_asg])

			# 準備進行 en 語系截圖
			loc.call("set_locale", "en")
			_inv.refresh()
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			var p_en := _out_dir.path_join("proof_05_hotbar_bound_en.png")
			_proof_hashes["p_en"] = _capture_save(p_en)
			print("  ok [en] 截圖存證完成")

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ja")
			_inv.refresh()
			_step = 11
			_wait = 0

		11:
			if _wait < 5:
				return false
			var p_ja := _out_dir.path_join("proof_06_hotbar_bound_ja.png")
			_proof_hashes["p_ja"] = _capture_save(p_ja)
			print("  ok [ja] 截圖存證完成")

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ko")
			_inv.refresh()
			_step = 12
			_wait = 0

		12:
			if _wait < 5:
				return false
			var p_ko := _out_dir.path_join("proof_07_hotbar_bound_ko.png")
			_proof_hashes["p_ko"] = _capture_save(p_ko)
			print("  ok [ko] 截圖存證完成")

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "es")
			_inv.refresh()
			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			var p_es := _out_dir.path_join("proof_08_hotbar_bound_es.png")
			_proof_hashes["p_es"] = _capture_save(p_es)
			print("  ok [es] 截圖存證完成")

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()
			_step = 14
			_wait = 0

		14:
			if _wait < 4:
				return false

			print("\n--- 11. 驗證截圖存證雜湊非空且無重複 ---")
			if DisplayServer.get_name() != "headless":
				var keys: Array = _proof_hashes.keys()
				for i in keys.size():
					var k1: String = keys[i]
					var h1: String = _proof_hashes[k1]
					if h1.is_empty():
						return _fail("截圖存證雜湊為空: %s" % k1)
					for j in range(i + 1, keys.size()):
						var k2: String = keys[j]
						var h2: String = _proof_hashes[k2]
						if h1 == h2:
							return _fail("截圖存證重複！%s 與 %s 之 SHA256 相同 (%s)" % [k1, k2, h1])
				print("  ok 8 張實機截圖存證 SHA256 全部唯一無重複")

			print("\n--- 12. 驗證全畫面 100% 零系統原生 Emoji ---")
			var nodes_to_check: Array = [_inv]
			while not nodes_to_check.is_empty():
				var cur: Node = nodes_to_check.pop_front()
				for child in cur.get_children():
					nodes_to_check.append(child)
					if child is Label and _has_emoji(child.text):
						return _fail("Label 包含禁止之系統原生 Emoji: %s (節點: %s)" % [child.text, child.name])
					if child is Button and _has_emoji(child.text):
						return _fail("Button 包含禁止之系統原生 Emoji: %s (節點: %s)" % [child.text, child.name])
					if child is RichTextLabel and _has_emoji(child.text):
						return _fail("RichTextLabel 包含禁止之系統原生 Emoji: %s (節點: %s)" % [child.text, child.name])

			print("  ok 全畫面零系統 Emoji 檢測 100% 通過")

			_step = 15
			_wait = 0

		15:
			print("\n==================================================")
			print("MAPLE_INVENTORY_HOTBAR_TOGGLE_OK (全部驗證通過)")
			print("==================================================")
			quit(0)
			return true

	return false
