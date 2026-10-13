extends SceneTree
## 木人樁試招戰鬥數據統計單元測試 (BattleSim & DummySettlementDialog)
## godot --headless -s res://scripts/battle/test_dummy_combat_stats.gd
##
## 驗證項目：
## 1. BattleSim 在木人樁戰鬥中準確記錄 max_hit_damage 與 total_hit_count
## 2. get_dummy_combat_stats() 回傳結構完整性與數值累計精確性
## 3. DummySettlementDialog 雙膠囊（最高單擊與總命中）節點結構與字級規範 (>=14px)
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態切換與數值保持一致、零 Emoji

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


func _stats() -> Dictionary:
	return {
		"name": "測試小白",
		"max_hp": 100,
		"hp": 100,
		"atk": 25,
		"def": 6,
		"speed": 12.0,
		"crit": 15.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.05,
		"can_skill": true,
		"slash_lv": 1,
		"weapon_class": "sword",
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
			print("TEST_DUMMY_COMBAT_STATS_OK")
			quit(0)
		else:
			push_error("TEST_DUMMY_COMBAT_STATS_FAIL")
			print("TEST_DUMMY_COMBAT_STATS_FAIL")
			quit(1)
		return true
	return false


func _run_all_tests() -> void:
	print("=== 開始 test_dummy_combat_stats 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# ── 檢驗 1: BattleSim 木人樁戰鬥數值累積 ──
	print("\n--- 檢驗 1: BattleSim 數值累計 (max_hit_damage & total_hit_count) ---")
	var sim := BattleSim.make_dummy_fight(_stats())
	var hits_recorded := 0
	var manual_max_dmg := 0
	sim.event.connect(func(kind: String, ev: Dictionary):
		if (kind == "hit" or kind == "skill_hit") and str(ev.get("attacker", "")) == "player":
			var d := int(ev.get("damage", 0))
			if d > 0:
				hits_recorded += 1
				manual_max_dmg = maxi(manual_max_dmg, d)
	)

	# 步進 6 秒
	var total_dt := 0.0
	while total_dt < 6.0 and not sim.finished:
		sim.step(0.1)
		total_dt += 0.1

	var stats := sim.get_dummy_combat_stats()
	var total_dmg := int(stats.get("total_damage", 0))
	var elapsed := float(stats.get("elapsed_time", 0.0))
	var dps := float(stats.get("dps", 0.0))
	var max_hit := int(stats.get("max_hit_damage", 0))
	var total_hits := int(stats.get("total_hit_count", 0))

	if total_dmg <= 0:
		_fail("BattleSim total_damage 應大於 0，得 %d" % total_dmg)
	else:
		print("  ok total_damage = %d" % total_dmg)

	if max_hit <= 0 or max_hit > total_dmg:
		_fail("BattleSim max_hit_damage 應在有效範圍 (0, total_dmg]，得 %d" % max_hit)
	else:
		print("  ok max_hit_damage = %d" % max_hit)

	if total_hits <= 0:
		_fail("BattleSim total_hit_count 應大於 0，得 %d" % total_hits)
	else:
		print("  ok total_hit_count = %d" % total_hits)

	if hits_recorded > 0 and (total_hits != hits_recorded or max_hit != manual_max_dmg):
		_fail("信號監聽比對失敗: sim total_hits=%d vs rec=%d, max_dmg=%d vs manual=%d" % [total_hits, hits_recorded, max_hit, manual_max_dmg])
	else:
		print("  ok 信號事件與統計完全一致 (hits=%d, max_dmg=%d)" % [total_hits, max_hit])

	if not stats.has("weapon_slot_damages") or not stats.has("weapon_swap_count"):
		_fail("stats 缺少 weapon_slot_damages 或 weapon_swap_count")
	else:
		print("  ok stats 包含 weapon_slot_damages 與 weapon_swap_count")

	# ── 檢驗 2: DummySettlementDialog 雙膠囊卡片佈局與字級 ──
	print("\n--- 檢驗 2: DummySettlementDialog 雙膠囊卡片佈局與字級規範 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var test_payload := {
		"total_damage": 640,
		"elapsed_time": 15.0,
		"dps": 42.6,
		"max_hit_damage": 95,
		"total_hit_count": 18,
	}

	var dlg: Control = DummySettlementDialogClass.show_dialog(root_node, test_payload)
	if dlg == null:
		_fail("無法建立 DummySettlementDialog 實例")
		return

	var cap_hbox := dlg.find_child("CapsulesHBox", true, false)
	var max_hit_cap := dlg.find_child("MaxHitCapsule", true, false)
	var hits_cap := dlg.find_child("TotalHitsCapsule", true, false)

	if cap_hbox == null:
		_fail("缺少 CapsulesHBox 容器")
	else:
		print("  ok 找到 CapsulesHBox")

	if max_hit_cap == null or hits_cap == null:
		_fail("缺少 MaxHitCapsule 或 TotalHitsCapsule 膠囊節點")
	else:
		print("  ok 找到 MaxHitCapsule 與 TotalHitsCapsule")

	var cap1_t: Label = max_hit_cap.find_child("TitleLabel", true, false) as Label
	var cap1_v: Label = max_hit_cap.find_child("MaxHitValueLabel", true, false) as Label
	var cap1_u: Label = max_hit_cap.find_child("UnitLabel", true, false) as Label

	var cap2_t: Label = hits_cap.find_child("TitleLabel", true, false) as Label
	var cap2_v: Label = hits_cap.find_child("TotalHitsValueLabel", true, false) as Label
	var cap2_u: Label = hits_cap.find_child("UnitLabel", true, false) as Label

	# 檢查字級 >= 14px
	for lbl in [cap1_t, cap1_u, cap2_t, cap2_u]:
		var fs: int = int(lbl.get_theme_font_size("font_size")) if lbl else 0
		if fs < 14:
			_fail("膠囊標籤字級應 >= 14px，節點 %s 得 %d" % [lbl.name if lbl else "null", fs])
		else:
			print("  ok %s 字級 %dpx >= 14px" % [lbl.name, fs])

	var v1_fs: int = int(cap1_v.get_theme_font_size("font_size")) if cap1_v else 0
	var v2_fs: int = int(cap2_v.get_theme_font_size("font_size")) if cap2_v else 0
	if v1_fs < 18 or v2_fs < 18:
		_fail("數值標籤字級應 >= 18px，得 v1=%d, v2=%d" % [v1_fs, v2_fs])
	else:
		print("  ok 數值標籤字級分別為 %dpx, %dpx (>= 18px)" % [v1_fs, v2_fs])

	# 檢驗 getters
	if dlg.get_max_hit_damage() != 95 or dlg.get_total_hit_count() != 18:
		_fail("getters 數值不符: max=%d, hits=%d" % [dlg.get_max_hit_damage(), dlg.get_total_hit_count()])
	else:
		print("  ok getters 數值正確 (max=95, hits=18)")

	# ── 檢驗 3: 六語系即時切換與零 Emoji ──
	print("\n--- 檢驗 3: 六語系動態切換與零 Emoji 驗證 ---")
	var expected_max := {
		"zh_TW": "最高單擊",
		"zh_CN": "最高单击",
		"en": "Max Hit",
		"ja": "最大単撃",
		"ko": "최고 단타",
		"es": "Golpe máx.",
	}
	var expected_tot := {
		"zh_TW": "總命中次數",
		"zh_CN": "总命中次数",
		"en": "Total Hits",
		"ja": "総命中回数",
		"ko": "총 적중 횟수",
		"es": "Total de impactos",
	}
	var expected_hit_unit := {
		"zh_TW": "次",
		"zh_CN": "次",
		"en": "hits",
		"ja": "回",
		"ko": "회",
		"es": "veces",
	}
	var expected_dmg_unit := {
		"zh_TW": "點",
		"zh_CN": "点",
		"en": "pts",
		"ja": "pt",
		"ko": "점",
		"es": "pts",
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		if cap1_t.text != expected_max[code]:
			_fail("[%s] 最高單擊文字不符: 期望 '%s'，得 '%s'" % [code, expected_max[code], cap1_t.text])
		if cap1_u.text != expected_dmg_unit[code]:
			_fail("[%s] 傷害單位不符: 期望 '%s'，得 '%s'" % [code, expected_dmg_unit[code], cap1_u.text])
		if cap2_t.text != expected_tot[code]:
			_fail("[%s] 總命中文字不符: 期望 '%s'，得 '%s'" % [code, expected_tot[code], cap2_t.text])
		if cap2_u.text != expected_hit_unit[code]:
			_fail("[%s] 命中單位不符: 期望 '%s'，得 '%s'" % [code, expected_hit_unit[code], cap2_u.text])

		if cap1_v.text != "95" or cap2_v.text != "18":
			_fail("[%s] 膠囊數值被切換語系篡改: v1=%s, v2=%s" % [code, cap1_v.text, cap2_v.text])

		for txt in [cap1_t.text, cap1_u.text, cap1_v.text, cap2_t.text, cap2_u.text, cap2_v.text]:
			if _has_emoji(txt):
				_fail("[%s] 膠囊包含系統 Emoji: '%s'" % [code, txt])

		print("  ✓ [%s] 雙膠囊即時刷新合格: '%s %s %s' | '%s %s %s'" % [
			code, cap1_t.text, cap1_v.text, cap1_u.text, cap2_t.text, cap2_v.text, cap2_u.text
		])

	dlg.queue_free()
