extends SceneTree
## Boss 戰失敗能量返還機制與 C0/C1 劇情保護把關測試
## 執行方式：godot --path game --headless -s res://scripts/systems/test_energy_defeat_refund.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var en := root.get_node_or_null("EnergySystem")
	var arena := root.get_node_or_null("ArenaSystem")
	var hunt := root.get_node_or_null("HuntSystem")
	if gs == null or en == null or arena == null or hunt == null:
		_fail("GameState／EnergySystem／ArenaSystem／HuntSystem autoload missing")
		return _finish()

	gs.reset_new_game()
	en.refresh()

	# ─────────────────────────────────────────────────────────────
	# 1. Boss 戰失敗返還測試：扣 3 返還 2，實際只損耗 1 點試錯成本
	# ─────────────────────────────────────────────────────────────
	# (a) 已通關雷歐（重複挑戰收首領價 3 點）
	gs.set_flag("boss.leo_cleared", true)
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_leo: Dictionary = en.try_spend_for_battle("leo")
	if not bool(sp_leo.get("ok", false)) or int(sp_leo.get("cost", 0)) != en.COST_BOSS:
		_fail("已通關雷歐應扣 %d 點，得 %s" % [en.COST_BOSS, str(sp_leo)])
	if int(gs.energy) != 12:
		_fail("扣 3 點後能量應為 12，得 %d" % int(gs.energy))

	var ref_leo: Dictionary = en.refund_on_defeat("leo")
	if int(ref_leo.get("refunded", 0)) != en.REFUND_BOSS_DEFEAT:
		_fail("雷歐失敗應返還 %d 點，得 %s" % [en.REFUND_BOSS_DEFEAT, str(ref_leo)])
	if int(gs.energy) != 14:
		_fail("雷歐失敗返還後能量應為 14（實損 1 點），得 %d" % int(gs.energy))
	print("  ok Boss 戰（已通關雷歐）失敗：扣 3 返 2，實際損耗 1 點 (15 -> 12 -> 14)")

	# (b) 秘境小王（黑鏽疤主 scar_lord，常規首領價 3 點）
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_scar: Dictionary = en.try_spend_for_battle("scar_lord")
	if not bool(sp_scar.get("ok", false)) or int(sp_scar.get("cost", 0)) != en.COST_BOSS:
		_fail("秘境小王 scar_lord 應扣 %d 點，得 %s" % [en.COST_BOSS, str(sp_scar)])
	if int(gs.energy) != 12:
		_fail("扣 3 點後能量應為 12，得 %d" % int(gs.energy))

	var ref_scar: Dictionary = en.refund_on_defeat("scar_lord")
	if int(ref_scar.get("refunded", 0)) != en.REFUND_BOSS_DEFEAT:
		_fail("秘境小王失敗應返還 %d 點，得 %s" % [en.REFUND_BOSS_DEFEAT, str(ref_scar)])
	if int(gs.energy) != 14:
		_fail("秘境小王失敗返還後能量應為 14（實損 1 點），得 %d" % int(gs.energy))
	print("  ok Boss 戰（秘境小王）失敗：扣 3 返 2，實際損耗 1 點 (15 -> 12 -> 14)")

	# ─────────────────────────────────────────────────────────────
	# 2. 一般怪（可重複農怪關卡）失敗：扣 1 點維持不變、不返還
	# ─────────────────────────────────────────────────────────────
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_mob: Dictionary = en.try_spend_for_battle("ash_rat")
	if not bool(sp_mob.get("ok", false)) or int(sp_mob.get("cost", 0)) != en.COST_MOB:
		_fail("一般怪 ash_rat 應扣 %d 點，得 %s" % [en.COST_MOB, str(sp_mob)])
	if int(gs.energy) != 14:
		_fail("扣 1 點後能量應為 14，得 %d" % int(gs.energy))

	var ref_mob: Dictionary = en.refund_on_defeat("ash_rat")
	if int(ref_mob.get("refunded", 0)) != 0:
		_fail("一般怪失敗不應返還，得 %s" % str(ref_mob))
	if int(gs.energy) != 14:
		_fail("一般怪失敗後能量應維持 14（實損 1 點），得 %d" % int(gs.energy))
	print("  ok 一般怪失敗：扣 1 不返，維持原扣點規則 (15 -> 14 -> 14)")

	# ─────────────────────────────────────────────────────────────
	# 3. C0／C1 主線劇情戰鬥（含雷歐初戰、序章狼）戰鬥失敗不扣能量
	# ─────────────────────────────────────────────────────────────
	# (a) C0 序章首戰（狼 wolf）未通關
	gs.flags.erase("c0_first_battle")
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_wolf: Dictionary = en.try_spend_for_battle("wolf")
	if int(sp_wolf.get("cost", -1)) != 0 or int(gs.energy) != 15:
		_fail("序章狼首戰開戰應免能量，得 %s energy=%d" % [str(sp_wolf), int(gs.energy)])
	var ref_wolf: Dictionary = en.refund_on_defeat("wolf")
	if int(gs.energy) != 15:
		_fail("序章狼首戰失敗能量應維持 15，得 %d" % int(gs.energy))
	print("  ok C0 序章狼首戰失敗：不扣能量 (實耗 0 點)")

	# (b) C1 主線首領初戰（雷歐 leo）未通關
	gs.flags.erase("boss.leo_cleared")
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_leo_first: Dictionary = en.try_spend_for_battle("leo")
	if int(sp_leo_first.get("cost", -1)) != 0 or int(gs.energy) != 15:
		_fail("雷歐初戰開戰應免能量，得 %s energy=%d" % [str(sp_leo_first), int(gs.energy)])
	var ref_leo_first: Dictionary = en.refund_on_defeat("leo")
	if int(gs.energy) != 15:
		_fail("雷歐初戰失敗能量應維持 15，得 %d" % int(gs.energy))
	print("  ok C1 雷歐初戰失敗：不扣能量 (實耗 0 點)")

	# (c) C1 主線劇情單次遭遇怪（荒路匪徒 road_bandit，有 once_flag）
	gs.chapter = "c1"
	gs.flags.erase("boss.leo_cleared")
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var sp_c1_sk: Dictionary = en.try_spend_for_battle("road_bandit")
	if int(gs.energy) != 14:
		_fail("開戰扣 1 點後應為 14，得 %d" % int(gs.energy))
	var ref_c1_sk: Dictionary = en.refund_on_defeat("road_bandit")
	if int(ref_c1_sk.get("refunded", 0)) != 1 or int(gs.energy) != 15:
		_fail("C1 主線劇情遭遇失敗應全額返還 1 點，得 %s energy=%d" % [str(ref_c1_sk), int(gs.energy)])
	print("  ok C1 主線劇情遭遇失敗：全額返還 1 點，實耗 0 點 (15 -> 14 -> 15)")

	# ─────────────────────────────────────────────────────────────
	# 4. 可重複農資源的演武場／狩獵場維持原扣點規則
	# ─────────────────────────────────────────────────────────────
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	var r_arena: Dictionary = en.try_spend_run("arena")
	if not bool(r_arena.get("ok", false)) or int(gs.energy) != 14:
		_fail("演武場入場應扣 1 點能量，得 %s energy=%d" % [str(r_arena), int(gs.energy)])
	var r_hunt: Dictionary = en.try_spend_run("hunt")
	if not bool(r_hunt.get("ok", false)) or int(gs.energy) != 13:
		_fail("狩獵場入場應扣 1 點能量，得 %s energy=%d" % [str(r_hunt), int(gs.energy)])
	print("  ok 演武場／狩獵場可重複農資源關卡：維持入場消耗 1 點體力")

	# ─────────────────────────────────────────────────────────────
	# 5. 連續失敗防崩盤情境驗證（問題六核心訴求）
	# ─────────────────────────────────────────────────────────────
	gs.set_flag("boss.leo_cleared", true)
	gs.energy = 15
	gs.energy_ts = Time.get_unix_time_from_system()
	# 連敗 1：
	en.try_spend_for_battle("leo")   # 15 -> 12
	en.refund_on_defeat("leo")       # 12 -> 14
	# 連敗 2：
	en.try_spend_for_battle("leo")   # 14 -> 11
	en.refund_on_defeat("leo")       # 11 -> 13
	if int(gs.energy) != 13:
		_fail("Boss 戰連敗 2 次後能量應剩餘 13 點（僅消耗 2 點），得 %d" % int(gs.energy))
	print("  ok 連續兩次 Boss 戰失敗防崩盤：15 -> 13（僅損耗 2 點，而非舊機制的 6 點/3小時）")

	_finish()


func _finish() -> void:
	if _ok:
		print("ENERGY_DEFEAT_REFUND_OK")
		quit(0)
	else:
		print("ENERGY_DEFEAT_REFUND_FAIL")
		quit(1)
