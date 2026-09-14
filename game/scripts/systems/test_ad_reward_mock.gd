extends SceneTree
## 獎勵型廣告（Mock）把關測試：godot --headless -s res://scripts/systems/test_ad_reward_mock.gd
##
## 驗證：
## 1. 呼叫看廣告後體力有增加（EnergySystem.claim_ad_energy）。
## 2. 每日上限有擋（預設 3 次，第 4 次被擋回且不發放）。
## 3. 次數隨換日（GameState flag）重置清零。
## 4. 戰鬥失敗二次機會復活的每日上限與換日重置。
## 5. MockAdDialog 本機讀秒與回呼流程正常。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var en := root.get_node_or_null("EnergySystem")
	if gs == null or en == null:
		_fail("GameState／EnergySystem autoload missing")
		return _finish()

	gs.reset_new_game()

	# ── 1. 體力獎勵型廣告初始狀態 ──
	en.refresh_ad_daily()
	if en.ad_rewards_used_today() != 0:
		_fail("初始已用次數應為 0，實際為 %d" % en.ad_rewards_used_today())
	if en.ad_rewards_left_today() != en.DAILY_AD_REWARD_CAP:
		_fail("初始剩餘次數應為 %d，實際為 %d" % [en.DAILY_AD_REWARD_CAP, en.ad_rewards_left_today()])
	if not en.can_claim_ad_energy():
		_fail("初始應可領取廣告體力")
	print("  ok 體力廣告初始狀態正常（0/%d）" % en.DAILY_AD_REWARD_CAP)

	# ── 2. 觀看廣告領取體力（增加 3 點）──
	gs.energy = 5
	var claim1: bool = en.claim_ad_energy(3)
	if not claim1:
		_fail("第 1 次領取體力廣告回傳失敗")
	if gs.energy != 8:
		_fail("領取 3 點體力後能量應為 8，實際為 %d" % int(gs.energy))
	if en.ad_rewards_used_today() != 1:
		_fail("第 1 次領取後已用次數應為 1，實際為 %d" % en.ad_rewards_used_today())
	if en.ad_rewards_left_today() != 2:
		_fail("第 1 次領取後剩餘次數應為 2，實際為 %d" % en.ad_rewards_left_today())
	print("  ok 觀看廣告後體力正確增加 3 點（5 -> 8），剩餘次數更新")

	# ── 3. 達每日上限（3 次）後攔截 ──
	var claim2: bool = en.claim_ad_energy(3)
	var claim3: bool = en.claim_ad_energy(3)
	if not claim2 or not claim3:
		_fail("第 2、3 次領取體力廣告回傳失敗")
	if en.ad_rewards_used_today() != 3:
		_fail("領取 3 次後已用次數應為 3，實際為 %d" % en.ad_rewards_used_today())
	if en.ad_rewards_left_today() != 0:
		_fail("領取 3 次後剩餘次數應為 0，實際為 %d" % en.ad_rewards_left_today())
	if en.can_claim_ad_energy():
		_fail("已達上限時 can_claim_ad_energy 應為 false")

	# 第 4 次嘗試領取：應被擋下
	var energy_before := int(gs.energy)
	var claim4: bool = en.claim_ad_energy(3)
	if claim4:
		_fail("超過每日上限時 claim_ad_energy 仍回傳 true")
	if int(gs.energy) != energy_before:
		_fail("超過每日上限時能量不應增加")
	if en.ad_rewards_used_today() != 3:
		_fail("超過每日上限時已用次數不應繼續累加")
	print("  ok 達到每日上限（3/3）後成功攔截第 4 次領取")

	# ── 4. 每日重置清零（換日）──
	gs.set_flag("energy.ad_reward_day", "2020-01-01")
	en.refresh_ad_daily()
	if en.ad_rewards_used_today() != 0:
		_fail("換日後已用次數應重置為 0，實際為 %d" % en.ad_rewards_used_today())
	if en.ad_rewards_left_today() != en.DAILY_AD_REWARD_CAP:
		_fail("換日後剩餘次數應重置為 %d，實際為 %d" % [en.DAILY_AD_REWARD_CAP, en.ad_rewards_left_today()])
	if not en.can_claim_ad_energy():
		_fail("換日後應恢復可領取狀態")
	print("  ok 換日後次數隨每日重置自動清零恢復 3 次")

	# ── 5. 戰鬥失敗二次機會復活上限與換日重置 ──
	if en.ad_revives_used_today() != 0 or en.ad_revives_left_today() != en.DAILY_AD_REVIVE_CAP:
		_fail("復活次數初始狀態異常")
	var r1: bool = en.claim_ad_revive()
	var r2: bool = en.claim_ad_revive()
	var r3: bool = en.claim_ad_revive()
	if not (r1 and r2 and r3):
		_fail("前 3 次復活應成功")
	if en.ad_revives_left_today() != 0 or en.can_claim_ad_revive():
		_fail("滿 3 次復活後應無剩餘次數")
	var r4: bool = en.claim_ad_revive()
	if r4:
		_fail("第 4 次復活應被擋下")

	# 復活換日重置
	gs.set_flag("battle.ad_revive_day", "2020-01-01")
	en.refresh_ad_daily()
	if en.ad_revives_used_today() != 0 or en.ad_revives_left_today() != en.DAILY_AD_REVIVE_CAP:
		_fail("復活換日重置異常")
	print("  ok 戰鬥復活二次機會上限與換日重置正常")

	# ── 6. MockAdDialog 元件回呼驗證 ──
	var MockAdClass: GDScript = load("res://scripts/ui/mock_ad_dialog.gd")
	if MockAdClass == null:
		_fail("無法載入 MockAdDialog")
		return _finish()

	var called := [false]
	var ad_node = MockAdClass.new()
	ad_node.setup("energy", func():
		called[0] = true
	)
	root.add_child(ad_node)
	ad_node.skip_countdown()
	ad_node._on_claim_reward()

	if not called[0]:
		_fail("MockAdDialog 完成後未呼叫 on_success 回呼")
	else:
		print("  ok MockAdDialog 假讀秒與完成回呼執行正常")

	_finish()


func _finish() -> void:
	if _ok:
		print("AD_REWARD_MOCK_OK")
		quit(0)
	else:
		print("AD_REWARD_MOCK_FAIL")
		quit(1)
