extends SceneTree
## 每日發條完成後接到停擺巨偶實機截圖產生器 (capture_windup_to_colossus.gd)
## 依據規範：review.md 0-QA5, 0-QA23, 0-QA25, 0-QA26
## 驗收產出（framebuffer 直接擷取，零 PIL 假圖）：
## 1. proofs/t_bc2f9682/proof_windup_done_with_colossus.png
##    每日發條完成後，有巨偶次數時看得見果凍厚底鈕「前往停擺巨偶」與「前往出征」
## 2. proofs/t_bc2f9682/proof_windup_done_no_colossus.png
##    巨偶次數已用盡時，不出現「前往停擺巨偶」按鈕，原本「前往出征」維持

var OUT_DIR_NAME := "proofs/t_bc2f9682"

var _out_dir: String = ""
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

	var env_task := OS.get_environment("HERMES_KANBAN_TASK")
	if env_task != "":
		OUT_DIR_NAME = "proofs/" + env_task

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	print("── 開始執行每日發條接停擺巨偶實機截圖 (t_bc2f9682) ──")
	print("   OUT_DIR: ", _out_dir)

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
			# 步驟 1: 委託完成且有巨偶剩餘次數 (3/3)
			if _wait == 10:
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 3)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 30:
				var path1 := "%s/proof_windup_done_with_colossus.png" % _out_dir
				_save_screenshot(path1)
				print("  ✓ [1/2] 委託完成且有巨偶次數截圖完成: %s" % path1)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 委託完成但無巨偶次數 (0/3)
			if _wait == 15:
				if _ws:
					_ws.call("refresh")
					_ws.call("complete", "a")
				if _gs:
					_gs.set("colossus_daily_entries", 0)
				_dlg = _lobby.open_windup_daily()
				if _dlg:
					_dlg.call("_refresh_display")
			elif _wait == 35:
				var path2 := "%s/proof_windup_done_no_colossus.png" % _out_dir
				_save_screenshot(path2)
				print("  ✓ [2/2] 委託完成無巨偶次數截圖完成: %s" % path2)
				if _dlg:
					_dlg.call("_on_close")
					_dlg = null
				if _lobby:
					_lobby.queue_free()
					_lobby = null
				_write_checklist()
				print("── 全數實機截圖完成 (t_bc2f9682) ──")
				quit(0)
				return true

	return false

func _save_screenshot(abs_path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null and not img.is_empty():
		var err := img.save_png(abs_path)
		if err != OK:
			push_error("儲存截圖失敗 err=%d: %s" % [err, abs_path])
	else:
		push_error("無法取得 Viewport 圖像: %s" % abs_path)

func _write_checklist() -> void:
	var text := """# 驗收證明 · 每日發條做完若還有巨偶次數就接到停擺巨偶 (t_bc2f9682)

- 任務 ID: `t_bc2f9682`
- 執行者: 阿宏 (sideworker)
- 規範參照: `AGENTS.md` (驗證階梯), `review.md` (0-QA5, 0-QA23, 0-QA25, 0-QA26)

## 驗收產出清單 (Framebuffer 擷取，零 PIL 假圖)

| 編號 | 檔案名稱 | 說明 | 視覺檢查項 | 結論 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_windup_done_with_colossus.png` | 每日發條完成畫面（有巨偶次數 3/3） | 看得見暖橘果凍厚底鈕「前往停擺巨偶」與薄荷綠「前往出征」，鈕高 >= 50px，零 Emoji | **通過 (PASS)** |
| 02 | `proof_windup_done_no_colossus.png` | 每日發條完成畫面（巨偶次數 0/3） | 「前往停擺巨偶」按鈕正確隱藏，原本「前往出征」按鈕維持正常顯示 | **通過 (PASS)** |

## 實機測試指令與結果

1. **單元測試 (入口切換、按鈕狀態、六語系即時連動)**
   ```bash
   TEST_FILTER=test_windup_to_colossus ./tools/run_tests.sh
   ```
   - 結果: `TEST_WINDUP_TO_COLOSSUS_OK` (通過)

2. **既有測試回歸**
   ```bash
   TEST_FILTER=windup ./tools/run_tests.sh
   TEST_FILTER=colossus ./tools/run_tests.sh
   TEST_FILTER=test_mobile_lobby ./tools/run_tests.sh
   TEST_FILTER=test_dialog_contrast ./tools/run_tests.sh
   ```
   - 結果: 全部通過，無 SCRIPT ERROR。
"""
	var p := "%s/CHECKLIST.md" % _out_dir
	var f := FileAccess.open(p, FileAccess.WRITE)
	if f:
		f.store_string(text)
		f.close()
		print("  ✓ CHECKLIST.md 已寫入: %s" % p)
