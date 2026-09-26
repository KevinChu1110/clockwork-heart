extends SceneTree
## 聚魂殿抽魂畫面六語系單元測試 (Soul Draw View i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含標題、抽一格按鈕、去玩具堆邊緣按鈕、票數資訊、錯誤提示對應翻譯
## 2. 實例化 SoulDrawPlayView，在切換 locale 時，標題、按鈕、票數列、錯誤提示即時刷新連動
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const SoulDrawPlayView = preload("res://scripts/ui/soul_draw/soul_draw_play_view.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_SOUL_DRAW_I18N_OK")
					quit(0)
				else:
					push_error("TEST_SOUL_DRAW_I18N_FAIL")
					print("TEST_SOUL_DRAW_I18N_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_soul_draw_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		_fail("找不到 Loc autoload")
		return

	# 1. 驗證詞條字典解析
	var expected_title := {
		"zh_TW": "抽魂 · 封靈罐",
		"zh_CN": "抽魂 · 封灵罐",
		"en": "Soul Draw · Soul Canister",
		"ja": "抽魂 · 封霊缶",
		"ko": "추혼 · 봉령캔",
		"es": "Extracción de Almas · Recipiente de Almas",
	}
	var expected_btn_pull := {
		"zh_TW": "上緊——抽一格",
		"zh_CN": "上紧——抽一格",
		"en": "Wind Up — Draw 1",
		"ja": "巻き上げ——一回引く",
		"ko": "태엽 감기——1칸 뽑기",
		"es": "Dar Cuerda — Extraer 1",
	}
	var expected_btn_continue := {
		"zh_TW": "去玩具堆邊緣",
		"zh_CN": "去玩具堆边缘",
		"en": "To the Toy-pile Edge",
		"ja": "玩具の山の縁へ",
		"ko": "장난감 더미 가장자리로",
		"es": "Ir a la orilla del montón",
	}
	var expected_ticket_fmt := {
		"zh_TW": "封靈票 ×%d · 今日已抽 %d",
		"zh_CN": "封灵票 ×%d · 今日已抽 %d",
		"en": "Soul Tickets ×%d · Pulled Today: %d",
		"ja": "封霊券 ×%d · 本日抽選 %d",
		"ko": "봉령 티켓 ×%d · 오늘 뽑기 %d",
		"es": "Boletos de Alma ×%d · Extraídas Hoy: %d",
	}
	var expected_err_tickets := {
		"zh_TW": "封靈票不足",
		"zh_CN": "封灵票不足",
		"en": "Not enough Soul Tickets",
		"ja": "封霊券が不足しています",
		"ko": "봉령 티켓 부족",
		"es": "Boletos de alma insuficientes",
	}

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var t_val := ContentLoc.text("ui", "抽魂 · 封靈罐")
		if t_val != expected_title[code]:
			_fail("ContentLoc ui '抽魂 · 封靈罐' [%s] 預期 '%s' 實得 '%s'" % [code, expected_title[code], t_val])
		else:
			print("  ✓ [%s] 標題詞條符合: %s" % [code, t_val])

		var pull_val := ContentLoc.text("ui", "上緊——抽一格")
		if pull_val != expected_btn_pull[code]:
			_fail("ContentLoc ui '上緊——抽一格' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_pull[code], pull_val])
		else:
			print("  ✓ [%s] 抽一格詞條符合: %s" % [code, pull_val])

		var cont_val := ContentLoc.text("ui", "去玩具堆邊緣")
		if cont_val != expected_btn_continue[code]:
			_fail("ContentLoc ui '去玩具堆邊緣' [%s] 預期 '%s' 實得 '%s'" % [code, expected_btn_continue[code], cont_val])
		else:
			print("  ✓ [%s] 次按鈕詞條符合: %s" % [code, cont_val])

		var tkt_val := ContentLoc.text("ui", "封靈票 ×%d · 今日已抽 %d")
		if tkt_val != expected_ticket_fmt[code]:
			_fail("ContentLoc ui '封靈票 ×%%d · 今日已抽 %%d' [%s] 預期 '%s' 實得 '%s'" % [code, expected_ticket_fmt[code], tkt_val])
		else:
			print("  ✓ [%s] 票數格式符合: %s" % [code, tkt_val])

		var err_val := ContentLoc.text("ui", "封靈票不足")
		if err_val != expected_err_tickets[code]:
			_fail("ContentLoc ui '封靈票不足' [%s] 預期 '%s' 實得 '%s'" % [code, expected_err_tickets[code], err_val])
		else:
			print("  ✓ [%s] 錯誤提示詞條符合: %s" % [code, err_val])

	# 2. 測試 SoulDrawPlayView 動態節點與 locale_changed 即時刷新
	print("\n--- 2. 測試 SoulDrawPlayView 節點即時刷新 ---")
	loc_node.call("set_locale", "zh_TW")
	var view = SoulDrawPlayView.new()
	root_node.add_child(view)

	var title_lbl: Label = view.get_node_or_null("TitleLabel")
	var ticket_lbl: Label = view.get_node_or_null("TicketLabel")
	var pull_btn: Button = view.get_node_or_null("PullBtn")
	var cont_btn: Button = view.get_node_or_null("ContinueBtn")
	var err_lbl: Label = view.get_node_or_null("ErrorLabel")

	if title_lbl == null or ticket_lbl == null or pull_btn == null or cont_btn == null or err_lbl == null:
		_fail("SoulDrawPlayView 缺少必要的 UI 節點")
		view.queue_free()
		return

	# 模擬票數不足以觸發錯誤提示顯示
	view.econ.soul_tickets = 0
	view.call("_refresh")
	view.call("_on_pull")
	if err_lbl.text != "封靈票不足":
		_fail("觸發無票抽卡後，_err 預期為 '封靈票不足'，實得: " + err_lbl.text)

	# 輪巡所有語系，檢驗 view 內部文字是否隨 set_locale 自動刷新連動
	for code in LOCALES:
		loc_node.call("set_locale", code)
		if title_lbl.text != expected_title[code]:
			_fail("View 刷新 [%s] 標題文字錯誤: 預期 '%s' 實得 '%s'" % [code, expected_title[code], title_lbl.text])
		else:
			print("  ✓ [%s] View 標題即時刷新: %s" % [code, title_lbl.text])

		if pull_btn.text != expected_btn_pull[code]:
			_fail("View 刷新 [%s] 主按鈕文字錯誤: 預期 '%s' 實得 '%s'" % [code, expected_btn_pull[code], pull_btn.text])
		else:
			print("  ✓ [%s] View 主按鈕即時刷新: %s" % [code, pull_btn.text])

		if cont_btn.text != expected_btn_continue[code]:
			_fail("View 刷新 [%s] 次按鈕文字錯誤: 預期 '%s' 實得 '%s'" % [code, expected_btn_continue[code], cont_btn.text])
		else:
			print("  ✓ [%s] View 次按鈕即時刷新: %s" % [code, cont_btn.text])

		var fmt_str: String = expected_ticket_fmt[code]
		var exp_ticket_text: String = fmt_str % [view.econ.soul_tickets, view.daily.daily_soul_pulls]
		if ticket_lbl.text != exp_ticket_text:
			_fail("View 刷新 [%s] 票數文字錯誤: 預期 '%s' 實得 '%s'" % [code, exp_ticket_text, ticket_lbl.text])
		else:
			print("  ✓ [%s] View 票數列即時刷新: %s" % [code, ticket_lbl.text])

		if err_lbl.text != expected_err_tickets[code]:
			_fail("View 刷新 [%s] 錯誤提示文字錯誤: 預期 '%s' 實得 '%s'" % [code, expected_err_tickets[code], err_lbl.text])
		else:
			print("  ✓ [%s] View 錯誤提示即時刷新: %s" % [code, err_lbl.text])

	# 3. 測試 SoulResultCard 結果卡即時切換六語系（掉落種類與名稱）
	print("\n--- 3. 測試 SoulResultCard 結果卡即時切換六語系 ---")
	var card = view.card
	if card == null:
		_fail("找不到 view.card")
		view.queue_free()
		return

	var badge_lbl: Label = card.get_node_or_null("RarityBadge/BadgeLabel")
	var drop_lbl: Label = card.get_node_or_null("DropIdLabel")
	if badge_lbl == null or drop_lbl == null:
		_fail("SoulResultCard 缺少 BadgeLabel 或 DropIdLabel")
		view.queue_free()
		return

	var test_drops := [
		{
			"drop": {"DropId": "drop_brass_gear", "kind": "part"},
			"expected_badge": {
				"zh_TW": "零件",
				"zh_CN": "零件",
				"en": "Part",
				"ja": "パーツ",
				"ko": "부품",
				"es": "Pieza"
			},
			"expected_drop_lbl": {
				"zh_TW": "【零件】 黃銅齒輪",
				"zh_CN": "【零件】 黄铜齿轮",
				"en": "【Part】 Brass Gear",
				"ja": "【パーツ】 真鍮の歯車",
				"ko": "【부품】 황동 톱니바퀴",
				"es": "【Pieza】 Engranaje de latón"
			}
		},
		{
			"drop": {"DropId": "drop_spring_coil", "kind": "part"},
			"expected_badge": {
				"zh_TW": "零件",
				"zh_CN": "零件",
				"en": "Part",
				"ja": "パーツ",
				"ko": "부품",
				"es": "Pieza"
			},
			"expected_drop_lbl": {
				"zh_TW": "【零件】 發條游絲",
				"zh_CN": "【零件】 发条游丝",
				"en": "【Part】 Balance Spring",
				"ja": "【パーツ】 ヒゲゼンマイ",
				"ko": "【부품】 태엽 헤어스프링",
				"es": "【Pieza】 Espiral de cuerda"
			}
		},
		{
			"drop": {"DropId": "drop_core_shard", "kind": "part"},
			"expected_badge": {
				"zh_TW": "零件",
				"zh_CN": "零件",
				"en": "Part",
				"ja": "パーツ",
				"ko": "부품",
				"es": "Pieza"
			},
			"expected_drop_lbl": {
				"zh_TW": "【零件】 核心碎片",
				"zh_CN": "【零件】 核心碎片",
				"en": "【Part】 Core Shard",
				"ja": "【パーツ】 コアの破片",
				"ko": "【부품】 코어 조각",
				"es": "【Pieza】 Fragmento de núcleo"
			}
		},
		{
			"drop": {"DropId": "outfit_cream", "kind": "outfit"},
			"expected_badge": {
				"zh_TW": "換裝",
				"zh_CN": "换装",
				"en": "Outfit",
				"ja": "着せ替え",
				"ko": "의상",
				"es": "Atuendo"
			},
			"expected_drop_lbl": {
				"zh_TW": "【換裝】 小白 · 奶油便服",
				"zh_CN": "【换装】 小白 · 奶油便服",
				"en": "【Outfit】 Shiro · Cream Casual",
				"ja": "【着せ替え】 小白・クリーム普段着",
				"ko": "【의상】 시로 · 크림 일상복",
				"es": "【Atuendo】 Blanco · Atuendo Crema"
			}
		},
		{
			"drop": {"DropId": "outfit_brass_vest", "kind": "outfit"},
			"expected_badge": {
				"zh_TW": "換裝",
				"zh_CN": "换装",
				"en": "Outfit",
				"ja": "着せ替え",
				"ko": "의상",
				"es": "Atuendo"
			},
			"expected_drop_lbl": {
				"zh_TW": "【換裝】 獅 · 黃銅背心",
				"zh_CN": "【换装】 狮 · 黄铜背心",
				"en": "【Outfit】 Lion · Brass Vest",
				"ja": "【着せ替え】 獅子・真鍮ベスト",
				"ko": "【의상】 사자 · 황동 조끼",
				"es": "【Atuendo】 León · Chaleco de latón"
			}
		},
		{
			"drop": {"DropId": "outfit_scarf_tunic", "kind": "outfit"},
			"expected_badge": {
				"zh_TW": "換裝",
				"zh_CN": "换装",
				"en": "Outfit",
				"ja": "着せ替え",
				"ko": "의상",
				"es": "Atuendo"
			},
			"expected_drop_lbl": {
				"zh_TW": "【換裝】 狐 · 圍巾長衫",
				"zh_CN": "【换装】 狐 · 围巾长衫",
				"en": "【Outfit】 Fox · Scarf Tunic",
				"ja": "【着せ替え】 狐・マフラー長羽織",
				"ko": "【의상】 여우 · 목도리 긴옷",
				"es": "【Atuendo】 Zorro · Túnica con bufanda"
			}
		},
		{
			"drop": {"DropId": "outfit_worker_apron", "kind": "outfit"},
			"expected_badge": {
				"zh_TW": "換裝",
				"zh_CN": "换装",
				"en": "Outfit",
				"ja": "着せ替え",
				"ko": "의상",
				"es": "Atuendo"
			},
			"expected_drop_lbl": {
				"zh_TW": "【換裝】 野豬 · 工匠工裙",
				"zh_CN": "【换装】 野猪 · 工匠工裙",
				"en": "【Outfit】 Boar · Artisan Apron",
				"ja": "【着せ替え】 猪・職人エプロン",
				"ko": "【의상】 멧돼지 · 장인 작업치마",
				"es": "【Atuendo】 Jabalí · Delantal de artesano"
			}
		},
		{
			"drop": {"DropId": "junk_enamel_chip", "kind": "junk"},
			"expected_badge": {
				"zh_TW": "雜件",
				"zh_CN": "杂件",
				"en": "Junk",
				"ja": "ジャンク",
				"ko": "잡동사니",
				"es": "Chatarra"
			},
			"expected_drop_lbl": {
				"zh_TW": "【雜件】 搪瓷碎屑",
				"zh_CN": "【杂件】 搪瓷碎屑",
				"en": "【Junk】 Enamel Chips",
				"ja": "【ジャンク】 エナメル片",
				"ko": "【잡동사니】 에나멜 조각",
				"es": "【Chatarra】 Fragmento de esmalte"
			}
		}
	]

	for td in test_drops:
		var d: Dictionary = td["drop"]
		card.show_drop(d)
		for code in LOCALES:
			loc_node.call("set_locale", code)
			var exp_b: String = td["expected_badge"][code]
			var exp_d: String = td["expected_drop_lbl"][code]
			if badge_lbl.text != exp_b:
				_fail("Card 刷新 [%s] 種類徽章文字錯誤: 預期 '%s' 實得 '%s'" % [code, exp_b, badge_lbl.text])
			else:
				print("  ✓ [%s] Card 徽章即時刷新符合: %s" % [code, badge_lbl.text])
			if drop_lbl.text != exp_d:
				_fail("Card 刷新 [%s] 掉落名稱文字錯誤: 預期 '%s' 實得 '%s'" % [code, exp_d, drop_lbl.text])
			else:
				print("  ✓ [%s] Card 掉落名即時刷新符合: %s" % [code, drop_lbl.text])

	view.queue_free()
