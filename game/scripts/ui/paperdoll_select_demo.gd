class_name PaperdollSelectDemo
extends Control
## 《發條之心》紙娃娃五族選角與即時換裝技術驗證面板 (PaperdollSelectDemo)
## 依據規格書 docs/design/paperdoll_slots.json 與手遊人體工學介面規範：
## 1. 橫向 5 大動物族縮圖按鈕（128x128 實體切片縮圖，按鈕熱區 180x108 >= 50px）。
## 2. 中央舞台顯示選取族系之 PaperdollCharacter 節點（7 大槽位疊合渲染）。
## 3. 部件槽即時換裝控制（外裝服飾 costume、機體塗裝 chassis 左右切換）。
## 4. 全程使用開源粉圓體 (OpenHuninn)，嚴禁系統 Emoji，多巴胺鮮亮高飽和配色。

signal character_confirmed(race_id: String, selections: Dictionary)
signal cancelled()

@export var creation_mode: bool = false:
	set(val):
		creation_mode = val
		_update_creation_mode_ui()

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 規格書 (res://data/tables/paperdoll_slots.json) 官方部件名稱快取
static var _spec_variant_names: Dictionary = {}

static func _load_spec_names() -> void:
	if not _spec_variant_names.is_empty():
		return
	const SPEC_PATH := "res://data/tables/paperdoll_slots.json"
	if FileAccess.file_exists(SPEC_PATH):
		var file := FileAccess.open(SPEC_PATH, FileAccess.READ)
		if file != null:
			var json_str := file.get_as_text()
			var json = JSON.parse_string(json_str)
			if json is Dictionary and json.has("slots_architecture"):
				var slots: Array = json["slots_architecture"].get("slots", [])
				for slot in slots:
					var variants: Array = slot.get("sample_variants", [])
					for v in variants:
						var vid: String = str(v.get("id", ""))
						var vname: String = str(v.get("name", ""))
						if not vid.is_empty() and not vname.is_empty():
							_spec_variant_names[vid] = vname

static func get_variant_spec_name(id: String, fallback: String = "") -> String:
	_load_spec_names()
	if id == "none":
		return "無外裝 (裸機素體)"
	if _spec_variant_names.has(id):
		return str(_spec_variant_names[id])
	return fallback if not fallback.is_empty() else id

## 五大種族詳細設定與可用部件變體表
const RACES_DATA: Dictionary = {
	"rabbit": {
		"id": "rabbit",
		"name_zh": "白金兔",
		"name_en": "Whitey",
		"archetype": "劍士 (knight)",
		"thumb": "res://assets/sprites/player/showcase/rabbit_idle_hd.png",
		"desc": "發條之心的守護象徵，身形輕巧，搭載高響應晨曦核心與剛性長耳。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "經典紅藍胡桃鉗金屬禮服與黃銅肩章"},
			{"id": "costume_steam_artisan", "name_zh": "蒸氣工匠吊帶工作裝", "desc": "耐磨工匠鍛鐵胸板與工具掛扣"},
			{"id": "costume_royal_parade", "name_zh": "皇家巡遊金屬禮服", "desc": "奢華深藍金屬胸甲與雙排齒輪扣典禮禮服"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白精密機械軀體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "溫潤微光象牙白高光琺瑯塗層"},
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "古典黃銅金屬原色重拋光鏡面"},
			{"id": "paint_midnight_navy", "name_zh": "午夜深藍烤漆", "desc": "深邃暗夜深藍高光琺瑯防護塗層"}
		]
	},
	"fox": {
		"id": "fox",
		"name_zh": "靈尾狐",
		"name_en": "Fox",
		"archetype": "法師 (mage)",
		"thumb": "res://assets/sprites/player/showcase/fox_idle_hd.png",
		"desc": "掌握星軌共鳴的靈動玩具法師，具備金屬雷達耳與分節發條尾。",
		"costumes": [
			{"id": "costume_astral_cape", "name_zh": "星紋見習占星斗篷", "desc": "深藍琺瑯釉面與星芒金屬扣"},
			{"id": "costume_astral_observer", "name_zh": "星象觀測者金屬儀裝", "desc": "黃銅星軌刻盤護胸與青銅鉚釘金屬儀裝"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現曜橙靈動狐型素體"}
		],
		"chassis": [
			{"id": "paint_fox_orange", "name_zh": "靈狐曜橙烤漆", "desc": "高飽和鮮明暖橘琺瑯烤漆"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "低調優雅素體象牙白烤漆"},
			{"id": "paint_emerald_glaze", "name_zh": "翡翠螢光釉面", "desc": "翡翠深林星光微粒高光琺瑯釉面"}
		]
	},
	"lion": {
		"id": "lion",
		"name_zh": "烈鬃獅",
		"name_en": "Lion",
		"archetype": "騎士 (knight)",
		"thumb": "res://assets/sprites/player/showcase/lion_idle_hd.png",
		"desc": "恪守騎士榮譽的黃銅機甲獅，配備金色板件鬃毛與折疊尾翼。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "典禮侍衛金屬胸甲與禮服分件"},
			{"id": "costume_steam_artisan", "name_zh": "蒸氣工匠吊帶工作裝", "desc": "工匠耐磨鍛鐵護胸吊帶與鉚釘金屬搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現全黃銅厚重鍛造素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "皇家黃金尊貴拋光金屬外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "皇家象牙白紀念版典雅塗裝"},
			{"id": "paint_midnight_navy", "name_zh": "午夜深藍烤漆", "desc": "深邃暗夜深藍高光琺瑯防護塗層"}
		]
	},
	"boar": {
		"id": "boar",
		"name_zh": "鋼牙豕",
		"name_en": "Boar",
		"archetype": "戰士 (viking)",
		"thumb": "res://assets/sprites/player/showcase/boar_idle_hd.png",
		"desc": "熔爐鐵匠鋪的重型開拓者，金屬鉚釘獠牙與強韌彈簧衝擊核心。",
		"costumes": [
			{"id": "costume_viking_harness", "name_zh": "粗獷鍛爐護胸鐵束帶", "desc": "鉚釘加固厚重鍛鐵戰士胸甲"},
			{"id": "costume_viking_ironclad", "name_zh": "維京重裝鍛鐵板甲", "desc": "耐高溫重型鍛鐵板甲與雙列鉚釘金屬護肩"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現剛硬生鐵鍛造衝擊素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "耐磨耐高溫黃銅金屬強化外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白抗衝擊塗裝"},
			{"id": "paint_molten_crimson", "name_zh": "赤焰熔爐烤漆", "desc": "耐高溫赤焰琺瑯防護塗層"}
		]
	},
	"macaque": {
		"id": "macaque",
		"name_zh": "靈爪猴",
		"name_en": "Macaque",
		"archetype": "武術家 (monk)",
		"thumb": "res://assets/sprites/player/showcase/macaque_idle_hd.png",
		"desc": "敏捷靈活的彈簧行者，同軸金屬耳與伸縮爪刃，機巧多變。",
		"costumes": [
			{"id": "costume_dawn_monk_tunic", "name_zh": "晨曦行者武道短褂", "desc": "輕量合金武道短褂分件"},
			{"id": "costume_zen_striker", "name_zh": "天元演武者機關甲", "desc": "青古銅榫卯護胸板與天元金黃鉚釘搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現極簡彈簧骨架素體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "高韌性象牙白減震琺瑯"},
			{"id": "paint_bamboo_bronze", "name_zh": "天元青古銅烤漆", "desc": "沉穩青古銅釉面金屬板件與黃銅關節"}
		]
	},
	"tiger": {
		"id": "tiger",
		"name_zh": "烈焰虎",
		"name_en": "Tiger",
		"archetype": "忍者 (ninja)",
		"thumb": "res://assets/sprites/player/showcase/tiger_idle_hd.png",
		"desc": "赤焰熔爐淬火工坊的迅捷玩具，雙短刃高頻暴擊，散熱尾管與熔火核心。",
		"costumes": [
			{"id": "costume_ember_tunic", "name_zh": "餘燼工匠淬火戰褂", "desc": "耐高溫輕量合金戰褂分件"},
			{"id": "costume_ash_ninja_garb", "name_zh": "灰燼夜行機關裝", "desc": "曜黑輕量合金機關戰裝與黃金齒輪暗扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現餘燼橙紅機甲素體"}
		],
		"chassis": [
			{"id": "paint_ember_orange", "name_zh": "原廠餘燼橙紅", "desc": "高溫陽極氧化耐熱橙紅烤漆"},
			{"id": "paint_volcano_black", "name_zh": "鍛爐淬火曜黑烤漆", "desc": "曜黑高光耐熱琺瑯與暗金黃銅關節"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光琺瑯塗層"}
		]
	},
	"bear": {
		"id": "bear",
		"name_zh": "玄軸熊",
		"name_en": "Iron Bear",
		"archetype": "戰士 (viking)",
		"thumb": "res://assets/sprites/player/showcase/bear_idle_hd.png",
		"desc": "玄軸工坊重型機甲，剛毅沉穩的發條巨熊，配置重裝外殼與高扭力擺線核心。",
		"costumes": [
			{"id": "costume_ironclad_overalls", "name_zh": "玄軸工坊重裝工作吊帶甲", "desc": "耐衝擊重型鍛造吊帶金屬胸甲"},
			{"id": "costume_berserker_cuirass", "name_zh": "狂戰破陣機關戰鎧", "desc": "重裝鍛鋼胸甲、雙肩鉸鏈護肩與維京鉚釘板甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現重型鍛鐵玄軸素體"}
		],
		"chassis": [
			{"id": "paint_bear_amber", "name_zh": "原廠玄軸琥珀棕", "desc": "沉穩深琥珀琺瑯金屬烤漆"},
			{"id": "paint_iron_quarry", "name_zh": "重裝礦山玄鐵灰", "desc": "沉穩深冷礦山玄鐵高光琺瑯與黃銅球窩關節"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白抗衝擊塗裝"}
		]
	},
	"crane": {
		"id": "crane",
		"name_zh": "雲嵐鶴",
		"name_en": "Cloud Crane",
		"archetype": "遊俠 (ranger)",
		"thumb": "res://assets/sprites/player/showcase/crane_idle_hd.png",
		"desc": "雲嵐機關閣的靈巧玩具，修長纖細的流線身形，搭載輕量雙羽導流翼板與羽翼尾機關。",
		"costumes": [
			{"id": "costume_zephyr_robe", "name_zh": "凌雲羽衣輕鋼道袍", "desc": "輕合金陶瓷薄板與雙羽導流道袍"},
			{"id": "costume_sky_hunter_mail", "name_zh": "晴空巡獵機關羽甲", "desc": "高機動輕合金折疊羽甲與導風肩甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現修長流線機關素體"}
		],
		"chassis": [
			{"id": "paint_crane_porcelain", "name_zh": "原廠冷淬青瓷白", "desc": "清雅雲嵐微光白瓷高光琺瑯"},
			{"id": "paint_zephyr_azure", "name_zh": "晴空凌雲湛藍", "desc": "晴空凌雲深邃湛藍高光琺瑯烤漆"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光塗層"}
		]
	},
	"penguin": {
		"id": "penguin",
		"name_zh": "蒸氣企鵝",
		"name_en": "Steam Penguin",
		"archetype": "遊俠 (ranger)",
		"thumb": "res://assets/sprites/player/showcase/penguin_idle_hd.png",
		"desc": "淵海發條港灣的憨厚重火手，耐高壓鍍鈦燕尾裝甲與防滑金屬腳蹼。",
		"costumes": [
			{"id": "costume_navigator_harness", "name_zh": "深海導航員大衣", "desc": "耐壓鍍鈦深藍大衣與黃銅導航儀扣"},
			{"id": "costume_abyssal_diver_cuirass", "name_zh": "淵海深潛耐壓機關鎧", "desc": "重型深海耐壓合金胸甲、雙肩減壓鉸鏈閥與極地破冰鉚釘護甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現耐壓鍍鈦企鵝素體"}
		],
		"chassis": [
			{"id": "paint_penguin_navy", "name_zh": "原廠深海鍍鈦藍", "desc": "高壓陽極氧化深海鍍鈦藍烤漆"},
			{"id": "paint_polar_frost", "name_zh": "極光冰川銀白", "desc": "極地破冰銀白高光鍍鉻烤漆與耐寒琺瑯"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光琺瑯塗層"}
		]
	},
	"tortoise": {
		"id": "tortoise",
		"name_zh": "玄機龜",
		"name_en": "The Xuanji Tortoise",
		"archetype": "法師 (mage)",
		"thumb": "res://assets/sprites/player/showcase/tortoise_idle_hd.png",
		"desc": "竹影道場的機關術宗師，青古銅龜甲板件與浮空八卦發條星盤。",
		"costumes": [
			{"id": "costume_zen_dojo_harness", "name_zh": "天元道場玄機護甲", "desc": "青古銅龜甲與乾坤道袍飾帶"},
			{"id": "costume_bagua_master_robe", "name_zh": "乾坤八卦宗師道鎧", "desc": "玄奧乾坤八卦紋金屬道鎧與太極護心鏡板"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現青古銅玄機素體"}
		],
		"chassis": [
			{"id": "paint_tortoise_jade", "name_zh": "原廠青銅古翠綠", "desc": "青古銅深翠綠金屬琺瑯烤漆"},
			{"id": "paint_basalt_black", "name_zh": "玄武黑曜淬火黑", "desc": "玄武黑曜淬火黑鋼與電氣青藍導線烤漆"}
		]
	},
	"elephant": {
		"id": "elephant",
		"name_zh": "鋼岳象",
		"name_en": "The Colossus Elephant",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/elephant_idle_hd.png",
		"desc": "巨輪工坊的開山巨靈，黃銅鉚接板件與六節套筒液壓長鼻。",
		"costumes": [
			{"id": "costume_cog_workshop_overalls", "name_zh": "巨輪工坊厚鋼工裝", "desc": "重型齒輪鉚接工裝與厚鋼護膝吊帶"},
			{"id": "costume_colossus_bastion_plate", "name_zh": "鋼岳要塞重裝戰鎧", "desc": "高爐鎢鋼重裝胸甲、雙層齒輪鉸鏈護肩與下擺護甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現黃銅原金重裝素體"}
		],
		"chassis": [
			{"id": "paint_elephant_brass", "name_zh": "原廠巨輪工坊黃銅原金", "desc": "重型工業黃銅原金與拋光金屬護甲"},
			{"id": "paint_tungsten_iron", "name_zh": "高爐鎢鋼淬火黑", "desc": "高爐鎢鋼淬火黑外殼與沉穩金屬消光厚板件"}
		]
	},
	"frog": {
		"id": "frog",
		"name_zh": "碧箸蛙",
		"name_en": "The Spring-Leg Frog",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/frog_idle_hd.png",
		"desc": "翡翠深林的靈動斥候，沖壓翠綠琺瑯馬口鐵板，雙聯凸透鏡眼與折疊板簧足柱。",
		"costumes": [
			{"id": "costume_spring_forest_courier", "name_zh": "碧箐巡林客工裝", "desc": "輕量油布披肩與黃銅齒輪滾邊巡林工裝"},
			{"id": "costume_astral_cape", "name_zh": "星紋斗篷", "desc": "深藍琺瑯釉面與星芒金屬扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現翠綠琺瑯跳蛙素體"}
		],
		"chassis": [
			{"id": "paint_frog_emerald", "name_zh": "原廠薄荷翡翠綠", "desc": "原廠薄荷翡翠綠高光琺瑯烤漆"}
		]
	},
	"panda": {
		"id": "panda",
		"name_zh": "瓷韻熊貓",
		"name_en": "The Porcelain Panda",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/panda_idle_hd.png",
		"desc": "自天元竹林悟道的發條陶瓷熊貓，黑白高溫生漆陶瓷板件，青古銅榫卯鉸鏈與太極重力平衡陀。",
		"costumes": [
			{"id": "costume_panda_zen_apprentice_robe", "name_zh": "禪道學徒生漆長袍", "desc": "高溫黑白生漆陶瓷板件與天元道場武道長袍"},
			{"id": "costume_dawn_monk_tunic", "name_zh": "晨曦武道短裋", "desc": "輕量合金武道短裋分件，武術家長袍"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現黑白雙色陶瓷機體素體"}
		],
		"chassis": [
			{"id": "paint_panda_porcelain", "name_zh": "羊脂白瓷生漆塗裝", "desc": "原廠羊脂白玉冰裂瓷與黑生漆高光塗裝"}
		]
	},
	"fawn": {
		"id": "fawn",
		"name_zh": "翠角鹿",
		"name_en": "The Emerald Fawn",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/fawn_idle_hd.png",
		"desc": "自翡翠深林守護巡林的發條小鹿，米白淺褐薄鐵皮板件，精密黃銅游標卡尺角尺天線與減震馬蹄墊。",
		"costumes": [
			{"id": "costume_fawn_emerald_scout_tunic", "name_zh": "翡翠林緣巡守工裝", "desc": "墨綠輕布料披肩配黃銅皮扣巡守工裝"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現米白淺褐原木紋金屬素體"}
		],
		"chassis": [
			{"id": "chassis_fawn_timber_tinplate_default", "name_zh": "雙色沖壓原木紋金屬板", "desc": "沖壓雙色象牙米白與淺褐原木紋金屬板，黃銅鉚釘包邊"}
		]
	},
	"hound": {
		"id": "hound",
		"name_zh": "星軌犬",
		"name_en": "The Orbit Hound",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/hound_idle_hd.png",
		"desc": "自星穹軌道巡弋守望的太空發條小狗，乳白工程塑料板件，高透聚碳酸酯胸腔視窗與微型雷達葉片耳。",
		"costumes": [
			{"id": "costume_hound_space_explorer_harness", "name_zh": "太空探索防護背帶", "desc": "輕量航天防護背帶，微型冷氣儲罐與塑料卡扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙乳白工程塑料素體"}
		],
		"chassis": [
			{"id": "chassis_hound_polymer_astro_default", "name_zh": "模組化乳白工程塑料板件", "desc": "高抗衝擊乳白工程塑料拼裝板件，夜光透窗與天藍飾線"}
		]
	},
	"owl": {
		"id": "owl",
		"name_zh": "靈鐘鴞",
		"name_en": "The Chrono Owl",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/owl_idle_hd.png",
		"desc": "自晨曦小鎮懸吊齒輪鐘樓守候天文走時的發條鐘鴞，沖壓黃銅疊片羽板，雙聯鐘面目鏡與擒縱陀飛輪透窗。",
		"costumes": [
			{"id": "costume_owl_dawn_astronomer_robe", "name_zh": "晨曦觀星學者短披肩斗篷", "desc": "深藍天鵝絨短披肩斗篷，金色星紋刺繡與黃銅胸針"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓黃銅疊片羽翼與午夜曜藍烤漆合金素體"}
		],
		"chassis": [
			{"id": "chassis_owl_brass_lamellae_default", "name_zh": "沖壓黃銅疊片羽翼板件", "desc": "沖壓黃銅疊片羽翼板件，午夜曜藍外裝烤漆，胸前高透石英擒縱陀飛輪透窗"}
		]
	},
	"cat": {
		"id": "cat",
		"name_zh": "幽影貓",
		"name_en": "The Umbral Cat",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/cat_idle_hd.png",
		"desc": "自巨輪城高聳屋脊踏著靜音蒸氣穿梭的發條黑貓，冷軋曜黑碳化鋼板件，折角拾音耳與九節平衡鋼索尾。",
		"costumes": [
			{"id": "costume_cat_skyspire_prowler_vest", "name_zh": "天街巡夜緊身工裝背心", "desc": "巨輪城天街巡夜緊身工裝背心，斜背金屬螺絲刀皮帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現曜黑碳化鋼裝甲與象牙米白琺瑯面頰板"}
		],
		"chassis": [
			{"id": "chassis_cat_obsidian_steel_default", "name_zh": "冷軋曜黑碳化鋼板件", "desc": "高硬度冷軋曜黑碳化鋼板件，象牙米白琺瑯面頰，足底黑色工程矽膠靜音墊"}
		]
	},
	"pangolin": {
		"id": "pangolin",
		"name_zh": "沙鱗穿山甲",
		"name_en": "The Dune Pangolin",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/pangolin_idle_hd.png",
		"desc": "自遺忘舊庫零件沙丘穿梭而出的發條穿山甲，沖壓暖橘覆鱗板件，扇形拾音耳與七節覆鱗尾。",
		"costumes": [
			{"id": "costume_pangolin_scavenger_tinker_vest", "name_zh": "齒輪營地拾荒工匠工裝背心", "desc": "齒輪營地拾荒工匠帆布工裝背心，斜背螺絲起子工具皮帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現暖橘電鍍金屬覆鱗與象牙米白琺瑯面頰板"}
		],
		"chassis": [
			{"id": "chassis_pangolin_dune_orange_default", "name_zh": "沖壓耐磨暖橘金屬覆鱗板件", "desc": "沖壓耐磨暖橘金屬覆鱗板件，象牙米白琺瑯面腹甲，足底黑色工程矽膠防滑墊"}
		]
	},
	"otter": {
		"id": "otter",
		"name_zh": "浪花海獺",
		"name_en": "The Tidal Otter",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/otter_idle_hd.png",
		"desc": "穿梭於琉璃汪洋水下發條宮殿的發條海獺，深海天藍耐壓電鍍合金板件，象牙米白琺瑯面腹甲與五節龍骨舵尾。",
		"costumes": [
			{"id": "costume_otter_deepsea_salvage_harness", "name_zh": "海淵打撈工匠耐壓雙肩吊帶工裝", "desc": "海淵打撈工匠耐壓雙肩吊帶工裝，胸前掛載微型黃銅洩壓閥與螺栓套筒皮帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現天藍電鍍耐壓板件與象牙米白琺瑯面腹甲"}
		],
		"chassis": [
			{"id": "chassis_otter_abyssal_cyan_default", "name_zh": "深海天藍耐壓電鍍合金板件", "desc": "深海天藍耐壓電鍍合金板件，象牙米白琺瑯面頰與前胸腹板，足底黑色工程矽膠防滑靴"}
		]
	},
	"raccoon": {
		"id": "raccoon",
		"name_zh": "星巡浣熊",
		"name_en": "The Orbit Raccoon",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/raccoon_idle_hd.png",
		"desc": "穿梭於星穹軌道透明太空艙與維修船塢的發條浣熊，電光航太青工程聚合物板件，象牙米白工程塑料胸腹板與五節同軸環形天線長尾。",
		"costumes": [
			{"id": "costume_raccoon_space_explorer_harness", "name_zh": "星穹宇航探險工裝背帶", "desc": "星穹宇航探險工裝背帶，胸前掛載微型氣壓表與磁吸工具掛環，肩部配有珊瑚粉耐磨護墊"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現電光航太青工程聚合物板件與象牙米白面龐胸板"}
		],
		"chassis": [
			{"id": "chassis_raccoon_orbit_aqua_default", "name_zh": "電光航太青工程聚合物板件", "desc": "電光航太青工程聚合物板件，象牙米白工程塑料面頰板與胸腹減震板，足底黑色磁吸工程矽膠靴"}
		]
	},
	"hedgehog": {
		"id": "hedgehog",
		"name_zh": "棘輪刺蝟",
		"name_en": "The Ratchet Hedgehog",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/hedgehog_idle_hd.png",
		"desc": "穿梭於晨曦小鎮懸吊齒輪鐘樓與集市的發條刺蝟工匠，琥珀橙拋光黃銅外殼，象牙米白琺瑯面龐與薄荷螢綠單片放大鏡。",
		"costumes": [
			{"id": "costume_hedgehog_marionette_tailor_vest", "name_zh": "晨曦提線裁縫工匠馬甲", "desc": "晨曦提線裁縫工匠馬甲，胸前縫嵌精紡棉線捲軸與螺絲刀插袋，領口佩戴珊瑚粉領結"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現溫暖琥珀橙拋光黃銅板件與象牙米白面龐胸板"}
		],
		"chassis": [
			{"id": "chassis_hedgehog_amber_brass_default", "name_zh": "溫暖琥珀橙拋光黃銅外殼", "desc": "溫暖琥珀橙拋光黃銅外殼，象牙米白琺瑯面頰板與胸腹減震板，足底黑色工匠矽膠靴"}
		]
	},
	"wolf": {
		"id": "wolf",
		"name_zh": "荒原鋼狼",
		"name_en": "The Scrap Wolf",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/wolf_idle_hd.png",
		"desc": "遊蕩於荒漠舊庫廢土的發條鋼狼騎士，多巴胺暖橘防鏽鋼板，象牙米白琺瑯面龐與星輝天藍雙聯晶核目鏡。",
		"costumes": [
			{"id": "costume_wolf_scavenger_scrap_plate_armor", "name_zh": "廢土拾荒者拼裝板甲", "desc": "胸前防鏽暖橘鋼胸甲搭配粗麻帆布肩帶，腰掛黃銅調節卡扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現多巴胺暖橘防鏽鋼板與象牙米白琺瑯前胸減震板"}
		],
		"chassis": [
			{"id": "chassis_wolf_warm_orange_default", "name_zh": "廢土多巴胺暖橘防鏽烤漆鋼板", "desc": "廢土多巴胺暖橘防鏽烤漆鋼板，象牙米白琺瑯面頰板與胸腹減震板，足底黑色工業矽膠行軍靴"}
		]
	},
	"seahorse": {
		"id": "seahorse",
		"name_zh": "琉璃海馬",
		"name_en": "The Crystal Seahorse",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/seahorse_idle_hd.png",
		"desc": "穿梭於琉璃汪洋海淵的發條海馬學者，高透海藍琺瑯烤漆，象牙米白陶瓷面頰與雙聯深海藍寶石透鏡目鏡。",
		"costumes": [
			{"id": "costume_seahorse_abyssal_scholar_harness", "name_zh": "海淵天宮星象輕甲工裝", "desc": "象牙白陶瓷釉面胸甲，兩側海藍鍍鈦弧形護肩，腰間附防腐蝕背帶與氣壓計"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現高透光海藍琺瑯烤漆裝甲板與象牙米白陶瓷胸板"}
		],
		"chassis": [
			{"id": "chassis_seahorse_abyssal_cyan_default", "name_zh": "琉璃海馬原廠海藍琺瑯烤漆素體", "desc": "多巴胺海藍琺瑯烤漆，鍍鈦水平防壓加強筋，五節高彈錳鋼螺旋板簧尾"}
		]
	},
	"kangaroo": {
		"id": "kangaroo",
		"name_zh": "鐵拳袋鼠",
		"name_en": "The Boxer Kangaroo",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/kangaroo_idle_hd.png",
		"desc": "巨輪城動力廣場的發條拳擊家，焦糖暖褐赤銅板件，雙螺旋減震彈簧腿與氣壓活塞雙拳套。",
		"costumes": [
			{"id": "costume_kangaroo_champion_belt_harness", "name_zh": "巨輪城工匠拳王加固背帶皮甲", "desc": "半圓形奶油米白琺瑯沖壓齒輪袋，加固棕褐皮帶與胡桃鉗朱紅滾邊"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現焦糖暖褐赤銅金屬裝甲與冷軋鎢鋼螺旋彈簧腿"}
		],
		"chassis": [
			{"id": "chassis_kangaroo_caramel_bronze_default", "name_zh": "鐵拳袋鼠原廠焦糖暖褐赤銅素體", "desc": "多巴胺焦糖暖褐赤銅烤漆，冷軋鎢鋼雙螺旋彈簧腿，分節重力平衡長尾"}
		]
	},
	"squirrel": {
		"id": "squirrel",
		"name_zh": "巡林松鼠",
		"name_en": "The Timber Squirrel",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/squirrel_idle_hd.png",
		"desc": "翡翠深林巨木樹屋的特快信差與巡守騎士，栗木暖褐銅板素體，西洋擊劍花劍與九節齒輪大尾巴。",
		"costumes": [
			{"id": "costume_squirrel_canopy_courier_harness", "name_zh": "林冠信差遊俠短披風與擊劍皮扣裝甲", "desc": "翡翠墨綠單側輕量披風，金黃齒輪搭扣皮革胸帶與沖壓藤蔓銅徽"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現栗木暖褐沖壓銅板裝甲與九節齒輪陀螺大尾巴"}
		],
		"chassis": [
			{"id": "chassis_squirrel_chestnut_bronze_default", "name_zh": "巡林松鼠原廠栗木暖褐沖壓銅板素體", "desc": "多巴胺栗木暖褐烤漆，奶油琺瑯面頰與胸板，鎢鋼冷軋球窩關節"}
		]
	},
	"salamander": {
		"id": "salamander",
		"name_zh": "熔火蜥蜴",
		"name_en": "The Magma Salamander",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/salamander_idle_hd.png",
		"desc": "赤焰熔爐管網深處的耐火工兵與鍛造戰士，黑曜鎢鋼素體，熔爐衝壓巨錘與五節重鋼同軸阻尼大尾巴。",
		"costumes": [
			{"id": "costume_salamander_foundry_sapper_apron", "name_zh": "地熱工兵耐火鉚接圍裙", "desc": "耐磨皮質圍裙，珊瑚粉金屬扣帶與金黃腰帶，胸前微型蒸氣壓力錶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現黑曜鎢鋼冷軋薄板件與五節重鋼同軸阻尼大尾巴"}
		],
		"chassis": [
			{"id": "chassis_salamander_magma_tungsten_default", "name_zh": "熔火蜥蜴原廠黑曜鎢鋼耐熱金屬素體", "desc": "黑曜鎢鋼冷軋薄板件，熔岩暖金飾邊，奶油米白琺瑯面罩"}
		]
	},
	"viper": {
		"id": "viper",
		"name_zh": "竹影青蛇",
		"name_en": "The Bamboo Viper",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/viper_idle_hd.png",
		"desc": "天元竹林深處的道場巡查木雕蛇偶，翠綠生漆素體，疾風竹影短匕與七節同軸鉸接木簧蛇尾。",
		"costumes": [
			{"id": "costume_viper_zen_dojo_shinobi_wrap", "name_zh": "道場竹影夜行忍裝", "desc": "水墨青石灰布甲搭配翠綠滾邊，天元金黃編織腰帶與珊瑚粉扣帶，胸前太極齒輪紋飾"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現翠綠生漆拋光竹片素體與七節同軸鉸接木簧蛇尾"}
		],
		"chassis": [
			{"id": "chassis_viper_bamboo_lacquer_default", "name_zh": "竹影青蛇原廠翠綠生漆鉸接木雕素體", "desc": "高剛性天然竹木纖維多層生漆拋光板件，奶油米白琺瑯面罩，溫潤翠綠琉璃珠目鏡"}
		]
	},
	"falcon": {
		"id": "falcon",
		"name_zh": "疾影神隼",
		"name_en": "The Swift Falcon",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/falcon_idle_hd.png",
		"desc": "翡翠深林高空的空境巡守神隼偶，象牙米白與暖金黃銅素體，疾影穿雲機關爪與三聯空氣動力滑翔舵板尾羽。",
		"costumes": [
			{"id": "costume_falcon_skyline_warden_harness", "name_zh": "空境巡守輕裝風行胸背甲", "desc": "曜石鐵灰耐磨皮革與輕量化薄鋼胸甲，翡翠綠滾邊飾條與天元金黃鎖扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙米白琺瑯冷軋薄鋼素體與沖壓高剛性黃銅疊片羽翼"}
		],
		"chassis": [
			{"id": "chassis_falcon_aero_brass_default", "name_zh": "疾影神隼原廠曜金冷軋合金素體", "desc": "象牙米白琺瑯冷軋薄鋼板件，內嵌高剛性疊片黃銅羽板，琥珀石英雙聯鷹眼目鏡"}
		]
	},
	"ram": {
		"id": "ram",
		"name_zh": "星盤靈羊",
		"name_en": "The Astral Ram",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/ram_idle_hd.png",
		"desc": "星穹軌道空間站的巡禮法師偶，象牙白聚合物素體，星軌游絲共鳴杖與雙螺旋超導游絲盤角。",
		"costumes": [
			{"id": "costume_ram_gravity_starlight_robe", "name_zh": "星軌漫步者引力法袍", "desc": "天藍色防靜電披肩法袍搭配珊瑚粉滾邊，重疊弧面琺瑯雲紋防護胸甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白工程聚合物塑料素體與弧面沖壓琺瑯雲紋疊片"}
		],
		"chassis": [
			{"id": "chassis_ram_astral_polymer_default", "name_zh": "星穹象牙白聚合物素體", "desc": "高光象牙白工程塑料板件，弧面琺瑯雲紋疊片，星光琥珀金色點陣LED目鏡"}
		]
	},
	"chameleon": {
		"id": "chameleon",
		"name_zh": "幻彩變色龍",
		"name_en": "The Mirage Chameleon",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/chameleon_idle_hd.png",
		"desc": "底層荒漠齒輪塚的拾荒哨戒長，鍍鈦變色合金素體，幻彩棱鏡複合機關弓與雙向自轉砲塔測距目鏡。",
		"costumes": [
			{"id": "costume_chameleon_wasteland_scout_rig", "name_zh": "荒原斥候防沙迷彩背心裝甲", "desc": "暖橘色耐磨防水帆布背心，胸前鉚接象牙白與薄荷綠防護胸甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白抗磨鍍鈦板件與多層光學干涉薄膜"}
		],
		"chassis": [
			{"id": "chassis_chameleon_mirage_titanium_default", "name_zh": "幻彩鍍鈦變色合金素體", "desc": "抗磨鍍鈦合金板件，微型螺絲嵌合線，琥珀金色石英凸透鏡"}
		]
	},
	"sailfish": {
		"id": "sailfish",
		"name_zh": "破浪旗魚",
		"name_en": "The Hydrofoil Sailfish",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/sailfish_idle_hd.png",
		"desc": "深海發條海淵的巡洋長，深海陽極氧化鍍鈦骨架，破浪螺旋合金長槍與多節發條折疊背鰭帆。",
		"costumes": [
			{"id": "costume_sailfish_abyssal_knight_cuirass", "name_zh": "海淵深潛騎士重裝護胸甲", "desc": "鈷藍色耐壓加厚鍍鈦胸甲，胸口鉚接象牙白與珊瑚金海錨紋飾"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現深海陽極氧化鈷藍鍍鈦板件與陶瓷胸腹板"}
		],
		"chassis": [
			{"id": "chassis_sailfish_abyssal_titanium_default", "name_zh": "破浪旗魚深海鍍鈦骨架素體", "desc": "抗侵蝕陽極氧化鈷藍鍍鈦板件，象牙白陶瓷胸腹，雙葉螺旋推進尾"}
		]
	},
	"rhino": {
		"id": "rhino",
		"name_zh": "重角犀牛",
		"name_en": "The Heavyhorn Rhino",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/rhino_idle_hd.png",
		"desc": "赤焰熔爐的破陣先鋒，粗砂鑄鐵重裝裝甲，雙聯衝壓重角與熔爐破陣重鋼戰斧。",
		"costumes": [
			{"id": "costume_rhino_crucible_smith_plate", "name_zh": "熔火鍛造重裝護胸甲", "desc": "黑曜耐火弧面胸甲，胸口鉚接拋光黃銅鐵砧浮雕與暖橘警示壓條"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現消光粗砂黑鑄鐵板件與黑曜淬火耐火層"}
		],
		"chassis": [
			{"id": "chassis_rhino_molten_iron_default", "name_zh": "重角犀牛熔鑄粗鐵素體", "desc": "粗砂黑鑄鐵板件，球窩關節配防燙天藍耐熱圈，發條配重短尾"}
		]
	},
	"bat": {
		"id": "bat",
		"name_zh": "星翼蝙蝠",
		"name_en": "The Starwing Bat",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/bat_idle_hd.png",
		"desc": "星穹軌道的失重暗影刺客，消光極光紫黑航太裝甲，雙聯聲納雷達耳與超導脈衝星紋鏢。",
		"costumes": [
			{"id": "costume_bat_orbital_stealth_harness", "name_zh": "星穹失重匿蹤飛行胸甲", "desc": "象牙米白琺瑯前甲，兩側微型冷氣向量反推噴嘴與珊瑚粉發光能量卡扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現消光極光紫黑航太工程塑料板件與雙耳聲納雷達"}
		],
		"chassis": [
			{"id": "chassis_bat_astral_polymer_default", "name_zh": "星翼蝙蝠極光紫黑航太聚合物素體", "desc": "消光極光紫黑航太塑料板件，曜黑球窩關節配珊瑚粉防塵圈，倒懸磁吸矽膠爪"}
		]
	},
	"gorilla": {
		"id": "gorilla",
		"name_zh": "鋼臂巨猩",
		"name_en": "The Steelarm Gorilla",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/gorilla_idle_hd.png",
		"desc": "黃銅都市的重裝武術家，消光鑄鐵沖壓黃銅裝甲，雙聯蒸氣壓力表與高壓鍛打拳套。",
		"costumes": [
			{"id": "costume_gorilla_steam_forge_boiler_harness", "name_zh": "巨輪鍛工高壓鍋爐背帶胸甲", "desc": "象牙米白琺瑯防護面板，耐磨工裝背帶與紫銅氣動活塞桿"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現消光鑄鐵板件與雙渦輪高壓排氣煙囪"}
		],
		"chassis": [
			{"id": "chassis_gorilla_brass_heavy_default", "name_zh": "鋼臂巨猩重型沖壓黃銅素體", "desc": "沖壓黃銅板件，鎢鋼前臂配球窩外露關節，菱形防滑金屬掌板"}
		]
	},
	"peacock": {
		"id": "peacock",
		"name_zh": "稜鏡孔雀",
		"name_en": "The Prism Peacock",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/peacock_idle_hd.png",
		"desc": "晨曦小鎮的光學法師，彩釉琺瑯金屬素體，萬花筒雙色寶石目鏡與聚能稜鏡。",
		"costumes": [
			{"id": "costume_peacock_marionette_court_cuirass", "name_zh": "木偶宮廷巴洛克金線胸甲", "desc": "奶油米白琺瑯面甲，多巴胺金卷草金紋與水滴寶石搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現彩釉琺瑯金屬板件與鉸接機械開屏晶扇"}
		],
		"chassis": [
			{"id": "chassis_peacock_glazed_porcelain_default", "name_zh": "稜鏡孔雀彩釉琺瑯金屬素體", "desc": "彩釉琺瑯外殼，黃銅球窩卡扣，芭蕾丁字步站姿"}
		]
	},
	"meerkat": {
		"id": "meerkat",
		"name_zh": "沙哨狐獴",
		"name_en": "The Sentry Meerkat",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/meerkat_idle_hd.png",
		"desc": "荒漠齒輪塚的高點哨兵遊俠，沖壓馬口鐵素體，潛望式測距目鏡與生鏽彈簧刺銃。",
		"costumes": [
			{"id": "costume_meerkat_patched_canvas_poncho", "name_zh": "廢土補丁帆布防沙短斗篷", "desc": "多巴胺亮橘與赭石耐磨帆布斗篷，生鏽黃銅搭扣與沖壓護胸板"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓馬口鐵板件與鉸接金屬三腳平衡擺尾"}
		],
		"chassis": [
			{"id": "chassis_meerkat_tinplate_default", "name_zh": "沙哨狐獴沖壓馬口鐵金屬素體", "desc": "沖壓耐磨馬口鐵板件，奶油米白防鏽漆面，直立哨兵站姿"}
		]
	},
	"courser": {
		"id": "courser",
		"name_zh": "鐵蹄駿駒",
		"name_en": "The Ironhoof Courser",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/courser_idle_hd.png",
		"desc": "晨曦小鎮的巡防正義騎士，奶油米白合金素體，波浪齒輪鬃甲與晨曦齒輪騎兵劍。",
		"costumes": [
			{"id": "costume_courser_dawn_patrol_cuirass", "name_zh": "晨曦巡防騎士拋光輕胸甲", "desc": "金黃暖橘滾邊拋光輕胸甲，薄荷綠琺瑯徽章與鞍轡飾帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現奶油米白琺瑯合金板件與金屬流線甩尾"}
		],
		"chassis": [
			{"id": "chassis_courser_cream_gold_default", "name_zh": "鐵蹄駿駒奶油金黃合金素體", "desc": "拋光奶油米白琺瑯板件，金黃黃銅接縫與鎢鋼耐磨蹄鐵，挺拔巡防站姿"}
		]
	},
	"beaver": {
		"id": "beaver",
		"name_zh": "劈木河狸",
		"name_en": "The Woodchopper Beaver",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/beaver_idle_hd.png",
		"desc": "翡翠深林的首席破障工兵，深森墨綠耐磨合金素體，沖壓雙聯黃銅鑿齒與深林拓荒劈木巨斧。",
		"costumes": [
			{"id": "costume_beaver_deepwood_sapper_harness", "name_zh": "深林開拓工兵抗磨胸甲", "desc": "暖橘滾邊深森耐磨胸甲，薄荷綠工具扣環與粗皮革斜背帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現深森墨綠防鏽漆板件與沖壓穿孔黃銅壓板扁尾"}
		],
		"chassis": [
			{"id": "chassis_beaver_brass_timber_default", "name_zh": "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體", "desc": "深森墨綠冷軋耐磨板件，金黃黃銅接縫與平整防滑腳掌，敦實水桶腰站姿"}
		]
	},
	"stoat": {
		"id": "stoat",
		"name_zh": "旋刃伶鼬",
		"name_en": "The Whirling Stoat",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/stoat_idle_hd.png",
		"desc": "荒漠舊庫的極速旋刃遊俠，鍍錫象牙白馬口鐵素體，沖壓防沙金屬兜帽與廢土旋刃弧光短匕。",
		"costumes": [
			{"id": "costume_stoat_scavenger_wind_cape", "name_zh": "廢土拾荒輕量防風斗篷", "desc": "多巴胺暖橘滾邊輕量防風斗篷，薄荷綠工具搭扣與多功能拾荒收納腰帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白鍍錫馬口鐵防砂板件與7節同軸彈簧黑尖尾"}
		],
		"chassis": [
			{"id": "chassis_stoat_ivory_tinplate_default", "name_zh": "旋刃伶鼬象牙白馬口鐵防砂素體", "desc": "象牙白鍍錫馬口鐵沖壓板件，黃銅接縫與微型高彈簧球窩關節，敏銳拱背低盤站姿"}
		]
	},
	"seal": {
		"id": "seal",
		"name_zh": "拍浪海豹",
		"name_en": "The Clapping Seal",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/seal_idle_hd.png",
		"desc": "琉璃汪洋的發條拍浪宗師，鍍鈦天藍馬口鐵板件素體，沖壓流體減阻兜帽與琉璃氣動拍浪拳套。",
		"costumes": [
			{"id": "costume_seal_deepsea_diver_harness", "name_zh": "深海武道防壓束帶", "desc": "多巴胺暖橘高抗撕裂加厚潛水束帶，珊瑚粉浮標小球與鍍金海錨金屬搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現鍍鈦天藍馬口鐵防蝕板件與氣動導流雙葉尾鰭"}
		],
		"chassis": [
			{"id": "chassis_seal_marine_titanium_default", "name_zh": "拍浪海豹鍍鈦流線防蝕素體", "desc": "鍍鈦天藍馬口鐵沖壓板件，奶白高溫瓷漆腹部與高密閉防水球窩關節，沉穩流線低盤站姿"}
		]
	},
	"raven": {
		"id": "raven",
		"name_zh": "星儀渡鴉",
		"name_en": "The Armillary Raven",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/raven_idle_hd.png",
		"desc": "黃銅都市的天文觀測法師，黑曜馬口鐵板件素體，天文占星金屬風帽與渾天星儀發條短杖。",
		"costumes": [
			{"id": "costume_raven_horologist_scholar_robe", "name_zh": "鐘錶學者齒輪短披肩", "desc": "多巴胺暖橘高抗撕裂帆布短斗篷，薄荷綠防磨滾邊與六角齒輪領針"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現黑曜白鐵雙色馬口鐵防鏽素體與多節聯動鎢鋼羽翼"}
		],
		"chassis": [
			{"id": "chassis_raven_obsidian_brass_default", "name_zh": "星儀渡鴉黑曜白鐵防鏽馬口鐵素體", "desc": "冷軋沖壓鍍黑曜冷鋼板件，奶油米白烤漆腹板與微型球窩關節，優雅微偏頭觀測立姿"}
		]
	},
	"kite": {
		"id": "kite",
		"name_zh": "熱流赤鳶",
		"name_en": "The Thermal Kite",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/kite_idle_hd.png",
		"desc": "赤焰熔爐的天頂滑翔巡檢遊俠，赤銅馬口鐵板件素體，沖壓猛禽頭罩與熱流淬火複合機關弓。",
		"costumes": [
			{"id": "costume_kite_welder_cape_belt", "name_zh": "阻燃帆布焊接短披風", "desc": "米白耐高溫石棉帆布短披風，亮橘耐火阻燃膠條與游標卡尺腰帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現赤銅黑曜耐熱馬口鐵素體與多節同軸彈簧鋼羽翼"}
		],
		"chassis": [
			{"id": "chassis_kite_copper_obsidian_default", "name_zh": "熱流赤鳶赤銅黑曜耐熱馬口鐵素體", "desc": "冷軋沖壓赤銅鍍層馬口鐵板件，黑曜淬火耐火磚護胸板與密封球窩關節，熱流巡檢微前傾立姿"}
		]
	},
	"swan": {
		"id": "swan",
		"name_zh": "旋音天鵝",
		"name_en": "The Melodic Swan",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/swan_idle_hd.png",
		"desc": "晨曦小鎮大劇院首席皇家近衛騎士，銀白琺瑯馬口鐵素體，八音皇冠護額與八音螺旋穿刺長槍。",
		"costumes": [
			{"id": "costume_swan_theatre_herald_cuirass", "name_zh": "大劇院儀仗近衛胸甲", "desc": "層疊沖壓薄鋼板甲，玫瑰金滾邊胸板與芭蕾金屬裙甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現銀白琺瑯防鏽馬口鐵素體與彈簧鋼羽翼"}
		],
		"chassis": [
			{"id": "chassis_swan_silver_enamel_default", "name_zh": "銀白琺瑯防鏽馬口鐵素體", "desc": "冷軋沖壓薄鋼板外覆銀白琺瑯烤漆，玫瑰金飾條與密封球窩關節，芭蕾挺拔立姿"}
		]
	},
	"bison": {
		"id": "bison",
		"name_zh": "撼地野牛",
		"name_en": "The Groundshaker Bison",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/bison_idle_hd.png",
		"desc": "荒漠齒輪塚舊庫首席拆解工程戰士，生鏽耐磨馬口鐵素體，工字鋼曲角重盔與廢土重砧碎鐵巨鎚。",
		"costumes": [
			{"id": "costume_bison_junkyard_demolition_cuirass", "name_zh": "舊庫拆解工兵重胸甲", "desc": "雙層沖壓生鐵板工裝背帶胸甲，配備多巴胺金黃黃銅大卡扣與防刮裙甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現生鏽耐磨馬口鐵素體與排氣煙囪"}
		],
		"chassis": [
			{"id": "chassis_bison_rusted_tinplate_default", "name_zh": "生鏽耐磨馬口鐵重裝素體", "desc": "沖壓深褐耐磨馬口鐵板覆亮橘防鏽烤漆，高扭力發條駝峰主機艙與密封抗震蹄踏"}
		]
	},
	"gecko": {
		"id": "gecko",
		"name_zh": "巡管守宮",
		"name_en": "The Conduit Gecko",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/gecko_idle_hd.png",
		"desc": "黃銅都市巨輪城管網特工暗忍，冷軋黃銅吸盤素體，管網巡檢防刮護額與黃銅棘輪多角機關鏢。",
		"costumes": [
			{"id": "costume_gecko_highpressure_stealth_harness", "name_zh": "耐熱工裝暗忍胸甲", "desc": "雙層沖壓薄黃銅工裝輕胸甲，配備多巴胺暖金卡扣與防刮金屬裙甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現冷軋黃銅微弧吸盤素體與散熱百葉槽"}
		],
		"chassis": [
			{"id": "chassis_gecko_brass_patina_default", "name_zh": "冷軋黃銅微弧吸盤素體", "desc": "冷軋薄黃銅板覆薄荷綠銅抗氧化琺瑯漆，四足微型間歇吸盤金屬爪與齒輪平衡尾"}
		]
	},
	"badger": {
		"id": "badger",
		"name_zh": "破星蜜獾",
		"name_en": "The Starbreaker Honey Badger",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/badger_idle_hd.png",
		"desc": "星穹軌道外星基地無畏前鋒武道家，高密度聚合物平頭抗衝擊素體，平頭防暴沖壓護額與逐星裂空機關爪。",
		"costumes": [
			{"id": "costume_badger_eva_heavy_harness", "name_zh": "軌道高抗衝擊防護工裝", "desc": "雙層加厚高密度聚合物胸甲，配備多巴胺暖金卡扣與防撞護肩"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現高密度聚合物平頭抗衝擊素體與象牙白隆脊板"}
		],
		"chassis": [
			{"id": "chassis_badger_polymer_space_default", "name_zh": "高密度聚合物平頭抗衝擊素體", "desc": "工程聚合物塑料模組覆深空消光曜黑塗層，背部嵌裝象牙白消光隆脊板件"}
		]
	},
	"capybara": {
		"id": "capybara",
		"name_zh": "澄心水豚",
		"name_en": "The Serene Capybara",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/capybara_idle_hd.png",
		"desc": "天元竹林道場禪意護盾法師，溫潤青瓷椴木禪意底盤，天元禪修竹笠斗笠與澄心太極護體靈晶。",
		"costumes": [
			{"id": "costume_capybara_tea_ceremony_wrap", "name_zh": "道場茶道防塵練功袍", "desc": "雙層加厚靛藍與米白粗麻禪袍，飾以暖金滾邊與多巴胺珊瑚粉茶道編織結"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現溫潤青瓷椴木禪意底盤與高透石英機芯視窗"}
		],
		"chassis": [
			{"id": "chassis_capybara_porcelain_timber_default", "name_zh": "溫潤青瓷椴木禪意底盤", "desc": "象牙米白青瓷板件與打磨椴木複合榫卯結構，腹部嵌裝高透石英視窗可見黃銅平衡陀"}
		]
	},
	"woodpecker": {
		"id": "woodpecker",
		"name_zh": "振律啄木鳥",
		"name_en": "The Resonance Woodpecker",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/woodpecker_idle_hd.png",
		"desc": "巨輪城摩天工坊高空巡檢火槍遊俠，鍍鎳鐵皮黃銅高剛性素體底盤，振律多巴胺亮紅散熱冠羽頭盔與振律重型氣動火銃。",
		"costumes": [
			{"id": "costume_woodpecker_skyspire_inspector_harness", "name_zh": "摩天工坊高空巡檢鉚接工裝", "desc": "雙層深灰耐磨帆布背帶與沖壓加固黃銅護胸板，飾有多巴胺亮橘防墜反光標識"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現鍍鎳薄鐵皮與鑄造黃銅素體底盤與高透石英機芯視窗"}
		],
		"chassis": [
			{"id": "chassis_woodpecker_tinplate_brass_default", "name_zh": "鍍鎳鐵皮黃銅高剛性素體底盤", "desc": "沖壓薄鋼板鍍鎳鏡面處理搭配鑄造黃銅骨架，腹部嵌圓形高透石英視窗"}
		]
	},
	"armadillo": {
		"id": "armadillo",
		"name_zh": "熔鎧犰狳",
		"name_en": "The Crucible Armadillo",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/armadillo_idle_hd.png",
		"desc": "赤焰熔爐鍛造神壇重裝板甲騎士，耐火鑄鐵球鉸素體底盤，黑曜淬火面甲頭盔與玄鐵重破大劍。",
		"costumes": [
			{"id": "costume_armadillo_foundry_anvil_cuirass", "name_zh": "熔爐鐵砧重裝板甲", "desc": "雙層沖壓鑄鐵護胸板與厚帆布隔熱襯墊，外鑲暖金黃銅防撞護角"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現消光黑曜鑄鐵與黃銅球鉸素體底盤與高透石英機芯視窗"}
		],
		"chassis": [
			{"id": "chassis_armadillo_crucible_iron_default", "name_zh": "耐火鑄鐵球鉸素體底盤", "desc": "高耐熱鑄鐵球鉸底盤搭配黃銅關節環，腹部包覆耐熱象牙白陶瓷隔熱層"}
		]
	},
	"caterpillar": {
		"id": "caterpillar",
		"name_zh": "風箱毛蟲",
		"name_en": "The Bellows Caterpillar",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/caterpillar_idle_hd.png",
		"desc": "翡翠深林發條蔓谷重裝工兵戰士，多節沖壓銅環風箱底盤，雙探針風箱護額頭盔與蔓谷風箱重壓鎚。",
		"costumes": [
			{"id": "costume_caterpillar_deepwood_sapper_cuirass", "name_zh": "蔓谷深林工兵板甲", "desc": "雙層熟褐帆布襯墊與沖壓銅護胸，外鑲天元金防撞包角與多巴胺亮橘安全扣帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現多節沖壓薄銅環片與墨綠摺疊皮革風箱素體底盤"}
		],
		"chassis": [
			{"id": "chassis_caterpillar_brass_bellows_default", "name_zh": "多節沖壓銅環風箱底盤", "desc": "六節同軸沖壓薄銅環片夾層墨綠摺疊風箱，腹底嵌裝雙排微型防滑棘輪滾足"}
		]
	},
	"cuttlefish": {
		"id": "cuttlefish",
		"name_zh": "墨影烏賊",
		"name_en": "The Inksmoke Cuttlefish",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/cuttlefish_idle_hd.png",
		"desc": "琉璃汪洋發條海淵暗影刺客，鍍鈦海藍搪瓷底盤，深潛圓頂頭盔、海淵墨影雙鋒匕與氣動發煙墨囊氣罐。",
		"costumes": [
			{"id": "costume_cuttlefish_abyssal_shinobi_cuirass", "name_zh": "海淵夜行輕量耐壓背心", "desc": "深海耐磨海軍藍浸膠帆布與天藍沖壓胸甲，薄荷綠防撞包角"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現鍍鈦合金與琉璃海藍搪瓷素體底盤"}
		],
		"chassis": [
			{"id": "chassis_cuttlefish_abyssal_cyan_default", "name_zh": "鍍鈦合金與琉璃海藍搪瓷素體底盤", "desc": "高抗壓防腐鍍鈦薄板外殼嵌合象牙白防滑陶瓷釉襯板，四對分節軟鋼機械觸肢滾足"}
		]
	},
	"crab": {
		"id": "crab",
		"name_zh": "熔砧石蟹",
		"name_en": "The Anvil Crab",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/crab_idle_hd.png",
		"desc": "赤焰熔爐鍛造火山近身武道家，沖壓鑄鐵矮萌甲殼，雙向潛望測距頭盔、黑曜衝壓熔岩拳套與雙聯氣動排煙煙囪。",
		"costumes": [
			{"id": "costume_crab_furnace_sapper_cuirass", "name_zh": "熔爐工兵重裝石磚胸甲", "desc": "黑曜石淬火磚紋胸甲，赤焰暖橘防撞條與黃銅鍛造鉚釘"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現鑄鐵鍛爐矮萌甲殼素體底盤"}
		],
		"chassis": [
			{"id": "chassis_crab_molten_iron_default", "name_zh": "鑄鐵鍛爐矮萌甲殼素體底盤", "desc": "沖壓粗獷鑄鐵板件嵌合象牙白耐火陶瓷釉板，三對同軸黃銅步進滾足與耐磨橡膠爪"}
		]
	},
	"camel": {
		"id": "camel",
		"name_zh": "日晷駱駝",
		"name_en": "The Sundial Camel",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/camel_idle_hd.png",
		"desc": "荒漠齒輪塚星象法師，沖壓耐磨馬口鐵雙峰底盤，日晷晷針兜帽、廢土日晷折射短杖與雙聯散熱油壺駝峰。",
		"costumes": [
			{"id": "costume_camel_scavenger_astronomer_robe", "name_zh": "廢土觀星學者帆布補丁長袍", "desc": "多色拼接帆布長袍，暖橘與芥末金黃，手作補丁與黃銅小鈴鐺"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現磨砂馬口鐵雙峰矮萌素體底盤"}
		],
		"chassis": [
			{"id": "chassis_camel_sanded_tinplate_default", "name_zh": "磨砂馬口鐵雙峰矮萌素體底盤", "desc": "沖壓耐磨馬口鐵板件邊緣暖金黃銅包邊，四足防滑橡膠馬蹄與微型螺旋彈簧"}
		]
	},
	"giraffe": {
		"id": "giraffe",
		"name_zh": "鐘塔長頸鹿",
		"name_en": "The Belfry Giraffe",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/giraffe_idle_hd.png",
		"desc": "晨曦小鎮懸吊鐘樓天軌守望遊俠，沖壓馬口鐵打磨胡桃木拼花矮萌底盤，三節黃銅伸縮頸管、晨曦禮賓防風呢絨斗篷與鐘樓天弦複合機關弓。",
		"costumes": [
			{"id": "costume_giraffe_dawn_herald_woolen_cape", "name_zh": "晨曦禮賓防風呢絨斗篷披肩", "desc": "多巴胺晨曦暖橘與奶油米白雙色呢絨披肩，黃銅雙聯排扣與精紡金線滾邊"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓馬口鐵胡桃拼花矮萌底盤"}
		],
		"chassis": [
			{"id": "chassis_giraffe_sanded_tinplate_default", "name_zh": "沖壓馬口鐵胡桃拼花矮萌底盤", "desc": "沖壓薄馬口鐵板件嵌合打磨胡桃木拼花，下身配置粗短圓柱形步進腿與多層階梯式黃銅防滑蹄"}
		]
	},
	"hippo": {
		"id": "hippo",
		"name_zh": "重閥河馬",
		"name_en": "The Steamvalve Hippo",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/hippo_idle_hd.png",
		"desc": "巨輪城防衛者與鋼鐵壁壘騎士，沖壓厚鑄黃銅鎢鋼矮萌底盤，雙聯旋轉洩壓安全閥門耳、抗震高壓鉚釘胸甲與重閥活塞衝刺長槍。",
		"costumes": [
			{"id": "costume_hippo_greatcog_high_pressure_cuirass", "name_zh": "巨輪城重裝抗震高壓鉚釘胸甲", "desc": "多巴胺巨輪暖橘厚鑄黃銅防護胸甲，冷軋鎢鋼排扣與珊瑚粉應急手動洩壓拉環"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓厚鑄黃銅鎢鋼矮萌底盤"}
		],
		"chassis": [
			{"id": "chassis_hippo_thick_cast_brass_default", "name_zh": "沖壓厚鑄黃銅鎢鋼矮萌底盤", "desc": "沖壓厚鑄耐壓黃銅板件包覆冷軋鎢鋼框架，四足圓柱形活塞避震腿與加厚黃銅防滑蹄蓋"}
		]
	},
	"mole": {
		"id": "mole",
		"name_zh": "星岩鼴鼠",
		"name_en": "The Asteroid Mole",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/mole_idle_hd.png",
		"desc": "高軌空間站採礦工程師與鋼鐵重裝戰士，乳白工程塑料合金採礦爪矮萌底盤，雙聯超導微型雷達葉片耳、防護工裝背帶褲與專屬星穹高頻等離子重鎚。",
		"costumes": [
			{"id": "costume_mole_orbital_sapper_dungarees", "name_zh": "軌道高抗衝擊防護工裝背帶褲", "desc": "多巴胺天藍高強度防護背帶工裝褲，薄荷綠螢光安全指示帶與黃銅快拆卡扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現乳白高密度工程塑料合金採礦爪底盤"}
		],
		"chassis": [
			{"id": "chassis_mole_milky_polymer_default", "name_zh": "乳白工程塑料合金採礦爪矮萌底盤", "desc": "高密度乳白工程塑料板件包覆冷軋鎢鋼框架，重型沖壓合金多齒採礦爪與四足防滑矽膠吸盤"}
		]
	},
	"petaurista": {
		"id": "petaurista",
		"name_zh": "嵐翼鼯鼠",
		"name_en": "The Stormwing Petaurista",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/petaurista_idle_hd.png",
		"desc": "天元竹林機關滑翔暗忍，溫潤象牙白瓷面甲配生漆打磨竹木拼花底盤，雙聯薄竹葉聲納收音耳、天元竹林摺疊翼膜暗忍胸甲與專屬竹影八卦旋刃機關鏢。",
		"costumes": [
			{"id": "costume_petaurista_folding_glider_wing_harness", "name_zh": "天元竹林摺疊翼膜暗忍胸甲", "desc": "多巴胺薄荷竹翠綠摺疊竹篾滑翔翼膜胸甲，黃銅活動鉸鏈與快拆胸扣帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白瓷與生漆竹木拼花底盤"}
		],
		"chassis": [
			{"id": "chassis_petaurista_lacquered_bamboo_default", "name_zh": "生漆竹木拼花矮萌底盤", "desc": "高溫燒製象牙白瓷板件與打磨椴木骨架，精工黃銅球形鉸鏈與四足防滑橡膠軟墊"}
		]
	},
	"lynx": {
		"id": "lynx",
		"name_zh": "提線猞猁",
		"name_en": "The Marionette Lynx",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/lynx_idle_hd.png",
		"desc": "晨曦小鎮木偶集市提線武道家，拋光胡桃木底盤配象牙白瓷面甲，雙聯黃銅金屬絲天線天籟耳簇、晨曦小鎮提線雜技工裝背心與專屬晨曦提線裂空機關爪。",
		"costumes": [
			{"id": "costume_lynx_marionette_acrobat_vest", "name_zh": "晨曦小鎮提線雜技工裝背心", "desc": "多巴胺暖橘彩漆與精梳蜂蠟提線雜技工裝背心，外露黃銅滑輪與快拆胸扣帶"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現拋光胡桃木雕刻與象牙白瓷底盤"}
		],
		"chassis": [
			{"id": "chassis_lynx_marionette_walnut_default", "name_zh": "提線木偶精雕胡桃木矮萌底盤", "desc": "百年陳化拋光胡桃木雕刻板件與象牙白瓷胸腹襯板，精工黃銅球窩鉸鏈與四足防滑橡膠軟墊"}
		]
	},
	"scarab": {
		"id": "scarab",
		"name_zh": "黑曜金龜",
		"name_en": "The Obsidian Scarab",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/scarab_idle_hd.png",
		"desc": "赤焰熔爐鍛造火山黑曜法師，粗砂鑄鐵底盤配象牙白瓷腮板，雙叉黃銅金角面罩、赤焰熔爐隔熱工匠護裙與專屬赤焰黑曜護體靈晶。",
		"costumes": [
			{"id": "costume_scarab_crucible_artisan_apron", "name_zh": "赤焰熔爐隔熱工匠護裙", "desc": "多巴胺暖橘彩釉厚帆布隔熱工匠護裙，領口薄荷綠密封飾條與黃銅排扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現淬火黑曜石陶瓷與粗砂鑄鐵底盤"}
		],
		"chassis": [
			{"id": "chassis_scarab_obsidian_forge_default", "name_zh": "黑曜耐火鑄鐵矮萌底盤", "desc": "高耐熱粗砂鑄鐵外殼配象牙白瓷耐火腮板，精工黃銅球窩鉸鏈與六足防滑橡膠軟墊"}
		]
	},
	"toucan": {
		"id": "toucan",
		"name_zh": "彩喙巨嘴鳥",
		"name_en": "The Prism-Bill Toucan",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/toucan_idle_hd.png",
		"desc": "翡翠深林高空光學遊俠，沖壓薄銅板輕量化合金底盤配象牙白瓷喉胸板，彩晶折光巨嘴面罩、蔓谷探險巡林獵裝與專屬林冠聚能氣動銃。",
		"costumes": [
			{"id": "costume_toucan_vine_valley_scout_harness", "name_zh": "蔓谷探險巡林獵裝", "desc": "多巴胺薄荷淺綠耐磨帆布巡林短馬甲，飾落日暖橘防風滾邊與黃銅排扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓雕花薄銅板與輕量化合金骨架底盤"}
		],
		"chassis": [
			{"id": "chassis_toucan_canopy_alloy_default", "name_zh": "林冠輕量化合金素體底盤", "desc": "輕量化鋁合金骨架配象牙白瓷喉胸板，精工黃銅三叉鳥爪與橡膠防滑抓握墊"}
		]
	},
	"walrus": {
		"id": "walrus",
		"name_zh": "破冰海象",
		"name_en": "The Icebreaker Walrus",
		"archetype": "騎士 (Knight)",
		"thumb": "res://assets/sprites/player/showcase/walrus_idle_hd.png",
		"desc": "琉璃汪洋海淵守護騎士，沖壓耐壓鍍鈦合金底盤配象牙白瓷腹板，雙聯鎢鋼長牙面罩、深淵領航雙排扣水手胸甲與專屬深淵破冰海軍短闊劍。",
		"costumes": [
			{"id": "costume_walrus_abyssal_peacoat_cuirass", "name_zh": "深淵領航雙排扣水手胸甲", "desc": "多巴胺天藍防寒防水呢絨雙排扣水手胸甲，飾落日暖橘防風滾邊與黃銅海錨扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓耐壓鍍鈦合金底盤與象牙白瓷護板"}
		],
		"chassis": [
			{"id": "chassis_walrus_icebreaker_alloy_default", "name_zh": "深淵耐壓鍍鈦合金底盤", "desc": "耐壓鍍鈦合金骨架配象牙白瓷腹板，厚實金屬腳蹼與防滑橡膠抓握墊"}
		]
	},
	"takin": {
		"id": "takin",
		"name_zh": "破竹羚牛",
		"name_en": "The Bamboo-Cleaving Takin",
		"archetype": "戰士 (Viking)",
		"thumb": "res://assets/sprites/player/showcase/takin_idle_hd.png",
		"desc": "竹影道場天元竹林拓荒戰士，青古銅鑄鐵重裝底盤配象牙白瓷護腹板，黃銅反曲扭角重盔、天元拓荒道袍重肩甲與專屬天元破竹開山巨斧。",
		"costumes": [
			{"id": "costume_takin_zen_pioneer_heavy_robe", "name_zh": "天元拓荒道袍重肩甲", "desc": "多巴胺奶油白與落日暖橘防磨滾邊道袍重肩甲，飾天元金黃銅鈕扣與減震閥"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現沖壓青古銅鑄鐵合金底盤與象牙白瓷護腹板"}
		],
		"chassis": [
			{"id": "chassis_takin_bronze_cast_default", "name_zh": "青古銅鑄鐵重裝底盤", "desc": "青古銅鑄鐵合金厚重骨架配象牙白瓷護板，防滑青石蹄與球形轉向鉸鏈"}
		]
	},
	"lemur": {
		"id": "lemur",
		"name_zh": "星環狐猴",
		"name_en": "The Star-Ring Lemur",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/lemur_idle_hd.png",
		"desc": "星穹軌道外星基地高機動忍者，象牙白工程聚合物底盤配冷光雷達耳罩面甲、琥珀脈衝星穹雙目鏡與專屬星軌脈衝雙鋒短匕。",
		"costumes": [
			{"id": "costume_lemur_astro_stealth_harness", "name_zh": "宇航匿蹤輕量安全吊帶胸甲", "desc": "多巴胺天藍金屬編織尼龍與暖橘反光條輕甲，配備四枚微型冷氣向量反推噴嘴"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白高抗衝擊工程聚合物底盤與導電矽膠防滑墊"}
		],
		"chassis": [
			{"id": "chassis_lemur_orbit_polymer_default", "name_zh": "星穹輕量聚合物高機動底盤", "desc": "象牙白工程塑料外殼配自潤滑尼龍球鉸，雙手掌底與足底嵌導電矽膠吸附墊"}
		]
	},
	"marmot": {
		"id": "marmot",
		"name_zh": "碎石旱獺",
		"name_en": "The Rockbreaker Marmot",
		"archetype": "武術家 (Monk)",
		"thumb": "res://assets/sprites/player/showcase/marmot_idle_hd.png",
		"desc": "荒漠齒輪塚遺忘舊庫破障武術家，沖壓生鐵馬口鐵耐磨底盤配合金鑿齒面罩、雙聯琥珀風鏡與專屬廢土偏心衝壓機關拳套。",
		"costumes": [
			{"id": "costume_marmot_scavenger_canvas_harness", "name_zh": "舊庫拾荒加固帆布工裝胸甲", "desc": "耐磨帆布配鍍鋅護胸鐵板，飾以暖金黃與落日暖橘警示斜紋"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現生鐵青灰沖壓耐磨馬口鐵底盤與黃銅抓地鉚釘足底"}
		],
		"chassis": [
			{"id": "chassis_marmot_quarry_tinplate_default", "name_zh": "碎石耐磨馬口鐵底盤", "desc": "沖壓生鐵青灰外殼配奶油米白隔震襯板，冷軋鎢鋼自潤滑球鉸與黃銅抓地鉚釘足底"}
		]
	},
	"firefly": {
		"id": "firefly",
		"name_zh": "靈燈飛螢",
		"name_en": "The Lantern Firefly",
		"archetype": "法師 (Mage)",
		"thumb": "res://assets/sprites/player/showcase/firefly_idle_hd.png",
		"desc": "翡翠深林發條蔓谷靈光法師，沖壓薄銅馬口鐵底盤配雙聯微調黃銅觸角、聚碳酸酯夜燈目鏡與專屬深林熒光藤蔓發條長杖。",
		"costumes": [
			{"id": "costume_firefly_vine_harness_cuirass", "name_zh": "藤蔓工裝編織輕量背心胸甲", "desc": "輕量金屬藤蔓編織背心，配薄銅護胸與快拆金屬扣，飾以天藍與落日暖橘警示條"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現薄荷綠沖壓薄銅深林耐磨板件與象牙白絕緣底板"}
		],
		"chassis": [
			{"id": "chassis_firefly_emerald_tinplate_default", "name_zh": "深林沖壓薄銅馬口鐵底盤", "desc": "沖壓薄銅深林耐磨烤漆板件配象牙白絕緣底板，黃銅球窩關節與防滑橡膠吸附減震墊"}
		]
	},
	"manta": {
		"id": "manta",
		"name_zh": "潮汐蝠魟",
		"name_en": "The Tidal Manta",
		"archetype": "遊俠 (Ranger)",
		"thumb": "res://assets/sprites/player/showcase/manta_idle_hd.png",
		"desc": "琉璃汪洋發條海淵穿浪遊俠，沖壓鍍鈦底盤配雙聯導流頭角、耐高壓石英目鏡與專屬海淵流體脈衝複合機關弓。",
		"costumes": [
			{"id": "costume_manta_diver_harness_cuirass", "name_zh": "深海潛水工裝編織輕量胸甲", "desc": "輕量金屬編織背心，配鍍鈦護胸與洩壓閥卡扣，飾以天元金黃與落日暖橘警示條"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現天藍沖壓耐蝕鍍鈦金屬板件與奶油米白絕緣底板"}
		],
		"chassis": [
			{"id": "chassis_manta_titanium_default", "name_zh": "深海沖壓耐蝕鍍鈦金屬底盤", "desc": "沖壓耐蝕鍍鈦金屬深海防鏽烤漆板件配奶油米白抗壓底板，黃銅球窩關節與防滑橡膠吸附墊"}
		]
	}
}

const RACE_KEYS: Array[String] = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "crane", "bear", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "kangaroo", "squirrel", "salamander", "viper", "falcon", "ram", "chameleon", "sailfish", "rhino", "bat", "gorilla", "peacock", "meerkat", "courser", "beaver", "stoat", "seal", "raven", "kite", "swan", "bison", "gecko", "badger", "capybara", "woodpecker", "armadillo", "caterpillar", "cuttlefish", "crab", "camel", "giraffe", "hippo", "mole", "petaurista", "lynx", "scarab", "toucan", "walrus", "takin", "lemur", "marmot", "firefly", "manta"]

const TAB_LAUNCH := "launch"
const TAB_EXPANSION := "expansion"

const LAUNCH_RACES: Array[String] = ["rabbit", "fox", "lion", "boar", "macaque"]
const EXPANSION_RACES: Array[String] = ["tiger", "crane", "bear", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "kangaroo", "squirrel", "salamander", "viper", "falcon", "ram", "chameleon", "sailfish", "rhino", "bat", "gorilla", "peacock", "meerkat", "courser", "beaver", "stoat", "seal", "raven", "kite", "swan", "bison", "gecko", "badger", "capybara", "woodpecker", "armadillo", "caterpillar", "cuttlefish", "crab", "camel", "giraffe", "hippo", "mole", "petaurista", "lynx", "scarab", "toucan", "walrus", "takin", "lemur", "marmot", "firefly", "manta"]

## 判斷種族是否已備齊前端立繪與展示切片資源（零美術佔位防護守衛）
static func has_race_assets(race_id: String) -> bool:
	if not RACES_DATA.has(race_id):
		return false
	var thumb_path: String = str(RACES_DATA[race_id].get("thumb", ""))
	if thumb_path.is_empty() or not (ResourceLoader.exists(thumb_path) or FileAccess.file_exists(thumb_path)):
		return false
	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	if PaperdollRenderer and PaperdollRenderer.has_method("has_race_assets"):
		return PaperdollRenderer.has_race_assets(race_id)
	return true

## 節點引用
@onready var character: PaperdollCharacter = $CenterStage/CharacterContainer/PaperdollCharacter as PaperdollCharacter
@onready var race_buttons_container: HBoxContainer = $TopRaceBar/ButtonsHBox as HBoxContainer
@onready var race_tab_bar: HBoxContainer = get_node_or_null("RaceTabBar") as HBoxContainer
@onready var btn_tab_launch: Button = get_node_or_null("RaceTabBar/BtnTab_launch") as Button
@onready var btn_tab_expansion: Button = get_node_or_null("RaceTabBar/BtnTab_expansion") as Button

@onready var hero_title_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroTitleLabel as Label
@onready var hero_archetype_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroArchetypeLabel as Label
@onready var hero_desc_label: Label = $CenterStage/DescPanel/HeroDescLabel as Label

@onready var costume_name_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeNameLabel as Label
@onready var costume_desc_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeDescLabel as Label
@onready var btn_costume_prev: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumePrev as Button
@onready var btn_costume_next: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumeNext as Button

@onready var chassis_name_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisNameLabel as Label
@onready var chassis_desc_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisDescLabel as Label
@onready var btn_chassis_prev: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisPrev as Button
@onready var btn_chassis_next: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisNext as Button

@onready var weapon_name_label: Label = $RightControlPanel/Margin/VBox/WeaponControl/WeaponDisplay/WeaponNameLabel as Label

@onready var slot_summary_label: Label = $RightControlPanel/Margin/VBox/StatusCard/SlotSummaryLabel as Label
@onready var btn_reset_default: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnResetDefault as Button
@onready var btn_capture_proof: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnCaptureProof as Button

var btn_confirm: Button = null
var btn_back: Button = null

## 執行期狀態
var _current_race_id: String = "rabbit"
var _costume_index: int = 0
var _chassis_index: int = 0
var _race_buttons: Dictionary = {}
var _breathe_tween: Tween = null
var _current_tab: String = TAB_LAUNCH

var _race_filter_chips: Dictionary = {}
var _current_filter_race: String = "all"


func _ready() -> void:
	_init_race_buttons()
	_init_category_tabs()
	_bind_controls()
	_connect_loc_signal()
	_update_creation_mode_ui()
	_update_tab_texts()
	_update_right_panel_labels()
	_update_race_buttons_text()
	switch_tab(TAB_LAUNCH)
	select_race("rabbit")
	_start_breathe_tween()


func _exit_tree() -> void:
	_stop_breathe_tween()
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc := (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc := (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_tab_texts()
	_update_right_panel_labels()
	_update_creation_mode_ui()
	_update_race_buttons_text()
	_apply_current_selections()


func _update_right_panel_labels() -> void:
	var panel_title = get_node_or_null("RightControlPanel/Margin/VBox/PanelTitle") as Label
	if panel_title and is_instance_valid(panel_title):
		panel_title.text = _t("即時換裝控制項 · 模組槽位調配")

	var costume_slot = get_node_or_null("RightControlPanel/Margin/VBox/CostumeControl/SlotLabel") as Label
	if costume_slot and is_instance_valid(costume_slot):
		costume_slot.text = _t("• 外裝服飾槽 (Costume Slot - Z:25)")

	var chassis_slot = get_node_or_null("RightControlPanel/Margin/VBox/ChassisControl/SlotLabel") as Label
	if chassis_slot and is_instance_valid(chassis_slot):
		chassis_slot.text = _t("• 軀體塗裝槽 (Chassis Shell - Z:10)")

	var weapon_slot = get_node_or_null("RightControlPanel/Margin/VBox/WeaponControl/SlotLabel") as Label
	if weapon_slot and is_instance_valid(weapon_slot):
		weapon_slot.text = _t("• 手持武器槽 (Weapon Slot - Z:40)")

	if btn_reset_default and is_instance_valid(btn_reset_default):
		btn_reset_default.text = _t("重設預設")

	if btn_capture_proof and is_instance_valid(btn_capture_proof):
		btn_capture_proof.text = _t("儲存驗證截圖")


func _update_tab_texts() -> void:
	var main_title = get_node_or_null("HeaderBadge/HeaderVBox/MainTitle") as Label
	if main_title and is_instance_valid(main_title):
		main_title.text = _t("發條之心 · 紙娃娃試衣間")
	if btn_tab_launch and is_instance_valid(btn_tab_launch):
		btn_tab_launch.text = _t("首發")
	if btn_tab_expansion and is_instance_valid(btn_tab_expansion):
		btn_tab_expansion.text = _t("擴充")


## 設定種族按鈕內部佈局與自適應邊距
func _setup_race_button_node(btn: Button, rid: String) -> void:
	if btn == null:
		return
	var margin = btn.get_node_or_null("Margin") as MarginContainer
	if margin:
		margin.add_theme_constant_override("margin_left", 10)
		margin.add_theme_constant_override("margin_right", 10)
		margin.add_theme_constant_override("margin_top", 4)
		margin.add_theme_constant_override("margin_bottom", 4)
	var vbox = btn.get_node_or_null("Margin/VBox") as VBoxContainer
	if vbox:
		vbox.add_theme_constant_override("separation", 2)
	var name_lbl = btn.get_node_or_null("Margin/VBox/NameLabel") as Label
	if name_lbl and RACES_DATA.has(rid):
		var rname: String = str(RACES_DATA[rid].get("name_zh", rid))
		_format_race_name_label(name_lbl, _t(rname))


## 種族名稱標籤格式化：啟用智慧詞折行、置中並依文字長度自適應字級，避免溢出碰撞 (0-QA23)
func _format_race_name_label(name_lbl: Label, loc_text: String) -> void:
	if name_lbl == null:
		return
	name_lbl.text = loc_text
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	name_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
	name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_lbl.custom_minimum_size = Vector2(0, 32)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)

	# 字級動態調適：確保在 en/es 語系長譯名下文字安全收納於卡框內，絕不溢出或跨卡重疊
	var tlen := loc_text.length()
	if tlen <= 5:
		name_lbl.add_theme_font_size_override("font_size", 15)
	elif tlen <= 10:
		name_lbl.add_theme_font_size_override("font_size", 13)
	elif tlen <= 20:
		name_lbl.add_theme_font_size_override("font_size", 12)
	else:
		name_lbl.add_theme_font_size_override("font_size", 11)


func _update_race_buttons_text() -> void:
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		if btn and is_instance_valid(btn):
			_setup_race_button_node(btn, rid)


## 初始化橫向種族選擇按鈕
func _init_race_buttons() -> void:
	var template_btn: Button = get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_rabbit") as Button
	for rid in RACE_KEYS:
		var btn_path := "TopRaceBar/ButtonsHBox/BtnRace_" + rid
		var btn: Button = get_node_or_null(btn_path) as Button
		# 若該種族尚無美術立繪與切片資源，前端防護不露出空卡
		if not has_race_assets(rid):
			if btn != null:
				btn.visible = false
			continue
		if btn == null and race_buttons_container != null and template_btn != null:
			# 動態補足新種族按鈕
			btn = template_btn.duplicate() as Button
			btn.name = "BtnRace_" + rid
			var thumb_rect = btn.get_node_or_null("Margin/VBox/Thumb")
			if thumb_rect is TextureRect:
				var thumb_path := str(RACES_DATA[rid].get("thumb", ""))
				if ResourceLoader.exists(thumb_path):
					thumb_rect.texture = load(thumb_path) as Texture2D
				else:
					thumb_rect.texture = null
			var end_spacer = race_buttons_container.get_node_or_null("EndSpacer")
			if end_spacer != null:
				race_buttons_container.add_child(btn)
				race_buttons_container.move_child(end_spacer, -1)
			else:
				race_buttons_container.add_child(btn)
		if btn != null:
			_race_buttons[rid] = btn
			_setup_race_button_node(btn, rid)
			var check_lbl = btn.get_node_or_null("Margin/VBox/CheckLabel")
			if check_lbl is Label:
				check_lbl.text = ""
				check_lbl.visible = false
			var thumb_rect = btn.get_node_or_null("Margin/VBox/Thumb")
			if thumb_rect is TextureRect:
				thumb_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				var thumb_path := str(RACES_DATA[rid].get("thumb", ""))
				if ResourceLoader.exists(thumb_path):
					thumb_rect.texture = load(thumb_path) as Texture2D
				else:
					thumb_rect.texture = null
			btn.pressed.connect(func(): select_race(rid))


## 初始化頂部「首發｜擴充」分頁 tab
func _init_category_tabs() -> void:
	if race_tab_bar == null:
		race_tab_bar = get_node_or_null("RaceTabBar") as HBoxContainer
	if race_tab_bar == null:
		race_tab_bar = HBoxContainer.new()
		race_tab_bar.name = "RaceTabBar"
		race_tab_bar.alignment = BoxContainer.ALIGNMENT_CENTER
		race_tab_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
		race_tab_bar.offset_left = 40.0
		race_tab_bar.offset_top = 64.0
		race_tab_bar.offset_right = -40.0
		race_tab_bar.offset_bottom = 116.0
		race_tab_bar.add_theme_constant_override("separation", 16)
		add_child(race_tab_bar)
		move_child(race_tab_bar, 3)

	if btn_tab_launch == null:
		btn_tab_launch = race_tab_bar.get_node_or_null("BtnTab_launch") as Button
	if btn_tab_launch == null:
		btn_tab_launch = Button.new()
		btn_tab_launch.name = "BtnTab_launch"
		btn_tab_launch.text = "首發"
		btn_tab_launch.custom_minimum_size = Vector2(160, 48)
		btn_tab_launch.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn_tab_launch.add_theme_font_size_override("font_size", 18)
		if ResourceLoader.exists(FONT_PATH):
			btn_tab_launch.add_theme_font_override("font", load(FONT_PATH) as Font)
		race_tab_bar.add_child(btn_tab_launch)

	if btn_tab_expansion == null:
		btn_tab_expansion = race_tab_bar.get_node_or_null("BtnTab_expansion") as Button
	if btn_tab_expansion == null:
		btn_tab_expansion = Button.new()
		btn_tab_expansion.name = "BtnTab_expansion"
		btn_tab_expansion.text = "擴充"
		btn_tab_expansion.custom_minimum_size = Vector2(160, 48)
		btn_tab_expansion.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn_tab_expansion.add_theme_font_size_override("font_size", 18)
		if ResourceLoader.exists(FONT_PATH):
			btn_tab_expansion.add_theme_font_override("font", load(FONT_PATH) as Font)
		race_tab_bar.add_child(btn_tab_expansion)

	if not btn_tab_launch.pressed.is_connected(_on_tab_launch_pressed):
		btn_tab_launch.pressed.connect(_on_tab_launch_pressed)
	if not btn_tab_expansion.pressed.is_connected(_on_tab_expansion_pressed):
		btn_tab_expansion.pressed.connect(_on_tab_expansion_pressed)

	_update_tab_texts()
	_update_tabs_visual()


func _on_tab_launch_pressed() -> void:
	switch_tab(TAB_LAUNCH)


func _on_tab_expansion_pressed() -> void:
	switch_tab(TAB_EXPANSION)


func get_current_tab() -> String:
	return _current_tab


func switch_tab(tab_name: String) -> void:
	if tab_name == "首發" or tab_name == "launch" or tab_name == _t("首發"):
		_current_tab = TAB_LAUNCH
	elif tab_name == "擴充" or tab_name == "expansion" or tab_name == _t("擴充"):
		_current_tab = TAB_EXPANSION
	else:
		_current_tab = TAB_LAUNCH

	_update_tabs_visual()
	_update_race_buttons_visibility()
	_update_race_buttons_visual()

	var scroll := get_node_or_null("TopRaceBar") as ScrollContainer
	if scroll:
		scroll.scroll_horizontal = 0


func _update_race_buttons_visibility() -> void:
	var active_races: Array[String] = LAUNCH_RACES if _current_tab == TAB_LAUNCH else EXPANSION_RACES
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		if btn:
			var is_in_tab: bool = (rid in active_races)
			var has_assets: bool = has_race_assets(rid)
			btn.visible = (is_in_tab and has_assets)


func _update_tabs_visual() -> void:
	if btn_tab_launch == null or btn_tab_expansion == null:
		return
	var is_launch := (_current_tab == TAB_LAUNCH)
	_apply_tab_style(btn_tab_launch, is_launch)
	_apply_tab_style(btn_tab_expansion, not is_launch)


func _apply_tab_style(btn: Button, is_active: bool) -> void:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(16)
	sb.border_color = Color("#1F1A3A") # 深藍紫
	sb.border_width_left = 2
	sb.border_width_top = 2
	sb.border_width_right = 2
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8

	if is_active:
		sb.bg_color = Color("#FFD028") # 多巴胺金黃
		sb.border_width_bottom = 5     # 立體果凍厚底
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		btn.add_theme_color_override("font_color", Color("#1F1A3A"))
	else:
		sb.bg_color = Color("#FFF8E7") # 奶油米白底
		sb.border_width_bottom = 3
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.08)
		sb.shadow_size = 2
		sb.shadow_offset = Vector2(0, 1)
		btn.add_theme_color_override("font_color", Color("#5A5270"))

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = Color("#FFE066") if is_active else Color("#FFF1D6")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = max(1, sb.border_width_bottom - 2)

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)


## 相容舊呼叫介面
func filter_race(race_id: String) -> void:
	if race_id != "all" and RACES_DATA.has(race_id):
		select_race(race_id)


## 綁定控制按鈕
func _bind_controls() -> void:
	if btn_costume_prev != null:
		btn_costume_prev.pressed.connect(_on_costume_prev_pressed)
	if btn_costume_next != null:
		btn_costume_next.pressed.connect(_on_costume_next_pressed)
	if btn_chassis_prev != null:
		btn_chassis_prev.pressed.connect(_on_chassis_prev_pressed)
	if btn_chassis_next != null:
		btn_chassis_next.pressed.connect(_on_chassis_next_pressed)
	if btn_reset_default != null:
		btn_reset_default.pressed.connect(reset_to_default)
	if btn_capture_proof != null:
		btn_capture_proof.pressed.connect(func(): save_proof_screenshot())

	var actions_row = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow")
	if actions_row != null:
		btn_confirm = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnConfirm") as Button
		if btn_confirm == null:
			btn_confirm = Button.new()
			btn_confirm.name = "BtnConfirm"
			btn_confirm.custom_minimum_size = Vector2(160, 52)
			btn_confirm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			btn_confirm.add_theme_font_size_override("font_size", 16)
			btn_confirm.add_theme_color_override("font_color", Color(0.04, 0.22, 0.08, 1.0))
			if btn_capture_proof:
				var sb = btn_capture_proof.get_theme_stylebox("normal")
				if sb:
					btn_confirm.add_theme_stylebox_override("normal", sb.duplicate())
			btn_confirm.text = _t("確認選擇 · 踏上旅途") if creation_mode else _t("確認選擇")
			actions_row.add_child(btn_confirm)
		else:
			btn_confirm.text = _t("確認選擇 · 踏上旅途") if creation_mode else _t("確認選擇")
		if not btn_confirm.pressed.is_connected(confirm_selection):
			btn_confirm.pressed.connect(confirm_selection)

		btn_back = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnBack") as Button
		if btn_back == null:
			btn_back = Button.new()
			btn_back.name = "BtnBack"
			btn_back.custom_minimum_size = Vector2(90, 52)
			btn_back.add_theme_font_size_override("font_size", 16)
			btn_back.add_theme_color_override("font_color", Color(0.12, 0.1, 0.22, 1.0))
			if btn_reset_default:
				var sb = btn_reset_default.get_theme_stylebox("normal")
				if sb:
					btn_back.add_theme_stylebox_override("normal", sb.duplicate())
			btn_back.text = _t("返回")
			btn_back.visible = creation_mode
			actions_row.add_child(btn_back)
		else:
			btn_back.text = _t("返回")
			btn_back.visible = creation_mode
		if not btn_back.pressed.is_connected(_on_back_pressed):
			btn_back.pressed.connect(_on_back_pressed)


func _on_back_pressed() -> void:
	close()


func _update_creation_mode_ui() -> void:
	if btn_confirm and is_instance_valid(btn_confirm):
		btn_confirm.text = _t("確認選擇 · 踏上旅途") if creation_mode else _t("確認選擇")
	if btn_back and is_instance_valid(btn_back):
		btn_back.text = _t("返回")
		btn_back.visible = creation_mode
	if btn_reset_default and is_instance_valid(btn_reset_default):
		btn_reset_default.text = _t("還原預設")
	if btn_capture_proof and is_instance_valid(btn_capture_proof):
		btn_capture_proof.visible = not creation_mode


## 確認選擇並同步寫入 GameState
func confirm_selection() -> void:
	var sel := get_current_selections()
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var gs = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs:
			gs.player_race = _current_race_id
			gs.paperdoll_slots = sel
			match _current_race_id:
				"rabbit": gs.player_name = "小白"
				"lion": gs.player_name = "烈鬃獅"
				"fox": gs.player_name = "靈尾狐"
				"boar": gs.player_name = "鋼牙豕"
				"macaque": gs.player_name = "靈爪猴"
				"tiger": gs.player_name = "烈焰虎"
				"bear": gs.player_name = "玄軸熊"
				"crane": gs.player_name = "雲嵐鶴"
				"penguin": gs.player_name = "蒸氣企鵝"
				"tortoise": gs.player_name = "玄機龜"
				"elephant": gs.player_name = "鋼岳象"
				"frog": gs.player_name = "碧簧蛙"
				"panda": gs.player_name = "瓷韻熊貓"
				"fawn": gs.player_name = "翠角鹿"
				"hound": gs.player_name = "星軌犬"
				"owl": gs.player_name = "靈鐘鴞"
				"cat": gs.player_name = "幽影貓"
				"pangolin": gs.player_name = "沙鱗穿山甲"
				"otter": gs.player_name = "浪花海獺"
				"raccoon": gs.player_name = "星巡浣熊"
				"hedgehog": gs.player_name = "棘輪刺蝟"
				"wolf": gs.player_name = "荒原鋼狼"
				"seahorse": gs.player_name = "琉璃海馬"
				"kangaroo": gs.player_name = "鐵拳袋鼠"
				"squirrel": gs.player_name = "巡林松鼠"
				"salamander": gs.player_name = "熔火蜥蜴"
				"viper": gs.player_name = "竹影青蛇"
				"falcon": gs.player_name = "疾影神隼"
				"ram": gs.player_name = "星盤靈羊"
				"chameleon": gs.player_name = "幻彩變色龍"
				"sailfish": gs.player_name = "破浪旗魚"
				"rhino": gs.player_name = "重角犀牛"
				"bat": gs.player_name = "星翼蝙蝠"
				"gorilla": gs.player_name = "鋼臂巨猩"
				"peacock": gs.player_name = "稜鏡孔雀"
				"meerkat": gs.player_name = "沙哨狐獴"
				"courser": gs.player_name = "鐵蹄駿駒"
				"beaver": gs.player_name = "劈木河狸"
				"stoat": gs.player_name = "旋刃伶鼬"
				"seal": gs.player_name = "拍浪海豹"
				"raven": gs.player_name = "星儀渡鴉"
				"kite": gs.player_name = "熱流赤鳶"
				"swan": gs.player_name = "旋音天鵝"
				"bison": gs.player_name = "撼地野牛"
				"gecko": gs.player_name = "巡管守宮"
				"badger": gs.player_name = "破星蜜獾"
				"capybara": gs.player_name = "澄心水豚"
				"woodpecker": gs.player_name = "振律啄木鳥"
				"armadillo": gs.player_name = "熔鎧犰狳"
				"caterpillar": gs.player_name = "風箱毛蟲"
				"cuttlefish": gs.player_name = "墨影烏賊"
				"crab": gs.player_name = "熔砧石蟹"
				"camel": gs.player_name = "日晷駱駝"
				"giraffe": gs.player_name = "鐘塔長頸鹿"
				"hippo": gs.player_name = "重閥河馬"
				"mole": gs.player_name = "星岩鼴鼠"
				"petaurista": gs.player_name = "嵐翼鼯鼠"
				"lynx": gs.player_name = "提線猞猁"
				"scarab": gs.player_name = "黑曜金龜"
				"toucan": gs.player_name = "彩喙巨嘴鳥"
				"walrus": gs.player_name = "破冰海象"
				"takin": gs.player_name = "破竹羚牛"
				"lemur": gs.player_name = "星環狐猴"
				"marmot": gs.player_name = "碎石旱獺"
				"firefly": gs.player_name = "靈燈飛螢"
				"manta": gs.player_name = "潮汐蝠魟"
				_: gs.player_name = "小白"
			if gs.has_method("equip_starter_weapon"):
				gs.call("equip_starter_weapon", _current_race_id)
	character_confirmed.emit(_current_race_id, sel)


## 選取指定種族
func select_race(race_id: String) -> void:
	if not RACES_DATA.has(race_id) or not has_race_assets(race_id):
		race_id = "rabbit"
	_current_race_id = race_id
	_costume_index = 0
	_chassis_index = 0

	if race_id in LAUNCH_RACES and _current_tab != TAB_LAUNCH:
		switch_tab(TAB_LAUNCH)
	elif race_id in EXPANSION_RACES and _current_tab != TAB_EXPANSION:
		switch_tab(TAB_EXPANSION)
	else:
		_update_race_buttons_visual()

	_apply_current_selections()


## 左右切換外裝
func _on_costume_prev_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index - 1 + costumes.size()) % costumes.size()
	_apply_current_selections()


func _on_costume_next_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index + 1) % costumes.size()
	_apply_current_selections()


## 左右切換塗裝
func _on_chassis_prev_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index - 1 + chassis_list.size()) % chassis_list.size()
	_apply_current_selections()


func _on_chassis_next_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index + 1) % chassis_list.size()
	_apply_current_selections()


## 重設為當前種族預設裝備
func reset_to_default() -> void:
	_costume_index = 0
	_chassis_index = 0
	_apply_current_selections()


## 套用並重新渲染紙娃娃
func _get_character() -> PaperdollCharacter:
	if character == null:
		character = get_node_or_null("CenterStage/CharacterContainer/PaperdollCharacter") as PaperdollCharacter
	return character

func _apply_current_selections() -> void:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}

	var selections: Dictionary = {}
	if cur_costume.has("id"):
		selections["costume"] = cur_costume["id"]
	if cur_chassis.has("id"):
		selections["chassis"] = cur_chassis["id"]

	# 驅動紙娃娃節點渲染
	var ch := _get_character()
	if ch != null:
		ch.render_character(_current_race_id, selections)

	# 中央舞台九族改讀 512 高清合成（合成失敗改讀立牌／showcase 256，不退回 128）
	_update_stage_512(selections)

	# 更新 UI 顯示文字與標記
	_update_info_ui(data, cur_costume, cur_chassis, selections)


var _sprite_512: Sprite2D = null
var force_composite_512_fail: bool = false

func _ensure_stage_sprite_512() -> void:
	if _sprite_512 != null and is_instance_valid(_sprite_512):
		return
	var ch := _get_character()
	if ch == null:
		return
	_sprite_512 = ch.get_node_or_null("Sprite512") as Sprite2D
	if _sprite_512 == null:
		_sprite_512 = Sprite2D.new()
		_sprite_512.name = "Sprite512"
		_sprite_512.centered = false
		_sprite_512.position = Vector2(-64, -120)
		_sprite_512.scale = Vector2(0.25, 0.25)
		_sprite_512.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		ch.add_child(_sprite_512)

func _update_stage_512(selections: Dictionary) -> void:
	var ch := _get_character()
	if ch == null:
		return
	_ensure_stage_sprite_512()

	var tex_512: Texture2D = null
	if not force_composite_512_fail:
		tex_512 = PaperdollRenderer.build_composite_texture_512(_current_race_id, selections)
		if tex_512 == null:
			var idle_candidate: Texture2D = SpriteDB.player_equipped_idle(_current_race_id, selections)
			if idle_candidate != null and idle_candidate.get_width() >= 256:
				tex_512 = idle_candidate

	# 合成失敗改讀官方立牌或本族 showcase idle 256，不准退回 128 模組切片 (0-ART26)
	if tex_512 == null or tex_512.get_width() < 256:
		var sc := SpriteDB.hero_showcase_hd_tex(_current_race_id)
		if sc != null and sc.get_width() >= 256:
			tex_512 = sc

	var layers := ch.get_node_or_null("Layers") as CanvasItem
	if tex_512 != null and tex_512.get_width() >= 256:
		_sprite_512.texture = tex_512
		_sprite_512.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var tw := float(tex_512.get_width())
		var th := float(tex_512.get_height())
		var s := 128.0 / tw if tw > 0.0 else 0.25
		_sprite_512.scale = Vector2(s, s)
		_sprite_512.position = Vector2(-64.0, 8.0 - th * s)
		_sprite_512.visible = true
		if layers != null:
			layers.visible = false
	else:
		_sprite_512.texture = null
		_sprite_512.visible = false
		if layers != null:
			layers.visible = false

func get_stage_texture() -> Texture2D:
	if _sprite_512 != null and _sprite_512.visible and _sprite_512.texture != null:
		return _sprite_512.texture
	return null

func get_stage_sprite_512() -> Sprite2D:
	return _sprite_512

func is_stage_512() -> bool:
	var t := get_stage_texture()
	return t != null and t.get_width() >= 256


## 更新 UI 資訊
func _update_info_ui(race_data: Dictionary, cur_costume: Dictionary, cur_chassis: Dictionary, selections: Dictionary = {}) -> void:
	var name_zh: String = str(race_data.get("name_zh", ""))
	var name_en: String = str(race_data.get("name_en", ""))
	var archetype: String = str(race_data.get("archetype", ""))
	var desc: String = str(race_data.get("desc", ""))

	var loc_name := _t(name_zh)
	if hero_title_label != null:
		if ContentLoc.locale() == "zh_TW":
			hero_title_label.text = "%s (%s)" % [name_zh, name_en]
		else:
			if loc_name != name_zh and loc_name != name_en:
				hero_title_label.text = "%s (%s)" % [loc_name, name_en]
			else:
				hero_title_label.text = loc_name

	if hero_archetype_label != null:
		if archetype == "未定案":
			hero_archetype_label.text = "【%s】" % _t("未定案")
		elif archetype.is_empty():
			hero_archetype_label.text = ""
		else:
			var arch_key := archetype
			if "(" in arch_key:
				arch_key = arch_key.split("(")[0].strip_edges()
			var loc_arch := _t(arch_key)
			if ContentLoc.locale() == "zh_TW":
				hero_archetype_label.text = "【%s】" % archetype
			else:
				hero_archetype_label.text = "【%s】" % loc_arch

	if hero_desc_label != null:
		hero_desc_label.text = _t(desc)

	# 外裝顯示
	if costume_name_label != null:
		var c_id := str(cur_costume.get("id", "none"))
		var c_name := get_variant_spec_name(c_id, str(cur_costume.get("name_zh", "未裝備")))
		var loc_c_name := _t(c_name)
		costume_name_label.text = "%s [%s]" % [loc_c_name, c_id]
	if costume_desc_label != null:
		costume_desc_label.text = _t(str(cur_costume.get("desc", "標準外觀")))

	# 塗裝顯示
	if chassis_name_label != null:
		var ch_id := str(cur_chassis.get("id", "paint_ivory_stock"))
		var ch_name := get_variant_spec_name(ch_id, str(cur_chassis.get("name_zh", "原廠塗裝")))
		var loc_ch_name := _t(ch_name)
		chassis_name_label.text = "%s [%s]" % [loc_ch_name, ch_id]
	if chassis_desc_label != null:
		chassis_desc_label.text = _t(str(cur_chassis.get("desc", "外殼拋光烤漆")))

	# 武器顯示
	if weapon_name_label != null:
		var default_wpn := str(PaperdollRenderer._get_default_variant_id(_current_race_id, "weapon"))
		var wpn_name := get_variant_spec_name(default_wpn, default_wpn)
		var loc_wpn := _t(wpn_name)
		weapon_name_label.text = "%s (%s)" % [loc_wpn, default_wpn]

	# 槽位總結
	if slot_summary_label != null:
		var total_slots := 7
		var loaded_count := 0
		if is_stage_512():
			var entries := PaperdollRenderer.get_sorted_slot_entries_512(_current_race_id, selections)
			for e in entries:
				var p: String = str(e.get("texture_path", ""))
				if p != "" and bool(e.get("is_loaded", false)):
					loaded_count += 1
			var fmt_512 := _t("7 大槽位狀態：512 高清合成就緒 (渲染: %d/%d)")
			slot_summary_label.text = fmt_512 % [loaded_count, total_slots]
		elif character != null:
			var entries := character.get_rendered_entries()
			for e in entries:
				if bool(e.get("is_loaded", false)):
					loaded_count += 1
			var fmt_all := _t("7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)")
			slot_summary_label.text = fmt_all % [entries.size(), loaded_count, entries.size()]


## 更新按鈕選取高亮樣式
const COLOR_BORDER := Color("#1F1A3A")      ## 深藍紫描邊
const COLOR_ORANGE := Color("#FFA010")      ## 暖橘選中果凍厚底
const COLOR_CARD_WARM := Color("#FFF8E7")   ## 奶油未選底
const COLOR_TEXT_DARK := Color("#1F1A3A")   ## 深色文字

func _update_race_buttons_visual() -> void:
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		var is_selected: bool = (rid == _current_race_id)

		# 依 review.md 31d：零系統 Emoji、零字元當圖示
		var check_lbl = btn.get_node_or_null("Margin/VBox/CheckLabel")
		if check_lbl is Label:
			check_lbl.text = ""
			check_lbl.visible = false

		var name_lbl = btn.get_node_or_null("Margin/VBox/NameLabel")
		if name_lbl is Label and RACES_DATA.has(rid):
			_format_race_name_label(name_lbl, _t(str(RACES_DATA[rid].get("name_zh", rid))))

		# 依日常憲法 §3 & review.md 0-QA11 / 0-UI1:
		# 未選取＝奶油卡＋深藍紫描邊底框 ≥3px (設為 4px)
		# 選中＝暖橘 #FFA010 果凍厚底 5~6px (設為 5px)
		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(16)
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		if is_selected:
			sb.bg_color = COLOR_ORANGE
			sb.border_width_bottom = 5
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
			sb.shadow_size = 6
			sb.shadow_offset = Vector2(0, 3)
		else:
			sb.bg_color = COLOR_CARD_WARM
			sb.border_width_bottom = 4
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.10)
			sb.shadow_size = 4
			sb.shadow_offset = Vector2(0, 2)

		var sb_h := sb.duplicate() as StyleBoxFlat
		sb_h.bg_color = Color("#FFB84D") if is_selected else Color("#FFF4D0")

		var sb_p := sb.duplicate() as StyleBoxFlat
		sb_p.border_width_bottom = max(1, sb.border_width_bottom - 2)

		btn.add_theme_stylebox_override("normal", sb)
		btn.add_theme_stylebox_override("hover", sb_h)
		btn.add_theme_stylebox_override("pressed", sb_p)
		btn.add_theme_stylebox_override("focus", sb)

		btn.modulate = Color.WHITE

		if is_selected and btn.visible:
			_scroll_to_race_btn(btn)


func _scroll_to_race_btn(btn: Button) -> void:
	call_deferred("_do_scroll_to_race_btn", btn)


func _do_scroll_to_race_btn(btn: Button) -> void:
	var scroll := get_node_or_null("TopRaceBar") as ScrollContainer
	if not scroll or not is_instance_valid(scroll) or not is_instance_valid(btn):
		return
	var hbar := scroll.get_h_scroll_bar()
	var view_w: float = scroll.size.x
	if view_w <= 0.0:
		return
	var btn_left: float = btn.position.x
	var btn_right: float = btn.position.x + btn.size.x
	var pad: float = 32.0
	var max_scroll: int = int(hbar.max_value - hbar.page) if hbar else 999999
	if btn_right + pad > scroll.scroll_horizontal + view_w:
		var target: int = int(ceil(btn_right + pad - view_w))
		target = clampi(target, 0, max_scroll)
		scroll.scroll_horizontal = target
	elif btn_left - pad < scroll.scroll_horizontal:
		var target: int = int(floor(max(0.0, btn_left - pad)))
		target = clampi(target, 0, max_scroll)
		scroll.scroll_horizontal = target


## 取得當前種族
func get_current_race() -> String:
	return _current_race_id


## 取得當前選取的部件組合
func get_current_selections() -> Dictionary:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])
	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}
	return {
		"race": _current_race_id,
		"costume": cur_costume.get("id", ""),
		"chassis": cur_chassis.get("id", "")
	}


## 儲存驗證截圖
func save_proof_screenshot(target_path: String = "") -> String:
	var path := target_path
	if path == "":
		path = "res://../screenshots/proof_paperdoll_select_demo.png"

	var global_path := ProjectSettings.globalize_path(path)
	var dir_path := global_path.get_base_dir()
	if not DirAccess.dir_exists_absolute(dir_path):
		DirAccess.make_dir_recursive_absolute(dir_path)

	# 透過 Viewport 截取 1280x720 完整高畫質畫面
	var vp := get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var err := img.save_png(global_path)
				if err == OK:
					print("[PaperdollSelectDemo] 成功儲存 Viewport 畫面截圖至：%s" % global_path)
					return global_path

	# Fallback: 若在無頭純合成模式，儲存中心角色合成圖
	if character != null:
		var char_path := global_path.replace(".png", "_character.png")
		if _sprite_512 != null and _sprite_512.visible and _sprite_512.texture != null:
			var img512 := _sprite_512.texture.get_image()
			if img512 != null and not img512.is_empty():
				img512.save_png(char_path)
				print("[PaperdollSelectDemo] 儲存角色 512 高清合成圖備用截圖至：%s" % char_path)
				return char_path
		character.save_composite_png(char_path)
		print("[PaperdollSelectDemo] 儲存角色合成圖備用截圖至：%s" % char_path)
		return char_path

	return ""


## 關閉面板並釋放
func close() -> void:
	_stop_breathe_tween()
	cancelled.emit()
	queue_free()


## 待機呼吸小動作 (對齊大廳／衣櫥／探索規範：scale 在 (1.03, 0.97) ↔ (0.98, 1.02)、週期約 1.1s、TRANS_SINE、loop)
func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid() and _breathe_tween.is_running():
		return
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if character:
		character.scale = Vector2.ONE
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(character, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(character, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _stop_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
		_breathe_tween = null
	if character:
		character.scale = Vector2.ONE


func is_breathe_running() -> bool:
	return _breathe_tween != null and _breathe_tween.is_valid() and _breathe_tween.is_running()

