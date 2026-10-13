extends SceneTree
## 《發條之心》大廳聚魂殿堂新增『一鍵卸下』全部戰魂果凍按鈕與連動安全防護驗收測試
## (test_soul_hall_unequip_all.gd)
##
## 依據任務 t_1c1c709a 驗收標準：
## 1. 大廳聚魂殿堂面板新增『一鍵卸下』立體果凍按鈕（BtnUnequipAllSouls），高度 >= 50px，符合多巴胺亮色盤。
## 2. 串接 SoulSystem.unequip_all_souls()，將所有魂槽之戰魂安全卸回背包，支援空槽防呆提示 Toast。
## 3. 卸下後即時刷新聚魂殿面板 BBCode 狀態與戰力屬性。
## 4. 具備完整一鍵配置 (BtnAutoEquipSouls) 與一鍵卸下雙向操作體驗。
## 5. 支援六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換，歐美語系零 CJK 殘留、零系統 Emoji。
## 6. 印出 TEST_SOUL_HALL_UNEQUIP_ALL_OK 哨兵，0 SCRIPT ERROR，quit(0)。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

const EXPECTED_UNEQUIP_TEXTS: Dictionary = {
	"zh_TW": "一鍵卸下",
	"zh_CN": "一键卸下",
	"en": "Quick Unsocket",
	"ja": "一括解除",
	"ko": "일괄 해제",
	"es": "Desengarzar Todo"
}
const EXPECTED_AUTO_TEXTS: Dictionary = {
	"zh_TW": "一鍵配置",
	"zh_CN": "一键配置",
	"en": "Auto Equip",
	"ja": "一括装着",
	"ko": "일괄 장착",
	"es": "Auto-equipar"
}

var _ok := true
var _frame := 0
var _step := 0
var _wait := 0

var _lobby: Control = null
var _ss: Node = null
var _gs: Node = null
var _loc: Node = null

var _btn_unequip: Button = null
var _btn_auto: Button = null
var _rtl_bbcode: RichTextLabel = null

var _signal_unequipped_received := false
var _signal_unequipped_payload: Dictionary = {}
var _out_dir: String = ""


func _fail(msg: String) -> bool:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false
	quit(1)
	return true


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2713 and u != 0x2715):
			return true
	return false


func _initialize() -> void:
	print("=== 開始執行 test_soul_hall_unequip_all 驗收測試 (t_1c1c709a) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_1c1c709a")
	if DisplayServer.get_name() != "headless":
		DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_ss = root.get_node_or_null("SoulSystem")
	if _ss == null:
		var SsClass = load("res://scripts/systems/soul_system.gd")
		if SsClass:
			_ss = SsClass.new()
			_ss.name = "SoulSystem"
			root.add_child(_ss)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)

	if _lobby.has_signal("souls_unequipped"):
		_lobby.connect("souls_unequipped", func(res: Dictionary):
			_signal_unequipped_received = true
			_signal_unequipped_payload = res
		)


func _save_viewport(filename: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	var target := _out_dir.path_join(filename)
	img.save_png(target)
	print("  [CAPTURE] Saved proof: %s" % filename)


func _process(_delta: float) -> bool:
	_frame += 1
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				_lobby.open_soul_hall()
				return false
			_test_nodes_and_specs()
			_step = 1
			_wait = 0
			return false

		1:
			if _wait < 5:
				return false
			_test_empty_safeguard()
			_step = 2
			_wait = 0
			return false

		2:
			if _wait < 5:
				return false
			_setup_equipped_slots()
			_step = 3
			_wait = 0
			return false

		3:
			if _wait < 5:
				return false
			_save_viewport("proof_02_slots_equipped_zh_TW.png")
			_test_full_unequip_and_bbcode()
			_step = 4
			_wait = 0
			return false

		4:
			if _wait < 5:
				return false
			_save_viewport("proof_03_unequip_success_toast_zh_TW.png")
			_test_bidirectional_flow()
			_step = 5
			_wait = 0
			return false

		5:
			if _wait < 5:
				return false
			_save_viewport("proof_04_auto_equip_best_zh_TW.png")
			# 再次一鍵卸下，清空槽位供語系切換展示
			_lobby.call("unequip_all_souls")
			_step = 6
			_wait = 0
			return false

		6:
			# 切換 en
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "en")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 6:
				return false
			_check_locale_button("en")
			_save_viewport("proof_05_locale_en.png")
			_step = 7
			_wait = 0
			return false

		7:
			# 切換 ja
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ja")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 6:
				return false
			_check_locale_button("ja")
			_save_viewport("proof_06_locale_ja.png")
			_step = 8
			_wait = 0
			return false

		8:
			# 切換 ko
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "ko")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 6:
				return false
			_check_locale_button("ko")
			_save_viewport("proof_07_locale_ko.png")
			_step = 9
			_wait = 0
			return false

		9:
			# 切換 es
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "es")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 6:
				return false
			_check_locale_button("es")
			_save_viewport("proof_08_locale_es.png")
			_step = 10
			_wait = 0
			return false

		10:
			# 切換 zh_CN
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_CN")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 6:
				return false
			_check_locale_button("zh_CN")
			_save_viewport("proof_09_locale_zh_CN.png")
			_step = 11
			_wait = 0
			return false

		11:
			# 切換回 zh_TW
			if _wait < 2:
				if _loc and _loc.has_method("set_locale"):
					_loc.call("set_locale", "zh_TW")
				_lobby.call("_apply_locale_texts")
				return false
			if _wait < 4:
				return false
			_check_locale_button("zh_TW")
			_finish()
			return true

	return false


func _test_nodes_and_specs() -> void:
	print("\n--- 1. 驗證聚魂殿堂 BtnUnequipAllSouls 節點存在性與外觀規格 ---")
	_lobby.open_soul_hall()
	_btn_unequip = _lobby.call("get_soul_hall_unequip_all_btn") as Button
	if _btn_unequip == null or not is_instance_valid(_btn_unequip):
		_fail("找不到聚魂殿堂一鍵卸下按鈕 (get_soul_hall_unequip_all_btn / BtnUnequipAllSouls)")
		return

	if _btn_unequip.name != "BtnUnequipAllSouls":
		_fail("按鈕名稱應為 BtnUnequipAllSouls，實得: %s" % _btn_unequip.name)
		return

	if _btn_unequip.custom_minimum_size.y < 50.0:
		_fail("BtnUnequipAllSouls 高度小於 50px，實得: %f" % _btn_unequip.custom_minimum_size.y)
		return
	print("  ok BtnUnequipAllSouls 按鈕尺寸符合規範: 高度=%.1fpx (>= 50px), 寬度=%.1fpx" % [
		_btn_unequip.custom_minimum_size.y, _btn_unequip.custom_minimum_size.x
	])

	var font_size: int = _btn_unequip.get_theme_font_size("font_size")
	if font_size < 16:
		_fail("BtnUnequipAllSouls 字級小於 16px，實得: %d" % font_size)
		return
	print("  ok BtnUnequipAllSouls 字級符合規範: %dpx (>= 16px)" % font_size)

	var sb: StyleBox = _btn_unequip.get_theme_stylebox("normal")
	if not (sb is StyleBoxFlat):
		_fail("BtnUnequipAllSouls normal 樣式應為 StyleBoxFlat")
		return
	var sbf := sb as StyleBoxFlat

	var exp_pink := Color("#FF5E8A")
	if sbf.bg_color.to_html(false) != exp_pink.to_html(false):
		_fail("BtnUnequipAllSouls 背景色不符珊瑚粉 #FF5E8A，實得: #%s" % sbf.bg_color.to_html(false))
		return

	var exp_border := Color("#1F1A3A")
	if sbf.border_color.to_html(false) != exp_border.to_html(false):
		_fail("BtnUnequipAllSouls 描邊色不符深藍紫 #1F1A3A，實得: #%s" % sbf.border_color.to_html(false))
		return

	if sbf.border_width_bottom < 4:
		_fail("BtnUnequipAllSouls 果凍厚底小於 4px，實得: %d" % sbf.border_width_bottom)
		return

	if sbf.corner_radius_top_left < 16:
		_fail("BtnUnequipAllSouls 圓角小於 16px，實得: %d" % sbf.corner_radius_top_left)
		return

	var fc: Color = _btn_unequip.get_theme_color("font_color")
	if fc.to_html(false) != exp_border.to_html(false):
		_fail("BtnUnequipAllSouls 文字顏色不符 #1F1A3A，實得: #%s" % fc.to_html(false))
		return

	print("  ok BtnUnequipAllSouls 珊瑚粉立體果凍按鈕樣式合規 (珊瑚粉 #FF5E8A, 描邊 #1F1A3A, 厚底 %dpx, 圓角 %dpx)" % [
		sbf.border_width_bottom, sbf.corner_radius_top_left
	])

	# 檢查一鍵配置按鈕
	_btn_auto = _lobby.call("get_soul_hall_auto_equip_btn") as Button
	if _btn_auto == null or not is_instance_valid(_btn_auto):
		_fail("找不到聚魂殿堂一鍵配置按鈕 (get_soul_hall_auto_equip_btn / BtnAutoEquipSouls)")
		return
	if _btn_auto.name != "BtnAutoEquipSouls":
		_fail("一鍵配置按鈕名稱應為 BtnAutoEquipSouls，實得: %s" % _btn_auto.name)
		return
	print("  ok BtnAutoEquipSouls 按鈕節點存在性與命名合規")

	# 檢查 BBCode 面板
	_rtl_bbcode = _lobby.call("get_soul_hall_status_bbcode_label") as RichTextLabel
	if _rtl_bbcode == null or not is_instance_valid(_rtl_bbcode):
		_fail("找不到聚魂殿堂 BBCode 狀態標籤 (get_soul_hall_status_bbcode_label / SoulStatusBBCode)")
		return
	if not _rtl_bbcode.bbcode_enabled:
		_fail("SoulStatusBBCode 未開啟 bbcode_enabled")
		return
	print("  ok SoulStatusBBCode 節點存在且 bbcode_enabled 為 true")


func _test_empty_safeguard() -> void:
	print("\n--- 2. 驗證空槽點擊安全防呆判定 ---")
	_gs.reset_new_game()
	_gs.weapon_tier = 11
	_ss.ensure_slots()
	for i in range(_gs.soul_slots.size()):
		_gs.soul_slots[i] = ""
	_lobby.call("_refresh_soul_hall_ui")

	_signal_unequipped_received = false
	var res: Dictionary = _lobby.call("unequip_all_souls") as Dictionary
	if bool(res.get("changed", true)):
		_fail("空槽點擊時 changed 應為 false")
		return
	if int(res.get("count", -1)) != 0:
		_fail("空槽點擊時 count 應為 0")
		return

	print("  ok 空槽安全判定無變更 (changed=false, count=0)")
	_save_viewport("proof_01_empty_safeguard_zh_TW.png")


func _setup_equipped_slots() -> void:
	print("\n--- 3. 配置滿槽戰魂 ---")
	_gs.reset_new_game()
	_gs.weapon_tier = 11
	_ss.ensure_slots()

	var s1 := {"id": "soul_atk_01", "star": "銳齒之魂", "quality": "吉", "level": 1, "equipped": true}
	var s2 := {"id": "soul_def_01", "star": "固甲之魂", "quality": "大吉", "level": 1, "equipped": true}
	var s3 := {"id": "soul_hp_01", "star": "旋簧之魂", "quality": "稀世", "level": 1, "equipped": true}
	var s4 := {"id": "soul_all_01", "star": "全衡之魂", "quality": "神", "level": 1, "equipped": false}
	_gs.souls = [s1, s2, s3, s4]
	_gs.soul_slots = ["soul_atk_01", "soul_def_01", "soul_hp_01"]

	_lobby.call("_refresh_soul_hall_ui")

	var bb_before: String = _rtl_bbcode.text
	if bb_before.find("銳齒之魂") < 0 or bb_before.find("固甲之魂") < 0:
		_fail("卸下前 BBCode 應顯示已裝備之戰魂名稱")
		return
	print("  ok 卸下前 BBCode 正確顯示已入魂狀態")


func _test_full_unequip_and_bbcode() -> void:
	print("\n--- 4. 執行滿槽一鍵卸下回背包與 BBCode 即時刷新 ---")
	_signal_unequipped_received = false
	var res: Dictionary = _lobby.call("unequip_all_souls") as Dictionary
	if not bool(res.get("changed", false)):
		_fail("滿槽一鍵卸下 changed 應為 true")
		return
	if int(res.get("count", 0)) != 3:
		_fail("滿槽一鍵卸下 count 應為 3，實得: %d" % int(res.get("count", 0)))
		return

	# 驗證槽位全空
	for i in range(_gs.soul_slots.size()):
		var sid: String = str(_gs.soul_slots[i])
		if not sid.is_empty():
			_fail("槽位 %d 未清空: %s" % [i, sid])
			return
	print("  ok 三大魂槽位完全清空為 \"\"")

	# 驗證背包內所有戰魂之 equipped 均為 false
	for s in _gs.souls:
		if bool(s.get("equipped", false)):
			_fail("戰魂 %s equipped 未重設為 false" % str(s.get("id", "")))
			return
	var bag: Array = _ss.bag_souls()
	if bag.size() != 4:
		_fail("背包戰魂數應為 4，實得: %d" % bag.size())
		return
	print("  ok 所有戰魂安全返還背包，bag_souls 包含全部 4 顆戰魂")

	# 驗證 BBCode 即時更新
	var bb_after: String = _rtl_bbcode.text
	if bb_after.find("槽1：空") < 0 or bb_after.find("槽2：空") < 0 or bb_after.find("槽3：空") < 0:
		_fail("卸下後 BBCode 應顯示槽位為空，實得:\n%s" % bb_after)
		return
	print("  ok 卸下後 BBCode 即時刷新為空槽狀態")

	# 驗證訊號觸發
	if not _signal_unequipped_received:
		_fail("未收到 souls_unequipped 訊號")
		return
	print("  ok souls_unequipped 訊號正確廣播")


func _test_bidirectional_flow() -> void:
	print("\n--- 5. 驗證一鍵配置與一鍵卸下雙向操作閉環 ---")
	var res_auto: Dictionary = _lobby.call("auto_equip_souls") as Dictionary
	if not bool(res_auto.get("ok", false)) or not bool(res_auto.get("changed", false)):
		_fail("一鍵配置應成功且 changed=true")
		return
	var slots: Array = [str(_gs.soul_slots[0]), str(_gs.soul_slots[1]), str(_gs.soul_slots[2])]
	if slots.has(""):
		_fail("一鍵配置後槽位不應有空槽: %s" % str(slots))
		return
	print("  ok 一鍵配置成功填滿最佳戰魂: %s" % str(slots))


func _check_locale_button(loc: String) -> void:
	var exp_txt: String = str(EXPECTED_UNEQUIP_TEXTS.get(loc, "一鍵卸下"))
	var cur_txt: String = _btn_unequip.text
	if cur_txt != exp_txt:
		_fail("[%s] BtnUnequipAllSouls 文案不符，期望: '%s'，實得: '%s'" % [loc, exp_txt, cur_txt])
		return

	if _has_emoji(cur_txt):
		_fail("[%s] BtnUnequipAllSouls 殘留 Emoji: '%s'" % [loc, cur_txt])
		return

	if loc in ["en", "es"]:
		if _has_cjk(cur_txt):
			_fail("[%s] 歐美語系殘留 CJK: '%s'" % [loc, cur_txt])
			return

	print("  ok [%s] 語系切換正常: '%s' (零 CJK, 零 Emoji)" % [loc, cur_txt])


func _finish() -> void:
	print("\n========================================================")
	print("🎉 所有驗證全數通過！TEST_SOUL_HALL_UNEQUIP_ALL_OK")
	print("========================================================\n")
	quit(0)
