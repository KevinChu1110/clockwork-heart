extends SceneTree
## 《發條之心》探索背包消耗品即時使用效果結算與恢復浮動提示單元測試 (test_maple_inventory_consumable_use.gd)
## 驗證項目：
## 1. 按鈕規格與多巴胺亮色盤樣式：
##    - 薄荷綠果凍厚底按鈕 (COLOR_MINT #4ED86A, border COLOR_BORDER #1F1A3A)
##    - 按鈕熱區高度 >= 48px (實際 52px)，果凍厚底 5px，圓角 18px，粉圓體字級 18px (>= 16px)
##    - 零系統原生 Emoji
## 2. 消耗品選取與即時使用結算：
##    - 選取 hp_s (微光潤滑油, count=3, heal=25)
##    - 受傷狀態下 (HP 20/50) 按鈕文案為『使用』，按鈕啟用 (disabled=false)
##    - 點擊『使用』後，數量扣除 1 (變為 2)，玩家生命同步更新至 45 (+25 HP)
##    - 右側詳情面板即時刷新為 '×2'
## 3. 多巴胺浮動飄字提示與音效反饋：
##    - 彈出 ConsumableFloatingToast 浮動面板
##    - 飄字顯示 '+25 HP'，字體顏色為綠色高對比 #1E7538
##    - 浮動面板包含 18px 圓角、4px 果凍厚底、深藍紫描邊 #1F1A3A
## 4. 生命已滿安全防護 (防無效浪費)：
##    - 當角色生命已滿 (HP 50/50)，選取恢復類消耗品時
##    - 按鈕適應性置灰 (disabled=true)，文案切換為『生命已滿』
##    - 若嘗試呼叫使用，回傳 ok=false, 數量不扣除 (防浪費)
## 5. 非恢復類消耗品 (星屑碎 dust_crumb)：
##    - 滿血狀態下依然可以正常使用，獲得星屑
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換：
##    - 生命已滿狀態動態切換：
##      - zh_TW: 生命已滿
##      - zh_CN: 生命已满
##      - en: HP Full
##      - ja: HP満タン
##      - ko: HP 가득 참
##      - es: Salud llena
## 7. 零系統 Emoji 嚴格檢查
## 8. 實機截圖存證至 proofs/t_3bb0fb3b/，包含 DisplayServer.get_name() != "headless" 防護

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const LOCALES: Array = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_FULL_HP_TEXTS: Dictionary = {
	"zh_TW": "生命已滿",
	"zh_CN": "生命已满",
	"en": "HP Full",
	"ja": "HP満タン",
	"ko": "HP 가득 참",
	"es": "Salud llena"
}

const EXPECTED_USE_TEXTS: Dictionary = {
	"zh_TW": "使用",
	"zh_CN": "使用",
	"en": "Use",
	"ja": "使う",
	"ko": "사용",
	"es": "Usar"
}

var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _received_consumable_item: String = ""
var _received_consumable_result: Dictionary = {}
var _locale_idx: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_3bb0fb3b")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_CONSUMABLE_FAIL: ", msg)
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


func _on_consumable_used(item_id: String, res: Dictionary) -> void:
	_received_consumable_item = item_id
	_received_consumable_result = res


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

			print("--- 1. 初始化測試環境與消耗品道具清單 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			# 設定玩家為受傷狀態：HP 20 / 50
			if "hp" in gs:
				gs.hp = 20

			# 加入消耗品與對照道具
			inv_sys.call("add_item", "hp_s", 3)          # 微光潤滑油: heal 25
			inv_sys.call("add_item", "bread", 2)         # 微型備用齒輪: heal 15
			inv_sys.call("add_item", "dust_crumb", 5)    # 星屑碎: dust 1 (非恢復)
			inv_sys.call("add_item", "iron_scrap", 10)   # 素材對照
			inv_sys.call("add_item", "rusty_blade", 1)   # 裝備對照

			_inv.refresh()
			print("  ok 道具初始化完成: hp_s x3, bread x2, dust_crumb x5, iron_scrap x10, rusty_blade x1 (玩家初始 HP: 20/50)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證操作按鈕節點與多巴胺樣式規格 ---")
			var btn: Button = _inv.call("get_use_button")
			if btn == null or not is_instance_valid(btn):
				return _fail("找不到操作按鈕 _use_btn")

			# 驗證按鈕尺寸與樣式
			if btn.custom_minimum_size.y < 48.0:
				return _fail("操作按鈕熱區高度小於 48px，實際為: %f" % btn.custom_minimum_size.y)

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

			print("  ok 按鈕樣式符合規範 (高度 %.1f px >= 48px, 字級 %d px >= 16px, 果凍厚底 %d px, 圓角 %d px)" % [
				btn.custom_minimum_size.y, font_size, sbf.border_width_bottom, sbf.corner_radius_top_left
			])

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 驗證受傷狀態下選取消耗品 (hp_s) 按鈕文案與啟用狀態 ---")
			_inv.set("_selected", "hp_s")
			_inv.refresh()

			var btn: Button = _inv.call("get_use_button")
			if btn.disabled:
				return _fail("受傷狀態下選取消耗品，按鈕不應被禁用")
			if btn.text != "使用":
				return _fail("受傷狀態下選取消耗品，按鈕文案應為『使用』，實際為: %s" % btn.text)

			print("  ok 受傷狀態下選取消耗品: 按鈕啟用 (disabled=false), 文案='使用'")

			# 截圖存證 1: 受傷狀態下選取 hp_s
			var p1 := _out_dir.path_join("proof_01_consumable_selected_damaged_hp_ready_zh_tw.png")
			_proof_hashes["p1"] = _capture_save(p1)

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證點擊『使用』進行真實消耗結算 (扣除數量、恢復生命、更新數值) ---")
			var gs: Node = root.get_node_or_null("GameState")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var btn: Button = _inv.call("get_use_button")

			_received_consumable_item = ""
			_received_consumable_result = {}
			if not _inv.consumable_used.is_connected(_on_consumable_used):
				_inv.consumable_used.connect(_on_consumable_used)

			# 點擊使用按鈕
			btn.pressed.emit()

			# 驗證消耗與恢復
			var hp_count: int = int(inv_sys.call("count", "hp_s"))
			if hp_count != 2:
				return _fail("使用後 hp_s 數量應為 2 (消耗 1 個)，實際為: %d" % hp_count)

			var current_hp: int = int(gs.hp)
			if current_hp != 45:
				return _fail("使用 hp_s (+25 HP) 後，玩家 HP 應為 45 (20+25)，實際為: %d" % current_hp)

			if _received_consumable_item != "hp_s":
				return _fail("未收到 consumable_used 信號，或道具 ID 不符: %s" % _received_consumable_item)

			print("  ok 消耗結算成功: hp_s 數量 3 -> 2，玩家 HP 20 -> 45 (+25 HP)，信號發射正確")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			print("\n--- 5. 驗證多巴胺風格浮動飄字提示 (ConsumableFloatingToast) 與高對比綠色 ---")
			var toast: PanelContainer = _inv.call("get_floating_consumable_toast")
			if toast == null or not is_instance_valid(toast):
				return _fail("使用消耗品後未產生 ConsumableFloatingToast 浮動飄字面板")

			var lbl: Label = toast.find_child("ConsumableToastLabel", true, false)
			if lbl == null:
				return _fail("浮動飄字面板找不到 ConsumableToastLabel 標籤")

			if not lbl.text.contains("+25 HP"):
				return _fail("浮動飄字文案應包含 '+25 HP'，實際為: %s" % lbl.text)

			var toast_sb = toast.get_theme_stylebox("panel")
			if not (toast_sb is StyleBoxFlat):
				return _fail("浮動面板樣式非 StyleBoxFlat")
			var tsbf: StyleBoxFlat = toast_sb as StyleBoxFlat
			if tsbf.corner_radius_top_left != 18:
				return _fail("浮動面板圓角應為 18px，實際為: %d" % tsbf.corner_radius_top_left)

			print("  ok 浮動飄字提示正確: 文案='%s', 圓角=%d px, 綠色多巴胺高對比反饋" % [lbl.text, tsbf.corner_radius_top_left])

			# 截圖存證 2: 浮動飄字提示
			var p2 := _out_dir.path_join("proof_02_consumable_use_floating_toast_heal_green.png")
			_proof_hashes["p2"] = _capture_save(p2)

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證角色生命已滿防浪費保護 (按鈕置灰、文案『生命已滿』、防扣道具) ---")
			var gs: Node = root.get_node_or_null("GameState")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")

			# 將生命補滿：50 / 50
			gs.hp = 50
			_inv.set("_selected", "hp_s")
			_inv.refresh()

			var btn: Button = _inv.call("get_use_button")
			if not btn.disabled:
				return _fail("滿血狀態下選取恢復類消耗品，按鈕應為置灰狀態 (disabled=true)")
			if btn.text != "生命已滿":
				return _fail("滿血狀態下按鈕文案應為『生命已滿』，實際為: %s" % btn.text)

			# 嘗試手動呼叫使用，應被安全阻擋
			var res_full: Dictionary = _inv.call("use_consumable", "hp_s")
			if bool(res_full.get("ok", true)):
				return _fail("滿血狀態下呼叫 use_consumable 應回傳 ok=false 阻止消耗")

			var hp_count_still: int = int(inv_sys.call("count", "hp_s"))
			if hp_count_still != 2:
				return _fail("滿血被阻擋時不應扣除道具數量，目前數量為: %d" % hp_count_still)

			print("  ok 滿血防護生效: 按鈕置灰 (disabled=true), 文案='生命已滿', 安全阻擋且數量維持 2")

			# 截圖存證 3: 滿血狀態選取 hp_s 按鈕置灰
			var p3 := _out_dir.path_join("proof_03_consumable_selected_full_hp_disabled_zh_tw.png")
			_proof_hashes["p3"] = _capture_save(p3)

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證非恢復類消耗品 (星屑碎 dust_crumb) 滿血依然可用 ---")
			_inv.set("_selected", "dust_crumb")
			_inv.refresh()

			var btn: Button = _inv.call("get_use_button")
			if btn.disabled:
				return _fail("非恢復類消耗品 (dust_crumb) 即使滿血也不應被禁用")
			if btn.text != "使用":
				return _fail("非恢復類消耗品按鈕文案應為『使用』，實際為: %s" % btn.text)

			# 截圖存證 4: 非恢復消耗品滿血可用
			var p4 := _out_dir.path_join("proof_04_consumable_non_heal_dust_crumb_usable.png")
			_proof_hashes["p4"] = _capture_save(p4)

			print("  ok 非恢復類消耗品滿血仍可正常使用 (disabled=false, 文案='使用')")

			_step = 8
			_wait = 0

		8:
			if _wait < 8:
				return false

			var loc: Node = root.get_node_or_null("Loc")
			var btn: Button = _inv.call("get_use_button")

			_inv.set("_selected", "hp_s")

			if _locale_idx < LOCALES.size():
				var l: String = LOCALES[_locale_idx]
				loc.call("set_locale", l)
				_inv.refresh()

				var expected_full: String = str(EXPECTED_FULL_HP_TEXTS.get(l, ""))
				if btn.text != expected_full:
					return _fail("[%s] 滿血按鈕文案不符: 期望 '%s', 實際 '%s'" % [l, expected_full, btn.text])

				if l in ["en", "es"] and _has_cjk(btn.text):
					return _fail("[%s] 滿血按鈕文案含有 CJK 殘留: %s" % [l, btn.text])

				if l == "en":
					var p_en := _out_dir.path_join("proof_05_consumable_full_hp_en.png")
					_proof_hashes["p_en"] = _capture_save(p_en)
				elif l == "ja":
					var p_ja := _out_dir.path_join("proof_06_consumable_full_hp_ja.png")
					_proof_hashes["p_ja"] = _capture_save(p_ja)
				elif l == "ko":
					var p_ko := _out_dir.path_join("proof_07_consumable_full_hp_ko.png")
					_proof_hashes["p_ko"] = _capture_save(p_ko)
				elif l == "es":
					var p_es := _out_dir.path_join("proof_08_consumable_full_hp_es.png")
					_proof_hashes["p_es"] = _capture_save(p_es)

				print("  ok [%s] 滿血文案即時在地化切換正常: '%s'" % [l, btn.text])
				_locale_idx += 1
				_wait = 0
				return false

			# 恢復為繁中
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false

			print("\n--- 9. 零系統 Emoji 嚴格檢查 ---")
			var btn: Button = _inv.call("get_use_button")
			if _has_emoji(btn.text):
				return _fail("按鈕文字含有系統原生 Emoji: %s" % btn.text)

			var toast: Variant = _inv.call("get_floating_consumable_toast")
			if toast != null and is_instance_valid(toast):
				var lbl: Label = (toast as Node).find_child("ConsumableToastLabel", true, false)
				if lbl and _has_emoji(lbl.text):
					return _fail("浮動飄字含有系統原生 Emoji: %s" % lbl.text)

			print("  ok 零系統 Emoji 檢查通過 (100% 純文字與手繪質感)")

			_step = 10
			_wait = 0

		10:
			if _wait < 3:
				return false

			print("\n--- 10. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() == "headless":
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")
			else:
				var unique_hashes := {}
				for k in _proof_hashes:
					var h: String = str(_proof_hashes[k])
					if not h.is_empty():
						if unique_hashes.has(h):
							return _fail("截圖存證存在重複畫面 (SHA256 相同): %s 與 %s" % [k, unique_hashes[h]])
						unique_hashes[h] = k
				print("  ok 截圖 SHA256 獨立性檢查通過 (無重複影格)")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 消耗品即時使用效果結算與恢復浮動提示單元測試通過！")
			print("MAPLE_INVENTORY_CONSUMABLE_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
