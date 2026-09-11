class_name WindStamina
extends RefCounted
## Ken W2-K1 · 場景內發條體力（WindStamina）
## 與 EnergySystem（長線能量池 MAX 15 自然回）分開：本類是 §8 節點節奏預算，
## 進出探索／戰鬥／拆解節點時扣點，胸口光環 HUD 顯示，禁止藍 mana 條。

signal changed(current: int, maximum: int)
signal depleted(action_id: String)
signal spent(action_id: String, amount: int, remaining: int)

const DATA_PATH := "res://data/ken/w2_k1_wind_stamina.json"

var max_stamina: int = 15
var current: int = 15
var costs: Dictionary = {}
var part_break: Dictionary = {}
var hud: Dictionary = {}
var combat_mode: String = "realtime_rhythm_budget"
var drop_names: Dictionary = {}
var data_id: String = "W2-K1"
var _loaded: bool = false


## 從 Ken JSON 載入常數；失敗時用內建預設（等同 W2-K1）。
func load_defaults() -> void:
	var raw: Variant = _read_json(DATA_PATH)
	if typeof(raw) == TYPE_DICTIONARY:
		_apply_dict(raw as Dictionary)
	else:
		_apply_dict(_builtin_defaults())
	current = max_stamina
	_loaded = true
	changed.emit(current, max_stamina)


func _builtin_defaults() -> Dictionary:
	return {
		"id": "W2-K1",
		"WindStaminaMax": 15,
		"costs": {
			"E02_exploreTick": 1,
			"B01_combatEnter": 2,
			"D01_dismantleEnter": 2,
			"B_strike": 1,
			"B_takeHit": 0,
			"D_pullPart": 1,
		},
		"partBreak": {
			"PartUnlockHP": 0.70,
			"PartHPRatio": 0.25,
			"BreakBonus": 1.25,
			"drops": ["drop_brass_gear", "drop_spring_coil", "drop_core_shard"],
		},
		"hud": {
			"style": "chest_glow_ring_ticks",
			"forbid": ["blue_mana_bar", "second_resource_bar"],
			"HudTickCount": 15,
			"glowColor": "#2EC4B6",
			"tickColorLit": "#D4A017",
			"tickColorDim": "#6B5A3E",
			"anchor": "player_chest",
			"ringRadiusPx": 28,
			"glowMin": 0.25,
			"glowMax": 1.0,
		},
		"combatMode": "realtime_rhythm_budget",
		"dropNames": {
			"drop_brass_gear": "黃銅齒輪",
			"drop_spring_coil": "發條彈簧",
			"drop_core_shard": "核心碎片",
		},
	}


func _apply_dict(d: Dictionary) -> void:
	data_id = str(d.get("id", "W2-K1"))
	max_stamina = int(d.get("WindStaminaMax", 15))
	costs = (d.get("costs", {}) as Dictionary).duplicate(true)
	part_break = (d.get("partBreak", {}) as Dictionary).duplicate(true)
	hud = (d.get("hud", {}) as Dictionary).duplicate(true)
	combat_mode = str(d.get("combatMode", "realtime_rhythm_budget"))
	drop_names = (d.get("dropNames", {}) as Dictionary).duplicate(true)


func _read_json(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		push_warning("WindStamina: missing %s — using builtins" % path)
		return null
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return null
	var txt := f.get_as_text()
	var parsed: Variant = JSON.parse_string(txt)
	return parsed


func reset_scene() -> void:
	if not _loaded:
		load_defaults()
	current = max_stamina
	changed.emit(current, max_stamina)


func cost_of(action_id: String) -> int:
	return int(costs.get(action_id, 0))


func can_afford(action_id: String) -> bool:
	return current >= cost_of(action_id)


## 嘗試扣點。成功回 true；不足則 emit depleted 並回 false。
func try_spend(action_id: String) -> bool:
	if not _loaded:
		load_defaults()
	var amt := cost_of(action_id)
	if amt <= 0:
		spent.emit(action_id, 0, current)
		return true
	if current < amt:
		depleted.emit(action_id)
		return false
	current -= amt
	spent.emit(action_id, amt, current)
	changed.emit(current, max_stamina)
	return true


func ratio() -> float:
	if max_stamina <= 0:
		return 0.0
	return clampf(float(current) / float(max_stamina), 0.0, 1.0)


func glow_alpha() -> float:
	var gmin := float(hud.get("glowMin", 0.25))
	var gmax := float(hud.get("glowMax", 1.0))
	return lerpf(gmin, gmax, ratio())


func part_unlock_hp() -> float:
	return float(part_break.get("PartUnlockHP", 0.70))


func part_hp_ratio() -> float:
	return float(part_break.get("PartHPRatio", 0.25))


func break_bonus() -> float:
	return float(part_break.get("BreakBonus", 1.25))


func primary_drop() -> String:
	var drops: Array = part_break.get("drops", ["drop_brass_gear"]) as Array
	if drops.is_empty():
		return "drop_brass_gear"
	return str(drops[0])


func drop_display_name(drop_id: String) -> String:
	return str(drop_names.get(drop_id, drop_id))


## HUD 契約：禁止藍 mana／第二資源條（供測試與 UI 自檢）。
func hud_forbids_blue_mana() -> bool:
	var forbid: Array = hud.get("forbid", []) as Array
	return forbid.has("blue_mana_bar") and forbid.has("second_resource_bar")


func hud_style() -> String:
	return str(hud.get("style", "chest_glow_ring_ticks"))
