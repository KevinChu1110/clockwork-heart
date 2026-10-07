extends SceneTree
## 單元測試：Boss 部位破壞掉落金色發條寶箱動效與機芯浮字提示 (爆點三規範驗證)
## 依據：docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點三, review.md 19b

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const BattleUnit := preload("res://scripts/battle/battle_unit.gd")
const CoreSystem := preload("res://scripts/systems/core_system.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const PartBreakChestFx := preload("res://scripts/battle/part_break_chest_fx.gd")

var _step: int = 0
var _wait: int = 0
var _battle: Control = null
var _loc_node: Node = null


func _initialize() -> void:
	print("=== 開始執行 test_boss_part_break_chest_fx ===")
	_test_core_slot_mappings()
	_test_chest_fx_component()
	_test_six_locales()
	_step = 1
	_wait = 0


func _test_core_slot_mappings() -> void:
	print("\n--- 1. 驗證 CoreSystem 部位至機芯五槽映射 (get_part_core_slot) ---")
	# 1.1 停擺巨偶三型態對照
	assert(CoreSystem.get_part_core_slot("colossus_lion", "溢能尖角", "spike") == CoreSystem.SLOT_MAINSPRING, "獅尖角應對應 mainspring")
	assert(CoreSystem.get_part_core_slot("colossus_lion", "溢能核心", "core") == CoreSystem.SLOT_SOUL_CORE, "獅核心應對應 soul_core")
	assert(CoreSystem.get_part_core_slot("colossus_puppet", "溢能尖角", "spike") == CoreSystem.SLOT_GEAR_TRAIN, "人偶尖角應對應 gear_train")
	assert(CoreSystem.get_part_core_slot("colossus_puppet", "溢能核心", "core") == CoreSystem.SLOT_ESCAPEMENT, "人偶核心應對應 escapement")
	assert(CoreSystem.get_part_core_slot("colossus_elephant", "溢能尖角", "spike") == CoreSystem.SLOT_CHASSIS, "巨象尖角應對應 chassis")
	assert(CoreSystem.get_part_core_slot("colossus_elephant", "溢能核心", "core") == CoreSystem.SLOT_SOUL_CORE, "巨象核心應對應 soul_core")

	# 1.2 常規章節 Boss 部位對照
	assert(CoreSystem.get_part_core_slot("leo", "獅衛重盔", "helm") == CoreSystem.SLOT_CHASSIS, "Leo 盔應對應 chassis")
	assert(CoreSystem.get_part_core_slot("leo", "獅衛重盾", "shield") == CoreSystem.SLOT_GEAR_TRAIN, "Leo 盾應對應 gear_train")
	assert(CoreSystem.get_part_core_slot("falcon", "疾影羽冠", "crest") == CoreSystem.SLOT_ESCAPEMENT, "Falcon 冠應對應 escapement")
	assert(CoreSystem.get_part_core_slot("falcon", "疾影雙翼", "wings") == CoreSystem.SLOT_ESCAPEMENT, "Falcon 翼應對應 escapement")
	assert(CoreSystem.get_part_core_slot("boar", "石角堅岩", "horn") == CoreSystem.SLOT_MAINSPRING, "Boar 角應對應 mainspring")
	assert(CoreSystem.get_part_core_slot("boar", "岩甲外殼", "shell") == CoreSystem.SLOT_CHASSIS, "Boar 殼應對應 chassis")
	assert(CoreSystem.get_part_core_slot("demon", "黑鏽核心", "core") == CoreSystem.SLOT_SOUL_CORE, "Demon 核心應對應 soul_core")

	# 1.3 五槽中文名稱完整
	for sid in CoreSystem.ALL_SLOT_IDS:
		var snm: String = CoreSystem.get_slot_name(sid)
		assert(snm != "", "槽位 %s 中文名稱不可為空" % sid)
	print("  [PASS] 停擺巨偶與各章 Boss 部位 100% 精確映射至機芯五槽")


func _test_chest_fx_component() -> void:
	print("\n--- 2. 驗證 PartBreakChestFx 動效元件獨立節點結構與動畫 ---")
	var dummy_parent := Node2D.new()
	root.add_child(dummy_parent)

	var fx: PartBreakChestFx = PartBreakChestFx.play(dummy_parent, Vector2(640, 360), "發條發電機", CoreSystem.SLOT_MAINSPRING)
	assert(fx != null, "PartBreakChestFx.play 應成功建立實例")
	assert(fx.name == "BossPartBreakChestFx", "節點名稱應為 BossPartBreakChestFx")

	# 檢驗關鍵子節點
	var spr: Sprite2D = fx.get_node_or_null("ChestContainer/ChestSprite") as Sprite2D
	var key: Sprite2D = fx.get_node_or_null("ChestContainer/WindingKeyIcon") as Sprite2D
	var part: CPUParticles2D = fx.get_node_or_null("GoldParticles") as CPUParticles2D
	var shd: Polygon2D = fx.get_node_or_null("ChestShadow") as Polygon2D
	var lbl: Label = fx.get_node_or_null("CorePromptLabel") as Label

	assert(spr != null, "應具備 ChestSprite 寶箱貼圖節點")
	assert(key != null, "應具備 WindingKeyIcon 發條鑰匙節點")
	assert(part != null, "應具備 GoldParticles 金色流光粒子節點")
	assert(shd != null, "應具備 ChestShadow 軟陰影節點")
	assert(lbl != null, "應具備 CorePromptLabel 機芯提示浮字節點")

	assert(part.emitting, "金色流光粒子啟動時必須為 emitting")
	assert("發條發電機" in lbl.text, "提示標籤應包含對應機芯名稱 (實際: %s)" % lbl.text)

	# 零系統 emoji
	for ch in lbl.text:
		var cp: int = ch.unicode_at(0)
		assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "標籤文字不准包含系統 emoji: %s" % lbl.text)

	dummy_parent.queue_free()
	print("  [PASS] PartBreakChestFx 寶箱節點、發條鑰匙、金色粒子與提示浮字全數就緒")


func _test_six_locales() -> void:
	print("\n--- 3. 驗證六語系字典定義與零系統 emoji ---")
	_loc_node = root.get_node_or_null("Loc")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var check_keys := [
		"掉落部位機芯：%s",
		"【機芯掉落】%s",
		"部位擊破！掉落發光寶箱與機芯：【%s】",
		"金色發條寶箱",
		"發條發電機",
		"機殼裝甲",
		"擒縱調速器",
		"傳動齒輪組",
		"共鳴核心",
	]

	for lc in locales:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", lc)
		for k in check_keys:
			var translated: String = ContentLoc.text("ui", k)
			assert(translated != "", "[%s] key '%s' 翻譯不可為空" % [lc, k])
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 不准包含系統 emoji: %s" % [lc, translated])

	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")
	print("  [PASS] 六語系字典齊全且 100% 零系統 emoji")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			print("\n--- 4. 實例化戰鬥畫面 (BattleView) 並模擬 Boss 部位破壞事件 ---")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			_step = 2
			_wait = 0
		2:
			if _wait == 2:
				_battle.call("setup", "leo")
			if _wait < 6:
				return false

			# 模擬觸發部位破壞事件 (Leo 盔破壞 -> 對應機殼裝甲)
			var break_data := {
				"boss_id": "leo",
				"part_id": "helm",
				"part_name": "獅衛重盔",
				"raw_name": "獅衛重盔",
				"staggered": true,
				"material": "knight_shard",
				"qty": 1,
				"hp": 200,
				"max_hp": 400,
			}
			_battle.call("_on_event", "part_broken", break_data)

			# 驗證寶箱動效節點被正確生成於戰鬥視圖下
			var chest_fx: Node = _battle.find_child("BossPartBreakChestFx", true, false)
			assert(chest_fx != null, "部位破壞時應生成 BossPartBreakChestFx 節點")

			var fx_particles: CPUParticles2D = chest_fx.get_node_or_null("GoldParticles") as CPUParticles2D
			assert(fx_particles != null, "BossPartBreakChestFx 應包含 GoldParticles 粒子系統")

			var fx_label: Label = chest_fx.get_node_or_null("CorePromptLabel") as Label
			assert(fx_label != null, "BossPartBreakChestFx 應包含 CorePromptLabel 浮字標籤")
			assert("機殼裝甲" in fx_label.text or "機芯" in fx_label.text, "浮字標籤應包含對應機芯名稱 (實際: %s)" % fx_label.text)

			# 驗證畫面震動反饋
			var cur_shake: float = float(_battle.get("_shake"))
			assert(cur_shake >= 0.4, "部位破壞震動 shake 必須 >= 0.4 (實際: %f)" % cur_shake)

			print("  [PASS] BattleView 部位破壞觸發金色發條寶箱動效節點與機芯浮字提示 (成功)")
			_step = 3
			_wait = 0
		3:
			if _wait < 5:
				return false
			if is_instance_valid(_battle):
				_battle.queue_free()
			print("\nTEST_BOSS_PART_BREAK_CHEST_FX_OK")
			quit(0)
			return false
	return false
