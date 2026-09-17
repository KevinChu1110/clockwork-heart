extends SceneTree
## 背包物品欄多巴胺 UI 測試
## 驗證項目：
## 1. 彈窗寬度在 740~760px 範圍內
## 2. 右上關閉按鈕尺寸 >= 50px
## 3. 主要操作按鈕高度 >= 50px
## 4. 24 格 (4x6) 物品欄配置
## 5. 全程 0 系統 emoji
## 6. 格子選取與明細連動

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step := 0
var _wait := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_FAIL: ", msg)
	quit(1)
	return true


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
			## 1. 驗證彈窗寬度 (740~760px)
			var card: PanelContainer = _inv.get_node_or_null("%InventoryCard") if _inv.has_node("%InventoryCard") else _inv.find_child("InventoryCard", true, false)
			if card == null:
				return _fail("找不到 InventoryCard 節點")
			var card_w := card.custom_minimum_size.x
			if card_w < 740.0 or card_w > 760.0:
				return _fail("彈窗寬度不符合 740~760px 規範，實際為: %f" % card_w)
			print("  ok 彈窗寬度符合規範: %f px" % card_w)

			## 2. 驗證右上關閉按鈕
			var close_btn: Button = _inv.find_child("CloseButton", true, false)
			if close_btn == null:
				return _fail("找不到 CloseButton 節點")
			if close_btn.custom_minimum_size.x < 50.0 or close_btn.custom_minimum_size.y < 50.0:
				return _fail("關閉按鈕尺寸小於 50px: %s" % str(close_btn.custom_minimum_size))
			if close_btn.text != "✕":
				return _fail("關閉按鈕文字應為 ✕，實際為: %s" % close_btn.text)
			print("  ok 關閉按鈕尺寸與符號符合規範: %s" % str(close_btn.custom_minimum_size))

			## 3. 驗證操作按鈕高度 >= 50px
			var use_btn: Button = _inv.get("_use_btn")
			var hb_btn: Button = _inv.get("_hb_btn")
			if use_btn == null or hb_btn == null:
				return _fail("找不到操作按鈕 _use_btn 或 _hb_btn")
			if use_btn.custom_minimum_size.y < 50.0 or hb_btn.custom_minimum_size.y < 50.0:
				return _fail("操作按鈕高度小於 50px")
			print("  ok 操作按鈕高度符合手遊規範: use=%f, hb=%f" % [use_btn.custom_minimum_size.y, hb_btn.custom_minimum_size.y])

			## 4. 驗證格子數量 24 格
			var cells: Array = _inv.get("_cells")
			if cells.size() != 24:
				return _fail("格子數量不為 24 格，實際為: %d" % cells.size())
			print("  ok 格子數量符合 4x6=24 格")

			## 5. 驗證 0 系統 emoji
			var full_text: String = ""
			for node in _inv.find_children("*", "Label", true, false):
				if node is Label:
					full_text += node.text
			for node in _inv.find_children("*", "Button", true, false):
				if node is Button:
					full_text += node.text
			var detail_rt: RichTextLabel = _inv.get("_detail")
			if detail_rt:
				full_text += detail_rt.text

			## 檢查常見 emoji Unicode 區間
			for ch in full_text:
				var cp := ch.unicode_at(0)
				if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713):
					return _fail("偵測到系統 Emoji: %s (U+%04X)" % [ch, cp])
			print("  ok 零系統 Emoji 檢查通過")

			## 6. 驗證 12 款道具圖示存在且能載入 (Texture2D)
			var expected_icons := [
				"antidote", "bread", "dust_crumb", "friendship_key",
				"hp_m", "hp_s", "hunt_core", "iron_scrap",
				"medal", "mist_shard", "windup_fragment", "wolf_fang"
			]
			for item_id in expected_icons:
				var path := "res://assets/icons/items/%s.png" % item_id
				if not ResourceLoader.exists(path):
					return _fail("道具圖示檔案不存在: %s" % path)
				var tex := load(path) as Texture2D
				if tex == null:
					return _fail("道具圖示載入失敗: %s" % path)
				var sz := tex.get_size()
				if sz.x != 64.0 or sz.y != 64.0:
					return _fail("道具圖示尺寸非 64x64: %s (size=%s)" % [path, str(sz)])
			print("  ok 12 款道具圖示全部存在、為 64x64 且可載入")

			## 7. 驗證格子圖示顯示與無圖 fallback
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys:
				inv_sys.call("add_item", "hp_m", 2)     # 有圖
				inv_sys.call("add_item", "star_ore", 3) # 無圖 (glyph: 砂)
				_inv.refresh()

				# 檢查第 0 格 (hp_m，有圖)
				var cell0: PanelContainer = cells[0]
				var ic0: TextureRect = cell0.find_child("Icon", true, false)
				var g0: Label = cell0.find_child("Glyph", true, false)
				if ic0 == null or not ic0.visible:
					return _fail("第 0 格 (hp_m) Icon TextureRect 應為 visible")
				if ic0.texture == null:
					return _fail("第 0 格 (hp_m) Icon TextureRect 缺少 texture")
				if g0 and g0.visible:
					return _fail("第 0 格 (hp_m) 有圖示時 Glyph 不應為 visible")
				print("  ok 格子有圖示道具 (hp_m) 正常顯示 TextureRect，隱藏單字佔位")

				# 檢查第 1 格 (star_ore，無圖)
				var cell1: PanelContainer = cells[1]
				var ic1: TextureRect = cell1.find_child("Icon", true, false)
				var g1: Label = cell1.find_child("Glyph", true, false)
				if ic1 and ic1.visible:
					return _fail("第 1 格 (star_ore) 無圖示時 Icon 不應為 visible")
				if g1 == null or not g1.visible:
					return _fail("第 1 格 (star_ore) 無圖示時 Glyph 應為 visible")
				if g1.text != "砂":
					return _fail("第 1 格 (star_ore) Glyph 應為「砂」，實際為: %s" % g1.text)
				print("  ok 格子無圖示道具 (star_ore) 正常 fallback 至單字 glyph")

				# 8. 驗證詳情卡大圖預覽
				# 選取 hp_m
				_inv.set("_selected", "hp_m")
				_inv.refresh()
				var d_ic: TextureRect = _inv.get("_detail_icon")
				var d_gly: Label = _inv.get("_detail_glyph")
				var d_name: Label = _inv.get("_detail_name")
				if d_ic == null or not d_ic.visible or d_ic.texture == null:
					return _fail("選取 hp_m 時詳情卡大圖預覽 _detail_icon 應為 visible 且有 texture")
				if d_gly and d_gly.visible:
					return _fail("選取 hp_m 時詳情卡 _detail_glyph 不應為 visible")
				if d_name and d_name.text != "中紅水":
					return _fail("選取 hp_m 時詳情卡標題應為「中紅水」，實際為: %s" % d_name.text)
				print("  ok 點選中紅水時詳情卡大圖預覽與標題連動正常")

			## 9. 驗證關閉邏輯
			_inv.close()
			if _inv.visible:
				return _fail("close() 後 visible 仍為 true")
			print("  ok 關閉行為正常")

			print("MAPLE_INVENTORY_OK")
			quit(0)
			return true
	return false
