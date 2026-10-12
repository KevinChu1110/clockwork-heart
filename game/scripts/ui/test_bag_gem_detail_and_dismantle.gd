extends SceneTree
## 無頭與實機單元測試：背包Tab裝備詳情顯示已鑲寶石並於拆解時安全返還 (t_2d2436f1)
##
## 覆蓋驗收項目：
## 1. GemSystem.get_gem_socket_info 數值與標籤計算精確性：
##    - 紅寶石 (red): 武器 -> 暴擊 (+2.0/lv)、防具/裝備 -> 生命% (+3.0%/lv)
##    - 黃寶石 (yellow): 武器 -> 攻擊% (+4.0%/lv)、防具/裝備 -> 防禦% (+4.0%/lv)
##    - 藍寶石 (blue): 武器 -> 命中 (+3.0/lv)、防具/裝備 -> 迴避 (+3.0/lv)
##    - 星級標籤 (凡、良、優、精、極) 與色碼高對比度 (#C2185B, #9A6B00, #1565C0)
## 2. 背包Tab選中裝備時 (_update_bag_detail) 詳情面板顯示：
##    - 未鑲嵌寶石之裝備：正常顯示器階與品質，不顯示寶石標籤，類型為「類型：武器」
##    - 鑲嵌寶石之裝備 (inst.gem)：類型切換為「類型：武器（已鑲寶石）」，詳情內清楚顯示寶石名稱、星級、屬性加成與高對比色碼標籤
## 3. 裝備拆解回收安全返還 (EquipmentSystem.dismantle)：
##    - 帶寶石裝備拆解時，自動將該寶石完整退回 GemSystem（add_gem / GameState.gem_bag）
##    - GemSystem 寶石儲備數量精確 +1，且寶石屬性 (color, level) 完全一致
##    - 拆解回傳 msg 與 Toast 清楚提示『返還寶石』
##    - 鐵屑 (iron_scrap) 與金幣 (gold) 依器階與品質正常入帳
## 4. 安全守門 (Protection)：
##    - 裝備鎖定時 (is_locked) 或穿戴中 (is_equipped)，拆解嚴格阻擋，寶石不退回、裝備不被銷毀
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 完整支援與零殘留、零 Emoji
## 6. 實機渲染存證：OpenGL3 下擷取真實截圖存證並驗證 SHA256 獨立不重複

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _wait := 0
var _lobby: Control = null
var _gs: Node = null
var _eq: Node = null
var _inv: Node = null
var _gem: Node = null
var _loc: Node = null
var _out_dir: String = ""
var _proof_hashes: Array[String] = []

var _proof_gem_weapon_uid := ""
var _proof_plain_weapon_uid := ""
var _proof_yellow_gem_uid := ""

func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false

func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			return true
	return false

func _initialize() -> void:
	print("=== 開始執行背包Tab裝備詳情已鑲寶石與拆解返還單元測試 (t_2d2436f1) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_2d2436f1")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_inv = root.get_node_or_null("InventorySystem")
	if _inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			_inv = InvClass.new()
			_inv.name = "InventorySystem"
			root.add_child(_inv)

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq = EqClass.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)

	_gem = root.get_node_or_null("GemSystem")
	if _gem == null:
		var GemClass = load("res://scripts/systems/gem_system.gd")
		if GemClass:
			_gem = GemClass.new()
			_gem.name = "GemSystem"
			root.add_child(_gem)

	if _gs == null or _loc == null or _inv == null or _eq == null or _gem == null:
		_fail("Autoload 節點初始化失敗")
		quit(1)
		return

	_gs.call("reset_new_game", "rabbit")
	_loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ✓ MobileLobby 初始化成功")

func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		0:
			_test_gem_socket_info_calculations()
			_step = 1
		1:
			_test_bag_detail_display()
			_step = 2
		2:
			_test_dismantle_safe_refund()
			_step = 3
		3:
			_test_locked_and_equipped_protection()
			_step = 4
		4:
			_test_six_locales()
			_step = 5
		5:
			# 切換至背包 Tab 準備實機截圖存證
			_lobby.call("_switch_tab", 4) # Tab.BAG == 4
			_setup_proof_items()
			_step = 6
		6:
			# 截圖 1: 選中帶紅寶石之武器，詳情顯示寶石名稱、星級與暴擊加成
			_lobby.set("_selected_bag_item", _proof_gem_weapon_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_01_bag_weapon_with_gem_selected_zh_TW.png")
			_wait = 0
			_step = 7
		7:
			# 截圖 2: 選中無寶石之普通武器，詳情無寶石資訊
			_lobby.set("_selected_bag_item", _proof_plain_weapon_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_02_bag_weapon_without_gem_selected.png")
			_wait = 0
			_step = 8
		8:
			# 截圖 3: 英文語系 (en) 選中黃寶石武器，顯示 Socketed Gem: Topaz · 3 Star (Rare) · Attack % +12.0%
			_loc.call("set_locale", "en")
			ContentLoc.reload()
			_lobby.call("_apply_locale_texts")
			_lobby.set("_selected_bag_item", _proof_yellow_gem_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_03_bag_weapon_with_yellow_gem_en.png")
			_loc.call("set_locale", "zh_TW")
			ContentLoc.reload()
			_lobby.call("_apply_locale_texts")
			_wait = 0
			_step = 9
		9:
			# 截圖 4: 點擊拆解回收帶寶石之裝備，Toast 提示「返還寶石【紅寶石 · 1 級】」
			_lobby.set("_selected_bag_item", _proof_gem_weapon_uid)
			_lobby.call("_refresh_bag_tab", false)
			var btn: Button = _lobby.get_bag_dismantle_button()
			if btn:
				btn.pressed.emit()
			_wait = 0
			_step = 10
		10:
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_04_bag_dismantle_toast_refund_gem.png")
			_wait = 0
			_step = 11
		11:
			# 截圖 5: 開啟手藝工坊寶石彈窗 (GemWorkshopDialog)，證明返還的紅寶石確實已安全進駐 GemSystem 寶石背包
			var GemWorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
			if GemWorkshopClass:
				var dlg = GemWorkshopClass.new()
				dlg.name = "ProofGemWorkshopDialog"
				root.add_child(dlg)
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save(_out_dir + "/proof_05_gem_safe_in_gem_workshop.png")
			_step = 20
		20:
			if _ok:
				print("\n=======================================================")
				print("TEST_BAG_GEM_DETAIL_AND_DISMANTLE_OK")
				print("=======================================================")
				quit(0)
			else:
				push_error("\nTEST_BAG_GEM_DETAIL_AND_DISMANTLE_FAIL")
				quit(1)

	return false

## 1. 測試 GemSystem.get_gem_socket_info 核心計算
func _test_gem_socket_info_calculations() -> void:
	print("\n--- 1. 測試 GemSystem.get_gem_socket_info 核心屬性計算 ---")
	# 紅寶石 1 級 武器
	var r1_wpn: Dictionary = _gem.get_gem_socket_info({"color": "red", "level": 1}, "weapon")
	assert(str(r1_wpn.get("color", "")) == "red", "color 應為 red")
	assert(int(r1_wpn.get("level", 0)) == 1, "level 應為 1")
	assert(str(r1_wpn.get("color_name", "")) == "紅寶石", "名稱應為 紅寶石")
	assert(str(r1_wpn.get("stars", "")) == "凡", "星級應為 凡")
	assert(str(r1_wpn.get("bonus_name", "")) == "暴擊", "武器紅寶石應為 暴擊")
	assert(str(r1_wpn.get("bonus_text", "")) == "+2.0", "1級暴擊加成應為 +2.0")
	assert(str(r1_wpn.get("color_hex", "")) == "#C2185B", "紅寶石色碼應為 #C2185B")
	print("  ✓ 紅寶石 Lv.1 (武器): 暴擊 +2.0, 星級: 凡, 色碼: #C2185B (PASS)")

	# 黃寶石 3 級 武器
	var y3_wpn: Dictionary = _gem.get_gem_socket_info({"color": "yellow", "level": 3}, "weapon")
	assert(str(y3_wpn.get("color_name", "")) == "黃寶石", "名稱應為 黃寶石")
	assert(str(y3_wpn.get("stars", "")) == "優", "星級應為 優")
	assert(str(y3_wpn.get("bonus_name", "")) == "攻擊%", "武器黃寶石應為 攻擊%")
	assert(str(y3_wpn.get("bonus_text", "")) == "+12.0%", "3級攻擊加成應為 +12.0%")
	assert(str(y3_wpn.get("color_hex", "")) == "#9A6B00", "黃寶石色碼應為 #9A6B00")
	print("  ✓ 黃寶石 Lv.3 (武器): 攻擊% +12.0%, 星級: 優, 色碼: #9A6B00 (PASS)")

	# 藍寶石 5 級 防具
	var b5_arm: Dictionary = _gem.get_gem_socket_info({"color": "blue", "level": 5}, "armor")
	assert(str(b5_arm.get("color_name", "")) == "藍寶石", "名稱應為 藍寶石")
	assert(str(b5_arm.get("stars", "")) == "極", "星級應為 極")
	assert(str(b5_arm.get("bonus_name", "")) == "迴避", "防具藍寶石應為 迴避")
	assert(str(b5_arm.get("bonus_text", "")) == "+15.0", "5級迴避加成應為 +15.0")
	assert(str(b5_arm.get("color_hex", "")) == "#1565C0", "藍寶石色碼應為 #1565C0")
	print("  ✓ 藍寶石 Lv.5 (防具): 迴避 +15.0, 星級: 極, 色碼: #1565C0 (PASS)")

## 2. 測試背包詳情面板之寶石資訊呈現
func _test_bag_detail_display() -> void:
	print("\n--- 2. 測試背包Tab物品詳情面板顯示寶石資訊 ---")
	_gs.reset_new_game("rabbit")
	_gs.equip_bag = []

	# 建立未鑲寶石的武器
	var plain_w: Dictionary = _eq.roll_instance("rusty_blade", "common")
	var plain_uid: String = str(plain_w.get("uid", ""))
	_eq.add_to_bag(plain_w)

	# 建立鑲嵌紅寶石 Lv.1 的武器
	var gem_w: Dictionary = _eq.roll_instance("dawn_blade", "uncommon")
	gem_w["gem"] = {"color": "red", "level": 1}
	var gem_uid: String = str(gem_w.get("uid", ""))
	_eq.add_to_bag(gem_w)

	_lobby.call("_switch_tab", 4)

	# 1. 選中未鑲寶石武器
	_lobby.set("_selected_bag_item", plain_uid)
	_lobby.call("_refresh_bag_tab", false)
	var detail_lbl: RichTextLabel = _lobby.get("_bag_detail")
	var kind_lbl: Label = _lobby.get("_bag_detail_kind")
	assert(detail_lbl != null, "找不到 _bag_detail")
	assert(kind_lbl.text == "類型：武器", "未鑲寶石武器類型應為 '類型：武器', 實際: %s" % kind_lbl.text)
	assert(not detail_lbl.text.contains("已鑲寶石："), "未鑲寶石武器詳情不應包含 '已鑲寶石：'")
	print("  ✓ 未鑲寶石武器詳情正常顯示，不含寶石標籤 (PASS)")

	# 2. 選中鑲嵌寶石武器
	_lobby.set("_selected_bag_item", gem_uid)
	_lobby.call("_refresh_bag_tab", false)
	assert(kind_lbl.text == "類型：武器（已鑲寶石）", "鑲寶石武器類型應為 '類型：武器（已鑲寶石）', 實際: %s" % kind_lbl.text)
	assert(detail_lbl.text.contains("已鑲寶石："), "詳情內應包含 '已鑲寶石：'")
	assert(detail_lbl.text.contains("紅寶石"), "詳情內應包含 '紅寶石'")
	assert(detail_lbl.text.contains("1 星（凡）"), "詳情內應包含 '1 星（凡）'")
	assert(detail_lbl.text.contains("暴擊 +2.0"), "詳情內應包含 '暴擊 +2.0'")
	assert(detail_lbl.text.contains("#C2185B"), "詳情內應包含高對比色碼 '#C2185B'")
	print("  ✓ 鑲寶石武器詳情完整顯示寶石名稱、星級、屬性加成與高對比色碼標籤 (PASS)")

## 3. 測試裝備拆解時安全返還寶石至 GemSystem
func _test_dismantle_safe_refund() -> void:
	print("\n--- 3. 測試裝備拆解時安全返還寶石至 GemSystem (防吞寶石) ---")
	_gs.reset_new_game("rabbit")
	_gs.equip_bag = []
	_gs.gem_bag = []
	_gs.gold = 50

	# 建立帶藍寶石 Lv.2 的武器
	var wpn: Dictionary = _eq.roll_instance("rusty_blade", "uncommon")
	wpn["gem"] = {"color": "blue", "level": 2}
	var uid: String = str(wpn.get("uid", ""))
	_eq.add_to_bag(wpn)

	var prev_gems: int = _gem.count_of("blue", 2)
	var prev_gem_bag_size: int = _gs.gem_bag.size()
	var prev_scrap: int = _inv.count("iron_scrap")
	var prev_gold: int = _gs.gold

	var res: Dictionary = _eq.dismantle(uid)
	assert(bool(res.get("ok", false)), "拆解應成功: %s" % res)
	assert(res.has("refunded_gem"), "回傳結果必須包含 refunded_gem")
	var ref_g: Dictionary = res.get("refunded_gem", {})
	assert(str(ref_g.get("color", "")) == "blue", "返還寶石顏色應為 blue")
	assert(int(ref_g.get("level", 0)) == 2, "返還寶石等級應為 2")

	# 驗證訊息包含『返還寶石』
	var msg: String = str(res.get("msg", ""))
	assert(msg.contains("返還寶石"), "拆解訊息必須包含『返還寶石』, 實際: %s" % msg)
	assert(msg.contains("藍寶石 · 2 級"), "拆解訊息必須包含寶石標籤, 實際: %s" % msg)

	# 驗證 GemSystem 與 GameState 寶石背包
	var new_gems: int = _gem.count_of("blue", 2)
	var new_gem_bag_size: int = _gs.gem_bag.size()
	assert(new_gems == prev_gems + 1, "GemSystem 藍寶石 2 級數量應精確 +1 (原本: %d, 現在: %d)" % [prev_gems, new_gems])
	assert(new_gem_bag_size == prev_gem_bag_size + 1, "GameState.gem_bag 總量應精確 +1")

	# 驗證裝備已被移除、資源正常獲得
	assert(_eq.find_bag(uid).is_empty(), "裝備應已自背包中乾淨移除")
	assert(_inv.count("iron_scrap") > prev_scrap, "鐵屑應增加")
	assert(_gs.gold > prev_gold, "金幣應增加")
	print("  ✓ 帶寶石裝備拆解成功返還寶石至 GemSystem，數量 +1 且防止吞寶石 (PASS)")

## 4. 測試鎖定與穿戴中裝備防拆 (安全守門)
func _test_locked_and_equipped_protection() -> void:
	print("\n--- 4. 測試鎖定與裝備中防拆保護 ---")
	_gs.reset_new_game("rabbit")
	_gs.equip_bag = []
	_gs.gem_bag = []

	var wpn: Dictionary = _eq.roll_instance("rusty_blade", "common")
	wpn["gem"] = {"color": "red", "level": 1}
	var uid: String = str(wpn.get("uid", ""))
	_eq.add_to_bag(wpn)

	# 1. 鎖定防拆
	_eq.set_locked(uid, true)
	var res_lock: Dictionary = _eq.dismantle(uid)
	assert(not bool(res_lock.get("ok", true)), "鎖定裝備禁止拆解")
	assert(_gs.gem_bag.size() == 0, "鎖定裝備拆解失敗不應返還寶石")
	assert(not _eq.find_bag(uid).is_empty(), "鎖定裝備不應被銷毀")
	_eq.set_locked(uid, false)
	print("  ✓ 鎖定裝備防拆保護通過 (PASS)")

	# 2. 裝備中防拆
	_eq.equip(uid)
	var res_equip: Dictionary = _eq.dismantle(uid)
	assert(not bool(res_equip.get("ok", true)), "穿戴中裝備禁止拆解")
	assert(_gs.gem_bag.size() == 0, "穿戴中裝備拆解失敗不應返還寶石")
	_eq.unequip(uid)
	print("  ✓ 穿戴中裝備防拆保護通過 (PASS)")

## 5. 測試六語系字典
func _test_six_locales() -> void:
	print("\n--- 5. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 字典支援 ---")
	for loc in LOCALES:
		_loc.call("set_locale", loc)
		ContentLoc.reload()

		var t_gem_prefix: String = ContentLoc.text("ui", "已鑲寶石：")
		var t_dismantle_toast: String = ContentLoc.text("ui", "拆解【%s】：獲得鐵屑 ×%d、金幣 +%d、返還寶石【%s】")
		var t_kind_socketed: String = ContentLoc.text("ui", "類型：%s（已鑲寶石）")
		var t_refund_gem: String = ContentLoc.text("ui", "返還寶石")

		assert(not t_gem_prefix.is_empty(), "[%s] '已鑲寶石：' 不應為空" % loc)
		assert(not t_dismantle_toast.is_empty(), "[%s] 拆解返還 Toast 文本不應為空" % loc)
		assert(not t_kind_socketed.is_empty(), "[%s] 類型已鑲嵌文本不應為空" % loc)
		assert(not t_refund_gem.is_empty(), "[%s] '返還寶石' 不應為空" % loc)

		assert(not _has_emoji(t_gem_prefix), "[%s] 嚴禁包含 Emoji" % loc)
		assert(not _has_emoji(t_dismantle_toast), "[%s] 嚴禁包含 Emoji" % loc)

		if loc in ["en", "es"]:
			assert(not _has_cjk(t_gem_prefix), "[%s] 歐美語系嚴禁殘留 CJK" % loc)
			assert(not _has_cjk(t_dismantle_toast), "[%s] 歐美語系嚴禁殘留 CJK" % loc)
			assert(not _has_cjk(t_refund_gem), "[%s] 歐美語系嚴禁殘留 CJK" % loc)

		print("  ✓ [%s] 六語系詞條完整通過驗證 (PASS)" % loc)

	_loc.call("set_locale", "zh_TW")
	ContentLoc.reload()

## 設定截圖測試項目
func _setup_proof_items() -> void:
	_gs.reset_new_game("rabbit")
	_gs.equip_bag = []
	_gs.gem_bag = []
	_gs.gold = 500

	# 1. 帶紅寶石之晨曦之刃
	var w1: Dictionary = _eq.roll_instance("dawn_blade", "rare")
	w1["gem"] = {"color": "red", "level": 1}
	_proof_gem_weapon_uid = str(w1.get("uid", ""))
	_eq.add_to_bag(w1)

	# 2. 無寶石之生鏽鐵劍
	var w2: Dictionary = _eq.roll_instance("rusty_blade", "common")
	_proof_plain_weapon_uid = str(w2.get("uid", ""))
	_eq.add_to_bag(w2)

	# 3. 帶黃寶石之晨曦之刃 (Lv.3)
	var w3: Dictionary = _eq.roll_instance("dawn_blade", "epic")
	w3["gem"] = {"color": "yellow", "level": 3}
	_proof_yellow_gem_uid = str(w3.get("uid", ""))
	_eq.add_to_bag(w3)

func _capture_and_save(path: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var img := root.get_texture().get_image()
	if img != null:
		img.save_png(path)
		var f := FileAccess.open(path, FileAccess.READ)
		if f != null:
			var data := f.get_buffer(f.get_length())
			var ctx := HashingContext.new()
			ctx.start(HashingContext.HASH_SHA256)
			ctx.update(data)
			var h := ctx.finish().hex_encode()
			assert(not _proof_hashes.has(h), "截圖不可重複 (SHA256 重複): %s" % path)
			_proof_hashes.append(h)
			print("  [PROOF] 已儲存截圖: ", path, " (SHA256: ", h.substr(0, 16), "...)")
