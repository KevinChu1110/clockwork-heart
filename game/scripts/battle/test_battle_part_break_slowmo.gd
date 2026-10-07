extends SceneTree
## 無頭測試：戰鬥部位破壞 0.4 秒慢動作頓挫與 Boss 部位將破 warn 音效整合
## 驗收重點：
## 1. Boss 部位血量 <= 20% 時自動播放 warn 音效（AudioManager.play_sfx("warn")），且每個部位只播一次。
## 2. warn 音效徹底移出格擋窗（king_slash_start 等不再觸發 warn）。
## 3. 部位破壞（part_break）瞬間觸發 0.4 秒慢動作頓挫（sim.slowmo == 0.4），並平滑恢復。
## 4. 部位破壞觸發 break 音效與金屬糖果屑特效整合介面。

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const BattleUnit := preload("res://scripts/battle/battle_unit.gd")

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error("FAIL: %s" % msg)
	print("  [FAIL] %s" % msg)
	_ok = false


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_all_tests()
		if _ok:
			print("\n=======================================================")
			print("TEST_BATTLE_PART_BREAK_SLOWMO_OK")
			quit(0)
		else:
			push_error("TEST_BATTLE_PART_BREAK_SLOWMO_FAIL")
			print("TEST_BATTLE_PART_BREAK_SLOWMO_FAIL")
			quit(1)
		return true
	return false


func _stats() -> Dictionary:
	return {
		"name": "兔勇者",
		"max_hp": 300,
		"hp": 300,
		"atk": 50,
		"def": 15,
		"speed": 12,
	}


func _run_all_tests() -> void:
	print("== 測試戰鬥部位破壞 0.4 秒慢動作頓挫與 Boss 部位將破 warn 音效 ==")
	_test_boss_part_warn_audio()
	_test_warn_removed_from_parry_window()
	_test_part_break_slowmo_sim()
	_test_part_break_view_interface()
	_test_part_break_audio_and_vfx()


func _test_boss_part_warn_audio() -> void:
	print("--- 1. 測試 Boss 部位血量 <= 20% 自動播放 warn 音效 ---")
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager 節點不存在")
		return
	am.clear_sfx_history()

	var sim: BattleSim = BattleSim.make_leo_fight(_stats())
	var leo := sim._primary_boss_unit()
	if leo == null or leo.parts.is_empty():
		_fail("Leo Boss 或部位遺失")
		return

	# 解鎖破部位破綻：本體壓到 50%
	leo.hp = int(float(leo.max_hp) * 0.5)
	sim.parts_break_unlocked = true
	sim.parts_break_stage = 2

	# 鎖定 shield 部位
	sim.focus_part_id = "shield"
	var shield_idx := -1
	for i in leo.parts.size():
		if str(leo.parts[i].get("id", "")) == "shield":
			shield_idx = i
			break
	if shield_idx == -1:
		_fail("Leo 找不到 shield 部位")
		return

	var max_hp := int(leo.parts[shield_idx].get("max_hp", 134))

	# 步驟 1-A：部位受到適度傷害，降至約 50%（> 20%）：不應觸發 warn
	# 扣約 60 點（dealt 45 * 1.35 = 61），剩餘約 73 點 (54% > 20%)
	sim._process_part_damage(leo, 45, false)
	var p: Dictionary = leo.parts[shield_idx]
	var cur_hp := int(p.get("hp", 0))
	var ratio := float(cur_hp) / float(max_hp)
	if ratio <= 0.20:
		_fail("測試前置傷害過大，部位已低於 20%")
		return
	if am.get_sfx_count("warn") != 0:
		_fail("部位血量高於 20% 時不應播放 warn，但播放了 %d 次" % am.get_sfx_count("warn"))
		return
	if bool(p.get("warned", false)):
		_fail("部位血量高於 20% 時 warned 不應為 true")
		return
	print("  ok - 部位血量高於 20%（剩餘 %d/%d）時未觸發 warn" % [cur_hp, max_hp])

	# 步驟 1-B：部位再次受到傷害，降至 <= 20% 且 > 0：應自動播放 1 次 warn 音效
	# 目標剩餘約 15~20 點。需再扣約 55 點（dealt 40 * 1.35 = 54）
	sim._process_part_damage(leo, 40, false)
	p = leo.parts[shield_idx]
	cur_hp = int(p.get("hp", 0))
	var ratio_low := float(cur_hp) / float(max_hp)
	if cur_hp <= 0:
		_fail("部位不應直接被打破，應保持 > 0")
		return
	if ratio_low > 0.20001:
		_fail("部位血量應降至 <= 20%，實際為 %f" % ratio_low)
		return
	if not bool(p.get("warned", false)):
		_fail("部位血量 <= 20% 時 warned 應標記為 true")
		return
	if am.get_sfx_count("warn") != 1:
		_fail("部位血量 <= 20% 應自動播放 1 次 warn，實際為 %d 次" % am.get_sfx_count("warn"))
		return
	print("  ok - 部位血量降至 <= 20%（剩餘 %d/%d）時自動播放 1 次 warn" % [cur_hp, max_hp])

	# 步驟 1-C：再次受到微量傷害（dealt 1，血量仍 <= 20% 且 > 0）：不應重複播放 warn
	if cur_hp > 2:
		sim._process_part_damage(leo, 1, false)
		if am.get_sfx_count("warn") != 1:
			_fail("再次受到微傷害不應重複播放 warn，實際計數: %d" % am.get_sfx_count("warn"))
			return
	print("  ok - 部位血量持續 <= 20% 時不重複播放 warn（維持 1 次）")


func _test_warn_removed_from_parry_window() -> void:
	print("--- 2. 測試 warn 音效徹底移出格擋窗 ---")
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager 節點不存在")
		return
	am.clear_sfx_history()

	# 觸發格擋窗前搖事件
	am.on_battle_event("king_slash_start", {"label": "王者斬"})
	if am.get_sfx_count("warn") != 0:
		_fail("king_slash_start 格擋窗不應播放 warn 音效")
		return

	print("  ok - king_slash_start 前搖不再播放 warn 音效（已移出格擋窗）")


func _test_part_break_slowmo_sim() -> void:
	print("--- 3. 測試部位破壞觸發 0.4 秒慢動作頓挫（sim.slowmo == 0.4）---")
	var sim: BattleSim = BattleSim.make_leo_fight(_stats())
	var leo := sim._primary_boss_unit()
	# 手動解鎖破部位門檻：本體壓到 30%（低於第二階段 40%，全部位可破）
	leo.hp = int(float(leo.max_hp) * 0.3)
	sim.parts_break_unlocked = true
	sim.parts_break_stage = 2

	sim.focus_part_id = "shield"
	var shield_idx := -1
	for i in leo.parts.size():
		if str(leo.parts[i].get("id", "")) == "shield":
			shield_idx = i
			break
	var max_hp := int(leo.parts[shield_idx].get("max_hp", 100))

	# 透過 Dictionary 容器確保閉包寫入
	var tracker := {
		"received": false,
		"slowmo": 0.0,
	}
	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "part_broken":
			tracker["received"] = true
			tracker["slowmo"] = float(data.get("slowmo", 0.0))
	)

	# 灌足量傷害打破該部位
	sim._process_part_damage(leo, max_hp + 500, true)
	if not bool(leo.parts[shield_idx].get("broken", false)):
		_fail("部位應該已經破壞")
		return

	if not bool(tracker["received"]):
		_fail("未收到 part_broken 事件")
		return

	var slowmo_val: float = float(tracker["slowmo"])
	if not is_equal_approx(slowmo_val, 0.4):
		_fail("part_broken 事件中的 slowmo 應為 0.4，實際為 %.2f" % slowmo_val)
		return

	if not is_equal_approx(sim.slowmo, 0.4):
		_fail("sim.slowmo 應為 0.4，實際為 %.2f" % sim.slowmo)
		return
	print("  ok - 部位破壞瞬間 sim.slowmo 設置為 0.4 秒")

	# 推進模擬 0.2 秒，slowmo 應遞減
	sim.step(0.2)
	if not is_equal_approx(sim.slowmo, 0.2):
		_fail("step(0.2) 後 sim.slowmo 應約為 0.2，實際為 %.2f" % sim.slowmo)
		return

	# 再推進 0.25 秒，slowmo 應回到 0.0
	sim.step(0.25)
	if not is_equal_approx(sim.slowmo, 0.0):
		_fail("step(0.25) 後 sim.slowmo 應回到 0.0，實際為 %.2f" % sim.slowmo)
		return
	print("  ok - 慢動作持續 0.4 秒後順暢歸零恢復")


func _test_part_break_view_interface() -> void:
	print("--- 4. 測試 BattleView 0.4 秒慢動作頓挫方法與相容性 ---")
	var battle_scene = load("res://scenes/battle/battle.tscn")
	if battle_scene == null:
		_fail("找不到 res://scenes/battle/battle.tscn")
		return

	var bv = battle_scene.instantiate()
	root.add_child(bv)

	if not bv.has_method("trigger_part_break_slowmo"):
		_fail("BattleView 缺少 trigger_part_break_slowmo 方法")
		bv.queue_free()
		return

	var orig_scale := Engine.time_scale
	bv.trigger_part_break_slowmo(0.4)
	if not is_equal_approx(Engine.time_scale, 0.15):
		_fail("trigger_part_break_slowmo 應將 Engine.time_scale 調降為 0.15，實際為: %.2f" % Engine.time_scale)
		Engine.time_scale = orig_scale
		bv.queue_free()
		return

	Engine.time_scale = orig_scale
	bv.queue_free()
	print("  ok - BattleView trigger_part_break_slowmo 正常頓挫縮放 Engine.time_scale")


func _test_part_break_audio_and_vfx() -> void:
	print("--- 5. 測試部位破壞 break 音效與糖果屑碎裂特效整合 ---")
	var am := root.get_node_or_null("AudioManager")
	if am != null:
		am.clear_sfx_history()
		am.on_battle_event("part_broken", {"part_name": "護盾", "boss_id": "leo"})
		if am.get_sfx_count("break") < 1:
			_fail("part_broken 事件應觸發 break 音效")
			return
		print("  ok - part_broken 觸發 break 音效")

	# 檢查糖果屑腳本存在
	var candy_path := "res://scripts/systems/candy_chip_vfx/candy_chip_vfx.gd"
	if not ResourceLoader.exists(candy_path):
		_fail("CandyChipVfx 腳本遺失: %s" % candy_path)
		return
	print("  ok - CandyChipVfx 金屬糖果屑碎裂特效資源正常")
