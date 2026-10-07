extends RefCounted
## 衣櫥玩具家族（任務書 §1、§2）
##
## 衣櫥分頁只用玩具家族：胡桃鉗兔、八音盒、錫兵、旋轉木馬。
## 主角永遠是兔子剪影（搪瓷黃銅板件、玻璃眼、胸口心形機芯、背上發條鑰匙）。
## 狐／獅／野豬三個毛皮種族從衣櫥與玩家看得到的地方拿掉；
## 舊存檔裡的種族 id 一律映射到家族，存檔照樣讀得進來。
##
## 規矩：本檔只放純資料與純函式，不碰 autoload，測試可以直接 preload。

## 主角本體美術（兔子剪影）
const HERO_ART_RACE := "rabbit"

## 衣櫥分頁順序就是這個陣列的順序
const FAMILIES: Array[Dictionary] = [
	{"id": "nutcracker_rabbit", "name_zh": "胡桃鉗兔", "archetype_zh": "近衛"},
	{"id": "music_box", "name_zh": "八音盒", "archetype_zh": "樂匣"},
	{"id": "tin_soldier", "name_zh": "錫兵", "archetype_zh": "儀隊"},
	{"id": "carousel", "name_zh": "旋轉木馬", "archetype_zh": "巡遊"},
]

const DEFAULT_FAMILY := "nutcracker_rabbit"

## 毛皮種族：衣櫥不可達、存檔載入時改回兔子本體
const FUR_RACE_IDS: Array[String] = ["fox", "lion", "boar"]

## 舊種族 id → 玩具家族（存檔相容用）。沒列到的 id 一律回 DEFAULT_FAMILY。
const LEGACY_RACE_TO_FAMILY: Dictionary = {
	"rabbit": "nutcracker_rabbit",
	"fox": "music_box",
	"lion": "tin_soldier",
	"boar": "tin_soldier",
	"macaque": "nutcracker_rabbit",
	"tiger": "tin_soldier",
	"bear": "tin_soldier",
	"crane": "music_box",
	"penguin": "carousel",
	"tortoise": "tin_soldier",
	"elephant": "tin_soldier",
	"frog": "music_box",
	"panda": "nutcracker_rabbit",
	"fawn": "carousel",
	"hound": "nutcracker_rabbit",
	"owl": "music_box",
	"cat": "nutcracker_rabbit",
	"pangolin": "tin_soldier",
	"otter": "nutcracker_rabbit",
	"raccoon": "nutcracker_rabbit",
	"hedgehog": "nutcracker_rabbit",
	"wolf": "tin_soldier",
	"seahorse": "carousel",
	"kangaroo": "nutcracker_rabbit",
	"squirrel": "nutcracker_rabbit",
	"salamander": "tin_soldier",
	"viper": "music_box",
	"falcon": "music_box",
	"ram": "music_box",
	"chameleon": "music_box",
	"sailfish": "carousel",
	"rhino": "tin_soldier",
	"bat": "music_box",
	"gorilla": "tin_soldier",
	"peacock": "music_box",
	"meerkat": "nutcracker_rabbit",
	"courser": "carousel",
	"beaver": "nutcracker_rabbit",
	"stoat": "nutcracker_rabbit",
	"seal": "carousel",
	"raven": "music_box",
	"kite": "music_box",
	"swan": "music_box",
	"bison": "tin_soldier",
	"gecko": "music_box",
	"badger": "nutcracker_rabbit",
	"capybara": "nutcracker_rabbit",
	"woodpecker": "music_box",
	"armadillo": "tin_soldier",
	"caterpillar": "music_box",
	"cuttlefish": "music_box",
	"crab": "tin_soldier",
	"camel": "carousel",
	"giraffe": "carousel",
	"hippo": "tin_soldier",
	"mole": "nutcracker_rabbit",
	"petaurista": "nutcracker_rabbit",
	"lynx": "nutcracker_rabbit",
	"scarab": "tin_soldier",
	"toucan": "music_box",
	"walrus": "tin_soldier",
	"takin": "tin_soldier",
	"lemur": "nutcracker_rabbit",
	"marmot": "nutcracker_rabbit",
	"firefly": "music_box",
	"manta": "carousel",
	"kingfisher": "music_box",
	"donkey": "carousel",
	"scorpion": "tin_soldier",
}

## 通用部件（不屬於本體原廠清單）分到哪個家族分頁。沒列到的通用部件歸 DEFAULT_FAMILY。
## 本體原廠部件（例如兔的胡桃鉗軍裝、三款塗裝）永遠留在本體所屬家族，避免舊存檔索引錯位。
const ITEM_FAMILY: Dictionary = {
	# 外裝
	"costume_viking_harness": "tin_soldier",
	"costume_viking_ironclad": "tin_soldier",
	"costume_royal_parade": "tin_soldier",
	"costume_astral_cape": "music_box",
	"costume_astral_observer": "music_box",
	"costume_dawn_monk_tunic": "carousel",
	# 塗裝
	"paint_nutcracker_red": "nutcracker_rabbit",
	"paint_midnight_navy": "tin_soldier",
	"paint_emerald_glaze": "music_box",
	"paint_brass_gold": "carousel",
	# 發條鑰匙
	"key_butterfly_t": "music_box",
	"key_swan_octave_dual_loop_brass": "music_box",
	"key_giraffe_three_ring_carillon_brass": "music_box",
	"key_petaurista_three_leaf_windchime_brass": "music_box",
	"key_woodpecker_high_frequency_percussion_key": "music_box",
	"key_lynx_twin_ring_chime_brass": "music_box",
	"key_royal_crown": "tin_soldier",
	"key_cross_pendulum": "tin_soldier",
	"key_heavy_cross_wheel": "tin_soldier",
	"key_wolf_heavy_pojun_cross": "tin_soldier",
	"key_bison_heavy_cross_t_bar_cast_iron": "tin_soldier",
	"key_gorilla_heavy_t_forged_key": "tin_soldier",
	"key_starlight_cog": "carousel",
	"key_winged_angel": "carousel",
	"key_twin_wing_concentric": "carousel",
	"key_tri_wing_zephyr": "carousel",
	"key_courser_baroque_trefoil_gold": "carousel",
	"key_peacock_filigree_sunburst_key": "carousel",
	# 武器
	"wpn_knight_lance": "tin_soldier",
	"wpn_anvil_greathammer": "tin_soldier",
	"weapon_hound_stellar_beacon_lance": "tin_soldier",
	"wpn_astral_staff": "music_box",
	"wpn_bagua_astrolabe": "music_box",
	"weapon_swan_octave_spiral_lance": "music_box",
	"weapon_courser_cavalry_saber": "carousel",
	"wpn_zephyr_wing_bow": "carousel",
	# 光學核心
	"core_astral_amethyst": "music_box",
	"core_pilot_visor": "tin_soldier",
	"core_amber_sun": "carousel",
	# 隨身奇玩
	"curio_floating_musicbox": "music_box",
	"curio_steam_exhaust": "tin_soldier",
}

## 任務書 §3：主角紙娃娃七層（列舉順序）。curio 在資料表裡的 slot_id 是 back_curio。
const PAPERDOLL_LAYERS: Array[String] = ["chassis", "head_unit", "optic_core", "costume", "curio", "weapon", "winding_key"]
const LAYER_SLOT_ALIASES: Dictionary = {"curio": "back_curio"}
## 主角兔 512 畫布的腳底基準線：最後一列不透明像素（素體三款塗裝 ±1 內；其他圖層不得低於它）
const HERO_BASELINE_Y_512 := 491


## 七層對應的資料表 slot_id（順序同 PAPERDOLL_LAYERS）
static func canonical_slot_ids() -> Array[String]:
	var out: Array[String] = []
	for l in PAPERDOLL_LAYERS:
		out.append(slot_id_for_layer(l))
	return out


static func family_ids() -> Array[String]:
	var out: Array[String] = []
	for f in FAMILIES:
		out.append(str(f.get("id", "")))
	return out


static func is_family(fid: String) -> bool:
	return family_ids().has(fid.strip_edges())


static func family_def(fid: String) -> Dictionary:
	for f in FAMILIES:
		if str(f.get("id", "")) == fid:
			return f
	return {}


static func family_name(fid: String) -> String:
	return str(family_def(fid).get("name_zh", ""))


static func is_fur_race(race_id: String) -> bool:
	return FUR_RACE_IDS.has(race_id.strip_edges().to_lower())


## 舊種族 id（或家族 id）→ 家族 id
static func family_of(race_or_family: String) -> String:
	var r := race_or_family.strip_edges().to_lower()
	if is_family(r):
		return r
	return str(LEGACY_RACE_TO_FAMILY.get(r, DEFAULT_FAMILY))


## 衣櫥／大廳／戰鬥要畫的本體：毛皮種族、空值、家族 id 一律回兔子本體
static func art_race_for(race_id: String) -> String:
	var r := race_id.strip_edges().to_lower()
	if r.is_empty() or is_fur_race(r) or is_family(r):
		return HERO_ART_RACE
	return r


## 資料表 slot_id（curio → back_curio）
static func slot_id_for_layer(layer: String) -> String:
	return str(LAYER_SLOT_ALIASES.get(layer, layer))


## 部件屬於哪個家族分頁。
##   native_ids：本體原廠清單（RACES_DATA 的 costumes／chassis，或資料表 race == 本體的部件）
##   回 "" 代表所有分頁都看得到（裸機、預設件）
##   順序：基本款 → 本體原廠件歸本體家族（兔子原廠三套都在胡桃鉗兔）→ ITEM_FAMILY 標記 → 其餘歸預設家族
static func family_of_item(item_id: String, art_race: String, native_ids: Array = [], base_ids: Array = []) -> String:
	var iid := item_id.strip_edges()
	if iid.is_empty() or iid in ["none", "bare", "empty"] or base_ids.has(iid):
		return ""
	if native_ids.has(iid):
		return family_of(art_race)
	return str(ITEM_FAMILY.get(iid, DEFAULT_FAMILY))


## 部件的資料表 race 是不是毛皮種族專屬（這種部件衣櫥一律不給）
static func is_fur_item(variant: Dictionary) -> bool:
	return is_fur_race(str(variant.get("race", "")))


## 毛皮種族的預設名字（舊存檔沒改名時，載入改回小白）
const FUR_DEFAULT_NAMES: Dictionary = {"靈尾狐": true, "烈鬃獅": true, "鋼牙豕": true}
const HERO_DEFAULT_NAME := "小白"
const SPEC_JSON_PATH := "res://data/tables/paperdoll_slots.json"

static var _fur_item_cache: Array = []
static var _fur_item_cache_ready := false


## 資料表裡標成毛皮種族專屬的部件 id（直接讀 JSON，不依賴渲染器）
static func fur_item_ids() -> Array:
	if _fur_item_cache_ready:
		return _fur_item_cache
	_fur_item_cache_ready = true
	_fur_item_cache = []
	if not FileAccess.file_exists(SPEC_JSON_PATH):
		return _fur_item_cache
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SPEC_JSON_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		return _fur_item_cache
	var slots: Variant = (parsed as Dictionary).get("slots_architecture", {}).get("slots", [])
	if typeof(slots) != TYPE_ARRAY:
		return _fur_item_cache
	for s in slots:
		if typeof(s) != TYPE_DICTIONARY:
			continue
		for key in ["sample_variants", "default_items"]:
			var vs: Variant = (s as Dictionary).get(key, [])
			if typeof(vs) != TYPE_ARRAY:
				continue
			for v in vs:
				if typeof(v) == TYPE_DICTIONARY and is_fur_item(v):
					_fur_item_cache.append(str((v as Dictionary).get("id", "")))
	return _fur_item_cache


## 舊存檔欄位正規化（純函式，只動傳進來的字典；不是毛皮種族就原樣退回）：
##   player_race 是毛皮種族 → 改回兔子本體；原 id 記 flags["wardrobe.legacy_race"]，家族記 flags["wardrobe.family"]
##   paperdoll_slots 裡毛皮種族專屬部件 → 拿掉，讓渲染器回預設
##   名字還是該族預設名 → 改回小白
static func normalize_legacy_save(d: Dictionary, fur_ids: Array = []) -> Dictionary:
	var raw := str(d.get("player_race", HERO_ART_RACE)).strip_edges().to_lower()
	if not (is_fur_race(raw) or is_family(raw)):
		return d
	var flags: Dictionary = {}
	if typeof(d.get("flags", null)) == TYPE_DICTIONARY:
		flags = d["flags"]
	flags["wardrobe.legacy_race"] = raw
	if not is_family(str(flags.get("wardrobe.family", ""))):
		flags["wardrobe.family"] = family_of(raw)
	d["flags"] = flags
	d["player_race"] = HERO_ART_RACE
	if FUR_DEFAULT_NAMES.has(str(d.get("player_name", ""))):
		d["player_name"] = HERO_DEFAULT_NAME
	var slots: Variant = d.get("paperdoll_slots", {})
	if typeof(slots) == TYPE_DICTIONARY:
		var sl: Dictionary = slots
		for k in sl.keys():
			if str(k) == "race":
				sl[k] = HERO_ART_RACE
			elif fur_ids.has(str(sl[k])):
				sl.erase(k)
		d["paperdoll_slots"] = sl
	return d
