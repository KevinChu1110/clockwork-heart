extends SceneTree
## 一次性去廣告假買斷與節點跳過廣告把關測試
## 執行方式：godot --path game --headless -s res://scripts/systems/test_remove_ads_mock.gd

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var gs := root.get_node_or_null("GameState")
	var en := root.get_node_or_null("EnergySystem")
	if gs == null or en == null:
		_fail("GameState／EnergySystem autoload missing")
		return _finish()

	gs.reset_new_game()
	en.refresh_ad_daily()

	var EnergyLackDialogClass: GDScript = load("res://scripts/ui/energy_lack_dialog.gd")
	var BattleDefeatDialogClass: GDScript = load("res://scripts/battle/battle_defeat_dialog.gd")
	var MobileSettingsClass: GDScript = load("res://scripts/ui/mobile_settings.gd")

	if EnergyLackDialogClass == null or BattleDefeatDialogClass == null or MobileSettingsClass == null:
		_fail("無法載入對應 UI 腳本")
		return _finish()

	# ── 1. 預設 false 狀態：正常顯示觀看廣告按鈕 ──
	if gs.has_removed_ads:
		_fail("新遊戲初始 has_removed_ads 應為 false")

	var lack_dlg1 = EnergyLackDialogClass.new()
	lack_dlg1._ready()
	root.add_child(lack_dlg1)
	var lack_btn1: Button = lack_dlg1.get_node_or_null("%WatchAdBtn")
	if lack_btn1 == null:
		lack_btn1 = lack_dlg1.find_child("WatchAdBtn", true, false) as Button
	if lack_btn1 == null:
		_fail("EnergyLackDialog 找不到 WatchAdBtn 按鈕")
	else:
		if not lack_btn1.text.contains("觀看廣告"):
			_fail("預設 false 時體力不足按鈕應包含『觀看廣告』，實際為: " + lack_btn1.text)
		if lack_btn1.text.contains("已移除廣告"):
			_fail("預設 false 時體力不足按鈕不應包含『已移除廣告』，實際為: " + lack_btn1.text)
		print("  ok 預設狀態體力不足按鈕正常顯示觀看廣告文字: ", lack_btn1.text)
	lack_dlg1.queue_free()

	var defeat_dlg1 = BattleDefeatDialogClass.new()
	defeat_dlg1._ready()
	root.add_child(defeat_dlg1)
	var revive_btn1: Button = defeat_dlg1.get_node_or_null("%ReviveAdBtn")
	if revive_btn1 == null:
		revive_btn1 = defeat_dlg1.find_child("ReviveAdBtn", true, false) as Button
	if revive_btn1 == null:
		_fail("BattleDefeatDialog 找不到 ReviveAdBtn 按鈕")
	else:
		if not revive_btn1.text.contains("觀看廣告"):
			_fail("預設 false 時戰鬥失敗按鈕應包含『觀看廣告』，實際為: " + revive_btn1.text)
		if revive_btn1.text.contains("已移除廣告"):
			_fail("預設 false 時戰鬥失敗按鈕不應包含『已移除廣告』，實際為: " + revive_btn1.text)
		print("  ok 預設狀態戰鬥失敗按鈕正常顯示觀看廣告文字: ", revive_btn1.text)
	defeat_dlg1.queue_free()

	# ── 2. 設定彈窗切換移除廣告開關 ──
	var settings_dlg = MobileSettingsClass.new()
	settings_dlg._ready()
	root.add_child(settings_dlg)
	var remove_btn: Button = settings_dlg.find_child("RemoveAdsBtn", true, false) as Button
	if remove_btn == null:
		_fail("MobileSettings 找不到 RemoveAdsBtn 按鈕")
	else:
		if not remove_btn.text.contains("移除廣告（測試用開關）"):
			_fail("設定按鈕名稱應包含『移除廣告（測試用開關）』，實際為: " + remove_btn.text)
		# 點擊切換為 true
		settings_dlg._on_toggle_remove_ads()
		if not gs.has_removed_ads:
			_fail("切換設定後 GameState.has_removed_ads 應為 true")
		if not remove_btn.text.contains("已啟用"):
			_fail("啟用後按鈕應顯示已啟用標記，實際為: " + remove_btn.text)
		print("  ok 設定彈窗成功切換移除廣告開關為 true: ", remove_btn.text)
	settings_dlg.queue_free()

	# ── 3. has_removed_ads = true 時：按鈕文字改為『已移除廣告，直接領取』，不再出現『觀看廣告』 ──
	var lack_dlg2 = EnergyLackDialogClass.new()
	lack_dlg2._ready()
	root.add_child(lack_dlg2)
	var lack_btn2: Button = lack_dlg2.find_child("WatchAdBtn", true, false) as Button
	if lack_btn2 == null:
		_fail("EnergyLackDialog (true) 找不到 WatchAdBtn 按鈕")
	else:
		if not lack_btn2.text.contains("已移除廣告，直接領取"):
			_fail("去廣告後體力按鈕應包含『已移除廣告，直接領取』，實際為: " + lack_btn2.text)
		if lack_btn2.text.contains("觀看廣告"):
			_fail("去廣告後體力按鈕不應再包含『觀看廣告』，實際為: " + lack_btn2.text)
		print("  ok 體力不足彈窗按鈕文字正確變更: ", lack_btn2.text)

		# 驗證跳過廣告播放直接發放體力
		gs.energy = 5
		var energy_granted_called := [false]
		lack_dlg2.energy_granted.connect(func(_amt: int): energy_granted_called[0] = true)
		lack_dlg2._on_watch_ad_clicked()

		if not energy_granted_called[0]:
			_fail("點擊領取後未發送 energy_granted 信號")
		if int(gs.energy) != 8:
			_fail("跳過廣告直接發放後能量應為 8，實際為 %d" % int(gs.energy))
		var mock_ad_child = lack_dlg2.find_child("MockAdDialog", true, false)
		if mock_ad_child != null:
			_fail("去廣告模式下不應生成 MockAdDialog")
		print("  ok 體力不足彈窗跳過廣告直接發放 3 點能量（5 -> 8）")
	lack_dlg2.queue_free()

	var defeat_dlg2 = BattleDefeatDialogClass.new()
	defeat_dlg2._ready()
	root.add_child(defeat_dlg2)
	var revive_btn2: Button = defeat_dlg2.find_child("ReviveAdBtn", true, false) as Button
	if revive_btn2 == null:
		_fail("BattleDefeatDialog (true) 找不到 ReviveAdBtn 按鈕")
	else:
		if not revive_btn2.text.contains("已移除廣告，直接領取"):
			_fail("去廣告後復活按鈕應包含『已移除廣告，直接領取』，實際為: " + revive_btn2.text)
		if revive_btn2.text.contains("觀看廣告"):
			_fail("去廣告後復活按鈕不應再包含『觀看廣告』，實際為: " + revive_btn2.text)
		print("  ok 戰鬥失敗彈窗按鈕文字正確變更: ", revive_btn2.text)

		# 驗證跳過廣告播放直接復活
		var revive_signal_called := [false]
		defeat_dlg2.revive_selected.connect(func(): revive_signal_called[0] = true)
		defeat_dlg2._on_revive_ad_clicked()

		if not revive_signal_called[0]:
			_fail("點擊領取後未發送 revive_selected 信號")
		var mock_ad_child2 = defeat_dlg2.find_child("MockAdDialog", true, false)
		if mock_ad_child2 != null:
			_fail("去廣告模式下不應生成 MockAdDialog")
		print("  ok 戰鬥失敗彈窗跳過廣告直接觸發二次機會復活")
	defeat_dlg2.queue_free()

	# ── 4. 存檔與讀檔序列化驗證 ──
	var save_dict: Dictionary = gs.to_dict()
	if not save_dict.has("has_removed_ads"):
		_fail("GameState.to_dict 缺少 has_removed_ads 欄位")
	elif not bool(save_dict["has_removed_ads"]):
		_fail("GameState.to_dict 的 has_removed_ads 應為 true")
	else:
		print("  ok 存檔字典序列化包含 has_removed_ads = true")

	# 重置後再讀取還原
	gs.has_removed_ads = false
	gs.from_dict(save_dict)
	if not gs.has_removed_ads:
		_fail("GameState.from_dict 還原後 has_removed_ads 應為 true")
	else:
		print("  ok 存檔字典還原後 has_removed_ads 正確為 true")

	# ── 5. 去廣告新增文案五語系 i18n 覆蓋驗證 ──
	var ContentLocClass := preload("res://scripts/systems/content_loc.gd")
	var remove_ads_keys: Array[String] = [
		"已移除廣告，直接領取  (%d/%d)",
		"已移除廣告，直接領取 (+3)  (%d/%d)",
		"今日領取次數已達上限 (0/%d)",
		"二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！",
		"出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！",
		"加值權限與功能測試",
		"移除廣告（測試用開關）",
		"· 已啟用",
		"· 未啟用",
		"已啟用移除廣告功能！",
		"已重置移除廣告狀態！"
	]
	for loc_code in ["en", "ja", "ko", "es", "zh_CN"]:
		var tbl: Dictionary = ContentLocClass._table("ui", loc_code)
		for k in remove_ads_keys:
			if not tbl.has(k):
				_fail("[%s] 去廣告文案缺少 i18n 譯文：%s" % [loc_code, k])
	print("  ok 去廣告 11 項文案五語系覆蓋正常（en, ja, ko, es, zh_CN）")

	_finish()


func _finish() -> void:
	if _ok:
		print("REMOVE_ADS_MOCK_OK")
		quit(0)
	else:
		print("REMOVE_ADS_MOCK_FAIL")
		quit(1)
