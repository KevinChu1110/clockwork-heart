extends RefCounted
class_name MapCatalog
## 大地圖定義：尺寸、出生點、實體列表。世界座標以 origin 為左上可行走區。
## 0.9：六域多層分區（40+ 張可走地圖）。

const TILE := 32
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

## 回傳 {title, bg_color, origin, size, spawn, art, entities:[{id,pos,size,label,color,solid?}]}
##
## 地名與物件標籤在非繁中會被 ContentLoc 換掉（domain "map"），以原文當 key。
## 不用物件 id 當 key 是因為同一個 id 在不同地圖上是不同的字（back_town 有
## 「回外城廣場」也有「回城」），實測 39 個這種撞名，用 id 會翻錯。
static func build(id: String) -> Dictionary:
	var m := _build_raw(id)
	if ContentLoc.locale() == "zh_TW":
		return m
	m = m.duplicate(true)
	m["title"] = ContentLoc.text("map", str(m.get("title", "")))
	for e in m.get("entities", []):
		if typeof(e) == TYPE_DICTIONARY:
			e["label"] = ContentLoc.text("map", str(e.get("label", "")))
	return m


static func _build_raw(id: String) -> Dictionary:
	match id:
		"village":
			return _village()
		"village_outskirts":
			return _village_outskirts()
		"village_mill":
			return _village_mill()
		"village_cave":
			return _village_cave()
		"village_grave":
			return _village_grave()
		"road":
			return _road()
		"road_bridge":
			return _road_bridge()
		"road_inn":
			return _road_inn()
		"road_ruins":
			return _road_ruins()
		"town":
			return _town()
		"town_forge":
			return _town_forge()
		"town_soul":
			return _town_soul()
		"town_gem":
			return _town_gem()
		"town_tutor":
			return _town_tutor()
		"town_keep":
			return _town_keep()
		"town_market":
			return _town_market()
		"town_sewers":
			return _town_sewers()
		"barracks_yard":
			return _barracks_yard()
		"wild":
			return _wild()
		"wild_ravine":
			return _wild_ravine()
		"wild_leo_court":
			return _wild_leo_court()
		"crossroads":
			return _crossroads()
		"cross_north":
			return _cross_north()
		"cross_east":
			return _cross_east()
		"caravan_camp":
			return _caravan_camp()
		"starfall_plain":
			return _starfall_plain()
		"blackflame_scar":
			return _blackflame_scar()
		"hunting_grounds":
			return _hunting_grounds()
		"mist_village":
			return _mist()
		"mist_deep":
			return _mist_deep()
		"mist_cliff":
			return _mist_cliff()
		"mist_shrine":
			return _mist_shrine()
		"mist_mirror":
			return _mist_mirror()
		"dojo":
			return _dojo()
		"dojo_inner":
			return _dojo_inner()
		"dojo_bamboo":
			return _dojo_bamboo()
		"dojo_peak":
			return _dojo_peak()
		"forest":
			return _forest()
		"forest_deep":
			return _forest_deep()
		"forest_canopy":
			return _forest_canopy()
		"forest_ruins":
			return _forest_ruins()
		"forest_lake":
			return _forest_lake()
		"coast":
			return _coast()
		"coast_cliff":
			return _coast_cliff()
		"coast_harbor":
			return _coast_harbor()
		"coast_cave":
			return _coast_cave()
		"coast_wreck":
			return _coast_wreck()
		"tower_camp":
			return _tower_camp()
		"tower_foyer":
			return _tower_foyer()
		"tower_stairs":
			return _tower_stairs()
		"tower_memory":
			return _tower_memory()
		_:
			return _fallback(id)


static func _base(title: String, col: Color, w: float, h: float, spawn: Vector2, art: String) -> Dictionary:
	return {
		"title": title,
		"bg_color": col,
		"origin": Vector2(40, 80),
		"size": Vector2(w, h),
		"spawn": spawn,
		"art": art,
		"entities": [],
	}


static func _e(id: String, x: float, y: float, w: float, h: float, label: String, c: Color, solid := false) -> Dictionary:
	return {"id": id, "pos": Vector2(x, y), "size": Vector2(w, h), "label": label, "color": c, "solid": solid}


## GameState 走執行期查找（見 SpriteDB._gs）：-s 測試編譯早於 autoload。
static func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


static func _flag(fid: String) -> bool:
	var gs := _gs()
	return gs != null and bool(gs.call("has_flag", fid))


# ═══════════════════════════════════════════
#  翠谷
# ═══════════════════════════════════════════

static func _village() -> Dictionary:
	## 原作村莊是一屏據點：人站廣場泥路上，點誰跟誰說話，不繞屋頂。
	var m := _base("翠谷村 · 夜（本村）", Color(0.08, 0.04, 0.05), 2800, 1562, Vector2(1360, 980), "village")
	m["entities"] = [
		_e("hut_a", 448, 506, 80, 72, "焦黑茅屋", Color(0.35, 0.25, 0.2), true),
		_e("hut_b", 816, 427, 72, 64, "塌半的倉", Color(0.4, 0.28, 0.2), true),
		_e("hut_c", 1139, 1280, 70, 60, "半毀木屋", Color(0.38, 0.26, 0.22), true),
		_e("maisui", 1476, 936, 48, 64, "麥穗", Color(0.85, 0.55, 0.45)),
		_e("well", 1470, 886, 52, 52, "井沿", Color(0.4, 0.42, 0.45), true),
		_e("sword", 1376, 932, 48, 48, "鏽劍", Color(0.55, 0.5, 0.4)),
		_e("ash_pile", 1698, 938, 44, 40, "灰堆", Color(0.3, 0.28, 0.28)),
		_e("fire", 1860, 823, 56, 56, "火光", Color(0.9, 0.35, 0.1), true),
		_e("cart", 1116, 652, 60, 52, "翻倒的車", Color(0.45, 0.35, 0.25), true),
		_e("fence_row", 556, 950, 200, 28, "燒焦籬笆", Color(0.3, 0.25, 0.2), true),
		_e("field_west", 414, 1154, 120, 48, "西邊田埂", Color(0.35, 0.3, 0.2)),
		_e("sign_east", 1718, 848, 44, 52, "往東", Color(0.4, 0.35, 0.25)),
		_e("exit_east", 1744, 860, 72, 80, "往東", Color(0.3, 0.25, 0.2)),
		_e("exit_outskirts", 298, 835, 72, 64, "村外田野", Color(0.35, 0.4, 0.3)),
		_e("to_cave", 2066, 220, 64, 56, "山邊洞窟", Color(0.3, 0.28, 0.32)),
		_e("to_grave", 2402, 1117, 64, 56, "村後墓園", Color(0.35, 0.32, 0.3)),
		_e("shrine_stub", 1626, 248, 48, 56, "村口小祠", Color(0.45, 0.4, 0.35), true),
		_e("orchard", 1972, 1292, 56, 48, "枯果園", Color(0.4, 0.35, 0.28)),
		_e("message_stone", 1556, 968, 48, 52, "留言石", Color(0.5, 0.55, 0.7), true),
	]
	return m


static func _village_outskirts() -> Dictionary:
	var m := _base("翠谷 · 村外田野", Color(0.07, 0.08, 0.06), 2600, 1451, Vector2(690, 951), "village")
	m["entities"] = [
		_e("back_village", 363, 786, 56, 56, "回村子", Color(0.4, 0.35, 0.3)),
		_e("scare_field", 653, 1040, 48, 56, "稻草人", Color(0.4, 0.35, 0.25)),
		_e("pond", 1040, 867, 80, 48, "乾涸池塘", Color(0.3, 0.35, 0.4), true),
		_e("woodpile", 870, 547, 56, 40, "木柴堆", Color(0.45, 0.35, 0.25)),
		_e("to_mill", 1425, 233, 64, 64, "風車田", Color(0.4, 0.42, 0.35)),
		_e("trail_east", 2292, 669, 72, 64, "接荒路", Color(0.35, 0.4, 0.3)),
		_e("windmill", 1726, 236, 60, 80, "風車殘架", Color(0.4, 0.38, 0.35), true),
		_e("stone_circle", 1676, 1157, 56, 48, "石圈", Color(0.42, 0.4, 0.38)),
	]
	return m


static func _village_mill() -> Dictionary:
	var m := _base("翠谷 · 風車田與碾坊", Color(0.09, 0.1, 0.07), 2400, 1350, Vector2(912, 1269), "village_mill")
	m["entities"] = [
		_e("back_from_mill", 840, 1215, 56, 56, "回田野", Color(0.4, 0.35, 0.3)),
		_e("big_mill", 864, 891, 96, 120, "巨風車", Color(0.45, 0.42, 0.38), true),
		_e("grain_silo", 1320, 864, 56, 64, "糧倉", Color(0.5, 0.4, 0.3), true),
		_e("miller_hut", 1680, 864, 64, 56, "碾坊主屋", Color(0.42, 0.36, 0.28), true),
		_e("wheat_sea", 2112, 837, 80, 48, "麥浪坡", Color(0.55, 0.5, 0.3)),
		_e("mill_to_road", 2208, 1080, 64, 56, "捷徑·荒路", Color(0.35, 0.4, 0.3)),
		_e("scare_b", 744, 1026, 40, 48, "第二稻草人", Color(0.4, 0.35, 0.25)),
	]
	return m


static func _village_cave() -> Dictionary:
	var m := _base("翠谷 · 山邊舊礦洞", Color(0.06, 0.06, 0.08), 2200, 1238, Vector2(304, 872), "village_cave")
	m["entities"] = [
		_e("back_from_cave", 276, 792, 56, 56, "回村子", Color(0.4, 0.35, 0.3)),
		_e("cave_mouth", 1056, 577, 80, 72, "洞口", Color(0.25, 0.25, 0.3), true),
		_e("ore_cart", 672, 783, 56, 40, "礦車", Color(0.4, 0.35, 0.3)),
		_e("glow_moss", 1384, 733, 40, 40, "螢光苔", Color(0.3, 0.55, 0.4)),
		_e("deep_dark", 1108, 866, 64, 56, "更深的黑", Color(0.2, 0.2, 0.25)),
		_e("old_pick", 592, 1059, 40, 36, "斷鎬", Color(0.45, 0.4, 0.35)),
		_e("echo_wall", 1688, 759, 48, 64, "回音壁", Color(0.35, 0.35, 0.4), true),
	]
	return m


static func _village_grave() -> Dictionary:
	var m := _base("翠谷 · 村後墓園", Color(0.07, 0.07, 0.09), 2200, 1238, Vector2(480, 947), "village_grave")
	var lamp_lab := "長明燈（亮）" if _flag("side.lantern_done") else "長明燈"
	m["entities"] = [
		_e("back_from_grave", 452, 866, 56, 56, "回村子", Color(0.4, 0.35, 0.3)),
		_e("stone_gate", 1284, 429, 64, 72, "墓園門", Color(0.4, 0.38, 0.4), true),
		_e("grave_a", 680, 849, 40, 48, "無名碑", Color(0.45, 0.42, 0.4), true),
		_e("grave_b", 900, 824, 40, 48, "舊碑", Color(0.42, 0.4, 0.38), true),
		_e("willow", 540, 867, 56, 80, "垂柳", Color(0.3, 0.4, 0.32), true),
		_e("lantern_post", 1166, 767, 36, 56, lamp_lab, Color(0.55, 0.5, 0.35)),
		_e("fresh_earth", 1072, 1105, 48, 40, "新土", Color(0.35, 0.3, 0.25)),
		_e("hill_edge", 1596, 750, 56, 48, "遠眺丘", Color(0.35, 0.38, 0.32)),
	]
	return m


# ═══════════════════════════════════════════
#  荒路
# ═══════════════════════════════════════════

static func _road() -> Dictionary:
	var m := _base("荒路 · 橫貫翠嶺東道", Color(0.12, 0.16, 0.22), 3600, 2009, Vector2(2520, 1763), "road")
	m["entities"] = [
		_e("look_back", 2376, 1672, 48, 48, "煙柱（村）", Color(0.4, 0.35, 0.35)),
		_e("milepost", 2232, 1403, 40, 56, "里程碑·一", Color(0.45, 0.42, 0.4), true),
		_e("to_road_inn", 1872, 969, 64, 56, "路旁客棧", Color(0.5, 0.4, 0.3)),
		_e("bush_a", 1512, 964, 48, 40, "灌木", Color(0.3, 0.35, 0.28)),
		_e("wolf", 1368, 701, 64, 64, "灌木異響", Color(0.35, 0.3, 0.35)),
		_e("milepost_b", 1800, 644, 40, 56, "里程碑·二", Color(0.45, 0.42, 0.4), true),
		_e("to_road_bridge", 684, 561, 64, 56, "大橋段", Color(0.4, 0.42, 0.45)),
		_e("to_road_ruins", 1808, 305, 64, 56, "古驛廢墟", Color(0.4, 0.38, 0.35)),
		_e("bush_b", 1980, 230, 48, 40, "黑刺叢", Color(0.28, 0.3, 0.28)),
		_e("road_stone", 1692, 419, 40, 36, "裂開的路石", Color(0.4, 0.38, 0.36)),
		_e("camp_ash", 1080, 692, 56, 40, "路人餘燼", Color(0.4, 0.3, 0.25)),
		_e("bridge", 900, 641, 80, 48, "小橋", Color(0.4, 0.38, 0.35), true),
		_e("dawn_glow", 2244, 345, 56, 56, "東邊亮光·城", Color(0.55, 0.5, 0.4)),
		_e("exit_town_hint", 180, 564, 72, 64, "通往騎士堡方向", Color(0.4, 0.4, 0.45)),
	]
	return m


static func _road_bridge() -> Dictionary:
	var m := _base("荒路 · 斷崖大橋", Color(0.1, 0.14, 0.2), 2600, 1462, Vector2(390, 877), "road_bridge")
	m["entities"] = [
		_e("back_road", 312, 804, 56, 56, "回主路", Color(0.4, 0.4, 0.45)),
		_e("bridge_arch", 1716, 643, 120, 64, "石拱橋", Color(0.45, 0.43, 0.42), true),
		_e("ravine_view", 910, 907, 64, 48, "深谷俯瞰", Color(0.3, 0.35, 0.4)),
		_e("toll_ruin", 1430, 673, 56, 56, "廢稅亭", Color(0.42, 0.38, 0.35), true),
		_e("broken_rail", 1872, 614, 80, 32, "斷欄杆", Color(0.4, 0.35, 0.3), true),
		_e("east_span", 2418, 658, 64, 56, "橋東·接主路", Color(0.4, 0.42, 0.45)),
		_e("nest_under", 1612, 877, 48, 40, "橋下鳥巢" + ("（已顧）" if _flag("side.nest_care_done") else ""), Color(0.35, 0.4, 0.3)),
	]
	return m


static func _road_inn() -> Dictionary:
	var m := _base("荒路 · 半塌客棧", Color(0.11, 0.1, 0.12), 2200, 1238, Vector2(990, 681), "road_inn")
	var hearth_lab := "壁爐（暖）" if _flag("side.hearth_lit") else "熄滅壁爐"
	m["entities"] = [
		_e("back_road", 2024, 966, 56, 56, "回主路", Color(0.4, 0.4, 0.45)),
		_e("inn_sign", 726, 817, 48, 56, "「歇腳」破牌", Color(0.5, 0.4, 0.3), true),
		_e("common_room", 528, 768, 80, 64, "大堂", Color(0.42, 0.35, 0.28), true),
		_e("hearth", 264, 780, 56, 48, hearth_lab, Color(0.35, 0.3, 0.28), true),
		_e("cellar_hatch", 924, 891, 48, 40, "地窖口", Color(0.3, 0.28, 0.25)),
		_e("stable_ruin", 1540, 557, 64, 56, "馬廄廢墟", Color(0.4, 0.36, 0.3), true),
		_e("guest_bed", 1848, 570, 48, 40, "塌床", Color(0.45, 0.38, 0.32)),
		_e("road_note", 1320, 990, 40, 40, "留言板", Color(0.5, 0.45, 0.35)),
	]
	return m


static func _road_ruins() -> Dictionary:
	var m := _base("荒路 · 古驛站廢墟", Color(0.1, 0.12, 0.14), 2400, 1350, Vector2(480, 1148), "road_ruins")
	m["entities"] = [
		_e("back_road", 384, 1188, 56, 56, "回主路", Color(0.4, 0.4, 0.45)),
		_e("column_a", 576, 783, 40, 72, "斷柱", Color(0.45, 0.42, 0.4), true),
		_e("column_b", 960, 756, 40, 64, "斷柱", Color(0.42, 0.4, 0.38), true),
		_e("mosaic", 1200, 918, 72, 48, "碎馬賽克", Color(0.5, 0.45, 0.4)),
		_e("courier_post", 1776, 864, 56, 56, "驛亭基座", Color(0.4, 0.38, 0.35), true),
		_e("sealed_chest", 840, 1013, 48, 40, "封箱", Color(0.45, 0.35, 0.25)),
		_e("star_mark", 1320, 405, 48, 48, "星曜刻紋", Color(0.5, 0.55, 0.7)),
		_e("to_starfall", 2112, 972, 64, 56, "往星落平原", Color(0.45, 0.5, 0.65)),
	]
	return m


# ═══════════════════════════════════════════
#  騎士堡
# ═══════════════════════════════════════════

static func _town() -> Dictionary:
	var m := _base("騎士堡壘 · 外城廣場", Color(0.1, 0.11, 0.14), 3200, 1785, Vector2(1640, 1508), "town")
	var flag_label := "旗幟（兔爪）" if _flag("c1_flag_paw") else "灰旗"
	## 整張廣場一屏看完：店門貼建築、人站泥路、出口在圖緣。腳點全在 walkmask 內，彼此 ≥100px。
	## 左屋＝鐵匠鋪、中央石屋＝武術館、右上掛旗木屋＝聚魂殿、右大屋＝手藝工坊、東北小徑＝出城。
	m["entities"] = [
		_e("greybeard", 1546, 885, 48, 64, "灰鬚", Color(0.55, 0.55, 0.6)),
		_e("tutor_hall", 1688, 848, 44, 44, "武術館", Color(0.5, 0.48, 0.52)),
		_e("wall_notice", 1426, 849, 44, 52, "告示牆", Color(0.45, 0.4, 0.35), true),
		_e("board_today", 1280, 1219, 48, 48, "今日村莊", Color(0.55, 0.45, 0.32), true),
		_e("hunt_board", 1488, 1326, 48, 48, "野外獵場", Color(0.4, 0.38, 0.32), true),
		_e("visit_board", 1072, 1250, 48, 44, "旅人木牌", Color(0.5, 0.48, 0.4), true),
		_e("message_stone", 1760, 1456, 48, 52, "留言石", Color(0.5, 0.55, 0.7), true),
		_e("to_market", 1160, 1586, 64, 56, "下城市集", Color(0.5, 0.4, 0.3)),
		_e("market", 1192, 1099, 64, 52, "攤位殘架", Color(0.5, 0.4, 0.3), true),
		_e("ding", 1008, 1560, 48, 64, "釘釘", Color(0.7, 0.4, 0.25)),
		_e("forge_sign", 834, 1491, 44, 44, "鐵匠鋪", Color(0.55, 0.4, 0.25)),
		_e("gem_shop", 2670, 1274, 52, 56, "手藝工坊", Color(0.75, 0.35, 0.4)),
		_e("fountain", 1848, 1153, 64, 52, "乾涸水池", Color(0.4, 0.45, 0.5), true),
		_e("flag", 982, 836, 48, 56, flag_label, Color(0.85, 0.75, 0.35), true),
		_e("star", 1984, 885, 48, 64, "星讀", Color(0.45, 0.5, 0.75)),
		_e("soul_hall", 2130, 848, 44, 44, "聚魂殿", Color(0.4, 0.45, 0.7)),
		_e("bench", 2112, 1231, 48, 36, "石凳", Color(0.45, 0.45, 0.48)),
		_e("sprout", 1632, 1185, 48, 64, "小芽", Color(0.55, 0.75, 0.45)),
		_e("silk", 2294, 908, 48, 64, "絲絨", Color(0.55, 0.5, 0.65)),
		_e("to_barracks_yard", 488, 1202, 64, 56, "演武場", Color(0.4, 0.38, 0.4)),
		_e("barracks", 436, 1096, 72, 64, "舊兵營", Color(0.4, 0.38, 0.4), true),
		_e("chapel", 1826, 793, 64, 72, "小禮拜堂", Color(0.45, 0.42, 0.48), true),
		_e("to_sewers", 1804, 1585, 56, 48, "下水道口", Color(0.3, 0.32, 0.3)),
		_e("gate_arch", 1292, 793, 56, 72, "內城門影", Color(0.4, 0.38, 0.42), true),
		_e("exit_keep", 1148, 854, 56, 56, "內城", Color(0.45, 0.4, 0.35)),
		_e("exit_wild", 2988, 417, 56, 56, "荒野", Color(0.35, 0.4, 0.3)),
		_e("exit_world", 588, 1452, 56, 56, "六域地圖", Color(0.4, 0.5, 0.55)),
		_e("menu_save", 1984, 1362, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("stable", 2392, 1354, 64, 56, "空馬廄", Color(0.42, 0.36, 0.3), true),
	]
	return m


static func _town_forge() -> Dictionary:
	## 原作村內鐵匠鋪：走進才見到爐與釘釘。世界 16:9，實體腳底對齊 ¾ 俯視地板。
	var m := _base("騎士堡 · 鐵匠鋪", Color(0.16, 0.08, 0.06), 1458, 820, Vector2(769, 769), "town_forge")
	m["entities"] = [
		_e("back_from_shop", 741, 786, 56, 48, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("ding", 628, 590, 48, 64, "釘釘·鐵匠", Color(0.7, 0.4, 0.25)),
		_e("anvil", 843, 565, 56, 40, "鐵砧", Color(0.5, 0.42, 0.35), true),
		_e("forge_hearth", 445, 532, 64, 56, "爐心", Color(0.75, 0.35, 0.18), true),
		_e("bellows", 249, 614, 48, 40, "風箱", Color(0.45, 0.32, 0.25), true),
		_e("scrap_bin", 1241, 630, 48, 40, "廢鐵桶", Color(0.4, 0.38, 0.32)),
	]
	return m


static func _town_soul() -> Dictionary:
	var m := _base("騎士堡 · 聚魂殿", Color(0.07, 0.08, 0.16), 1458, 820, Vector2(769, 785), "town_soul")
	m["entities"] = [
		_e("back_from_shop", 741, 795, 56, 48, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("star", 687, 606, 48, 64, "星讀", Color(0.45, 0.5, 0.75)),
		_e("astrolabe", 508, 508, 56, 48, "星盤台", Color(0.4, 0.45, 0.7), true),
		_e("gourd_shelf", 337, 532, 48, 56, "葫蘆架", Color(0.35, 0.5, 0.4), true),
		_e("star_mat", 810, 569, 64, 36, "觀星墊", Color(0.3, 0.32, 0.5)),
	]
	return m


static func _town_gem() -> Dictionary:
	var m := _base("騎士堡 · 手藝工坊", Color(0.14, 0.07, 0.09), 1458, 820, Vector2(740, 769), "town_gem")
	m["entities"] = [
		_e("back_from_shop", 858, 786, 56, 48, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("gem_clerk", 512, 574, 48, 64, "工坊師傅", Color(0.75, 0.35, 0.4)),
		_e("gem_case", 1062, 426, 56, 48, "寶石櫃", Color(0.7, 0.3, 0.35), true),
		_e("cold_furnace", 333, 504, 56, 52, "冷熔爐", Color(0.45, 0.28, 0.3), true),
		_e("shard_box", 337, 634, 48, 36, "碎片匣", Color(0.55, 0.4, 0.35)),
	]
	return m


static func _town_tutor() -> Dictionary:
	var m := _base("騎士堡 · 武術館", Color(0.11, 0.1, 0.12), 1458, 820, Vector2(507, 736), "town_tutor")
	m["entities"] = [
		_e("back_from_shop", 449, 737, 56, 48, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("greybeard", 599, 557, 48, 64, "灰鬚", Color(0.55, 0.55, 0.6)),
		_e("training_dummy", 778, 500, 40, 56, "木人樁", Color(0.5, 0.42, 0.32), true),
		_e("weapon_wall", 274, 410, 56, 64, "兵器牆", Color(0.45, 0.42, 0.4), true),
		_e("floor_mat", 412, 487, 72, 36, "練武墊", Color(0.4, 0.35, 0.3)),
	]
	return m


static func _town_keep() -> Dictionary:
	var m := _base("騎士堡 · 內城與內殿道", Color(0.09, 0.09, 0.12), 2600, 1451, Vector2(690, 1154), "town")
	m["entities"] = [
		_e("back_town", 571, 1170, 56, 56, "回外城廣場", Color(0.4, 0.4, 0.45)),
		_e("hall", 936, 675, 80, 72, "騎士舊廳", Color(0.4, 0.38, 0.42), true),
		_e("armor", 1177, 677, 40, 56, "空盔甲架", Color(0.5, 0.5, 0.55)),
		_e("throne_hall", 1421, 662, 72, 64, "議政廳門", Color(0.45, 0.4, 0.35), true),
		_e("keep_well", 1264, 961, 48, 48, "內井", Color(0.4, 0.42, 0.48), true),
		_e("statue_knight", 679, 829, 48, 64, "無名騎士像", Color(0.5, 0.48, 0.5), true),
		_e("archive", 1741, 706, 56, 56, "檔案庫門", Color(0.42, 0.4, 0.45), true),
		_e("silk", 1810, 858, 48, 64, "絲絨·書吏", Color(0.55, 0.5, 0.65)),
		_e("codex_shelf", 1862, 787, 48, 48, "典籍架", Color(0.45, 0.4, 0.5), true),
		_e("exit_wild_inner", 1044, 1322, 72, 64, "側門·荒野", Color(0.35, 0.4, 0.3)),
		_e("to_leo_court", 2309, 387, 64, 56, "內殿前院道", Color(0.5, 0.4, 0.3)),
	]
	return m


static func _town_market() -> Dictionary:
	var m := _base("騎士堡 · 下城市集", Color(0.11, 0.1, 0.12), 2600, 1451, Vector2(560, 1270), "town_market")
	m["entities"] = [
		_e("back_from_market", 532, 1185, 56, 56, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("stall_a", 740, 612, 56, 48, "布攤", Color(0.55, 0.4, 0.35), true),
		_e("stall_b", 1156, 554, 56, 48, "藥草攤", Color(0.4, 0.55, 0.35), true),
		_e("stall_c", 1520, 583, 56, 48, "空攤", Color(0.45, 0.4, 0.35), true),
		_e("scale_table", 796, 882, 48, 40, "天秤台", Color(0.5, 0.48, 0.4)),
		_e("beggar", 592, 1077, 40, 48, "坐地老人", Color(0.4, 0.38, 0.35)),
		_e("alley_dark", 1888, 662, 48, 56, "窄巷", Color(0.3, 0.3, 0.32)),
		_e("spice_smell", 1732, 940, 48, 40, "香料殘跡", Color(0.55, 0.4, 0.3)),
		_e("to_sewers", 1468, 1280, 56, 48, "市集下水口", Color(0.3, 0.32, 0.3)),
	]
	return m


static func _town_sewers() -> Dictionary:
	var m := _base("騎士堡 · 舊下水道", Color(0.06, 0.08, 0.07), 2400, 1350, Vector2(760, 1268), "town_sewers")
	m["entities"] = [
		_e("back_from_sewers", 732, 1185, 56, 56, "爬回地面", Color(0.4, 0.4, 0.45)),
		_e("pipe_a", 344, 788, 64, 48, "鐵管", Color(0.35, 0.38, 0.35), true),
		_e("slime_pool", 820, 1093, 72, 40, "黏液池", Color(0.3, 0.4, 0.3), true),
		_e("rat_nest", 1120, 877, 48, 40, "鼠窩", Color(0.35, 0.3, 0.28)),
		_e("sealed_door", 1452, 799, 56, 64, "封死鐵門", Color(0.4, 0.4, 0.42), true),
		_e("echo_drip", 1268, 1228, 40, 40, "滴水聲", Color(0.4, 0.45, 0.5)),
		_e("ladder_out", 2032, 969, 48, 56, "另一出口", Color(0.4, 0.42, 0.4)),
	]
	return m


static func _barracks_yard() -> Dictionary:
	var m := _base("騎士堡 · 演武場", Color(0.1, 0.1, 0.12), 2400, 1340, Vector2(328, 375), "barracks_yard")
	var blade_lab := "空武器架" if _flag("item.broken_blade") or _flag("side.ding_debt_done") else "武器架（斷劍）"
	m["entities"] = [
		_e("back_from_barracks", 300, 292, 56, 56, "回廣場", Color(0.4, 0.4, 0.45)),
		_e("training_ring", 1190, 750, 100, 80, "圓形演武台", Color(0.45, 0.4, 0.35), true),
		_e("weapon_rack", 592, 587, 48, 56, blade_lab, Color(0.5, 0.45, 0.4), true),
		_e("target_dummy", 836, 989, 40, 56, "木靶", Color(0.45, 0.35, 0.28)),
		_e("banner_stand", 644, 472, 40, 64, "團旗架", Color(0.55, 0.4, 0.3), true),
		_e("officer_desk", 1500, 595, 56, 48, "隊長桌", Color(0.4, 0.35, 0.3), true),
		_e("sand_pit", 1584, 997, 80, 48, "沙坑", Color(0.5, 0.45, 0.35)),
		_e("knight_orphan", 1504, 1061, 48, 64, "遺孤少年", Color(0.5, 0.48, 0.55)),
		_e("message_stone", 980, 880, 48, 52, "留言石", Color(0.5, 0.55, 0.72), true),
	]
	return m


static func _wild() -> Dictionary:
	var m := _base("城外荒野 · 焦土平原", Color(0.08, 0.12, 0.08), 3200, 1800, Vector2(320, 655), "wild")
	var ents: Array = [
		_e("back_town", 224, 602, 56, 56, "回城", Color(0.35, 0.4, 0.35)),
		_e("burnt_field", 320, 937, 64, 48, "焦麥田邊", Color(0.45, 0.38, 0.2)),
		_e("camp", 576, 1073, 64, 52, "焦麥田", Color(0.45, 0.4, 0.2), true),
		_e("scarecrow", 768, 781, 40, 56, "燒焦稻草人", Color(0.4, 0.35, 0.25)),
		_e("wild_shrine", 640, 533, 44, 52, "路邊小祠", Color(0.45, 0.4, 0.35)),
		_e("supply_crate", 448, 1385, 48, 40, "補給箱", Color(0.5, 0.4, 0.3)),
		_e("tower", 1536, 1168, 56, 72, "廢棄哨塔", Color(0.4, 0.38, 0.35), true),
		_e("to_wild_ravine", 960, 1479, 64, 56, "深裂谷", Color(0.3, 0.28, 0.25)),
		_e("rubble", 1760, 890, 52, 40, "石牆碎塊", Color(0.4, 0.38, 0.36)),
		_e("trail_mark", 1600, 530, 44, 40, "爪印土", Color(0.35, 0.4, 0.3)),
		_e("ravine", 1920, 1475, 100, 40, "乾裂溝", Color(0.3, 0.28, 0.25), true),
		_e("hill_view", 2304, 397, 56, 48, "遠眺丘", Color(0.35, 0.4, 0.3)),
	]
	if _flag("boss.leo_cleared"):
		ents.append(_e("path_mist", 2112, 1571, 72, 64, "霧道（東南方）", Color(0.5, 0.55, 0.7)))
		ents.append(_e("path_crossroads", 2880, 1526, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)))
		ents.append(_e("to_leo_court", 2560, 849, 64, 56, "內殿前院", Color(0.5, 0.4, 0.3)))
		ents.append(_e("leo_gate", 2784, 945, 72, 80, "內殿（已通）", Color(0.4, 0.35, 0.25), true))
	else:
		ents.append(_e("to_leo_court", 2560, 849, 64, 56, "內殿前院", Color(0.55, 0.4, 0.25)))
		ents.append(_e("leo_gate", 2784, 947, 80, 88, "內殿·雷歐", Color(0.65, 0.45, 0.2), true))
	m["entities"] = ents
	return m


static func _wild_ravine() -> Dictionary:
	var m := _base("荒野 · 深裂谷", Color(0.07, 0.09, 0.07), 2400, 1350, Vector2(288, 1215), "wild_ravine")
	m["entities"] = [
		_e("back_wild", 216, 1148, 56, 56, "回平原", Color(0.35, 0.4, 0.3)),
		_e("cliff_edge", 720, 837, 80, 40, "崖緣", Color(0.35, 0.32, 0.28), true),
		_e("rope_bridge", 1248, 770, 100, 40, "繩橋", Color(0.45, 0.38, 0.3), true),
		_e("bone_pile", 480, 1242, 48, 40, "獸骨", Color(0.5, 0.48, 0.45)),
		_e("echo_canyon", 2040, 608, 56, 48, "回音峽", Color(0.35, 0.4, 0.38)),
		_e("black_vein", 432, 783, 56, 40, "黑焰脈紋", Color(0.3, 0.2, 0.35)),
	]
	return m


static func _wild_leo_court() -> Dictionary:
	var m := _base("荒野 · 內殿前院", Color(0.1, 0.09, 0.08), 2400, 1350, Vector2(312, 1242), "wild_leo_court")
	m["entities"] = [
		_e("back_wild", 312, 1175, 56, 56, "回焦土", Color(0.35, 0.4, 0.3)),
		_e("lion_statue", 576, 864, 64, 80, "石獅像", Color(0.55, 0.45, 0.3), true),
		_e("courtyard", 1200, 1080, 100, 72, "石板院", Color(0.45, 0.4, 0.35), true),
		_e("banner_torn", 864, 999, 40, 56, "撕破旗", Color(0.5, 0.35, 0.25)),
		_e("leo_gate", 1248, 594, 80, 88, "內殿·雷歐", Color(0.65, 0.45, 0.2), true),
		_e("honor_plaque", 1584, 945, 48, 48, "榮譽碑", Color(0.5, 0.48, 0.4), true),
	]
	return m


# ═══════════════════════════════════════════
#  岔路與秘境
# ═══════════════════════════════════════════

static func _crossroads() -> Dictionary:
	var m := _base("六域岔路 · 翠嶺之心道", Color(0.1, 0.12, 0.1), 3000, 1674, Vector2(1350, 1081), "road")
	var ents: Array = [
		_e("sign_board", 1410, 625, 64, 56, "六域路標", Color(0.45, 0.4, 0.3), true),
		_e("camp_fire", 1140, 938, 48, 48, "旅人營火", Color(0.9, 0.4, 0.15), true),
		_e("merchant", 1230, 990, 48, 64, "行商", Color(0.6, 0.5, 0.4)),
		_e("path_knight", 180, 651, 72, 64, "西·騎士堡", Color(0.5, 0.45, 0.4)),
		_e("path_mist_c", 2100, 1510, 72, 64, "南·霧隱", Color(0.5, 0.55, 0.7)),
		_e("path_dojo_c", 1740, 83, 72, 64, "北·道場", Color(0.4, 0.55, 0.35)),
		_e("path_forest_c", 2400, 85, 72, 64, "東北·森林", Color(0.35, 0.55, 0.4)),
		_e("path_coast_c", 2400, 537, 72, 64, "東南·海岸", Color(0.4, 0.55, 0.65)),
		_e("path_tower_c", 2700, 198, 72, 64, "東·法師之塔", Color(0.45, 0.35, 0.55)),
		_e("to_cross_north", 1620, 91, 64, 56, "北山道", Color(0.4, 0.5, 0.4)),
		_e("to_cross_east", 2820, 421, 64, 56, "東塔荒原道", Color(0.4, 0.35, 0.45)),
		_e("to_caravan", 900, 760, 64, 56, "行商驛站", Color(0.55, 0.45, 0.35)),
		_e("to_starfall", 600, 309, 64, 56, "星落平原", Color(0.45, 0.5, 0.7)),
		_e("to_hunt", 1800, 987, 64, 56, "野外獵場", Color(0.65, 0.35, 0.4)),
		_e("ruin_pillar", 1560, 401, 40, 64, "古柱", Color(0.4, 0.38, 0.36), true),
		_e("save_cross", 1260, 1210, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("world_map_stone", 1650, 803, 56, 48, "世界輿圖石", Color(0.4, 0.5, 0.55)),
	]
	## 雷歐後、未完結前：岔路擋道的黑焰浪人
	if _flag("boss.leo_cleared") and not _flag("side.ronin_done"):
		ents.append(_e("ronin", 1500, 945, 52, 68, "黑焰浪人", Color(0.35, 0.2, 0.35)))
	elif _flag("side.ronin_spared"):
		ents.append(_e("ronin", 1500, 944, 48, 64, "浪人（收刃）", Color(0.4, 0.35, 0.4)))
	m["entities"] = ents
	return m


static func _cross_north() -> Dictionary:
	var m := _base("岔路 · 北山道", Color(0.09, 0.12, 0.1), 2400, 1350, Vector2(840, 1242), "cross_north")
	m["entities"] = [
		_e("back_cross", 768, 1188, 56, 56, "回岔路", Color(0.45, 0.5, 0.4)),
		_e("switchback", 1080, 891, 64, 48, "之字坡", Color(0.4, 0.42, 0.38)),
		_e("pine_row", 240, 1013, 80, 56, "松林", Color(0.3, 0.45, 0.35), true),
		_e("wayshrine", 1680, 918, 48, 56, "山神小祠", Color(0.45, 0.42, 0.4), true),
		_e("path_dojo_c", 2160, 864, 72, 64, "通往道場", Color(0.4, 0.55, 0.35)),
		_e("cloud_view", 1200, 540, 56, 48, "雲海眺望", Color(0.5, 0.55, 0.6)),
	]
	return m


static func _cross_east() -> Dictionary:
	var m := _base("岔路 · 東塔荒原道", Color(0.1, 0.09, 0.14), 2600, 1462, Vector2(260, 760), "cross_east")
	m["entities"] = [
		_e("back_cross", 130, 760, 56, 56, "回岔路", Color(0.45, 0.5, 0.4)),
		_e("dead_trees", 468, 994, 72, 56, "枯樹陣", Color(0.35, 0.3, 0.35), true),
		_e("ash_wind", 1248, 1170, 56, 40, "灰風帶", Color(0.4, 0.35, 0.4)),
		_e("to_blackflame_scar", 1248, 146, 64, 56, "黑焰疤地", Color(0.35, 0.2, 0.4)),
		_e("path_tower_c", 2392, 760, 72, 64, "塔下方向", Color(0.45, 0.35, 0.55)),
		_e("watch_rock", 1716, 673, 48, 48, "眺望岩", Color(0.4, 0.38, 0.42)),
	]
	return m


static func _caravan_camp() -> Dictionary:
	var m := _base("行商驛站 · 星途旅人落腳處", Color(0.1, 0.11, 0.12), 2400, 1340, Vector2(712, 1125), "caravan_camp")
	var letter_lab := "行商頭領" if not _flag("item.true_letter") else "行商（待交信）"
	m["entities"] = [
		_e("back_cross", 684, 1096, 56, 56, "回岔路", Color(0.45, 0.5, 0.4)),
		_e("wagon_a", 1204, 560, 72, 56, "篷車", Color(0.5, 0.4, 0.3), true),
		_e("wagon_b", 1780, 614, 72, 56, "篷車", Color(0.48, 0.38, 0.28), true),
		_e("merchant", 1360, 686, 48, 64, letter_lab, Color(0.6, 0.5, 0.4)),
		_e("amber", 1264, 847, 48, 64, "琥珀·商人", Color(0.75, 0.55, 0.3)),
		_e("camp_fire", 1528, 809, 48, 48, "營火", Color(0.9, 0.4, 0.15), true),
		_e("goods_pile", 1740, 943, 56, 48, "貨堆", Color(0.45, 0.4, 0.35)),
		_e("map_table", 1120, 844, 48, 40, "地圖桌", Color(0.5, 0.45, 0.35)),
		_e("guard_dog", 1076, 687, 40, 36, "守車犬", Color(0.4, 0.35, 0.3)),
	]
	return m


static func _starfall_plain() -> Dictionary:
	var m := _base("星落平原 · 十四星夜空", Color(0.05, 0.06, 0.12), 2800, 1563, Vector2(179, 859), "starfall_plain")
	m["entities"] = [
		_e("back_cross", 124, 773, 56, 56, "回岔路", Color(0.45, 0.5, 0.4)),
		_e("meteor_stone", 486, 749, 56, 48, "隕星石", Color(0.5, 0.55, 0.75), true),
		_e("constellation", 1338, 707, 64, 48, "星圖刻地", Color(0.45, 0.5, 0.7)),
		_e("star_reader_camp", 1886, 668, 56, 56, "星讀帳篷", Color(0.4, 0.4, 0.55), true),
		_e("night_bloom", 1094, 1253, 40, 40, "夜開花", Color(0.5, 0.4, 0.6)),
		_e("wish_pool", 1551, 1087, 64, 48, "許願淺池" + ("（已許）" if _flag("side.star_wish_done") else ""), Color(0.35, 0.4, 0.55), true),
		_e("to_road_ruins", 2678, 879, 64, 56, "接古驛", Color(0.4, 0.38, 0.35)),
	]
	return m


static func _hunting_grounds() -> Dictionary:
	var m := _base("野外獵場 · 黑焰溢地", Color(0.09, 0.06, 0.08), 3000, 1674, Vector2(340, 950), "hunting_grounds")
	m["entities"] = [
		_e("hunt_board", 904, 518, 72, 64, "狩獵告示", Color(0.65, 0.4, 0.35), true),
		_e("hunt_start", 1388, 761, 64, 56, "開始狩獵", Color(0.75, 0.35, 0.4)),
		_e("hunt_recycler", 1752, 619, 56, 64, "溢物回收", Color(0.55, 0.5, 0.4)),
		_e("camp_ash", 612, 1178, 56, 40, "獵手餘燼", Color(0.4, 0.3, 0.25)),
		_e("bone_pile", 1216, 1044, 48, 40, "獸骨堆", Color(0.5, 0.48, 0.45)),
		_e("scar_vein", 1992, 1078, 56, 40, "溢脈", Color(0.35, 0.2, 0.35)),
		_e("save_hunt", 376, 1405, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("back_cross", 252, 861, 56, 56, "回岔路", Color(0.45, 0.5, 0.4)),
		_e("exit_world", 2652, 861, 56, 56, "世界輿圖", Color(0.4, 0.5, 0.55)),
		_e("path_knight", 1808, 1464, 64, 56, "往騎士堡", Color(0.5, 0.45, 0.4)),
	]
	return m


static func _blackflame_scar() -> Dictionary:
	var m := _base("黑焰疤地 · 被吞噬的土地", Color(0.08, 0.05, 0.1), 2600, 1451, Vector2(196, 1212), "blackflame_scar")
	m["entities"] = [
		_e("back_cross", 168, 1185, 56, 56, "退回荒原道", Color(0.4, 0.35, 0.45)),
		_e("char_soil", 520, 1106, 80, 48, "焦裂地", Color(0.25, 0.15, 0.2), true),
		_e("flame_vent", 900, 1069, 48, 56, "焰口", Color(0.5, 0.2, 0.45), true),
		_e("obsidian", 1160, 1201, 48, 40, "黑曜碎", Color(0.2, 0.18, 0.25)),
		_e("lost_banner", 1424, 837, 40, 56, "半融旗", Color(0.4, 0.25, 0.3)),
		_e("whisper_stone", 1888, 758, 48, 48, "低語石", Color(0.35, 0.25, 0.4), true),
		_e("scar_boss", 2184, 1095, 80, 88, "黑焰疤主", Color(0.65, 0.25, 0.45)),
		_e("path_tower_c", 2448, 1177, 72, 64, "疤地盡頭·塔", Color(0.45, 0.35, 0.55)),
	]
	return m


# ═══════════════════════════════════════════
#  霧隱
# ═══════════════════════════════════════════

static func _mist() -> Dictionary:
	var m := _base("霧隱村 · 外圍", Color(0.1, 0.11, 0.16), 3000, 1674, Vector2(220, 850), "mist_village")
	var ents: Array = [
		_e("fog_hide", 436, 953, 48, 64, "霧隱", Color(0.5, 0.55, 0.7)),
		_e("lantern", 862, 810, 36, 40, "霧燈", Color(0.55, 0.55, 0.7)),
		_e("well_fog", 1218, 806, 44, 44, "霧井", Color(0.4, 0.45, 0.55), true),
		_e("inn", 788, 1363, 64, 56, "客棧（營火）", Color(0.55, 0.4, 0.3)),
		_e("laundry", 556, 1379, 48, 40, "曬衣繩", Color(0.55, 0.5, 0.6)),
		_e("cat_shadow", 1100, 1383, 40, 36, "影貓", Color(0.35, 0.35, 0.4)),
		_e("train", 1516, 1137, 48, 48, "霧廊訓練", Color(0.4, 0.45, 0.55)),
		_e("shrine", 1816, 1095, 48, 56, "霧祠", Color(0.45, 0.48, 0.6), true),
		_e("to_mist_shrine", 2052, 1170, 56, 48, "霧祠深處", Color(0.45, 0.5, 0.65)),
		_e("alley_gate", 1568, 1363, 64, 56, "深巷入口", Color(0.4, 0.42, 0.5)),
		_e("to_mist_cliff", 1988, 1363, 64, 56, "霧崖", Color(0.45, 0.5, 0.6)),
		_e("to_mist_mirror", 2348, 1363, 64, 56, "鏡廊", Color(0.5, 0.55, 0.7)),
		_e("fog_gate", 2640, 1298, 80, 88, "幻廊·白霧", Color(0.65, 0.7, 0.85)),
		_e("save_c2", 256, 1170, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("back_knight", 192, 769, 56, 48, "回騎士堡", Color(0.4, 0.4, 0.45)),
		_e("exit_cross_m", 2704, 1556, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)),
		_e("message_stone", 980, 1360, 48, 52, "留言石", Color(0.5, 0.55, 0.75), true),
	]
	if _flag("boss.white_fog_cleared"):
		ents.append(_e("path_dojo", 2824, 1422, 72, 64, "山道·道場", Color(0.4, 0.55, 0.35)))
	m["entities"] = ents
	return m


static func _mist_deep() -> Dictionary:
	var m := _base("霧隱 · 深巷與影廊前", Color(0.08, 0.09, 0.14), 2200, 1228, Vector2(348, 841), "mist_village")
	m["entities"] = [
		_e("back_mist", 320, 761, 56, 56, "回霧隱村", Color(0.45, 0.5, 0.6)),
		_e("mirror", 676, 581, 48, 64, "霧鏡", Color(0.5, 0.55, 0.65), true),
		_e("mask_shop", 672, 1006, 56, 56, "面具攤", Color(0.45, 0.4, 0.5), true),
		_e("echo_well", 1248, 842, 48, 48, "回聲井", Color(0.4, 0.45, 0.55), true),
		_e("to_mist_mirror", 1332, 1014, 56, 48, "鏡廊入口", Color(0.5, 0.55, 0.7)),
		_e("fog_gate_deep", 1896, 982, 72, 80, "幻廊側門", Color(0.65, 0.7, 0.85)),
	]
	return m


static func _mist_cliff() -> Dictionary:
	var m := _base("霧隱 · 霧崖觀台", Color(0.09, 0.1, 0.15), 2200, 1238, Vector2(1210, 1176), "mist_cliff")
	m["entities"] = [
		_e("back_from_mist_sub", 1144, 1114, 56, 56, "回霧隱村", Color(0.45, 0.5, 0.6)),
		_e("cliff_rail", 1452, 891, 100, 32, "崖欄", Color(0.4, 0.42, 0.5), true),
		_e("fog_sea", 1276, 1015, 80, 48, "霧海", Color(0.5, 0.55, 0.65)),
		_e("bell_tower", 1716, 817, 48, 72, "霧鐘樓", Color(0.45, 0.45, 0.55), true),
		_e("kite_string", 1892, 990, 40, 40, "斷線風箏", Color(0.55, 0.5, 0.45)),
		_e("overlook", 1540, 1114, 56, 48, "遠眺六域", Color(0.45, 0.5, 0.6)),
	]
	return m


static func _mist_shrine() -> Dictionary:
	var m := _base("霧隱 · 霧祠內殿", Color(0.08, 0.09, 0.14), 2000, 1116, Vector2(640, 1107), "mist_shrine")
	var incense_lab := "香爐（已燃）" if _flag("side.fog_incense_done") else "香爐"
	m["entities"] = [
		_e("back_from_mist_sub", 612, 1028, 56, 56, "出祠", Color(0.45, 0.5, 0.6)),
		_e("fox_statue", 1272, 440, 56, 64, "白狐像", Color(0.7, 0.72, 0.8), true),
		_e("incense", 1120, 620, 40, 40, incense_lab, Color(0.5, 0.45, 0.4)),
		_e("prayer_strip", 896, 671, 48, 56, "願條", Color(0.55, 0.5, 0.6)),
		_e("secret_panel", 1496, 568, 48, 48, "暗板", Color(0.4, 0.4, 0.5)),
	]
	return m


static func _mist_mirror() -> Dictionary:
	var m := _base("霧隱 · 鏡廊迷宮", Color(0.07, 0.08, 0.13), 2400, 1350, Vector2(232, 1295), "mist_mirror")
	m["entities"] = [
		_e("back_from_mist_sub", 204, 1212, 56, 56, "出廊", Color(0.45, 0.5, 0.6)),
		_e("mirror_a", 352, 988, 48, 64, "鏡·一", Color(0.55, 0.6, 0.7), true),
		_e("mirror_b", 832, 1150, 48, 64, "鏡·二", Color(0.5, 0.55, 0.65), true),
		_e("mirror_c", 1504, 1150, 48, 64, "鏡·三", Color(0.55, 0.58, 0.7), true),
		_e("false_exit", 2124, 1058, 56, 48, "假出口", Color(0.4, 0.42, 0.5)),
		_e("true_path", 1164, 869, 56, 48, "真影道", Color(0.5, 0.55, 0.75)),
		_e("mirror_boss", 1008, 748, 80, 88, "鏡廊殘影", Color(0.7, 0.75, 0.9)),
		_e("fog_gate_deep", 1252, 662, 72, 80, "幻廊核心", Color(0.65, 0.7, 0.85)),
	]
	return m


# ═══════════════════════════════════════════
#  道場
# ═══════════════════════════════════════════

static func _dojo() -> Dictionary:
	var m := _base("武鬥道場 · 山門院落", Color(0.12, 0.14, 0.1), 2800, 1563, Vector2(264, 1393), "dojo")
	var ents: Array = [
		_e("acha", 688, 641, 48, 64, "阿茶", Color(0.7, 0.55, 0.4)),
		_e("gate_bell", 1248, 172, 48, 64, "山門鐘", Color(0.55, 0.5, 0.35)),
		_e("training_dummy", 804, 837, 40, 56, "木人樁", Color(0.5, 0.4, 0.3)),
		_e("scroll_wall", 1416, 407, 48, 48, "拳譜牆", Color(0.45, 0.42, 0.35), true),
		_e("stone_garden", 964, 567, 56, 44, "石庭", Color(0.4, 0.45, 0.4)),
		_e("tea", 1752, 563, 48, 48, "茶席", Color(0.5, 0.4, 0.3)),
		_e("to_dojo_inner", 1744, 837, 64, 56, "內院", Color(0.4, 0.5, 0.35)),
		_e("to_dojo_bamboo", 1464, 1056, 64, 56, "竹林徑", Color(0.35, 0.5, 0.35)),
		_e("to_dojo_peak", 1856, 1243, 64, 56, "山巔道", Color(0.4, 0.48, 0.4)),
		_e("trial_hall", 2296, 1305, 80, 88, "試煉堂·阿波", Color(0.35, 0.5, 0.3)),
		_e("dorm", 848, 962, 64, 56, "僧寮", Color(0.4, 0.38, 0.32), true),
		_e("save_c3", 408, 1251, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("back_mist", 180, 1407, 56, 48, "回霧隱村", Color(0.45, 0.5, 0.6)),
		_e("exit_cross_d", 228, 1454, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)),
	]
	if _flag("boss.abo_cleared"):
		ents.append(_e("path_forest", 452, 1391, 72, 64, "林道·遊俠", Color(0.35, 0.55, 0.4)))
		ents.append(_e("path_tower", 2468, 1391, 72, 64, "向塔之路", Color(0.4, 0.3, 0.5)))
	m["entities"] = ents
	return m


static func _dojo_inner() -> Dictionary:
	var m := _base("道場 · 內院與靜室", Color(0.11, 0.13, 0.1), 2200, 1238, Vector2(700, 871), "dojo_inner")
	m["entities"] = [
		_e("back_dojo", 672, 780, 56, 56, "回山門", Color(0.4, 0.5, 0.35)),
		_e("zen_pond", 792, 513, 80, 48, "靜心池", Color(0.35, 0.45, 0.5), true),
		_e("scripture", 1160, 437, 48, 56, "經閣", Color(0.45, 0.4, 0.35), true),
		_e("meditation", 1464, 617, 56, 48, "打坐席", Color(0.4, 0.42, 0.35)),
		_e("master_room", 1812, 677, 64, 56, "掌門靜室", Color(0.42, 0.38, 0.32), true),
	]
	return m


static func _dojo_bamboo() -> Dictionary:
	var m := _base("道場 · 竹林徑", Color(0.08, 0.14, 0.09), 2400, 1350, Vector2(472, 1052), "dojo_bamboo")
	m["entities"] = [
		_e("back_dojo", 444, 969, 56, 56, "回山門", Color(0.4, 0.5, 0.35)),
		_e("bamboo_wall", 672, 718, 80, 64, "竹牆", Color(0.3, 0.5, 0.35), true),
		_e("stream_stone", 1120, 823, 48, 40, "溪石", Color(0.4, 0.45, 0.4)),
		_e("hidden_spar", 1692, 842, 56, 48, "隱切磋場", Color(0.4, 0.48, 0.35)),
		_e("leaf_pile", 1936, 1043, 48, 36, "落葉堆", Color(0.4, 0.45, 0.3)),
		_e("to_dojo_peak", 1208, 240, 64, 56, "上山巔", Color(0.4, 0.48, 0.4)),
	]
	return m


static func _dojo_peak() -> Dictionary:
	var m := _base("道場 · 山巔試煉台", Color(0.12, 0.14, 0.16), 2200, 1228, Vector2(484, 1007), "dojo_peak")
	m["entities"] = [
		_e("back_dojo", 396, 958, 56, 56, "下山", Color(0.4, 0.5, 0.35)),
		_e("peak_platform", 990, 675, 100, 72, "試煉台", Color(0.45, 0.42, 0.38), true),
		_e("wind_flag", 1100, 467, 40, 56, "風旗", Color(0.5, 0.45, 0.35)),
		_e("trial_hall", 1408, 737, 80, 88, "巔上·阿波影", Color(0.35, 0.5, 0.3)),
		_e("sunrise_view", 1936, 344, 56, 48, "日出眺", Color(0.6, 0.5, 0.4)),
	]
	return m


# ═══════════════════════════════════════════
#  森林
# ═══════════════════════════════════════════

static func _forest() -> Dictionary:
	## ¾ 俯視樹海：路從下緣接到上緣，小屋在右。座標是腳底對齊新路。
	var m := _base("遊俠森林 · 樹海邊緣", Color(0.06, 0.12, 0.08), 3200, 1786, Vector2(1576, 1652), "forest")
	var ents: Array = [
		_e("wind_ear", 1232, 945, 48, 64, "風耳", Color(0.45, 0.7, 0.5)),
		_e("treehouse", 2208, 873, 64, 64, "樹屋聚落", Color(0.4, 0.55, 0.35)),
		_e("kite_stuck", 660, 933, 40, 40, "卡住的風箏", Color(0.7, 0.5, 0.4)),
		_e("arrow_path", 676, 957, 56, 48, "箭道", Color(0.35, 0.5, 0.4)),
		_e("watch_tower", 2512, 998, 48, 64, "觀風塔", Color(0.45, 0.5, 0.4)),
		_e("herb_slope", 528, 1014, 48, 48, "藥草坡", Color(0.4, 0.6, 0.35)),
		_e("stream", 2496, 1149, 48, 36, "溪流", Color(0.35, 0.5, 0.55)),
		_e("owl_post", 1364, 1139, 40, 48, "貓頭鷹樁", Color(0.4, 0.35, 0.3)),
		_e("deep_gate", 1608, 595, 64, 56, "深林入口", Color(0.3, 0.45, 0.3)),
		_e("to_forest_canopy", 2560, 917, 64, 56, "樹冠層", Color(0.35, 0.55, 0.4)),
		_e("to_forest_lake", 2624, 1417, 64, 56, "靜湖", Color(0.35, 0.5, 0.55)),
		_e("to_forest_ruins", 2240, 1310, 64, 56, "古遊俠遺址", Color(0.4, 0.45, 0.35)),
		_e("falcon_nest", 2496, 1512, 80, 88, "疾影巢", Color(0.4, 0.75, 0.55)),
		_e("save_c4", 1296, 1461, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("back_dojo", 1612, 211, 56, 48, "回道場", Color(0.4, 0.45, 0.35)),
		_e("exit_cross_f", 1540, 1695, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)),
	]
	if _flag("boss.shadowwind_cleared"):
		ents.append(_e("path_coast", 1860, 1659, 72, 64, "海岸道", Color(0.4, 0.55, 0.65)))
	m["entities"] = ents
	return m


static func _forest_deep() -> Dictionary:
	var m := _base("深林 · 風道迷宮", Color(0.05, 0.1, 0.06), 2600, 1451, Vector2(1340, 399), "forest")
	m["entities"] = [
		_e("back_forest", 1312, 198, 56, 56, "回樹海邊緣", Color(0.35, 0.5, 0.4)),
		_e("wind_tunnel", 580, 758, 64, 48, "風道", Color(0.4, 0.6, 0.5)),
		_e("nest_mark", 1316, 734, 48, 48, "羽痕石", Color(0.45, 0.5, 0.4)),
		_e("hidden_cache", 432, 795, 48, 40, "獵人藏匿處", Color(0.4, 0.35, 0.3)),
		_e("to_forest_canopy", 2084, 757, 56, 48, "爬上樹冠", Color(0.35, 0.55, 0.4)),
		_e("falcon_nest_deep", 1996, 1238, 72, 80, "疾影巢（近）", Color(0.4, 0.75, 0.55)),
	]
	return m


static func _forest_canopy() -> Dictionary:
	var m := _base("森林 · 樹冠層", Color(0.08, 0.14, 0.1), 2400, 1350, Vector2(232, 1160), "forest_canopy")
	m["entities"] = [
		_e("back_from_forest_sub", 204, 1104, 56, 56, "下樹", Color(0.35, 0.5, 0.4)),
		_e("bridge_rope", 518, 310, 100, 40, "藤橋", Color(0.4, 0.45, 0.3), true),
		_e("nest_platform", 1016, 591, 64, 56, "巢台", Color(0.45, 0.5, 0.35), true),
		_e("wind_chime", 1364, 580, 40, 40, "風鈴", Color(0.5, 0.55, 0.45)),
		_e("eagle_view", 1884, 302, 56, 48, "鷹眼眺望", Color(0.4, 0.55, 0.5)),
		_e("to_forest_ruins", 2076, 1112, 56, 48, "藤蔓下·遺址", Color(0.4, 0.45, 0.35)),
	]
	return m


static func _forest_ruins() -> Dictionary:
	var m := _base("森林 · 古遊俠遺址", Color(0.07, 0.1, 0.08), 2400, 1350, Vector2(256, 674), "forest_ruins")
	m["entities"] = [
		_e("back_from_forest_sub", 228, 591, 56, 56, "回樹海", Color(0.35, 0.5, 0.4)),
		_e("arch_ruin", 724, 759, 72, 64, "石拱廢墟", Color(0.45, 0.42, 0.38), true),
		_e("bow_relief", 1120, 699, 48, 56, "弓神浮雕", Color(0.4, 0.45, 0.4), true),
		_e("arrow_well", 880, 1004, 48, 48, "箭井", Color(0.35, 0.4, 0.38), true),
		_e("moss_script", 1596, 823, 56, 40, "苔文", Color(0.35, 0.5, 0.35)),
		_e("chest_root", 1792, 1039, 48, 40, "根纏箱", Color(0.4, 0.35, 0.28)),
	]
	return m


static func _forest_lake() -> Dictionary:
	var m := _base("森林 · 靜湖", Color(0.06, 0.11, 0.12), 2400, 1340, Vector2(280, 1259), "forest_lake")
	m["entities"] = [
		_e("back_from_forest_sub", 252, 1176, 56, 56, "回樹海", Color(0.35, 0.5, 0.4)),
		_e("lake_shore", 940, 1050, 120, 48, "湖岸", Color(0.35, 0.5, 0.55), true),
		_e("reed", 592, 871, 48, 40, "蘆葦", Color(0.4, 0.5, 0.35)),
		_e("dock_log", 1208, 928, 64, 36, "原木碼頭", Color(0.45, 0.4, 0.3)),
		_e("reflection", 1692, 1077, 56, 48, "倒影奇", Color(0.4, 0.5, 0.55)),
		_e("heron", 2084, 1104, 40, 48, "蒼鷺", Color(0.5, 0.55, 0.5)),
	]
	return m


# ═══════════════════════════════════════════
#  海岸
# ═══════════════════════════════════════════

static func _coast() -> Dictionary:
	var m := _base("維京海岸 · 碼頭與岸道", Color(0.12, 0.16, 0.2), 3200, 1786, Vector2(232, 1616), "coast")
	var ents: Array = [
		_e("tide_roar", 624, 1123, 48, 64, "潮吼", Color(0.65, 0.45, 0.35)),
		_e("dock", 1064, 582, 64, 52, "碼頭鎮", Color(0.4, 0.45, 0.5)),
		_e("to_coast_harbor", 1416, 953, 64, 56, "深港", Color(0.4, 0.48, 0.55)),
		_e("boat_wreck", 1480, 1108, 64, 44, "破船骸", Color(0.4, 0.35, 0.3)),
		_e("forge_c5", 720, 810, 48, 56, "岸邊鍛爐", Color(0.7, 0.4, 0.25)),
		_e("net_rack", 880, 719, 48, 40, "漁網架", Color(0.45, 0.4, 0.35)),
		_e("cliff_path", 1068, 782, 56, 48, "峭壁道", Color(0.45, 0.42, 0.4)),
		_e("runestone", 1360, 524, 48, 56, "符文石", Color(0.5, 0.48, 0.55), true),
		_e("to_coast_cave", 1672, 399, 64, 56, "潮汐洞", Color(0.35, 0.4, 0.45)),
		_e("to_coast_wreck", 1992, 310, 64, 56, "沉船灣", Color(0.4, 0.38, 0.35)),
		_e("cliff_gate", 2280, 238, 64, 56, "崖上祭壇道", Color(0.5, 0.4, 0.35)),
		_e("boar_cliff", 2560, 171, 80, 88, "石拳崖", Color(0.6, 0.4, 0.3)),
		_e("save_c5", 464, 1282, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("back_forest", 300, 1461, 56, 48, "回森林", Color(0.35, 0.5, 0.4)),
		_e("exit_cross_c", 132, 1623, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)),
	]
	if _flag("boss.stonefist_cleared"):
		ents.append(_e("path_tower_c5", 2756, 248, 72, 64, "向塔之路", Color(0.45, 0.35, 0.55)))
	m["entities"] = ents
	return m


static func _coast_cliff() -> Dictionary:
	var m := _base("崖上 · 祭壇與浪聲", Color(0.1, 0.13, 0.16), 2200, 1228, Vector2(260, 1038), "coast")
	m["entities"] = [
		_e("back_coast", 166, 1056, 56, 56, "回碼頭", Color(0.4, 0.5, 0.55)),
		_e("altar", 514, 552, 64, 56, "浪祭壇", Color(0.5, 0.45, 0.4), true),
		_e("beacon", 702, 421, 40, 64, "烽火台", Color(0.55, 0.4, 0.3), true),
		_e("boar_cliff_near", 1544, 160, 72, 80, "石拳崖近路", Color(0.6, 0.4, 0.3)),
		_e("gull_nest", 1076, 326, 40, 36, "海鷗巢", Color(0.5, 0.48, 0.45)),
	]
	return m


static func _coast_harbor() -> Dictionary:
	var m := _base("海岸 · 深港碼頭", Color(0.1, 0.14, 0.18), 2600, 1451, Vector2(2276, 370), "coast_harbor")
	m["entities"] = [
		_e("back_from_coast_sub", 2248, 227, 56, 56, "回岸道", Color(0.4, 0.5, 0.55)),
		_e("longship", 458, 779, 100, 56, "長船", Color(0.4, 0.35, 0.3), true),
		_e("crane", 1628, 617, 48, 72, "吊桿", Color(0.45, 0.42, 0.4), true),
		_e("warehouse", 2084, 895, 72, 56, "貨倉", Color(0.4, 0.38, 0.35), true),
		_e("tide_gauge", 1528, 1077, 40, 48, "潮位尺", Color(0.4, 0.45, 0.5)),
		_e("captain_post", 1832, 467, 56, 48, "船長柱", Color(0.5, 0.4, 0.35)),
	]
	return m


static func _coast_cave() -> Dictionary:
	var m := _base("海岸 · 潮汐洞", Color(0.08, 0.1, 0.14), 2200, 1238, Vector2(590, 699), "coast_cave")
	m["entities"] = [
		_e("back_from_coast_sub", 540, 618, 56, 56, "出洞", Color(0.4, 0.5, 0.55)),
		_e("tide_pool", 708, 688, 72, 48, "潮池", Color(0.3, 0.4, 0.5), true),
		_e("crystal", 1890, 800, 40, 48, "海晶", Color(0.4, 0.55, 0.65)),
		_e("pirate_mark", 1380, 560, 48, 40, "海盜標記", Color(0.45, 0.35, 0.3)),
		_e("air_hole", 944, 510, 40, 40, "氣孔光", Color(0.5, 0.55, 0.6)),
		_e("deep_water", 1372, 1047, 64, 48, "深水", Color(0.25, 0.3, 0.4), true),
	]
	return m


static func _coast_wreck() -> Dictionary:
	var m := _base("海岸 · 沉船灣", Color(0.1, 0.12, 0.14), 2400, 1339, Vector2(520, 272), "coast_wreck")
	m["entities"] = [
		_e("back_from_coast_sub", 336, 139, 56, 56, "回岸道", Color(0.4, 0.5, 0.55)),
		_e("hull", 844, 353, 120, 72, "船體殘骸", Color(0.4, 0.35, 0.3), true),
		_e("mast", 1016, 58, 40, 80, "斷桅", Color(0.42, 0.38, 0.32), true),
		_e("chest_half", 1228, 460, 48, 40, "半埋箱", Color(0.5, 0.4, 0.25)),
		_e("skull_rock", 1420, 281, 48, 48, "頭骨岩", Color(0.45, 0.42, 0.4)),
		_e("wreck_boss", 720, 461, 80, 88, "沉船船長影", Color(0.45, 0.55, 0.7)),
		_e("to_coast_cave", 852, 701, 56, 48, "洞口（內側）", Color(0.35, 0.4, 0.45)),
	]
	return m


# ═══════════════════════════════════════════
#  塔
# ═══════════════════════════════════════════

static func _tower_camp() -> Dictionary:
	var m := _base("法師之塔 · 塔下營地", Color(0.08, 0.07, 0.12), 2800, 1575, Vector2(488, 1088), "tower")
	var ents: Array = [
		_e("duanye", 800, 898, 48, 64, "斷頁", Color(0.55, 0.45, 0.65)),
		_e("refugee_fire", 740, 1260, 56, 48, "逃難營火", Color(0.9, 0.4, 0.15), true),
		_e("tent_a", 456, 1198, 64, 48, "帳棚", Color(0.4, 0.35, 0.4), true),
		_e("tent_b", 1128, 1386, 64, 48, "帳棚", Color(0.38, 0.35, 0.42), true),
		_e("scroll_pile", 1248, 796, 48, 40, "散落卷軸", Color(0.5, 0.45, 0.4)),
		_e("message_stone", 1022, 1064, 52, 56, "留言石", Color(0.5, 0.55, 0.75), true),
		_e("candle_altar", 1468, 965, 56, 60, "通關燭火", Color(0.95, 0.75, 0.35), true),
		_e("tower_gate", 784, 772, 80, 96, "塔門", Color(0.35, 0.25, 0.4), true),
		_e("to_tower_foyer", 960, 748, 64, 56, "進入塔門廳", Color(0.45, 0.35, 0.5)),
		_e("climb_tower", 1688, 804, 64, 64, "登上塔", Color(0.5, 0.35, 0.55)),
		_e("save_tower", 688, 1386, 48, 48, "存檔石", Color(0.4, 0.45, 0.5)),
		_e("exit_cross_t", 2356, 1402, 72, 64, "六域岔路", Color(0.45, 0.5, 0.4)),
		_e("path_back_wild", 460, 1008, 56, 48, "回荒野", Color(0.35, 0.4, 0.3)),
	]
	## 勸降成功：塔下再見
	if _flag("side.ronin_spared"):
		ents.append(_e("ronin", 1584, 1244, 48, 64, "浪人（守營）", Color(0.4, 0.35, 0.42)))
	m["entities"] = ents
	return m


static func _tower_foyer() -> Dictionary:
	var m := _base("法師之塔 · 門廳", Color(0.07, 0.06, 0.11), 2400, 1340, Vector2(280, 1259), "tower_foyer")
	m["entities"] = [
		_e("back_tower_camp", 252, 1176, 56, 56, "回營地", Color(0.4, 0.35, 0.5)),
		_e("pillar_a", 548, 831, 40, 80, "黑石柱", Color(0.3, 0.25, 0.35), true),
		_e("pillar_b", 596, 1045, 40, 80, "黑石柱", Color(0.3, 0.25, 0.35), true),
		_e("mural", 1152, 801, 80, 56, "封印壁畫", Color(0.4, 0.3, 0.45), true),
		_e("to_tower_stairs", 1112, 480, 64, 56, "螺旋階", Color(0.45, 0.35, 0.5)),
		_e("to_tower_memory", 1736, 989, 64, 56, "回憶層入口", Color(0.5, 0.4, 0.55)),
		_e("climb_tower", 2072, 900, 64, 64, "直接登頂路", Color(0.5, 0.35, 0.55)),
	]
	return m


static func _tower_stairs() -> Dictionary:
	var m := _base("法師之塔 · 螺旋階", Color(0.06, 0.05, 0.1), 2200, 1238, Vector2(568, 1095), "tower_stairs")
	m["entities"] = [
		_e("back_tower_camp", 540, 1014, 56, 56, "下塔", Color(0.4, 0.35, 0.5)),
		_e("step_mark", 456, 783, 48, 40, "腳印", Color(0.35, 0.3, 0.4)),
		_e("window_slit", 592, 552, 40, 48, "狹窗", Color(0.3, 0.35, 0.45)),
		_e("echo_step", 1072, 486, 48, 40, "回音階", Color(0.4, 0.35, 0.45)),
		_e("to_tower_memory", 1596, 577, 56, 48, "回憶層", Color(0.5, 0.4, 0.55)),
		_e("climb_tower", 1724, 833, 64, 64, "更高處", Color(0.5, 0.35, 0.55)),
	]
	return m


static func _tower_memory() -> Dictionary:
	var m := _base("法師之塔 · 回憶層", Color(0.08, 0.06, 0.12), 2400, 1350, Vector2(280, 1268), "tower_memory")
	m["entities"] = [
		_e("back_tower_camp", 252, 1185, 56, 56, "離開回憶", Color(0.4, 0.35, 0.5)),
		_e("memory_orb_a", 496, 1004, 48, 48, "記憶球·村", Color(0.55, 0.45, 0.4)),
		_e("memory_orb_b", 784, 1112, 48, 48, "記憶球·堡", Color(0.5, 0.45, 0.55)),
		_e("memory_orb_c", 1600, 1085, 48, 48, "記憶球·聖獸", Color(0.5, 0.55, 0.45)),
		_e("throne_shadow", 1156, 772, 72, 64, "王座影", Color(0.35, 0.25, 0.4), true),
		_e("climb_tower", 2024, 961, 64, 64, "面對終焉", Color(0.55, 0.35, 0.5)),
	]
	return m


static func _fallback(id: String) -> Dictionary:
	return _base(id, Color(0.1, 0.1, 0.12), 2000, 1000, Vector2(200, 400), id)


## 與 _build_raw 的 match 對齊。測底圖尺寸／walkmask 用這份，不要另外手抄 id。
static func ids() -> PackedStringArray:
	return PackedStringArray([
		"village", "village_outskirts", "village_mill", "village_cave", "village_grave",
		"road", "road_bridge", "road_inn", "road_ruins",
		"town", "town_forge", "town_soul", "town_gem", "town_tutor",
		"town_keep", "town_market", "town_sewers", "barracks_yard",
		"wild", "wild_ravine", "wild_leo_court",
		"crossroads", "cross_north", "cross_east",
		"caravan_camp", "starfall_plain", "blackflame_scar", "hunting_grounds",
		"mist_village", "mist_deep", "mist_cliff", "mist_shrine", "mist_mirror",
		"dojo", "dojo_inner", "dojo_bamboo", "dojo_peak",
		"forest", "forest_deep", "forest_canopy", "forest_ruins", "forest_lake",
		"coast", "coast_cliff", "coast_harbor", "coast_cave", "coast_wreck",
		"tower_camp", "tower_foyer", "tower_stairs", "tower_memory",
	])
