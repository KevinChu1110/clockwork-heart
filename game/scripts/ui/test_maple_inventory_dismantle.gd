extends SceneTree
## 《發條之心》探索背包裝備拆解回收與安全防護單元測試 (test_maple_inventory_dismantle.gd)
## 驗證項目：
## 1. 按鈕規格與樣式：
##    - 多巴胺珊瑚粉果凍厚底按鈕 (COLOR_PINK #FF5E8A, border #1F1A3A)
##    - 按鈕熱區高度 >= 48px (實際 52px)，果凍厚底 5px，圓角 18px，字級 18px (>= 16px)
## 2. 非裝備道具與未選取狀態：
##    - 未選取時拆解按鈕隱藏 (visible=false)
##    - 選取消耗品 (hp_s) 與素材 (iron_scrap) 維持原快捷欄按鈕 (visible=true, disabled=false, 文案=『放到快捷欄』)，拆解按鈕隱藏
## 3. 未穿戴未鎖定裝備 (rusty_blade)：
##    - 提供『拆解回收』按鈕 (visible=true, disabled=false)
##    - 快捷欄按鈕隱藏 (visible=false)
## 4. 防誤拆安全保護：
##    - 已鎖定裝備 (ash_mail)：按鈕置灰 (disabled=true)，文案顯示『已鎖定無法拆解』，阻擋拆解
##    - 已穿戴裝備 (meager_edge)：按鈕置灰 (disabled=true)，文案顯示『已穿戴無法拆解』，阻擋拆解
## 5. 拆解成功與寶石安全返還：
##    - 拆解鑲嵌紅寶石之裝備，獲得鐵屑與金幣，寶石安全返還至 GemSystem，裝備自背包成功移除
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、零系統 Emoji
## 7. 實機截圖存證至 proofs/t_783e312b/，包含 DisplayServer.get_name() != "headless" 防護與 SHA256 驗證

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _gem_blade_uid: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_783e312b")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_DISMANTLE_FAIL: ", msg)
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

			print("--- 1. 初始化測試環境與道具裝備 ---")
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

			# 加入測試道具
			inv_sys.call("add_item", "rusty_blade", 1)  # 武器 (未穿戴、未鎖定)
			inv_sys.call("add_item", "ash_mail", 1)     # 防具 (將設為鎖定)
			inv_sys.call("add_item", "meager_edge", 1)  # 武器 (將設為穿戴中)
			inv_sys.call("add_item", "hp_s", 5)         # 消耗品
			inv_sys.call("add_item", "iron_scrap", 10)  # 素材
			inv_sys.call("add_item", "key_rusty", 1)    # 重要道具

			# 穿戴 meager_edge
			gs.equip_worn["w_meager"] = {
				"uid": "w_meager",
				"base_id": "meager_edge",
				"name": "微光刃",
				"slot": "weapon",
				"rolled": {"atk": 10.0}
			}
			gs.weapon_loadout[0] = "meager_edge"
			gs.equip_slots["weapon"] = "meager_edge"

			# 鎖定 ash_mail
			eq_sys.call("set_locked", "ash_mail", true)

			# 確保 rusty_blade 未鎖定未穿戴
			eq_sys.call("set_locked", "rusty_blade", false)

			# 建立一把鑲嵌紅寶石 Lv.1 的裝備加入 equip_bag
			var gem_w: Dictionary = eq_sys.call("roll_instance", "rusty_blade", "fine") as Dictionary
			_gem_blade_uid = str(gem_w.get("uid", "gem_blade_test_01"))
			gem_w["uid"] = _gem_blade_uid
			gem_w["name"] = "赤紅發條短劍"
			gem_w["gem"] = {"color": "red", "level": 1}
			eq_sys.call("add_to_bag", gem_w)
			eq_sys.call("set_locked", _gem_blade_uid, false)

			_inv.refresh()
			print("  ok 道具與裝備初始化完成 (rusty_blade, ash_mail, meager_edge, hp_s, iron_scrap, %s)" % _gem_blade_uid)

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證拆解回收按鈕基本規格與多巴胺果凍樣式 ---")
			var btn: Button = _inv.call("get_dismantle_button")
			if btn == null or not is_instance_valid(btn):
				return _fail("找不到拆解回收按鈕 (get_dismantle_button)")

			if btn.custom_minimum_size.y < 48.0:
				return _fail("按鈕熱區高度小於 48px，實際為: %f" % btn.custom_minimum_size.y)
			print("  ok 按鈕熱區高度符合手遊人體工學: %.1f px (>= 48px)" % btn.custom_minimum_size.y)

			var font_size: int = btn.get_theme_font_size("font_size")
			if font_size < 16:
				return _fail("按鈕字級小於 16px，實際為: %d" % font_size)
			print("  ok 按鈕字級符合規範: %d px (>= 16px)" % font_size)

			var sb = btn.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("按鈕 normal 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if sbf.border_width_bottom != 5 or sbf.corner_radius_top_left != 18:
				return _fail("按鈕果凍立體厚底 (5px) 或圓角 (18px) 不符，實得: bottom=%d, radius=%d" % [sbf.border_width_bottom, sbf.corner_radius_top_left])
			if sbf.bg_color != Color("#FF5E8A"):
				return _fail("按鈕底色非多巴胺珊瑚粉 (#FF5E8A)，實得: %s" % sbf.bg_color.to_html())
			print("  ok 按鈕樣式符合規範 (珊瑚粉 #FF5E8A, 果凍厚底 5px, 圓角 18px)")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 驗證未選取狀態 ---")
			var btn: Button = _inv.call("get_dismantle_button")
			_inv.set("_selected", "")
			_inv.refresh()

			if btn.visible:
				return _fail("未選取道具時拆解按鈕應為隱藏 (visible=false)")
			var hb_btn: Button = null
			for child in _inv.find_children("*", "Button", true, false):
				if child.text == "放到快捷欄":
					hb_btn = child
					break
			if hb_btn != null:
				if not hb_btn.visible:
					return _fail("未選取狀態下快捷欄按鈕應為可見")
				if not hb_btn.disabled:
					return _fail("未選取狀態下快捷欄按鈕應為置灰 (disabled=true)")
			print("  ok 未選取狀態正確 (拆解按鈕隱藏，快捷欄按鈕置灰)")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證消耗品與素材選取時維持原有快捷欄行為 ---")
			var btn: Button = _inv.call("get_dismantle_button")

			# 4.1 消耗品 (hp_s)
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if btn.visible:
				return _fail("選取消耗品時拆解按鈕應隱藏 (visible=false)")
			var hb_btn: Button = null
			for child in _inv.find_children("*", "Button", true, false):
				if child.text == "放到快捷欄":
					hb_btn = child
					break
			if hb_btn == null or not hb_btn.visible or hb_btn.disabled:
				return _fail("選取消耗品時快捷欄按鈕應為可見且啟用 (visible=true, disabled=false)")
			print("  ok 消耗品選取時維持快捷欄按鈕啟用，拆解按鈕隱藏")

			# 4.2 素材 (iron_scrap)
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if btn.visible:
				return _fail("選取素材時拆解按鈕應隱藏 (visible=false)")
			if hb_btn == null or not hb_btn.visible or hb_btn.disabled:
				return _fail("選取素材時快捷欄按鈕應為可見且啟用 (visible=true, disabled=false)")
			print("  ok 素材選取時維持快捷欄按鈕啟用，拆解按鈕隱藏")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			print("\n--- 5. 驗證選取未穿戴且未鎖定裝備 (rusty_blade) 之『拆解回收』啟用狀態 ---")
			var btn: Button = _inv.call("get_dismantle_button")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			if not btn.visible:
				return _fail("選取裝備時拆解按鈕應為可見 (visible=true)")
			if btn.disabled:
				return _fail("未穿戴未鎖定裝備拆解按鈕不應被置灰 (disabled=false)")
			if btn.text != "拆解回收":
				return _fail("未穿戴未鎖定裝備按鈕文案應為『拆解回收』，實得: '%s'" % btn.text)

			# 檢查快捷欄按鈕在此時隱藏
			for child in _inv.find_children("*", "Button", true, false):
				if child != btn and (child.name.contains("hb") or child.tooltip_text.contains("快捷") or child.text == "放到快捷欄"):
					if child.visible:
						return _fail("選取裝備時快捷欄按鈕應隱藏 (visible=false)")

			print("  ok 選取未穿戴未鎖定裝備正確提供『拆解回收』啟用按鈕")
			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			_proof_hashes["ready"] = _capture_save(_out_dir.path_join("proof_01_dismantle_ready.png"))
			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證已鎖定防誤拆安全保護 (ash_mail) ---")
			var btn: Button = _inv.call("get_dismantle_button")
			_inv.set("_selected", "ash_mail")
			_inv.refresh()

			if not btn.visible:
				return _fail("選取已鎖定裝備時拆解按鈕應為可見")
			if not btn.disabled:
				return _fail("選取已鎖定裝備時拆解按鈕應置灰 (disabled=true)")
			if btn.text != "已鎖定無法拆解":
				return _fail("已鎖定裝備拆解按鈕文案應為『已鎖定無法拆解』，實得: '%s'" % btn.text)

			# 測試阻擋
			var res_block: Dictionary = _inv.call("dismantle_selected")
			if bool(res_block.get("ok", false)):
				return _fail("已鎖定裝備呼叫 dismantle_selected 應被阻擋，但回傳 ok=true")
			print("  ok 已鎖定防誤拆保護生效: disabled=true, 文案='已鎖定無法拆解', 阻擋執行")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			_proof_hashes["locked"] = _capture_save(_out_dir.path_join("proof_02_dismantle_locked_protected.png"))
			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證已穿戴防誤拆安全保護 (meager_edge) ---")
			var btn: Button = _inv.call("get_dismantle_button")
			_inv.set("_selected", "meager_edge")
			_inv.refresh()

			if not btn.visible:
				return _fail("選取已穿戴裝備時拆解按鈕應為可見")
			if not btn.disabled:
				return _fail("選取已穿戴裝備時拆解按鈕應置灰 (disabled=true)")
			if btn.text != "已穿戴無法拆解":
				return _fail("已穿戴裝備拆解按鈕文案應為『已穿戴無法拆解』，實得: '%s'" % btn.text)

			# 測試阻擋
			var res_block: Dictionary = _inv.call("dismantle_selected")
			if bool(res_block.get("ok", false)):
				return _fail("已穿戴裝備呼叫 dismantle_selected 應被阻擋，但回傳 ok=true")
			print("  ok 已穿戴防誤拆保護生效: disabled=true, 文案='已穿戴無法拆解', 阻擋執行")
			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			_proof_hashes["equipped"] = _capture_save(_out_dir.path_join("proof_03_dismantle_equipped_protected.png"))
			_step = 11
			_wait = 0

		11:
			if _wait < 3:
				return false

			print("\n--- 8. 驗證鎖定/解鎖動態切換時拆解按鈕狀態即時連動 ---")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var btn: Button = _inv.call("get_dismantle_button")

			# 解鎖 ash_mail
			eq_sys.call("set_locked", "ash_mail", false)
			_inv.refresh()
			_inv.set("_selected", "ash_mail")
			_inv.refresh()

			if btn.disabled or btn.text != "拆解回收":
				return _fail("解鎖後 ash_mail 拆解按鈕應解除置灰並顯示『拆解回收』，實得: disabled=%s, text=%s" % [btn.disabled, btn.text])
			print("  ok 解鎖後按鈕即時恢復啟用 (disabled=false, 文案='拆解回收')")

			# 重新鎖定 ash_mail
			eq_sys.call("set_locked", "ash_mail", true)
			_inv.refresh()
			_inv.set("_selected", "ash_mail")
			_inv.refresh()

			if not btn.disabled or btn.text != "已鎖定無法拆解":
				return _fail("重新鎖定後 ash_mail 拆解按鈕應即時置灰並顯示『已鎖定無法拆解』")
			print("  ok 重新鎖定後按鈕即時置灰 (disabled=true, 文案='已鎖定無法拆解')")

			_step = 12
			_wait = 0

		12:
			if _wait < 3:
				return false

			print("\n--- 9. 驗證拆解成功、鐵屑與金幣產出、鑲嵌寶石安全返還 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var gem_sys: Node = root.get_node_or_null("GemSystem")

			var init_scrap: int = int(inv_sys.call("count", "iron_scrap"))
			var init_gold: int = int(gs.get("gold"))
			var init_gems: int = int(gem_sys.call("count_of", "red", 1)) if gem_sys else 0

			_inv.set("_selected", _gem_blade_uid)
			_inv.refresh()

			var btn: Button = _inv.call("get_dismantle_button")
			if btn.disabled:
				return _fail("待拆解之鑲寶裝備 %s 拆解按鈕應為啟用狀態" % _gem_blade_uid)

			var res: Dictionary = _inv.call("dismantle_selected")
			if not bool(res.get("ok", false)):
				return _fail("執行 dismantle_selected 失敗: %s" % res)

			var new_scrap: int = int(inv_sys.call("count", "iron_scrap"))
			var new_gold: int = int(gs.get("gold"))
			var new_gems: int = int(gem_sys.call("count_of", "red", 1)) if gem_sys else 0

			if new_scrap <= init_scrap:
				return _fail("拆解後鐵屑未增加: 初始=%d, 拆解後=%d" % [init_scrap, new_scrap])
			if new_gold < init_gold:
				return _fail("拆解後金幣異常減少")
			if new_gems != init_gems + 1:
				return _fail("拆解後鑲嵌寶石未安全返還: 初始=%d, 返還後=%d (應為 %d)" % [init_gems, new_gems, init_gems + 1])

			# 驗證裝備自背包移除
			var chk_inst: Dictionary = eq_sys.call("find_bag", _gem_blade_uid) as Dictionary
			if not chk_inst.is_empty():
				return _fail("拆解後裝備仍殘留在 equip_bag")

			print("  ok 拆解成功！獲得鐵屑 +%d (總計 %d)、金幣 (總計 %d)、安全返還紅寶石 Lv.1 (總計 %d)" % [
				new_scrap - init_scrap, new_scrap, new_gold, new_gems
			])
			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			_proof_hashes["success"] = _capture_save(_out_dir.path_join("proof_04_dismantle_success_and_refund.png"))
			_step = 14
			_wait = 0

		14:
			if _wait < 3:
				return false

			print("\n--- 10. 驗證拆解普通背包裝備 (rusty_blade) 並同步移除 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			var res_plain: Dictionary = _inv.call("dismantle_selected")
			if not bool(res_plain.get("ok", false)):
				return _fail("拆解 rusty_blade 失敗: %s" % res_plain)
			if bool(inv_sys.call("has_item", "rusty_blade", 1)):
				return _fail("拆解後 rusty_blade 仍殘留在 InventorySystem")
			print("  ok 普通裝備 rusty_blade 拆解成功並自 InventorySystem 乾淨移除")

			_step = 15
			_wait = 0

		15:
			if _wait < 3:
				return false

			print("\n--- 11. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var btn: Button = _inv.call("get_dismantle_button")

			# 重新加入測試武器供六語系檢查
			inv_sys.call("add_item", "rusty_blade", 1)
			eq_sys.call("set_locked", "rusty_blade", false)

			var lang_checks: Dictionary = {
				"zh_TW": {
					"ready": "拆解回收",
					"locked": "已鎖定無法拆解",
					"worn": "已穿戴無法拆解"
				},
				"zh_CN": {
					"ready": "拆解回收",
					"locked": "已锁定无法拆解",
					"worn": "已穿戴无法拆解"
				},
				"en": {
					"ready": "Dismantle",
					"locked": "Locked (Cannot Dismantle)",
					"worn": "Equipped (Cannot Dismantle)"
				},
				"ja": {
					"ready": "分解回収",
					"locked": "ロック中（分解不可）",
					"worn": "装備中（分解不可）"
				},
				"ko": {
					"ready": "분해 회수",
					"locked": "잠금 중（분해 불가）",
					"worn": "장착 중（분해 불가）"
				},
				"es": {
					"ready": "Desmantelar",
					"locked": "Bloqueado (No Desmantelar)",
					"worn": "Equipado (No Desmantelar)"
				}
			}

			for l in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
				loc.call("set_locale", l)
				_inv.refresh()

				# 1. 測試未穿戴未鎖定文案
				_inv.set("_selected", "rusty_blade")
				_inv.refresh()
				var exp_ready: String = lang_checks[l]["ready"]
				if btn.text != exp_ready:
					return _fail("[%s] 未鎖定拆解文案不符: 預期='%s', 實得='%s'" % [l, exp_ready, btn.text])

				# 2. 測試已鎖定文案
				_inv.set("_selected", "ash_mail")
				_inv.refresh()
				var exp_locked: String = lang_checks[l]["locked"]
				if btn.text != exp_locked:
					return _fail("[%s] 已鎖定拆解文案不符: 預期='%s', 實得='%s'" % [l, exp_locked, btn.text])

				# 3. 測試已穿戴文案
				_inv.set("_selected", "meager_edge")
				_inv.refresh()
				var exp_worn: String = lang_checks[l]["worn"]
				if btn.text != exp_worn:
					return _fail("[%s] 已穿戴拆解文案不符: 預期='%s', 實得='%s'" % [l, exp_worn, btn.text])

				# 4. 歐美語系 (en, es) 零 CJK 檢查
				if l in ["en", "es"]:
					var check_list: Array[String] = [btn.text, exp_ready, exp_locked, exp_worn]
					for s: String in check_list:
						for idx: int in s.length():
							var cp: int = s.unicode_at(idx)
							if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
								return _fail("[%s] 歐美語系殘留 CJK 字元: %s" % [l, s[idx]])

				print("  ok [%s] 語系文案完全對齊: ready='%s', locked='%s', worn='%s'" % [l, exp_ready, exp_locked, exp_worn])

			# 在英文語系存證截圖 (選取 rusty_blade)
			loc.call("set_locale", "en")
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			_step = 16
			_wait = 0

		16:
			if _wait < 5:
				return false
			_proof_hashes["en"] = _capture_save(_out_dir.path_join("proof_05_dismantle_i18n_en.png"))

			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()
			_step = 17
			_wait = 0

		17:
			if _wait < 3:
				return false

			print("\n--- 12. 零系統 Emoji 嚴格檢查 ---")
			var all_text := ""
			for lbl in _inv.find_children("*", "Label", true, false):
				if lbl is Label:
					all_text += lbl.text
			for b in _inv.find_children("*", "Button", true, false):
				if b is Button:
					all_text += b.text

			for idx: int in all_text.length():
				var cp: int = all_text.unicode_at(idx)
				if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713):
					return _fail("偵測到違規系統 Emoji: %s (U+%04X)" % [all_text[idx], cp])
			print("  ok 零系統 Emoji 檢查通過 (100% 純文字與手繪質感)")

			_step = 18
			_wait = 0

		18:
			if _wait < 3:
				return false

			print("\n--- 13. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var h_ready: String = _proof_hashes.get("ready", "")
				var h_locked: String = _proof_hashes.get("locked", "")
				var h_equipped: String = _proof_hashes.get("equipped", "")
				var h_success: String = _proof_hashes.get("success", "")
				var h_en: String = _proof_hashes.get("en", "")

				if h_ready == h_locked:
					return _fail("截圖 ready 與 locked SHA256 不得相同")
				if h_locked == h_equipped:
					return _fail("截圖 locked 與 equipped SHA256 不得相同")
				if h_equipped == h_success:
					return _fail("截圖 equipped 與 success SHA256 不得相同")
				if h_success == h_en:
					return _fail("截圖 success 與 en SHA256 不得相同")
				print("  ok 所有存證截圖 SHA256 雜湊值全數獨立不重複")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 裝備拆解回收與安全防護單元測試通過！")
			print("MAPLE_INVENTORY_DISMANTLE_OK")
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
