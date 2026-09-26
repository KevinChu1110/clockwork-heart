extends RefCounted
class_name RegionCatalog
## 四地區・關卡表（玩家可見）。對齊原作「四個地區／數個關卡／數張地圖」。
## 內部仍用六域探索；此表是戰役進度視圖。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## 四地區；每區數關；每關對應探索地圖／通關旗
static func regions() -> Array:
	return [
		{
			"id": "r1",
			"name": _t("第一區・閣樓與堡壘"),
			"blurb": _t("閣樓、堡壘與野原。初試鋒刃。"),
			"stages": [
				{
					"id": "r1_s1",
					"name": _t("關卡 1・玩具堆外緣"),
					"maps": [{"id": "road", "label": _t("玩具堆外緣")}],
					"unlock": [],
					"clear_flag": "c0_first_battle",
					"boss": "",
					"goto": {"map": "road", "screen": "C0_ROAD"},
				},
				{
					"id": "r1_s2",
					"name": _t("關卡 2・堡壘的門"),
					"maps": [
						{"id": "town", "label": _t("堡壘廣場")},
						{"id": "wild", "label": _t("堡外野原")},
					],
					"unlock": ["c0_first_battle"],
					"clear_flag": "boss.leo_cleared",
					"boss": _t("守衛泰坦·雷歐"),
					"goto": {"map": "town", "screen": "C1_TOWN"},
				},
			],
		},
		{
			"id": "r2",
			"name": _t("第二區・白霧之地"),
			"blurb": _t("白霧、霧崖與鏡廊。看破虛影。"),
			"stages": [
				{
					"id": "r2_s1",
					"name": _t("關卡 1・白霧之地"),
					"maps": [
						{"id": "mist_village", "label": _t("白霧之地外緣")},
						{"id": "mist_cliff", "label": _t("霧崖")},
					],
					"unlock": ["boss.leo_cleared"],
					"clear_flag": "boss.white_fog_cleared",
					"boss": _t("白霧"),
					"goto": {"map": "mist_village", "screen": "C2_MIST"},
				},
				{
					"id": "r2_s2",
					"name": _t("關卡 2・鏡廊"),
					"maps": [{"id": "mist_mirror", "label": _t("鏡廊")}],
					"unlock": ["boss.leo_cleared"],
					"clear_flag": "boss.white_fog_cleared",
					"boss": _t("鏡廊殘影（秘境）"),
					"optional": true,
					"goto": {"map": "mist_mirror", "screen": "C2_MIST"},
				},
			],
		},
		{
			"id": "r3",
			"name": _t("第三區・道場與西林"),
			"blurb": _t("道場、森林與石岸。力與速的試煉。"),
			"stages": [
				{
					"id": "r3_s1",
					"name": _t("關卡 1・武鬥道場"),
					"maps": [{"id": "dojo", "label": _t("武鬥道場")}],
					"unlock": ["boss.white_fog_cleared"],
					"clear_flag": "boss.abo_cleared",
					"boss": _t("阿波"),
					"goto": {"map": "dojo", "screen": "C3_DOJO"},
				},
				{
					"id": "r3_s2",
					"name": _t("關卡 2・西林"),
					"maps": [{"id": "forest", "label": _t("西林")}],
					"unlock": ["boss.abo_cleared"],
					"clear_flag": "boss.shadowwind_cleared",
					"boss": _t("疾影"),
					"goto": {"map": "forest", "screen": "C4_FOREST"},
				},
				{
					"id": "r3_s3",
					"name": _t("關卡 3・石拳海岸"),
					"maps": [{"id": "coast_cliff", "label": _t("石岸")}],
					"unlock": ["boss.shadowwind_cleared"],
					"clear_flag": "boss.stonefist_cleared",
					"boss": _t("石拳"),
					"goto": {"map": "coast_cliff", "screen": "C5_COAST"},
				},
			],
		},
		{
			"id": "r4",
			"name": _t("第四區・潮岸與終境"),
			"blurb": _t("沉船、疤地與通天塔。旅程的盡頭。"),
			"stages": [
				{
					"id": "r4_s1",
					"name": _t("關卡 1・潮岸沉船"),
					"maps": [
						{"id": "coast", "label": _t("海岸")},
						{"id": "coast_wreck", "label": _t("沉船")},
					],
					"unlock": ["boss.stonefist_cleared"],
					"clear_flag": "soul.relic.wreck_captain",
					"boss": _t("沉船船長影（秘境）"),
					"optional": true,
					"goto": {"map": "coast", "screen": "C5_COAST"},
				},
				{
					"id": "r4_s2",
					"name": _t("關卡 2・通天塔"),
					"maps": [
						{"id": "tower_camp", "label": _t("塔下營地")},
						{"id": "tower_foyer", "label": _t("通天塔層")},
					],
					"unlock": ["boss.stonefist_cleared"],
					"clear_flag": "boss.demon_cleared",
					"boss": _t("塔底"),
					## 魔王在塔裡，不在疤地：前往要開塔下營地（main 會走 _go_c6_camp 的門檻）
					"goto": {"map": "tower_camp", "screen": "C6_TOWER"},
				},
			],
		},
	]


static func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


static func _flags_ok(need: Array) -> bool:
	var gs := _gs()
	for f in need:
		if gs and not gs.has_flag(str(f)):
			return false
	return true


static func stage_state(stage: Dictionary) -> String:
	## locked | open | cleared
	var unlock: Array = stage.get("unlock", [])
	if not _flags_ok(unlock):
		return "locked"
	var cf := str(stage.get("clear_flag", ""))
	var gs := _gs()
	if cf != "" and gs and gs.has_flag(cf):
		return "cleared"
	return "open"


static func region_progress(region: Dictionary) -> Dictionary:
	var stages: Array = region.get("stages", [])
	var cleared := 0
	for s in stages:
		if stage_state(s) == "cleared":
			cleared += 1
	return {"cleared": cleared, "total": stages.size()}


## 主線「下一站」：第一個已解鎖未通關的必經關卡；主線全清後退而指秘境；都清了回空
static func next_objective() -> Dictionary:
	var fallback: Dictionary = {}
	for r in regions():
		for s in r.get("stages", []):
			if stage_state(s) != "open":
				continue
			var row: Dictionary = s.duplicate(true)
			row["region"] = str(r.get("name", ""))
			if bool(s.get("optional", false)):
				if fallback.is_empty():
					fallback = row
				continue
			return row
	return fallback


## 各關建議等級：讀取 pacing_s1.json（表上未定義關卡維持 0）。
## 主線指引、雷歐前的軟提示與出征關卡皆以本表為準。
const PACING_TABLE_PATH := "res://data/tables/pacing_s1.json"
static var SUGGEST_LV: Dictionary = _load_suggest_lv()
static var EXPEDITION_SUGGEST_LV: Dictionary = _load_expedition_suggest_lv()


static func _load_suggest_lv() -> Dictionary:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("suggest_lv_table"):
			var tbl: Dictionary = dt.call("suggest_lv_table")
			if not tbl.is_empty():
				return tbl.duplicate()
	if FileAccess.file_exists(PACING_TABLE_PATH):
		var f := FileAccess.open(PACING_TABLE_PATH, FileAccess.READ)
		if f != null:
			var data = JSON.parse_string(f.get_as_text())
			if data is Dictionary:
				var slv = data.get("suggest_lv", {})
				if slv is Dictionary:
					return slv.duplicate()
	return {}


static func _load_expedition_suggest_lv() -> Dictionary:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("expedition_suggest_lv_table"):
			var tbl: Dictionary = dt.call("expedition_suggest_lv_table")
			if not tbl.is_empty():
				return tbl.duplicate()
	if FileAccess.file_exists(PACING_TABLE_PATH):
		var f := FileAccess.open(PACING_TABLE_PATH, FileAccess.READ)
		if f != null:
			var data = JSON.parse_string(f.get_as_text())
			if data is Dictionary:
				var slv = data.get("expedition_suggest_lv", {})
				if slv is Dictionary:
					return slv.duplicate()
	return {}


static func expedition_suggest_lv(stage_num: String) -> int:
	if EXPEDITION_SUGGEST_LV.is_empty():
		EXPEDITION_SUGGEST_LV = _load_expedition_suggest_lv()
	return int(EXPEDITION_SUGGEST_LV.get(stage_num, 0))


static func suggest_lv(stage_id: String) -> int:
	if SUGGEST_LV.is_empty():
		SUGGEST_LV = _load_suggest_lv()
	if SUGGEST_LV.has(stage_id):
		return int(SUGGEST_LV.get(stage_id, 0))
	return expedition_suggest_lv(stage_id)


static func next_objective_line() -> String:
	var o := next_objective()
	if o.is_empty():
		return _t("主線已完結——發條新村、演武與獵場都在等你。")
	var boss := str(o.get("boss", ""))
	var line: String
	if boss != "":
		line = _t("下一站：%s · %s") % [str(o.get("name", "")), boss]
	else:
		line = _t("下一站：%s") % str(o.get("name", ""))
	## 等級還不到就把數字講出來。鍛造完 Lv2 直衝雷歐是 0% 勝率，
	## 而指引只寫「下一站：雷歐」——玩家照著走會撞牆，還不知道該練到幾級。
	var need := suggest_lv(str(o.get("id", "")))
	var gs := _gs()
	var p_lv := int(gs.get("level")) if gs and "level" in gs else 1
	if need > 0 and p_lv < need:
		line += _t("（建議 Lv%d）") % need
	return line


static func status_bbcode() -> String:
	var lines: PackedStringArray = []
	lines.append(_t("[b]世界地圖・四地區關卡[/b]"))
	lines.append("[color=#fc9]%s[/color]" % next_objective_line())
	lines.append(_t("四區，各有數關。點關卡可前往。"))
	lines.append("")
	for r in regions():
		var prog: Dictionary = region_progress(r)
		lines.append("[b]%s[/b]  %d／%d" % [str(r.get("name", "")), int(prog.cleared), int(prog.total)])
		lines.append(str(r.get("blurb", "")))
		for s in r.get("stages", []):
			var st := stage_state(s)
			var mark := "·"
			if st == "open":
				mark = "▶"
			elif st == "cleared":
				mark = "✓"
			var boss := str(s.get("boss", ""))
			var boss_s := (" · " + boss) if boss != "" else ""
			lines.append("  %s %s%s" % [mark, str(s.get("name", "")), boss_s])
			var maps: Array = s.get("maps", [])
			if not maps.is_empty():
				var bits: PackedStringArray = []
				for m in maps:
					bits.append(str(m.get("label", m.get("id", ""))))
				lines.append("     " + _t("地圖：") + "、".join(bits))
		lines.append("")
	return "\n".join(lines)


static func flat_open_stages() -> Array:
	var out: Array = []
	for r in regions():
		for s in r.get("stages", []):
			var st := stage_state(s)
			if st == "locked":
				continue
			var row: Dictionary = s.duplicate(true)
			row["region"] = str(r.get("name", ""))
			row["state"] = st
			out.append(row)
	return out
