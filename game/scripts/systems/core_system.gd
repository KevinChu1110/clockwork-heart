extends Node
## 機芯部件與八色階校準系統 (CoreSystem)
## 遵循 CORE_LOOP_REVAMP_PROPOSAL 支柱二與 PRODUCT_LOCK 規範：
## 1. 分數對應八色階：灰(<0) 白(0) 橘(1~4) 藍(5~22) 紫(23~39) 金(40~54) 綠(55~69) 紅(70+)
## 2. 每個機芯部件最多校準 7 次，第 8 次校準被拒絕
## 3. 校準失敗不刪裝備、不碎裝（安全彈簧保底機制）
## 4. 五槽名稱固定：發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心
## 5. 硬限制：數值只准動 ATK/DEF/HP/CRIT/CRIT_DMG；不准動 ATB、攻速、前搖、命中等時間模型

const MAX_CALIBRATIONS: int = 7
const CALIBRATION_SCRAP_COST: int = 5

signal part_calibrated(slot_id: String, part: Dictionary, result: Dictionary)
signal part_dropped(part: Dictionary)
signal part_dismantled(part: Dictionary, scrap_gain: int)
signal part_unequipped(slot_id: String, part: Dictionary)

static var player_parts: Dictionary = {}
static var core_inventory: Array = []
static var inventory: Array = []
static var _shuffle_bag: Array[String] = []
static var _last_dropped_slot: String = ""
static var _has_new_core_drop_flag: bool = false

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

const DEFAULT_COLOSSUS_DROP_TIER_WEIGHTS: Dictionary = {
	"gray": 20,
	"white": 180,
	"orange": 200,
	"blue": 250,
	"purple": 180,
	"gold": 100,
	"green": 50,
	"red": 20,
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

## 停擺巨偶部位對應五槽對照表（0-QA27 對齊既有三隻巨偶 parts）
## 破壞部位決定掉落機芯部件槽位：
## 失控發條獅：溢能尖角 -> 發條發電機 (mainspring)、溢能核心 -> 共鳴核心 (soul_core)
## 霧鐘提線人偶：溢能尖角 -> 傳動齒輪組 (gear_train)、溢能核心 -> 擒縱調速器 (escapement)
## 黑鏽蒸氣巨象：溢能尖角 -> 機殼裝甲 (chassis)、溢能核心 -> 共鳴核心 (soul_core)
const COLOSSUS_PART_SLOT_MAP: Dictionary = {
	"colossus_lion": {
		"溢能尖角": SLOT_MAINSPRING,
		"spike": SLOT_MAINSPRING,
		"溢能核心": SLOT_SOUL_CORE,
		"core": SLOT_SOUL_CORE,
	},
	"colossus_puppet": {
		"溢能尖角": SLOT_GEAR_TRAIN,
		"spike": SLOT_GEAR_TRAIN,
		"溢能核心": SLOT_ESCAPEMENT,
		"core": SLOT_ESCAPEMENT,
	},
	"colossus_elephant": {
		"溢能尖角": SLOT_CHASSIS,
		"spike": SLOT_CHASSIS,
		"溢能核心": SLOT_SOUL_CORE,
		"core": SLOT_SOUL_CORE,
	},
}


## 查詢停擺巨偶部位對應之機芯五槽代號（若未指定或非巨偶部位則傳回空字串）
static func get_colossus_part_slot(boss_id: String = "", part_key: String = "") -> String:
	var bid := boss_id.strip_edges().to_lower()
	var pkey := part_key.strip_edges()

	# 1. 優先查特定巨偶部位表 (boss_id, part_name / part_id)
	if COLOSSUS_PART_SLOT_MAP.has(bid):
		var bmap: Dictionary = COLOSSUS_PART_SLOT_MAP[bid]
		if bmap.has(pkey):
			return normalize_slot_id(str(bmap[pkey]))
		if bmap.has(pkey.to_lower()):
			return normalize_slot_id(str(bmap[pkey.to_lower()]))

	# 2. 通用別名與語意對應
	match pkey.to_lower():
		"mainspring", "spring", "發條", "發條部位", "發條發電機", "背後主發條", "主發條":
			return SLOT_MAINSPRING
		"chassis", "機殼", "機殼部位", "機殼裝甲", "外殼", "裝甲", "平衡擺輪", "擺輪":
			return SLOT_CHASSIS
		"escapement", "governor", "調速器", "調速器部位", "擒縱調速器", "鐘擺", "擒縱叉":
			return SLOT_ESCAPEMENT
		"gear_train", "gears", "齒輪", "齒輪部位", "傳動齒輪組", "齒輪組", "傳動齒輪":
			return SLOT_GEAR_TRAIN
		"soul_core", "core", "核心", "核心部位", "共鳴核心", "溢能核心":
			return SLOT_SOUL_CORE
		"溢能尖角", "spike":
			return SLOT_MAINSPRING

	return ""

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

const TIER_ORDER: Array[String] = [
	TIER_GRAY,
	TIER_WHITE,
	TIER_ORANGE,
	TIER_BLUE,
	TIER_PURPLE,
	TIER_GOLD,
	TIER_GREEN,
	TIER_RED
]

## 機芯拆解回收鐵屑數量表（寫死對照表，精神對齊既有裝備拆解：灰1／白2／橘3／藍4／紫5／金6／綠8／紅10）
const CORE_DISMANTLE_SCRAP_MAP: Dictionary = {
	TIER_GRAY: 1,
	TIER_WHITE: 2,
	TIER_ORANGE: 3,
	TIER_BLUE: 4,
	TIER_PURPLE: 5,
	TIER_GOLD: 6,
	TIER_GREEN: 8,
	TIER_RED: 10,
}

const TIER_MIN_SCORES: Dictionary = {
	TIER_GRAY: -10,
	TIER_WHITE: 0,
	TIER_ORANGE: 1,
	TIER_BLUE: 5,
	TIER_PURPLE: 23,
	TIER_GOLD: 40,
	TIER_GREEN: 55,
	TIER_RED: 70
}

const TIER_MAX_SCORES: Dictionary = {
	TIER_GRAY: -1,
	TIER_WHITE: 0,
	TIER_ORANGE: 4,
	TIER_BLUE: 22,
	TIER_PURPLE: 39,
	TIER_GOLD: 54,
	TIER_GREEN: 69,
	TIER_RED: 999999
}

static var calibration_seed: Variant = null

static func set_calibration_seed(s: Variant) -> void:
	calibration_seed = s

static func get_tier_index(tier_id: String) -> int:
	var idx := TIER_ORDER.find(tier_id)
	return idx if idx >= 0 else 1

static func get_tier_id_by_index(index: int) -> String:
	var clamped := clampi(index, 0, TIER_ORDER.size() - 1)
	return TIER_ORDER[clamped]

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
		"spring_generator", "slot_01", "generator", "發條發電機", "0", "mainspring", "主發條", "發條":
			return SLOT_MAINSPRING
		"chassis_armor", "slot_02", "armor", "機殼裝甲", "1", "chassis", "平衡擺輪", "擺輪":
			return SLOT_CHASSIS
		"escapement_governor", "slot_03", "governor", "擒縱調速器", "2", "escapement", "擒縱叉":
			return SLOT_ESCAPEMENT
		"transmission_gears", "slot_04", "gears", "傳動齒輪組", "3", "gear_train", "傳動齒輪", "齒輪":
			return SLOT_GEAR_TRAIN
		"resonance_core", "slot_05", "core", "共鳴核心", "4", "soul_core", "核心":
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
		"tier_jump_count": 0,
		"has_jumped_tier": false,
		"initial_tier": tier_info.get("id", TIER_WHITE),
		"history": []
	}


## 檢查機芯部件是否還能進行校準
static func can_calibrate(part: Dictionary) -> bool:
	if part == null or part.is_empty():
		return false
	if bool(part.get("is_broken", false)):
		return false
	return int(part.get("calibration_count", 0)) < MAX_CALIBRATIONS


static func get_calibration_roll_weights() -> Dictionary:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("get_calibration_roll_weights"):
			return dt.call("get_calibration_roll_weights")
	if FileAccess.file_exists(TABLE_PATH):
		var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY and data.has("calibration_rules"):
				var cr = data["calibration_rules"]
				if typeof(cr) == TYPE_DICTIONARY and cr.has("roll_weights"):
					return cr["roll_weights"]
	return {"fail": 20, "maintain": 40, "jump_1": 30, "jump_2": 10}


static func get_calibration_pity_rule() -> Dictionary:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("get_calibration_pity_rule"):
			return dt.call("get_calibration_pity_rule")
	if FileAccess.file_exists(TABLE_PATH):
		var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY and data.has("calibration_rules"):
				var cr = data["calibration_rules"]
				if typeof(cr) == TYPE_DICTIONARY and cr.has("pity_rule"):
					return cr["pity_rule"]
	return {"pity_attempt": 7, "min_jump": 1}


## 判定單次機芯校準結果型別：fail / maintain / jump_1 / jump_2
## 含第七次未跳階保底與紅階封頂邏輯
static func roll_calibration_type(part: Dictionary, seed_val: Variant = null) -> Dictionary:
	var cur_score: int = int(part.get("score", 0))
	var tier_info := get_tier_by_score(cur_score)
	var cur_tier_id := str(tier_info.get("id", TIER_WHITE))
	var cur_tier_idx := get_tier_index(cur_tier_id)
	var cur_count: int = int(part.get("calibration_count", 0))
	var is_7th_attempt: bool = (cur_count + 1 == MAX_CALIBRATIONS)

	# 檢查是否曾經跳過階
	var has_jumped: bool = bool(part.get("has_jumped_tier", false)) or int(part.get("tier_jump_count", 0)) > 0
	if not has_jumped:
		var hist: Array = part.get("history", [])
		for h in hist:
			if typeof(h) == TYPE_DICTIONARY and int(h.get("tier_jump", 0)) > 0:
				has_jumped = true
				break

	# 讀取權重
	var weights := get_calibration_roll_weights()
	var w_fail: int = int(weights.get("fail", 20))
	var w_maintain: int = int(weights.get("maintain", 40))
	var w_jump1: int = int(weights.get("jump_1", 30))
	var w_jump2: int = int(weights.get("jump_2", 10))
	var total_w := w_fail + w_maintain + w_jump1 + w_jump2
	if total_w <= 0:
		total_w = 100
		w_fail = 20
		w_maintain = 40
		w_jump1 = 30
		w_jump2 = 10

	var rng := RandomNumberGenerator.new()
	if seed_val != null:
		rng.seed = int(seed_val)
	elif calibration_seed != null:
		rng.seed = int(calibration_seed)
	else:
		rng.randomize()

	var roll_val := rng.randi_range(0, total_w - 1)
	var roll_type := "fail"
	if roll_val < w_fail:
		roll_type = "fail"
	elif roll_val < w_fail + w_maintain:
		roll_type = "maintain"
	elif roll_val < w_fail + w_maintain + w_jump1:
		roll_type = "jump_1"
	else:
		roll_type = "jump_2"

	var pity_triggered: bool = false
	# 第七次保底：同一部件第七次若還沒跳過階，保底至少跳一階；已是最高紅階就維持紅、仍扣次數
	if is_7th_attempt and not has_jumped:
		if cur_tier_idx >= 7:
			# 已是最高紅階：維持紅、仍扣次數
			roll_type = "maintain"
			pity_triggered = false
		else:
			# 尚未跳過階且非紅階：保底至少跳一階
			pity_triggered = true
			if roll_type == "fail" or roll_type == "maintain":
				roll_type = "jump_1"

	# 紅階封頂檢驗：已是最高紅階就維持紅
	if cur_tier_idx >= 7:
		if roll_type == "jump_1" or roll_type == "jump_2":
			roll_type = "maintain"

	return {
		"roll_type": roll_type,
		"pity_triggered": pity_triggered,
		"cur_tier_idx": cur_tier_idx,
		"cur_tier_id": cur_tier_id,
		"cur_score": cur_score
	}


## 計算特定 roll_type 對應的 score_delta、stat_delta 與 tier_jump
## 硬限制：僅動 ATK/DEF/HP/CRIT/CRIT_DMG，零時間模型改動
static func calculate_roll_deltas(slot_id: String, roll_type: String, cur_tier_idx: int, cur_score: int) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var score_delta := 0
	var stat_delta: Dictionary = {}
	var tier_jump := 0
	var target_tier_idx := cur_tier_idx

	match roll_type:
		"fail":
			score_delta = 0
			stat_delta = {}
			tier_jump = 0
			target_tier_idx = cur_tier_idx
		"maintain":
			tier_jump = 0
			target_tier_idx = cur_tier_idx
			if cur_tier_idx >= 7: # 紅階維持紅階微調
				score_delta = 1
			elif cur_tier_idx == 1: # 白階 (0分)
				score_delta = 0
			else:
				var max_s: int = int(TIER_MAX_SCORES.get(get_tier_id_by_index(cur_tier_idx), cur_score))
				score_delta = 1 if cur_score < max_s else 0
			
			match norm:
				SLOT_MAINSPRING:
					stat_delta = {"ATK": 1, "HP": 5}
				SLOT_CHASSIS:
					stat_delta = {"DEF": 1, "HP": 8}
				SLOT_ESCAPEMENT:
					stat_delta = {"CRIT": 0.5, "CRIT_DMG": 1.0}
				SLOT_GEAR_TRAIN:
					stat_delta = {"ATK": 1, "DEF": 1}
				SLOT_SOUL_CORE:
					stat_delta = {"ATK": 1, "DEF": 1, "HP": 5}
				_:
					stat_delta = {"ATK": 1}

		"jump_1":
			if cur_tier_idx >= 7:
				target_tier_idx = 7
				tier_jump = 0
				score_delta = 1
			else:
				target_tier_idx = cur_tier_idx + 1
				tier_jump = 1
				var target_tier_id := get_tier_id_by_index(target_tier_idx)
				var min_s: int = int(TIER_MIN_SCORES.get(target_tier_id, cur_score + 1))
				score_delta = maxi(1, min_s - cur_score)

			match norm:
				SLOT_MAINSPRING:
					stat_delta = {"ATK": 3, "HP": 12}
				SLOT_CHASSIS:
					stat_delta = {"DEF": 3, "HP": 18}
				SLOT_ESCAPEMENT:
					stat_delta = {"CRIT": 1.0, "CRIT_DMG": 3.0}
				SLOT_GEAR_TRAIN:
					stat_delta = {"ATK": 2, "DEF": 2}
				SLOT_SOUL_CORE:
					stat_delta = {"ATK": 2, "DEF": 2, "HP": 18}
				_:
					stat_delta = {"ATK": 2}

		"jump_2":
			if cur_tier_idx >= 7:
				target_tier_idx = 7
				tier_jump = 0
				score_delta = 2
			elif cur_tier_idx == 6: # 綠階跳兩階封頂於紅階
				target_tier_idx = 7
				tier_jump = 1
				var min_s: int = int(TIER_MIN_SCORES.get(TIER_RED, 70))
				score_delta = maxi(2, min_s - cur_score)
			else:
				target_tier_idx = cur_tier_idx + 2
				tier_jump = 2
				var target_tier_id := get_tier_id_by_index(target_tier_idx)
				var min_s: int = int(TIER_MIN_SCORES.get(target_tier_id, cur_score + 2))
				score_delta = maxi(2, min_s - cur_score)

			match norm:
				SLOT_MAINSPRING:
					stat_delta = {"ATK": 6, "HP": 25}
				SLOT_CHASSIS:
					stat_delta = {"DEF": 6, "HP": 35}
				SLOT_ESCAPEMENT:
					stat_delta = {"CRIT": 2.0, "CRIT_DMG": 5.0}
				SLOT_GEAR_TRAIN:
					stat_delta = {"ATK": 4, "DEF": 4}
				SLOT_SOUL_CORE:
					stat_delta = {"ATK": 4, "DEF": 4, "HP": 35}
				_:
					stat_delta = {"ATK": 4}

	return {
		"score_delta": score_delta,
		"stat_delta": stat_delta,
		"tier_jump": tier_jump,
		"target_tier_idx": target_tier_idx
	}


## 取得結果對應之繁中提示與多語言 key
static func get_calibration_result_message(roll_type: String, pity_triggered: bool, is_red_cap: bool) -> Dictionary:
	if roll_type == "fail":
		return {
			"key": "CALIBRATE_FAIL",
			"text": "校準未達標，安全彈簧保護不碎裝"
		}
	elif pity_triggered:
		return {
			"key": "CALIBRATE_PITY_JUMP",
			"text": "第七次保底啟動！突破跳階成功"
		}
	elif is_red_cap:
		return {
			"key": "CALIBRATE_RED_MAX",
			"text": "已達極限紅階，微調維持頂階"
		}
	elif roll_type == "jump_2":
		return {
			"key": "CALIBRATE_JUMP_2",
			"text": "極限跳兩階！發條大幅進階"
		}
	elif roll_type == "jump_1":
		return {
			"key": "CALIBRATE_JUMP_1",
			"text": "跳一階成功！發條突破進階"
		}
	else: # maintain
		return {
			"key": "CALIBRATE_MAINTAIN",
			"text": "校準微調完成，維持同階"
		}


## 對機芯部件進行校準
## roll_success: 本次校準判定是否成功
## stat_delta: 成功或微調時變動的數值（只准含 ATK/DEF/HP/CRIT/CRIT_DMG）
## score_delta: 變動的分數
## 回傳結果包含 ok, rejected, code, roll_type, tier_jump, pity_triggered, part 等
static func calibrate(part: Dictionary, roll_success: bool = true, stat_delta: Dictionary = {}, score_delta: int = 0, roll_type: String = "", tier_jump: int = 0, pity_triggered: bool = false, message_override: String = "", message_key: String = "") -> Dictionary:
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

	var prev_score: int = int(part.get("score", 0))
	var prev_tier: String = str(part.get("tier", TIER_WHITE))
	var prev_tier_idx: int = get_tier_index(prev_tier)

	if roll_type.is_empty():
		if not roll_success:
			roll_type = "fail"
		elif tier_jump > 0:
			roll_type = "jump_%d" % mini(tier_jump, 2)
		else:
			roll_type = "maintain"

	var msg_text := message_override
	var msg_k := message_key
	if msg_text.is_empty():
		var is_red_cap := (prev_tier_idx >= 7 and roll_success)
		var msg_info := get_calibration_result_message(roll_type, pity_triggered, is_red_cap)
		msg_text = str(msg_info.get("text", "發條校準完成"))
		msg_k = str(msg_info.get("key", "CALIBRATE_MAINTAIN"))

	if roll_success:
		# 成功：套用數值與分數調整
		var stats: Dictionary = part.get("stats", {})
		for sk in stat_delta.keys():
			var s_upper := str(sk).to_upper()
			var cur_val = stats.get(s_upper, 0)
			stats[s_upper] = cur_val + stat_delta[sk]
		part["stats"] = stats

		var new_score: int = prev_score + score_delta
		part["score"] = new_score
		var tier_info := get_tier_by_score(new_score)
		var new_tier: String = str(tier_info.get("id", TIER_WHITE))
		part["tier"] = new_tier
		part["tier_name"] = tier_info.get("name", "白")
		part["is_broken"] = false

		var new_tier_idx: int = get_tier_index(new_tier)
		var actual_jump: int = maxi(0, new_tier_idx - prev_tier_idx)
		if tier_jump == 0 and actual_jump > 0:
			tier_jump = actual_jump

		if tier_jump > 0:
			part["tier_jump_count"] = int(part.get("tier_jump_count", 0)) + tier_jump
			part["has_jumped_tier"] = true

		var entry := {
			"attempt": current_count,
			"success": true,
			"roll_type": roll_type,
			"tier_jump": tier_jump,
			"pity_triggered": pity_triggered,
			"score_delta": score_delta,
			"stat_delta": stat_delta.duplicate(),
			"new_score": new_score,
			"new_tier": new_tier
		}
		var hist: Array = part.get("history", [])
		hist.append(entry)
		part["history"] = hist

		return {
			"ok": true,
			"rejected": false,
			"code": "SUCCESS",
			"roll_type": roll_type,
			"tier_jump": tier_jump,
			"pity_triggered": pity_triggered,
			"message": msg_text,
			"message_key": msg_k,
			"part": part,
			"calibration_count": current_count,
			"prev_tier": prev_tier,
			"new_tier": new_tier,
			"prev_score": prev_score,
			"new_score": new_score,
			"score_delta": score_delta,
			"stat_delta": stat_delta,
			"is_broken": false,
			"destroyed": false
		}
	else:
		# 規則 3：校準失敗不刪裝備、不碎裝（安全彈簧保護）
		part["is_broken"] = false

		var entry := {
			"attempt": current_count,
			"success": false,
			"roll_type": "fail",
			"tier_jump": 0,
			"pity_triggered": false,
			"score_delta": 0,
			"stat_delta": {},
			"new_score": prev_score,
			"new_tier": prev_tier
		}
		var hist: Array = part.get("history", [])
		hist.append(entry)
		part["history"] = hist

		return {
			"ok": false,
			"rejected": false,
			"code": "CALIBRATION_FAILED",
			"roll_type": "fail",
			"tier_jump": 0,
			"pity_triggered": false,
			"message": msg_text,
			"message_key": msg_k,
			"part": part,
			"calibration_count": current_count,
			"prev_tier": prev_tier,
			"new_tier": prev_tier,
			"prev_score": prev_score,
			"new_score": prev_score,
			"score_delta": 0,
			"stat_delta": {},
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
			if gs.has_method("ensure_core_slots"):
				gs.ensure_core_slots("white")


## 取得單次校準所需消耗的鐵屑數量（優先從 DataTables / core_color_tiers.json 讀取）
static func get_calibration_scrap_cost() -> int:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("get_calibration_scrap_cost"):
			return int(dt.call("get_calibration_scrap_cost"))
	if FileAccess.file_exists(TABLE_PATH):
		var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY and data.has("calibration_rules"):
				var cr = data["calibration_rules"]
				if typeof(cr) == TYPE_DICTIONARY and cr.has("iron_scrap_cost"):
					return int(cr["iron_scrap_cost"])
	return CALIBRATION_SCRAP_COST


## 取得玩家當前持有的鐵屑數量
static func get_player_scrap() -> int:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_method("count"):
			return int(inv.call("count", "iron_scrap"))
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and "inventory" in gs and gs.inventory is Dictionary:
			return int(gs.inventory.get("iron_scrap", 0))
	return 0


## 檢查玩家是否有足夠鐵屑進行校準
static func has_enough_scrap_to_calibrate() -> bool:
	return get_player_scrap() >= get_calibration_scrap_cost()


## 扣除玩家鐵屑
static func consume_player_scrap(amount: int) -> bool:
	if amount <= 0:
		return true
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_method("remove_item"):
			return bool(inv.call("remove_item", "iron_scrap", amount))
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and "inventory" in gs and gs.inventory is Dictionary:
			var cur: int = int(gs.inventory.get("iron_scrap", 0))
			if cur < amount:
				return false
			gs.inventory["iron_scrap"] = cur - amount
			return true
	return false


## 對任意機芯部件執行單次完整校準（含隨機擲骰、跳階、第七次保底與安全彈簧不碎裝）
## 參數 roll_success: null 為標準隨機擲骰；也可顯式指定 true/false 或 "fail"/"maintain"/"jump_1"/"jump_2"
static func calibrate_part(part: Dictionary, roll_success: Variant = null, stat_delta: Dictionary = {}, score_delta: int = 0, seed_val: Variant = null) -> Dictionary:
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

	var slot_id := str(part.get("slot", SLOT_MAINSPRING))
	var norm := normalize_slot_id(slot_id)
	var cur_score: int = int(part.get("score", 0))
	var tier_info := get_tier_by_score(cur_score)
	var cur_tier_id := str(tier_info.get("id", TIER_WHITE))
	var cur_tier_idx := get_tier_index(cur_tier_id)

	var roll_type := ""
	var is_success := true
	var pity_triggered := false
	var tier_jump := 0
	var final_stats := stat_delta.duplicate()
	var final_score_delta := score_delta

	if typeof(roll_success) == TYPE_STRING:
		roll_type = str(roll_success).to_lower()
		is_success = (roll_type != "fail")
		var roll_data := calculate_roll_deltas(norm, roll_type, cur_tier_idx, cur_score)
		if final_stats.is_empty():
			final_stats = roll_data.stat_delta
		if final_score_delta == 0:
			final_score_delta = roll_data.score_delta
		tier_jump = roll_data.tier_jump
	elif typeof(roll_success) == TYPE_BOOL:
		is_success = bool(roll_success)
		if not is_success:
			roll_type = "fail"
			final_stats = {}
			final_score_delta = 0
			tier_jump = 0
		else:
			if not final_stats.is_empty() or final_score_delta != 0:
				# 向後相容既有自訂參數
				var test_score := cur_score + final_score_delta
				var test_tier_idx := get_tier_index(str(get_tier_by_score(test_score).get("id", TIER_WHITE)))
				tier_jump = maxi(0, test_tier_idx - cur_tier_idx)
				roll_type = ("jump_%d" % mini(tier_jump, 2)) if tier_jump > 0 else "maintain"
			else:
				var roll_res := roll_calibration_type(part, seed_val)
				roll_type = str(roll_res.roll_type)
				if roll_type == "fail":
					roll_type = "maintain"
				pity_triggered = bool(roll_res.pity_triggered)
				var roll_data := calculate_roll_deltas(norm, roll_type, cur_tier_idx, cur_score)
				final_stats = roll_data.stat_delta
				final_score_delta = roll_data.score_delta
				tier_jump = roll_data.tier_jump
	else:
		# 正常隨機擲骰：roll_success == null
		var roll_res := roll_calibration_type(part, seed_val)
		roll_type = str(roll_res.roll_type)
		pity_triggered = bool(roll_res.pity_triggered)
		is_success = (roll_type != "fail")
		var roll_data := calculate_roll_deltas(norm, roll_type, cur_tier_idx, cur_score)
		if final_stats.is_empty():
			final_stats = roll_data.stat_delta
		if final_score_delta == 0:
			final_score_delta = roll_data.score_delta
		tier_jump = roll_data.tier_jump

	return calibrate(part, is_success, final_stats, final_score_delta, roll_type, tier_jump, pity_triggered)


## 執行玩家機芯部件單次校準
## roll_success: null 為標準隨機擲骰（含跳階/保底）；也可顯式指定 true/false 或 "fail"/"maintain"/"jump_1"/"jump_2"
static func calibrate_player_part(slot_id: String, roll_success: Variant = null, stat_delta: Dictionary = {}, score_delta: int = 0, seed_val: Variant = null) -> Dictionary:
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

	var cost := get_calibration_scrap_cost()
	var cur_scrap := get_player_scrap()
	if cur_scrap < cost:
		return {
			"ok": false,
			"rejected": true,
			"code": "INSUFFICIENT_SCRAP",
			"message": "鐵屑不足！校準需要 %d 鐵屑。" % cost,
			"part": part,
			"scrap_cost": cost,
			"current_scrap": cur_scrap,
			"calibration_count": int(part.get("calibration_count", 0)),
			"is_broken": bool(part.get("is_broken", false)),
			"destroyed": false
		}

	consume_player_scrap(cost)

	var res := calibrate_part(part, roll_success, stat_delta, score_delta, seed_val)
	res["used_scrap"] = cost
	res["scrap_cost"] = cost
	res["remaining_scrap"] = get_player_scrap()

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


## 卸下部件至未裝備背包
static func unequip_part(slot_id: String) -> Dictionary:
	var norm := normalize_slot_id(slot_id)
	var tree := Engine.get_main_loop()
	var cs: Node = null
	if tree is SceneTree and (tree as SceneTree).root != null:
		var root = (tree as SceneTree).root
		cs = root.get_node_or_null("CoreSystem")
		var gs: Node = root.get_node_or_null("GameState")
		if gs and "core_slots" in gs and gs.core_slots.has(norm):
			var old: Dictionary = gs.core_slots[norm]
			gs.core_slots.erase(norm)
			if player_parts.has(norm):
				player_parts.erase(norm)
			if not old.is_empty():
				add_part_to_inventory(old)
			if cs and cs.has_signal("part_unequipped"):
				cs.emit_signal("part_unequipped", norm, old)
			return old
	if player_parts.has(norm):
		var old: Dictionary = player_parts[norm]
		player_parts.erase(norm)
		if not old.is_empty():
			add_part_to_inventory(old)
		if cs and cs.has_signal("part_unequipped"):
			cs.emit_signal("part_unequipped", norm, old)
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


## 取得八色階掉落機率權重表（支援來源：關卡／巨偶，預設 stage）
static func get_drop_weights(source: String = "stage") -> Dictionary:
	var is_colossus := (source == "colossus" or source.begins_with("colossus_"))
	var default_weights: Dictionary = DEFAULT_COLOSSUS_DROP_TIER_WEIGHTS if is_colossus else DEFAULT_DROP_TIER_WEIGHTS
	var weights := default_weights.duplicate()
	if FileAccess.file_exists(TABLE_PATH):
		var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
		if f:
			var data = JSON.parse_string(f.get_as_text())
			if typeof(data) == TYPE_DICTIONARY and data.has("tiers") and typeof(data["tiers"]) == TYPE_ARRAY:
				for tdef in data["tiers"]:
					if typeof(tdef) == TYPE_DICTIONARY and tdef.has("id"):
						var tid := str(tdef["id"])
						if is_colossus and tdef.has("colossus_drop_weight"):
							weights[tid] = int(tdef["colossus_drop_weight"])
						elif not is_colossus and tdef.has("drop_weight"):
							weights[tid] = int(tdef["drop_weight"])
	return weights


static func _parse_roll_args(arg1: Variant, arg2: String) -> Array:
	var rng: RandomNumberGenerator = null
	var source: String = "stage"
	if arg1 is RandomNumberGenerator:
		rng = arg1
		source = arg2
	elif typeof(arg1) == TYPE_STRING:
		source = str(arg1)
	else:
		source = arg2
	return [rng, source]


## 依權重隨機抽取八色階之一（支援傳入來源：關卡／巨偶）
static func roll_tier(arg1: Variant = null, arg2: String = "stage") -> String:
	var parsed: Array = _parse_roll_args(arg1, arg2)
	var rng: RandomNumberGenerator = parsed[0]
	var source: String = parsed[1]
	var weights := get_drop_weights(source)
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


## 重設 5-bag 洗牌袋（單元測試或重新洗牌使用）
static func reset_shuffle_bag() -> void:
	_shuffle_bag.clear()
	_last_dropped_slot = ""


## 取得玩家目前尚未裝備的槽位清單（支援 GameState.core_slots）
static func get_unfilled_slots() -> Array[String]:
	var unfilled: Array[String] = []
	var equipped: Dictionary = {}
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs and gs.core_slots is Dictionary:
			equipped = gs.core_slots
	for sid in ALL_SLOT_IDS:
		var p = equipped.get(sid, null)
		if p == null or (typeof(p) == TYPE_DICTIONARY and p.is_empty()):
			unfilled.append(sid)
	return unfilled


## 5-bag 洗牌袋（Shuffle Bag）演算法抽取槽位：
## 1. 優先補足全身未湊齊的機芯槽位（未湊齊者先出袋，湊齊者後排）
## 2. 杜絕連續掉同槽垃圾（跨袋時新袋首抽避開前一袋最後一抽）
## 3. 保證每 5 抽必定五槽各 1 顆，極度平滑保底
static func roll_slot_shuffle_bag(rng: RandomNumberGenerator = null, priority_unfilled: bool = true) -> String:
	if _shuffle_bag.is_empty():
		var missing: Array[String] = []
		var owned: Array[String] = []
		var unfilled: Array[String] = []
		if priority_unfilled:
			unfilled = get_unfilled_slots()
		for sid in ALL_SLOT_IDS:
			if unfilled.has(sid):
				missing.append(sid)
			else:
				owned.append(sid)

		# 洗牌 missing
		var n_m := missing.size()
		for i in range(n_m - 1, 0, -1):
			var j := rng.randi_range(0, i) if rng != null else (randi() % (i + 1))
			var tmp := missing[i]
			missing[i] = missing[j]
			missing[j] = tmp

		# 洗牌 owned
		var n_o := owned.size()
		for i in range(n_o - 1, 0, -1):
			var j := rng.randi_range(0, i) if rng != null else (randi() % (i + 1))
			var tmp2 := owned[i]
			owned[i] = owned[j]
			owned[j] = tmp2

		_shuffle_bag.clear()
		for sid in missing:
			_shuffle_bag.append(sid)
		for sid in owned:
			_shuffle_bag.append(sid)

		# 杜絕連續掉同槽：若新袋首抽與上一袋最後一抽相同，且袋內有其他選項，則與同優先度組或下一項交換
		if _last_dropped_slot != "" and _shuffle_bag.size() > 1 and _shuffle_bag[0] == _last_dropped_slot:
			var swap_idx := 1
			if missing.size() > 1:
				swap_idx = 1
			elif _shuffle_bag.size() > 1:
				swap_idx = 1
			var t := _shuffle_bag[0]
			_shuffle_bag[0] = _shuffle_bag[swap_idx]
			_shuffle_bag[swap_idx] = t

	var picked: String = _shuffle_bag.pop_front()
	_last_dropped_slot = picked
	return picked


## 依 5-bag 洗牌袋隨機抽取五槽之一
static func roll_slot(rng: RandomNumberGenerator = null) -> String:
	return roll_slot_shuffle_bag(rng, true)


## 隨機生成一顆五槽機芯戰利品部件（遵循 create_part 規格與八色階權重，支援傳入來源關卡／巨偶，支援指定槽位鎖定與洗牌袋）
static func roll_battle_drop(arg1: Variant = null, arg2: String = "stage", slot_override: String = "") -> Dictionary:
	var parsed: Array = _parse_roll_args(arg1, arg2)
	var rng: RandomNumberGenerator = parsed[0]
	var source: String = parsed[1]
	var norm_slot_override := normalize_slot_id(slot_override) if slot_override != "" else ""
	var slot_id: String = ""
	if norm_slot_override in ALL_SLOT_IDS:
		slot_id = norm_slot_override
		var found_idx := _shuffle_bag.find(slot_id)
		if found_idx >= 0:
			_shuffle_bag.remove_at(found_idx)
		_last_dropped_slot = slot_id
	else:
		slot_id = roll_slot(rng)
	var tier_id := roll_tier(rng, source)
	var part := create_part_by_tier(slot_id, tier_id)
	if source == "colossus" or source.begins_with("colossus_"):
		part["is_colossus"] = true
		part["drop_source"] = source
	else:
		part["drop_source"] = "stage"
	if norm_slot_override in ALL_SLOT_IDS:
		part["slot_locked_by_part"] = true
	return part


## 將機芯部件加入背包／庫存（同步 GameState.core_bag 與 CoreSystem.inventory）
static func add_part_to_inventory(part: Dictionary) -> void:
	if part == null or part.is_empty():
		return
	var part_copy: Dictionary = part.duplicate(true)
	var slot_id: String = normalize_slot_id(str(part_copy.get("slot", SLOT_MAINSPRING)))
	part_copy["slot"] = slot_id
	if not part_copy.has("slot_name") or str(part_copy.get("slot_name", "")).is_empty():
		part_copy["slot_name"] = get_slot_name(slot_id)
	if not part_copy.has("uid") or str(part_copy.get("uid", "")).is_empty():
		_uid_counter += 1
		part_copy["uid"] = "core_%s_%d_%d" % [slot_id, int(Time.get_unix_time_from_system() * 1000), _uid_counter]

	var tree := Engine.get_main_loop()
	var gs: Node = null
	var cs: Node = null
	if tree is SceneTree and (tree as SceneTree).root != null:
		var root = (tree as SceneTree).root
		gs = root.get_node_or_null("GameState")
		cs = root.get_node_or_null("CoreSystem")

	mark_new_core_drop(true)

	if gs and gs.has_method("add_core_part"):
		gs.call("add_core_part", part_copy)
		core_inventory = gs.core_bag
		inventory = core_inventory
	else:
		var p_uid: String = str(part_copy.get("uid", ""))
		var exists := false
		if not p_uid.is_empty():
			for p in core_inventory:
				if p is Dictionary and str(p.get("uid", "")) == p_uid:
					exists = true
					break
		if not exists:
			core_inventory.append(part_copy)
		inventory = core_inventory

	if cs and cs.has_signal("part_dropped"):
		cs.emit_signal("part_dropped", part_copy)


static func has_new_core_drop() -> bool:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_method("has_new_core_part"):
			return bool(gs.call("has_new_core_part"))
	return _has_new_core_drop_flag


static func clear_new_core_drop() -> void:
	_has_new_core_drop_flag = false
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_method("clear_new_core_drop"):
			gs.call("clear_new_core_drop")


static func mark_new_core_drop(val: bool = true) -> void:
	_has_new_core_drop_flag = val
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_method("mark_new_core_drop"):
			gs.call("mark_new_core_drop", val)


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
	clear_new_core_drop()
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


## 戰鬥勝利結算掉落：抽取部件、入袋並傳回（支援傳入來源：關卡／巨偶，支援指定槽位鎖定）
static func roll_and_add_battle_drop(arg1: Variant = null, arg2: String = "stage", slot_override: String = "") -> Dictionary:
	var part := roll_battle_drop(arg1, arg2, slot_override)
	add_part_to_inventory(part)
	return part


## 戰鬥勝利掛鉤（別名，支援傳入來源：關卡／巨偶，支援指定槽位鎖定）
static func on_battle_won(arg1: Variant = null, arg2: String = "stage", slot_override: String = "") -> Dictionary:
	return roll_and_add_battle_drop(arg1, arg2, slot_override)


## 取得機芯拆解所能獲得的鐵屑數量（寫死對照表：灰1／白2／橘3／藍4／紫5／金6／綠8／紅10）
static func get_dismantle_scrap_yield(part: Dictionary) -> int:
	if part.is_empty():
		return 0
	var tier_id: String = str(part.get("tier", TIER_WHITE)).to_lower().strip_edges()
	match tier_id:
		"灰", "gray": return 1
		"白", "white": return 2
		"橘", "orange": return 3
		"藍", "青", "blue": return 4
		"紫", "purple": return 5
		"金", "gold": return 6
		"綠", "green": return 8
		"紅", "red": return 10
	if CORE_DISMANTLE_SCRAP_MAP.has(tier_id):
		return int(CORE_DISMANTLE_SCRAP_MAP[tier_id])
	return 2


## 增加玩家鐵屑（使用既有道具 iron_scrap）
static func add_player_scrap(amount: int) -> bool:
	if amount <= 0:
		return true
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
		if inv and inv.has_method("add_item"):
			var ok = bool(inv.call("add_item", "iron_scrap", amount))
			if ok:
				return true
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and "inventory" in gs and gs.inventory is Dictionary:
			var cur: int = int(gs.inventory.get("iron_scrap", 0))
			gs.inventory["iron_scrap"] = cur + amount
			return true
	return false


## 檢查指定部件是否為已裝備狀態（已裝備槽上的機芯不可拆）
static func is_part_equipped(part_or_uid: Variant) -> bool:
	var target_uid := ""
	if typeof(part_or_uid) == TYPE_STRING:
		target_uid = str(part_or_uid).strip_edges()
	elif typeof(part_or_uid) == TYPE_DICTIONARY:
		target_uid = str(part_or_uid.get("uid", "")).strip_edges()

	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and "core_slots" in gs and gs.core_slots is Dictionary:
			for sid in gs.core_slots.keys():
				var sp = gs.core_slots[sid]
				if typeof(sp) == TYPE_DICTIONARY and not sp.is_empty():
					if not target_uid.is_empty() and str(sp.get("uid", "")) == target_uid:
						return true
					if typeof(part_or_uid) == TYPE_DICTIONARY and sp == part_or_uid:
						return true
	return false


## 拆解未裝備機芯部件為既有鐵屑 (iron_scrap)
## 遵循規範：已裝備不可拆、各色階對照表、扣除背包部件、鐵屑入袋
static func dismantle_part(part_or_uid: Variant) -> Dictionary:
	var uid := ""
	var target_part: Dictionary = {}
	if typeof(part_or_uid) == TYPE_STRING:
		uid = str(part_or_uid).strip_edges()
	elif typeof(part_or_uid) == TYPE_DICTIONARY:
		target_part = part_or_uid
		uid = str(part_or_uid.get("uid", "")).strip_edges()

	if uid.is_empty() and target_part.is_empty():
		return {"ok": false, "reason": "invalid_argument", "message": "無效的機芯參數"}

	# 1. 檢查是否已裝備槽位：已裝備不可拆解！
	if is_part_equipped(part_or_uid):
		return {"ok": false, "reason": "is_equipped", "message": "已裝備槽上的機芯不可拆"}

	# 2. 檢查背包中是否存在此機芯
	var inv_list := get_inventory()
	var found_idx := -1
	for i in range(inv_list.size()):
		var p = inv_list[i]
		if typeof(p) == TYPE_DICTIONARY:
			if not uid.is_empty() and str(p.get("uid", "")) == uid:
				target_part = p
				found_idx = i
				break
			elif target_part.is_empty() == false and p == target_part:
				target_part = p
				found_idx = i
				break

	if found_idx < 0:
		return {"ok": false, "reason": "not_in_inventory", "message": "背包中找不到該未裝備機芯"}

	# 3. 計算獲得鐵屑數量
	var scrap_gain := get_dismantle_scrap_yield(target_part)

	# 4. 從背包中移除機芯
	var part_uid_to_remove: String = uid if not uid.is_empty() else str(target_part.get("uid", ""))
	var removed_part := remove_part_from_inventory(part_uid_to_remove)
	if removed_part.is_empty():
		if found_idx >= 0 and found_idx < core_inventory.size():
			removed_part = core_inventory[found_idx]
			core_inventory.remove_at(found_idx)
			inventory = core_inventory

	# 5. 增加鐵屑到玩家背包 (iron_scrap)
	add_player_scrap(scrap_gain)

	# 6. 發出通知訊號
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var cs: Node = (tree as SceneTree).root.get_node_or_null("CoreSystem")
		if cs and cs.has_signal("part_dismantled"):
			cs.emit_signal("part_dismantled", target_part, scrap_gain)

	return {
		"ok": true,
		"iron_scrap": scrap_gain,
		"scrap": scrap_gain,
		"part": target_part,
		"tier": target_part.get("tier", TIER_WHITE),
		"message": "成功拆解機芯，獲得 %d 鐵屑" % scrap_gain
	}
