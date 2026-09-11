extends RefCounted
## 四角色 loadout（xiaobai／lion／fox／pig）；禁 tin_soldier／gear_bear。
## 模組邊界：角色⇄base／outfit 對照；動畫幀仍可先共用兔 oh_*。

const SoulDrawConfigScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_config.gd")
const FramesScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_frames.gd")

var soul_cfg
## CharacterId → {outfitId, unlockedOutfits:[]}
var loadouts: Dictionary = {}
var active_character_id: String = "xiaobai"
var last_error: String = ""


func setup(cfg = null) -> bool:
	soul_cfg = cfg if cfg != null else SoulDrawConfigScript.new()
	if soul_cfg.raw.is_empty():
		if not soul_cfg.load_from():
			last_error = "soul_config_failed"
			return false
	loadouts.clear()
	for cid in soul_cfg.character_ids():
		var d: Dictionary = soul_cfg.character_def(cid)
		var def_outfit: String = str(d.get("defaultOutfit", ""))
		loadouts[cid] = {
			"outfitId": def_outfit,
			"unlockedOutfits": [def_outfit],
			"baseAsset": str(d.get("baseAsset", "")),
		}
	active_character_id = "xiaobai"
	if not soul_cfg.is_character_allowed(active_character_id):
		var ids: PackedStringArray = soul_cfg.character_ids()
		active_character_id = ids[0] if ids.size() > 0 else ""
	return true


func select_character(character_id: String) -> bool:
	character_id = soul_cfg.resolve_character_id(character_id)
	if not soul_cfg.is_character_allowed(character_id):
		last_error = "blocked_or_unknown:%s" % character_id
		return false
	active_character_id = character_id
	return true


func unlock_outfit(outfit_id: String) -> bool:
	outfit_id = soul_cfg.resolve_outfit_id(outfit_id)
	var odef: Dictionary = soul_cfg.outfit_def(outfit_id)
	if odef.is_empty():
		last_error = "unknown_outfit:%s" % outfit_id
		return false
	var cid: String = str(odef.get("CharacterId", ""))
	if not loadouts.has(cid):
		last_error = "no_loadout:%s" % cid
		return false
	var bag: Dictionary = loadouts[cid]
	var unlocked: Array = bag.get("unlockedOutfits", []) as Array
	if not unlocked.has(outfit_id):
		unlocked.append(outfit_id)
		bag["unlockedOutfits"] = unlocked
	return true


func equip_outfit(character_id: String, outfit_id: String) -> bool:
	outfit_id = soul_cfg.resolve_outfit_id(outfit_id)
	if not select_character(character_id):
		return false
	var bag: Dictionary = loadouts[character_id]
	var unlocked: Array = bag.get("unlockedOutfits", []) as Array
	if not unlocked.has(outfit_id):
		last_error = "outfit_locked:%s" % outfit_id
		return false
	var odef: Dictionary = soul_cfg.outfit_def(outfit_id)
	if str(odef.get("CharacterId", "")) != character_id:
		last_error = "outfit_character_mismatch"
		return false
	bag["outfitId"] = outfit_id
	return true


func apply_soul_drop(drop: Dictionary) -> void:
	## 抽魂結果寫入 unlocked；outfit 類才解鎖
	if str(drop.get("kind", "")) != "outfit":
		return
	unlock_outfit(str(drop.get("DropId", "")))


func base_path(character_id: String = "") -> String:
	var cid: String = character_id if character_id != "" else active_character_id
	var bag: Dictionary = loadouts.get(cid, {}) as Dictionary
	return str(bag.get("baseAsset", ""))


func outfit_atlas_path() -> String:
	return str(soul_cfg.outfit_atlas)


func outfit_atlas_rect(outfit_id: String) -> Rect2:
	## outfits_x4：四欄橫切（1280×720 → 每欄 320×720）
	var odef: Dictionary = soul_cfg.outfit_def(outfit_id)
	var col: int = int(odef.get("atlasCol", 0))
	var cols: int = max(1, int(soul_cfg.outfit_atlas_cols))
	# 以常見 1280 寬為預設；載入時 View 可依實際紋理覆寫
	var cell_w := 1280.0 / float(cols)
	return Rect2(col * cell_w, 0.0, cell_w, 720.0)


func display_frame_for_phase(phase: String) -> String:
	## MVP：動作幀仍共用兔 frames/；base 圖供選角預覽
	match phase:
		"battle":
			return FramesScript.anim_path("ready")
		"dismantle":
			return FramesScript.anim_path("dismantle_pull")
		_:
			return FramesScript.anim_path("explore_walk")


func summary() -> Dictionary:
	var bag: Dictionary = loadouts.get(active_character_id, {}) as Dictionary
	return {
		"activeCharacterId": active_character_id,
		"allowed": Array(soul_cfg.character_ids()),
		"blocked": soul_cfg.blocked,
		"outfitId": str(bag.get("outfitId", "")),
		"unlockedOutfits": bag.get("unlockedOutfits", []),
		"baseAsset": base_path(),
		"outfitAtlas": outfit_atlas_path(),
	}
