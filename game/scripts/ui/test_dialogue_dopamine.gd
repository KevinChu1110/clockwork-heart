extends SceneTree
## 對話框與過場字幕多巴胺亮色盤單元測試：
## godot --headless -s res://scripts/ui/test_dialogue_dopamine.gd

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const DialogueBoxScene = preload("res://scenes/ui/dialogue_box.tscn")
const CutscenePlayerScript = preload("res://scripts/ui/cutscene_player.gd")

var _ok := true
var _step := 0
var _wait := 0
var _dbox: DialogueBox = null
var _cutscene: CutscenePlayer = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			print("=== 開始對話框與過場字幕多巴胺亮色盤測試 ===")

			# 1. 驗證 UiStyle.dialogue_style()
			var ds: StyleBoxFlat = UiStyle.dialogue_style()
			if ds == null:
				_fail("UiStyle.dialogue_style() 回傳 null")
			else:
				var expected_bg := Color("#FFFDF8")
				if not ds.bg_color.is_equal_approx(expected_bg):
					_fail("dialogue_style 底板背景色非奶油白 #FFFDF8: %s" % ds.bg_color.to_html())
				else:
					print("  [OK] dialogue_style 底板背景色為奶油白 #FFFDF8")

				var expected_border := Color("#1F1A3A")
				if not ds.border_color.is_equal_approx(expected_border):
					_fail("dialogue_style 描邊非深藍紫 #1F1A3A: %s" % ds.border_color.to_html())
				else:
					print("  [OK] dialogue_style 描邊為深藍紫 #1F1A3A")

				var r := ds.corner_radius_top_left
				if r < 18 or r > 24:
					_fail("dialogue_style 圓角不在 18~24px: %d" % r)
				else:
					print("  [OK] dialogue_style 圓角為 %d px (符合 18~24px 規範)" % r)

				if ds.border_width_bottom < 4:
					_fail("dialogue_style 缺少果凍厚底 (bottom border < 4px): %d" % ds.border_width_bottom)
				else:
					print("  [OK] dialogue_style 底邊厚度為 %d px (果凍厚底)" % ds.border_width_bottom)

			# 建立 DialogueBox
			_dbox = DialogueBoxScene.instantiate()
			root.add_child(_dbox)
			_step = 1
			_wait = 0
			return false

		1:
			# 等待 DialogueBox _ready 完成
			if _wait < 5:
				return false

			var test_lines := [
				{
					"speaker": "小白",
					"text": "報告指揮官！前方偵測到齒輪廢墟的能量波動，我們必須立刻前往調查！",
				}
			]
			_dbox.play(test_lines)
			_dbox._finish_typing()

			var speaker_lbl: Label = _dbox.get_node("%Speaker") as Label
			var body_lbl: RichTextLabel = _dbox.get_node("%Body") as RichTextLabel
			var hint_lbl: Label = _dbox.get_node("%ContinueHint") as Label
			var pframe: PanelContainer = _dbox.get_node("%PortraitFrame") as PanelContainer

			# 驗證人名
			var spk_col := speaker_lbl.get_theme_color("font_color")
			if not spk_col.is_equal_approx(Color("#1F1A3A")):
				_fail("DialogueBox 人名字色非深藍紫 #1F1A3A: %s" % spk_col.to_html())
			else:
				print("  [OK] DialogueBox 人名字色為深藍紫 #1F1A3A")

			var spk_sz := speaker_lbl.get_theme_font_size("font_size")
			if spk_sz < 16 or spk_sz > 24:
				_fail("DialogueBox 人名字級不在 16~24px: %d" % spk_sz)
			else:
				print("  [OK] DialogueBox 人名字級為 %d px" % spk_sz)

			# 驗證內文
			var body_col := body_lbl.get_theme_color("default_color")
			if not body_col.is_equal_approx(Color("#1F1A3A")):
				_fail("DialogueBox 內文字色非深藍紫 #1F1A3A: %s" % body_col.to_html())
			else:
				print("  [OK] DialogueBox 內文字色為深藍紫 #1F1A3A (無白底白字)")

			var body_sz := body_lbl.get_theme_font_size("normal_font_size")
			if body_sz < 16 or body_sz > 24:
				_fail("DialogueBox 內文字級不在 16~24px: %d" % body_sz)
			else:
				print("  [OK] DialogueBox 內文字級為 %d px" % body_sz)

			# 驗證提示
			var hint_sz := hint_lbl.get_theme_font_size("font_size")
			if hint_sz < 16 or hint_sz > 24:
				_fail("DialogueBox 提示字級不在 16~24px: %d" % hint_sz)
			else:
				print("  [OK] DialogueBox 提示字級為 %d px (無小字)" % hint_sz)

			var hint_col := hint_lbl.get_theme_color("font_color")
			if hint_col.is_equal_approx(Color.WHITE) or hint_col.v > 0.85:
				_fail("DialogueBox 提示字色為淺色/白色，在亮底不可讀: %s" % hint_col.to_html())
			else:
				print("  [OK] DialogueBox 提示字色為深藍紫系 %s (可讀)" % hint_col.to_html())

			# 驗證頭像框亮底
			var pfs := pframe.get_theme_stylebox("panel") as StyleBoxFlat
			if pfs != null:
				if pfs.bg_color.v < 0.8:
					_fail("DialogueBox 頭像框為暗色底: %s" % pfs.bg_color.to_html())
				else:
					print("  [OK] DialogueBox 頭像框為亮色卡片底 #%s" % pfs.bg_color.to_html())

			# 移除 DialogueBox，準備測試 CutscenePlayer
			_dbox.queue_free()
			_cutscene = CutscenePlayerScript.new()
			root.add_child(_cutscene)
			_step = 2
			_wait = 0
			return false

		2:
			# 等待 CutscenePlayer _ready 完成
			if _wait < 5:
				return false

			var cs_slides := [
				{
					"speaker": "麥穗",
					"text": "在這個被齒輪與發條運轉的世界裡，每一顆心臟都有它甦醒的時刻。",
				}
			]
			_cutscene.play(cs_slides)

			var cs_panel: PanelContainer = _cutscene.get("_caption_panel")
			var cs_spk: Label = _cutscene.get("_speaker")
			var cs_body: RichTextLabel = _cutscene.get("_body")
			var cs_hint: Label = _cutscene.get("_hint")

			var cs_sb := cs_panel.get_theme_stylebox("panel") as StyleBoxFlat
			if cs_sb == null or not cs_sb.bg_color.is_equal_approx(Color("#FFFDF8")):
				_fail("CutscenePlayer 字幕條未套用多巴胺亮色 dialogue_style")
			else:
				print("  [OK] CutscenePlayer 字幕條套用多巴胺奶油白底板 #FFFDF8")

			var cs_spk_col := cs_spk.get_theme_color("font_color")
			if not cs_spk_col.is_equal_approx(Color("#1F1A3A")):
				_fail("CutscenePlayer 說話人字色非深藍紫 #1F1A3A: %s" % cs_spk_col.to_html())
			else:
				print("  [OK] CutscenePlayer 說話人字色為深藍紫 #1F1A3A")

			var cs_body_col := cs_body.get_theme_color("default_color")
			if not cs_body_col.is_equal_approx(Color("#1F1A3A")):
				_fail("CutscenePlayer 內文字色非深藍紫 #1F1A3A: %s" % cs_body_col.to_html())
			else:
				print("  [OK] CutscenePlayer 內文字色為深藍紫 #1F1A3A (無白底白字)")

			var cs_hint_sz := cs_hint.get_theme_font_size("font_size")
			if cs_hint_sz < 16 or cs_hint_sz > 24:
				_fail("CutscenePlayer 提示字級不在 16~24px: %d" % cs_hint_sz)
			else:
				print("  [OK] CutscenePlayer 提示字級為 %d px" % cs_hint_sz)

			var cs_hint_col := cs_hint.get_theme_color("font_color")
			if cs_hint_col.is_equal_approx(Color.WHITE) or cs_hint_col.v > 0.85:
				_fail("CutscenePlayer 提示字色為淺色/白色: %s" % cs_hint_col.to_html())
			else:
				print("  [OK] CutscenePlayer 提示字色為深藍紫系 %s (可讀)" % cs_hint_col.to_html())

			if _ok:
				print("DIALOGUE_DOPAMINE_TEST_OK")
				quit(0)
			else:
				print("DIALOGUE_DOPAMINE_TEST_FAIL")
				quit(1)
			return true

	return false
