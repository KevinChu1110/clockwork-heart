extends SceneTree
## godot --headless -s res://scripts/systems/test_soul_system.gd


func _initialize() -> void:
	var ok := true
	var ss = root.get_node_or_null("SoulSystem")
	var gs = root.get_node_or_null("GameState")
	if ss == null or gs == null:
		push_error("autoload missing")
		quit(1)
		return
	gs.reset_new_game()
	gs.weapon_tier = 2
	gs.weapon_atk = 9
	gs.gold = 500
	gs.soul_vessel = "綠葫蘆"
	gs.soul_free_draws = 1
	gs.soul_free_day = ss.today_key()
	ss.ensure_slots()
	if ss.slot_count() != 1:
		push_error("tier2 should have 1 slot got %d" % ss.slot_count())
		ok = false
	else:
		print("slots OK")

	var starter: Dictionary = ss.grant_starter_soul()
	if starter.is_empty():
		push_error("starter empty")
		ok = false
	var b: Dictionary = ss.total_equipped_bonus()
	if int(b.get("atk", 0)) < 1:
		push_error("starter should give atk")
		ok = false
	else:
		print("starter equip OK atk+", b.get("atk"))

	## 免費抽一次
	var before_free: int = int(gs.soul_free_draws)
	var rolled: Dictionary = ss.ritual()
	if rolled.is_empty() or int(gs.soul_free_draws) != before_free - 1:
		push_error("free ritual fail free=%s soul=%s" % [gs.soul_free_draws, rolled])
		ok = false
	else:
		print("free ritual OK ", ss.soul_display(rolled), " vessel=", gs.soul_vessel)

	## 付費抽：無免費時扣金
	gs.soul_free_draws = 0
	var cost: int = ss.vessel_cost()
	var gold0: int = int(gs.gold)
	var paid: Dictionary = ss.ritual()
	if paid.is_empty() or int(gs.gold) != gold0 - cost:
		push_error("paid ritual fail gold %s→%s cost %s" % [gold0, gs.gold, cost])
		ok = false
	else:
		print("paid ritual OK -%d gold vessel=%s" % [cost, gs.soul_vessel])

	## ×10：有錢就能連抽；錢不夠就停
	gs.soul_free_draws = 0
	gs.soul_vessel = "綠葫蘆"
	gs.gold = ss.vessel_cost() * 10
	if not ss.can_ritual_batch(10):
		push_error("should afford x10")
		ok = false
	var bag0: int = gs.souls.size()
	var batch: Array = ss.ritual_batch(10)
	if batch.size() < 1:
		push_error("x10 empty")
		ok = false
	elif gs.souls.size() != bag0 + batch.size():
		push_error("x10 bag mismatch")
		ok = false
	else:
		print("x10 OK n=%d gold_left=%d vessel=%s" % [batch.size(), gs.gold, gs.soul_vessel])
	gs.gold = 0
	gs.soul_free_draws = 0
	if ss.can_ritual_batch(10):
		push_error("x10 should deny empty gold")
		ok = false

	## 橙葫蘆 100% 神 → 必摔綠
	gs.soul_vessel = "橙葫蘆"
	gs.soul_free_draws = 1
	gs.gold = 5000
	var orange: Dictionary = ss.ritual()
	if str(orange.get("quality", "")) != "神" or str(gs.soul_vessel) != "綠葫蘆":
		push_error("orange should yield 神 and reset green got q=%s v=%s" % [
			orange.get("quality"), gs.soul_vessel
		])
		ok = false
	else:
		print("orange jackpot reset OK ", ss.soul_display(orange))

	## 合成：塞 3 顆同款
	gs.souls = []
	gs.soul_slots = [""]
	for i in 3:
		gs.souls.append({
			"id": "t%d" % i, "star": "破軍", "quality": "凡", "level": 0, "equipped": false
		})
	var fused: Dictionary = ss.fuse("破軍", "凡", 0)
	if fused.is_empty() or int(fused.get("level", -1)) != 1:
		push_error("fuse fail")
		ok = false
	else:
		print("fuse OK ", ss.soul_display(fused), " bag=", ss.bag_souls().size())

	gs.weapon_tier = 6
	ss.ensure_slots()
	if ss.slot_count() != 2:
		push_error("tier6 slots")
		ok = false
	else:
		print("tier6 slots OK")

	if ss.STARS.size() < 14:
		push_error("need 14 stars got %d" % ss.STARS.size())
		ok = false
	else:
		print("fourteen stars OK")

	## 神魂＝神品質戰魂，最高 10 級（聚俠網）；凡品仍 3 階
	if ss.fuse_max_level("凡") != 3 or ss.fuse_max_level("神") != 10:
		push_error("fuse cap 凡/神")
		ok = false
	else:
		print("shen cap 10 OK")
	gs.souls = []
	gs.soul_slots = [""]
	for i in 3:
		gs.souls.append({
			"id": "s%d" % i, "star": "天機", "quality": "神", "level": 9, "equipped": false
		})
	if not ss.can_fuse("天機", "神", 9):
		push_error("神 lv9 should fuse to 10")
		ok = false
	var shen: Dictionary = ss.fuse("天機", "神", 9)
	if shen.is_empty() or int(shen.get("level", 0)) != 10:
		push_error("神 fuse to 10 fail %s" % shen)
		ok = false
	elif ss.can_fuse("天機", "神", 10):
		push_error("神 should stop at 10")
		ok = false
	else:
		print("shen lv10 OK ", ss.soul_display(shen))

	## 入魂對比：空槽應顯示從 0 起的增減
	gs.souls = [{
		"id": "cmp1", "star": "破軍", "quality": "凡", "level": 0, "equipped": false
	}]
	gs.soul_slots = [""]
	var cmp: Dictionary = ss.compare_embed("cmp1", 0)
	if str(cmp.get("line", "")).find("槽1") < 0:
		push_error("compare line missing slot %s" % cmp)
		ok = false
	else:
		print("embed compare OK ", cmp.get("line"))

	## 虔誠度：每抽 +10、滿 100 產 1 碎片
	gs.set_flag("soul.piety", 0)
	gs.set_flag("soul.shards", 0)
	gs.soul_free_draws = 0
	gs.gold = 99999
	gs.soul_vessel = "綠葫蘆"
	for i in 10:
		ss.ritual(true)
	if ss.shards() != 1 or ss.piety() != 0:
		push_error("10 draws should yield 1 shard (shards=%d piety=%d)" % [ss.shards(), ss.piety()])
		ok = false
	else:
		print("piety→shard OK")

	## 碎片兌換：扣片、得指定品質
	gs.set_flag("soul.shards", 6)
	var n0: int = gs.souls.size()
	var ex: Dictionary = ss.exchange_shards("稀世")
	if not bool(ex.get("ok", false)) or ss.shards() != 0 or gs.souls.size() != n0 + 1:
		push_error("exchange fail %s shards=%d" % [ex, ss.shards()])
		ok = false
	elif str((ex.get("soul", {}) as Dictionary).get("quality", "")) != "稀世":
		push_error("exchange quality wrong %s" % ex)
		ok = false
	else:
		print("shard exchange OK ", ss.soul_display(ex.get("soul", {})))
	var ex2: Dictionary = ss.exchange_shards("神")
	if bool(ex2.get("ok", false)):
		push_error("exchange without shards should fail")
		ok = false
	else:
		print("shard shortage blocked OK")

	## 養魂：廢魂餵最強、逐級進位；入槽魂不能當飼料
	gs.souls = [
		{"id": "t1", "star": "武曲", "quality": "稀世", "level": 0, "equipped": false},
		{"id": "j1", "star": "破軍", "quality": "凡", "level": 0, "equipped": false},
		{"id": "j2", "star": "破軍", "quality": "大凶", "level": 0, "equipped": false},
		{"id": "j3", "star": "破軍", "quality": "凡", "level": 0, "equipped": true},
	]
	gs.soul_slots = ["j3"]
	var ab: Dictionary = ss.absorb_junk_auto()
	if not bool(ab.get("ok", false)) or int(ab.get("eaten", 0)) != 2:
		push_error("absorb should eat 2 junk %s" % ab)
		ok = false
	elif gs.souls.size() != 2:
		push_error("junk should be removed, left %d" % gs.souls.size())
		ok = false
	else:
		print("absorb OK xp+", ab.get("xp"), " lv=", ab.get("level"))
	## 45 經驗不夠 60 → 0 級；再餵到升級
	var big: Array = []
	for i in 6:
		big.append({"id": "k%d" % i, "star": "破軍", "quality": "吉", "level": 0, "equipped": false})
	gs.souls += big
	var fids: Array = []
	for s in big:
		fids.append(s["id"])
	var ab2: Dictionary = ss.absorb("t1", fids)
	if not bool(ab2.get("ok", false)) or int(ab2.get("level", 0)) < 1:
		push_error("feeding 360xp should level up %s" % ab2)
		ok = false
	else:
		print("feed level-up OK lv=", ab2.get("level"))

	if ok:
		print("SOUL_OK")
		quit(0)
	else:
		print("SOUL_FAIL")
		quit(1)
