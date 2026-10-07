extends SceneTree
## 自動彈開單元測試 (test_auto_deflect.gd)
##
## 依據 2026-10-05 任務書與 t_764676f5 驗收規範：
## 1. 戰鬥為自動回合，自動彈開（deflect）改由閃避與速度判定，不依賴手動按鍵
## 2. 數值判定驗證：依 Formulas.deflect_chance，閃避 (eva) 與速度 (speed) 越高，彈開機率越高
## 3. 實戰模擬驗證：高閃避/高速度玩家在無任何按鍵操作下自動觸發完美彈開，受傷為 0 且反擊部位
## 4. 低閃避/低速度玩家在無操作下不觸發彈開，承受正常前搖高傷

const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")
const FormulasClass := preload("res://scripts/battle/formulas.gd")


func _initialize() -> void:
	print("=== 開始 test_auto_deflect 測試 ===")
	test_formula_deflect_chance()
	test_high_eva_auto_deflect()
	test_low_eva_no_deflect()
	test_speed_difference_impact()
	print("AUTO_DEFLECT_OK")
	quit(0)


func test_formula_deflect_chance() -> void:
	print("--- 1. 驗證 Formulas.deflect_chance 數值公式 ---")
	# 零閃避、速度相同 -> 機率為 0
	var zero_rate := FormulasClass.deflect_chance(10.0, 10.0, 0.0, 0.0)
	assert(zero_rate == 0, "零閃避且同速時彈開機率應為 0")

	# 高閃避 (30 eva) -> 至少 30% 機率
	var eva_rate := FormulasClass.deflect_chance(10.0, 10.0, 0.0, 30.0)
	assert(eva_rate == 30, "30 閃避且同速時彈開機率應為 30")

	# 高速度差 (def_spd 30 vs atk_spd 10: diff=20 -> sqrt(100)=10) -> 速度加成 10
	var spd_rate := FormulasClass.deflect_chance(10.0, 30.0, 0.0, 0.0)
	assert(spd_rate == 10, "速度差為 20 時速度加成應為 10")

	# 速度與閃避疊加 (diff=20 (+10) + 40 eva = 50)
	var combo_rate := FormulasClass.deflect_chance(10.0, 30.0, 0.0, 40.0)
	assert(combo_rate == 50, "速度加成 10 與 40 閃避疊加應為 50")

	# 機率上限 (cap 90)
	var capped_rate := FormulasClass.deflect_chance(10.0, 100.0, 0.0, 100.0)
	assert(capped_rate <= 90, "彈開機率應受限於 cap 90")
	print("  ✓ 公式判定：閃避與速度差正確疊加，上限鎖定 90%")


func test_high_eva_auto_deflect() -> void:
	print("--- 2. 驗證高閃避/速度角色自動彈開（無任何按鍵輸入） ---")
	var sim = BattleSimClass.make_world_fight({
		"name": "小白",
		"max_hp": 200,
		"hp": 200,
		"atk": 30,
		"def": 10,
		"speed": 50.0,
		"eva": 90.0, # 保證 90% 彈開
		"hit": 0.0,
	}, "colossus_lion")

	var boss = sim.get_unit("colossus_lion")
	var player = sim.get_unit("player")
	var initial_hp: int = player.hp

	var parry_emitted := {"count": 0, "banner": ""}
	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "perfect_parry":
			parry_emitted["count"] += 1
			parry_emitted["banner"] = str(data.get("banner", ""))
	)

	# 觸發巨偶蓄力前搖
	sim.trigger_colossus_windup()
	assert(boss.telegraph_active, "巨偶應已進入前搖")

	# 不調用任何 try_parry() 或 try_react()，直接步進模擬至前搖結束
	# 前搖時間約 1.85s，每次步進 0.05s
	while boss.telegraph_active and not sim.finished:
		sim.step(0.05)

	# 驗證自動彈開成功觸發
	assert(parry_emitted["count"] >= 1, "高閃避角色在前搖結束時應自動觸發完美彈開")
	assert(player.hp == initial_hp, "自動彈開後玩家應免受前搖高傷")
	assert(boss.state == BattleUnit.State.RECOVER, "被彈開後 Boss 應進入 RECOVER 硬直")
	print("  ✓ 自動彈開成功：無按鍵干預下觸發完美彈開，玩家無傷，Boss 進入硬直")


func test_low_eva_no_deflect() -> void:
	print("--- 3. 驗證低閃避/低速度角色不彈開，承受正常前搖傷害 ---")
	var sim = BattleSimClass.make_world_fight({
		"name": "小白",
		"max_hp": 500,
		"hp": 500,
		"atk": 20,
		"def": 5,
		"speed": 5.0, # 遠低於 Boss 速度
		"eva": 0.0,   # 0 閃避
		"hit": 0.0,
	}, "colossus_lion")

	var boss = sim.get_unit("colossus_lion")
	var player = sim.get_unit("player")
	var initial_hp: int = player.hp

	var parry_count := 0
	sim.event.connect(func(kind: String, _data: Dictionary):
		if kind == "perfect_parry":
			parry_count += 1
	)

	sim.trigger_colossus_windup()
	while boss.telegraph_active and not sim.finished:
		sim.step(0.05)

	assert(parry_count == 0, "0 閃避且低速角色不應觸發自動彈開")
	assert(player.hp < initial_hp, "未彈開時玩家應承受前搖傷害")
	print("  ✓ 低屬性角色未彈開：未觸發 parry，正常結算傷害")


func test_speed_difference_impact() -> void:
	print("--- 4. 驗證速度優勢顯著提高彈開統計率 ---")
	var fast_deflects := 0
	var slow_deflects := 0
	var trials := 50

	for i in range(trials):
		# 高速組 (speed 40, eva 20)
		var sim_fast = BattleSimClass.make_world_fight({
			"name": "小白", "max_hp": 300, "hp": 300, "atk": 20, "def": 10,
			"speed": 40.0, "eva": 20.0, "hit": 0.0,
		}, "colossus_lion")
		sim_fast.rng.seed = 1000 + i
		var boss_fast = sim_fast.get_unit("colossus_lion")
		sim_fast.trigger_colossus_windup()
		var fast_res := {"hit": false}
		sim_fast.event.connect(func(k: String, _d: Dictionary):
			if k == "perfect_parry":
				fast_res["hit"] = true
		)
		while boss_fast.telegraph_active and not sim_fast.finished:
			sim_fast.step(0.05)
		if fast_res["hit"]:
			fast_deflects += 1

		# 低速組 (speed 5, eva 0)
		var sim_slow = BattleSimClass.make_world_fight({
			"name": "小白", "max_hp": 300, "hp": 300, "atk": 20, "def": 10,
			"speed": 5.0, "eva": 0.0, "hit": 0.0,
		}, "colossus_lion")
		sim_slow.rng.seed = 1000 + i
		var boss_slow = sim_slow.get_unit("colossus_lion")
		sim_slow.trigger_colossus_windup()
		var slow_res := {"hit": false}
		sim_slow.event.connect(func(k: String, _d: Dictionary):
			if k == "perfect_parry":
				slow_res["hit"] = true
		)
		while boss_slow.telegraph_active and not sim_slow.finished:
			sim_slow.step(0.05)
		if slow_res["hit"]:
			slow_deflects += 1

	print("  統計結果 (50 次): 高速+高閃組 彈開 %d 次 vs 低速+零閃組 彈開 %d 次" % [fast_deflects, slow_deflects])
	assert(fast_deflects > slow_deflects, "高速高閃組彈開次數應顯著高於低速組")
	assert(slow_deflects == 0, "低速零閃組彈開率應為 0")
	print("  ✓ 速度與閃避判定有效性驗證通過")
