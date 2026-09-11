extends RefCounted
## W6-K3 紙娃娃設定載入器：Slots／Anim／WeaponClass 以 JSON 為準。
## 模組邊界：只負責讀取與查詢，不負責繪製或動畫播放。

const DEFAULT_PATH := "res://data/ken/w6_k3_paper_doll.json"

var raw: Dictionary = {}
var character_id: String = "xiaobai"
var equip_slots: Array = []
var weapon_class: Dictionary = {}
var anim: Dictionary = {}
var defaults: Dictionary = {}


func load_from(path: String = DEFAULT_PATH) -> bool:
	## 從 Ken 鎖定的 W6-K3 JSON 載入；失敗回 false。
	if not FileAccess.file_exists(path):
		push_error("PaperDollConfig: missing %s" % path)
		return false
	var txt := FileAccess.get_file_as_string(path)
	var parsed = JSON.parse_string(txt)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("PaperDollConfig: invalid JSON %s" % path)
		return false
	raw = parsed as Dictionary
	var pd: Dictionary = raw.get("paperDoll", {}) as Dictionary
	character_id = str(pd.get("characterId", "xiaobai"))
	equip_slots = pd.get("EquipSlots", []) as Array
	weapon_class = pd.get("WeaponClass", {}) as Dictionary
	anim = pd.get("Anim", {}) as Dictionary
	defaults = pd.get("defaults", {}) as Dictionary
	return true


func slot_ids() -> PackedStringArray:
	var out: PackedStringArray = []
	for s in equip_slots:
		if typeof(s) == TYPE_DICTIONARY:
			out.append(str((s as Dictionary).get("SlotId", "")))
	return out


func slot_def(slot_id: String) -> Dictionary:
	for s in equip_slots:
		if typeof(s) == TYPE_DICTIONARY:
			var d: Dictionary = s
			if str(d.get("SlotId", "")) == slot_id:
				return d
	return {}


func mvp_weapon_class() -> String:
	return str(weapon_class.get("MVP", "one_hand"))


func is_weapon_class_allowed(wc: String) -> bool:
	var allowed: Array = weapon_class.get("allowed", []) as Array
	if allowed.is_empty():
		return wc == mvp_weapon_class()
	return allowed.has(wc)


func is_weapon_class_blocked(wc: String) -> bool:
	var blocked: Array = weapon_class.get("blocked", []) as Array
	return blocked.has(wc)


func anim_def(anim_id: String) -> Dictionary:
	if anim.has(anim_id):
		return anim[anim_id] as Dictionary
	return {}


func chest_binds_wind_stamina_glow() -> bool:
	var d: Dictionary = slot_def("chest_heart")
	return str(d.get("bindsHud", "")) == "WindStaminaGlow"


func back_key_always_on_back() -> bool:
	var d: Dictionary = slot_def("back_key")
	return str(d.get("rule", "")) == "always_on_back" or str(d.get("anchor", "")) == "back"
