class_name ClockworkEnergyPrototype
extends RefCounted
## 戰鬥原型：發條能量條分配機制（數值與戰鬥邏輯層）
## 特色：四職業共用單一發條能量池；滿額時開啟短暫倒數視窗；
## 支援手動挑選或超時自動智慧分配（保證絕不卡關）。

signal state_changed()
signal allocation_started(countdown_sec: float)
signal allocation_completed(profession_id: String, hero_name: String, is_auto: bool, skill_name: String)
signal combat_log_added(text: String, is_highlight: bool)
signal battle_ended(won: bool)

## 共用發條能量設定
const MAX_SHARED_ENERGY := 100.0
const ALLOCATION_THRESHOLD := 50.0  ## 達到此門檻即可觸發技能分配
const ALLOCATION_COST := 50.0       ## 每次分配消耗能量
const COUNTDOWN_SECONDS := 3.5      ## 手動決策時間（秒）

## 戰鬥狀態
var shared_energy: float = 0.0
var is_allocating: bool = false
var allocation_countdown: float = 0.0
var battle_over: bool = false
var battle_won: bool = false
var elapsed_battle_time: float = 0.0
var energy_regen_mult: float = 1.0
var energy_regen_buff_timer: float = 0.0

## 隊伍英雄（四職業）
var heroes: Dictionary = {}
## 敵方守衛
var enemy: Dictionary = {}

## 戰鬥紀錄
var combat_logs: Array[Dictionary] = []

## 統計數據（用於驗證與回報分析）
var stats: Dictionary = {
	"total_allocations": 0,
	"manual_allocations": 0,
	"auto_allocations": 0,
	"hero_picks": {
		"swordsman": 0,
		"knight": 0,
		"mage": 0,
		"warrior": 0
	},
	"stall_count": 0,        ## 發生卡住次數（預期永遠為 0）
	"total_damage_dealt": 0,
	"total_damage_taken": 0
}


func _init() -> void:
	reset_battle()


## 重置戰鬥原型數據
func reset_battle() -> void:
	shared_energy = 15.0  ## 開場給予少量啟動能量
	is_allocating = false
	allocation_countdown = 0.0
	battle_over = false
	battle_won = false
	elapsed_battle_time = 0.0
	energy_regen_mult = 1.0
	energy_regen_buff_timer = 0.0

	heroes = {
		"swordsman": {
			"id": "swordsman",
			"name": "兔小白",
			"profession": "劍士",
			"weapon": "單手長劍",
			"role_desc": "單體爆發輸出",
			"max_hp": 800,
			"hp": 800,
			"atk": 95,
			"speed": 1.2,
			"action_timer": 0.0,
			"skill_name": "疾風穿刺",
			"skill_desc": "對目標發動高速三連刺，造成 320 點暴擊傷害",
			"shield": 0
		},
		"knight": {
			"id": "knight",
			"name": "獅子",
			"profession": "騎士",
			"weapon": "皇家長槍",
			"role_desc": "團隊護盾與嘲諷",
			"max_hp": 1200,
			"hp": 1200,
			"atk": 50,
			"speed": 0.9,
			"action_timer": 0.0,
			"skill_name": "銅壁聖盾",
			"skill_desc": "為全隊展開 400 點發條護盾，並吸引首領仇恨",
			"shield": 0
		},
		"mage": {
			"id": "mage",
			"name": "狐狸",
			"profession": "法師",
			"weapon": "星屑法杖",
			"role_desc": "元素群攻與共鳴充能",
			"max_hp": 650,
			"hp": 650,
			"atk": 75,
			"speed": 1.0,
			"action_timer": 0.0,
			"skill_name": "星屑共鳴",
			"skill_desc": "轟擊敵方造成 180 點魔法傷害，並使全隊發條回能加速 50%",
			"shield": 0
		},
		"warrior": {
			"id": "warrior",
			"name": "野豬",
			"profession": "戰士",
			"weapon": "重錘",
			"role_desc": "重錘硬直與破甲削弱",
			"max_hp": 950,
			"hp": 950,
			"atk": 65,
			"speed": 0.85,
			"action_timer": 0.0,
			"skill_name": "撼地破甲",
			"skill_desc": "巨錘猛擊地面造成 220 點衝擊，粉碎目標 50% 護甲持續 6 秒",
			"shield": 0
		}
	}

	enemy = {
		"name": "發條巨像·零號守衛",
		"max_hp": 3600,
		"hp": 3600,
		"atk": 85,
		"armor": 60,
		"max_armor": 60,
		"armor_break_timer": 0.0,
		"speed": 0.7,
		"action_timer": 0.0,
		"telegraph_timer": 0.0,
		"is_telegraphing": false
	}

	combat_logs.clear()
	add_log("【戰鬥開始】四職業小隊遭遇發條巨像！共用發條能量系統已啟動。", true)


## 新增戰鬥紀錄
func add_log(msg: String, is_highlight: bool = false) -> void:
	var entry := {
		"time": elapsed_battle_time,
		"text": msg,
		"highlight": is_highlight
	}
	combat_logs.append(entry)
	if combat_logs.size() > 50:
		combat_logs.pop_front()
	combat_log_added.emit(msg, is_highlight)


## 推進戰鬥邏輯一步（秒數 delta）
func update(delta: float) -> void:
	if battle_over:
		return

	elapsed_battle_time += delta

	## 若正處於技能分配倒數視窗
	if is_allocating:
		allocation_countdown -= delta
		if allocation_countdown <= 0.0:
			## 逾時！自動智慧分配，保證絕對不卡關！
			_execute_auto_allocation()
		state_changed.emit()
		return

	## 回能增益計時器
	if energy_regen_buff_timer > 0.0:
		energy_regen_buff_timer -= delta
		if energy_regen_buff_timer <= 0.0:
			energy_regen_mult = 1.0
			add_log("［能量狀態］星屑共鳴回能加速效果已結束。")

	## 敵方破甲計時器
	if enemy["armor_break_timer"] > 0.0:
		enemy["armor_break_timer"] -= delta
		if enemy["armor_break_timer"] <= 0.0:
			enemy["armor"] = enemy["max_armor"]
			add_log("［首領狀態］發條巨像的裝甲板件已自我修復完成。")

	## 自然與戰鬥蓄能
	var base_regen := 10.0 * energy_regen_mult * delta
	shared_energy = minf(MAX_SHARED_ENERGY, shared_energy + base_regen)

	## 英雄普通攻擊輪替
	for p_id in heroes.keys():
		var hero: Dictionary = heroes[p_id]
		if hero["hp"] <= 0:
			continue
		hero["action_timer"] += delta * hero["speed"]
		if hero["action_timer"] >= 2.0:
			hero["action_timer"] -= 2.0
			_hero_basic_attack(p_id)

	## 敵方普通攻擊 / 蓄力攻擊
	enemy["action_timer"] += delta * enemy["speed"]
	if enemy["action_timer"] >= 3.5:
		enemy["action_timer"] -= 3.5
		_enemy_attack()

	## 檢查是否達成能量分配條件
	if shared_energy >= ALLOCATION_THRESHOLD and not is_allocating:
		_trigger_allocation_window()

	state_changed.emit()


## 觸發能量分配視窗
func _trigger_allocation_window() -> void:
	is_allocating = true
	allocation_countdown = COUNTDOWN_SECONDS
	add_log("【發條過載】共用能量池已滿額！請在 %.1f 秒內指派技能施放對象！" % COUNTDOWN_SECONDS, true)
	allocation_started.emit(COUNTDOWN_SECONDS)


## 手動選擇分配對象
func allocate_manual(profession_id: String) -> bool:
	if not is_allocating:
		return false
	if not heroes.has(profession_id):
		return false
	if heroes[profession_id]["hp"] <= 0:
		add_log("［提示］該角色已損壞癱瘓，無法分配能量！")
		return false

	stats["total_allocations"] += 1
	stats["manual_allocations"] += 1
	stats["hero_picks"][profession_id] += 1

	_apply_allocation(profession_id, false)
	return true


## 倒數結束：自動智慧分配（保證永不卡關）
func _execute_auto_allocation() -> void:
	stats["total_allocations"] += 1
	stats["auto_allocations"] += 1

	var target_id := pick_smart_fallback_target()
	stats["hero_picks"][target_id] += 1

	_apply_allocation(target_id, true)


## 智慧保底挑選策略
## 1. 隊友殘血急需護盾 -> 騎士
## 2. 首領護甲尚存且未破甲 -> 戰士破甲
## 3. 回能增益中斷且隊伍良好 -> 法師加速
## 4. 其餘情況 -> 劍士爆發極限輸出
func pick_smart_fallback_target() -> String:
	## 1. 救急檢查：任一隊員血量低於 45% 且騎士存活
	for p_id in heroes.keys():
		var h: Dictionary = heroes[p_id]
		if h["hp"] > 0 and float(h["hp"]) / float(h["max_hp"]) < 0.45:
			if heroes["knight"]["hp"] > 0:
				return "knight"

	## 2. 破甲檢查：首領護甲 > 20 且戰士存活
	if enemy["armor"] > 20 and heroes["warrior"]["hp"] > 0:
		return "warrior"

	## 3. 回能加速檢查：若尚無法師加速且法師存活
	if energy_regen_buff_timer <= 0.0 and heroes["mage"]["hp"] > 0:
		return "mage"

	## 4. 預設單體爆發輸出
	if heroes["swordsman"]["hp"] > 0:
		return "swordsman"

	## 備援：挑選第一個存活的英雄
	for p_id in heroes.keys():
		if heroes[p_id]["hp"] > 0:
			return p_id

	return "swordsman"


## 執行分配並施放專屬技能
func _apply_allocation(profession_id: String, is_auto: bool) -> void:
	var hero: Dictionary = heroes[profession_id]
	shared_energy = maxf(0.0, shared_energy - ALLOCATION_COST)
	is_allocating = false
	allocation_countdown = 0.0

	var prefix := "［系統自動分配］" if is_auto else "［手動精準分配］"
	add_log("%s 能量成功注入【%s·%s】，施放絕技【%s】！" % [
		prefix, hero["profession"], hero["name"], hero["skill_name"]
	], true)

	match profession_id:
		"swordsman":
			## 劍士：疾風穿刺（320 點高額傷害）
			var def_mitigation: float = float(enemy["armor"]) * 0.5
			var dmg: int = maxi(120, int(360.0 - def_mitigation))
			_damage_enemy(dmg, "兔小白的疾風穿刺貫穿巨像核心！")
		"knight":
			## 騎士：銅壁聖盾（全體 400 護盾）
			for p_id in heroes.keys():
				if heroes[p_id]["hp"] > 0:
					heroes[p_id]["shield"] += 400
			add_log("獅子舉起發條重盾，為全體隊友展開 400 點高能防禦矩陣！")
		"mage":
			## 法師：星屑共鳴（180 傷害 + 充能加速）
			_damage_enemy(180, "狐狸詠唱星屑法陣，引發魔力共振！")
			energy_regen_mult = 1.6
			energy_regen_buff_timer = 7.0
			add_log("全隊發條運轉齒輪加速咬合，能量獲取速度提升 60%（持續 7 秒）！")
		"warrior":
			## 戰士：撼地破甲（220 傷害 + 破甲）
			_damage_enemy(220, "野豬揮舞重錘粉碎地面，震裂巨像裝甲！")
			enemy["armor"] = 0
			enemy["armor_break_timer"] = 7.0
			add_log("巨像裝甲板件全面崩解！進入易傷破甲狀態（持續 7 秒）！")

	allocation_completed.emit(profession_id, hero["name"], is_auto, hero["skill_name"])


## 英雄普通攻擊
func _hero_basic_attack(profession_id: String) -> void:
	var hero: Dictionary = heroes[profession_id]
	var dmg: int = maxi(15, int(hero["atk"] - (enemy["armor"] * 0.3)))
	_damage_enemy(dmg, "%s·%s 揮舞 %s 進行普通斬擊。" % [hero["profession"], hero["name"], hero["weapon"]])
	## 普攻額外微量回能
	shared_energy = minf(MAX_SHARED_ENERGY, shared_energy + 4.0)


## 敵方普通攻擊
func _enemy_attack() -> void:
	## 挑選目標：優先打前排騎士或隨機存活隊員
	var alive_targets: Array[String] = []
	for p_id in heroes.keys():
		if heroes[p_id]["hp"] > 0:
			alive_targets.append(p_id)

	if alive_targets.is_empty():
		_check_battle_end()
		return

	var target_id: String = "knight"
	if heroes["knight"]["hp"] <= 0 or randf() < 0.35:
		target_id = alive_targets.pick_random()

	var target: Dictionary = heroes[target_id]
	var raw_dmg: int = enemy["atk"]
	var actual_dmg := raw_dmg

	## 護盾吸收
	if target["shield"] > 0:
		if target["shield"] >= actual_dmg:
			target["shield"] -= actual_dmg
			add_log("發條巨像重擊【%s】，護盾完全抵擋了 %d 點傷害！" % [target["name"], actual_dmg])
			actual_dmg = 0
		else:
			actual_dmg -= target["shield"]
			add_log("發條巨像擊破【%s】的護盾，造成餘威 %d 點傷害！" % [target["name"], actual_dmg])
			target["shield"] = 0

	if actual_dmg > 0:
		target["hp"] = maxi(0, target["hp"] - actual_dmg)
		stats["total_damage_taken"] += actual_dmg
		add_log("發條巨像揮舞巨拳命中【%s·%s】，造成 %d 點損傷！" % [target["profession"], target["name"], actual_dmg])
		if target["hp"] <= 0:
			add_log("警報！【%s·%s】發條崩解暫時失去行動能力！" % [target["profession"], target["name"]], true)

	_check_battle_end()


## 傷害敵方
func _damage_enemy(dmg: int, detail: String) -> void:
	enemy["hp"] = maxi(0, enemy["hp"] - dmg)
	stats["total_damage_dealt"] += dmg
	add_log("敵方受到 %d 點傷害！（%s）" % [dmg, detail])
	_check_battle_end()


## 結算勝負
func _check_battle_end() -> void:
	if battle_over:
		return

	if enemy["hp"] <= 0:
		battle_over = true
		battle_won = true
		add_log("✓【戰鬥勝利】發條巨像完全瓦解，齒輪四散！四職業能量協作成功！", true)
		battle_ended.emit(true)
		return

	var all_dead := true
	for p_id in heroes.keys():
		if heroes[p_id]["hp"] > 0:
			all_dead = false
			break

	if all_dead:
		battle_over = true
		battle_won = false
		add_log("✕【全隊癱瘓】小隊全體停擺，戰鬥失敗！", true)
		battle_ended.emit(false)
