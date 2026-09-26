extends SceneTree
## 體力不足彈窗六語系即時刷新單元測試 (test_energy_lack_i18n.gd)
##
## 驗證：
## 1. 六語系 ui.json 包含標題、能量數字、說明、看廣告鈕、稍後再來等詞條
## 2. 實例化 EnergyLackDialog，開著彈窗時切換語系 (Loc.locale_changed)，整窗文字即時刷新
## 3. 移除廣告模式下 (has_removed_ads = true) 的說明與按鈕六語系即時切換
## 4. 廣告次數耗盡模式下 (can_claim = false) 的按鈕六語系即時切換
## 5. 0-QA24 檢核：en, es 語系下完全無 CJK 中文字元殘留；ja 日文漢字正確
## 6. 零系統 emoji、橫屏尺寸 740~760、關閉鈕 >= 50px

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const EnergyLackDialogClass = preload("res://scripts/ui/energy_lack_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_ENERGY_LACK_I18N_OK")
					quit(0)
				else:
					push_error("TEST_ENERGY_LACK_I18N_FAIL")
					print("TEST_ENERGY_LACK_I18N_FAIL")
					quit(1)
				return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_energy_lack_i18n 測試 ===")

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc_node == null or gs == null or es == null:
		_fail("Autoload 節點初始化失敗")
		return

	# 1. 預期六語系對照表
	var expected_title := {
		"zh_TW": "能量不足",
		"zh_CN": "能量不足",
		"en": "Insufficient Energy",
		"ja": "エネルギー不足",
		"ko": "에너지 부족",
		"es": "Energía insuficiente",
	}

	var expected_back := {
		"zh_TW": "稍後再來",
		"zh_CN": "稍后再来",
		"en": "Come Back Later",
		"ja": "後で来る",
		"ko": "나중에 오기",
		"es": "Volver más tarde",
	}

	var expected_energy_fmt := {
		"zh_TW": "當前能量：%d／%d",
		"zh_CN": "当前能量：%d／%d",
		"en": "Current Energy: %d/%d",
		"ja": "現在のエネルギー：%d／%d",
		"ko": "현재 에너지: %d/%d",
		"es": "Energía actual: %d/%d",
	}

	var expected_desc_normal := {
		"zh_TW": "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！",
		"zh_CN": "出发探索或挑战战斗需要充足的发条能量。\n您可以稍候等待能量自然恢复，或是观看广告立即补充 3 点能量！",
		"en": "Exploring or challenging battles requires plenty of clockwork energy.\nYou can wait for natural recovery or watch an ad to instantly restore 3 energy!",
		"ja": "探索や戦闘に挑むには、十分なぜんまいエネルギーが必要です。\n自然回復を待つか、広告を視聴して直ちにエネルギーを3回復できます！",
		"ko": "탐색을 떠나거나 전투에 도전하려면 충분한 태엽 에너지가 필요합니다.\n자연 회복을 기다리거나, 광고를 시청하여 즉시 에너지를 3 보충할 수 있습니다!",
		"es": "Explorar o combatir requiere suficiente energía de cuerda.\n¡Puedes esperar a la recuperación natural o ver un anuncio para recargar 3 de energía al instante!",
	}

	var expected_desc_no_ads := {
		"zh_TW": "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！",
		"zh_CN": "出发探索或挑战战斗需要充足的发条能量。\n您可以稍候等待能量自然恢复，或是直接领取补充 3 点能量！",
		"en": "Exploring or challenging battles requires plenty of clockwork energy.\nYou can wait for natural recovery or directly claim 3 energy!",
		"ja": "探索や戦闘に挑むには、十分なぜんまいエネルギーが必要です。\n自然回復を待つか、直接受け取ってエネルギーを3回復できます！",
		"ko": "탐색을 떠나거나 전투에 도전하려면 충분한 태엽 에너지가 필요합니다.\n자연 회복을 기다리거나, 바로 수령하여 즉시 에너지를 3 보충할 수 있습니다!",
		"es": "Explorar o combatir requiere suficiente energía de cuerda.\n¡Puedes esperar a la recuperación natural o reclamar directamente 3 de energía!",
	}

	var expected_btn_claim_normal_fmt := {
		"zh_TW": "觀看廣告回復能量 (+3)  (%d/%d)",
		"zh_CN": "观看广告恢复能量 (+3)  (%d/%d)",
		"en": "Watch Ad to Restore Energy (+3)  (%d/%d)",
		"ja": "広告を見てエネルギー回復 (+3)  (%d/%d)",
		"ko": "광고 보고 에너지 회복 (+3)  (%d/%d)",
		"es": "Ver anuncio y recuperar energía (+3)  (%d/%d)",
	}

	var expected_btn_claim_no_ads_fmt := {
		"zh_TW": "已移除廣告，直接領取 (+3)  (%d/%d)",
		"zh_CN": "已移除广告，直接领取 (+3)  (%d/%d)",
		"en": "Ads Removed, Claim Directly (+3)  (%d/%d)",
		"ja": "広告削除済み、直接受取 (+3)  (%d/%d)",
		"ko": "광고 제거됨, 즉시 수령 (+3)  (%d/%d)",
		"es": "Anuncios eliminados, reclamar directamente (+3)  (%d/%d)",
	}

	var expected_btn_limit_normal_fmt := {
		"zh_TW": "今日廣告次數已達上限 (0/%d)",
		"zh_CN": "今日广告次数已达上限 (0/%d)",
		"en": "Daily ad limit reached (0/%d)",
		"ja": "本日の広告上限に達しました (0/%d)",
		"ko": "오늘 광고 횟수 상한 도달 (0/%d)",
		"es": "Límite de anuncios diario alcanzado (0/%d)",
	}

	var expected_btn_limit_no_ads_fmt := {
		"zh_TW": "今日領取次數已達上限 (0/%d)",
		"zh_CN": "今日领取次数已达上限 (0/%d)",
		"en": "Daily claim limit reached (0/%d)",
		"ja": "本日の受取上限に達しました (0/%d)",
		"ko": "오늘 수령 횟수 상한 도달 (0/%d)",
		"es": "Límite de reclamos diario alcanzado (0/%d)",
	}

	print("\n--- 1. 驗證六語系字典靜態映射與 ContentLoc.text ---")
	for code in LOCALES:
		loc_node.call("set_locale", code)
		ContentLoc.reload()

		var t_title := ContentLoc.text("ui", "能量不足")
		if t_title != expected_title[code]:
			_fail("[%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])

		var t_back := ContentLoc.text("ui", "稍後再來")
		if t_back != expected_back[code]:
			_fail("[%s] 返回按鈕翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_back[code], t_back])

		var t_energy := ContentLoc.text("ui", "當前能量：%d／%d")
		if t_energy != expected_energy_fmt[code]:
			_fail("[%s] 能量格式翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_energy_fmt[code], t_energy])

		var t_desc := ContentLoc.text("ui", "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！")
		if t_desc != expected_desc_normal[code]:
			_fail("[%s] 一般說明翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_desc_normal[code], t_desc])

		var t_ad_btn := ContentLoc.text("ui", "觀看廣告回復能量 (+3)  (%d/%d)")
		if t_ad_btn != expected_btn_claim_normal_fmt[code]:
			_fail("[%s] 看廣告按鈕翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_btn_claim_normal_fmt[code], t_ad_btn])

		if code in ["en", "es"]:
			if _has_cjk(t_title) or _has_cjk(t_back) or _has_cjk(t_energy) or _has_cjk(t_desc) or _has_cjk(t_ad_btn):
				_fail("[%s] 詞條存在 CJK 中文字元殘留！" % code)

		if _has_emoji(t_title) or _has_emoji(t_back) or _has_emoji(t_energy) or _has_emoji(t_desc) or _has_emoji(t_ad_btn):
			_fail("[%s] 詞條存在 Emoji！" % code)

		print("  ✓ [%s] 字典詞條檢核通過 (標題: '%s', 按鈕: '%s')" % [code, t_title, t_ad_btn % [3, 3]])

	print("\n--- 2. 驗證 EnergyLackDialog 實例與 locale_changed 即時動態連動 ---")
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	gs.reset_new_game()
	gs.energy = 2
	es.refresh()
	es.refresh_ad_daily()

	var dlg: Control = EnergyLackDialogClass.new()
	root.add_child(dlg)

	var title_node: Label = dlg.find_child("TitleLbl", true, false) as Label
	var back_node: Button = dlg.find_child("BackBtn", true, false) as Button
	var ad_btn_node: Button = dlg.find_child("WatchAdBtn", true, false) as Button
	var energy_lbl: Label = dlg.find_child("EnergyValLabel", true, false) as Label
	var desc_lbl: Label = dlg.find_child("DescLbl", true, false) as Label
	var status_lbl: Label = dlg.find_child("StatusDetailLabel", true, false) as Label
	var card_node: PanelContainer = dlg.find_child("EnergyLackCard", true, false) as PanelContainer
	var close_node: Button = dlg.find_child("CloseBtn", true, false) as Button

	if title_node == null or back_node == null or ad_btn_node == null or energy_lbl == null or desc_lbl == null:
		_fail("EnergyLackDialog 子節點查找失敗")
		dlg.queue_free()
		return

	# 尺寸規範驗證 (橫屏 740~760，關閉鈕 >= 50px)
	if card_node.custom_minimum_size.x < 740 or card_node.custom_minimum_size.x > 760:
		_fail("卡片寬度不符規範 (740~760): %f" % card_node.custom_minimum_size.x)
	else:
		print("  ✓ 卡片寬度符合規範: %f" % card_node.custom_minimum_size.x)

	if close_node == null or close_node.custom_minimum_size.x < 50 or close_node.custom_minimum_size.y < 50:
		_fail("關閉按鈕尺寸小於 50px: %s" % (close_node.custom_minimum_size if close_node else "null"))
	else:
		print("  ✓ 右上關閉按鈕尺寸符合規範: %s" % str(close_node.custom_minimum_size))

	# 初始繁中檢查
	if title_node.text != expected_title["zh_TW"]:
		_fail("初始繁中標題不符: %s" % title_node.text)
	if back_node.text != expected_back["zh_TW"]:
		_fail("初始繁中返回按鈕不符: %s" % back_node.text)
	if not ad_btn_node.text.contains("觀看廣告回復能量"):
		_fail("初始繁中看廣告按鈕不符: %s" % ad_btn_node.text)
	print("  ✓ 初始繁中內容驗證正確")

	# 動態切換六語系測試 (彈窗保持開啟狀態)
	for code in LOCALES:
		loc_node.call("set_locale", code)

		var exp_title: String = expected_title[code]
		var exp_back: String = expected_back[code]
		var exp_energy: String = expected_energy_fmt[code] % [gs.energy, 15]
		var exp_desc: String = expected_desc_normal[code]
		var exp_ad_btn: String = expected_btn_claim_normal_fmt[code] % [3, 3]

		if title_node.text != exp_title:
			_fail("[%s] 標題未即時更新: 實際 '%s'，期望 '%s'" % [code, title_node.text, exp_title])
		if back_node.text != exp_back:
			_fail("[%s] 返回按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, back_node.text, exp_back])
		if energy_lbl.text != exp_energy:
			_fail("[%s] 能量標籤未即時更新: 實際 '%s'，期望 '%s'" % [code, energy_lbl.text, exp_energy])
		if desc_lbl.text != exp_desc:
			_fail("[%s] 說明標籤未即時更新: 實際 '%s'，期望 '%s'" % [code, desc_lbl.text, exp_desc])
		if ad_btn_node.text != exp_ad_btn:
			_fail("[%s] 看廣告按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, ad_btn_node.text, exp_ad_btn])

		if code in ["en", "es"]:
			if _has_cjk(title_node.text) or _has_cjk(back_node.text) or _has_cjk(energy_lbl.text) or _has_cjk(desc_lbl.text) or _has_cjk(ad_btn_node.text):
				_fail("[%s] 畫面文字存在 CJK 中文字元殘留！" % code)

		if _has_emoji(title_node.text) or _has_emoji(back_node.text) or _has_emoji(energy_lbl.text) or _has_emoji(desc_lbl.text) or _has_emoji(ad_btn_node.text):
			_fail("[%s] 畫面文字存在 Emoji！" % code)

		print("  ✓ [%s] 開窗即時切換連動驗證成功: 標題='%s' | 按鈕='%s'" % [code, title_node.text, ad_btn_node.text])

	print("\n--- 3. 驗證已移除廣告模式 (has_removed_ads = true) 下的六語系即時切換 ---")
	gs.has_removed_ads = true
	dlg.call("_refresh_display")

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var exp_desc_no: String = expected_desc_no_ads[code]
		var exp_btn_no: String = expected_btn_claim_no_ads_fmt[code] % [3, 3]

		if desc_lbl.text != exp_desc_no:
			_fail("[%s] 免廣告說明未即時更新: 實際 '%s'，期望 '%s'" % [code, desc_lbl.text, exp_desc_no])
		if ad_btn_node.text != exp_btn_no:
			_fail("[%s] 免廣告按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, ad_btn_node.text, exp_btn_no])

		if code in ["en", "es"]:
			if _has_cjk(desc_lbl.text) or _has_cjk(ad_btn_node.text):
				_fail("[%s] 免廣告畫面文字存在 CJK 殘留！" % code)

		print("  ✓ [%s] 免廣告即時切換連動驗證成功: 按鈕='%s'" % [code, ad_btn_node.text])

	print("\n--- 4. 驗證次數上限耗盡模式下的六語系即時切換 ---")
	# 設為次數已用盡 (3/3)
	gs.set_flag("energy.ad_reward_count", 3)
	dlg.call("_refresh_display")

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var exp_btn_limit: String = expected_btn_limit_no_ads_fmt[code] % 3
		if ad_btn_node.text != exp_btn_limit:
			_fail("[%s] 次數用盡按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, ad_btn_node.text, exp_btn_limit])
		if not ad_btn_node.disabled:
			_fail("[%s] 次數用盡按鈕應為 disabled" % code)

		print("  ✓ [%s] 次數用盡按鈕即時切換連動驗證成功: 按鈕='%s'" % [code, ad_btn_node.text])

	# 測試完畢清理
	dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	gs.reset_new_game()
	print("  ✓ 測試清理與語系復原完成")
