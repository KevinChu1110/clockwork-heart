extends RefCounted
## 抽魂卡面目錄：卡圖、名稱、稀有度框的唯一來源（單抽卡與十連面板共用）。
## 規則（美術任務書 §2/§3）：
## - 每張卡都要是完整零件圖，不准空白、散點、生成失敗圖。
## - 抽卡框只有五色：白、藍、紫、金、彩。內部多階（含機芯八階）只在顯示時壓成五色，不動經濟資料。
## - 「核心碎片」卡已作廢：舊 DropId 一律轉成發條游絲顯示。

## 五色框，順序即稀有度高低。
const FRAME_ORDER: Array[String] = ["white", "blue", "purple", "gold", "rainbow"]

const FRAMES := {
	"white": {
		"frame": Color("#8A8FA3"),
		"bg": Color("#FFFDF8"),
		"glow": Color(0.6, 0.65, 0.75, 0.5),
		"badge": Color("#EAECF0"),
		"stars": "★",
		"name": "普通",
	},
	"blue": {
		"frame": Color("#38A0FF"),
		"bg": Color("#FFFDF8"),
		"glow": Color(0.22, 0.63, 1.0, 0.65),
		"badge": Color("#38A0FF"),
		"stars": "★ ★",
		"name": "精良",
	},
	"purple": {
		"frame": Color("#A259FF"),
		"bg": Color("#FFFDF8"),
		"glow": Color(0.64, 0.35, 1.0, 0.70),
		"badge": Color("#A259FF"),
		"stars": "★ ★ ★",
		"name": "稀有",
	},
	"gold": {
		"frame": Color("#FFD028"),
		"bg": Color("#FFFDF8"),
		"glow": Color(1.0, 0.82, 0.16, 0.75),
		"badge": Color("#FFD028"),
		"stars": "★ ★ ★ ★",
		"name": "傳說",
	},
	"rainbow": {
		"frame": Color("#FF5E8A"),
		"bg": Color("#FFFDF8"),
		"glow": Color(1.0, 0.45, 0.75, 0.80),
		"badge": Color("#FFD028"),
		"stars": "★ ★ ★ ★ ★",
		"name": "炫彩",
		"rainbow": true,
	},
}

## 彩框用的彩帶色（只拿來畫框頂一條，不當主色）
const RAINBOW_STOPS: Array[Color] = [
	Color("#FF5E8A"), Color("#FFA010"), Color("#FFD028"), Color("#4ED86A"), Color("#38A0FF"), Color("#A259FF"),
]

## 內部階 → 顯示五色。涵蓋：
## - 機芯／裝備八階（core_system：gray < white < orange < blue < purple < gold < green < red）
## - 舊文件八色階（白 綠 藍 紫 金 橘 紅 彩）
## - 戰魂品質（大凶 凡 吉 大吉 稀世 神 秘境）
const TIER_TO_FRAME := {
	"gray": "white",
	"white": "white",
	"orange": "blue",
	"blue": "blue",
	"purple": "purple",
	"gold": "gold",
	"green": "rainbow",
	"red": "rainbow",
	"rainbow": "rainbow",
	"白": "white",
	"綠": "white",
	"藍": "blue",
	"紫": "purple",
	"金": "gold",
	"橘": "gold",
	"紅": "rainbow",
	"彩": "rainbow",
	"大凶": "white",
	"凡": "white",
	"吉": "blue",
	"大吉": "purple",
	"稀世": "gold",
	"秘境": "gold",
	"神": "rainbow",
}

## 作廢的 DropId → 接手的有效零件（舊存檔／舊結果字典仍可顯示）
const RETIRED_DROPS := {
	"drop_core_shard": "drop_spring_coil",
}

## 卡圖：全部是透明底、主體完整的 128px 圖示
const DROP_ASSETS := {
	"drop_brass_gear": "res://assets/icons/core_slots/slot_04_transmission_gears.png",
	"drop_spring_coil": "res://assets/icons/core_slots/slot_01_spring_generator.png",
	"junk_enamel_chip": "res://assets/icons/core_slots/slot_02_chassis_armor.png",
	"outfit_cream": "res://assets/icons/soul_draw/outfit_cream.png",
	"outfit_brass_vest": "res://assets/icons/soul_draw/outfit_brass_vest.png",
	"outfit_scarf_tunic": "res://assets/icons/soul_draw/outfit_scarf_tunic.png",
	"outfit_worker_apron": "res://assets/icons/soul_draw/outfit_worker_apron.png",
}

## 查無對照時的保底卡圖（完整零件，不會空白）
const FALLBACK_ART := "res://assets/icons/core_slots/slot_01_spring_generator.png"
## 還沒抽之前的待機卡圖：發條鑰匙
const IDLE_ART := "res://assets/icons/hud/icon_energy_key.png"

## 內部階（經濟資料用，可多於五階）；顯示一律走 frame_for_tier()
const DROP_TIERS := {
	"junk_enamel_chip": "white",
	"drop_brass_gear": "orange",
	"drop_spring_coil": "blue",
	"outfit_cream": "purple",
	"outfit_brass_vest": "purple",
	"outfit_scarf_tunic": "purple",
	"outfit_worker_apron": "purple",
}

## 換裝名用玩具家族（任務書 §2：衣櫥不再用狐／獅／野豬）；字串與衣櫥線共用同一組 i18n key
const DROP_NAMES := {
	"drop_brass_gear": "黃銅齒輪",
	"drop_spring_coil": "發條游絲",
	"outfit_cream": "小白 · 奶油便服",
	"outfit_brass_vest": "錫兵 · 黃銅背心",
	"outfit_scarf_tunic": "八音盒 · 圍巾長衫",
	"outfit_worker_apron": "錫兵 · 工匠工裙",
	"junk_enamel_chip": "搪瓷碎屑",
}

const KIND_NAMES := {
	"outfit": "換裝",
	"part": "零件",
	"junk": "雜件",
}


static func resolve_drop_id(drop_id: String) -> String:
	return str(RETIRED_DROPS.get(drop_id, drop_id))


static func is_retired(drop_id: String) -> bool:
	return RETIRED_DROPS.has(drop_id)


static func frame_for_tier(internal_tier: String) -> String:
	if FRAMES.has(internal_tier):
		return internal_tier
	return str(TIER_TO_FRAME.get(internal_tier, "blue"))


static func frame_key_for_drop(drop: Dictionary) -> String:
	var kind: String = str(drop.get("kind", ""))
	if kind == "outfit":
		return frame_for_tier("purple")
	if kind == "junk":
		return frame_for_tier("white")
	var drop_id := resolve_drop_id(str(drop.get("DropId", "")))
	return frame_for_tier(str(DROP_TIERS.get(drop_id, "blue")))


static func frame_data(frame_key: String) -> Dictionary:
	return FRAMES.get(frame_for_tier(frame_key), FRAMES["blue"]) as Dictionary


static func art_path(drop_id: String) -> String:
	var p: String = str(DROP_ASSETS.get(resolve_drop_id(drop_id), ""))
	if p != "" and ResourceLoader.exists(p):
		return p
	return FALLBACK_ART


static func art_texture(drop_id: String) -> Texture2D:
	var p := art_path(drop_id)
	if ResourceLoader.exists(p):
		return load(p) as Texture2D
	return null


static func idle_texture() -> Texture2D:
	if ResourceLoader.exists(IDLE_ART):
		return load(IDLE_ART) as Texture2D
	return load(FALLBACK_ART) as Texture2D


static func drop_name(drop_id: String) -> String:
	var rid := resolve_drop_id(drop_id)
	return str(DROP_NAMES.get(rid, rid))


static func kind_name(kind: String) -> String:
	return str(KIND_NAMES.get(kind, kind))


static func normalize_drop(drop: Dictionary) -> Dictionary:
	## 回傳可顯示的掉落字典：作廢 DropId 換成接手零件
	var out := drop.duplicate()
	var did := str(out.get("DropId", ""))
	if is_retired(did):
		out["DropId"] = resolve_drop_id(did)
		out["kind"] = "part"
		out["retiredFrom"] = did
	return out


static func rainbow_band(height: int = 6) -> TextureRect:
	## 彩框專用：卡頂一條彩帶
	var grad := Gradient.new()
	var offs := PackedFloat32Array()
	var cols := PackedColorArray()
	var n := RAINBOW_STOPS.size()
	for i in n:
		offs.append(float(i) / float(n - 1))
		cols.append(RAINBOW_STOPS[i])
	grad.offsets = offs
	grad.colors = cols
	var tex := GradientTexture2D.new()
	tex.gradient = grad
	tex.width = 64
	tex.height = 1
	var band := TextureRect.new()
	band.name = "RainbowBand"
	band.texture = tex
	band.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	band.stretch_mode = TextureRect.STRETCH_SCALE
	band.set_anchors_preset(Control.PRESET_TOP_WIDE)
	band.offset_left = 16
	band.offset_right = -16
	band.offset_top = 4
	band.offset_bottom = 4 + height
	band.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return band
