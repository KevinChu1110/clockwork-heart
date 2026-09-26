extends Node
## 機芯部件與八色階校準系統 (CoreSystem)
## 遵循 CORE_LOOP_REVAMP_PROPOSAL 支柱二與 PRODUCT_LOCK 規範：
## 1. 分數對應八色階：灰(<0) 白(0) 橘(1~4) 藍(5~22) 紫(23~39) 金(40~54) 綠(55~69) 紅(70+)
## 2. 每個機芯部件最多校準 7 次，第 8 次校準被拒絕
## 3. 校準失敗不刪裝備、不碎裝（安全彈簧保底機制）
## 4. 五槽名稱固定：發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心
## 5. 硬限制：數值只准動 ATK/DEF/HP/CRIT/CRIT_DMG；不准動 ATB、攻速、前搖、命中等時間模型

const MAX_CALIBRATIONS: int = 7

signal part_calibrated(slot_id: String, part: Dictionary, result: Dictionary)

static var player_parts: Dictionary = {}

const SLOT_MAINSPRING: String = "mainspring"
const SLOT_CHASSIS: String = "chassis"
const SLOT_ESCAPEMENT: String = "escapement"
const SLOT_GEAR_TRAIN: String = "gear_train"
const SLOT_SOUL_CORE: String = "soul_core"

const ALL_SLOT_IDS: Array[String] = [
	SLOT_MAINSPRING,
	SLOT_CHASSIS,
	SLOT_ESCAPEMENT,
	SLOT_GEAR_TRAIN,
	SLOT_SOUL_CORE
]

const SLOT_NAMES: Dictionary = {
	SLOT_MAINSPRING: "發條發電機",
	SLOT_CHASSIS: "機殼裝甲",
	SLOT_ESCAPEMENT: "擒縱調速器",
	SLOT_GEAR_TRAIN: "傳動齒輪組",
	SLOT_SOUL_CORE: "共鳴核心"
}

const SLOT_NAMES_EN: Dictionary = {
	SLOT_MAINSPRING: "Mainspring Dynamo",
	SLOT_CHASSIS: "Chassis Armor",
	SLOT_ESCAPEMENT: "Escapement Regulator",
	SLOT_GEAR_TRAIN: "Gear Train Assembly",
	SLOT_SOUL_CORE: "Resonance Core"
}

const TIER_GRAY: String = "gray"
const TIER_WHITE: String = "white"
const TIER_ORANGE: String = "orange"
const TIER_BLUE: String = "blue"
const TIER_PURPLE: String = "purple"
const TIER_GOLD: String = "gold"
const TIER_GREEN: String = "green"
const TIER_RED: String = "red"

const ALL_TIER_IDS: Array[String] = [
	TIER_GRAY,
	TIER_WHITE,
	TIER_ORANGE,
	TIER_BLUE,
	TIER_PURPLE,
	TIER_GOLD,
	TIER_GREEN,
	TIER_RED
]

const TIER_NAMES: Dictionary = {
	TIER_GRAY: "灰",
	TIER_WHITE: "白",
	TIER_ORANGE: "橘",
	TIER_BLUE: "藍",
	TIER_PURPLE: "紫",
	TIER_GOLD: "金",
	TIER_GREEN: "綠",
	TIER_RED: "紅"
}

const TIER_HEXES: Dictionary = {
	TIER_GRAY: "#8E8E93",
	TIER_WHITE: "#FFFFFF",
	TIER_ORANGE: "#FFA010",
	TIER_BLUE: "#38A0FF",
	TIER_PURPLE: "#A855F7",
	TIER_GOLD: "#FFD028",
	TIER_GREEN: "#4ED86A",
	TIER_RED: "#FF5E8A"
}

const TIER_COLORS: Dictionary = {
	TIER_GRAY: Color(0.557, 0.557, 0.576, 1.0),
	TIER_WHITE: Color(1.0, 1.0, 1.0, 1.0),
	TIER_ORANGE: Color(1.0, 0.627, 0.063, 1.0),
	TIER_BLUE: Color(0.22, 0.627, 1.0, 1.0),
	TIER_PURPLE: Color(0.659, 0.333, 0.969, 1.0),
	TIER_GOLD: Color(1.0, 0.816, 0.157, 1.0),
	TIER_GREEN: Color(0.306, 0.847, 0.416, 1.0),
	TIER_RED: Color(1.0, 0.369, 0.541, 1.0)
}

## 硬限制准入數值清單：只准動 ATK/DEF/HP/CRIT/CRIT_DMG
const ALLOWED_STATS: Array[String] = ["ATK", "DEF", "HP", "CRIT", "CRIT_DMG"]

## 硬限制嚴禁更動之時間模型數值
const PROHIBITED_STATS: Array[String] = [
	"ATB",
	"SPEED",
	"ATTACK_SPEED",
	"WINDUP",
	"HIT",
	"MISS",
	"CAST_TIME",
	"RECOVERY_TIME"
]

const TABLE_PATH: String = "res://data/tables/core_color_tiers.json"


func _ready() -> void:
	pass


## 檢查數值是否在白名單內（ATK/DEF/HP/CRIT/CRIT_DMG）
static func is_stat_allowed(stat: String) -> bool:
	var s := stat.strip_edges().to_upper()
	return s in ALLOWED_STATS


## 檢查數值是否為被鎖定的時間模型數值
static func is_stat_prohibited(stat: String) -> bool:
	var s := stat.strip_edges().to_upper()
	return s in PROHIBITED_STATS or not (s in ALLOWED_STATS)


## 依校準分數對上八色階：灰(<0) 白(0) 橘(1~4) 藍(5~22) 紫(23~39) 金(40~54) 綠(55~69) 紅(70+)
static func get_tier_by_score(score: int) -> Dictionary:
	var tier_id := ""
	var min_score: Variant = null
	var max_score: Variant = null
	var desc := ""

	if score < 0:
		tier_id = TIER_GRAY
		min_score = null
		max_score = -1
		desc = "失調機芯（分數 < 0）"
	elif score == 0:
		tier_id = TIER_WHITE
		min_score = 0
		max_score = 0
		desc = "出廠白板（分數 0）"
	elif score >= 1 and score <= 4:
		tier_id = TIER_ORANGE
		min_score = 1
		max_score = 4
		desc = "微調部件（分數 1~4）"
	elif score >= 5 and score <= 22:
		tier_id = TIER_BLUE
		min_score = 5
		max_score = 22
		desc = "標準部件（分數 5~22）"
	elif score >= 23 and score <= 39:
		tier_id = TIER_PURPLE
		min_score = 23
		max_score = 39
		desc = "精準部件（分數 23~39）"
	elif score >= 40 and score <= 54:
		tier_id = TIER_GOLD
		min_score = 40
		max_score = 54
		desc = "卓越部件（分數 40~54）"
	elif score >= 55 and score <= 69:
		tier_id = TIER_GREEN
		min_score = 55
		max_score = 69
		desc = "完美部件（分數 55~69）"
	else: # score >= 70
		tier_id = TIER_RED
		min_score = 70
		max_score = null
		desc = "極限超越（分數 70+）"

	var c: Color = TIER_COLORS.get(tier_id, Color.WHITE)
	return {
		"id": tier_id,
		"name": TIER_NAMES.get(tier_id, tier_id),
		"hex": TIER_HEXES.get(tier_id, "#FFFFFF"),
		"color": c,
		"modulate": c,
		"min_score": min_score,
		"max_score": max_score,
		"desc": desc
	}


## 取得色階 modulate Color
static func get_tier_color(tier_id: String) -> Color:
	return TIER_COLORS.get(tier_id, Color.WHITE)


## 取得分數對應之 modulate Color
static func get_tier_modulate(score: int) -> Color:
	var info := get_tier_by_score(score)
	return info.get("modulate", Color.WHITE)


## 取得槽位中文名
static func get_slot_name(slot_id: String) -> String:
	return str(SLOT_NAMES.get(slot_id, slot_id))


## 取得五槽完整定義表
static func get_slot_defs() -> Dictionary:
	var res := {}
	for sid in ALL_SLOT_IDS:
		res[sid] = {
			"id": sid,
			"name": SLOT_NAMES.get(sid, sid),
			"name_en": SLOT_NAMES_EN.get(sid, sid)
		}
	return res


## 建立全新機芯部件資料結構
static func create_part(slot_id: String, initial_score: int = 0, initial_stats: Dictionary = {}) -> Dictionary:
	if not (slot_id in ALL_SLOT_IDS):
		push_warning("未知機芯槽位：%s" % slot_id)

	# 驗證 initial_stats，若含非法屬性則排除
	var sanitized_stats := {}
	for k in initial_stats.keys():
		var sk := str(k).to_upper()
		if is_stat_allowed(sk):
			sanitized_stats[sk] = initial_stats[k]
		else:
			push_warning("機芯部件初始數值含有不合規屬性：%s，已自動過濾" % sk)

	var tier_info := get_tier_by_score(initial_score)
	return {
		"uid": "core_%s_%d" % [slot_id, Time.get_unix_time_from_system() * 1000 + randi() % 1000],
		"slot": slot_id,
		"slot_name": get_slot_name(slot_id),
		"score": initial_score,
		"tier": tier_info.get("id", TIER_WHITE),
		"tier_name": tier_info.get("name", "白"),
		"calibration_count": 0,
		"max_calibrations": MAX_CALIBRATIONS,
		"stats": sanitized_stats,
		"is_broken": false,
		"history": []
	}


## 檢查機芯部件是否還能進行校準
static func can_calibrate(part: Dictionary) -> bool:
	if part == null or part.is_empty():
		return false
	if bool(part.get("is_broken", false)):
		return false
	return int(part.get("calibration_count", 0)) < MAX_CALIBRATIONS


## 對機芯部件進行校準
## roll_success: 本次校準判定是否成功
## stat_delta: 成功或微調時變動的數值（只准含 ATK/DEF/HP/CRIT/CRIT_DMG）
## score_delta: 變動的分數
## 回傳結果包含 ok, rejected, code, part, calibration_count, is_broken 等
static func calibrate(part: Dictionary, roll_success: bool = true, stat_delta: Dictionary = {}, score_delta: int = 0) -> Dictionary:
	if part == null or part.is_empty():
		return {
			"ok": false,
			"rejected": true,
			"code": "INVALID_PART",
			"message": "無效的部件資料",
			"part": part
		}

	var current_count: int = int(part.get("calibration_count", 0))

	# 規則 2：每個機芯部件最多校準 7 次，第 8 次校準被拒絕
	if current_count >= MAX_CALIBRATIONS:
		return {
			"ok": false,
			"rejected": true,
			"code": "MAX_CALIBRATION_REACHED",
			"message": "已達最大校準次數上限（%d 次），無法再校準" % MAX_CALIBRATIONS,
			"part": part,
			"calibration_count": current_count,
			"is_broken": bool(part.get("is_broken", false)),
			"destroyed": false
		}

	# 硬限制檢驗：數值只准動 ATK/DEF/HP/CRIT/CRIT_DMG
	for sk in stat_delta.keys():
		var s_upper := str(sk).to_upper()
		if not is_stat_allowed(s_upper):
			return {
				"ok": false,
				"rejected": true,
				"code": "PROHIBITED_STAT",
				"message": "數值只准動 ATK/DEF/HP/CRIT/CRIT_DMG，嚴禁更動時間模型（%s）" % sk,
				"part": part,
				"calibration_count": current_count,
				"is_broken": bool(part.get("is_broken", false)),
				"destroyed": false
			}

	# 消耗 1 次校準機會
	current_count += 1
	part["calibration_count"] = current_count

	if roll_success:
		# 成功：套用數值與分數調整
		var stats: Dictionary = part.get("stats", {})
		for sk in stat_delta.keys():
			var s_upper := str(sk).to_upper()
			var cur_val = stats.get(s_upper, 0)
			stats[s_upper] = cur_val + stat_delta[sk]
		part["stats"] = stats

		var new_score: int = int(part.get("score", 0)) + score_delta
		part["score"] = new_score
		var tier_info := get_tier_by_score(new_score)
		part["tier"] = tier_info.get("id", TIER_WHITE)
		part["tier_name"] = tier_info.get("name", "白")
		part["is_broken"] = false

		var entry := {
			"attempt": current_count,
			"success": true,
			"score_delta": score_delta,
			"stat_delta": stat_delta.duplicate(),
			"new_score": new_score,
			"new_tier": part["tier"]
		}
		var hist: Array = part.get("history", [])
		hist.append(entry)
		part["history"] = hist

		return {
			"ok": true,
			"rejected": false,
			"code": "SUCCESS",
			"message": "發條校準成功",
			"part": part,
			"calibration_count": current_count,
			"is_broken": false,
			"destroyed": false
		}
	else:
		# 規則 3：校準失敗不刪裝備、不碎裝（安全彈簧保護）
		part["is_broken"] = false

		var entry := {
			"attempt": current_count,
			"success": false,
			"score_delta": 0,
			"stat_delta": {},
			"new_score": part.get("score", 0),
			"new_tier": part.get("tier", TIER_WHITE)
		}
		var hist: Array = part.get("history", [])
		hist.append(entry)
		part["history"] = hist

		return {
			"ok": false,
			"rejected": false,
			"code": "CALIBRATION_FAILED",
			"message": "校準未達標，安全彈簧啟動：裝備完好無損，不碎裝",
			"part": part,
			"calibration_count": current_count,
			"is_broken": false,
			"destroyed": false
		}


## 標準槽位預設數值
static func get_slot_default_stats(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	match norm:
		SLOT_MAINSPRING:
			return {"ATK": 10, "HP": 30}
		SLOT_CHASSIS:
			return {"DEF": 10, "HP": 50}
		SLOT_ESCAPEMENT:
			return {"CRIT": 2, "CRIT_DMG": 4}
		SLOT_GEAR_TRAIN:
			return {"ATK": 6, "DEF": 6}
		SLOT_SOUL_CORE:
			return {"HP": 40, "ATK": 5, "DEF": 5}
	return {"ATK": 5}


## 正規化槽位識別碼（相容 SpriteDB 與 CoreSystem 命名）
static func normalize_slot_id(slot_id: String) -> String:
	match str(slot_id).strip_edges().to_lower():
		"mainspring", "spring_generator", "slot_01", "generator", "發條發電機", "0":
			return SLOT_MAINSPRING
		"chassis", "chassis_armor", "slot_02", "armor", "機殼裝甲", "1":
			return SLOT_CHASSIS
		"escapement", "escapement_governor", "slot_03", "governor", "擒縱調速器", "2":
			return SLOT_ESCAPEMENT
		"gear_train", "transmission_gears", "slot_04", "gears", "傳動齒輪組", "3":
			return SLOT_GEAR_TRAIN
		"soul_core", "resonance_core", "slot_05", "core", "共鳴核心", "4":
			return SLOT_SOUL_CORE
		_:
			return slot_id


## 取得玩家槽位機芯部件（若無則自動初始化白板）
static func get_player_part(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	if not player_parts.has(norm):
		var base_stats := get_slot_default_stats(norm)
		player_parts[norm] = create_part(norm, 0, base_stats)
	return player_parts[norm]


## 取得所有五槽玩家部件
static func get_all_player_parts() -> Dictionary:
	var res := {}
	for sid in ALL_SLOT_IDS:
		res[sid] = get_player_part(sid)
	return res


## 重置玩家部件（測試或新遊戲用）
static func reset_player_parts() -> void:
	player_parts.clear()


## 執行玩家機芯部件單次校準
## roll_success: null 為預設成功，可顯式指定 true/false
static func calibrate_player_part(slot_id: String, roll_success: Variant = null, stat_delta: Dictionary = {}, score_delta: int = 0) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var part := get_player_part(norm)

	if not can_calibrate(part):
		return {
			"ok": false,
			"rejected": true,
			"code": "MAX_CALIBRATION_REACHED",
			"message": "已達最大校準次數上限（7 次），無法再校準",
			"part": part,
			"calibration_count": int(part.get("calibration_count", MAX_CALIBRATIONS)),
			"is_broken": bool(part.get("is_broken", false)),
			"destroyed": false
		}

	var is_success: bool = true
	if roll_success != null:
		is_success = bool(roll_success)

	var final_stats := stat_delta.duplicate()
	var final_score_delta := score_delta

	if is_success and final_stats.is_empty() and final_score_delta == 0:
		final_score_delta = 6
		match norm:
			SLOT_MAINSPRING:
				final_stats = {"ATK": 3, "HP": 10}
			SLOT_CHASSIS:
				final_stats = {"DEF": 3, "HP": 15}
			SLOT_ESCAPEMENT:
				final_stats = {"CRIT": 1, "CRIT_DMG": 2}
			SLOT_GEAR_TRAIN:
				final_stats = {"ATK": 2, "DEF": 2}
			SLOT_SOUL_CORE:
				final_stats = {"ATK": 2, "DEF": 2, "HP": 15}
			_:
				final_stats = {"ATK": 2}

	var res := calibrate(part, is_success, final_stats, final_score_delta)
	player_parts[norm] = part

	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var cs: Node = (loop as SceneTree).root.get_node_or_null("CoreSystem")
		if cs and cs.has_signal("part_calibrated"):
			cs.emit_signal("part_calibrated", norm, part, res)

	return res

