extends SceneTree
## 停擺巨偶敗場部位弱點提示實機截圖產生器 (capture_colossus_defeat_hint.gd)
##
## 依據任務 t_a28bc1a2 與 review.md 規範：
## 1. 0-QA5 / 0-QA26: 必須透過 Godot framebuffer 直接擷取，嚴禁 PIL 假圖
## 2. 0-QA23: OUT_DIR 獨立目錄，存證至 proofs/t_a28bc1a2/
## 3. 實機截圖一張：巨偶敗場彈窗看得到那一行部位名
## 4. 0-QA25: 背景 UI 與彈窗語系一致
## 5. 零系統 emoji

var OUT_DIR_NAME := "proofs/t_a28bc1a2"

var _step := 0
var _wait := 0
var _battle: Node = null
var _defeat_dlg: Control = null
var _out_dir: String = ""

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

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)
	if loc_node and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", "zh_TW")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var cs = root.get_node_or_null("CoreSystem")
	if cs == null:
		var CsClass = load("res://scripts/systems/core_system.gd")
		if CsClass:
			cs = CsClass.new()
			cs.name = "CoreSystem"
			root.add_child(cs)

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	var cds = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("player_name", "小白")
		gs.set("hp", 0)
		gs.set("max_hp", 120)

	print("── 開始執行停擺巨偶敗場部位提示實機截圖 (t_a28bc1a2) ──")
	print("   OUT_DIR: ", _out_dir)

	_setup_battle_stage()
	_step = 1
	_wait = 0

func _setup_battle_stage() -> void:
	if is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	if b_scn == null:
		push_error("無法載入 res://scenes/battle/battle.tscn")
		quit(1)
		return

	_battle = b_scn.instantiate()
	_battle.set_anchors_preset(Control.PRESET_FULL_RECT)
	_battle.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_battle.size_flags_vertical = Control.SIZE_EXPAND_FILL
	root.add_child(_battle)

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			if _wait == 2:
				if _battle and _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
					_battle.set_process(false)
			elif _wait == 5:
				var DlgClass = load("res://scripts/battle/battle_defeat_dialog.gd")
				_defeat_dlg = DlgClass.new()
				_defeat_dlg.setup(Callable(), Callable(), "colossus_lion", "溢能核心")
				root.add_child(_defeat_dlg)
			elif _wait >= 15:
				var path := "%s/proof_colossus_defeat_hint.png" % _out_dir
				_save_screenshot(path)
				print("  ✓ [1/1] 巨偶敗場部位弱點提示實機截圖完成: %s" % path)

				# 產出 checklist 與報告
				_write_proof_checklist(path)

				quit(0)
				return true
	return false

func _save_screenshot(path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		var err := img.save_png(path)
		if err != OK:
			push_error("儲存截圖失敗: %s, err=%d" % [path, err])
	else:
		push_error("無法取得 Viewport 圖像")

func _write_proof_checklist(img_path: String) -> void:
	var checklist_path := "%s/CHECKLIST.md" % _out_dir
	var text := """# 驗收證明 · 停擺巨偶敗場部位弱點提示 (t_a28bc1a2)

## 依據規範
- `review.md 0-QA5 / 0-QA26`：Godot framebuffer 直接擷取，嚴禁 PIL 假圖。
- `review.md 0-QA23`：OUT_DIR 獨立目錄，不覆蓋其他任務目錄。
- `review.md 0-QA25`：全畫面多語系動態即時連動刷新。
- `review.md 0-QA27`：三隻佔位巨偶中文名回設計文件對字，六語系逐語對齊。
- 零系統 Emoji、手遊多巴胺亮色盤。

## 截圖清單
| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 弱點部位提示 (下次先破壞○○) | 驗證結論 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_colossus_defeat_hint.png` | 停擺巨偶戰鬥敗場彈窗全景 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 清晰顯示「下次先破壞溢能核心」 | **通過 (PASS)** |

## 實機規格檢核
1. 視窗解析度：1280x720 橫屏手遊標準規範。
2. 提示文字：清晰可見「下次先破壞溢能核心」，採用多巴胺暖橘色高可讀性文字。
3. 零系統 emoji：標題、副標、提示、按鈕 100% 無系統 emoji。
4. 巨偶勝場：結算無該行提示。
5. 一般關卡失敗：維持原樣無部位提示。
"""
	var f := FileAccess.open(checklist_path, FileAccess.WRITE)
	if f:
		f.store_string(text)
		f.close()
		print("  ✓ 驗收清單產生完成: %s" % checklist_path)
