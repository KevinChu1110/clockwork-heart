extends SceneTree
## 單元測試：戰鬥雜魚與關卡敵名六語系與即時切換驗證 (test_enemy_name_i18n.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 0-QA24, 0-QA25
## 驗證：
## 1. 世界內容表 13 個雜魚／關卡敵名在六語系 (zh_TW, zh_CN, en, ja, ko, es) 下均有正確對應，無漏翻、無系統 emoji。
## 2. BattleSim.make_world_fight 在不同語系下建立之 BattleUnit.display_name 正確在地化。
## 3. 戰鬥畫面在 en／ja 下啟動時，頂欄敵名為該語系譯文而非繁中原文。
## 4. 戰鬥中動態切換語系 (locale_changed)，頂欄敵名、鎖定提示、部位提示即時同步切換。
## 5. 切回繁中 (zh_TW) 正確還原。

const WorldContent = preload("res://scripts/world/world_content.gd")
const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const EXPECTED_ENEMIES: Dictionary = {
	"ash_rat": {
		"zh_TW": "灰燼鼠",
		"zh_CN": "灰烬鼠",
		"en": "Ash Rat",
		"ja": "灰燼鼠",
		"ko": "잿불 쥐",
		"es": "Rata de ceniza"
	},
	"road_bandit": {
		"zh_TW": "荒路匪徒",
		"zh_CN": "荒路匪徒",
		"en": "Road Bandit",
		"ja": "荒路の匪徒",
		"ko": "황로 비적",
		"es": "Bandido del camino"
	},
	"sewer_slime": {
		"zh_TW": "下水黏漿",
		"zh_CN": "下水黏浆",
		"en": "Sewer Slime",
		"ja": "下水の粘漿",
		"ko": "하수 점액",
		"es": "Limo de cloaca"
	},
	"fog_shade": {
		"zh_TW": "霧影",
		"zh_CN": "雾影",
		"en": "Mist Shade",
		"ja": "霧影",
		"ko": "안개 그림자",
		"es": "Sombra de niebla"
	},
	"bamboo_spirit": {
		"zh_TW": "竹影拳靈",
		"zh_CN": "竹影拳灵",
		"en": "Bamboo Fist Spirit",
		"ja": "竹影の拳霊",
		"ko": "죽영 권령",
		"es": "Espíritu de puño del bambú"
	},
	"forest_sprite": {
		"zh_TW": "林間風妖",
		"zh_CN": "林间风妖",
		"en": "Forest Wind Sprite",
		"ja": "林間の風妖",
		"ko": "숲속 바람 요괴",
		"es": "Duende del viento del bosque"
	},
	"coast_raider": {
		"zh_TW": "潮襲海盜",
		"zh_CN": "潮袭海盗",
		"en": "Tide Raider",
		"ja": "潮襲いの海賊",
		"ko": "파도 습격 해적",
		"es": "Saqueador de la marea"
	},
	"scar_wisp": {
		"zh_TW": "疤地焰靈",
		"zh_CN": "疤地焰灵",
		"en": "Scar Flame Wisp",
		"ja": "傷跡の焰霊",
		"ko": "흉터 불꽃 정령",
		"es": "Fuego fatuo de la cicatriz"
	},
	"heart_demon": {
		"zh_TW": "心魔",
		"zh_CN": "心魔",
		"en": "Heart Demon",
		"ja": "心魔",
		"ko": "심마",
		"es": "Demonio interior"
	},
	"black_ronin": {
		"zh_TW": "黑鏽浪人",
		"zh_CN": "黑锈浪人",
		"en": "Blight Rust Wanderer",
		"ja": "黒錆の浪人",
		"ko": "검은 녹 낭인",
		"es": "Errante de Óxido Negro"
	},
	"scar_lord": {
		"zh_TW": "黑鏽疤主",
		"zh_CN": "黑锈疤主",
		"en": "Scar Lord of Blight Rust",
		"ja": "黒錆の傷跡の主",
		"ko": "검은 녹 흉터의 주인",
		"es": "Señor de la Cicatriz de Óxido Negro"
	},
	"mirror_wraith": {
		"zh_TW": "鏡廊殘影",
		"zh_CN": "镜廊残影",
		"en": "Mirror Hall Afterimage",
		"ja": "鏡廊の残影",
		"ko": "거울 회랑 잔영",
		"es": "Estela de la galería de espejos"
	},
	"wreck_captain": {
		"zh_TW": "沉船船長影",
		"zh_CN": "沉船船长影",
		"en": "Shadow of the Wreck's Captain",
		"ja": "沈船の船長の影",
		"ko": "침몰선 선장의 그림자",
		"es": "Sombra del capitán del naufragio"
	}
}

var _ok := true
var _loc: Node = null
var _gs: Node = null
var _step := 0
var _wait := 0
var _battle: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  [OK] ", msg)

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始戰鬥雜魚與關卡敵名六語系驗證測試 ===")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GSClass = load("res://scripts/autoload/game_state.gd")
		if GSClass:
			_gs = GSClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	# 1. 靜態字典與 WorldContent.enemy_def 全語系覆蓋檢驗
	print("\n--- 1. 靜態字典與 WorldContent.enemy_def 六語系檢驗 ---")
	for lc in LOCALES:
		_loc.call("set_locale", lc)
		for mode in EXPECTED_ENEMIES.keys():
			var d: Dictionary = WorldContent.enemy_def(mode)
			var expected: String = str(EXPECTED_ENEMIES[mode][lc])
			var actual: String = str(d.get("name", ""))
			_assert(actual == expected, "[%s] %s 敵名應為 '%s'，實際為: '%s'" % [lc, mode, expected, actual])

	# 2. BattleSim.make_world_fight 敵方 display_name 檢驗
	print("\n--- 2. BattleSim.make_world_fight display_name 檢驗 ---")
	var dummy_stats := {"name": "小白", "max_hp": 100, "hp": 100, "atk": 20, "def": 5, "speed": 10.0}
	_loc.call("set_locale", "en")
	var sim_en := BattleSim.make_world_fight(dummy_stats, "ash_rat")
	var u_en := sim_en.get_unit("ash_rat")
	_assert(u_en != null and u_en.display_name == "Ash Rat", "EN 建立之 ash_rat display_name 應為 'Ash Rat'，實際為: %s" % (u_en.display_name if u_en else "null"))

	_loc.call("set_locale", "ja")
	var sim_ja := BattleSim.make_world_fight(dummy_stats, "road_bandit")
	var u_ja := sim_ja.get_unit("road_bandit")
	_assert(u_ja != null and u_ja.display_name == "荒路の匪徒", "JA 建立之 road_bandit display_name 應為 '荒路の匪徒'，實際為: %s" % (u_ja.display_name if u_ja else "null"))

	# 切回繁中準備進入場景測試
	_loc.call("set_locale", "zh_TW")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 3. 測試在 en 下啟動雜魚戰，並即時切換 ja / zh_TW
			if _wait == 1:
				print("\n--- 3. 戰鬥畫面在 en 啟動並動態切換語系 ---")
				_loc.call("set_locale", "en")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "road_bandit")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "Road Bandit", "EN 戰鬥頂欄敵名應為 'Road Bandit'，實際為: '%s'" % (en_label.text if en_label else "null"))

				# 即時切換至 ja
				_loc.call("set_locale", "ja")
			elif _wait == 5:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "荒路の匪徒", "即時切換 JA 後頂欄敵名應為 '荒路の匪徒'，實際為: '%s'" % (en_label.text if en_label else "null"))
				var u_bandit: BattleUnit = _battle.get("sim").get_unit("road_bandit") if _battle.get("sim") else null
				_assert(u_bandit != null and u_bandit.display_name == "荒路の匪徒", "即時切換 JA 後 sim BattleUnit.display_name 應同步換為 '荒路の匪徒'")

				# 即時切回繁中 zh_TW
				_loc.call("set_locale", "zh_TW")
			elif _wait == 7:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				_assert(en_label != null and en_label.text == "荒路匪徒", "即時切回繁中後頂欄敵名應還原為 '荒路匪徒'，實際為: '%s'" % (en_label.text if en_label else "null"))

				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 2
				_wait = 0

		2:
			# 4. 測試帶部位的關卡敵名 (scar_lord) 頂欄敵名與鎖定提示同步換
			if _wait == 1:
				print("\n--- 4. 帶部位敵名 (scar_lord) 頂欄敵名與鎖定提示同步切換 ---")
				_loc.call("set_locale", "zh_TW")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "scar_lord")
			elif _wait == 3:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				var parry_label: Label = _battle.get_node_or_null("%ParryHint")
				var focus_label: Label = _battle.get("_focus_hint")
				_assert(en_label != null and en_label.text == "黑鏽疤主", "繁中 scar_lord 頂欄敵名應為 '黑鏽疤主'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(focus_label != null and focus_label.text == "部位鎖定 → 溢能核心", "繁中部位鎖定提示應為 '部位鎖定 → 溢能核心'，實際為: '%s'" % (focus_label.text if focus_label else "null"))
				_assert(parry_label != null and parry_label.text.contains("鎖定：溢能核心"), "繁中 parry_hint 應包含 '鎖定：溢能核心'，實際為: '%s'" % (parry_label.text if parry_label else "null"))

				# 即時切換至 en
				_loc.call("set_locale", "en")
			elif _wait == 5:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				var parry_label: Label = _battle.get_node_or_null("%ParryHint")
				var focus_label: Label = _battle.get("_focus_hint")
				_assert(en_label != null and en_label.text == "Scar Lord of Blight Rust", "切換 EN 後頂欄敵名應為 'Scar Lord of Blight Rust'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(focus_label != null and focus_label.text == "Part locked → Overflow Core", "切換 EN 後部位鎖定提示應為 'Part locked → Overflow Core'，實際為: '%s'" % (focus_label.text if focus_label else "null"))
				_assert(parry_label != null and parry_label.text.contains("Locked: Overflow Core"), "切換 EN 後 parry_hint 應包含 'Locked: Overflow Core'，實際為: '%s'" % (parry_label.text if parry_label else "null"))

				# 即時切換至 ja
				_loc.call("set_locale", "ja")
			elif _wait == 7:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				var parry_label: Label = _battle.get_node_or_null("%ParryHint")
				var focus_label: Label = _battle.get("_focus_hint")
				_assert(en_label != null and en_label.text == "黒錆の傷跡の主", "切換 JA 後頂欄敵名應為 '黒錆の傷跡の主'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(focus_label != null and focus_label.text == "部位捕捉 → 溢れ核", "切換 JA 後部位鎖定提示應為 '部位捕捉 → 溢れ核'，實際為: '%s'" % (focus_label.text if focus_label else "null"))
				_assert(parry_label != null and parry_label.text.contains("捕捉：溢れ核"), "切換 JA 後 parry_hint 應包含 '捕捉：溢れ核'，實際為: '%s'" % (parry_label.text if parry_label else "null"))

				# 即時切回繁中 zh_TW
				_loc.call("set_locale", "zh_TW")
			elif _wait == 9:
				var en_label: Label = _battle.get_node_or_null("%EnemyName")
				var focus_label: Label = _battle.get("_focus_hint")
				_assert(en_label != null and en_label.text == "黑鏽疤主", "還原繁中後頂欄敵名應為 '黑鏽疤主'，實際為: '%s'" % (en_label.text if en_label else "null"))
				_assert(focus_label != null and focus_label.text == "部位鎖定 → 溢能核心", "還原繁中後部位鎖定提示應為 '部位鎖定 → 溢能核心'，實際為: '%s'" % (focus_label.text if focus_label else "null"))

				if _battle and is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				# 5. 結算
				if _ok:
					print("\nTEST_ENEMY_NAME_I18N_OK")
					quit(0)
				else:
					print("\nTEST_ENEMY_NAME_I18N_FAIL")
					quit(1)
				return true
	return false
