extends SceneTree
## 木人樁結算卡六語系單元測試 (Dummy Settlement Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含結算卡標題、副標、三張卡片標籤/單位/說明、說明句、完成按鈕對應翻譯
## 2. 實例化 DummySettlementDialog，在切換 locale 時，標題、按鈕、各卡片標籤即時刷新連動
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留、零系統 emoji、數值不變

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const DummySettlementDialogClass = preload("res://scripts/battle/dummy_settlement_dialog.gd")

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
			print("TEST_DUMMY_SETTLEMENT_I18N_OK")
			quit(0)
		else:
			push_error("TEST_DUMMY_SETTLEMENT_I18N_FAIL")
			print("TEST_DUMMY_SETTLEMENT_I18N_FAIL")
			quit(1)
		return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		# Basic emoji blocks
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_dummy_settlement_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 預期詞條字典定義
	var expected_title := {
		"zh_TW": "木人試招數據卡",
		"zh_CN": "木人试招数据卡",
		"en": "Dummy Trial Report",
		"ja": "木人試技データカード",
		"ko": "목인 연습 데이터 카드",
		"es": "Ficha de prueba con muñeco",
	}

	var expected_sub := {
		"zh_TW": "武術館「招」軸訓練回饋 · 能量消耗 0",
		"zh_CN": "武术馆「招」轴训练反馈 · 能量消耗 0",
		"en": "Martial Hall Skill Training Feedback · Energy Cost: 0",
		"ja": "武術館「技」訓練フィードバック · エネルギー消費 0",
		"ko": "무술관 「기술」 훈련 피드백 · 에너지 소모 0",
		"es": "Entrenamiento en sala marcial · Coste de energía 0",
	}

	var expected_card1_header := {
		"zh_TW": "本次總傷害",
		"zh_CN": "本次总伤害",
		"en": "Total Damage",
		"ja": "総ダメージ",
		"ko": "총 피해량",
		"es": "Daño total",
	}

	var expected_card1_sub := {
		"zh_TW": "招式命中累積",
		"zh_CN": "招式命中累积",
		"en": "Cumulative Hits",
		"ja": "技命中累積",
		"ko": "기술 적중 누적",
		"es": "Impactos acumulados",
	}

	var expected_card1_unit := {
		"zh_TW": "點",
		"zh_CN": "点",
		"en": "pts",
		"ja": "pt",
		"ko": "점",
		"es": "pts",
	}

	var expected_card2_header := {
		"zh_TW": "試招耗時",
		"zh_CN": "试招耗时",
		"en": "Trial Duration",
		"ja": "試技時間",
		"ko": "연습 시간",
		"es": "Tiempo de prueba",
	}

	var expected_card2_sub := {
		"zh_TW": "戰鬥歷程秒數",
		"zh_CN": "战斗历程秒数",
		"en": "Combat Duration (s)",
		"ja": "戦闘時間（秒）",
		"ko": "전투 시간(초)",
		"es": "Duración en segundos",
	}

	var expected_card2_unit := {
		"zh_TW": "秒",
		"zh_CN": "秒",
		"en": "s",
		"ja": "秒",
		"ko": "초",
		"es": "s",
	}

	var expected_card3_header := {
		"zh_TW": "秒傷 (DPS)",
		"zh_CN": "秒伤 (DPS)",
		"en": "DPS",
		"ja": "秒間ダメージ (DPS)",
		"ko": "초당 피해량 (DPS)",
		"es": "DPS",
	}

	var expected_card3_sub := {
		"zh_TW": "每秒平均輸出",
		"zh_CN": "每秒平均输出",
		"en": "Avg Damage / Second",
		"ja": "毎秒平均ダメージ",
		"ko": "초당 평균 공격력",
		"es": "Daño medio / segundo",
	}

	var expected_card3_unit := {
		"zh_TW": "點 / 秒",
		"zh_CN": "点 / 秒",
		"en": "pts / s",
		"ja": "pt / 秒",
		"ko": "점 / 초",
		"es": "pts / s",
	}

	var expected_tip := {
		"zh_TW": "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。",
		"zh_CN": "木人桩为不消耗能量的自由试招训练。可在武术馆兵器架调配各色兵刃，体会不同招式的出招前摇与段数节奏。",
		"en": "Training dummy practice consumes no energy. Switch weapons at the Martial Hall rack to feel the wind-up and combo rhythm of each style.",
		"ja": "木人での試技はエネルギーを消費しない自由訓練です。武術館の武器架で多彩な武器を試し、技の発生や連撃のリズムを掴みましょう。",
		"ko": "목인 연습은 에너지를 소모하지 않는 자유 훈련입니다. 무술관 무기 거치대에서 다양한 무기를 골라 기술의 선딜레이와 연타 리듬을 익혀보세요.",
		"es": "La práctica con el muñeco no consume energía. Elige armas en el armero de la sala marcial para dominar los tiempos y el ritmo de cada técnica.",
	}

	var expected_confirm := {
		"zh_TW": "完成試招",
		"zh_CN": "完成试招",
		"en": "Finish Trial",
		"ja": "試技を終了",
		"ko": "연습 완료",
		"es": "Finalizar prueba",
	}

	# 1. 檢驗字典查表解析
	print("\n--- 檢驗 1: 六語系字典 ContentLoc 查表解析 ---")
	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "木人試招數據卡")
		if t_title != expected_title[code]:
			_fail("[%s] 標題不符: 期望 '%s'，得 '%s'" % [code, expected_title[code], t_title])

		var t_sub := ContentLoc.text("ui", "武術館「招」軸訓練回饋 · 能量消耗 0")
		if t_sub != expected_sub[code]:
			_fail("[%s] 副標不符: 期望 '%s'，得 '%s'" % [code, expected_sub[code], t_sub])

		var t_c1h := ContentLoc.text("ui", "本次總傷害")
		if t_c1h != expected_card1_header[code]:
			_fail("[%s] 卡1標題不符: 期望 '%s'，得 '%s'" % [code, expected_card1_header[code], t_c1h])

		var t_c1s := ContentLoc.text("ui", "招式命中累積")
		if t_c1s != expected_card1_sub[code]:
			_fail("[%s] 卡1說明不符: 期望 '%s'，得 '%s'" % [code, expected_card1_sub[code], t_c1s])

		var t_c1u := ContentLoc.text("ui", "點")
		if t_c1u != expected_card1_unit[code]:
			_fail("[%s] 卡1單位不符: 期望 '%s'，得 '%s'" % [code, expected_card1_unit[code], t_c1u])

		var t_c2h := ContentLoc.text("ui", "試招耗時")
		if t_c2h != expected_card2_header[code]:
			_fail("[%s] 卡2標題不符: 期望 '%s'，得 '%s'" % [code, expected_card2_header[code], t_c2h])

		var t_c2s := ContentLoc.text("ui", "戰鬥歷程秒數")
		if t_c2s != expected_card2_sub[code]:
			_fail("[%s] 卡2說明不符: 期望 '%s'，得 '%s'" % [code, expected_card2_sub[code], t_c2s])

		var t_c2u := ContentLoc.text("ui", "秒")
		if t_c2u != expected_card2_unit[code]:
			_fail("[%s] 卡2單位不符: 期望 '%s'，得 '%s'" % [code, expected_card2_unit[code], t_c2u])

		var t_c3h := ContentLoc.text("ui", "秒傷 (DPS)")
		if t_c3h != expected_card3_header[code]:
			_fail("[%s] 卡3標題不符: 期望 '%s'，得 '%s'" % [code, expected_card3_header[code], t_c3h])

		var t_c3s := ContentLoc.text("ui", "每秒平均輸出")
		if t_c3s != expected_card3_sub[code]:
			_fail("[%s] 卡3說明不符: 期望 '%s'，得 '%s'" % [code, expected_card3_sub[code], t_c3s])

		var t_c3u := ContentLoc.text("ui", "點 / 秒")
		if t_c3u != expected_card3_unit[code]:
			_fail("[%s] 卡3單位不符: 期望 '%s'，得 '%s'" % [code, expected_card3_unit[code], t_c3u])

		var t_tip := ContentLoc.text("ui", "木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。")
		if t_tip != expected_tip[code]:
			_fail("[%s] 說明句不符: 期望 '%s'，得 '%s'" % [code, expected_tip[code], t_tip])

		var t_conf := ContentLoc.text("ui", "完成試招")
		if t_conf != expected_confirm[code]:
			_fail("[%s] 確認按鈕不符: 期望 '%s'，得 '%s'" % [code, expected_confirm[code], t_conf])

		print("  ✓ [%s] 字典全部 13 條通過" % code)

	# 2. 檢驗 DummySettlementDialog 實例化與 locale_changed 動態刷新
	print("\n--- 檢驗 2: DummySettlementDialog 動態切換與節點即時刷新 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var stats := {
		"total_damage": 500,
		"elapsed_time": 12.8,
		"dps": 39.1,
	}

	var dlg: Control = DummySettlementDialogClass.show_dialog(root_node, stats)
	if dlg == null:
		_fail("DummySettlementDialog 實例化失敗")
		return

	var title_lbl: Label = dlg.find_child("TitleLabel", true, false)
	var sub_lbl: Label = dlg.find_child("SubTitleLabel", true, false)
	var tip_lbl: Label = dlg.find_child("TipLabel", true, false)
	var confirm_btn: Button = dlg.find_child("ConfirmButton", true, false)

	var c1: Control = dlg.find_child("TotalDamageCard", true, false)
	var c2: Control = dlg.find_child("ElapsedTimeCard", true, false)
	var c3: Control = dlg.find_child("DpsCard", true, false)

	var c1_hdr: Label = c1.find_child("HeaderLabel", true, false) if c1 else null
	var c1_sub: Label = c1.find_child("SubTagLabel", true, false) if c1 else null
	var c1_unit: Label = c1.find_child("UnitLabel", true, false) if c1 else null
	var c1_val: Label = c1.find_child("DamageValueLabel", true, false) if c1 else null

	var c2_hdr: Label = c2.find_child("HeaderLabel", true, false) if c2 else null
	var c2_sub: Label = c2.find_child("SubTagLabel", true, false) if c2 else null
	var c2_unit: Label = c2.find_child("UnitLabel", true, false) if c2 else null
	var c2_val: Label = c2.find_child("TimeValueLabel", true, false) if c2 else null

	var c3_hdr: Label = c3.find_child("HeaderLabel", true, false) if c3 else null
	var c3_sub: Label = c3.find_child("SubTagLabel", true, false) if c3 else null
	var c3_unit: Label = c3.find_child("UnitLabel", true, false) if c3 else null
	var c3_val: Label = c3.find_child("DpsValueLabel", true, false) if c3 else null

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		# 檢驗標題
		if not title_lbl or title_lbl.text != expected_title[code]:
			_fail("[%s] 節點 TitleLabel 刷新不符: 得 '%s'" % [code, title_lbl.text if title_lbl else "null"])
		# 檢驗副標
		if not sub_lbl or sub_lbl.text != expected_sub[code]:
			_fail("[%s] 節點 SubTitleLabel 刷新不符: 得 '%s'" % [code, sub_lbl.text if sub_lbl else "null"])

		# 檢驗卡片 1
		if not c1_hdr or c1_hdr.text != expected_card1_header[code]:
			_fail("[%s] 卡1 HeaderLabel 刷新不符: 得 '%s'" % [code, c1_hdr.text if c1_hdr else "null"])
		if not c1_sub or c1_sub.text != expected_card1_sub[code]:
			_fail("[%s] 卡1 SubTagLabel 刷新不符: 得 '%s'" % [code, c1_sub.text if c1_sub else "null"])
		if not c1_unit or c1_unit.text != expected_card1_unit[code]:
			_fail("[%s] 卡1 UnitLabel 刷新不符: 得 '%s'" % [code, c1_unit.text if c1_unit else "null"])

		# 檢驗卡片 2
		if not c2_hdr or c2_hdr.text != expected_card2_header[code]:
			_fail("[%s] 卡2 HeaderLabel 刷新不符: 得 '%s'" % [code, c2_hdr.text if c2_hdr else "null"])
		if not c2_sub or c2_sub.text != expected_card2_sub[code]:
			_fail("[%s] 卡2 SubTagLabel 刷新不符: 得 '%s'" % [code, c2_sub.text if c2_sub else "null"])
		if not c2_unit or c2_unit.text != expected_card2_unit[code]:
			_fail("[%s] 卡2 UnitLabel 刷新不符: 得 '%s'" % [code, c2_unit.text if c2_unit else "null"])

		# 檢驗卡片 3
		if not c3_hdr or c3_hdr.text != expected_card3_header[code]:
			_fail("[%s] 卡3 HeaderLabel 刷新不符: 得 '%s'" % [code, c3_hdr.text if c3_hdr else "null"])
		if not c3_sub or c3_sub.text != expected_card3_sub[code]:
			_fail("[%s] 卡3 SubTagLabel 刷新不符: 得 '%s'" % [code, c3_sub.text if c3_sub else "null"])
		if not c3_unit or c3_unit.text != expected_card3_unit[code]:
			_fail("[%s] 卡3 UnitLabel 刷新不符: 得 '%s'" % [code, c3_unit.text if c3_unit else "null"])

		# 檢驗說明句與確認鈕
		if not tip_lbl or tip_lbl.text != expected_tip[code]:
			_fail("[%s] 節點 TipLabel 刷新不符: 得 '%s'" % [code, tip_lbl.text if tip_lbl else "null"])
		if not confirm_btn or confirm_btn.text != expected_confirm[code]:
			_fail("[%s] 節點 ConfirmButton 刷新不符: 得 '%s'" % [code, confirm_btn.text if confirm_btn else "null"])

		# 檢驗數值保持一致
		if not c1_val or c1_val.text != "500":
			_fail("[%s] 卡1 總傷害數值被篡改: 得 '%s'" % [code, c1_val.text if c1_val else "null"])
		if not c2_val or c2_val.text != "12.8":
			_fail("[%s] 卡2 耗時數值被篡改: 得 '%s'" % [code, c2_val.text if c2_val else "null"])
		if not c3_val or c3_val.text != "39.1":
			_fail("[%s] 卡3 DPS 數值被篡改: 得 '%s'" % [code, c3_val.text if c3_val else "null"])

		# 檢驗零 emoji
		for txt in [title_lbl.text, sub_lbl.text, c1_hdr.text, c1_sub.text, c1_unit.text, c2_hdr.text, c2_sub.text, c2_unit.text, c3_hdr.text, c3_sub.text, c3_unit.text, tip_lbl.text, confirm_btn.text]:
			if _has_emoji(txt):
				_fail("[%s] 偵測到系統 Emoji: '%s'" % [code, txt])

		print("  ✓ [%s] 即時切換連動與文字/數值全數合格" % code)

	dlg.queue_free()
