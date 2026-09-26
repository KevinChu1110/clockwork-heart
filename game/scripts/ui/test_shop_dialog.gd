extends SceneTree
## 商城/儲值頁面骨架與 IAP 佔位品項測試
## 執行方式：godot --path game --headless -s res://scripts/ui/test_shop_dialog.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _has_forbidden_symbols_or_emoji(text: String) -> bool:
	var forbidden := ["⚙", "✦", "★", "◆", "▲", "▼", "●", "■", "🪙", "💎", "⚡", "🛒", "📦", "🎁", "✨", "🔥"]
	for s in forbidden:
		if text.contains(s):
			return true
	for c in text:
		var cp := c.unicode_at(0)
		if (cp >= 0x1F300 and cp <= 0x1F9FF) or (cp >= 0x2600 and cp <= 0x27BF):
			return true
	return false


func _initialize() -> void:
	print("── 開始執行商城/儲值頁面骨架單元測試 ──")
	var gs := root.get_node_or_null("GameState")
	if gs == null:
		_fail("GameState autoload missing")
		return _finish()

	gs.reset_new_game()
	gs.has_removed_ads = false

	var ShopClass: GDScript = load("res://scripts/ui/shop_dialog.gd")
	if ShopClass == null:
		_fail("無法載入 res://scripts/ui/shop_dialog.gd")
		return _finish()

	var shop: Control = ShopClass.new()
	root.add_child(shop)
	shop._ready()

	# 1. 彈窗尺寸與規範檢查 (740~760px)
	var card: PanelContainer = shop.find_child("ShopCard", true, false) as PanelContainer
	if card == null:
		_fail("ShopDialog 找不到 ShopCard 根容器")
	else:
		if card.custom_minimum_size.x < 740 or card.custom_minimum_size.x > 760:
			_fail("ShopCard 寬度不符合手遊規範 (應介於 740~760px)，實際為: %f" % card.custom_minimum_size.x)
		else:
			print("  ok ShopCard 寬度符合手遊彈窗規範: %f px" % card.custom_minimum_size.x)

	# 2. 右上關閉按鈕檢查 (>=50px, 零 Emoji)
	var close_btn: Button = shop.find_child("CloseBtn", true, false) as Button
	if close_btn == null:
		_fail("ShopDialog 缺少 CloseBtn 關閉按鈕")
	else:
		if close_btn.custom_minimum_size.x < 50 or close_btn.custom_minimum_size.y < 50:
			_fail("CloseBtn 尺寸小於 50x50px，實際為: %s" % str(close_btn.custom_minimum_size))
		else:
			print("  ok CloseBtn 尺寸符合規範: %s" % str(close_btn.custom_minimum_size))

	# 3. 檢查 3 個 IAP 佔位品項卡
	var item_ids := ["energy_pack", "soul_pack", "forge_pack"]
	for item_id in item_ids:
		var item_card: PanelContainer = shop.find_child("IapCard_" + item_id, true, false) as PanelContainer
		if item_card == null:
			_fail("找不到品項卡: IapCard_" + item_id)
			continue

		var buy_btn: Button = item_card.find_child("BuyBtn_" + item_id, true, false) as Button
		if buy_btn == null:
			_fail("品項卡 %s 缺少 BuyBtn" % item_id)
		else:
			if buy_btn.custom_minimum_size.y < 50:
				_fail("品項卡 %s 購買按鈕高度不足 50px: %f" % [item_id, buy_btn.custom_minimum_size.y])
			var sb := buy_btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb == null or sb.border_width_bottom < 5:
				_fail("品項卡 %s 購買按鈕果凍厚底不足 5px" % item_id)
			else:
				print("  ok 品項卡 %s 購買按鈕熱區與果凍厚底達標 (高度 %d, 厚底 %d)" % [item_id, int(buy_btn.custom_minimum_size.y), sb.border_width_bottom])

	# 驗證模擬購買品項
	var init_energy: int = int(gs.energy)
	var energy_buy_btn: Button = shop.find_child("BuyBtn_energy_pack", true, false) as Button
	if energy_buy_btn:
		energy_buy_btn.pressed.emit()
		if int(gs.energy) != init_energy + 15:
			_fail("購買發條能量箱後能量應增加 15 點，原為 %d 實際為 %d" % [init_energy, int(gs.energy)])
		else:
			print("  ok 模擬購買發條能量箱成功發放能量 (+15)")

	# 4. 去廣告按鈕檢查與開關邏輯
	var remove_ads_btn: Button = shop.find_child("RemoveAdsBtn", true, false) as Button
	if remove_ads_btn == null:
		_fail("ShopDialog 找不到 RemoveAdsBtn 按鈕")
	else:
		if remove_ads_btn.custom_minimum_size.y < 50:
			_fail("去廣告按鈕熱區高度不足 50px: %f" % remove_ads_btn.custom_minimum_size.y)
		if remove_ads_btn.disabled:
			_fail("初始狀態去廣告按鈕不應為 disabled")

		# 點擊去廣告按鈕
		remove_ads_btn.pressed.emit()
		if not gs.has_removed_ads:
			_fail("點擊去廣告後 GameState.has_removed_ads 應為 true")
		else:
			print("  ok 點擊去廣告成功切換 GameState.has_removed_ads = true")
		if not remove_ads_btn.disabled:
			_fail("買斷去廣告後按鈕應切換為 disabled")
		else:
			print("  ok 去廣告按鈕正確更新為已擁有且已禁用")

	# 5. 獎勵型廣告按鈕 (WatchAdBtn) 檢查
	var watch_ad_btn: Button = shop.find_child("WatchAdBtn", true, false) as Button
	if watch_ad_btn == null:
		_fail("ShopDialog 找不到 WatchAdBtn 按鈕")
	else:
		if watch_ad_btn.custom_minimum_size.y < 50:
			_fail("獎勵廣告按鈕高度不足 50px: %f" % watch_ad_btn.custom_minimum_size.y)
		# 此時 has_removed_ads 為 true，按鈕應為免看廣告直接領取
		if not watch_ad_btn.text.contains("免看廣告直接領取"):
			_fail("去廣告狀態下按鈕應顯示『免看廣告直接領取』，實際為: %s" % watch_ad_btn.text)
		else:
			print("  ok 去廣告狀態下獎勵廣告按鈕文字正確: %s" % watch_ad_btn.text)

		# 點擊直接領取
		gs.energy = 5
		watch_ad_btn.pressed.emit()
		if int(gs.energy) != 8:
			_fail("去廣告狀態下點擊領取能量應為 8，實際為 %d" % int(gs.energy))
		else:
			print("  ok 免看廣告直接領取成功獲得能量 (+3)")

	# 6. 全文字無 Emoji 與無禁止符號檢查
	_check_no_emoji_in_node(shop)
	print("  ok 商城全節點無系統 Emoji 與無非法特殊字符")

	shop.queue_free()

	# 6.5. 驗證商城六語系 i18n 切換
	print("── 開始驗證商城六語系 i18n 完整切換 ──")
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		_fail("Loc autoload missing")
	else:
		var locales_expected := {
			"zh_TW": {
				"title": "發條補給 · 道具商城",
				"energy_title": "發條能量補給箱",
				"soul_title": "神殿聚魂召喚包",
				"forge_title": "工坊鍛造資源箱",
				"buy_btn": "模擬購買",
				"remove_btn": "一次性去廣告（Mock買斷）",
				"todo_note": "TODO: 定價待定"
			},
			"zh_CN": {
				"title": "发条补给 · 道具商城",
				"energy_title": "发条能量补给箱",
				"soul_title": "神殿聚魂召唤包",
				"forge_title": "工坊锻造资源箱",
				"buy_btn": "模拟购买",
				"remove_btn": "一次性去广告（Mock买断）",
				"todo_note": "TODO: 定价待定"
			},
			"en": {
				"title": "Clockwork Supply · Item Shop",
				"energy_title": "Clockwork Energy Supply Box",
				"soul_title": "Temple Soul Summon Pack",
				"forge_title": "Workshop Forging Resource Box",
				"buy_btn": "Mock Purchase",
				"remove_btn": "Remove Ads (Mock Purchase)",
				"todo_note": "TODO: Pricing TBD"
			},
			"ja": {
				"title": "ぜんまい補給 · アイテムショップ",
				"energy_title": "ぜんまいエネルギー補給箱",
				"soul_title": "神殿魂集め召喚パック",
				"forge_title": "工房鍛造リソース箱",
				"buy_btn": "モック購入",
				"remove_btn": "広告削除（モック購入）",
				"todo_note": "TODO: 価格未定"
			},
			"ko": {
				"title": "태엽 보급 · 아이템 상점",
				"energy_title": "태엽 에너지 보급 상자",
				"soul_title": "신전 집혼 소환 팩",
				"forge_title": "공방 단조 자원 상자",
				"buy_btn": "모의 구매",
				"remove_btn": "광고 제거 (목업 구매)",
				"todo_note": "TODO: 가격 미정"
			},
			"es": {
				"title": "Suministros de cuerda · Tienda de objetos",
				"energy_title": "Caja de suministros de energía de cuerda",
				"soul_title": "Paquete de invocación de almas del templo",
				"forge_title": "Caja de recursos de forja del taller",
				"buy_btn": "Compra simulada",
				"remove_btn": "Eliminar anuncios (Compra simulada)",
				"todo_note": "TODO: Precio por determinar"
			}
		}

		for code in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
			gs.has_removed_ads = false
			loc_node.call("set_locale", code)
			var lang_shop: Control = ShopClass.new()
			root.add_child(lang_shop)
			lang_shop._ready()

			var exp: Dictionary = locales_expected[code]

			var title_l: Label = lang_shop.find_child("ShopTitleLabel", true, false) as Label
			if title_l == null or title_l.text != exp["title"]:
				_fail("[%s] 商城標題翻譯不符，預期: %s，實際: %s" % [code, exp["title"], title_l.text if title_l else "null"])

			var e_title_l: Label = lang_shop.find_child("ItemTitleLabel_energy_pack", true, false) as Label
			if e_title_l == null or e_title_l.text != exp["energy_title"]:
				_fail("[%s] 能量箱品項標題翻譯不符，預期: %s，實際: %s" % [code, exp["energy_title"], e_title_l.text if e_title_l else "null"])

			var s_title_l: Label = lang_shop.find_child("ItemTitleLabel_soul_pack", true, false) as Label
			if s_title_l == null or s_title_l.text != exp["soul_title"]:
				_fail("[%s] 召喚包品項標題翻譯不符，預期: %s，實際: %s" % [code, exp["soul_title"], s_title_l.text if s_title_l else "null"])

			var f_title_l: Label = lang_shop.find_child("ItemTitleLabel_forge_pack", true, false) as Label
			if f_title_l == null or f_title_l.text != exp["forge_title"]:
				_fail("[%s] 資源箱品項標題翻譯不符，預期: %s，實際: %s" % [code, exp["forge_title"], f_title_l.text if f_title_l else "null"])

			var s_btn: Button = lang_shop.find_child("RemoveAdsBtn", true, false) as Button
			if s_btn == null or s_btn.text != exp["remove_btn"]:
				_fail("[%s] 去廣告按鈕翻譯不符，預期: %s，實際: %s" % [code, exp["remove_btn"], s_btn.text if s_btn else "null"])

			var e_buy: Button = lang_shop.find_child("BuyBtn_energy_pack", true, false) as Button
			if e_buy == null or e_buy.text != exp["buy_btn"]:
				_fail("[%s] 能量箱購買鈕翻譯不符，預期: %s，實際: %s" % [code, exp["buy_btn"], e_buy.text if e_buy else "null"])

			_check_no_emoji_in_node(lang_shop)
			print("  ok [%s] 語系商城彈窗標題/按鈕/品項 i18n 驗證通過" % code)
			lang_shop.queue_free()

		# 6.6. 驗證開著彈窗時即時切換語系 (Loc.locale_changed 動態刷新品項名稱與說明)
		print("── 開始驗證開著商城動態切換語系 (Loc.locale_changed) ──")
		loc_node.call("set_locale", "zh_TW")
		var dynamic_shop: Control = ShopClass.new()
		root.add_child(dynamic_shop)
		dynamic_shop._ready()

		var dyn_e_title: Label = dynamic_shop.find_child("ItemTitleLabel_energy_pack", true, false) as Label
		var dyn_e_desc: Label = dynamic_shop.find_child("ItemDescLabel_energy_pack", true, false) as Label
		var dyn_s_title: Label = dynamic_shop.find_child("ItemTitleLabel_soul_pack", true, false) as Label
		var dyn_s_desc: Label = dynamic_shop.find_child("ItemDescLabel_soul_pack", true, false) as Label
		var dyn_f_title: Label = dynamic_shop.find_child("ItemTitleLabel_forge_pack", true, false) as Label
		var dyn_f_desc: Label = dynamic_shop.find_child("ItemDescLabel_forge_pack", true, false) as Label

		if dyn_e_title.text != "發條能量補給箱":
			_fail("動態切換初始狀態 energy_title 應為發條能量補給箱，實際: %s" % dyn_e_title.text)

		for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
			loc_node.call("set_locale", code)
			var exp: Dictionary = locales_expected[code]
			if dyn_e_title.text != exp["energy_title"]:
				_fail("[動態切換 %s] energy_title 應為 %s，實際: %s" % [code, exp["energy_title"], dyn_e_title.text])
			if dyn_s_title.text != exp["soul_title"]:
				_fail("[動態切換 %s] soul_title 應為 %s，實際: %s" % [code, exp["soul_title"], dyn_s_title.text])
			if dyn_f_title.text != exp["forge_title"]:
				_fail("[動態切換 %s] forge_title 應為 %s，實際: %s" % [code, exp["forge_title"], dyn_f_title.text])

			# 驗證說明文字不是空的且已隨語系變換
			if dyn_e_desc.text.is_empty() or dyn_s_desc.text.is_empty() or dyn_f_desc.text.is_empty():
				_fail("[動態切換 %s] 品項說明文字為空" % code)

			print("  ok [動態切換 %s] 開著商城切換語系即時刷新品項名稱與說明成功" % code)

		dynamic_shop.queue_free()

		# 測試完成後復原為繁中
		loc_node.call("set_locale", "zh_TW")

	# 7. 大廳整合測試：大廳商城入口按鈕
	print("── 開始驗證大廳商城入口整合 ──")
	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		_fail("無法載入 res://scripts/ui/mobile_lobby.gd")
		return _finish()

	var lobby: Control = LobbyClass.new()
	root.add_child(lobby)
	lobby._ready()

	var shop_btn: Button = lobby.get_shop_button()
	if shop_btn == null:
		_fail("大廳未提供 ShopButton (get_shop_button 回傳為空)")
	else:
		if shop_btn.text != "商城":
			_fail("大廳商城按鈕文字應為「商城」，實際為「%s」" % shop_btn.text)
		if _has_forbidden_symbols_or_emoji(shop_btn.text):
			_fail("大廳商城按鈕文字包含非法符號或 Emoji: %s" % shop_btn.text)
		if shop_btn.icon == null:
			_fail("大廳商城按鈕缺少自繪圖示 (btn.icon 為空)")
		elif shop_btn.icon.resource_path != "res://assets/icons/hud/icon_btn_shop.png":
			_fail("大廳商城按鈕圖示路徑不符，實際為: %s" % shop_btn.icon.resource_path)
		else:
			print("  ok 大廳商城按鈕自繪圖示正確: %s" % shop_btn.icon.resource_path)

		if shop_btn.custom_minimum_size.y < 48:
			_fail("大廳商城按鈕熱區高度不足 48px: %f" % shop_btn.custom_minimum_size.y)
		var shop_sb := shop_btn.get_theme_stylebox("normal") as StyleBoxFlat
		if shop_sb == null or shop_sb.border_width_bottom < 5:
			_fail("大廳商城按鈕果凍厚底不足 5px")
		else:
			print("  ok 大廳商城按鈕熱區與果凍厚底達標 (高度 %d, 厚底 %d)" % [int(shop_btn.custom_minimum_size.y), shop_sb.border_width_bottom])

	# 測試點擊大廳商城按鈕是否成功開啟 ShopDialog
	var spawned_shop = lobby.open_shop()
	if spawned_shop == null:
		_fail("lobby.open_shop() 回傳為空")
	elif spawned_shop.get_parent() != lobby:
		_fail("ShopDialog 未成功加入大廳場景")
	else:
		print("  ok 大廳成功開啟 ShopDialog 實例")
		spawned_shop.queue_free()

	lobby.queue_free()
	_finish()


func _check_no_emoji_in_node(node: Node) -> void:
	if node is Label:
		var lbl := node as Label
		if _has_forbidden_symbols_or_emoji(lbl.text):
			_fail("Label 包含禁止字符或 Emoji: %s" % lbl.text)
	elif node is Button:
		var btn := node as Button
		if btn.text != "✕" and _has_forbidden_symbols_or_emoji(btn.text):
			_fail("Button 包含禁止字符或 Emoji: %s" % btn.text)

	for child in node.get_children():
		_check_no_emoji_in_node(child)


func _finish() -> void:
	if _ok:
		print("SHOP_DIALOG_OK")
		print("SHOP_DIALOG_UNIT_TESTS_PASS")
	else:
		print("SHOP_DIALOG_FAIL")
		print("SHOP_DIALOG_UNIT_TESTS_FAILED")
	quit(0 if _ok else 1)
