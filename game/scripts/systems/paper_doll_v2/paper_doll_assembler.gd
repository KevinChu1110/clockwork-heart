extends RefCounted
## 紙娃娃組裝器：依 W6-K3 強制副手 empty、MVP one_hand、背鑰永在背。
## 模組邊界：產出 loadout／可見槽／AnimId；不直接碰 Texture。

const PaperDollConfigScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_config.gd")

## 相位 → 暫用整圖 composite（層切 PNG 未齊前）
const PHASE_COMPOSITE := {
	"explore": "res://assets/sprites/pack_a/v2/xiaobai_e03.png",
	"battle": "res://assets/sprites/pack_a/v2/xiaobai_b02.png",
	"dismantle": "res://assets/sprites/pack_a/v2/xiaobai_d02.png",
}

var config
## SlotId → asset_id（空字串＝不顯示／empty）
var loadout: Dictionary = {}
var current_weapon_class: String = "one_hand"
var current_anim: String = "idle"
var current_phase: String = "explore"
var last_error: String = ""


func setup(cfg = null) -> bool:
	config = cfg if cfg != null else PaperDollConfigScript.new()
	if config.raw.is_empty():
		if not config.load_from():
			last_error = "config_load_failed"
			return false
	_apply_defaults()
	# MVP 硬規則
	current_weapon_class = config.mvp_weapon_class()
	_enforce_weapon_rules()
	_ensure_identity_slots()
	return true


func _apply_defaults() -> void:
	loadout.clear()
	for sid in config.slot_ids():
		loadout[sid] = ""
	for k in config.defaults.keys():
		loadout[str(k)] = str(config.defaults[k])
	# defaults 可能用 weapon_off=empty 等
	if not loadout.has("weapon_off") or str(loadout["weapon_off"]) == "":
		loadout["weapon_off"] = "empty"


func _ensure_identity_slots() -> void:
	## 身份層不可空：body_base / face / chest_heart / back_key
	if str(loadout.get("body_base", "")) == "":
		loadout["body_base"] = "body_cream_default"
	if str(loadout.get("face", "")) == "":
		loadout["face"] = "face_default"
	if str(loadout.get("chest_heart", "")) == "":
		loadout["chest_heart"] = "chest_heart_teal"
	if str(loadout.get("back_key", "")) == "":
		loadout["back_key"] = "back_key_brass"
	# 背鑰規則：永遠在背，不可挪到手
	if config.back_key_always_on_back():
		# 禁止把背鑰寫進主／副手
		if str(loadout.get("weapon_main", "")) == str(loadout.get("back_key", "")):
			loadout["weapon_main"] = str(config.defaults.get("weapon_main", "sword_1h_brass"))
		if str(loadout.get("weapon_off", "")) == str(loadout.get("back_key", "")):
			loadout["weapon_off"] = "empty"


func _enforce_weapon_rules() -> void:
	last_error = ""
	var mvp: String = config.mvp_weapon_class()
	if config.is_weapon_class_blocked(current_weapon_class):
		last_error = "blocked_weapon_class:%s" % current_weapon_class
		current_weapon_class = mvp
	if not config.is_weapon_class_allowed(current_weapon_class):
		last_error = "disallowed_weapon_class:%s" % current_weapon_class
		current_weapon_class = mvp
	# MVP：副手只能 empty
	var off_def: Dictionary = config.slot_def("weapon_off")
	if str(off_def.get("mvp", "")) == "empty_only":
		loadout["weapon_off"] = "empty"
	# one_hand：主手必須有預設劍（戰鬥相才畫）
	if current_weapon_class == "one_hand":
		if str(loadout.get("weapon_main", "")) == "" or str(loadout.get("weapon_main", "")) == "empty":
			loadout["weapon_main"] = str(config.defaults.get("weapon_main", "sword_1h_brass"))


func set_weapon_class(wc: String) -> bool:
	## 嘗試切換 WeaponClass；被擋則回 false 並維持 MVP。
	if config.is_weapon_class_blocked(wc) or not config.is_weapon_class_allowed(wc):
		last_error = "reject_weapon_class:%s" % wc
		current_weapon_class = config.mvp_weapon_class()
		_enforce_weapon_rules()
		return false
	current_weapon_class = wc
	_enforce_weapon_rules()
	return true


func equip(slot_id: String, asset_id: String) -> bool:
	## 裝備單一槽；身份／MVP 規則可覆寫。
	if config.slot_def(slot_id).is_empty():
		last_error = "unknown_slot:%s" % slot_id
		return false
	if slot_id == "weapon_off":
		var off_def: Dictionary = config.slot_def("weapon_off")
		if str(off_def.get("mvp", "")) == "empty_only" and asset_id != "empty":
			last_error = "weapon_off_mvp_empty_only"
			loadout["weapon_off"] = "empty"
			return false
	if slot_id == "back_key" and asset_id == "empty":
		last_error = "back_key_required"
		return false
	if slot_id in ["weapon_main", "weapon_off"] and asset_id == str(loadout.get("back_key", "back_key_brass")):
		last_error = "back_key_never_in_hand"
		return false
	loadout[slot_id] = asset_id
	_enforce_weapon_rules()
	_ensure_identity_slots()
	return true


func set_phase(phase: String) -> void:
	## explore | battle | dismantle
	current_phase = phase
	match phase:
		"explore":
			current_anim = "explore_walk"
		"battle":
			current_anim = "ready"
		"dismantle":
			current_anim = "dismantle_pull"
		_:
			current_anim = "idle"


func play_anim(anim_id: String) -> bool:
	var d: Dictionary = config.anim_def(anim_id)
	if d.is_empty():
		last_error = "unknown_anim:%s" % anim_id
		return false
	var need_wc := str(d.get("weaponClass", ""))
	if need_wc != "" and need_wc != current_weapon_class:
		last_error = "anim_weapon_mismatch:%s" % anim_id
		return false
	current_anim = anim_id
	return true


func visible_slots_for_phase() -> PackedStringArray:
	## 依相位決定顯示哪些槽（武器僅戰鬥相）。
	var out: PackedStringArray = [
		"back_key", "body_base", "outfit", "face", "helmet", "chest_heart"
	]
	if current_phase == "battle":
		out.append("weapon_main")
		# MVP empty：副手不畫
		if str(loadout.get("weapon_off", "empty")) != "empty":
			out.append("weapon_off")
	if current_anim in ["hit", "dismantle_pull"] or str(loadout.get("vfx", "")) != "":
		out.append("vfx")
	return out


func composite_path_for_phase() -> String:
	## 層切未齊時用 Alice v2 三相整圖；退役舊 s8_smoke 電影皮。
	return str(PHASE_COMPOSITE.get(current_phase, PHASE_COMPOSITE["explore"]))


func chest_heart_hud_bound() -> bool:
	return config.chest_binds_wind_stamina_glow()


func summary() -> Dictionary:
	return {
		"characterId": config.character_id,
		"phase": current_phase,
		"anim": current_anim,
		"weaponClass": current_weapon_class,
		"weapon_off": str(loadout.get("weapon_off", "")),
		"weapon_main": str(loadout.get("weapon_main", "")),
		"back_key": str(loadout.get("back_key", "")),
		"chest_heart": str(loadout.get("chest_heart", "")),
		"bindsWindStaminaGlow": chest_heart_hud_bound(),
		"backKeyAlwaysOnBack": config.back_key_always_on_back(),
		"composite": composite_path_for_phase(),
		"visibleSlots": Array(visible_slots_for_phase()),
		"lastError": last_error,
	}
