extends SceneTree
## 單元測試：戰鬥發條超載爆裂（Overwind Burst）滿怒視覺、音效與六語系驗證
## 依據規範：docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點一, review.md 19b/0-ART51

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const BattleUnit := preload("res://scripts/battle/battle_unit.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	print("=== 開始執行 test_combat_overwind_burst ===")
	_test_sim_events()
	_test_audio_event()
	_test_six_locales()
	_step = 1
	_wait = 0


func _test_sim_events() -> void:
	print("\n--- 1. 驗證 BattleSim 滿怒與技能釋放時觸發 overwind_burst 事件 ---")
	var stats := {"name": "兔勇者", "max_hp": 100, "atk": 30, "def": 10, "speed": 10, "can_skill": true}
	var sim := BattleSim.make_tutorial_wolf_fight(stats)
	var p := sim.get_unit("player")

	var events: Array[Dictionary] = []
	sim.event.connect(func(kind: String, data: Dictionary):
		if kind == "overwind_burst":
			events.append(data)
	)

	# 1.1 累加怒氣跨越滿怒閾值 (rage >= 100)
	p.rage = 85.0
	sim._gain_rage(p, 25.0)
	assert(events.size() == 1, "滿怒應觸發 1 次 overwind_burst 事件")
	assert(str(events[0].get("source", "")) == "rage_full", "事件 source 應為 rage_full")
	print("  [PASS] 累怒滿額觸發 overwind_burst (source=rage_full)")

	# 1.2 手動暴怒觸發
	events.clear()
	p.rage = 100.0
	p.fury_active = false
	var res_fury := sim.trigger_fury_awakening()
	assert(res_fury, "手動暴怒應成功")
	assert(events.size() == 1, "手動暴怒應觸發 overwind_burst")
	assert(str(events[0].get("source", "")) == "manual_fury", "事件 source 應為 manual_fury")
	print("  [PASS] 手動暴怒觸發 overwind_burst (source=manual_fury)")

	# 1.3 滿怒施放技能觸發
	events.clear()
	var sim_skill := BattleSim.make_tutorial_wolf_fight(stats)
	var p_skill := sim_skill.get_unit("player")
	sim_skill.event.connect(func(kind: String, data: Dictionary):
		if kind == "overwind_burst":
			events.append(data)
	)
	p_skill.rage = 100.0
	p_skill.can_skill = true
	p_skill.bare_fisted = false
	var steps := 0
	while events.is_empty() and steps < 200:
		sim_skill.step(0.05)
		steps += 1
	assert(events.size() >= 1, "滿怒出手施放技能應觸發 overwind_burst")
	print("  [PASS] 滿怒技能出手觸發 overwind_burst (steps=%d)" % steps)


func _test_audio_event() -> void:
	print("\n--- 2. 驗證 AudioManager 音效整合 ---")
	var am: Node = root.get_node_or_null("AudioManager")
	if am != null:
		assert(am.has_method("play_overwind_burst"), "AudioManager 應具備 play_overwind_burst 方法")
		am.call("play_overwind_burst")
		am.call("on_battle_event", "overwind_burst", {"id": "player"})
		print("  [PASS] AudioManager 成功接收並播放 overwind_burst 音效")
	else:
		print("  [SKIP] AudioManager autoload 不在單元測試樹中，略過直接播放")


func _test_six_locales() -> void:
	print("\n--- 3. 驗證六語系同步提示與零系統 emoji ---")
	_loc_node = root.get_node_or_null("Loc")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var check_keys := [
		"發條超載爆裂！",
		"發條超載爆裂",
		"超載爆裂！",
		"[color=#ffcc00]發條超載爆裂！轉數全滿 · 金屬狂暴！[/color]"
	]

	for lc in locales:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", lc)
		for k in check_keys:
			var translated: String = ContentLoc.text("ui", k)
			assert(translated != "", "[%s] key '%s' 翻譯不可為空" % [lc, k])
			if lc == "en":
				assert("Overwind Burst" in translated, "[en] 應包含 Overwind Burst 英文譯名: %s" % translated)
			elif lc == "ja":
				assert("ぜんまい" in translated or "過負荷" in translated, "[ja] 應包含日文譯名: %s" % translated)
			elif lc == "ko":
				assert("태엽" in translated or "과부하" in translated, "[ko] 應包含韓文譯名: %s" % translated)
			elif lc == "es":
				assert("Sobrecarga" in translated, "[es] 應包含西文譯名: %s" % translated)
			# 檢驗 0 系統 emoji
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 不准包含系統 emoji: %s" % [lc, translated])

	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")
	print("  [PASS] 六語系字典齊全、動態切換正常且 100% 零系統 emoji")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			print("\n--- 4. 建立 BattleView 實例並驗證節點與觸發 ---")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			_step = 2
			_wait = 0
		2:
			if _wait == 2:
				_battle.call("setup", "leo")
			if _wait < 5:
				return false
			var vig: TextureRect = _battle.get_node_or_null("OverwindVignette") as TextureRect
			var sparks: CPUParticles2D = _battle.get_node_or_null("BurstSparks") as CPUParticles2D
			var gears: CPUParticles2D = _battle.get_node_or_null("BurstGears") as CPUParticles2D
			var bnr: Label = _battle.get_node_or_null("OverwindBanner") as Label

			assert(vig != null, "應具備 OverwindVignette 節點")
			assert(sparks != null, "應具備 BurstSparks 節點")
			assert(gears != null, "應具備 BurstGears 節點")
			assert(bnr != null, "應具備 OverwindBanner 節點")
			assert(vig.texture != null, "暗角 Overlay 必須具備有效漸層紋理")

			# 觸發超載爆裂
			_battle.call("trigger_overwind_burst", "unit_test")

			assert(vig.visible, "觸發瞬間暗角 Overlay 必須可見")
			assert(sparks.emitting, "金色火花粒子必須開始噴射")
			assert(gears.emitting, "齒輪粒子必須開始噴射")
			assert(bnr.visible, "超載橫幅必須彈出")
			var cur_shake: float = float(_battle.get("_shake"))
			assert(cur_shake >= 0.3, "螢幕震動 shake 必須 >= 0.3 (實際: %f)" % cur_shake)

			print("  [PASS] BattleView 0.3秒暗角、震動、粒子噴射與橫幅全數正常啟用")
			_step = 3
			_wait = 0
		3:
			if _wait < 5:
				return false
			if is_instance_valid(_battle):
				_battle.queue_free()
			print("\nTEST_COMBAT_OVERWIND_BURST_OK")
			quit(0)
			return false
	return false
