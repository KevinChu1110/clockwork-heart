extends SceneTree
## 能量制的把關測試：godot --headless -s res://scripts/systems/test_energy_gate.gd
##
## 守一件事：**演武／獵場的「波次免能量」只放行那一波的對手。**
##
## 踩過：cost_for_mode() 只看 is_run_active()。開一場獵場打贏第一波、不收尾
## （進度存在旗標裡，重開遊戲還在），之後野原雜魚、秘境小王、雷歐、魔王
## 全部 0 能量 —— 一點能量把整個能量制關掉。不報錯、畫面上還會照常顯示
## 「能量 15／15」，只是永遠不會掉。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var en := root.get_node_or_null("EnergySystem")
	var hunt := root.get_node_or_null("HuntSystem")
	var arena := root.get_node_or_null("ArenaSystem")
	if gs == null or en == null or hunt == null or arena == null:
		_fail("GameState／EnergySystem／HuntSystem／ArenaSystem autoload missing")
		return _finish()
	gs.reset_new_game()
	gs.set_flag("c0_first_battle", true)
	gs.set_flag("c1_entered_city", true)

	## 沒有任何場次進行中：雜魚 1、首領 3
	if int(en.cost_for_mode("ash_rat")) != en.COST_MOB:
		_fail("平時雜魚應耗 %d，得 %d" % [en.COST_MOB, int(en.cost_for_mode("ash_rat"))])
	if int(en.cost_for_mode("leo")) != en.COST_BOSS:
		_fail("平時雷歐應耗 %d，得 %d" % [en.COST_BOSS, int(en.cost_for_mode("leo"))])

	## 獵場開跑（第一波 ash_rat）
	var r: Dictionary = hunt.start_run(true)
	if not bool(r.get("ok", false)):
		_fail("獵場開不了：%s" % str(r.get("msg", "")))
		return _finish()
	var wave_mode := str(hunt.wave_mode())
	if int(en.cost_for_mode(wave_mode)) != 0:
		_fail("獵場進行中，本波對手 %s 應免能量，得 %d" % [wave_mode, int(en.cost_for_mode(wave_mode))])
	if int(en.cost_for_mode("leo")) != en.COST_BOSS:
		_fail("獵場進行中打雷歐居然只耗 %d（應 %d）—— 一點能量換整個能量制失效" % [
			int(en.cost_for_mode("leo")), en.COST_BOSS
		])
	if int(en.cost_for_mode("scar_lord")) != en.COST_BOSS:
		_fail("獵場進行中打秘境小王只耗 %d（應 %d）" % [int(en.cost_for_mode("scar_lord")), en.COST_BOSS])
	var other_mob := "coast_raider" if wave_mode != "coast_raider" else "ash_rat"
	if int(en.cost_for_mode(other_mob)) != en.COST_MOB:
		_fail("獵場進行中打別種雜魚 %s 只耗 %d（應 %d）" % [other_mob, int(en.cost_for_mode(other_mob)), en.COST_MOB])
	hunt.abandon_run()
	print("  ok 獵場進行中：本波 %s 免費，雷歐仍 %d、別種雜魚仍 %d" % [wave_mode, en.COST_BOSS, en.COST_MOB])

	## 演武同理
	var ra: Dictionary = arena.start_run(true)
	if not bool(ra.get("ok", false)):
		_fail("演武開不了：%s" % str(ra.get("msg", "")))
		return _finish()
	var am := str(arena.wave_mode())
	if int(en.cost_for_mode(am)) != 0:
		_fail("演武進行中，本波對手 %s 應免能量" % am)
	if int(en.cost_for_mode("demon")) != en.COST_BOSS:
		_fail("演武進行中打魔王只耗 %d（應 %d）" % [int(en.cost_for_mode("demon")), en.COST_BOSS])
	arena.abandon_run()
	print("  ok 演武進行中：本波 %s 免費，魔王仍 %d" % [am, en.COST_BOSS])

	## 收尾後回到正常價
	if int(en.cost_for_mode("ash_rat")) != en.COST_MOB:
		_fail("放棄場次後雜魚應回到 %d" % en.COST_MOB)

	## 好友挑戰的 pending 旗：只放行殘影戰本身。
	## 旗會跟著中途存檔留下來（戰鬥中喝藥就會存），殘影戰打一半關遊戲，
	## 重開後只看旗的話下一場不管打誰都免費。
	var visit := root.get_node_or_null("VisitSystem")
	if visit == null:
		_fail("VisitSystem autoload missing")
		return _finish()
	gs.set_flag("visit.pending_id", "stale_shadow")
	if int(en.cost_for_mode("pvp_snap")) != 0:
		_fail("拜訪中殘影戰應免能量，得 %d" % int(en.cost_for_mode("pvp_snap")))
	if int(en.cost_for_mode("leo")) != en.COST_BOSS:
		_fail("殘留的拜訪旗讓雷歐只耗 %d（應 %d）" % [int(en.cost_for_mode("leo")), en.COST_BOSS])
	if int(en.cost_for_mode("ash_rat")) != en.COST_MOB:
		_fail("殘留的拜訪旗讓雜魚只耗 %d（應 %d）" % [int(en.cost_for_mode("ash_rat")), en.COST_MOB])
	visit.clear_pending()
	print("  ok 拜訪旗只放行殘影戰：pvp_snap 0、雷歐 %d、雜魚 %d" % [en.COST_BOSS, en.COST_MOB])
	_finish()


func _finish() -> void:
	if _ok:
		print("ENERGY_GATE_OK")
		quit(0)
	else:
		print("ENERGY_GATE_FAIL")
		quit(1)
