extends SceneTree
## 探索性 QA 第四十八輪 實機巡檢存證腳本 (tools/capture_qa_round48.gd)
## 任務: t_912c8ab4 (每日發條接到停擺巨偶合主線後找破圖)
## 依據規範: review.md 0-QA5, 0-QA23, 0-QA24, 0-QA25, 0-QA26
##
## 驗收重點:
## 1. 0-QA5 / 0-QA26: 嚴格使用 Godot Viewport Framebuffer 原生截圖，零 PIL、零繪製假圖。
## 2. 0-QA23: OUT_DIR 嚴格限定為 proofs/t_912c8ab4/，絕不覆蓋或污染其他任務目錄。
## 3. 實機場景測試:
##    - proof_01_windup_with_colossus_zh.png: 每日發條完成後有次數(3/3)出現「前往停擺巨偶」按鈕(暖橘果凍厚底，>=48px，零Emoji)
##    - proof_02_windup_no_colossus_zh.png: 每日發條完成後巨偶次數(0/3)已用完，不出現該按鈕，維持「前往出征」
##    - proof_03_windup_with_colossus_en.png: 英文 (en) 查截字/折行/按鈕熱區與文字對比
##    - proof_04_windup_with_colossus_ja.png: 日文 (ja) 查截字/折行/按鈕熱區與文字對比
##    - proof_05_old_feature_lobby.png: 舊功能驗證 - 大廳主介面、角色待機、頂欄能量與Dock
##    - proof_06_old_feature_sortie_colossus.png: 舊功能驗證 - 出征分頁停擺巨偶模式切換與關卡卡片
##    - proof_07_old_feature_wardrobe.png: 舊功能驗證 - 衣櫥換裝彈窗、套裝卡片與紙娃娃預覽

var OUT_DIR := ""
var _step := 0
var _wait := 0
var _lobby: Control = null
var _dlg: Control = null
var _gs: Node = null
var _ws: Node = null
var _cds: Node = null
var _loc_node: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	OUT_DIR = ProjectSettings.globalize_path("res://../proofs/t_912c8ab4")
	DirAccess.make_dir_recursive_absolute(OUT_DIR)

	print("=== 開始執行 QA 第四十八輪實機巡檢存證腳本 (t_912c8ab4) ===")
	print("OUT_DIR: ", OUT_DIR)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_ws = root.get_node_or_null("WindupDailySystem")
	if _ws == null:
		var WsClass = load("res://scripts/systems/windup_daily.gd")
		if WsClass:
			_ws = WsClass.new()
			_ws.name = "WindupDailySystem"
			root.add_child(_ws)

	_cds = root.get_node_or_null("ColossusDailySystem")
	if _cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			_cds = CdsClass.new()
			_cds.name = "ColossusDailySystem"
			root.add_child(_cds)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)

	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 繁中 (zh_TW) 委託完成且有巨偶剩餘次數 (3/3)
			if _wait == 10:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 3)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 30:
				var p1 := "%s/proof_01_windup_with_colossus_zh.png" % OUT_DIR
				_save_screenshot(p1)
				print("  ✓ [1/7] 繁中 (zh_TW) 委託完成有巨偶次數: %s" % p1)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 繁中 (zh_TW) 委託完成但無巨偶次數 (0/3)
			if _wait == 10:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 0)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 30:
				var p2 := "%s/proof_02_windup_no_colossus_zh.png" % OUT_DIR
				_save_screenshot(p2)
				print("  ✓ [2/7] 繁中 (zh_TW) 委託完成無巨偶次數: %s" % p2)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 英文 (en) 委託完成且有巨偶次數 (3/3)
			if _wait == 10:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 3)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 30:
				var p3 := "%s/proof_03_windup_with_colossus_en.png" % OUT_DIR
				_save_screenshot(p3)
				print("  ✓ [3/7] 英文 (en) 委託完成有巨偶次數: %s" % p3)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 日文 (ja) 委託完成且有巨偶次數 (3/3)
			if _wait == 10:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 3)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 30:
				var p4 := "%s/proof_04_windup_with_colossus_ja.png" % OUT_DIR
				_save_screenshot(p4)
				print("  ✓ [4/7] 日文 (ja) 委託完成有巨偶次數: %s" % p4)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 舊功能回歸 - 大廳主介面 (zh_TW)
			if _wait == 10:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _lobby:
					_lobby.call("_switch_tab", 0) # Tab.MAIN
					_lobby.call("refresh_hud")
			elif _wait == 30:
				var p5 := "%s/proof_05_old_feature_lobby.png" % OUT_DIR
				_save_screenshot(p5)
				print("  ✓ [5/7] 舊功能驗證 - 大廳主介面: %s" % p5)
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 舊功能回歸 - 前往停擺巨偶 / 出征分頁
			if _wait == 10:
				if _lobby:
					_lobby.call("go_to_colossus")
			elif _wait == 30:
				var p6 := "%s/proof_06_old_feature_sortie_colossus.png" % OUT_DIR
				_save_screenshot(p6)
				print("  ✓ [6/7] 舊功能驗證 - 出征停擺巨偶: %s" % p6)
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 舊功能回歸 - 衣櫥換裝介面
			if _wait == 10:
				if _lobby:
					_lobby.call("_switch_tab", 0) # 先回主頁
					_lobby.call("open_wardrobe")
			elif _wait == 35:
				var p7 := "%s/proof_07_old_feature_wardrobe.png" % OUT_DIR
				_save_screenshot(p7)
				print("  ✓ [7/7] 舊功能驗證 - 衣櫥換裝彈窗: %s" % p7)
				if _lobby:
					var w_dlg = _lobby.find_child("WardrobeDialog", true, false)
					if w_dlg:
						w_dlg.queue_free()
					_lobby.queue_free()
					_lobby = null
				print("── 全數實機截圖完成 (t_912c8ab4) ──")
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Viewport is null: " + abs_path)
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Texture is null: " + abs_path)
		return
	var img: Image = tex.get_image()
	if img != null and not img.is_empty():
		var err := img.save_png(abs_path)
		if err != OK:
			push_error("儲存截圖失敗 err=%d: %s" % [err, abs_path])
	else:
		push_error("無法取得 Viewport 圖像: %s" % abs_path)
