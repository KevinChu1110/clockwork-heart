class_name BattleDefeatDialog
extends Control
## 《發條之心》戰鬥失敗結算彈窗（含看廣告二次機會復活掛鉤）
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 零系統 emoji、零開發用語。
## 6. 連接 EnergySystem 看廣告復活二次機會邏輯。

signal revive_selected()
signal give_up_selected()

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const MockAdDialogScript := preload("res://scripts/ui/mock_ad_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## ── 多巴胺鮮亮色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫文字
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉
const COLOR_TEXT_MINT  := Color("#1A7A30")  ## 壓明度薄荷綠

var _dialog_card: PanelContainer
var _revive_btn: Button
var _hint_lbl: Label
var _tip_lbl: Label
var _cached_font: Font = null
var _mode: String = ""

var _on_revive: Callable = Callable()
var _on_give_up: Callable = Callable()


static func show_dialog(parent: Node, on_revive: Callable = Callable(), on_give_up: Callable = Callable(), mode: String = "") -> Control:
	var dlg = load("res://scripts/battle/battle_defeat_dialog.gd").new()
	dlg.setup(on_revive, on_give_up, mode)
	parent.add_child(dlg)
	return dlg


func setup(on_revive: Callable = Callable(), on_give_up: Callable = Callable(), mode: String = "") -> void:
	_on_revive = on_revive
	_on_give_up = on_give_up
	_mode = mode


func _ready() -> void:
	name = "BattleDefeatDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 95

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build_ui()
	_refresh_display()


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	# 2. 置中卡片 (寬 750px)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "DefeatCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 420)
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 18)
	margin.add_theme_constant_override("margin_bottom", 20)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	margin.add_child(v)

	# 標題列 + 關閉鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.text = _t("戰鬥失敗")
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_PINK)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_give_up_clicked)
	head.add_child(close_btn)

	# 分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_PINK
	v.add_child(sep)

	# 說明卡片
	var desc_card := PanelContainer.new()
	desc_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	v.add_child(desc_card)

	var dc_m := MarginContainer.new()
	dc_m.add_theme_constant_override("margin_left", 20)
	dc_m.add_theme_constant_override("margin_right", 20)
	dc_m.add_theme_constant_override("margin_top", 14)
	dc_m.add_theme_constant_override("margin_bottom", 14)
	desc_card.add_child(dc_m)

	var dc_v := VBoxContainer.new()
	dc_v.add_theme_constant_override("separation", 8)
	dc_m.add_child(dc_v)

	var sub_lbl := Label.new()
	sub_lbl.text = _t("發條動能耗盡，齒輪暫時停擺！")
	sub_lbl.add_theme_font_size_override("font_size", 19)
	sub_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		sub_lbl.add_theme_font_override("font", _cached_font)
	dc_v.add_child(sub_lbl)

	var hint_lbl := Label.new()
	_hint_lbl = hint_lbl
	hint_lbl.text = _t("二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！")
	hint_lbl.add_theme_font_size_override("font_size", 15)
	hint_lbl.add_theme_color_override("font_color", COLOR_TEXT_MINT)
	if _cached_font:
		hint_lbl.add_theme_font_override("font", _cached_font)
	dc_v.add_child(hint_lbl)

	var tip_lbl := Label.new()
	_tip_lbl = tip_lbl
	tip_lbl.text = _t("若是選擇承認敗北，將返回城鎮整頓裝備與招式。")
	tip_lbl.add_theme_font_size_override("font_size", 15)
	tip_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		tip_lbl.add_theme_font_override("font", _cached_font)
	v.add_child(tip_lbl)

	# 底部操作按鈕 (高度 >= 50px)
	var btn_h := HBoxContainer.new()
	btn_h.add_theme_constant_override("separation", 16)
	btn_h.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(btn_h)

	# 觀看廣告立即復活按鈕 (珊瑚粉/薄荷綠立體果凍厚底)
	_revive_btn = Button.new()
	_revive_btn.name = "ReviveAdBtn"
	_revive_btn.custom_minimum_size = Vector2(340, 52)
	_revive_btn.add_theme_font_size_override("font_size", 18)
	_revive_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	_revive_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_revive_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_revive_btn.add_theme_font_override("font", _cached_font)
	_revive_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6))
	_revive_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5CE879"), COLOR_BORDER, 6))
	_revive_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3DBB55"), COLOR_BORDER, 2))
	_revive_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#B0ADBE"), COLOR_BORDER, 3))
	_revive_btn.pressed.connect(_on_revive_ad_clicked)
	btn_h.add_child(_revive_btn)

	# 結束戰鬥按鈕 (溫暖米黃/橙底)
	var give_up_btn := Button.new()
	give_up_btn.name = "GiveUpBtn"
	give_up_btn.text = _t("結束戰鬥")
	give_up_btn.custom_minimum_size = Vector2(180, 52)
	give_up_btn.add_theme_font_size_override("font_size", 18)
	give_up_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		give_up_btn.add_theme_font_override("font", _cached_font)
	give_up_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 6))
	give_up_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFF0D0"), COLOR_BORDER, 6))
	give_up_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#FFE0A0"), COLOR_BORDER, 2))
	give_up_btn.pressed.connect(_on_give_up_clicked)
	btn_h.add_child(give_up_btn)


func _is_ad_removed() -> bool:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var es: Node = (loop as SceneTree).root.get_node_or_null("EnergySystem")
		if es and es.has_method("is_ad_removed"):
			return bool(es.call("is_ad_removed"))
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if "has_removed_ads" in gs:
				return bool(gs.get("has_removed_ads"))
			if gs.has_method("get_flag"):
				return bool(gs.call("get_flag", "has_removed_ads", false))
	return false


func _refresh_display() -> void:
	var left := 0
	var cap := 3
	var can_claim := false
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es:
		if es.has_method("ad_revives_left_today"):
			left = int(es.call("ad_revives_left_today"))
		if "DAILY_AD_REVIVE_CAP" in es:
			cap = int(es.get("DAILY_AD_REVIVE_CAP"))
		if es.has_method("can_claim_ad_revive"):
			can_claim = bool(es.call("can_claim_ad_revive"))

	var ad_removed := _is_ad_removed()
	if _hint_lbl:
		if ad_removed:
			_hint_lbl.text = _t("二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！")
		else:
			_hint_lbl.text = _t("二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！")

	if _revive_btn:
		if can_claim:
			_revive_btn.disabled = false
			if ad_removed:
				_revive_btn.text = _t("已移除廣告，直接領取  (%d/%d)") % [left, cap]
			else:
				_revive_btn.text = _t("觀看廣告立即復活  (%d/%d)") % [left, cap]
		else:
			_revive_btn.disabled = true
			_revive_btn.text = _t("今日復活次數已達上限 (0/%d)") % cap

	if _tip_lbl:
		var has_refund := false
		if es:
			var target_mode := _mode
			if target_mode == "" and "last_spent_mode" in es:
				target_mode = str(es.get("last_spent_mode"))
			if es.has_method("is_boss_mode") and bool(es.call("is_boss_mode", target_mode)):
				var spent: int = int(es.get("last_spent_cost")) if "last_spent_cost" in es else 0
				if spent >= 3 or (spent == 0 and es.has_method("cost_for_mode") and int(es.call("cost_for_mode", target_mode)) >= 3):
					has_refund = true
		if has_refund:
			_tip_lbl.text = _t("若是選擇承認敗北，將返還 2 點能量並返回整頓。")
		else:
			_tip_lbl.text = _t("若是選擇承認敗北，將返回城鎮整頓裝備與招式。")


func _on_revive_ad_clicked() -> void:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es and es.has_method("can_claim_ad_revive") and not bool(es.call("can_claim_ad_revive")):
		return

	if _is_ad_removed():
		_on_ad_revive_success()
		return

	# 開啟假讀秒占位廣告
	MockAdDialogScript.show_ad(self, "revive", func():
		_on_ad_revive_success()
	)


func _on_ad_revive_success() -> void:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es and es.has_method("claim_ad_revive"):
		es.call("claim_ad_revive")

	revive_selected.emit()
	if _on_revive.is_valid():
		_on_revive.call()
	queue_free()


func _on_give_up_clicked() -> void:
	give_up_selected.emit()
	if _on_give_up.is_valid():
		_on_give_up.call()
	queue_free()


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


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 18
	sb.content_margin_right = 18
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.3)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb
