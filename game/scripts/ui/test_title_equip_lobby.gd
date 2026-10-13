extends SceneTree
## 《發條之心》TitleWallDialog 支援點擊佩戴稱號與大廳頭頂稱號名牌即時刷新連動測試
## (test_title_equip_lobby.gd)
##
## 驗收規範：
## 1. GameState 持久化保存玩家當前佩戴稱號（預設「初出茅廬」），提供 get_equipped_title() 與 set_equipped_title()，支援 to_dict/from_dict 存檔。
## 2. TitleWallDialog 稱號牆卡片中，已解鎖稱號點擊支援「佩戴稱號」功能，顯示「✓ 佩戴中」高亮果凍標籤與金黃光框（COLOR_GOLD，底厚 6px）。
## 3. 大廳 mobile_lobby.gd 頭頂稱號名牌 _hero_title_tag 讀取 GameState 佩戴稱號即時刷新，換稱號即時更新文字。
## 4. 支援六語系動態切換：zh_TW, zh_CN, en, ja, ko, es，稱號名牌與狀態標籤即時連動，零系統原生 Emoji。
## 5. 哨兵輸出：TEST_TITLE_EQUIP_LOBBY_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const TitleWallDialogScn = preload("res://scripts/ui/title_wall_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_DEFAULT_TITLES: Dictionary = {
	"zh_TW": "初出茅廬",
	"zh_CN": "初出茅庐",
	"en": "Fledgling Novice",
	"ja": "駆け出し",
	"ko": "풋내기 모험가",
	"es": "Novato Principiante"
}
const EXPECTED_EQUIPPED_BADGE: Dictionary = {
	"zh_TW": "✓ 佩戴中",
	"zh_CN": "✓ 佩戴中",
	"en": "✓ Equipped",
	"ja": "✓ 装備中",
	"ko": "✓ 착용 중",
	"es": "✓ Equipado"
}
const EXPECTED_CLAW_PARRY_TITLES: Dictionary = {
	"zh_TW": "以劍抵爪",
	"zh_CN": "以剑抵爪",
	"en": "Sword Against Claw",
	"ja": "剣もて爪を受く",
	"ko": "검으로 발톱을 받다",
	"es": "Espada contra zarpa"
}

var _lobby: Control = null
var _dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_7269c551")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TITLE_EQUIP_LOBBY_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var buf := file.get_buffer(file.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	return ctx.finish().hex_encode()


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("_update_ui_texts"):
		_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 驗證 GameState 持久化保存與預設佩戴稱號 ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			# 預設值驗證
			gs.reset_new_game()
			var default_title: String = gs.get_equipped_title()
			if default_title != "初出茅廬":
				return _fail("GameState 預設佩戴稱號應為『初出茅廬』，實際為: %s" % default_title)
			print("  ok GameState.get_equipped_title() 預設值正確為『初出茅廬』")

			# 訊號發射驗證
			var signal_state := {"received": false, "title": ""}
			var conn = func(t: String):
				signal_state["received"] = true
				signal_state["title"] = t
			gs.equipped_title_changed.connect(conn)

			gs.set_equipped_title("看破者")
			if not signal_state["received"] or signal_state["title"] != "看破者":
				return _fail("set_equipped_title 未正確觸發 equipped_title_changed 訊號")
			if gs.get_equipped_title() != "看破者":
				return _fail("GameState 佩戴稱號未更新為『看破者』")
			gs.equipped_title_changed.disconnect(conn)
			print("  ok GameState.set_equipped_title() 成功更新並觸發 equipped_title_changed 訊號")

			# 存檔 round-trip 驗證
			var save_dict: Dictionary = gs.to_dict()
			if str(save_dict.get("equipped_title", "")) != "看破者":
				return _fail("GameState.to_dict() 未包含正確的 equipped_title: %s" % str(save_dict.get("equipped_title")))

			gs.reset_new_game()
			if gs.get_equipped_title() != "初出茅廬":
				return _fail("GameState.reset_new_game() 未還原預設佩戴稱號")

			gs.from_dict(save_dict)
			if gs.get_equipped_title() != "看破者":
				return _fail("GameState.from_dict() 未正確還原佩戴稱號『看破者』")
			print("  ok GameState.to_dict() / from_dict() 存檔 round-trip 持久化驗證通過")

			# 還原為初出茅廬以供大廳初始驗證
			gs.set_equipped_title("初出茅廬")
			_switch_locale("zh_TW")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證大廳頭頂稱號名牌 _hero_title_tag 初始顯示與即時連動 ===")
			var title_text: String = _lobby.call("get_hero_title_text")
			if title_text != "【初出茅廬】":
				return _fail("大廳初始頭頂稱號名牌文字應為『【初出茅廬】』，實際為: %s" % title_text)
			print("  ok 大廳初始頭頂名牌正確顯示『【初出茅廬】』")

			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_zh_TW_lobby_default_title.png"))

			# 透過 GameState 換稱號，準備在下一幀驗證即時刷新
			var gs: Node = root.get_node_or_null("GameState")
			gs.set_equipped_title("以劍抵爪")
			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var updated_text: String = _lobby.call("get_hero_title_text")
			if updated_text != "【以劍抵爪】":
				return _fail("GameState 變更佩戴稱號後，大廳頭頂名牌未即時刷新為『【以劍抵爪】』，實際為: %s" % updated_text)
			print("  ok GameState 變更佩戴稱號後，大廳頭頂名牌即時連動更新為『【以劍抵爪】』")

			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_zh_TW_lobby_equipped_linkage.png"))

			# 開啟稱號牆彈窗
			_dlg = _lobby.call("open_title_wall_dialog")
			if _dlg == null:
				return _fail("無法開啟 TitleWallDialog 稱號牆視窗")
			print("  ok 大廳成功開啟 TitleWallDialog 稱號牆視窗")

			var gs: Node = root.get_node_or_null("GameState")
			gs.set_flag("title.claw_parry", true)
			gs.set_flag("title.fog_seer", true)
			_dlg.call("_update_ui_texts")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			print("\n=== 3. 驗證 TitleWallDialog 點擊佩戴、金黃光框與高亮果凍標籤 ===")
			var card_claw := _dlg.call("get_card_by_flag", "title.claw_parry") as PanelContainer
			if card_claw == null:
				return _fail("稱號牆找不到『title.claw_parry』卡片")

			# 驗證當前已佩戴狀態
			var is_claw_eq: bool = _dlg.call("is_card_equipped", "title.claw_parry")
			if not is_claw_eq:
				return _fail("以劍抵爪卡片應為已佩戴狀態")

			var badge_claw: Label = card_claw.find_child("BadgeLabel", true, false) as Label
			if badge_claw == null or badge_claw.text != "✓ 佩戴中":
				return _fail("佩戴中卡片標籤應為『✓ 佩戴中』，實際為: %s" % (badge_claw.text if badge_claw else "null"))

			# 驗證金黃光框樣式 (StyleBoxFlat)
			var sb_claw = card_claw.get_theme_stylebox("panel")
			if not (sb_claw is StyleBoxFlat):
				return _fail("佩戴中卡片 StyleBox 應為 StyleBoxFlat")
			if (sb_claw as StyleBoxFlat).border_color != Color("#FFD028"):
				return _fail("佩戴中卡片邊框色應為金黃 #FFD028，實際為: %s" % str((sb_claw as StyleBoxFlat).border_color))
			if (sb_claw as StyleBoxFlat).border_width_bottom != 6:
				return _fail("佩戴中卡片立體果凍厚底應為 6px，實際為: %d" % (sb_claw as StyleBoxFlat).border_width_bottom)
			print("  ok 佩戴中卡片正確展示『✓ 佩戴中』高亮果凍標籤與金黃光框厚底 (6px)")

			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_zh_TW_title_wall_equip_claw_parry.png"))

			# 點擊已解鎖未佩戴之『看破者』切換佩戴
			var card_fog := _dlg.call("get_card_by_flag", "title.fog_seer") as PanelContainer
			if card_fog == null:
				return _fail("稱號牆找不到『title.fog_seer』卡片")

			_dlg.call("_on_card_clicked", card_fog)

			var gs: Node = root.get_node_or_null("GameState")
			if gs.get_equipped_title() != "看破者":
				return _fail("點擊看破者後 GameState 佩戴稱號未更新為『看破者』")

			# 驗證看破者轉為佩戴中，以劍抵爪恢復為已解鎖
			var badge_fog: Label = card_fog.find_child("BadgeLabel", true, false) as Label
			if badge_fog == null or badge_fog.text != "✓ 佩戴中":
				return _fail("看破者標籤應切換為『✓ 佩戴中』，實際為: %s" % (badge_fog.text if badge_fog else "null"))

			if badge_claw.text != "已解鎖":
				return _fail("舊稱號以劍抵爪標籤應恢復為『已解鎖』，實際為: %s" % badge_claw.text)

			var sb_claw_un := card_claw.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_claw_un.border_color != Color("#FFA010"):
				return _fail("未佩戴已解鎖卡片邊框應為暖橘 #FFA010")

			# 驗證大廳頭頂名牌同步更新為看破者
			var lobby_title: String = _lobby.call("get_hero_title_text")
			if lobby_title != "【看破者】":
				return _fail("點擊切換稱號後大廳名牌未即時更新為『【看破者】』，實際為: %s" % lobby_title)
			print("  ok 點擊切換稱號：舊稱號恢復『已解鎖』，新稱號切換『✓ 佩戴中』，大廳即時同步刷新！")

			# 驗證點擊未解鎖卡片不可佩戴
			var card_demon := _dlg.call("get_card_by_flag", "title.cleared") as PanelContainer
			if card_demon:
				card_demon.set_meta("is_unlocked", false)
				_dlg.call("_on_card_clicked", card_demon)
				if gs.get_equipped_title() != "看破者":
					return _fail("未解鎖卡片不應能被佩戴")
				print("  ok 未解鎖卡片防護有效，點擊無法佩戴")

			# 切換回以劍抵爪並準備多語系檢查
			_dlg.call("equip_title", "title.claw_parry")
			_switch_locale("en")
			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 4. 驗證英文語系 (en) 稱號牆與大廳連動 ===")
			# 截圖 04: 英文稱號牆 (包含 ✓ Equipped)
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_en_title_wall_equipped.png"))

			# 關閉彈窗回到大廳進行英文大廳截圖
			if _dlg and is_instance_valid(_dlg):
				_dlg.queue_free()
				_dlg = null
			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			# 截圖 05: 英文大廳頭頂名牌 【Sword Against Claw】
			var en_tag: String = _lobby.call("get_hero_title_text")
			if en_tag != "【Sword Against Claw】":
				return _fail("英文大廳名牌應為『【Sword Against Claw】』，實際為: %s" % en_tag)
			print("  ok 英文大廳頭頂名牌連動正常: %s" % en_tag)

			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_en_lobby_equipped_linkage.png"))

			# 重新開啟彈窗並切換至日語 (ja)
			_dlg = _lobby.call("open_title_wall_dialog")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set_flag("title.claw_parry", true)
			_switch_locale("ja")
			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 5. 驗證日語語系 (ja) 與六語系全量連動 ===")
			# 截圖 06: 日文稱號牆 (包含 ✓ 装備中)
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_ja_title_wall_equipped.png"))

			# 全量檢查六語系文字與無 Emoji 規範
			for loc in LOCALES:
				_switch_locale(loc)
				var exp_tag = "【%s】" % str(EXPECTED_CLAW_PARRY_TITLES[loc])
				var actual_tag: String = _lobby.call("get_hero_title_text")
				if actual_tag != exp_tag:
					return _fail("[%s] 大廳頭頂稱號名牌語系切換不符: 期望 '%s', 實際 '%s'" % [loc, exp_tag, actual_tag])

				var card_claw := _dlg.call("get_card_by_flag", "title.claw_parry") as PanelContainer
				var badge_claw: Label = card_claw.find_child("BadgeLabel", true, false) as Label
				var exp_badge: String = str(EXPECTED_EQUIPPED_BADGE[loc])
				if badge_claw == null or badge_claw.text != exp_badge:
					return _fail("[%s] 佩戴中卡片標籤語系切換不符: 期望 '%s', 實際 '%s'" % [loc, exp_badge, badge_claw.text if badge_claw else "null"])

				_check_no_emoji(actual_tag, "%s 大廳頭頂稱號名牌" % loc)
				_check_no_emoji(badge_claw.text, "%s 稱號卡片佩戴標籤" % loc)
				print("  ✓ [%s] 語系連動驗證通過 (名牌=%s, 標籤=%s, 零系統 Emoji)" % [loc, actual_tag, badge_claw.text])

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false
			print("\n=== 6. 實機截圖 SHA256 獨立性驗證 ===")
			if DisplayServer.get_name() != "headless":
				var keys := ["proof_01", "proof_02", "proof_03", "proof_04", "proof_05", "proof_06"]
				var seen_hashes: Dictionary = {}
				for k in keys:
					var h: String = _proof_hashes.get(k, "")
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 6 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 TitleWallDialog 佩戴稱號與大廳頭頂名牌連動測試全綠！")
			print("TEST_TITLE_EQUIP_LOBBY_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
