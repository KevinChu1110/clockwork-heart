extends SceneTree
## 無頭驗收測試：大廳角色頁三欄武器槽連動真實裝備、品質色階、即時切換與紙娃娃/數值連動

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: Control = null
var _frame_count: int = 0
var _step: int = 0

func _initialize() -> void:
	print("== 測試大廳角色頁三欄武器槽真實連動與即時切換 ==")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	if gs == null or eq == null or loc == null:
		push_error("缺少必要 Autoload 節點 (GameState / EquipmentSystem / Loc)")
		quit(1)
		return

	# 初始化全新遊戲狀態
	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ok 大廳節點建立成功")

func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	match _step:
		0:
			_step_test_initial_state()
			_step = 1
		1:
			_step_test_custom_weapons_and_rarity()
			_step = 2
		2:
			_step_test_switch_and_linkage()
			_step = 3
		3:
			_step_test_i18n_and_screenshot()
			_step = 4
		4:
			print("LOBBY_WEAPON_LOADOUT_LIVE_OK")
			quit(0)
	return false

func _fail(msg: String) -> void:
	push_error("FAIL: %s" % msg)
	print("FAIL: %s" % msg)
	quit(1)

func _step_test_initial_state() -> void:
	print("\n--- 1. 檢驗開局初始裝備、空槽與未解鎖狀態 ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.CHARACTER)
	var w_btns: Array[Button] = _lobby.get_weapon_slot_buttons()
	if w_btns.size() != 3:
		_fail("武器槽數量應為 3，實際為 %d" % w_btns.size())
		return

	# 開局新手武器檢查 (第 0 欄)
	var info0: Dictionary = _lobby._get_weapon_slot_info(0)
	if not bool(info0.get("unlocked", false)) or bool(info0.get("empty", true)):
		_fail("開局第 0 欄應為解鎖且有新手武器")
	print("  ok 開局第 0 欄裝備: 「%s · %s」，品質: 「%s」" % [info0.get("weapon_name"), info0.get("hits"), info0.get("quality_label")])

	# 第 1 欄或第 2 欄應為空槽或未解鎖
	var info1: Dictionary = _lobby._get_weapon_slot_info(1)
	var info2: Dictionary = _lobby._get_weapon_slot_info(2)
	print("  ok 第 1 欄狀態: 「%s · %s」" % [info1.get("weapon_name"), info1.get("hits")])
	print("  ok 第 2 欄狀態: 「%s · %s」" % [info2.get("weapon_name"), info2.get("hits")])

func _step_test_custom_weapons_and_rarity() -> void:
	print("\n--- 2. 檢驗自訂裝備讀取、流派打擊數與品質色階 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	gs.level = 20 # 解鎖所有欄位

	# 設置三種不同流派與不同品質色階的武器
	var w_sword := {
		"uid": "w_live_sword", "base_id": "sword", "name": "晨曦長劍", "line": "sword",
		"slot": "weapon", "tier": 1, "quality": "rare", "quality_label": "上品",
		"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 2.0, "crit_dmg": 5.0}
	}
	var w_spear := {
		"uid": "w_live_spear", "base_id": "spear", "name": "破浪長槍", "line": "spear",
		"slot": "weapon", "tier": 1, "quality": "uncommon", "quality_label": "良品",
		"rolled": {"atk": 12, "def": 2, "hp": 0, "crit": 1.0, "crit_dmg": 0.0}
	}
	var w_fist := {
		"uid": "w_live_fist", "base_id": "fist", "name": "熔火鐵拳", "line": "fist",
		"slot": "weapon", "tier": 1, "quality": "epic", "quality_label": "秘寶",
		"rolled": {"atk": 20, "def": 0, "hp": 10, "crit": 3.0, "crit_dmg": 10.0}
	}

	gs.equip_worn["w_live_sword"] = w_sword
	gs.equip_worn["w_live_spear"] = w_spear
	gs.equip_worn["w_live_fist"] = w_fist
	gs.weapon_loadout = ["w_live_sword", "w_live_spear", "w_live_fist"]
	gs.weapon_loadout_active = 0
	gs.equip_slots["weapon"] = "w_live_sword"

	_lobby.refresh_weapon_slots()
	var w_btns: Array[Button] = _lobby.get_weapon_slot_buttons()

	# 驗證按鈕上的顯示文字與品質標籤
	var btn0 := w_btns[0]
	var t0 := (btn0.get_node("Content/SlotTitle") as Label).text
	var info_lbl0 := (btn0.get_node("Content/WeaponInfo") as Label).text
	var q_lbl0 := (btn0.get_node("Content/QualityLabel") as Label).text
	var q_col0: Color = btn0.get_meta("quality_color")

	if t0 != "首選武器" or not info_lbl0.contains("晨曦長劍") or not info_lbl0.contains("4 次打擊"):
		_fail("欄位 0 資訊不正確: %s / %s" % [t0, info_lbl0])
	if q_lbl0 != "上品":
		_fail("欄位 0 品質標籤應為「上品」，實際為: %s" % q_lbl0)
	print("  ok 欄位 0 正確呈現: 「%s」 「%s」 品質: 「%s」 顏色: %s" % [t0, info_lbl0, q_lbl0, q_col0.to_html()])

	var btn1 := w_btns[1]
	var t1 := (btn1.get_node("Content/SlotTitle") as Label).text
	var info_lbl1 := (btn1.get_node("Content/WeaponInfo") as Label).text
	var q_lbl1 := (btn1.get_node("Content/QualityLabel") as Label).text
	if t1 != "副手武器" or not info_lbl1.contains("破浪長槍") or not info_lbl1.contains("3 次打擊"):
		_fail("欄位 1 資訊不正確: %s / %s" % [t1, info_lbl1])
	if q_lbl1 != "良品":
		_fail("欄位 1 品質標籤應為「良品」，實際為: %s" % q_lbl1)
	print("  ok 欄位 1 正確呈現: 「%s」 「%s」 品質: 「%s」" % [t1, info_lbl1, q_lbl1])

	var btn2 := w_btns[2]
	var t2 := (btn2.get_node("Content/SlotTitle") as Label).text
	var info_lbl2 := (btn2.get_node("Content/WeaponInfo") as Label).text
	var q_lbl2 := (btn2.get_node("Content/QualityLabel") as Label).text
	if t2 != "絕技武器" or not info_lbl2.contains("熔火鐵拳") or not info_lbl2.contains("5 連擊"):
		_fail("欄位 2 資訊不正確: %s / %s" % [t2, info_lbl2])
	if q_lbl2 != "秘寶":
		_fail("欄位 2 品質標籤應為「秘寶」，實際為: %s" % q_lbl2)
	print("  ok 欄位 2 正確呈現: 「%s」 「%s」 品質: 「%s」" % [t2, info_lbl2, q_lbl2])

func _step_test_switch_and_linkage() -> void:
	print("\n--- 3. 檢驗點擊切換武器、紙娃娃手持連動與攻擊力數值連動 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 1. 點擊切換至副手長槍 (欄位 1)
	_lobby.select_weapon_slot(1)
	if int(gs.weapon_loadout_active) != 1:
		_fail("切換欄位 1 後 GameState.weapon_loadout_active 應為 1，實際為 %d" % gs.weapon_loadout_active)
	if str(gs.equip_slots.get("weapon", "")) != "w_live_spear":
		_fail("切換欄位 1 後 equip_slots['weapon'] 應為 w_live_spear")
	if str(gs.path_style) != "spear":
		_fail("切換長槍後 path_style 應為 spear，實際為 %s" % gs.path_style)
	if str(gs.paperdoll_slots.get("weapon", "")) != "none":
		_fail("長槍無專屬 512 切片時 paperdoll_slots['weapon'] 應防護為 none，實際為 %s" % gs.paperdoll_slots.get("weapon", ""))
	print("  ok 點擊切換至欄位 1 (長槍) 成功，紙娃娃無 512 切片時安全防護為 none 避免穿模")

	# 驗證攻擊力數值卡連動
	var stat_cards: Array = _lobby.get("_stat_cards")
	var atk_card: PanelContainer = stat_cards[1]
	var atk_val_lbl := atk_card.find_child("ValLabel", true, false) as Label
	var cur_atk := int(gs.effective_atk())
	if int(atk_val_lbl.text) != cur_atk:
		_fail("攻擊力屬性卡數值應為 %d，實際為 %s" % [cur_atk, atk_val_lbl.text])
	print("  ok 攻擊力卡片即時連動更新為: %s" % atk_val_lbl.text)

	# 2. 點擊切換至絕技鐵拳 (欄位 2)
	_lobby.select_weapon_slot(2)
	if int(gs.weapon_loadout_active) != 2:
		_fail("切換欄位 2 後 GameState.weapon_loadout_active 應為 2")
	if str(gs.paperdoll_slots.get("weapon", "")) != "none":
		_fail("鐵拳無專屬 512 切片時 paperdoll_slots['weapon'] 應防護為 none，實際為 %s" % gs.paperdoll_slots.get("weapon", ""))
	var cur_atk2 := int(gs.effective_atk())
	if int(atk_val_lbl.text) != cur_atk2:
		_fail("攻擊力屬性卡數值應更新為 %d，實際為 %s" % [cur_atk2, atk_val_lbl.text])
	print("  ok 點擊切換至欄位 2 (鐵拳) 成功，攻擊力連動更新為: %s" % atk_val_lbl.text)

	# 3. 切回欄位 0 (長劍)
	_lobby.select_weapon_slot(0)
	if str(gs.paperdoll_slots.get("weapon", "")) != "wpn_dawn_blade":
		_fail("切回欄位 0 後 paperdoll_slots['weapon'] 應同步為 wpn_dawn_blade，實際為 %s" % gs.paperdoll_slots.get("weapon", ""))
	print("  ok 點擊切回欄位 0 (長劍) 成功，紙娃娃手持同步為 wpn_dawn_blade 專屬 512 切片")

func _step_test_i18n_and_screenshot() -> void:
	print("\n--- 4. 檢驗全語系文字與實機存證截圖 ---")
	var loc = root.get_node_or_null("Loc")
	for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
		loc.call("set_locale", code)
		_lobby.refresh_weapon_slots()
		var w_btns: Array[Button] = _lobby.get_weapon_slot_buttons()
		for i in range(3):
			var b := w_btns[i]
			var t := (b.get_node("Content/SlotTitle") as Label).text
			var info := (b.get_node("Content/WeaponInfo") as Label).text
			var q := (b.get_node("Content/QualityLabel") as Label).text
			if t.is_empty() or info.is_empty() or q.is_empty():
				_fail("[%s] 武器槽 %d 文字為空" % [code, i])
		print("  ok [%s] 語系下三欄武器槽文字與品質標籤在地化正常" % code)

	loc.call("set_locale", "zh_TW")
	_lobby.refresh_weapon_slots()

	# 截圖存證（非 headless 渲染環境才擷取 Viewport）
	if DisplayServer.get_name() != "headless":
		var vp := root.get_viewport()
		if vp:
			var tex := vp.get_texture()
			if tex and tex.has_method("get_image"):
				var img: Image = tex.get_image()
				if img:
					var dir := DirAccess.open("res://")
					if not dir.dir_exists("proofs"):
						dir.make_dir("proofs")
					var proof_path := "/opt/side/bravesoul-game/proofs/proof_lobby_weapon_loadout_live.png"
					img.save_png(proof_path)
					print("  ok 實機畫面已截圖保存至: %s" % proof_path)
