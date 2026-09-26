extends SceneTree
## 第一季節奏與等級上限測試：godot --headless -s res://scripts/systems/test_pacing_s1.gd
##
## 驗證：
## 1. pacing_s1.json 格式正確且 s1_cap == 30
## 2. GameState.get_level_cap() == 30，等級到 30 後 add_xp 經驗可累、level 不再加、數值不再成長
## 3. RegionCatalog.SUGGEST_LV 讀自 pacing_s1.json，表上未列關卡維持 0
## 4. 各章節建議等級區間符合 C0–C3 (1–15)、C4–C6 (16–25)、高難／後段 (26–30)
## 5. 「本季上限」六語系翻譯齊全且零系統 Emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始 test_pacing_s1 測試 ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	if gs == null:
		_fail("找不到 GameState autoload")
		_finish()
		return

	_test_pacing_json()
	_test_level_cap(gs)
	_test_suggest_lv()
	_test_i18n_and_no_emoji()

	_finish()


func _test_pacing_json() -> void:
	print("--- 1. 檢驗 pacing_s1.json 配置 ---")
	var path := "res://data/tables/pacing_s1.json"
	if not FileAccess.file_exists(path):
		_fail("找不到規格檔：%s" % path)
		return
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		_fail("無法開啟規格檔：%s" % path)
		return
	var data = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		_fail("pacing_s1.json 不是 Dictionary")
		return

	var cap := int(data.get("s1_cap", 0))
	if cap != 30:
		_fail("s1_cap 應為 30，實際為 %d" % cap)
	else:
		print("  ok s1_cap == 30")

	var ch: Dictionary = data.get("chapters", {})
	if ch.is_empty():
		_fail("缺少 chapters 節點")
	else:
		var c0_c3: Dictionary = ch.get("C0_C3", {})
		var c4_c6: Dictionary = ch.get("C4_C6", {})
		var eg: Dictionary = ch.get("endgame", {})
		if int(c0_c3.get("min_lv", 0)) != 1 or int(c0_c3.get("max_lv", 0)) != 15:
			_fail("C0_C3 區間不符：應為 1~15，得 %s~%s" % [str(c0_c3.get("min_lv")), str(c0_c3.get("max_lv"))])
		if int(c4_c6.get("min_lv", 0)) != 16 or int(c4_c6.get("max_lv", 0)) != 25:
			_fail("C4_C6 區間不符：應為 16~25，得 %s~%s" % [str(c4_c6.get("min_lv")), str(c4_c6.get("max_lv"))])
		if int(eg.get("min_lv", 0)) != 26 or int(eg.get("max_lv", 0)) != 30:
			_fail("endgame 區間不符：應為 26~30，得 %s~%s" % [str(eg.get("min_lv")), str(eg.get("max_lv"))])
		print("  ok 章節節奏定義覆蓋 C0–C3 (1–15)、C4–C6 (16–25)、高難 (26–30)")


func _test_level_cap(gs: Node) -> void:
	print("--- 2. 檢驗 GameState 等級上限與 add_xp 行為 ---")
	if not gs.has_method("get_level_cap"):
		_fail("GameState 缺少 get_level_cap() 方法")
		return

	var cap: int = gs.get_level_cap()
	if cap != 30:
		_fail("GameState.get_level_cap() 應為 30，實際為 %d" % cap)
	else:
		print("  ok GameState 等級上限讀表確認為 30")

	# 測試從 1 級升級
	gs.level = 1
	gs.xp = 0
	gs.max_hp = 100
	gs.atk = 10
	gs.def_stat = 5
	gs.speed = 10

	# 測試在 Lv30 時 add_xp
	gs.level = 30
	gs.xp = 120
	var hp_before: int = gs.max_hp
	var atk_before: int = gs.atk
	var def_before: int = gs.def_stat
	var sp_before: int = gs.speed

	var res: Dictionary = gs.add_xp(500)
	if int(res.get("levels", -1)) != 0:
		_fail("Lv30 add_xp 應獲得 0 個升級，實際獲得 %d" % int(res.get("levels", -1)))
	if gs.level != 30:
		_fail("Lv30 add_xp 後等級不應增加，實際為 %d" % gs.level)
	if gs.xp != 620:
		_fail("Lv30 add_xp 經驗應累積 (120+500=620)，實際為 %d" % gs.xp)
	if gs.max_hp != hp_before or gs.atk != atk_before or gs.def_stat != def_before or gs.speed != sp_before:
		_fail("Lv30 add_xp 後數值不應成長")

	print("  ok Lv30 拿經驗：經驗可累 (120→620)、level 仍為 30、面板數值無成長")

	# 測試新號升級停在 30
	gs.level = 29
	gs.xp = 0
	var req: int = gs.xp_to_next()
	var res2: Dictionary = gs.add_xp(req * 5) # 給予巨量經驗足以升多次
	if gs.level != 30:
		_fail("連續加經驗應於 Lv30 停止，實際等級為 %d" % gs.level)
	if int(res2.get("levels", 0)) != 1:
		_fail("Lv29 獲得巨量經驗應只升 1 級至 30，實際升級數：%d" % int(res2.get("levels", 0)))
	print("  ok 新號連續加經驗升至 Lv30 準確停止")


func _test_suggest_lv() -> void:
	print("--- 3. 檢驗 RegionCatalog.SUGGEST_LV 讀表 ---")
	var RegionCatalog = load("res://scripts/world/region_catalog.gd")
	if RegionCatalog == null:
		_fail("無法載入 RegionCatalog")
		return

	# 檢查各關卡
	var leo_lv := int(RegionCatalog.suggest_lv("r1_s2"))
	var fog_lv := int(RegionCatalog.suggest_lv("r2_s1"))
	var abo_lv := int(RegionCatalog.suggest_lv("r3_s1"))
	var shadow_lv := int(RegionCatalog.suggest_lv("r3_s2"))
	var stone_lv := int(RegionCatalog.suggest_lv("r3_s3"))
	var demon_lv := int(RegionCatalog.suggest_lv("r4_s2"))

	if leo_lv != 10:
		_fail("r1_s2 (雷歐) 建議等級應為 10，實際為 %d" % leo_lv)
	if fog_lv < 1 or fog_lv > 15:
		_fail("r2_s1 (白霧, C2) 建議等級應在 C0-C3 區間 (1-15)，實際為 %d" % fog_lv)
	if abo_lv < 1 or abo_lv > 15:
		_fail("r3_s1 (阿波, C3) 建議等級應在 C0-C3 區間 (1-15)，實際為 %d" % abo_lv)
	if shadow_lv < 16 or shadow_lv > 25:
		_fail("r3_s2 (疾影, C4) 建議等級應在 C4-C6 區間 (16-25)，實際為 %d" % shadow_lv)
	if stone_lv < 16 or stone_lv > 25:
		_fail("r3_s3 (石拳, C5) 建議等級應在 C4-C6 區間 (16-25)，實際為 %d" % stone_lv)
	if demon_lv < 16 or demon_lv > 25:
		_fail("r4_s2 (魔王, C6) 建議等級應在 C4-C6 區間 (16-25)，實際為 %d" % demon_lv)

	# 表上沒寫的關卡維持 0
	var r1_s1 := int(RegionCatalog.suggest_lv("r1_s1"))
	var r2_s2 := int(RegionCatalog.suggest_lv("r2_s2"))
	var r4_s1 := int(RegionCatalog.suggest_lv("r4_s1"))
	var unk := int(RegionCatalog.suggest_lv("nonexistent_stage"))

	if r1_s1 != 0 or r2_s2 != 0 or r4_s1 != 0 or unk != 0:
		_fail("表上未寫之關卡應維持 0：r1_s1=%d, r2_s2=%d, r4_s1=%d, unk=%d" % [r1_s1, r2_s2, r4_s1, unk])
	else:
		print("  ok 表上未寫之關卡維持 0（r1_s1=0, r2_s2=0, r4_s1=0, unk=0）")

	print("  ok 建議等級讀表數值：雷歐=%d, 白霧=%d, 阿波=%d, 疾影=%d, 石拳=%d, 魔王=%d" % [
		leo_lv, fog_lv, abo_lv, shadow_lv, stone_lv, demon_lv
	])


func _test_i18n_and_no_emoji() -> void:
	print("--- 4. 檢驗「本季上限」六語系翻譯與零 Emoji ---")
	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	for loc in locales:
		if loc_node:
			loc_node.set("locale", loc)
		var t := ContentLoc.text("ui", "本季上限")
		if t.strip_edges() == "" or t == "本季上限" and loc in ["en", "ja", "ko", "es"]:
			_fail("[%s] 「本季上限」未翻譯或為空：%s" % [loc, t])
		# 檢查 Emoji
		for ch in t:
			var code := ch.unicode_at(0)
			if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
				_fail("[%s] 「本季上限」包含禁止 Emoji：'%s'" % [loc, t])
		print("  ok [%s] 本季上限 -> %s" % [loc, t])

	# 切回繁中
	if loc_node:
		loc_node.set("locale", "zh_TW")


func _finish() -> void:
	if _ok:
		print("PACING_S1_OK")
		quit(0)
	else:
		print("PACING_S1_FAIL")
		quit(1)
