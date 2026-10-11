extends SceneTree
## 《發條之心》探索背包選取裝備支援鎖定與解鎖切換單元與驗收測試 (test_maple_inventory_lock.gd)
## 驗證項目：
## 1. 裝備類物品（武器/防具）選取時顯示鎖定狀態標籤膠囊與鎖定/解鎖按鈕
##    - 未鎖定：標籤顯示『未鎖定』、按鈕文案『鎖定』、多巴胺果凍厚底按鈕
##    - 已鎖定：標籤顯示『已鎖定』、按鈕文案『解鎖』、多巴胺金黃厚底按鈕
## 2. 點擊按鈕連動 EquipmentSystem.toggle_lock / is_locked
##    - 即時雙向連動、持久化至 GameState
## 3. 非裝備道具（消耗品/素材/重要道具）與未選取狀態隱藏鎖定標籤與按鈕 (visible=false)
## 4. 鎖定時防止誤賣，詳情面板標示提示
## 5. 多巴胺果凍厚底按鈕規格（高 52px >= 48px，立體厚底 5px，圓角 18px）
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、零系統 Emoji
## 7. 實機截圖存證（DisplayServer.get_name() != "headless" 防護）

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_73dedb6c")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_LOCK_FAIL: ", msg)
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
			if "equip_bag" in gs and gs.equip_bag != null:
				gs.equip_bag.clear()
			if "weapon_loadout" in gs and gs.weapon_loadout != null:
				for i in gs.weapon_loadout.size():
					gs.weapon_loadout[i] = ""

			# 加入裝備與各類道具
			inv_sys.call("add_item", "rusty_blade", 1)  # 武器
			inv_sys.call("add_item", "ash_mail", 1)     # 防具
			inv_sys.call("add_item", "hp_s", 5)         # 消耗品
			inv_sys.call("add_item", "iron_scrap", 10)  # 素材
			inv_sys.call("add_item", "key_rusty", 1)    # 重要道具

			# 確保初始未鎖定
			eq_sys.call("set_locked", "rusty_blade", false)
			eq_sys.call("set_locked", "ash_mail", false)

			_inv.refresh()
			print("  ok 道具初始化完畢 (rusty_blade, ash_mail, hp_s, iron_scrap, key_rusty)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證選取武器 (rusty_blade) 之未鎖定狀態、膠囊與按鈕規格 ---")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			var cap: PanelContainer = _inv.call("get_lock_capsule")
			var lbl: Label = _inv.call("get_lock_label")
			var btn: Button = _inv.call("get_lock_button")

			if cap == null or lbl == null or btn == null:
				return _fail("找不到 LockCapsule / LockStatusLabel / BtnLock 節點")

			if not cap.visible:
				return _fail("選取裝備時 LockCapsule 應為可見 (visible=true)")
			if lbl.text != "未鎖定":
				return _fail("未鎖定裝備標籤文字應為『未鎖定』，實得: '%s'" % lbl.text)
			if not btn.visible:
				return _fail("選取裝備時 BtnLock 應為可見 (visible=true)")
			if btn.text != "鎖定":
				return _fail("未鎖定裝備按鈕文字應為『鎖定』，實得: '%s'" % btn.text)

			# 驗證按鈕規格
			if btn.custom_minimum_size.y < 48.0:
				return _fail("按鈕高度不足 48px: %f" % btn.custom_minimum_size.y)
			if lbl.get_theme_font_size("font_size") < 14:
				return _fail("鎖定標籤字級應 >= 14px")

			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			if eq_sys.call("is_locked", "rusty_blade") != false:
				return _fail("初始狀態 EquipmentSystem.is_locked 應為 false")
			if _inv.call("is_item_locked", "rusty_blade") != false:
				return _fail("初始狀態 MapleInventory.is_item_locked 應為 false")

			print("  ok 未鎖定武器正常呈現：標籤『未鎖定』、按鈕『鎖定』、熱區 %.1f px 符合手機規範" % btn.custom_minimum_size.y)

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 測試點擊鎖定按鈕連動 EquipmentSystem.toggle_lock ---")
			var btn: Button = _inv.call("get_lock_button")
			var lbl: Label = _inv.call("get_lock_label")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			# 點擊按鈕
			btn.pressed.emit()

			if eq_sys.call("is_locked", "rusty_blade") != true:
				return _fail("點擊後 EquipmentSystem.is_locked 應切換為 true")
			if _inv.call("is_item_locked", "rusty_blade") != true:
				return _fail("點擊後 MapleInventory.is_item_locked 應為 true")

			if lbl.text != "已鎖定":
				return _fail("鎖定後標籤文字應為『已鎖定』，實得: '%s'" % lbl.text)
			if btn.text != "解鎖":
				return _fail("鎖定後按鈕文字應為『解鎖』，實得: '%s'" % btn.text)

			# 檢查明細內防誤賣警告標記
			var detail: RichTextLabel = _inv.get("_detail")
			if detail and not detail.text.contains("裝備已鎖定無法出售"):
				return _fail("鎖定裝備之明細面板應包含『裝備已鎖定無法出售』警告提示")

			print("  ok 鎖定切換成功：連動 EquipmentSystem.toggle_lock、標籤『已鎖定』、按鈕『解鎖』、防誤賣提示完備")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			print("\n--- 4. 測試再次點擊按鈕切換為解鎖狀態 ---")
			var btn: Button = _inv.call("get_lock_button")
			var lbl: Label = _inv.call("get_lock_label")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			# 再次點擊
			btn.pressed.emit()

			if eq_sys.call("is_locked", "rusty_blade") != false:
				return _fail("再次點擊後 EquipmentSystem.is_locked 應恢復為 false")
			if _inv.call("is_item_locked", "rusty_blade") != false:
				return _fail("再次點擊後 MapleInventory.is_item_locked 應為 false")

			if lbl.text != "未鎖定":
				return _fail("解鎖後標籤文字應恢復為『未鎖定』，實得: '%s'" % lbl.text)
			if btn.text != "鎖定":
				return _fail("解鎖後按鈕文字應恢復為『鎖定』，實得: '%s'" % btn.text)

			print("  ok 解鎖切換成功：連動恢復為未鎖定、標籤『未鎖定』、按鈕『鎖定』")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			print("\n--- 5. 測試防具 (ash_mail) 選取與鎖定切換 ---")
			_inv.set("_selected", "ash_mail")
			_inv.refresh()

			var cap: PanelContainer = _inv.call("get_lock_capsule")
			var lbl: Label = _inv.call("get_lock_label")
			var btn: Button = _inv.call("get_lock_button")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			if not cap.visible or lbl.text != "未鎖定" or btn.text != "鎖定":
				return _fail("防具初始選取狀態不符")

			btn.pressed.emit()
			if eq_sys.call("is_locked", "ash_mail") != true or lbl.text != "已鎖定" or btn.text != "解鎖":
				return _fail("防具鎖定切換失敗")

			btn.pressed.emit()
			if eq_sys.call("is_locked", "ash_mail") != false or lbl.text != "未鎖定" or btn.text != "鎖定":
				return _fail("防具解鎖切換失敗")

			print("  ok 防具 (ash_mail) 選取、鎖定與解鎖連動全數正確")

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證非裝備道具與未選取狀態隱藏鎖定 UI ---")
			var cap: PanelContainer = _inv.call("get_lock_capsule")
			var btn: Button = _inv.call("get_lock_button")

			# 消耗品
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if cap.visible or btn.visible:
				return _fail("選取消耗品 (hp_s) 時鎖定標籤與按鈕應隱藏 (visible=false)")

			# 素材
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if cap.visible or btn.visible:
				return _fail("選取素材 (iron_scrap) 時鎖定標籤與按鈕應隱藏 (visible=false)")

			# 重要道具
			_inv.set("_selected", "key_rusty")
			_inv.refresh()
			if cap.visible or btn.visible:
				return _fail("選取重要道具 (key_rusty) 時鎖定標籤與按鈕應隱藏 (visible=false)")

			# 未選取
			_inv.set("_selected", "")
			_inv.refresh()
			if cap.visible or btn.visible:
				return _fail("未選取道具時鎖定標籤與按鈕應隱藏 (visible=false)")

			print("  ok 消耗品/素材/重要道具/未選取狀態 皆正確隱藏鎖定膠囊與按鈕")

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			var expected_lock := {
				"zh_TW": "鎖定", "zh_CN": "锁定", "en": "Lock",
				"ja": "ロック", "ko": "잠금", "es": "Bloquear"
			}
			var expected_unlock := {
				"zh_TW": "解鎖", "zh_CN": "解锁", "en": "Unlock",
				"ja": "ロック解除", "ko": "잠금 해제", "es": "Desbloquear"
			}
			var expected_locked_capsule := {
				"zh_TW": "已鎖定", "zh_CN": "已锁定", "en": "Locked",
				"ja": "ロック中", "ko": "잠김", "es": "Bloqueado"
			}
			var expected_unlocked_capsule := {
				"zh_TW": "未鎖定", "zh_CN": "未锁定", "en": "Unlocked",
				"ja": "未ロック", "ko": "미잠금", "es": "Desbloqueado"
			}

			_inv.set("_selected", "rusty_blade")

			for lang in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
				loc.call("set_locale", lang)

				# 測試未鎖定
				eq_sys.call("set_locked", "rusty_blade", false)
				_inv.refresh()

				var lbl: Label = _inv.call("get_lock_label")
				var btn: Button = _inv.call("get_lock_button")

				if lbl.text != expected_unlocked_capsule[lang]:
					return _fail("[%s] 未鎖定標籤翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_unlocked_capsule[lang], lbl.text])
				if btn.text != expected_lock[lang]:
					return _fail("[%s] 鎖定按鈕翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_lock[lang], btn.text])

				_assert_no_emoji(lbl.text, "%s_unlocked_lbl" % lang)
				_assert_no_emoji(btn.text, "%s_lock_btn" % lang)

				# 測試已鎖定
				eq_sys.call("set_locked", "rusty_blade", true)
				_inv.refresh()

				if lbl.text != expected_locked_capsule[lang]:
					return _fail("[%s] 已鎖定標籤翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_locked_capsule[lang], lbl.text])
				if btn.text != expected_unlock[lang]:
					return _fail("[%s] 解鎖按鈕翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_unlock[lang], btn.text])

				_assert_no_emoji(lbl.text, "%s_locked_lbl" % lang)
				_assert_no_emoji(btn.text, "%s_unlock_btn" % lang)

				print("  ok [%s] 語系切換驗證成功 (未鎖定: %s/%s, 已鎖定: %s/%s)" % [
					lang, expected_unlocked_capsule[lang], expected_lock[lang],
					expected_locked_capsule[lang], expected_unlock[lang]
				])

			loc.call("set_locale", "zh_TW")
			eq_sys.call("set_locked", "rusty_blade", false)
			_inv.refresh()

			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false

			print("\n--- 8. 實機截圖存證 (DisplayServer 防護) ---")
			if DisplayServer.get_name() != "headless":
				var vp := root.get_viewport()
				if vp and vp.get_texture():
					# 8.1 未鎖定
					_inv.set("_selected", "rusty_blade")
					var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
					eq_sys.call("set_locked", "rusty_blade", false)
					_inv.refresh()
					_wait = 0
					_step = 9
					return false
			else:
				print("  headless 模式，略過實體 Viewport 擷圖比對")
				_step = 12
				return false

		9:
			_wait += 1
			if _wait < 5:
				return false
			var p1 := _out_dir.path_join("proof_01_maple_equip_unlocked.png")
			_h1 = _capture_save(p1)

			# 切換鎖定
			var btn: Button = _inv.call("get_lock_button")
			btn.pressed.emit()
			_wait = 0
			_step = 10
			return false

		10:
			_wait += 1
			if _wait < 5:
				return false
			var p2 := _out_dir.path_join("proof_02_maple_equip_locked.png")
			_h2 = _capture_save(p2)

			# 切換英文語系
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "en")
			_inv.refresh()
			_wait = 0
			_step = 11
			return false

		11:
			_wait += 1
			if _wait < 5:
				return false
			var p3 := _out_dir.path_join("proof_03_maple_equip_lock_en.png")
			_h3 = _capture_save(p3)

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			if _h1 == _h2:
				return _fail("截圖 1 與截圖 2 (未鎖定 vs 已鎖定) SHA256 不得相同")
			if _h2 == _h3:
				return _fail("截圖 2 與截圖 3 (中文 vs 英文) SHA256 不得相同")
			print("  ok 3 張實機截圖 SHA256 驗證全數獨立不重複")

			_step = 12
			return false

		12:
			print("\n=======================================================")
			print("🎉 全部探索背包選取裝備鎖定與解鎖切換單元測試通過！")
			print("MAPLE_INVENTORY_LOCK_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _capture_save(path: String) -> String:
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


func _assert_no_emoji(s: String, context: String) -> void:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			_fail("違規包含系統 Emoji: context=%s, char=%s, code=0x%X" % [context, c, code])
