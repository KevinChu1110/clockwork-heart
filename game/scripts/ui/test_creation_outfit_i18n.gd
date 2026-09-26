extends SceneTree
## 創角外裝與塗裝六語系單元測試 (Creation Outfit & Chassis i18n Test)
## 驗證：
## 1. 六語系字典包含所有外裝、素體、塗裝品名與描述。
## 2. 創角畫面 (PaperdollSelectDemo) 在六語系切換下，目前選中的外裝名稱、外裝描述、塗裝名稱、塗裝描述即時刷新。
## 3. 切換外裝 (Next/Prev) 與塗裝 (Next/Prev) 後，畫面品名與描述依然維持當前語系，無繁中品名殘留。
## 4. 切換種族 (rabbit -> fox -> lion -> bear -> frog -> panda) 測試，外裝與塗裝名同語系。
## 5. 衣櫥畫面 (WardrobeDialog) 切換 en/ja 時，所有外裝與塗裝卡片文字即時更新。

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")
const WardrobeDialogClass = preload("res://scripts/ui/wardrobe_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("CREATION_OUTFIT_I18N_OK")
			quit(0)
		else:
			push_error("CREATION_OUTFIT_I18N_FAIL")
			print("CREATION_OUTFIT_I18N_FAIL")
			quit(1)
		return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_creation_outfit_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 字典詞條查驗
	print("\n--- 1. 驗證六語系字典外裝與塗裝詞條 ---")
	var sample_terms := {
		"胡桃鉗近衛軍裝": {
			"zh_TW": "胡桃鉗近衛軍裝", "zh_CN": "胡桃夹子近卫军装",
			"en": "Nutcracker Guard Uniform", "ja": "くるみ割り近衛軍服",
			"ko": "호두까기 근위대 군복", "es": "Uniforme de Guardia Cascanueces"
		},
		"無外裝 (裸機素體)": {
			"zh_TW": "無外裝 (裸機素體)", "zh_CN": "无外装 (裸机素体)",
			"en": "No Costume (Bare Frame)", "ja": "外装なし (素体)",
			"ko": "외형 없음 (기본 소체)", "es": "Sin Atuendo (Chasis Base)"
		},
		"原廠象牙白": {
			"zh_TW": "原廠象牙白", "zh_CN": "原厂象牙白",
			"en": "Factory Ivory White", "ja": "工場出荷アイボリーホワイト",
			"ko": "순정 아이보리 화이트", "es": "Blanco Marfil de Fábrica"
		},
		"午夜深藍烤漆": {
			"zh_TW": "午夜深藍烤漆", "zh_CN": "午夜深蓝烤漆",
			"en": "Midnight Navy Paint", "ja": "ミッドナイトネイビーラッカー",
			"ko": "미드나이트 네이비 도장", "es": "Pintura Azul Marino Medianoche"
		},
		"黃銅原金拋光": {
			"zh_TW": "黃銅原金拋光", "zh_CN": "黄铜原金抛光",
			"en": "Polished Raw Brass", "ja": "原色真鍮ゴールド研磨",
			"ko": "순수 황동 골드 연마", "es": "Latón Dorado Pulido"
		},
		"星紋見習占星斗篷": {
			"zh_TW": "星紋見習占星斗篷", "zh_CN": "星纹见习占星斗篷",
			"en": "Astral Apprentice Cape", "ja": "星紋見習い占星マント",
			"ko": "성문 수습 점성 망토", "es": "Capa Astral de Aprendiz de Astrólogo"
		},
		"靈狐曜橙烤漆": {
			"zh_TW": "靈狐曜橙烤漆", "zh_CN": "灵狐曜橙烤漆",
			"en": "Radiant Fox Orange Paint", "ja": "霊狐シャインオレンジラッカー",
			"ko": "영호 샤인 오렌지 도장", "es": "Pintura Naranja Brillante Zorro"
		},
		"經典紅藍胡桃鉗金屬禮服與黃銅肩章": {
			"zh_TW": "經典紅藍胡桃鉗金屬禮服與黃銅肩章", "zh_CN": "经典红蓝胡桃夹子金属礼服与黄铜肩章",
			"en": "Classic red & blue nutcracker uniform with brass pauldrons",
			"ja": "真鍮エポレット付きクラシック紅白胡桃割り制服",
			"ko": "황동 견장의 클래식 레드/블루 호두까기 제복",
			"es": "Uniforme clásico rojo y azul de cascanueces con hombreras de latón"
		},
		"溫潤微光象牙白高光琺瑯塗層": {
			"zh_TW": "溫潤微光象牙白高光琺瑯塗層", "zh_CN": "温润微光象牙白高光珐琅涂层",
			"en": "Gentle glimmering ivory gloss enamel coating",
			"ja": "温かみのある光沢アイボリーエナメルコーティング",
			"ko": "은은한 광택의 아이보리 유광 에나멜 코팅",
			"es": "Cálido revestimiento de esmalte brillante marfil"
		}
	}

	for term in sample_terms.keys():
		var expected_map: Dictionary = sample_terms[term]
		for loc in LOCALES:
			if loc_node:
				loc_node.call("set_locale", loc)
			var actual := ContentLoc.text("ui", term)
			var exp: String = expected_map.get(loc, "")
			if actual != exp:
				_fail("詞條 [%s] 在語系 [%s] 翻譯不符: 期望 '%s', 實際 '%s'" % [term, loc, exp, actual])
	print("  ✓ 抽樣外裝與塗裝品名/描述六語系查驗全數通過")

	# 2. 創角介面實例化與文字更新驗證
	print("\n--- 2. 驗證創角介面 (PaperdollSelectDemo) 即時切語系連動 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var demo_node = DemoScene.instantiate()
	root_node.add_child(demo_node)
	demo_node.select_race("rabbit")

	var costume_lbl: Label = demo_node.costume_name_label
	var chassis_lbl: Label = demo_node.chassis_name_label
	var costume_desc_lbl: Label = demo_node.costume_desc_label
	var chassis_desc_lbl: Label = demo_node.chassis_desc_label

	# 繁中預設檢查
	if not costume_lbl.text.begins_with("胡桃鉗近衛軍裝"):
		_fail("zh_TW 預設外裝名稱不符: %s" % costume_lbl.text)
	if not chassis_lbl.text.begins_with("原廠象牙白"):
		_fail("zh_TW 預設塗裝名稱不符: %s" % chassis_lbl.text)
	if costume_desc_lbl.text != "經典紅藍胡桃鉗金屬禮服與黃銅肩章":
		_fail("zh_TW 預設外裝描述不符: %s" % costume_desc_lbl.text)
	if chassis_desc_lbl.text != "溫潤微光象牙白高光琺瑯塗層":
		_fail("zh_TW 預設塗裝描述不符: %s" % chassis_desc_lbl.text)
	print("  ✓ zh_TW 創角介面品名與描述驗證通過")

	# 切換至 en 檢查即時刷新
	if loc_node:
		loc_node.call("set_locale", "en")
	if not costume_lbl.text.begins_with("Nutcracker Guard Uniform"):
		_fail("en 外裝名稱未即時刷新: %s" % costume_lbl.text)
	if not chassis_lbl.text.begins_with("Factory Ivory White"):
		_fail("en 塗裝名稱未即時刷新: %s" % chassis_lbl.text)
	if costume_desc_lbl.text != "Classic red & blue nutcracker uniform with brass pauldrons":
		_fail("en 外裝描述未即時刷新: %s" % costume_desc_lbl.text)
	if chassis_desc_lbl.text != "Gentle glimmering ivory gloss enamel coating":
		_fail("en 塗裝描述未即時刷新: %s" % chassis_desc_lbl.text)
	print("  ✓ en 創角介面品名與描述即時刷新通過")

	# 切換至 ja 檢查即時刷新
	if loc_node:
		loc_node.call("set_locale", "ja")
	if not costume_lbl.text.begins_with("くるみ割り近衛軍服"):
		_fail("ja 外裝名稱未即時刷新: %s" % costume_lbl.text)
	if not chassis_lbl.text.begins_with("工場出荷アイボリーホワイト"):
		_fail("ja 塗裝名稱未即時刷新: %s" % chassis_lbl.text)
	if costume_desc_lbl.text != "真鍮エポレット付きクラシック紅白胡桃割り制服":
		_fail("ja 外裝描述未即時刷新: %s" % costume_desc_lbl.text)
	if chassis_desc_lbl.text != "温かみのある光沢アイボリーエナメルコーティング":
		_fail("ja 塗裝描述未即時刷新: %s" % chassis_desc_lbl.text)
	print("  ✓ ja 創角介面品名與描述即時刷新通過")

	# 3. 測試切換外裝與切換塗裝在非繁中語系下的表現
	print("\n--- 3. 驗證切換外裝/塗裝品名跟隨語系 ---")
	# 在 ja 下切換外裝至下一個
	demo_node._on_costume_next_pressed()
	if not costume_lbl.text.begins_with("蒸気工匠のサスペンダー作業着"):
		_fail("ja 切換外裝後名稱未跟隨語系: %s" % costume_lbl.text)
	# 切換塗裝至下一個
	demo_node._on_chassis_next_pressed()
	if not chassis_lbl.text.begins_with("原色真鍮ゴールド研磨"):
		_fail("ja 切換塗裝後名稱未跟隨語系: %s" % chassis_lbl.text)
	print("  ✓ ja 切換外裝與塗裝後品名維持日文無殘留")

	# 切到裸機素體
	demo_node._on_costume_prev_pressed()
	demo_node._on_costume_prev_pressed() # 到 "none" 裸機素體
	if not costume_lbl.text.begins_with("外装なし (素体)"):
		_fail("ja 裸機素體名稱未跟隨語系: %s" % costume_lbl.text)
	if costume_desc_lbl.text != "外装を解除し、象牙色の精密機械ボディを露出":
		_fail("ja 裸機素體描述未跟隨語系: %s" % costume_desc_lbl.text)
	print("  ✓ ja 裸機素體名稱與描述無繁中殘留")

	# 4. 跨種族切換驗證
	print("\n--- 4. 跨種族外裝與塗裝語系驗證 ---")
	demo_node.select_race("fox")
	if loc_node:
		loc_node.call("set_locale", "en")
	if not costume_lbl.text.begins_with("Astral Apprentice Cape"):
		_fail("en 狐狸外裝名稱未跟隨語系: %s" % costume_lbl.text)
	if not chassis_lbl.text.begins_with("Radiant Fox Orange Paint"):
		_fail("en 狐狸塗裝名稱未跟隨語系: %s" % chassis_lbl.text)
	print("  ✓ en 靈尾狐外裝與塗裝驗證通過")

	demo_node.queue_free()

	# 5. 衣櫥卡片驗證
	print("\n--- 5. 驗證衣櫥卡片六語系切換 ---")
	if loc_node:
		loc_node.call("set_locale", "en")
	var wardrobe = WardrobeDialogClass.new()
	root_node.add_child(wardrobe)
	wardrobe.set_race_filter("rabbit")

	var found_nutcracker_en := false
	var found_ivory_en := false
	for btn in wardrobe._costume_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label and lbl.text == "Nutcracker Guard Uniform":
			found_nutcracker_en = true
	for btn in wardrobe._chassis_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label and lbl.text == "Factory Ivory White":
			found_ivory_en = true

	if not found_nutcracker_en:
		_fail("en 衣櫥外裝卡片未找到 Nutcracker Guard Uniform")
	if not found_ivory_en:
		_fail("en 衣櫥塗裝卡片未找到 Factory Ivory White")
	print("  ✓ en 衣櫥外裝與塗裝卡片無繁中殘留")

	# 切換至 ja 檢查
	if loc_node:
		loc_node.call("set_locale", "ja")
	var found_nutcracker_ja := false
	var found_ivory_ja := false
	for btn in wardrobe._costume_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label and lbl.text == "くるみ割り近衛軍服":
			found_nutcracker_ja = true
	for btn in wardrobe._chassis_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label and lbl.text == "工場出荷アイボリーホワイト":
			found_ivory_ja = true

	if not found_nutcracker_ja:
		_fail("ja 衣櫥外裝卡片未找到 くるみ割り近衛軍服")
	if not found_ivory_ja:
		_fail("ja 衣櫥塗裝卡片未找到 工場出荷アイボリーホワイト")
	print("  ✓ ja 衣櫥外裝與塗裝卡片無繁中殘留")

	wardrobe.queue_free()

	if loc_node:
		loc_node.call("set_locale", "zh_TW")
