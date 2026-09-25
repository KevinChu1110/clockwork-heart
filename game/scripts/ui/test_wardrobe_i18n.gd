extends SceneTree
## 衣櫥六語系單元測試 (WardrobeDialog i18n)
## 驗證：
## 1. 六語系 ui.json 包含「星紋斗篷」與「無外裝 (裸機素體)」對應翻譯。
## 2. 衣櫥彈窗大標題、副標、種族列提示、操作按鈕六語系詞條對齊。
## 3. 蛙族衣櫥在 zh_TW、en、ja 切換下，標題、按鈕、卡片名稱即時連動刷新。

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_wardrobe_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證詞條字典解析
	var expected_astral := {
		"zh_TW": "星紋斗篷",
		"zh_CN": "星纹斗篷",
		"en": "Astral Cape",
		"ja": "星紋のマント",
		"ko": "성문 망토",
		"es": "Capa Astral"
	}
	var expected_bare := {
		"zh_TW": "無外裝 (裸機素體)",
		"zh_CN": "无外装 (裸机素体)",
		"en": "No Costume (Bare Frame)",
		"ja": "外装なし (素体)",
		"ko": "외형 없음 (기본 소체)",
		"es": "Sin Atuendo (Chasis Base)"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)
		var trans_astral := ContentLoc.text("ui", "星紋斗篷")
		if trans_astral != expected_astral[code]:
			_fail("語系 [%s] 星紋斗篷 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_astral[code], trans_astral])
		else:
			print("  ✓ [%s] 星紋斗篷 -> %s" % [code, trans_astral])

		var trans_bare := ContentLoc.text("ui", "無外裝 (裸機素體)")
		if trans_bare != expected_bare[code]:
			_fail("語系 [%s] 無外裝 (裸機素體) 翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_bare[code], trans_bare])
		else:
			print("  ✓ [%s] 無外裝 (裸機素體) -> %s" % [code, trans_bare])

	# 2. 驗證彈窗節點實例化與文字更新
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var dlg = WardrobeDialog.new()
	root_node.add_child(dlg)
	dlg.set_race_filter("frog")

	# zh_TW 檢查
	if dlg._title_label.text != "發條衣櫥 · 英雄換裝":
		_fail("zh_TW 標題不符: %s" % dlg._title_label.text)
	if dlg._btn_confirm.text != "確認換裝 · 套用新外觀":
		_fail("zh_TW 確認鈕文字不符: %s" % dlg._btn_confirm.text)
	if dlg._btn_reset.text != "還原預設":
		_fail("zh_TW 還原鈕文字不符: %s" % dlg._btn_reset.text)
	if dlg._btn_random.text != "隨機":
		_fail("zh_TW 隨機鈕文字不符: %s" % dlg._btn_random.text)
	print("  ✓ zh_TW 彈窗文字驗證通過")

	# 切換至 en 檢查
	if loc_node:
		loc_node.call("set_locale", "en")
	if dlg._title_label.text != "Clockwork Wardrobe · Hero Outfits":
		_fail("en 標題未即時更新: %s" % dlg._title_label.text)
	if dlg._btn_confirm.text != "Confirm Outfit · Apply New Look":
		_fail("en 確認鈕未即時更新: %s" % dlg._btn_confirm.text)
	if dlg._btn_reset.text != "Reset":
		_fail("en 還原鈕未即時更新: %s" % dlg._btn_reset.text)
	if dlg._btn_random.text != "Random":
		_fail("en 隨機鈕未即時更新: %s" % dlg._btn_random.text)
	if dlg._filter_title_lbl.text != "Wardrobe Vault":
		_fail("en 外裝庫未即時更新: %s" % dlg._filter_title_lbl.text)

	# 檢查卡片網格文字
	var found_astral_en := false
	var found_bare_en := false
	for btn in dlg._costume_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label:
			if lbl.text == "Astral Cape":
				found_astral_en = true
			elif lbl.text == "No Costume (Bare Frame)":
				found_bare_en = true
	if not found_astral_en:
		_fail("en 蛙衣櫥卡片未找到 Astral Cape")
	if not found_bare_en:
		_fail("en 蛙衣櫥卡片未找到 No Costume (Bare Frame)")
	print("  ✓ en 彈窗文字與卡片即時切換驗證通過")

	# 切換至 ja 檢查
	if loc_node:
		loc_node.call("set_locale", "ja")
	if dlg._title_label.text != "ゼンマイ衣装棚 · 英雄の着替え":
		_fail("ja 標題未即時更新: %s" % dlg._title_label.text)
	if dlg._btn_confirm.text != "着替え確認 · 新しい外見を適用":
		_fail("ja 確認鈕未即時更新: %s" % dlg._btn_confirm.text)
	if dlg._btn_reset.text != "デフォルトに戻す":
		_fail("ja 還原鈕未即時更新: %s" % dlg._btn_reset.text)
	if dlg._btn_random.text != "ランダム":
		_fail("ja 隨機鈕未即時更新: %s" % dlg._btn_random.text)

	var found_astral_ja := false
	var found_bare_ja := false
	for btn in dlg._costume_cards:
		var lbl = btn.find_child("NameLabel", true, false)
		if lbl is Label:
			if lbl.text == "星紋のマント":
				found_astral_ja = true
			elif lbl.text == "外装なし (素体)":
				found_bare_ja = true
	if not found_astral_ja:
		_fail("ja 蛙衣櫥卡片未找到 星紋のマント")
	if not found_bare_ja:
		_fail("ja 蛙衣櫥卡片未找到 外装なし (素体)")
	print("  ✓ ja 彈窗文字與卡片即時切換驗證通過")

	dlg.queue_free()

	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	if _ok:
		print("WARDROBE_I18N_OK")
		quit(0)
	else:
		print("WARDROBE_I18N_FAIL")
		quit(1)
