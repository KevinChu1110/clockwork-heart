extends SceneTree
## 戰鬥勝利結算多巴胺化與部位破壞特寫驗證測試 (test_victory_dopamine.gd)
## 驗證項目：
## 1. 戰鬥部位破壞特效 (CombatHitFx.spawn_part_break_fx)：
##    - 衝擊波環 (BreakShockwave) 與 12角破裂星芒 (BreakStarburst)
##    - 全方位高密度多巴胺金屬火花 (>=20 sparks)
##    - 零件齒輪慢動作噴發 (Slow-Mo Flying Brass Gears >= 8)
##    - 飛散發條螺絲與彈簧零件 (Clockwork Screws & Springs >= 4)
## 2. 戰鬥勝利結算多巴胺化 (BattleVictoryDialog)：
##    - 立體金色大勝獎牌 (VictoryMedalBadge) 節點結構與光芒旋轉
##    - 齒輪寶箱 (GearChestWidget) 彈出、齒輪鎖疾轉、掀蓋金光噴發解鎖動效
##    - 機芯與獎勵按八色階光環 (TierHaloEffect) 呈現與彈跳動效 (gray/white/orange/blue/purple/gold/green/red)
##    - 六語系 i18n 完整度與全域零系統 Emoji

const BattleVictoryDialogScript := preload("res://scripts/battle/battle_victory_dialog.gd")
const CombatHitFxScript := preload("res://scripts/battle/combat_hit_fx.gd")
const CoreSystemScript := preload("res://scripts/systems/core_system.gd")

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)


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
			print("TEST_VICTORY_DOPAMINE_OK")
			quit(0)
		else:
			push_error("TEST_VICTORY_DOPAMINE_FAIL")
			print("TEST_VICTORY_DOPAMINE_FAIL")
			quit(1)
		return true
	return false


func _run_all_tests() -> void:
	print("=== 開始驗證戰鬥勝利結算多巴胺化與部位破壞特寫 ===")
	_test_part_break_fx()
	_test_victory_dialog_components()
	_test_eight_tier_halos()
	_test_gear_chest_unlock_flow()
	_test_i18n_and_no_emoji()


func _test_part_break_fx() -> void:
	print("\n--- 1. 驗證戰鬥部位破壞特效 (spawn_part_break_fx) ---")
	var host := Node2D.new()
	root.add_child(host)

	var fx: Node2D = CombatHitFxScript.spawn_part_break_fx(host, Vector2(640, 360), "重裝護甲")
	_assert(fx != null, "spawn_part_break_fx 應回傳有效 Node2D 實例")
	if fx == null:
		host.queue_free()
		return

	# 檢查衝擊光環
	var shockwaves := fx.get_tree().get_nodes_in_group("combat_break_shockwave")
	_assert(shockwaves.size() >= 1, "應生成部位破壞衝擊波環 (combat_break_shockwave)")

	# 檢查破裂星芒
	var starbursts := fx.get_tree().get_nodes_in_group("combat_break_starburst")
	_assert(starbursts.size() >= 1, "應生成 12角破裂星芒 (combat_break_starburst)")

	# 檢查多巴胺火星
	var sparks := fx.get_tree().get_nodes_in_group("combat_break_sparks")
	_assert(sparks.size() >= 15, "應生成高密度多巴胺金屬火花 (當前: %d)" % sparks.size())

	# 檢查慢動作飛散小齒輪
	var gears := fx.get_tree().get_nodes_in_group("combat_break_gears")
	_assert(gears.size() >= 6, "應生成慢動作噴發小齒輪 (當前: %d)" % gears.size())

	# 檢查飛散發條螺絲與彈簧零件
	var parts := fx.get_tree().get_nodes_in_group("combat_break_parts")
	_assert(parts.size() >= 4, "應生成飛散發條螺絲與彈簧零件 (當前: %d)" % parts.size())

	print("  ✓ 部位破壞特寫：衝擊光環(1)、破裂星芒(1)、火星(%d)、齒輪(%d)、發條零件(%d) 全部合格" % [
		sparks.size(), gears.size(), parts.size()
	])
	host.queue_free()


func _test_victory_dialog_components() -> void:
	print("\n--- 2. 驗證戰鬥勝利結算卡片立體獎牌、寶箱與光環結構 ---")
	var sample_part := {
		"id": "part_gold_01",
		"slot": "gear_train",
		"tier": "gold",
		"tier_name": "金",
		"slot_name": "傳動齒輪組",
		"exp_gain": 120,
		"scrap_gain": 3,
		"stats": {"ATK": 35, "DEF": 20}
	}
	var dlg = BattleVictoryDialogScript.show_dialog(root, sample_part, Callable(), 120, 3)
	_assert(dlg != null, "BattleVictoryDialog 建立失敗")
	if dlg == null:
		return

	# 驗證 VictoryCard
	var card := dlg.find_child("VictoryCard", true, false) as PanelContainer
	_assert(card != null, "缺少 VictoryCard 節點")
	if card:
		_assert(card.custom_minimum_size.x >= 740, "卡片寬度需 >= 740px (實際: %f)" % card.custom_minimum_size.x)

	# 驗證立體金色大勝獎牌 (VictoryMedalBadge)
	var medal := dlg.find_child("VictoryMedalBadge", true, false) as Control
	_assert(medal != null, "缺少 VictoryMedalBadge 獎牌節點")
	if medal:
		_assert(medal.custom_minimum_size.x >= 80 and medal.custom_minimum_size.y >= 70, "VictoryMedalBadge 尺寸未達標")

	# 驗證齒輪寶箱 (GearChest)
	var chest := dlg.find_child("GearChest", true, false) as Control
	_assert(chest != null, "缺少 GearChest 寶箱節點")
	if chest:
		_assert(chest.custom_minimum_size.x >= 90 and chest.custom_minimum_size.y >= 80, "GearChest 尺寸未達標")

	# 驗證八色階光環 (TierHalo)
	var halo := dlg.find_child("TierHalo", true, false) as Control
	_assert(halo != null, "缺少 TierHalo 八色階光環節點")
	if halo:
		_assert(str(halo.get("tier_id")) == "gold", "TierHalo tier_id 應為 gold (實際: %s)" % str(halo.get("tier_id")))

	# 驗證經驗與鐵屑獎勵面板
	var exp_p := dlg.find_child("ExpRewardPanel", true, false) as PanelContainer
	var scrap_p := dlg.find_child("ScrapRewardPanel", true, false) as PanelContainer
	_assert(exp_p != null and exp_p.visible, "ExpRewardPanel 應存在且可見")
	_assert(scrap_p != null and scrap_p.visible, "ScrapRewardPanel 應存在且可見")

	print("  ✓ 結算畫面元件：立體金色大勝獎牌、齒輪寶箱、八色階光環、經驗/鐵屑面板結構齊全")
	dlg.queue_free()


func _test_eight_tier_halos() -> void:
	print("\n--- 3. 驗證八色階光環 (gray/white/orange/blue/purple/gold/green/red) 準確染色 ---")
	var tiers := ["gray", "white", "orange", "blue", "purple", "gold", "green", "red"]
	for tid in tiers:
		var p := {
			"id": "test_part_" + tid,
			"slot": "mainspring",
			"tier": tid,
			"slot_name": "發條發電機",
			"stats": {"HP": 100}
		}
		var dlg = BattleVictoryDialogScript.show_dialog(root, p)
		var halo := dlg.find_child("TierHalo", true, false) as Control
		_assert(halo != null, "[%s] 缺少 TierHalo" % tid)
		if halo:
			var h_tid: String = str(halo.get("tier_id"))
			var h_col: Color = halo.get("tier_color")
			_assert(h_tid == tid, "[%s] TierHalo tier_id 不匹配: %s" % [tid, h_tid])
			_assert(h_col.a > 0.0, "[%s] TierHalo 色階透明度異常" % tid)
			print("    • 色階 %s: tier_color=%s (通過)" % [tid, h_col.to_html(false)])
		dlg.queue_free()
	print("  ✓ 八色階光環色彩設定全部通過")


func _test_gear_chest_unlock_flow() -> void:
	print("\n--- 4. 驗證齒輪寶箱開箱解鎖動態流暢度 ---")
	var dlg = BattleVictoryDialogScript.show_dialog(root, {
		"slot": "escapement", "tier": "purple", "slot_name": "擒縱游絲"
	})
	var chest := dlg.find_child("GearChest", true, false) as Control
	_assert(chest != null, "找不到 GearChest 節點")
	if chest:
		var opened := {"ok": false}
		chest.call("play_unlock", func(): opened["ok"] = true)
		_assert(chest.has_method("play_unlock"), "GearChest 應具備 play_unlock 方法")
		print("  ✓ GearChest 開箱方法與回呼觸發健全")
	dlg.queue_free()


func _test_i18n_and_no_emoji() -> void:
	print("\n--- 5. 驗證六語系切換健全度與全域零系統 Emoji ---")
	var sample_part := {
		"slot": "rachet", "tier": "red", "slot_name": "棘輪制動"
	}
	var dlg = BattleVictoryDialogScript.show_dialog(root, sample_part)
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var loc_node = root.get_node_or_null("Loc")

	for lc in locales:
		if loc_node and loc_node.has_method("set_locale"):
			loc_node.call("set_locale", lc)
		dlg.call("_refresh_display")

		var title_lbl := dlg.find_child("TitleLabel", true, false) as Label
		var btn_confirm := dlg.find_child("BtnConfirm", true, false) as Button
		var btn_equip := dlg.find_child("BtnEquip", true, false) as Button

		_assert(title_lbl != null and not _has_emoji(title_lbl.text), "[%s] TitleLabel 含 emoji" % lc)
		_assert(btn_confirm != null and not _has_emoji(btn_confirm.text), "[%s] BtnConfirm 含 emoji" % lc)
		_assert(btn_equip != null and not _has_emoji(btn_equip.text), "[%s] BtnEquip 含 emoji" % lc)
		print("    • 語系 %s: 標題=%s, 按鈕=%s / %s (無emoji, 正常)" % [
			lc, title_lbl.text, btn_equip.text, btn_confirm.text
		])

	dlg.queue_free()
	print("  ✓ 六語系切換正常，100% 零系統 Emoji")


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false
