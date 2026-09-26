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
signal part_dropped(part: Dictionary)

static var player_parts: Dictionary = {}
static var core_inventory: Array = []
static var inventory: Array = []

const DEFAULT_DROP_TIER_WEIGHTS: Dictionary = {
	"gray": 50,
	"white": 450,
	"orange": 240,
	"blue": 150,
	"purple": 60,
	"gold": 30,
	"green": 15,
	"red": 5,
}

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

const TIER_DEFAULT_SCORES: Dictionary = {
	TIER_GRAY: -1,
	TIER_WHITE: 0,
	TIER_ORANGE: 3,
	TIER_BLUE: 15,
	TIER_PURPLE: 30,
	TIER_GOLD: 45,
	TIER_GREEN: 60,
	TIER_RED: 75,
}

## 各槽位在八色階下的基礎靜態數值加成
## 嚴格遵循硬限制：只准動 ATK/DEF/HP/CRIT/CRIT_DMG，零時間模型改動
const TIER_BASE_STATS: Dictionary = {
	SLOT_MAINSPRING: {
		TIER_GRAY: {"ATK": 0, "HP": 5},
		TIER_WHITE: {"ATK": 2, "HP": 10},
		TIER_ORANGE: {"ATK": 4, "HP": 20},
		TIER_BLUE: {"ATK": 8, "HP": 40},
		TIER_PURPLE: {"ATK": 14, "HP": 70},
		TIER_GOLD: {"ATK": 22, "HP": 110},
		TIER_GREEN: {"ATK": 32, "HP": 160},
		TIER_RED: {"ATK": 45, "HP": 220},
	},
	SLOT_CHASSIS: {
		TIER_GRAY: {"DEF": 0, "HP": 5},
		TIER_WHITE: {"DEF": 2, "HP": 10},
		TIER_ORANGE: {"DEF": 4, "HP": 20},
		TIER_BLUE: {"DEF": 7, "HP": 40},
		TIER_PURPLE: {"DEF": 12, "HP": 70},
		TIER_GOLD: {"DEF": 18, "HP": 110},
		TIER_GREEN: {"DEF": 26, "HP": 160},
		TIER_RED: {"DEF": 36, "HP": 220},
	},
	SLOT_ESCAPEMENT: {
		TIER_GRAY: {"CRIT": 0.0, "CRIT_DMG": 0.0},
		TIER_WHITE: {"CRIT": 1.0, "CRIT_DMG": 2.0},
		TIER_ORANGE: {"CRIT": 2.0, "CRIT_DMG": 4.0},
		TIER_BLUE: {"CRIT": 3.5, "CRIT_DMG": 8.0},
		TIER_PURPLE: {"CRIT": 5.5, "CRIT_DMG": 13.0},
		TIER_GOLD: {"CRIT": 8.0, "CRIT_DMG": 20.0},
		TIER_GREEN: {"CRIT": 11.5, "CRIT_DMG": 28.0},
		TIER_RED: {"CRIT": 16.0, "CRIT_DMG": 38.0},
	},
	SLOT_GEAR_TRAIN: {
		TIER_GRAY: {"ATK": 0, "DEF": 0},
		TIER_WHITE: {"ATK": 2, "DEF": 1},
		TIER_ORANGE: {"ATK": 4, "DEF": 2},
		TIER_BLUE: {"ATK": 7, "DEF": 4},
		TIER_PURPLE: {"ATK": 12, "DEF": 7},
		TIER_GOLD: {"ATK": 18, "DEF": 11},
		TIER_GREEN: {"ATK": 26, "DEF": 16},
		TIER_RED: {"ATK": 36, "DEF": 22},
	},
	SLOT_SOUL_CORE: {
		TIER_GRAY: {"ATK": 0, "DEF": 0, "HP": 10, "CRIT": 0.0, "CRIT_DMG": 0.0},
		TIER_WHITE: {"ATK": 1, "DEF": 1, "HP": 20, "CRIT": 0.5, "CRIT_DMG": 1.0},
		TIER_ORANGE: {"ATK": 2, "DEF": 2, "HP": 40, "CRIT": 1.0, "CRIT_DMG": 2.0},
		TIER_BLUE: {"ATK": 4, "DEF": 4, "HP": 70, "CRIT": 2.0, "CRIT_DMG": 4.0},
		TIER_PURPLE: {"ATK": 7, "DEF": 7, "HP": 120, "CRIT": 3.5, "CRIT_DMG": 7.0},
		TIER_GOLD: {"ATK": 12, "DEF": 11, "HP": 180, "CRIT": 5.5, "CRIT_DMG": 11.0},
		TIER_GREEN: {"ATK": 18, "DEF": 16, "HP": 260, "CRIT": 8.0, "CRIT_DMG": 16.0},
		TIER_RED: {"ATK": 25, "DEF": 22, "HP": 360, "CRIT": 12.0, "CRIT_DMG": 24.0},
	},
}

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


## 正規化槽位代號（支援別名相容）
static func normalize_slot_id(slot_id: String) -> String:
	var s := slot_id.strip_edges().to_lower()
	match s:
		"spring_generator", "slot_01", "generator", "發條發電機", "0", "mainspring":
			return SLOT_MAINSPRING
		"chassis_armor", "slot_02", "armor", "機殼裝甲", "1", "chassis":
			return SLOT_CHASSIS
		"escapement_governor", "slot_03", "governor", "擒縱調速器", "2", "escapement":
			return SLOT_ESCAPEMENT
		"transmission_gears", "slot_04", "gears", "傳動齒輪組", "3", "gear_train":
			return SLOT_GEAR_TRAIN
		"resonance_core", "slot_05", "core", "共鳴核心", "4", "soul_core":
			return SLOT_SOUL_CORE
		_:
			return s


## 取得槽位中文名
static func get_slot_name(slot_id: String) -> String:
	var norm := normalize_slot_id(slot_id)
	return str(SLOT_NAMES.get(norm, slot_id))


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


static var _uid_counter: int = 0


## 建立全新機芯部件資料結構
static func create_part(slot_id: String, initial_score: int = 0, initial_stats: Dictionary = {}) -> Dictionary:
	var norm_slot := normalize_slot_id(slot_id)
	if not (norm_slot in ALL_SLOT_IDS):
		push_warning("未知機芯槽位：%s" % slot_id)

	# 驗證 initial_stats，若含非法屬性則排除
	var sanitized_stats := {}
	for k in initial_stats.keys():
		var sk := str(k).to_upper()
		if is_stat_allowed(sk):
			sanitized_stats[sk] = initial_stats[k]
		else:
			push_warning("機芯部件初始數值含有不合規屬性：%s，已自動過濾" % sk)

	_uid_counter += 1
	var tier_info := get_tier_by_score(initial_score)
	return {
		"uid": "core_%s_%d_%d" % [norm_slot, int(Time.get_unix_time_from_system() * 1000), _uid_counter],
		"slot": norm_slot,
		"slot_name": get_slot_name(norm_slot),
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


## 取得玩家槽位機芯部件（若無則自動初始化白板）
static func get_player_part(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			gs.ensure_core_slots("white")
			if gs.core_slots.has(norm):
				return gs.core_slots[norm]
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
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			gs.core_slots.clear()


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
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			gs.core_slots[norm] = part

	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var cs: Node = (loop as SceneTree).root.get_node_or_null("CoreSystem")
		if cs and cs.has_signal("part_calibrated"):
			cs.emit_signal("part_calibrated", norm, part, res)

	return res


## 取得指定槽位與色階的基礎數值加成
static func get_tier_base_stats(slot_id: String, tier_id: String) -> Dictionary:
	var norm_slot := normalize_slot_id(slot_id)
	var slot_tiers: Dictionary = TIER_BASE_STATS.get(norm_slot, {})
	var base: Dictionary = slot_tiers.get(tier_id, slot_tiers.get(TIER_WHITE, {}))
	return base.duplicate(true)


## 取得單一機芯部件的實質戰鬥加成數值（含色階基礎值與校準增量）
## 硬限制：僅產出 ATK/DEF/HP/CRIT/CRIT_DMG，零時間模型改動
static func get_part_stats(part: Dictionary) -> Dictionary:
	if part == null or part.is_empty():
		return {"atk": 0, "def": 0, "hp": 0, "crit": 0.0, "crit_dmg": 0.0}
	var slot_id := normalize_slot_id(str(part.get("slot", "")))
	var tier_id := str(part.get("tier", ""))
	if tier_id.is_empty():
		var sc: int = int(part.get("score", 0))
		tier_id = str(get_tier_by_score(sc).get("id", TIER_WHITE))
	var base := get_tier_base_stats(slot_id, tier_id)
	var rolled: Dictionary = part.get("stats", {})

	var atk_val: int = int(base.get("ATK", 0)) + int(rolled.get("ATK", 0))
	var def_val: int = int(base.get("DEF", 0)) + int(rolled.get("DEF", 0))
	var hp_val: int = int(base.get("HP", 0)) + int(rolled.get("HP", 0))
	var crit_val: float = float(base.get("CRIT", 0.0)) + float(rolled.get("CRIT", 0.0))
	var crit_dmg_val: float = float(base.get("CRIT_DMG", 0.0)) + float(rolled.get("CRIT_DMG", 0.0))

	return {
		"atk": atk_val,
		"def": def_val,
		"hp": hp_val,
		"crit": crit_val,
		"crit_dmg": crit_dmg_val
	}


## 彙整所有已裝備槽位部件的總戰鬥屬性加成
static func get_total_bonuses(slots: Dictionary) -> Dictionary:
	var total := {"atk": 0, "def": 0, "hp": 0, "crit": 0.0, "crit_dmg": 0.0}
	if slots == null or slots.is_empty():
		return total
	for sid in ALL_SLOT_IDS:
		var part: Variant = slots.get(sid, null)
		if part == null or typeof(part) != TYPE_DICTIONARY or (part as Dictionary).is_empty():
			for k in slots.keys():
				if normalize_slot_id(str(k)) == sid:
					part = slots[k]
					break
		if typeof(part) == TYPE_DICTIONARY and not (part as Dictionary).is_empty():
			var pstats: Dictionary = get_part_stats(part as Dictionary)
			total["atk"] = int(total["atk"]) + int(pstats.get("atk", 0))
			total["def"] = int(total["def"]) + int(pstats.get("def", 0))
			total["hp"] = int(total["hp"]) + int(pstats.get("hp", 0))
			total["crit"] = float(total["crit"]) + float(pstats.get("crit", 0.0))
			total["crit_dmg"] = float(total["crit_dmg"]) + float(pstats.get("crit_dmg", 0.0))
	return total


## 運行時彙總玩家當前裝備五槽機芯戰鬥加成
static func total_core_bonuses() -> Dictionary:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			return get_total_bonuses(gs.get("core_slots"))
	return {"atk": 0, "def": 0, "hp": 0, "crit": 0.0, "crit_dmg": 0.0}


## 快速建立出廠白板部件
static func create_white_part(slot_id: String) -> Dictionary:
	return create_part(slot_id, 0)


## 快速建立指定色階部件
static func create_part_by_tier(slot_id: String, tier_id: String, bonus_stats: Dictionary = {}) -> Dictionary:
	var norm_slot := normalize_slot_id(slot_id)
	var sc: int = int(TIER_DEFAULT_SCORES.get(tier_id, 0))
	return create_part(norm_slot, sc, bonus_stats)


## 裝備部件至 GameState.core_slots
static func equip_part(slot_id: String, part: Dictionary) -> bool:
	var norm := normalize_slot_id(slot_id)
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			gs.core_slots[norm] = part.duplicate(true)
			return true
	return false


## 卸下部件
static func unequip_part(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs and gs.core_slots.has(norm):
			var old: Dictionary = gs.core_slots[norm]
			gs.core_slots.erase(norm)
			return old
	return {}


## 取得已裝備部件
static func get_equipped_part(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs:
			return (gs.core_slots.get(norm, {}) as Dictionary).duplicate(true)
	return {}


## 取得八色階掉落機率權重表
static func get_drop_weights() -> Dictionary:
	var weights := DEFAULT_DROP_TIER_WEIGHTS.duplicate()
	if FileAccess.file_exists(TABLE_PATH):
		var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY and data.has("tiers") and typeof(data["tiers"]) == TYPE_ARRAY:
				for tdef in data["tiers"]:
					if typeof(tdef) == TYPE_DICTIONARY and tdef.has("id") and tdef.has("drop_weight"):
						weights[str(tdef["id"])] = int(tdef["drop_weight"])
	return weights


## 依權重隨機抽取八色階之一
static func roll_tier(rng: RandomNumberGenerator = null) -> String:
	var weights := get_drop_weights()
	var total_w: int = 0
	for tid in ALL_TIER_IDS:
		total_w += int(weights.get(tid, 0))
	if total_w <= 0:
		return TIER_WHITE
	var roll_val: int = rng.randi_range(1, total_w) if rng != null else (randi() % total_w + 1)
	var accum: int = 0
	for tid in ALL_TIER_IDS:
		accum += int(weights.get(tid, 0))
		if roll_val <= accum:
			return tid
	return TIER_WHITE


## 隨機抽取五槽之一
static func roll_slot(rng: RandomNumberGenerator = null) -> String:
	var idx: int = rng.randi_range(0, ALL_SLOT_IDS.size() - 1) if rng != null else (randi() % ALL_SLOT_IDS.size())
	return ALL_SLOT_IDS[idx]


## 隨機生成一顆五槽機芯戰利品部件（遵循 create_part 規格與八色階權重）
static func roll_battle_drop(rng: RandomNumberGenerator = null) -> Dictionary:
	var slot_id := roll_slot(rng)
	var tier_id := roll_tier(rng)
	return create_part_by_tier(slot_id, tier_id)


## 將機芯部件加入背包／庫存（同步 GameState.core_bag 與 CoreSystem.inventory）
static func add_part_to_inventory(part: Dictionary) -> void:
	if part == null or part.is_empty():
		return
	var part_copy: Dictionary = part.duplicate(true)
	var tree := Engine.get_main_loop()
	var gs: Node = null
	var cs: Node = null
	if tree is SceneTree and (tree as SceneTree).root != null:
		var root = (tree as SceneTree).root
		gs = root.get_node_or_null("GameState")
		cs = root.get_node_or_null("CoreSystem")

	if gs and gs.has_method("add_core_part"):
		gs.call("add_core_part", part_copy)
		core_inventory = gs.core_bag
		inventory = core_inventory
	else:
		core_inventory.append(part_copy)
		inventory = core_inventory

	if cs and cs.has_signal("part_dropped"):
		cs.emit_signal("part_dropped", part_copy)


## 取得當前機芯背包清單
static func get_inventory() -> Array:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_bag" in gs and typeof(gs.core_bag) == TYPE_ARRAY:
			core_inventory = gs.core_bag
			inventory = core_inventory
			return gs.core_bag
	inventory = core_inventory
	return core_inventory


## 清空機芯背包（測試用）
static func clear_inventory() -> void:
	core_inventory.clear()
	inventory.clear()
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if "core_bag" in gs and typeof(gs.core_bag) == TYPE_ARRAY:
				gs.core_bag.clear()
			if "core_inventory" in gs and typeof(gs.core_inventory) == TYPE_ARRAY:
				gs.core_inventory.clear()


## 從背包移除指定 uid 之部件
static func remove_part_from_inventory(part_uid: String) -> Dictionary:
	var removed := {}
	var tree := Engine.get_main_loop()
	var gs: Node = null
	if tree is SceneTree and (tree as SceneTree).root != null:
		gs = (tree as SceneTree).root.get_node_or_null("GameState")

	if gs and gs.has_method("remove_core_part"):
		var r = gs.call("remove_core_part", part_uid)
		if typeof(r) == TYPE_DICTIONARY:
			removed = r
		core_inventory = gs.core_bag
		inventory = core_inventory
	else:
		for i in range(core_inventory.size()):
			var p: Dictionary = core_inventory[i]
			if str(p.get("uid", "")) == part_uid:
				removed = p
				core_inventory.remove_at(i)
				break
		inventory = core_inventory
	return removed


## 戰鬥勝利結算掉落：抽取部件、入袋並傳回
static func roll_and_add_battle_drop(rng: RandomNumberGenerator = null) -> Dictionary:
	var part := roll_battle_drop(rng)
	add_part_to_inventory(part)
	return part


## 戰鬥勝利掛鉤（別名）
static func on_battle_won(rng: RandomNumberGenerator = null) -> Dictionary:
	return roll_and_add_battle_drop(rng)
