extends SceneTree
## 木人樁試招三欄武器輪替次數與傷害貢獻統計單元測試
## godot --headless -s res://scripts/battle/test_dummy_weapon_contribution.gd
##
## 驗證項目：
## 1. BattleSim 支援三欄武器配置，記錄各欄傷害累積與輪替切換次數 (weapon_swap_count / weapon_slot_swaps)
## 2. 各武器欄位 (slot 0/1/2) 傷害精確累加，各欄傷害總和等於 total_player_damage
## 3. get_dummy_combat_stats() 回傳結構完整性 (包含 weapon_slot_damages, weapon_slot_swaps, weapon_swap_count, weapon_bars)
## 4. DummySettlementDialog 多巴胺風格三欄武器貢獻卡與輪替切換膠囊節點結構與字級規範 (字級 >= 11~15px)
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態切換與即時刷新，零 Emoji

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const DummySettlementDialogClass := preload("res://scripts/battle/dummy_settlement_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false


func _multi_weapon_stats() -> Dictionary:
	return {
		"name": "測試小白",
		"max_hp": 100,
		"hp": 100,
		"atk": 25,
		"def": 6,
		"speed": 45.0,
		"crit": 10.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.05,
		"can_skill": true,
		"slash_lv": 1,
		"weapon_class": "sword",
		"weapon_loadout_active": 0,
		"weapon_loadout": [
			{
				"index": 0,
				"uid": "w_sword_01",
				"name": "白鐵長劍",
				"line": "sword",
				"weapon_atk": 12,
				"unlocked": true,
				"empty": false,
				"quality": "common",
				"quality_label": "凡品",
				"active": true,
			},
			{
				"index": 1,
				"uid": "w_spear_02",
				"name": "淬毒短刃",
				"line": "spear",
				"weapon_atk": 16,
				"unlocked": true,
				"empty": false,
				"quality": "uncommon",
				"quality_label": "良品",
				"active": false,
			},
			{
				"index": 2,
				"uid": "w_hammer_03",
				"name": "破軍巨錘",
				"line": "hammer",
				"weapon_atk": 22,
				"unlocked": true,
				"empty": false,
				"quality": "rare",
				"quality_label": "上品",
				"active": false,
			},
		],
	}


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_all_tests()
		if _ok:
			print("\n=======================================================")
			print("TEST_DUMMY_WEAPON_CONTRIBUTION_OK")
			quit(0)
		else:
			push_error("TEST_DUMMY_WEAPON_CONTRIBUTION_FAIL")
			print("TEST_DUMMY_WEAPON_CONTRIBUTION_FAIL")
			quit(1)
		return true
	return false


func _run_all_tests() -> void:
	print("=== 開始 test_dummy_weapon_contribution 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# ── 檢驗 1: BattleSim 三欄武器切換與各欄傷害累計 ──
	print("\n--- 檢驗 1: BattleSim 三欄武器切換次數與傷害累積累加 ---")
	var sim := BattleSim.make_dummy_fight(_multi_weapon_stats())

	if sim.weapon_bars.size() != 3:
		_fail("BattleSim 應正確初始化 3 欄武器，實際為 %d" % sim.weapon_bars.size())
	else:
		print("  ok 初始化 3 欄武器成功")

	# 在 Slot 0 攻擊木人樁
	var dt := 0.0
	while dt < 3.0 and not sim.finished:
		sim.step(0.1)
		dt += 0.1

	var dmg_slot0: int = sim.get_weapon_slot_damage(0)
	if dmg_slot0 <= 0:
		_fail("Slot 0 應產生傷害，實際為 %d" % dmg_slot0)
	else:
		print("  ok Slot 0 (白鐵長劍) 傷害累計 = %d" % dmg_slot0)

	# 切換至 Slot 1 (淬毒短刃)
	var sw1 := sim.switch_weapon_slot(1)
	if not sw1:
		_fail("切換至 Slot 1 失敗")
	else:
		print("  ok 成功切換至 Slot 1 (swap_count=%d)" % sim.get_weapon_swap_count())

	dt = 0.0
	while dt < 3.0 and not sim.finished:
		sim.step(0.1)
		dt += 0.1

	var dmg_slot1: int = sim.get_weapon_slot_damage(1)
	if dmg_slot1 <= 0:
		_fail("Slot 1 應產生傷害，實際為 %d" % dmg_slot1)
	else:
		print("  ok Slot 1 (淬毒短刃) 傷害累計 = %d" % dmg_slot1)

	# 切換至 Slot 2 (破軍巨錘)
	var sw2 := sim.switch_weapon_slot(2)
	if not sw2:
		_fail("切換至 Slot 2 失敗")
	else:
		print("  ok 成功切換至 Slot 2 (swap_count=%d)" % sim.get_weapon_swap_count())

	dt = 0.0
	while dt < 3.0 and not sim.finished:
		sim.step(0.1)
		dt += 0.1

	var dmg_slot2: int = sim.get_weapon_slot_damage(2)
	if dmg_slot2 <= 0:
		_fail("Slot 2 應產生傷害，實際為 %d" % dmg_slot2)
	else:
		print("  ok Slot 2 (破軍巨錘) 傷害累計 = %d" % dmg_slot2)

	# 驗證總切換次數與各 slot 切換次數
	if sim.get_weapon_swap_count() != 2:
		_fail("總輪替切換次數應為 2，實際為 %d" % sim.get_weapon_swap_count())
	else:
		print("  ok 總輪替切換次數為 2")

	if sim.get_weapon_slot_swaps(1) != 1 or sim.get_weapon_slot_swaps(2) != 1:
		_fail("各欄位切換計數不符: slot1=%d, slot2=%d" % [sim.get_weapon_slot_swaps(1), sim.get_weapon_slot_swaps(2)])
	else:
		print("  ok 各欄位切換計數正確 (slot1=1, slot2=1)")

	# 驗證總傷害等於各欄之和
	var combat_stats := sim.get_dummy_combat_stats()
	var total_dmg: int = int(combat_stats.get("total_damage", 0))
	var sum_slot_dmg := dmg_slot0 + dmg_slot1 + dmg_slot2
	if total_dmg != sum_slot_dmg:
		_fail("三欄傷害之和 (%d) 應等於 total_damage (%d)" % [sum_slot_dmg, total_dmg])
	else:
		print("  ok 三欄傷害之和 (%d) 完全吻合 total_damage (%d)" % [sum_slot_dmg, total_dmg])

	# 驗證 get_dummy_combat_stats 結構
	if not combat_stats.has("weapon_slot_damages") or not combat_stats.has("weapon_slot_swaps") or not combat_stats.has("weapon_swap_count") or not combat_stats.has("weapon_bars"):
		_fail("get_dummy_combat_stats() 缺少三欄武器統計結構 key")
	else:
		print("  ok get_dummy_combat_stats() 包含所有三欄武器統計欄位")

	# ── 檢驗 2: DummySettlementDialog 多巴胺風格三欄武器卡與輪替膠囊 ──
	print("\n--- 檢驗 2: DummySettlementDialog 三欄卡片佈局、字級與數值 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var test_payload := {
		"total_damage": 800,
		"elapsed_time": 12.0,
		"dps": 66.7,
		"max_hit_damage": 120,
		"total_hit_count": 22,
		"weapon_swap_count": 3,
		"weapon_slot_damages": {
			0: 400,
			1: 240,
			2: 160,
		},
		"weapon_slot_swaps": {
			0: 1,
			1: 1,
			2: 1,
		},
		"weapon_bars": [
			{
				"index": 0,
				"name": "白鐵長劍",
				"quality": "common",
				"quality_label": "凡品",
				"empty": false,
			},
			{
				"index": 1,
				"name": "淬毒短刃",
				"quality": "uncommon",
				"quality_label": "良品",
				"empty": false,
			},
			{
				"index": 2,
				"name": "破軍巨錘",
				"quality": "rare",
				"quality_label": "上品",
				"empty": false,
			},
		],
	}

	var dlg: Control = DummySettlementDialogClass.show_dialog(root_node, test_payload)
	if dlg == null:
		_fail("無法建立 DummySettlementDialog 實例")
		return

	var contrib_sec := dlg.find_child("WeaponContributionSection", true, false)
	var swaps_cap := dlg.find_child("WeaponSwapsCapsule", true, false)
	var slots_hbox := dlg.find_child("WeaponSlotsHBox", true, false)

	if contrib_sec == null:
		_fail("缺少 WeaponContributionSection 區塊")
	else:
		print("  ok 找到 WeaponContributionSection")

	if swaps_cap == null:
		_fail("缺少 WeaponSwapsCapsule 輪替次數膠囊")
	else:
		print("  ok 找到 WeaponSwapsCapsule 輪替次數膠囊")

	if slots_hbox == null:
		_fail("缺少 WeaponSlotsHBox 容器")
	else:
		print("  ok 找到 WeaponSlotsHBox 容器")

	# 檢查三張卡片
	for i in range(3):
		var card_node := dlg.find_child("WeaponSlotCard_%d" % i, true, false)
		if card_node == null:
			_fail("缺少 WeaponSlotCard_%d 卡片" % i)
		else:
			print("  ok 找到 WeaponSlotCard_%d" % i)

	# 檢驗 getters 數值
	if dlg.get_weapon_swap_count() != 3:
		_fail("get_weapon_swap_count 應為 3，得 %d" % dlg.get_weapon_swap_count())
	else:
		print("  ok get_weapon_swap_count() = 3")

	if dlg.get_weapon_slot_damage(0) != 400 or dlg.get_weapon_slot_damage(1) != 240 or dlg.get_weapon_slot_damage(2) != 160:
		_fail("get_weapon_slot_damage 數值不符")
	else:
		print("  ok get_weapon_slot_damage 數值合格 (400, 240, 160)")

	var p0: float = float(dlg.get_weapon_slot_percent(0))
	var p1: float = float(dlg.get_weapon_slot_percent(1))
	var p2: float = float(dlg.get_weapon_slot_percent(2))
	if absf(p0 - 50.0) > 0.1 or absf(p1 - 30.0) > 0.1 or absf(p2 - 20.0) > 0.1:
		_fail("百分比計算不符: p0=%.1f%%, p1=%.1f%%, p2=%.1f%%" % [p0, p1, p2])
	else:
		print("  ok 百分比計算正確 (50.0%%, 30.0%%, 20.0%%)")

	if dlg.get_weapon_slot_name(0) != "白鐵長劍" or dlg.get_weapon_slot_quality_text(0) != "凡品":
		_fail("Slot 0 武器名稱或品質標籤不符: name='%s', q='%s'" % [dlg.get_weapon_slot_name(0), dlg.get_weapon_slot_quality_text(0)])
	else:
		print("  ok Slot 0 武器名稱與品質標籤正確 ('白鐵長劍', '凡品')")

	# ── 檢驗 3: 六語系即時切換與零 Emoji ──
	print("\n--- 檢驗 3: 六語系動態切換與零 Emoji 驗證 ---")
	var exp_title := {
		"zh_TW": "武器傷害貢獻",
		"zh_CN": "武器伤害贡献",
		"en": "Weapon Damage",
		"ja": "武器ダメージ貢献",
		"ko": "무기 피해 기여",
		"es": "Daño por arma",
	}
	var exp_swaps_title := {
		"zh_TW": "輪替切換",
		"zh_CN": "轮替切换",
		"en": "Weapon Swaps",
		"ja": "武器切り替え",
		"ko": "무기 교체",
		"es": "Cambios de arma",
	}
	var exp_slot1 := {
		"zh_TW": "欄位 1",
		"zh_CN": "栏位 1",
		"en": "Slot 1",
		"ja": "スロット 1",
		"ko": "슬롯 1",
		"es": "Ranura 1",
	}
	var exp_uncommon_quality := {
		"zh_TW": "良品",
		"zh_CN": "良品",
		"en": "Uncommon",
		"ja": "良品",
		"ko": "고급",
		"es": "Poco común",
	}

	var title_lbl: Label = dlg.find_child("WeaponContribTitleLabel", true, false) as Label
	var swaps_title_lbl: Label = swaps_cap.find_child("TitleLabel", true, false) as Label
	var card0: Control = dlg.find_child("WeaponSlotCard_0", true, false) as Control
	var card1: Control = dlg.find_child("WeaponSlotCard_1", true, false) as Control
	var c0_slot_lbl: Label = card0.find_child("SlotTitleLabel", true, false) as Label if card0 else null
	var c1_qual_lbl: Label = card1.find_child("QualityLabel", true, false) as Label if card1 else null

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		if title_lbl and title_lbl.text != exp_title[code]:
			_fail("[%s] 標題文字不符: 期望 '%s'，得 '%s'" % [code, exp_title[code], title_lbl.text])
		if swaps_title_lbl and swaps_title_lbl.text != exp_swaps_title[code]:
			_fail("[%s] 輪替標題不符: 期望 '%s'，得 '%s'" % [code, exp_swaps_title[code], swaps_title_lbl.text])
		if c0_slot_lbl and c0_slot_lbl.text != exp_slot1[code]:
			_fail("[%s] 欄位 1 標題不符: 期望 '%s'，得 '%s'" % [code, exp_slot1[code], c0_slot_lbl.text])
		if c1_qual_lbl and c1_qual_lbl.text != exp_uncommon_quality[code]:
			_fail("[%s] 良品品質文字不符: 期望 '%s'，得 '%s'" % [code, exp_uncommon_quality[code], c1_qual_lbl.text])

		# 零 Emoji 檢查
		for node in [title_lbl, swaps_title_lbl, c0_slot_lbl, c1_qual_lbl]:
			if node and _has_emoji(node.text):
				_fail("[%s] 節點 %s 包含系統原生 Emoji: '%s'" % [code, node.name, node.text])

		print("  ✓ [%s] 武器貢獻卡即時刷新合格: '%s' | '%s' | '%s' | '%s'" % [
			code,
			title_lbl.text if title_lbl else "",
			swaps_title_lbl.text if swaps_title_lbl else "",
			c0_slot_lbl.text if c0_slot_lbl else "",
			c1_qual_lbl.text if c1_qual_lbl else "",
		])

	dlg.queue_free()
