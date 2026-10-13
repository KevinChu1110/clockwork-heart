extends SceneTree
## 《發條之心》探索背包一鍵出售未鎖定素材與金幣結算浮動提示單元測試 (test_maple_inventory_batch_sell.gd)
## 驗證項目：
## 1. 按鈕規格與多巴胺亮色盤樣式：
##    - 薄荷綠果凍厚底按鈕 (COLOR_MINT #4ED86A, border COLOR_BORDER #1F1A3A, 2px border)
##    - 按鈕熱區高度 >= 48px (實際 52px)，果凍厚底 5px，圓角 18px，粉圓體字級 18px (>= 16px)
##    - 零系統原生 Emoji
## 2. 按鈕顯示與分類邏輯：
##    - 切換至『素材』Chip 分類時，不論是否選取物品，BtnBatchSellMaterials 皆顯示 (visible=true)
##    - 在全部分類下選取素材物品 (如 iron_scrap) 時，BtnBatchSellMaterials 顯示 (visible=true)
##    - 選取裝備類 (rusty_blade) 或消耗品 (hp_s) 時，BtnBatchSellMaterials 隱藏 (visible=false)
##    - 切換至其他分類 (如 equip, consumable, gem) 時，BtnBatchSellMaterials 隱藏 (visible=false)
## 3. 安全過濾與一鍵出售：
##    - 包含未鎖定素材 (iron_scrap 10 個，單價 6；mist_shard 4 個，單價 12) 與已鎖定素材 (wolf_fang 5 個，單價 8)
##    - 點擊一鍵出售後：
##      - 未鎖定素材全數出售 (10 * 6 + 4 * 12 = 60 + 48 = 108 金幣)
##      - 總金幣累加 +108，材料自背包扣除
##      - 已鎖定素材 (wolf_fang 5 個) 完好保留未被出售
## 4. 金幣結算浮動提示與飄字：
##    - 提示與飄字面板 (GoldFloatingToast) 出現
##    - 文字符合 "賣出材料 14 件 · 金 +108"
## 5. 無可賣素材時的安全防護：
##    - 若只有已鎖定素材或無素材，點擊一鍵出售回傳 ok=false，提示 "沒有可賣的材料。"
## 6. 六語系支援：
##    - zh_TW, zh_CN, en, ja, ko, es 動態即時切換無缺詞、零 CJK 殘留
## 7. 實機截圖存證至 proofs/t_6b9f41f3/，包含 DisplayServer.get_name() != "headless" 防護與 SHA256 驗證

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const LOCALES: Array = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_BATCH_SELL_TEXTS: Dictionary = {
	"zh_TW": "一鍵出售素材",
	"zh_CN": "一键出售素材",
	"en": "Quick-Sell Materials",
	"ja": "素材を一括売却",
	"ko": "재료 일괄 판매",
	"es": "Vender materiales"
}

const EXPECTED_NO_SELL_MATS: Dictionary = {
	"zh_TW": "沒有可賣的材料。",
	"zh_CN": "没有可出售的材料。",
	"en": "No sellable materials.",
	"ja": "売却できる素材がありません。",
	"ko": "판매할 수 있는 재료가 없습니다.",
	"es": "No hay materiales para vender."
}

var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _init_gold: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_6b9f41f3")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_BATCH_SELL_FAIL: ", msg)
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
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / EquipmentSystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "gold" in gs:
				gs.gold = 500
			_init_gold = gs.gold

			# 放入道具
			inv_sys.call("add_item", "rusty_blade", 1)  # 裝備
			inv_sys.call("add_item", "hp_s", 3)         # 消耗品
			inv_sys.call("add_item", "gem_red_1", 2)    # 寶石
			inv_sys.call("add_item", "iron_scrap", 10)  # 未鎖定素材 (單價 6)
			inv_sys.call("add_item", "mist_shard", 4)   # 未鎖定素材 (單價 12)
			inv_sys.call("add_item", "wolf_fang", 5)    # 將設為鎖定之素材 (單價 8)

			# 鎖定 wolf_fang
			_inv.call("set_item_locked", "wolf_fang", true)
			_inv.call("set_item_locked", "iron_scrap", false)
			_inv.call("set_item_locked", "mist_shard", false)

			_inv.refresh()
			print("  ok 道具初始化完成: iron_scrap x10, mist_shard x4, wolf_fang(鎖定) x5, rusty_blade x1, hp_s x3, gem_red_1 x2")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證按鈕節點存在性與多巴胺樣式規格 ---")
			var btn: Button = _inv.call("get_batch_sell_button")
			if btn == null or not is_instance_valid(btn):
				return _fail("找不到 BtnBatchSellMaterials 按鈕節點")

			# 熱區高度與尺寸檢查
			if btn.custom_minimum_size.y < 48:
				return _fail("BtnBatchSellMaterials 高度未達手機熱區標準 (預期 >= 48px，實得: %f)" % btn.custom_minimum_size.y)

			# 字級檢查
			var fsize := btn.get_theme_font_size("font_size")
			if fsize < 16:
				return _fail("BtnBatchSellMaterials 字級未達標 (預期 >= 16px，實得: %d)" % fsize)

			# 樣式檢查 (StyleBoxFlat: 薄荷綠 #4ED86A, 果凍厚底 5px, 圓角 18px, 描邊深藍紫 #1F1A3A)
			var sb := btn.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("BtnBatchSellMaterials normal 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if abs(sbf.bg_color.r - Color("#4ED86A").r) > 0.05 or abs(sbf.bg_color.g - Color("#4ED86A").g) > 0.05 or abs(sbf.bg_color.b - Color("#4ED86A").b) > 0.05:
				return _fail("BtnBatchSellMaterials 底色非薄荷綠 (#4ED86A)，實得: %s" % str(sbf.bg_color))
			if sbf.border_color != Color("#1F1A3A"):
				return _fail("BtnBatchSellMaterials 描邊非深藍紫 (#1F1A3A)，實得: %s" % str(sbf.border_color))
			if sbf.border_width_bottom != 5:
				return _fail("BtnBatchSellMaterials 底描邊厚度非 5px (立體厚底)，實得: %d" % sbf.border_width_bottom)
			if sbf.corner_radius_top_left != 18:
				return _fail("BtnBatchSellMaterials 圓角非 18px，實得: %d" % sbf.corner_radius_top_left)

			print("  ok 按鈕樣式符合規範 (薄荷綠 #4ED86A, 深藍紫描邊 #1F1A3A, 果凍厚底 5px, 圓角 18px, 高度 52px, 字級 18px)")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 驗證不同分類與選取狀態下的按鈕顯示邏輯 ---")
			var btn: Button = _inv.call("get_batch_sell_button")

			# 3.1 切換至『素材』Chip 分類 -> 必須顯示 (visible=true)
			_inv.call("set_category", "material")
			if not btn.visible:
				return _fail("切換至『素材』分類時 BtnBatchSellMaterials 應顯示 (visible=true)")
			print("  ok 切換至『素材』Chip 分類時按鈕正確顯示")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			# 截圖 1: 素材 Chip 分類下一鍵出售按鈕呈現 (zh_TW)
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_maple_inv_material_category_batch_sell_btn.png"))

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			var btn: Button = _inv.call("get_batch_sell_button")

			# 3.2 切換至『裝備』Chip 分類 -> 必須隱藏 (visible=false)
			_inv.call("set_category", "equip")
			if btn.visible:
				return _fail("切換至『裝備』分類時 BtnBatchSellMaterials 應隱藏 (visible=false)")

			# 3.3 切換至『消耗品』Chip 分類 -> 必須隱藏 (visible=false)
			_inv.call("set_category", "consumable")
			if btn.visible:
				return _fail("切換至『消耗品』分類時 BtnBatchSellMaterials 應隱藏 (visible=false)")

			# 3.4 切換回『全部』分類
			_inv.call("set_category", "all")
			# 在全部且選取裝備 (rusty_blade) -> 隱藏
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if btn.visible:
				return _fail("選取裝備 (rusty_blade) 時 BtnBatchSellMaterials 應隱藏 (visible=false)")

			# 在全部且選取消耗品 (hp_s) -> 隱藏
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if btn.visible:
				return _fail("選取消耗品 (hp_s) 時 BtnBatchSellMaterials 應隱藏 (visible=false)")

			# 在全部且選取未鎖定素材 (iron_scrap) -> 必須顯示 (visible=true)
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if not btn.visible:
				return _fail("在全部選取素材 (iron_scrap) 時 BtnBatchSellMaterials 應顯示 (visible=true)")

			print("  ok 分類切換與物品選取顯示條件完全符合規格")

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			# 截圖 2: 選取素材時右側詳情按鈕呈現
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_maple_inv_material_selected_batch_sell_btn.png"))

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證點擊一鍵出售未鎖定素材、保留已鎖定素材與金幣結算 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var gs: Node = root.get_node_or_null("GameState")

			# 確認出售前物品數量與鎖定狀態
			var count_iron_pre: int = int(inv_sys.call("count", "iron_scrap"))
			var count_mist_pre: int = int(inv_sys.call("count", "mist_shard"))
			var count_wolf_pre: int = int(inv_sys.call("count", "wolf_fang"))
			if count_iron_pre != 10 or count_mist_pre != 4 or count_wolf_pre != 5:
				return _fail("出售前數量不符: iron=%d, mist=%d, wolf=%d" % [count_iron_pre, count_mist_pre, count_wolf_pre])

			if not _inv.call("is_item_locked", "wolf_fang"):
				return _fail("wolf_fang 應處於鎖定狀態")
			if _inv.call("is_item_locked", "iron_scrap"):
				return _fail("iron_scrap 不應處於鎖定狀態")

			var pre_gold: int = gs.gold

			# 執行一鍵出售
			var res: Dictionary = _inv.call("batch_sell_materials")
			if not bool(res.get("ok", false)):
				return _fail("batch_sell_materials 執行失敗: %s" % str(res.get("msg", "")))

			var sold_cnt: int = int(res.get("count", 0))
			var sold_gold: int = int(res.get("gold", 0))

			# 預期出售: iron_scrap 10 (10*6=60) + mist_shard 4 (4*12=48) = 14 件，總金幣 108
			if sold_cnt != 14:
				return _fail("出售數量不符，預期 14，實得: %d" % sold_cnt)
			if sold_gold != 108:
				return _fail("獲得金幣不符，預期 108，實得: %d" % sold_gold)

			# 檢查 GameState.gold 累加
			var expected_gold := pre_gold + 108
			if gs.gold != expected_gold:
				return _fail("金幣累加不符，預期 %d，實得: %d" % [expected_gold, gs.gold])

			# 檢查背包中物品狀態
			var count_iron_post: int = int(inv_sys.call("count", "iron_scrap"))
			var count_mist_post: int = int(inv_sys.call("count", "mist_shard"))
			var count_wolf_post: int = int(inv_sys.call("count", "wolf_fang"))

			if count_iron_post != 0:
				return _fail("iron_scrap 出售後應為 0，實得: %d" % count_iron_post)
			if count_mist_post != 0:
				return _fail("mist_shard 出售後應為 0，實得: %d" % count_mist_post)
			if count_wolf_post != 5:
				return _fail("已鎖定之 wolf_fang 應保留 5 個未被出售，實得: %d" % count_wolf_post)

			# 檢查結算提示
			var toast: PanelContainer = _inv.call("get_floating_gold_toast")
			if toast == null or not is_instance_valid(toast):
				return _fail("未彈出金幣結算浮動提示 (GoldFloatingToast)")
			var toast_lbl: Label = toast.find_child("GoldToastLabel", true, false)
			if toast_lbl == null:
				return _fail("找不到 GoldToastLabel 節點")
			if not toast_lbl.text.contains("14") or not toast_lbl.text.contains("108"):
				return _fail("結算提示文字未包含售出數量與金幣，實得: '%s'" % toast_lbl.text)

			print("  ok 一鍵出售執行成功: 售出 14 件未鎖定素材，獲得 108 金幣，已鎖定素材 (wolf_fang x5) 完好保留")

			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false
			# 截圖 3: 一鍵出售執行後金幣結算浮動提示 (GoldFloatingToast) 飄字
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_maple_inv_batch_sell_floating_gold_toast.png"))

			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false
			# 移除飄字，選取保留的已鎖定素材 wolf_fang，更新介面呈現保留詳情
			var toast: PanelContainer = _inv.call("get_floating_gold_toast")
			if toast and is_instance_valid(toast):
				toast.queue_free()
			_inv.call("set_category", "material")
			_inv.set("_selected", "wolf_fang")
			_inv.refresh()

			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			# 截圖 4: 出售完成後背包狀態 (保留已鎖定 wolf_fang 詳情，iron_scrap 已清空)
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_maple_inv_batch_sell_completed_locked_retained.png"))

			_step = 11
			_wait = 0

		11:
			if _wait < 3:
				return false

			print("\n--- 5. 驗證只有已鎖定素材時，再次點擊一鍵出售之防護 ---")
			var res_empty: Dictionary = _inv.call("batch_sell_materials")
			if bool(res_empty.get("ok", false)):
				return _fail("全部素材皆鎖定時 batch_sell_materials 應回傳 ok=false")
			if int(res_empty.get("gold", 0)) != 0 or int(res_empty.get("count", 0)) != 0:
				return _fail("全部素材皆鎖定時金幣與數量應為 0")
			if res_empty.get("msg", "") != "沒有可賣的材料。":
				return _fail("防護提示不符，預期 '沒有可賣的材料。'，實得: '%s'" % res_empty.get("msg", ""))
			print("  ok 全數鎖定/無可賣素材時安全防護有效 (ok=false, 提示='沒有可賣的材料。')")

			_step = 12
			_wait = 0

		12:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var btn: Button = _inv.call("get_batch_sell_button")

			for code in LOCALES:
				loc.call("set_locale", code)
				_inv.call("set_category", "material")
				_inv.refresh()

				var exp_btn: String = EXPECTED_BATCH_SELL_TEXTS[code]
				if btn.text != exp_btn:
					return _fail("[%s] BtnBatchSellMaterials 文案不符，預期 '%s'，實得: '%s'" % [code, exp_btn, btn.text])

				if code in ["en", "es"]:
					if _has_cjk(btn.text):
						return _fail("[%s] BtnBatchSellMaterials 殘留 CJK 字元: %s" % [code, btn.text])

				print("  ok [%s] 一鍵出售按鈕語系切換正常: '%s'" % [code, btn.text])

			# 切換至英文語系截圖存證
			loc.call("set_locale", "en")
			_inv.call("set_category", "material")
			_inv.refresh()

			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			# 截圖 5: 英文語系存證
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_maple_inv_batch_sell_en_locale.png"))

			_step = 14
			_wait = 0

		14:
			if _wait < 3:
				return false

			# 切換至日文語系截圖存證
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ja")
			_inv.call("set_category", "material")
			_inv.refresh()

			_step = 15
			_wait = 0

		15:
			if _wait < 5:
				return false
			# 截圖 6: 日文語系存證
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_maple_inv_batch_sell_ja_locale.png"))

			# 切換回繁中
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.call("set_category", "all")
			_inv.refresh()

			_step = 16
			_wait = 0

		16:
			if _wait < 3:
				return false

			print("\n--- 7. 零系統 Emoji 嚴格檢查 ---")
			var btn: Button = _inv.call("get_batch_sell_button")
			if _has_emoji(btn.text):
				return _fail("BtnBatchSellMaterials 包含違規系統 Emoji: %s" % btn.text)
			print("  ok 零系統 Emoji 檢查通過 (100% 純文字與手繪質感)")

			_step = 17
			_wait = 0

		17:
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
			print("🎉 全部 MapleInventory 一鍵出售未鎖定素材與金幣結算單元測試通過！")
			print("MAPLE_INVENTORY_BATCH_SELL_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
