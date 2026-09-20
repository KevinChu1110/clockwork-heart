class_name TitleWallDialog
extends Control
## 《發條之心》標題成就稱號牆卡片網格視窗 (TitleWallDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，底部操作按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底板奶油米白 #FFFDF8。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 稱號卡片 2 欄網格：每卡顯示稱號名 + 一句條件。
##    已解鎖 = 暖橘果凍厚底 5~6px + 「已解鎖」標籤；未解鎖 = 壓暗奶油底、條件清晰可讀 + 「未解鎖」標籤。
## 6. 字級標題 20~24、卡片 16+，零 13px 以下小字。
## 7. 新解鎖稱號若有，頂部一條金黃卡片提示，零雜亂 BBCode。
## 8. 零系統 Emoji、零字元圖示、零新產圖。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_UNLOCKED := Color("#FFF8E7")  ## 溫暖米黃卡片底（已解鎖）
const COLOR_CARD_LOCKED := Color("#EDE6DC")  ## 壓暗奶油底（未解鎖）
const COLOR_CARD_LOCKED_BORDER := Color("#C4B8A8") ## 壓暗邊框（未解鎖）
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MUTED  := Color("#6B635B")  ## 壓暗深褐文字（清楚可讀）
const COLOR_DESC_UNLOCKED := Color("#4A3E38") ## 已解鎖條件說明字
const COLOR_DESC_LOCKED   := Color("#59514A") ## 未解鎖條件說明字

var _newly: Array[String] = []
var _back_cb: Callable = Callable()
var _fortress_cb: Callable = Callable()
var _back_text: String = "返回標題"

var _dialog_card: PanelContainer
var _card_grid: GridContainer
var _cards: Array[PanelContainer] = []
var _cached_font: Font = null
var _built: bool = false


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


func setup(newly: Array[String], back_cb: Callable, fortress_cb: Callable = Callable(), back_text: String = "返回標題") -> void:
	_newly = newly
	_back_cb = back_cb
	_fortress_cb = fortress_cb
	if back_text != "":
		_back_text = back_text
	if is_inside_tree():
		_rebuild()


func _ready() -> void:
	name = "TitleWallDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	if not _built:
		_build_ui()


func _rebuild() -> void:
	for c in get_children():
		c.queue_free()
	_cards.clear()
	_built = false
	_build_ui()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 5, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 10
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
		sb.shadow_size = 5
		sb.shadow_offset = Vector2(0, 3)
	return sb


func _apply_label_style(lbl: Label, size: int, color: Color = COLOR_TEXT_DARK, outline_col: Color = Color(0, 0, 0, 0), outline_sz: int = 0) -> void:
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	if outline_sz > 0:
		lbl.add_theme_color_override("font_outline_color", outline_col)
		lbl.add_theme_constant_override("outline_size", outline_sz)
	if _cached_font:
		lbl.add_theme_font_override("font", _cached_font)


func _build_ui() -> void:
	_built = true

	# 0. 底層風景圖（避免黑底，若有標題／村莊底圖則帶入）
	var bg_tex: Texture2D = null
	for path in [
		"res://assets/sprites/illustrations/title_bg_clockwork.png",
		"res://assets/sprites/illustrations/title_bg.png",
		"res://assets/sprites/maps/village_bg.png"
	]:
		if ResourceLoader.exists(path):
			bg_tex = load(path) as Texture2D
			break
	if bg_tex:
		var bg_art := TextureRect.new()
		bg_art.name = "BackgroundArt"
		bg_art.set_anchors_preset(Control.PRESET_FULL_RECT)
		bg_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		bg_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		bg_art.texture = bg_tex
		bg_art.modulate = Color(0.70, 0.68, 0.75, 0.70)
		bg_art.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(bg_art)

	# 1. 全螢幕半透明遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	var scrim_btn := Button.new()
	scrim_btn.name = "ScrimClick"
	scrim_btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_btn.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_btn.add_theme_stylebox_override("normal", esb)
	scrim_btn.add_theme_stylebox_override("hover", esb)
	scrim_btn.add_theme_stylebox_override("pressed", esb)
	scrim_btn.pressed.connect(_on_close)
	scrim.add_child(scrim_btn)

	# 2. 置中卡片 (寬 750px，符合 740~760px 規範)
	var center := CenterContainer.new()
	center.name = "CenterContainer"
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "TitleWallCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 520)
	_dialog_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v_main := VBoxContainer.new()
	v_main.add_theme_constant_override("separation", 10)
	margin.add_child(v_main)

	# 3. 頂部標題與關閉列
	var head := HBoxContainer.new()
	head.alignment = BoxContainer.ALIGNMENT_CENTER
	head.add_theme_constant_override("separation", 10)
	v_main.add_child(head)

	var title_lbl := Label.new()
	title_lbl.name = "TitleLabel"
	title_lbl.text = _t("成就 · 稱號牆")
	_apply_label_style(title_lbl, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 3)
	head.add_child(title_lbl)

	# 稱號統計進度
	var tc: Node = Engine.get_main_loop().root.get_node_or_null("TitleCatalog") if Engine.get_main_loop() else null
	var unlocked_num: int = tc.unlocked_count() if tc and tc.has_method("unlocked_count") else 0
	var total_num: int = tc.total_count() if tc and tc.has_method("total_count") else 24

	var count_lbl := Label.new()
	count_lbl.name = "CountLabel"
	count_lbl.text = _t("（已解鎖 %d／%d）") % [unlocked_num, total_num]
	_apply_label_style(count_lbl, 18, COLOR_TEXT_GOLD, COLOR_BORDER, 2)
	count_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(count_lbl)

	# 右上「✕」關閉按鈕 (50x50，珊瑚粉果凍厚底按鈕)
	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 暖橘色粗分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v_main.add_child(sep)

	# 4. 新解鎖提示條（若有新解鎖）
	if not _newly.is_empty():
		var banner_panel := PanelContainer.new()
		banner_panel.name = "NewlyUnlockedBanner"
		var b_sb := StyleBoxFlat.new()
		b_sb.bg_color = Color("#FFF4D0")  ## 柔和金黃底
		b_sb.border_color = COLOR_ORANGE
		b_sb.set_border_width_all(2)
		b_sb.border_width_bottom = 4
		b_sb.set_corner_radius_all(14)
		b_sb.content_margin_left = 16
		b_sb.content_margin_right = 16
		b_sb.content_margin_top = 8
		b_sb.content_margin_bottom = 8
		banner_panel.add_theme_stylebox_override("panel", b_sb)
		v_main.add_child(banner_panel)

		var banner_lbl := Label.new()
		banner_lbl.name = "NewlyUnlockedLabel"
		banner_lbl.text = _t("新解鎖稱號：%s") % "、".join(_newly)
		_apply_label_style(banner_lbl, 16, COLOR_TEXT_GOLD, COLOR_BORDER, 2)
		banner_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		banner_panel.add_child(banner_lbl)

	# 5. 稱號卡片網格 (2 欄滾動區)
	var scroll := ScrollContainer.new()
	scroll.name = "TitleWallScroll"
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	scroll.custom_minimum_size = Vector2(0, 310)
	v_main.add_child(scroll)

	_card_grid = GridContainer.new()
	_card_grid.name = "TitleCardGrid"
	_card_grid.columns = 2
	_card_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_card_grid.add_theme_constant_override("h_separation", 12)
	_card_grid.add_theme_constant_override("v_separation", 10)
	scroll.add_child(_card_grid)

	_populate_title_cards(tc)

	# 6. 底部操作按鈕列
	var foot := HBoxContainer.new()
	foot.name = "ButtonRow"
	foot.alignment = BoxContainer.ALIGNMENT_CENTER
	foot.add_theme_constant_override("separation", 16)
	v_main.add_child(foot)

	# 返回標題 / 回到廣場 果凍按鈕 (高度 >= 50px)
	var back_btn := Button.new()
	back_btn.name = "BackBtn"
	back_btn.text = _t(_back_text)
	back_btn.custom_minimum_size = Vector2(220, 52)
	back_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 20))
	back_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB236"), COLOR_BORDER, 5, 20))
	back_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#E08805"), COLOR_BORDER, 2, 20))
	back_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	back_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	back_btn.add_theme_constant_override("outline_size", 3)
	back_btn.add_theme_font_size_override("font_size", 20)
	if _cached_font:
		back_btn.add_theme_font_override("font", _cached_font)
	back_btn.pressed.connect(_on_close)
	foot.add_child(back_btn)

	# 通關後若有堡壘入口，做成次要果凍按鈕
	if _fortress_cb.is_valid():
		var fortress_btn := Button.new()
		fortress_btn.name = "FortressBtn"
		fortress_btn.text = _t("堡壘")
		fortress_btn.custom_minimum_size = Vector2(180, 52)
		fortress_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 20))
		fortress_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#66E27F"), COLOR_BORDER, 5, 20))
		fortress_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3CB855"), COLOR_BORDER, 2, 20))
		fortress_btn.add_theme_color_override("font_color", COLOR_BORDER)
		fortress_btn.add_theme_color_override("font_outline_color", Color("#FFFFFF"))
		fortress_btn.add_theme_constant_override("outline_size", 2)
		fortress_btn.add_theme_font_size_override("font_size", 20)
		if _cached_font:
			fortress_btn.add_theme_font_override("font", _cached_font)
		fortress_btn.pressed.connect(_on_fortress)
		foot.add_child(fortress_btn)


func _populate_title_cards(tc: Node) -> void:
	var entries: Array = tc.entries() if tc and tc.has_method("entries") else []
	for i in entries.size():
		var entry: Dictionary = entries[i]
		var unlocked: bool = tc.is_unlocked(entry) if tc and tc.has_method("is_unlocked") else false
		var card := _create_title_card(entry, unlocked, i)
		_card_grid.add_child(card)
		_cards.append(card)


func _create_title_card(entry: Dictionary, unlocked: bool, index: int) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "TitleCard_%d" % index
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(330, 84)
	card.mouse_filter = Control.MOUSE_FILTER_STOP
	card.set_meta("is_unlocked", unlocked)
	card.set_meta("flag", str(entry.get("flag", "")))

	# 卡片底板：已解鎖＝暖橘果凍厚底 5px；未解鎖＝壓暗奶油底
	var card_sb := StyleBoxFlat.new()
	if unlocked:
		card_sb.bg_color = COLOR_CARD_UNLOCKED
		card_sb.border_color = COLOR_ORANGE
		card_sb.set_border_width_all(2)
		card_sb.border_width_bottom = 5  ## 暖橘果凍厚底 5px
		card_sb.set_corner_radius_all(16)
		card_sb.shadow_color = Color(0.9, 0.5, 0.1, 0.15)
		card_sb.shadow_size = 4
		card_sb.shadow_offset = Vector2(0, 2)
	else:
		card_sb.bg_color = COLOR_CARD_LOCKED
		card_sb.border_color = COLOR_CARD_LOCKED_BORDER
		card_sb.set_border_width_all(2)
		card_sb.border_width_bottom = 3
		card_sb.set_corner_radius_all(16)

	card.add_theme_stylebox_override("panel", card_sb)

	var cm := MarginContainer.new()
	cm.add_theme_constant_override("margin_left", 14)
	cm.add_theme_constant_override("margin_right", 14)
	cm.add_theme_constant_override("margin_top", 10)
	cm.add_theme_constant_override("margin_bottom", 12)
	card.add_child(cm)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	cm.add_child(v)

	# 頂部：稱號名 + 解鎖狀態標籤
	var top_row := HBoxContainer.new()
	top_row.alignment = BoxContainer.ALIGNMENT_CENTER
	top_row.add_theme_constant_override("separation", 8)
	v.add_child(top_row)

	var name_lbl := Label.new()
	name_lbl.name = "NameLabel"
	name_lbl.text = str(entry.get("name", ""))
	if unlocked:
		_apply_label_style(name_lbl, 18, COLOR_TEXT_DARK, Color("#FFFDF8"), 2)
	else:
		_apply_label_style(name_lbl, 18, COLOR_TEXT_MUTED, Color(0, 0, 0, 0), 0)
	name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_lbl.clip_text = false
	top_row.add_child(name_lbl)

	# 狀態標籤（已解鎖 / 未解鎖，零 Emoji，字級 16）
	var badge_panel := PanelContainer.new()
	badge_panel.name = "BadgePanel"
	var b_sb := StyleBoxFlat.new()
	b_sb.set_corner_radius_all(10)
	b_sb.content_margin_left = 10
	b_sb.content_margin_right = 10
	b_sb.content_margin_top = 2
	b_sb.content_margin_bottom = 3

	var badge_lbl := Label.new()
	badge_lbl.name = "BadgeLabel"

	if unlocked:
		b_sb.bg_color = COLOR_ORANGE
		b_sb.border_color = COLOR_BORDER
		b_sb.set_border_width_all(2)
		b_sb.border_width_bottom = 3
		badge_lbl.text = _t("已解鎖")
		_apply_label_style(badge_lbl, 16, Color("#FFFFFF"), COLOR_BORDER, 2)
	else:
		b_sb.bg_color = Color("#DED6CA")
		b_sb.border_color = Color("#A89E90")
		b_sb.set_border_width_all(1)
		b_sb.border_width_bottom = 2
		badge_lbl.text = _t("未解鎖")
		_apply_label_style(badge_lbl, 16, Color("#706860"), Color(0, 0, 0, 0), 0)

	badge_panel.add_theme_stylebox_override("panel", b_sb)
	badge_panel.add_child(badge_lbl)
	top_row.add_child(badge_panel)

	# 底部：一句條件（條件仍清晰可讀，字級 16）
	var desc_lbl := Label.new()
	desc_lbl.name = "DescLabel"
	desc_lbl.text = str(entry.get("desc", ""))
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if unlocked:
		_apply_label_style(desc_lbl, 16, COLOR_DESC_UNLOCKED, Color(0, 0, 0, 0), 0)
	else:
		_apply_label_style(desc_lbl, 16, COLOR_DESC_LOCKED, Color(0, 0, 0, 0), 0)
	v.add_child(desc_lbl)

	# 點擊拇指觸控回饋
	card.gui_input.connect(func(event: InputEvent):
		if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			var am: Node = Engine.get_main_loop().root.get_node_or_null("AudioManager") if Engine.get_main_loop() else null
			if am and am.has_method("play_ui"):
				am.play_ui()
	)

	return card


func get_card_count() -> int:
	return _cards.size()


func get_cards() -> Array[PanelContainer]:
	return _cards


func _on_close() -> void:
	closed.emit()
	if _back_cb.is_valid():
		_back_cb.call()
	else:
		queue_free()


func _on_fortress() -> void:
	closed.emit()
	if _fortress_cb.is_valid():
		_fortress_cb.call()
	else:
		queue_free()
