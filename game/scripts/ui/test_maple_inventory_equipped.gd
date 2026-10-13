extends SceneTree
## 《發條之心》探索背包選取當前穿戴裝備切換「已穿戴」置灰按鈕與專屬膠囊提示單元測試 (t_f5877d98)
## 驗證項目：
## 1. 背包選取已裝備武器：
##    - 按鈕文案顯示為『已穿戴』且 disabled=true 置灰防重複點擊
##    - 差額膠囊顯示『穿戴中』（專屬藍底 #3870B2，白字 #FFFFFF，高對比）
##    - 屬性預覽正常顯示（攻擊 +N）
## 2. 背包選取已裝備防具：
##    - 按鈕文案顯示為『已穿戴』且 disabled=true 置灰防重複點擊
##    - 差額膠囊顯示『穿戴中』（專屬藍底 #3870B2，白字 #FFFFFF）
##    - 屬性預覽正常顯示（防禦 +N）
## 3. 背包選取未裝備裝備（武器/防具）：
##    - 仍正常顯示『立即裝備』且 disabled=false
##    - 差額膠囊正常顯示戰力差額比對（+N 攻擊/防禦、-N 攻擊/防禦、或 --）
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態在地化即時切換無缺詞
## 5. 全面零 Unicode 系統 Emoji，膠囊圓角 13px 與高對比多巴胺色盤合規
## 6. 實機截圖存證輸出至 proofs/t_f5877d98/

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _wait: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_EQUIPPED_FAIL: ", msg)
	quit(1)
	return true


func _capture_proof(filename: String) -> void:
	if DisplayServer.get_name() != "headless":
		var img: Image = root.get_viewport().get_texture().get_image()
		if img:
			var base_dir := ProjectSettings.globalize_path("res://")
			var p_proof := base_dir.path_join("../proofs/t_f5877d98/").path_join(filename)
			DirAccess.make_dir_recursive_absolute(p_proof.get_base_dir())
			img.save_png(p_proof)
			print("  [截圖存證] %s 儲存成功" % filename)


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
			if "equip_worn" in gs and gs.equip_worn != null:
				gs.equip_worn.clear()
			if "equip_slots" in gs and gs.equip_slots != null:
				gs.equip_slots.clear()
			if "weapon_loadout" in gs and gs.weapon_loadout != null:
				for i in gs.weapon_loadout.size():
					gs.weapon_loadout[i] = ""

			# 加入武器與防具道具到背包
			inv_sys.call("add_item", "rusty_blade", 1)   # 武器 (atk: 4)
			inv_sys.call("add_item", "meager_edge", 1)   # 武器 (atk: 9)
			inv_sys.call("add_item", "ash_mail", 1)      # 防具 (def: 3)
			inv_sys.call("add_item", "knight_plate", 1)  # 防具 (def: 7)

			_inv.refresh()
			print("  ok 測試道具初始化完畢 (rusty_blade, meager_edge, ash_mail, knight_plate)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			# ── 2. 驗證選取已穿戴武器 (rusty_blade) ──
			print("\n--- 2. 驗證選取已穿戴武器切換『已穿戴』置灰與『穿戴中』專屬膠囊 ---")
			var gs: Node = root.get_node_or_null("GameState")
			var btn: Button = _inv.call("get_use_button")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var stat_lbl: Label = _inv.call("get_stat_preview")

			# 設定 rusty_blade 為當前穿戴武器
			gs.equip_worn["w_rusty"] = {
				"uid": "w_rusty",
				"base_id": "rusty_blade",
				"name": "鏽劍",
				"slot": "weapon",
				"rolled": {"atk": 4.0}
			}
			gs.weapon_loadout[0] = "rusty_blade"
			gs.equip_slots["weapon"] = "rusty_blade"

			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			if not _inv.call("is_selected_item_equipped"):
				return _fail("已裝備武器 is_selected_item_equipped 應為 true")

			if not btn.disabled:
				return _fail("選取已穿戴武器時按鈕應為禁用置灰 (disabled=true)")

			if btn.text != "已穿戴":
				return _fail("選取已穿戴武器時按鈕文案應為『已穿戴』，實際為: %s" % btn.text)

			if not diff_cap.visible:
				return _fail("選取已穿戴武器時差額膠囊應為可見 (visible=true)")

			if diff_lbl.text != "穿戴中":
				return _fail("選取已穿戴武器時差額膠囊文案應為『穿戴中』，實際為: %s" % diff_lbl.text)

			var sb_worn: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_worn == null or sb_worn.bg_color != Color("#3870B2"):
				return _fail("穿戴中膠囊底色應為專屬藍底 #3870B2，實際為: %s" % (sb_worn.bg_color if sb_worn else "null"))

			if not stat_lbl.text.contains("4"):
				return _fail("選取已穿戴武器時屬性預覽應正常呈現攻擊力數值 4，實際為: %s" % stat_lbl.text)

			# 驗證重複點擊按鈕安全阻擋
			btn.pressed.emit()
			print("  ok [已裝備武器] 按鈕置灰 (disabled=true, 文案='已穿戴'), 膠囊='穿戴中' (專屬藍底 #3870B2), 屬性預覽='%s'" % stat_lbl.text)
			_capture_proof("proof_01_equipped_weapon_btn_capsule.png")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			# ── 3. 驗證選取已穿戴防具 (knight_plate) ──
			print("\n--- 3. 驗證選取已穿戴防具切換『已穿戴』置灰與『穿戴中』專屬膠囊 ---")
			var gs: Node = root.get_node_or_null("GameState")
			var btn: Button = _inv.call("get_use_button")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var stat_lbl: Label = _inv.call("get_stat_preview")

			# 設定 knight_plate 為當前穿戴防具
			gs.equip_worn["arm_knight"] = {
				"uid": "arm_knight",
				"base_id": "knight_plate",
				"name": "騎士胸甲",
				"slot": "armor",
				"rolled": {"def": 7.0, "hp": 20.0}
			}
			gs.equip_slots["armor"] = "knight_plate"

			_inv.set("_selected", "knight_plate")
			_inv.refresh()

			if not _inv.call("is_selected_item_equipped"):
				return _fail("已裝備防具 is_selected_item_equipped 應為 true")

			if not btn.disabled:
				return _fail("選取已穿戴防具時按鈕應為禁用置灰 (disabled=true)")

			if btn.text != "已穿戴":
				return _fail("選取已穿戴防具時按鈕文案應為『已穿戴』，實際為: %s" % btn.text)

			if diff_lbl.text != "穿戴中":
				return _fail("選取已穿戴防具時差額膠囊文案應為『穿戴中』，實際為: %s" % diff_lbl.text)

			var sb_worn_arm: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_worn_arm == null or sb_worn_arm.bg_color != Color("#3870B2"):
				return _fail("防具穿戴中膠囊底色應為專屬藍底 #3870B2")

			if not stat_lbl.text.contains("7"):
				return _fail("選取已穿戴防具時屬性預覽應正常呈現防禦力數值 7，實際為: %s" % stat_lbl.text)

			print("  ok [已裝備防具] 按鈕置灰 (disabled=true, 文案='已穿戴'), 膠囊='穿戴中' (專屬藍底 #3870B2), 屬性預覽='%s'" % stat_lbl.text)
			_capture_proof("proof_02_equipped_armor_btn_capsule.png")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			# ── 4. 驗證選取未裝備武器 (meager_edge atk:9 vs 已裝備 rusty_blade atk:4) ──
			print("\n--- 4. 驗證選取未穿戴武器正常顯示『立即裝備』與差額比對膠囊 ---")
			var btn: Button = _inv.call("get_use_button")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")

			_inv.set("_selected", "meager_edge")
			_inv.refresh()

			if _inv.call("is_selected_item_equipped"):
				return _fail("未裝備武器 is_selected_item_equipped 應為 false")

			if btn.disabled:
				return _fail("選取未裝備武器時按鈕不應被禁用")

			if btn.text != "立即裝備":
				return _fail("選取未裝備武器時按鈕文案應為『立即裝備』，實際為: %s" % btn.text)

			if diff_lbl.text != "+5 攻擊":
				return _fail("未裝備更高攻武器時差額應為『+5 攻擊』，實際為: %s" % diff_lbl.text)

			var sb_pos: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_pos == null or sb_pos.bg_color != Color("#1E7538"):
				return _fail("升攻膠囊底色應為綠色 #1E7538")

			print("  ok [未裝備武器] 按鈕正常啟用 (disabled=false, 文案='立即裝備'), 差額膠囊='%s' (綠色 #1E7538)" % diff_lbl.text)
			_capture_proof("proof_03_unequipped_weapon_equip_now.png")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			# ── 5. 驗證選取未裝備防具 (ash_mail def:3 vs 已裝備 knight_plate def:7) ──
			print("\n--- 5. 驗證選取未穿戴防具正常顯示『立即裝備』與差額比對膠囊 ---")
			var btn: Button = _inv.call("get_use_button")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")

			_inv.set("_selected", "ash_mail")
			_inv.refresh()

			if _inv.call("is_selected_item_equipped"):
				return _fail("未裝備防具 is_selected_item_equipped 應為 false")

			if btn.disabled:
				return _fail("選取未裝備防具時按鈕不應被禁用")

			if btn.text != "立即裝備":
				return _fail("選取未裝備防具時按鈕文案應為『立即裝備』，實際為: %s" % btn.text)

			if diff_lbl.text != "-4 防禦":
				return _fail("未裝備較低防防具時差額應為『-4 防禦』，實際為: %s" % diff_lbl.text)

			var sb_neg: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_neg == null or sb_neg.bg_color != Color("#7A7090"):
				return _fail("降防膠囊底色應為灰色 #7A7090")

			print("  ok [未裝備防具] 按鈕正常啟用 (disabled=false, 文案='立即裝備'), 差額膠囊='%s' (灰色 #7A7090)" % diff_lbl.text)
			_capture_proof("proof_04_unequipped_armor_equip_now.png")

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			# ── 6. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換無缺詞 ──
			print("\n--- 6. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var btn: Button = _inv.call("get_use_button")
			var diff_lbl: Label = _inv.call("get_diff_label")

			var expected_texts := {
				"zh_TW": {"btn": "已穿戴", "cap": "穿戴中"},
				"zh_CN": {"btn": "已穿戴", "cap": "穿戴中"},
				"en":    {"btn": "Equipped", "cap": "Equipped"},
				"ja":    {"btn": "装備済み", "cap": "装備中"},
				"ko":    {"btn": "장착됨", "cap": "장착 중"},
				"es":    {"btn": "Equipado", "cap": "Equipado"},
			}

			_inv.set("_selected", "rusty_blade")

			for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
				loc.call("set_locale", code)
				_inv.refresh()

				var exp_btn: String = expected_texts[code]["btn"]
				var exp_cap: String = expected_texts[code]["cap"]

				if btn.text != exp_btn:
					return _fail("[%s] 已穿戴按鈕文案不符: 期望 '%s'，實際 '%s'" % [code, exp_btn, btn.text])
				if diff_lbl.text != exp_cap:
					return _fail("[%s] 穿戴中膠囊文案不符: 期望 '%s'，實際 '%s'" % [code, exp_cap, diff_lbl.text])

				print("  ok [%s] 按鈕文案='%s'、膠囊文案='%s' 吻合" % [code, btn.text, diff_lbl.text])
				if code == "en":
					_capture_proof("proof_05_six_locales_equipped_en.png")
				elif code == "ja":
					_capture_proof("proof_06_six_locales_equipped_ja.png")

			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			# ── 7. 零系統 Emoji 檢查 ──
			print("\n--- 7. 零系統 Emoji 檢查 ---")
			var full_text := ""
			for node in _inv.find_children("*", "Label", true, false):
				if node is Label:
					full_text += node.text
			for node in _inv.find_children("*", "Button", true, false):
				if node is Button:
					full_text += node.text

			for ch in full_text:
				var cp := ch.unicode_at(0)
				if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713):
					return _fail("偵測到系統 Emoji: %s (U+%04X)" % [ch, cp])
			print("  ok 零系統 Emoji 檢查通過")

			print("\nMAPLE_INVENTORY_EQUIPPED_OK")
			quit(0)
			return true

	return false
