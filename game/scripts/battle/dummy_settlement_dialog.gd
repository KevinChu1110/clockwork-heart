class_name DummySettlementDialog
extends Control
## 《發條之心》木人樁試招結算數據卡 (DummySettlementDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~32px 加粗帶深色厚描邊，零小字。
## 6. 零 emoji、零系統字型符號。
## 7. 「招」軸訓練回饋，不混用「器／魂」用語。
## 8. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換)。

signal confirmed()
signal retry_requested()

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 奶油米白底
const COLOR_CARD_WARM   := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_AMBER  := Color("#FFEED6")  ## 暖琥珀柔和卡片底
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_AMBER  := Color("#B05000")  ## 壓明度暖琥珀
const COLOR_TEXT_MUTED  := Color("#7A6E8A")  ## 輔助標籤灰紫

var _dialog_card: PanelContainer
var _damage_label: Label
var _time_label: Label
var _dps_label: Label
var _tip_label: Label
var _retry_btn: Button
var _confirm_btn: Button
var _cached_font: Font = null

var _title_lbl: Label
var _sub_lbl: Label
var _card1_header_lbl: Label
var _card1_sub_lbl: Label
var _card1_unit_lbl: Label
var _card2_header_lbl: Label
var _card2_sub_lbl: Label
var _card2_unit_lbl: Label
var _card3_header_lbl: Label
var _card3_sub_lbl: Label
var _card3_unit_lbl: Label
var _record_badge: PanelContainer
var _record_badge_lbl: Label
var _best_dps_lbl: Label
var _max_hit_label: Label
var _max_hit_title_lbl: Label
var _max_hit_unit_lbl: Label
var _total_hits_label: Label
var _total_hits_title_lbl: Label
var _total_hits_unit_lbl: Label

var _weapon_contrib_section: VBoxContainer
var _weapon_contrib_title_lbl: Label
var _weapon_swaps_capsule: PanelContainer
var _weapon_swaps_title_lbl: Label
var _weapon_swaps_value_lbl: Label
var _weapon_swaps_unit_lbl: Label
var _weapon_slot_cards: Array = []

var _total_damage: int = 0
var _elapsed_time: float = 0.0
var _dps: float = 0.0
var _best_dps: float = 0.0
var _max_hit_damage: int = 0
var _total_hit_count: int = 0
var _weapon_slot_damages: Dictionary = {0: 0, 1: 0, 2: 0}
var _weapon_slot_swaps: Dictionary = {0: 0, 1: 0, 2: 0}
var _weapon_swap_count: int = 0
var _weapon_bars: Array = []
var _is_new_record: bool = false
var _record_evaluated: bool = false
var _on_confirm: Callable = Callable()
var _on_retry: Callable = Callable()


static func _get_game_state() -> Object:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var n = (loop as SceneTree).root.get_node_or_null("GameState")
		if n != null:
			return n
	if Engine.has_singleton("GameState"):
		return Engine.get_singleton("GameState")
	return null


func _evaluate_record(stats: Dictionary = {}) -> void:
	_record_evaluated = true
	var gs = _get_game_state()
	var prev_best: float = 0.0
	if stats.has("best_dummy_dps"):
		prev_best = float(stats.get("best_dummy_dps", 0.0))
	elif gs != null and "best_dummy_dps" in gs:
		prev_best = float(gs.best_dummy_dps)

	if _dps > prev_best:
		_is_new_record = true
		_best_dps = _dps
		if gs != null and "best_dummy_dps" in gs:
			gs.best_dummy_dps = _dps
	else:
		_is_new_record = false
		_best_dps = prev_best


static func show_dialog(parent: Node, stats: Dictionary = {}, on_confirm: Callable = Callable(), on_retry: Callable = Callable()) -> Control:
	var dlg = load("res://scripts/battle/dummy_settlement_dialog.gd").new()
	dlg.setup(stats, on_confirm, on_retry)
	parent.add_child(dlg)
	return dlg


func setup(stats: Dictionary = {}, on_confirm: Callable = Callable(), on_retry: Callable = Callable()) -> void:
	_total_damage = int(stats.get("total_damage", 0))
	_elapsed_time = float(stats.get("elapsed_time", 0.0))
	_dps = float(stats.get("dps", 0.0))
	_max_hit_damage = int(stats.get("max_hit_damage", 0))
	_total_hit_count = int(stats.get("total_hit_count", 0))
	_weapon_slot_damages = stats.get("weapon_slot_damages", {0: 0, 1: 0, 2: 0}).duplicate(true)
	_weapon_slot_swaps = stats.get("weapon_slot_swaps", {0: 0, 1: 0, 2: 0}).duplicate(true)
	_weapon_swap_count = int(stats.get("weapon_swap_count", 0))
	_weapon_bars = stats.get("weapon_bars", []).duplicate(true)
	_on_confirm = on_confirm
	_on_retry = on_retry
	_evaluate_record(stats)

	if _dialog_card == null:
		_build_ui()
	_update_ui_texts()
	_refresh_display()


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	_refresh_display()


func _ready() -> void:
	name = "DummySettlementDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 95

	if ResourceLoader.exists(FONT_PATH) and _cached_font == null:
		_cached_font = load(FONT_PATH) as Font

	_connect_loc_signal()

	if not _record_evaluated:
		_evaluate_record({})

	if _dialog_card == null:
		_build_ui()
	_update_ui_texts()
	_refresh_display()


func _build_ui() -> void:
	if _dialog_card != null:
		return

	if ResourceLoader.exists(FONT_PATH) and _cached_font == null:
		_cached_font = load(FONT_PATH) as Font

	# 1. 全螢幕半透明遮罩 (Scrim) - 輕透半透明遮罩，使背後戰鬥場景清晰可見
	var scrim := ResponsiveUi.make_scrim(Color(0.05, 0.04, 0.08, 0.42))
	add_child(scrim)

	# 2. 置中容器
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	# 3. 彈窗主卡片 (寬 750px，浮空微陰影)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "DummySettlementCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 560)
	_dialog_card.add_theme_stylebox_override("panel", _create_floating_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 14)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	margin.add_child(v)

	# ── 標題列 + 關閉按鈕 ──
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_col := VBoxContainer.new()
	title_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_col.add_theme_constant_override("separation", 2)
	head.add_child(title_col)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.add_theme_font_size_override("font_size", 22)
	_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_title_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_title_lbl)

	_sub_lbl = Label.new()
	_sub_lbl.name = "SubTitleLabel"
	_sub_lbl.add_theme_font_size_override("font_size", 13)
	_sub_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	if _cached_font:
		_sub_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_sub_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_confirm_clicked)
	head.add_child(close_btn)

	# ── 分隔線 ──
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# ── 三項數據核心卡片 (總傷害 / 耗時 / DPS) ──
	var stats_hbox := HBoxContainer.new()
	stats_hbox.name = "StatsHBox"
	stats_hbox.add_theme_constant_override("separation", 12)
	v.add_child(stats_hbox)

	# 卡片 1: 本次總傷害
	var res1 := _build_metric_card(
		"TotalDamageCard",
		"DamageValueLabel",
		COLOR_CARD_GOLD,
		COLOR_TEXT_GOLD
	)
	_damage_label = res1.value_label
	_card1_header_lbl = res1.header_label
	_card1_sub_lbl = res1.sub_label
	_card1_unit_lbl = res1.unit_label
	stats_hbox.add_child(res1.card)

	# 卡片 2: 戰鬥耗時
	var res2 := _build_metric_card(
		"ElapsedTimeCard",
		"TimeValueLabel",
		COLOR_CARD_WARM,
		COLOR_TEXT_ORANGE
	)
	_time_label = res2.value_label
	_card2_header_lbl = res2.header_label
	_card2_sub_lbl = res2.sub_label
	_card2_unit_lbl = res2.unit_label
	stats_hbox.add_child(res2.card)

	# 卡片 3: 本次DPS
	var res3 := _build_metric_card(
		"DpsCard",
		"DpsValueLabel",
		COLOR_CARD_AMBER,
		COLOR_TEXT_AMBER
	)
	_dps_label = res3.value_label
	_card3_header_lbl = res3.header_label
	_card3_sub_lbl = res3.sub_label
	_card3_unit_lbl = res3.unit_label

	# 右上角金黃果凍「新紀錄」膠囊標籤（#FFD028 帶深藍紫描邊，零 Emoji）
	var badge_overlay := MarginContainer.new()
	badge_overlay.name = "BadgeOverlay"
	badge_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	badge_overlay.add_theme_constant_override("margin_top", 6)
	badge_overlay.add_theme_constant_override("margin_right", 8)
	res3.card.add_child(badge_overlay)

	var badge_box := HBoxContainer.new()
	badge_box.name = "BadgeBox"
	badge_box.alignment = BoxContainer.ALIGNMENT_END
	badge_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	badge_overlay.add_child(badge_box)

	_record_badge = PanelContainer.new()
	_record_badge.name = "NewRecordBadge"
	_record_badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var badge_sb := StyleBoxFlat.new()
	badge_sb.bg_color = COLOR_GOLD
	badge_sb.border_color = COLOR_BORDER
	badge_sb.set_border_width_all(2)
	badge_sb.border_width_bottom = 4
	badge_sb.set_corner_radius_all(10)
	badge_sb.content_margin_left = 8
	badge_sb.content_margin_right = 8
	badge_sb.content_margin_top = 2
	badge_sb.content_margin_bottom = 4
	_record_badge.add_theme_stylebox_override("panel", badge_sb)

	_record_badge_lbl = Label.new()
	_record_badge_lbl.name = "NewRecordLabel"
	_record_badge_lbl.text = _t("新紀錄")
	_record_badge_lbl.add_theme_font_size_override("font_size", 12)
	_record_badge_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_record_badge_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_record_badge_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_record_badge_lbl.add_theme_font_override("font", _cached_font)
	_record_badge.add_child(_record_badge_lbl)
	badge_box.add_child(_record_badge)

	# 底部歷史最佳 DPS 輔助說明
	_best_dps_lbl = Label.new()
	_best_dps_lbl.name = "BestDpsLabel"
	_best_dps_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_best_dps_lbl.add_theme_font_size_override("font_size", 12)
	_best_dps_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_best_dps_lbl.add_theme_font_override("font", _cached_font)
	var dps_vbox: VBoxContainer = res3.get("vbox") as VBoxContainer
	if dps_vbox:
		dps_vbox.add_child(_best_dps_lbl)

	stats_hbox.add_child(res3.card)

	# ── 多巴胺雙膠囊數據列 (最高單擊 / 總命中次數) ──
	var capsules_hbox := HBoxContainer.new()
	capsules_hbox.name = "CapsulesHBox"
	capsules_hbox.add_theme_constant_override("separation", 14)
	v.add_child(capsules_hbox)

	# 膠囊 1: 最高單擊 (多巴胺天藍柔和卡片底，字級 >= 14px 加粗深藍紫文字，零 Emoji)
	var res_capsule1 := _build_capsule_card(
		"MaxHitCapsule",
		"MaxHitValueLabel",
		Color("#F0F7FF"),
		COLOR_SKY
	)
	_max_hit_label = res_capsule1.value_label
	_max_hit_title_lbl = res_capsule1.title_label
	_max_hit_unit_lbl = res_capsule1.unit_label
	capsules_hbox.add_child(res_capsule1.card)

	# 膠囊 2: 總命中次數 (多巴胺薄荷綠柔和卡片底，字級 >= 14px 加粗深藍紫文字，零 Emoji)
	var res_capsule2 := _build_capsule_card(
		"TotalHitsCapsule",
		"TotalHitsValueLabel",
		Color("#F0FAF2"),
		COLOR_MINT
	)
	_total_hits_label = res_capsule2.value_label
	_total_hits_title_lbl = res_capsule2.title_label
	_total_hits_unit_lbl = res_capsule2.unit_label
	capsules_hbox.add_child(res_capsule2.card)

	# ── 多巴胺三欄武器貢獻卡與輪替次數展示列 ──
	_build_weapon_contribution_section(v)

	# ── 提示說明卡片 ──
	var tip_card := PanelContainer.new()
	tip_card.name = "TipCard"
	tip_card.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 16))
	v.add_child(tip_card)

	var tip_margin := MarginContainer.new()
	tip_margin.add_theme_constant_override("margin_left", 16)
	tip_margin.add_theme_constant_override("margin_right", 16)
	tip_margin.add_theme_constant_override("margin_top", 10)
	tip_margin.add_theme_constant_override("margin_bottom", 10)
	tip_card.add_child(tip_margin)

	_tip_label = Label.new()
	_tip_label.name = "TipLabel"
	_tip_label.add_theme_font_size_override("font_size", 14)
	_tip_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_tip_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if _cached_font:
		_tip_label.add_theme_font_override("font", _cached_font)
	tip_margin.add_child(_tip_label)

	# ── 底部按鈕區（再次試招與完成試招雙鍵並列） ──
	var btn_center := CenterContainer.new()
	btn_center.name = "ButtonCenterContainer"
	v.add_child(btn_center)

	var btn_hbox := HBoxContainer.new()
	btn_hbox.name = "ButtonHBox"
	btn_hbox.add_theme_constant_override("separation", 18)
	btn_center.add_child(btn_hbox)

	# 1. 再次試招按鈕（暖橘立體厚底 >= 48px，高度 52px）
	_retry_btn = Button.new()
	_retry_btn.name = "RetryButton"
	_retry_btn.custom_minimum_size = Vector2(200, 52)
	_retry_btn.add_theme_font_size_override("font_size", 18)
	_retry_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_retry_btn.add_theme_font_override("font", _cached_font)

	var retry_normal := _create_button_style(COLOR_ORANGE, COLOR_BORDER, 6, 20)
	var retry_hover := _create_button_style(Color("#FFB535"), COLOR_BORDER, 6, 20)
	var retry_pressed := _create_button_style(Color("#E08000"), COLOR_BORDER, 2, 20)
	retry_pressed.content_margin_top = 12
	retry_pressed.content_margin_bottom = 8

	_retry_btn.add_theme_stylebox_override("normal", retry_normal)
	_retry_btn.add_theme_stylebox_override("hover", retry_hover)
	_retry_btn.add_theme_stylebox_override("pressed", retry_pressed)
	_retry_btn.add_theme_stylebox_override("focus", retry_normal)

	_retry_btn.pressed.connect(_on_retry_clicked)
	btn_hbox.add_child(_retry_btn)

	# 2. 完成試招按鈕（金黃立體厚底 >= 48px，高度 52px）
	_confirm_btn = Button.new()
	_confirm_btn.name = "ConfirmButton"
	_confirm_btn.custom_minimum_size = Vector2(200, 52)
	_confirm_btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_confirm_btn.add_theme_font_size_override("font_size", 18)
	_confirm_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_confirm_btn.add_theme_font_override("font", _cached_font)

	var btn_normal := _create_button_style(COLOR_GOLD, COLOR_BORDER, 6, 20)
	var btn_hover := _create_button_style(Color("#FFE050"), COLOR_BORDER, 6, 20)
	var btn_pressed := _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 20)
	btn_pressed.content_margin_top = 12
	btn_pressed.content_margin_bottom = 8

	_confirm_btn.add_theme_stylebox_override("normal", btn_normal)
	_confirm_btn.add_theme_stylebox_override("hover", btn_hover)
	_confirm_btn.add_theme_stylebox_override("pressed", btn_pressed)
	_confirm_btn.add_theme_stylebox_override("focus", btn_normal)

	_confirm_btn.pressed.connect(_on_confirm_clicked)
	btn_hbox.add_child(_confirm_btn)

	_update_ui_texts()


func _update_ui_texts() -> void:
	if _title_lbl and is_instance_valid(_title_lbl):
		_title_lbl.text = _t("木人試招數據卡")
	if _sub_lbl and is_instance_valid(_sub_lbl):
		_sub_lbl.text = _t("武術館「招」軸訓練回饋 · 能量消耗 0")

	if _card1_header_lbl and is_instance_valid(_card1_header_lbl):
		_card1_header_lbl.text = _t("本次總傷害")
	if _card1_sub_lbl and is_instance_valid(_card1_sub_lbl):
		_card1_sub_lbl.text = _t("招式命中累積")
	if _card1_unit_lbl and is_instance_valid(_card1_unit_lbl):
		_card1_unit_lbl.text = _t("點")

	if _card2_header_lbl and is_instance_valid(_card2_header_lbl):
		_card2_header_lbl.text = _t("試招耗時")
	if _card2_sub_lbl and is_instance_valid(_card2_sub_lbl):
		_card2_sub_lbl.text = _t("戰鬥歷程秒數")
	if _card2_unit_lbl and is_instance_valid(_card2_unit_lbl):
		_card2_unit_lbl.text = _t("秒")

	if _card3_header_lbl and is_instance_valid(_card3_header_lbl):
		_card3_header_lbl.text = _t("秒傷 (DPS)")
	if _card3_sub_lbl and is_instance_valid(_card3_sub_lbl):
		_card3_sub_lbl.text = _t("每秒平均輸出")
	if _card3_unit_lbl and is_instance_valid(_card3_unit_lbl):
		_card3_unit_lbl.text = _t("點 / 秒")

	if _tip_label and is_instance_valid(_tip_label):
		_tip_label.text = _t("木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。")
	if _retry_btn and is_instance_valid(_retry_btn):
		_retry_btn.text = _t("再次試招")
	if _confirm_btn and is_instance_valid(_confirm_btn):
		_confirm_btn.text = _t("完成試招")
	if _record_badge_lbl and is_instance_valid(_record_badge_lbl):
		_record_badge_lbl.text = _t("新紀錄")
	if _best_dps_lbl and is_instance_valid(_best_dps_lbl):
		_best_dps_lbl.text = _t("歷史最佳：%.1f DPS") % _best_dps

	if _max_hit_title_lbl and is_instance_valid(_max_hit_title_lbl):
		_max_hit_title_lbl.text = _t("最高單擊")
	if _max_hit_unit_lbl and is_instance_valid(_max_hit_unit_lbl):
		_max_hit_unit_lbl.text = _t("點")
	if _total_hits_title_lbl and is_instance_valid(_total_hits_title_lbl):
		_total_hits_title_lbl.text = _t("總命中次數")
	if _total_hits_unit_lbl and is_instance_valid(_total_hits_unit_lbl):
		_total_hits_unit_lbl.text = _t("次")

	if _weapon_contrib_title_lbl and is_instance_valid(_weapon_contrib_title_lbl):
		_weapon_contrib_title_lbl.text = _t("武器傷害貢獻")
	if _weapon_swaps_title_lbl and is_instance_valid(_weapon_swaps_title_lbl):
		_weapon_swaps_title_lbl.text = _t("輪替切換")
	if _weapon_swaps_unit_lbl and is_instance_valid(_weapon_swaps_unit_lbl):
		_weapon_swaps_unit_lbl.text = _t("次")

	for slot_idx in range(_weapon_slot_cards.size()):
		var c_data: Dictionary = _weapon_slot_cards[slot_idx]
		var slot_title_lbl: Label = c_data.get("slot_title_label")
		if slot_title_lbl and is_instance_valid(slot_title_lbl):
			slot_title_lbl.text = _t("欄位 %d") % (slot_idx + 1)


func _build_metric_card(card_name: String, val_name: String, bg_col: Color, accent_col: Color) -> Dictionary:
	var card := PanelContainer.new()
	card.name = card_name
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(0, 112)
	card.add_theme_stylebox_override("panel", _create_inner_card_style(bg_col, COLOR_BORDER, 2, 4, 18))

	var m := MarginContainer.new()
	m.name = "Margin"
	m.add_theme_constant_override("margin_left", 12)
	m.add_theme_constant_override("margin_right", 12)
	m.add_theme_constant_override("margin_top", 8)
	m.add_theme_constant_override("margin_bottom", 8)
	card.add_child(m)

	var cv := VBoxContainer.new()
	cv.name = "VBox"
	cv.add_theme_constant_override("separation", 4)
	cv.alignment = BoxContainer.ALIGNMENT_CENTER
	m.add_child(cv)

	var h_lbl := Label.new()
	h_lbl.name = "HeaderLabel"
	h_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	h_lbl.add_theme_font_size_override("font_size", 16)
	h_lbl.add_theme_color_override("font_color", accent_col)
	if _cached_font:
		h_lbl.add_theme_font_override("font", _cached_font)
	cv.add_child(h_lbl)

	var v_row := HBoxContainer.new()
	v_row.name = "ValueRow"
	v_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v_row.add_theme_constant_override("separation", 4)
	cv.add_child(v_row)

	var val_lbl := Label.new()
	val_lbl.name = val_name
	val_lbl.text = "0"
	val_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	val_lbl.add_theme_font_size_override("font_size", 30)
	val_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	val_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	val_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		val_lbl.add_theme_font_override("font", _cached_font)
	v_row.add_child(val_lbl)

	var u_lbl := Label.new()
	u_lbl.name = "UnitLabel"
	u_lbl.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
	u_lbl.add_theme_font_size_override("font_size", 14)
	u_lbl.add_theme_color_override("font_color", accent_col)
	if _cached_font:
		u_lbl.add_theme_font_override("font", _cached_font)
	v_row.add_child(u_lbl)

	var sub_tag := Label.new()
	sub_tag.name = "SubTagLabel"
	sub_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub_tag.add_theme_font_size_override("font_size", 12)
	sub_tag.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		sub_tag.add_theme_font_override("font", _cached_font)
	cv.add_child(sub_tag)

	return {
		"card": card,
		"value_label": val_lbl,
		"header_label": h_lbl,
		"sub_label": sub_tag,
		"unit_label": u_lbl,
		"vbox": cv
	}


func _build_capsule_card(card_name: String, val_name: String, bg_col: Color, accent_col: Color) -> Dictionary:
	var card := PanelContainer.new()
	card.name = card_name
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(0, 44)
	card.add_theme_stylebox_override("panel", _create_inner_card_style(bg_col, COLOR_BORDER, 2, 3, 16))

	var m := MarginContainer.new()
	m.name = "Margin"
	m.add_theme_constant_override("margin_left", 16)
	m.add_theme_constant_override("margin_right", 16)
	m.add_theme_constant_override("margin_top", 8)
	m.add_theme_constant_override("margin_bottom", 8)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.name = "HBox"
	h.add_theme_constant_override("separation", 8)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	m.add_child(h)

	var t_lbl := Label.new()
	t_lbl.name = "TitleLabel"
	t_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	t_lbl.add_theme_font_size_override("font_size", 14)
	t_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		t_lbl.add_theme_font_override("font", _cached_font)
	h.add_child(t_lbl)

	var val_lbl := Label.new()
	val_lbl.name = val_name
	val_lbl.text = "0"
	val_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	val_lbl.add_theme_font_size_override("font_size", 20)
	val_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	val_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	val_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		val_lbl.add_theme_font_override("font", _cached_font)
	h.add_child(val_lbl)

	var u_lbl := Label.new()
	u_lbl.name = "UnitLabel"
	u_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	u_lbl.add_theme_font_size_override("font_size", 14)
	u_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		u_lbl.add_theme_font_override("font", _cached_font)
	h.add_child(u_lbl)

	return {
		"card": card,
		"value_label": val_lbl,
		"title_label": t_lbl,
		"unit_label": u_lbl,
	}


func _get_quality_info(quality_key: String) -> Dictionary:
	match quality_key:
		"uncommon":
			return {"label": _t("良品"), "color": Color("#2E9E4A")}
		"rare":
			return {"label": _t("上品"), "color": Color("#2575FC")}
		"epic":
			return {"label": _t("極品"), "color": Color("#9B51E0")}
		"legendary":
			return {"label": _t("神品"), "color": Color("#FFA010")}
		"none", "empty", "locked":
			return {"label": _t("未裝備"), "color": Color("#8E8A9F")}
		_:
			return {"label": _t("凡品"), "color": Color("#8E8A9F")}


func _build_weapon_contribution_section(parent: VBoxContainer) -> void:
	_weapon_contrib_section = VBoxContainer.new()
	_weapon_contrib_section.name = "WeaponContributionSection"
	_weapon_contrib_section.add_theme_constant_override("separation", 6)
	parent.add_child(_weapon_contrib_section)

	# 1. 頂部標題與輪替次數膠囊
	var header_hbox := HBoxContainer.new()
	header_hbox.name = "WeaponContribHeaderHBox"
	header_hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	_weapon_contrib_section.add_child(header_hbox)

	_weapon_contrib_title_lbl = Label.new()
	_weapon_contrib_title_lbl.name = "WeaponContribTitleLabel"
	_weapon_contrib_title_lbl.text = _t("武器傷害貢獻")
	_weapon_contrib_title_lbl.add_theme_font_size_override("font_size", 14)
	_weapon_contrib_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_weapon_contrib_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_weapon_contrib_title_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_weapon_contrib_title_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(_weapon_contrib_title_lbl)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	spacer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	header_hbox.add_child(spacer)

	# 輪替切換次數膠囊卡片 (琥珀柔和底 #FFEED6, 圓角 12px, 零 Emoji)
	_weapon_swaps_capsule = PanelContainer.new()
	_weapon_swaps_capsule.name = "WeaponSwapsCapsule"
	_weapon_swaps_capsule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var swaps_sb := StyleBoxFlat.new()
	swaps_sb.bg_color = Color("#FFF3E0")
	swaps_sb.border_color = COLOR_BORDER
	swaps_sb.set_border_width_all(2)
	swaps_sb.border_width_bottom = 3
	swaps_sb.set_corner_radius_all(12)
	swaps_sb.content_margin_left = 10
	swaps_sb.content_margin_right = 10
	swaps_sb.content_margin_top = 3
	swaps_sb.content_margin_bottom = 3
	_weapon_swaps_capsule.add_theme_stylebox_override("panel", swaps_sb)
	header_hbox.add_child(_weapon_swaps_capsule)

	var swaps_hbox := HBoxContainer.new()
	swaps_hbox.name = "SwapsHBox"
	swaps_hbox.add_theme_constant_override("separation", 6)
	swaps_hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	_weapon_swaps_capsule.add_child(swaps_hbox)

	_weapon_swaps_title_lbl = Label.new()
	_weapon_swaps_title_lbl.name = "TitleLabel"
	_weapon_swaps_title_lbl.text = _t("輪替切換")
	_weapon_swaps_title_lbl.add_theme_font_size_override("font_size", 12)
	_weapon_swaps_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_AMBER)
	if _cached_font:
		_weapon_swaps_title_lbl.add_theme_font_override("font", _cached_font)
	swaps_hbox.add_child(_weapon_swaps_title_lbl)

	_weapon_swaps_value_lbl = Label.new()
	_weapon_swaps_value_lbl.name = "SwapsValueLabel"
	_weapon_swaps_value_lbl.text = "0"
	_weapon_swaps_value_lbl.add_theme_font_size_override("font_size", 15)
	_weapon_swaps_value_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_weapon_swaps_value_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_weapon_swaps_value_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_weapon_swaps_value_lbl.add_theme_font_override("font", _cached_font)
	swaps_hbox.add_child(_weapon_swaps_value_lbl)

	_weapon_swaps_unit_lbl = Label.new()
	_weapon_swaps_unit_lbl.name = "UnitLabel"
	_weapon_swaps_unit_lbl.text = _t("次")
	_weapon_swaps_unit_lbl.add_theme_font_size_override("font_size", 12)
	_weapon_swaps_unit_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_weapon_swaps_unit_lbl.add_theme_font_override("font", _cached_font)
	swaps_hbox.add_child(_weapon_swaps_unit_lbl)

	# 2. 三欄武器卡片列 (WeaponSlotsHBox)
	var slots_hbox := HBoxContainer.new()
	slots_hbox.name = "WeaponSlotsHBox"
	slots_hbox.add_theme_constant_override("separation", 10)
	_weapon_contrib_section.add_child(slots_hbox)

	_weapon_slot_cards.clear()
	var slot_bg_colors := [Color("#F4F8FD"), Color("#F4FAF5"), Color("#FFF9EE")]
	var slot_accent_colors := [COLOR_SKY, COLOR_MINT, COLOR_ORANGE]

	for slot_idx in range(3):
		var card_dict := _build_single_weapon_slot_card(
			slot_idx,
			slot_bg_colors[slot_idx],
			slot_accent_colors[slot_idx]
		)
		slots_hbox.add_child(card_dict.card)
		_weapon_slot_cards.append(card_dict)


func _build_single_weapon_slot_card(slot_idx: int, bg_col: Color, accent_col: Color) -> Dictionary:
	var card := PanelContainer.new()
	card.name = "WeaponSlotCard_%d" % slot_idx
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(0, 84)
	card.add_theme_stylebox_override("panel", _create_inner_card_style(bg_col, COLOR_BORDER, 2, 3, 14))

	var m := MarginContainer.new()
	m.name = "Margin"
	m.add_theme_constant_override("margin_left", 10)
	m.add_theme_constant_override("margin_right", 10)
	m.add_theme_constant_override("margin_top", 6)
	m.add_theme_constant_override("margin_bottom", 6)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.name = "VBox"
	v.add_theme_constant_override("separation", 3)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	m.add_child(v)

	# Row 1: 欄位標籤與品質色階標籤
	var row1 := HBoxContainer.new()
	row1.name = "HeaderRow"
	v.add_child(row1)

	var slot_title_lbl := Label.new()
	slot_title_lbl.name = "SlotTitleLabel"
	slot_title_lbl.text = _t("欄位 %d") % (slot_idx + 1)
	slot_title_lbl.add_theme_font_size_override("font_size", 12)
	slot_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		slot_title_lbl.add_theme_font_override("font", _cached_font)
	row1.add_child(slot_title_lbl)

	var row1_sp := Control.new()
	row1_sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row1.add_child(row1_sp)

	var quality_badge := PanelContainer.new()
	quality_badge.name = "QualityBadge"
	var q_sb := StyleBoxFlat.new()
	q_sb.bg_color = Color("#8E8A9F")
	q_sb.set_corner_radius_all(6)
	q_sb.content_margin_left = 6
	q_sb.content_margin_right = 6
	q_sb.content_margin_top = 1
	q_sb.content_margin_bottom = 2
	quality_badge.add_theme_stylebox_override("panel", q_sb)
	row1.add_child(quality_badge)

	var quality_lbl := Label.new()
	quality_lbl.name = "QualityLabel"
	quality_lbl.text = _t("凡品")
	quality_lbl.add_theme_font_size_override("font_size", 10)
	quality_lbl.add_theme_color_override("font_color", Color.WHITE)
	if _cached_font:
		quality_lbl.add_theme_font_override("font", _cached_font)
	quality_badge.add_child(quality_lbl)

	# Row 2: 武器名稱
	var name_lbl := Label.new()
	name_lbl.name = "WeaponNameLabel"
	name_lbl.text = _t("未裝備")
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	name_lbl.add_theme_font_size_override("font_size", 13)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	name_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	name_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	v.add_child(name_lbl)

	# Row 3: 傷害佔比與數值
	var row3 := HBoxContainer.new()
	row3.name = "DamageRow"
	row3.add_theme_constant_override("separation", 6)
	v.add_child(row3)

	var pct_lbl := Label.new()
	pct_lbl.name = "DamagePercentLabel"
	pct_lbl.text = "0.0%"
	pct_lbl.add_theme_font_size_override("font_size", 15)
	pct_lbl.add_theme_color_override("font_color", accent_col)
	pct_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	pct_lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		pct_lbl.add_theme_font_override("font", _cached_font)
	row3.add_child(pct_lbl)

	var dmg_val_lbl := Label.new()
	dmg_val_lbl.name = "DamageValueLabel"
	dmg_val_lbl.text = "(0 點)"
	dmg_val_lbl.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
	dmg_val_lbl.add_theme_font_size_override("font_size", 11)
	dmg_val_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		dmg_val_lbl.add_theme_font_override("font", _cached_font)
	row3.add_child(dmg_val_lbl)

	# Row 4: 傷害進度條 (ProgressBar)
	var bar := ProgressBar.new()
	bar.name = "DamageProgressBar"
	bar.custom_minimum_size = Vector2(0, 6)
	bar.show_percentage = false
	bar.min_value = 0.0
	bar.max_value = 100.0
	bar.value = 0.0

	var bar_bg := StyleBoxFlat.new()
	bar_bg.bg_color = Color("#E4E0D8")
	bar_bg.set_corner_radius_all(3)
	bar.add_theme_stylebox_override("background", bar_bg)

	var bar_fill := StyleBoxFlat.new()
	bar_fill.bg_color = accent_col
	bar_fill.set_corner_radius_all(3)
	bar.add_theme_stylebox_override("fill", bar_fill)
	v.add_child(bar)

	return {
		"card": card,
		"slot_title_label": slot_title_lbl,
		"quality_badge": quality_badge,
		"quality_label": quality_lbl,
		"name_label": name_lbl,
		"percent_label": pct_lbl,
		"damage_label": dmg_val_lbl,
		"progress_bar": bar,
		"quality_stylebox": q_sb,
		"accent_color": accent_col,
	}


func _refresh_display() -> void:
	if _damage_label:
		_damage_label.text = str(_total_damage)
	if _time_label:
		_time_label.text = "%.1f" % _elapsed_time
	if _dps_label:
		_dps_label.text = "%.1f" % _dps
	if _max_hit_label:
		_max_hit_label.text = str(_max_hit_damage)
	if _total_hits_label:
		_total_hits_label.text = str(_total_hit_count)
	if _record_badge:
		_record_badge.visible = _is_new_record
	if _best_dps_lbl:
		_best_dps_lbl.visible = not _is_new_record
		_best_dps_lbl.text = _t("歷史最佳：%.1f DPS") % _best_dps

	if _weapon_swaps_value_lbl and is_instance_valid(_weapon_swaps_value_lbl):
		_weapon_swaps_value_lbl.text = str(_weapon_swap_count)

	for slot_idx in range(_weapon_slot_cards.size()):
		var c_data: Dictionary = _weapon_slot_cards[slot_idx]
		var dmg: int = int(_weapon_slot_damages.get(slot_idx, 0))
		var pct: float = (float(dmg) / float(_total_damage) * 100.0) if _total_damage > 0 else 0.0

		var bar_info: Dictionary = {}
		if slot_idx < _weapon_bars.size():
			bar_info = _weapon_bars[slot_idx]

		var w_name: String = str(bar_info.get("name", ""))
		var is_empty: bool = bool(bar_info.get("empty", w_name.is_empty()))
		if is_empty or w_name.is_empty():
			w_name = _t("未裝備")

		var q_key: String = str(bar_info.get("quality", "common"))
		if is_empty:
			q_key = "none"
		var q_info: Dictionary = _get_quality_info(q_key)

		var name_lbl: Label = c_data.get("name_label")
		if name_lbl and is_instance_valid(name_lbl):
			name_lbl.text = w_name

		var q_lbl: Label = c_data.get("quality_label")
		if q_lbl and is_instance_valid(q_lbl):
			q_lbl.text = q_info.label

		var q_sb: StyleBoxFlat = c_data.get("quality_stylebox")
		if q_sb:
			q_sb.bg_color = q_info.color

		var pct_lbl: Label = c_data.get("percent_label")
		if pct_lbl and is_instance_valid(pct_lbl):
			pct_lbl.text = "%.1f%%" % pct

		var dmg_lbl: Label = c_data.get("damage_label")
		if dmg_lbl and is_instance_valid(dmg_lbl):
			dmg_lbl.text = "(%d %s)" % [dmg, _t("點")]

		var pbar: ProgressBar = c_data.get("progress_bar")
		if pbar and is_instance_valid(pbar):
			pbar.value = pct


func _on_confirm_clicked() -> void:
	confirmed.emit()
	if _on_confirm.is_valid():
		_on_confirm.call()
	queue_free()


func _on_retry_clicked() -> void:
	retry_requested.emit()
	if _on_retry.is_valid():
		_on_retry.call()
	queue_free()


func get_total_damage() -> int:
	return _total_damage


func get_elapsed_time() -> float:
	return _elapsed_time


func get_dps() -> float:
	return _dps


func get_damage_text() -> String:
	return _damage_label.text if _damage_label else ""


func get_time_text() -> String:
	return _time_label.text if _time_label else ""


func get_dps_text() -> String:
	return _dps_label.text if _dps_label else ""


func get_max_hit_damage() -> int:
	return _max_hit_damage


func get_total_hit_count() -> int:
	return _total_hit_count


func get_max_hit_text() -> String:
	return _max_hit_label.text if _max_hit_label else ""


func get_total_hits_text() -> String:
	return _total_hits_label.text if _total_hits_label else ""


func get_max_hit_title_text() -> String:
	return _max_hit_title_lbl.text if _max_hit_title_lbl else ""


func get_total_hits_title_text() -> String:
	return _total_hits_title_lbl.text if _total_hits_title_lbl else ""


func get_title_text() -> String:
	return _title_lbl.text if _title_lbl else ""


func get_subtitle_text() -> String:
	return _sub_lbl.text if _sub_lbl else ""


func get_tip_text() -> String:
	return _tip_label.text if _tip_label else ""


func get_retry_text() -> String:
	return _retry_btn.text if _retry_btn else ""


func get_confirm_text() -> String:
	return _confirm_btn.text if _confirm_btn else ""


func is_new_record() -> bool:
	return _is_new_record


func get_best_dps() -> float:
	return _best_dps


func get_best_dps_text() -> String:
	return _best_dps_lbl.text if _best_dps_lbl else ""


func get_record_badge_text() -> String:
	return _record_badge_lbl.text if _record_badge_lbl else ""


func is_record_badge_visible() -> bool:
	return _record_badge != null and _record_badge.visible


func is_best_dps_label_visible() -> bool:
	return _best_dps_lbl != null and _best_dps_lbl.visible


func get_record_badge() -> Control:
	return _record_badge


func get_best_dps_label() -> Label:
	return _best_dps_lbl


func get_weapon_slot_damage(slot: int) -> int:
	return int(_weapon_slot_damages.get(slot, 0))


func get_weapon_slot_percent(slot: int) -> float:
	if _total_damage <= 0:
		return 0.0
	return float(get_weapon_slot_damage(slot)) / float(_total_damage) * 100.0


func get_weapon_swap_count() -> int:
	return _weapon_swap_count


func get_weapon_swaps_text() -> String:
	return _weapon_swaps_value_lbl.text if _weapon_swaps_value_lbl else ""


func get_weapon_contrib_title_text() -> String:
	return _weapon_contrib_title_lbl.text if _weapon_contrib_title_lbl else ""


func get_weapon_swaps_title_text() -> String:
	return _weapon_swaps_title_lbl.text if _weapon_swaps_title_lbl else ""


func get_weapon_slot_card(slot: int) -> Control:
	if slot >= 0 and slot < _weapon_slot_cards.size():
		return _weapon_slot_cards[slot].get("card")
	return null


func get_weapon_slot_name(slot: int) -> String:
	if slot >= 0 and slot < _weapon_slot_cards.size():
		var lbl: Label = _weapon_slot_cards[slot].get("name_label")
		return lbl.text if lbl else ""
	return ""


func get_weapon_slot_quality_text(slot: int) -> String:
	if slot >= 0 and slot < _weapon_slot_cards.size():
		var lbl: Label = _weapon_slot_cards[slot].get("quality_label")
		return lbl.text if lbl else ""
	return ""


func get_weapon_slot_percent_text(slot: int) -> String:
	if slot >= 0 and slot < _weapon_slot_cards.size():
		var lbl: Label = _weapon_slot_cards[slot].get("percent_label")
		return lbl.text if lbl else ""
	return ""


func get_weapon_slot_damage_text(slot: int) -> String:
	if slot >= 0 and slot < _weapon_slot_cards.size():
		var lbl: Label = _weapon_slot_cards[slot].get("damage_label")
		return lbl.text if lbl else ""
	return ""


func _create_floating_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	return sb


func _create_inner_card_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 18) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 18
	sb.content_margin_right = 18
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8 + bottom_border
	return sb
