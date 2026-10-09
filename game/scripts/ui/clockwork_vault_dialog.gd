class_name ClockworkVaultDialog
extends Control
## 《發條之心》發條儲能庫放置收益彈窗 (ClockworkVaultDialog)
## 依據 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點二
## 規範：橫屏彈窗寬 720px、多巴胺鮮亮高飽和色盤、果凍厚底 5~6px、熱區 >= 48px、零系統 emoji、六語系支援

class LocHelper:
	static func t(k: String) -> String:
		var loop := Engine.get_main_loop()
		if loop is SceneTree:
			var loc_node = (loop as SceneTree).root.get_node_or_null("Loc")
			if loc_node != null and loc_node.has_method("t"):
				return str(loc_node.t(k))
		return k

const Loc = LocHelper

signal closed()
signal rewards_claimed(gold: int, scrap: int)

const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺鮮亮色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_OBSIDIAN   := Color(0.08, 0.07, 0.11, 0.96) ## 黑曜石卡片底
const COLOR_OBSIDIAN_SLOT := Color(0.04, 0.03, 0.06, 0.95) ## 凹槽黑曜石
const COLOR_BRASS_GOLD := Color(0.83, 0.68, 0.22, 1.0) ## 黃銅古典金

var _scrim: ColorRect
var _dialog_card: PanelContainer
var _title_label: Label
var _desc_label: Label
var _time_label: Label
var _progress_bar_bg: PanelContainer
var _progress_bar_fill: Panel
var _gold_num_label: Label
var _gold_title_label: Label
var _scrap_num_label: Label
var _scrap_title_label: Label
var _btn_claim: Button
var _btn_close: Button
var _cached_font: Font = null
var _fx_container: Control = null


func _init() -> void:
	name = "ClockworkVaultDialog"
	set_anchors_preset(Control.PRESET_FULL_RECT)


func _ready() -> void:
	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	_build_ui()
	refresh_display()

	var loc_node = Engine.get_main_loop().root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_signal("locale_changed"):
		loc_node.connect("locale_changed", Callable(self, "_on_locale_changed"))


func _exit_tree() -> void:
	var loc_node = Engine.get_main_loop().root.get_node_or_null("Loc")
	if loc_node != null and loc_node.is_connected("locale_changed", Callable(self, "_on_locale_changed")):
		loc_node.disconnect("locale_changed", Callable(self, "_on_locale_changed"))


func _on_locale_changed(_new_locale: String) -> void:
	_update_localized_texts()
	refresh_display()


func _build_ui() -> void:
	## 1. 全螢幕半透明遮罩
	_scrim = ColorRect.new()
	_scrim.name = "Scrim"
	_scrim.set_anchors_preset(Control.PRESET_FULL_RECT)
	_scrim.color = Color(0.02, 0.02, 0.04, 0.72)
	_scrim.gui_input.connect(func(ev: InputEvent):
		if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
			_on_close_pressed()
	)
	add_child(_scrim)

	## 特效圖層
	_fx_container = Control.new()
	_fx_container.name = "FxContainer"
	_fx_container.set_anchors_preset(Control.PRESET_FULL_RECT)
	_fx_container.mouse_filter = Control.MOUSE_FILTER_IGNORE

	## 2. 彈窗主體卡片 (寬 720, 高 460, 置中)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "VaultCard"
	_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
	_dialog_card.custom_minimum_size = Vector2(720, 460)
	_dialog_card.offset_left = -360
	_dialog_card.offset_right = 360
	_dialog_card.offset_top = -230
	_dialog_card.offset_bottom = 230

	var csb := StyleBoxFlat.new()
	csb.bg_color = COLOR_OBSIDIAN
	csb.border_color = COLOR_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 6
	csb.set_corner_radius_all(22)
	csb.content_margin_left = 28
	csb.content_margin_right = 28
	csb.content_margin_top = 22
	csb.content_margin_bottom = 24
	csb.shadow_color = Color(0.0, 0.0, 0.0, 0.45)
	csb.shadow_size = 18
	csb.shadow_offset = Vector2(0, 8)
	_dialog_card.add_theme_stylebox_override("panel", csb)
	add_child(_dialog_card)
	add_child(_fx_container)

	## 黃銅雙層內邊框
	var inner_rim := Panel.new()
	inner_rim.set_anchors_preset(Control.PRESET_FULL_RECT)
	inner_rim.offset_left = 4
	inner_rim.offset_top = 4
	inner_rim.offset_right = -4
	inner_rim.offset_bottom = -8
	inner_rim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var irsb := StyleBoxFlat.new()
	irsb.draw_center = false
	irsb.border_color = Color(0.83, 0.68, 0.22, 0.45)
	irsb.set_border_width_all(1)
	irsb.set_corner_radius_all(19)
	inner_rim.add_theme_stylebox_override("panel", irsb)
	_dialog_card.add_child(inner_rim)

	## 卡片內容主排版 (VBox)
	var main_vbox := VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 14)
	_dialog_card.add_child(main_vbox)

	## 頂部欄：標題徽章 + 右側關閉按鈕
	var head_hbox := HBoxContainer.new()
	head_hbox.alignment = BoxContainer.ALIGNMENT_BEGIN
	main_vbox.add_child(head_hbox)

	var title_badge := PanelContainer.new()
	var tbsb := StyleBoxFlat.new()
	tbsb.bg_color = Color(0.22, 0.18, 0.12, 0.9)
	tbsb.border_color = COLOR_BRASS_GOLD
	tbsb.set_border_width_all(1)
	tbsb.border_width_bottom = 3
	tbsb.set_corner_radius_all(14)
	tbsb.content_margin_left = 16
	tbsb.content_margin_right = 16
	tbsb.content_margin_top = 6
	tbsb.content_margin_bottom = 6
	title_badge.add_theme_stylebox_override("panel", tbsb)
	head_hbox.add_child(title_badge)

	_title_label = Label.new()
	_title_label.name = "VaultTitleLabel"
	_title_label.text = Loc.t("vault.popup_title")
	_title_label.add_theme_color_override("font_color", COLOR_GOLD)
	_title_label.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_title_label.add_theme_font_override("font", _cached_font)
	title_badge.add_child(_title_label)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head_hbox.add_child(spacer)

	## 關閉按鈕 (熱區 50x50, 果凍厚底 5px)
	_btn_close = Button.new()
	_btn_close.name = "CloseButton"
	_btn_close.text = "✕"
	_btn_close.custom_minimum_size = Vector2(50, 50)
	_btn_close.focus_mode = Control.FOCUS_NONE
	var close_sb := StyleBoxFlat.new()
	close_sb.bg_color = Color(0.18, 0.15, 0.22, 0.9)
	close_sb.border_color = COLOR_BORDER
	close_sb.set_border_width_all(2)
	close_sb.border_width_bottom = 5
	close_sb.set_corner_radius_all(16)
	_btn_close.add_theme_stylebox_override("normal", close_sb)
	_btn_close.add_theme_stylebox_override("hover", close_sb)
	_btn_close.add_theme_stylebox_override("pressed", close_sb)
	_btn_close.add_theme_color_override("font_color", Color("#F4EBD4"))
	_btn_close.add_theme_font_size_override("font_size", 18)
	_btn_close.pressed.connect(_on_close_pressed)
	head_hbox.add_child(_btn_close)

	## 說明文案
	_desc_label = Label.new()
	_desc_label.name = "VaultDescLabel"
	_desc_label.text = Loc.t("vault.desc")
	_desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_desc_label.add_theme_color_override("font_color", Color("#C9BFA8"))
	_desc_label.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		_desc_label.add_theme_font_override("font", _cached_font)
	main_vbox.add_child(_desc_label)

	## 儲能進度區：時間標籤 + 雙層立體果凍進度條
	var progress_box := VBoxContainer.new()
	progress_box.add_theme_constant_override("separation", 6)
	main_vbox.add_child(progress_box)

	var prog_head_hbox := HBoxContainer.new()
	progress_box.add_child(prog_head_hbox)

	var cap_title := Label.new()
	cap_title.text = Loc.t("vault.capacity")
	cap_title.add_theme_color_override("font_color", COLOR_BRASS_GOLD)
	cap_title.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		cap_title.add_theme_font_override("font", _cached_font)
	prog_head_hbox.add_child(cap_title)

	var prog_spacer := Control.new()
	prog_spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	prog_head_hbox.add_child(prog_spacer)

	_time_label = Label.new()
	_time_label.name = "VaultTimeLabel"
	_time_label.text = "00:00:00 / 08:00:00 (0%)"
	_time_label.add_theme_color_override("font_color", Color("#F4EBD4"))
	_time_label.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		_time_label.add_theme_font_override("font", _cached_font)
	prog_head_hbox.add_child(_time_label)

	## 進度條背景槽
	_progress_bar_bg = PanelContainer.new()
	_progress_bar_bg.name = "ProgressBarBg"
	_progress_bar_bg.custom_minimum_size = Vector2(0, 22)
	var pbsb := StyleBoxFlat.new()
	pbsb.bg_color = COLOR_OBSIDIAN_SLOT
	pbsb.border_color = COLOR_BORDER
	pbsb.set_border_width_all(2)
	pbsb.border_width_bottom = 4
	pbsb.set_corner_radius_all(11)
	_progress_bar_bg.add_theme_stylebox_override("panel", pbsb)
	_progress_bar_bg.resized.connect(func():
		if _progress_bar_fill and _progress_bar_bg:
			refresh_display()
	)
	progress_box.add_child(_progress_bar_bg)

	## 進度條填充 (以 Panel 自訂寬度實作平滑動畫)
	var fill_clip := Control.new()
	fill_clip.set_anchors_preset(Control.PRESET_FULL_RECT)
	fill_clip.clip_contents = true
	_progress_bar_bg.add_child(fill_clip)

	_progress_bar_fill = Panel.new()
	_progress_bar_fill.name = "ProgressBarFill"
	_progress_bar_fill.custom_minimum_size = Vector2(0, 20)
	var fillsb := StyleBoxFlat.new()
	fillsb.bg_color = COLOR_GOLD
	fillsb.border_color = Color("#FFA010")
	fillsb.set_border_width_all(1)
	fillsb.border_width_bottom = 3
	fillsb.set_corner_radius_all(10)
	_progress_bar_fill.add_theme_stylebox_override("panel", fillsb)
	fill_clip.add_child(_progress_bar_fill)

	## 獎勵展示區 (雙卡片 HBox)
	var cards_hbox := HBoxContainer.new()
	cards_hbox.add_theme_constant_override("separation", 18)
	cards_hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	main_vbox.add_child(cards_hbox)

	## 金幣獎勵卡
	var gold_card := PanelContainer.new()
	gold_card.custom_minimum_size = Vector2(310, 110)
	gold_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var gsb := StyleBoxFlat.new()
	gsb.bg_color = Color(0.12, 0.10, 0.15, 0.95)
	gsb.border_color = COLOR_BORDER
	gsb.set_border_width_all(2)
	gsb.border_width_bottom = 5
	gsb.set_corner_radius_all(16)
	gsb.content_margin_left = 16
	gsb.content_margin_right = 16
	gsb.content_margin_top = 12
	gsb.content_margin_bottom = 12
	gold_card.add_theme_stylebox_override("panel", gsb)
	cards_hbox.add_child(gold_card)

	var gv := VBoxContainer.new()
	gv.alignment = BoxContainer.ALIGNMENT_CENTER
	gv.add_theme_constant_override("separation", 4)
	gold_card.add_child(gv)

	_gold_title_label = Label.new()
	_gold_title_label.text = Loc.t("vault.gold_reward")
	_gold_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_gold_title_label.add_theme_color_override("font_color", COLOR_BRASS_GOLD)
	_gold_title_label.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		_gold_title_label.add_theme_font_override("font", _cached_font)
	gv.add_child(_gold_title_label)

	_gold_num_label = Label.new()
	_gold_num_label.name = "GoldNumLabel"
	_gold_num_label.text = "+ 0"
	_gold_num_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_gold_num_label.add_theme_color_override("font_color", COLOR_GOLD)
	_gold_num_label.add_theme_font_size_override("font_size", 28)
	if _cached_font:
		_gold_num_label.add_theme_font_override("font", _cached_font)
	gv.add_child(_gold_num_label)

	## 鐵屑獎勵卡
	var scrap_card := PanelContainer.new()
	scrap_card.custom_minimum_size = Vector2(310, 110)
	scrap_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var ssb := StyleBoxFlat.new()
	ssb.bg_color = Color(0.12, 0.10, 0.15, 0.95)
	ssb.border_color = COLOR_BORDER
	ssb.set_border_width_all(2)
	ssb.border_width_bottom = 5
	ssb.set_corner_radius_all(16)
	ssb.content_margin_left = 16
	ssb.content_margin_right = 16
	ssb.content_margin_top = 12
	ssb.content_margin_bottom = 12
	scrap_card.add_theme_stylebox_override("panel", ssb)
	cards_hbox.add_child(scrap_card)

	var sv := VBoxContainer.new()
	sv.alignment = BoxContainer.ALIGNMENT_CENTER
	sv.add_theme_constant_override("separation", 4)
	scrap_card.add_child(sv)

	_scrap_title_label = Label.new()
	_scrap_title_label.text = Loc.t("vault.scrap_reward")
	_scrap_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_scrap_title_label.add_theme_color_override("font_color", Color("#6B8CAE"))
	_scrap_title_label.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		_scrap_title_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_scrap_title_label)

	_scrap_num_label = Label.new()
	_scrap_num_label.name = "ScrapNumLabel"
	_scrap_num_label.text = "+ 0"
	_scrap_num_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_scrap_num_label.add_theme_color_override("font_color", COLOR_SKY)
	_scrap_num_label.add_theme_font_size_override("font_size", 28)
	if _cached_font:
		_scrap_num_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_scrap_num_label)

	## 底部操作按鈕：一鍵領取 (熱區 260x52, 厚底 6px, 立體果凍)
	var foot_box := HBoxContainer.new()
	foot_box.alignment = BoxContainer.ALIGNMENT_CENTER
	main_vbox.add_child(foot_box)

	_btn_claim = Button.new()
	_btn_claim.name = "ClaimButton"
	_btn_claim.custom_minimum_size = Vector2(260, 52)
	_btn_claim.focus_mode = Control.FOCUS_NONE

	var claim_sb := StyleBoxFlat.new()
	claim_sb.bg_color = COLOR_GOLD
	claim_sb.border_color = COLOR_BORDER
	claim_sb.set_border_width_all(2)
	claim_sb.border_width_bottom = 6
	claim_sb.set_corner_radius_all(18)
	_btn_claim.add_theme_stylebox_override("normal", claim_sb)
	_btn_claim.add_theme_stylebox_override("hover", claim_sb)
	_btn_claim.add_theme_stylebox_override("pressed", claim_sb)
	_btn_claim.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_claim.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_btn_claim.add_theme_font_override("font", _cached_font)
	_btn_claim.pressed.connect(_on_claim_pressed)
	foot_box.add_child(_btn_claim)


func _update_localized_texts() -> void:
	if _title_label:
		_title_label.text = Loc.t("vault.popup_title")
	if _desc_label:
		_desc_label.text = Loc.t("vault.desc")
	if _gold_title_label:
		_gold_title_label.text = Loc.t("vault.gold_reward")
	if _scrap_title_label:
		_scrap_title_label.text = Loc.t("vault.scrap_reward")


## 刷新顯示數值與進度條
func refresh_display() -> void:
	var st: Dictionary = IdleClockworkVault.get_status()
	var sec: float = float(st.get("elapsed_seconds", 0.0))
	var gold: int = int(st.get("gold", 0))
	var scrap: int = int(st.get("iron_scrap", 0))
	var ratio: float = float(st.get("progress_ratio", 0.0))
	var is_full: bool = bool(st.get("is_full", false))

	## 格式化時間 hh:mm:ss
	var hrs_i := int(sec / 3600.0)
	var mins_i := int(fmod(sec, 3600.0) / 60.0)
	var secs_i := int(fmod(sec, 60.0))
	var time_str := "%02d:%02d:%02d / 08:00:00" % [hrs_i, mins_i, secs_i]
	var pct_str := "(%d%%)" % int(ratio * 100.0)
	if is_full:
		pct_str = "[%s]" % Loc.t("vault.max_cap")

	if _time_label:
		_time_label.text = "%s %s" % [time_str, pct_str]

	if _gold_num_label:
		_gold_num_label.text = "+ %d" % gold
	if _scrap_num_label:
		_scrap_num_label.text = "+ %d" % scrap

	## 更新進度條寬度
	if _progress_bar_fill and _progress_bar_bg:
		var total_w: float = _progress_bar_bg.size.x - 4.0  ## 扣除左右邊框 2px*2
		if total_w < 300.0:
			total_w = 660.0  ## 預設寬度（未完成排版週期時使用卡片內槽寬 660px）
		var target_w: float = total_w * ratio
		_progress_bar_fill.visible = (ratio > 0.001)
		_progress_bar_fill.custom_minimum_size = Vector2(target_w, 20)
		_progress_bar_fill.size = Vector2(target_w, 20)

	## 更新領取按鈕狀態
	if _btn_claim:
		if gold > 0 or scrap > 0:
			_btn_claim.text = Loc.t("vault.btn_claim")
			_btn_claim.disabled = false
			_btn_claim.modulate = Color(1, 1, 1, 1)
		else:
			_btn_claim.text = Loc.t("vault.charging")
			_btn_claim.disabled = true
			_btn_claim.modulate = Color(0.7, 0.7, 0.7, 1)


func _on_claim_pressed() -> void:
	var res: Dictionary = IdleClockworkVault.claim()
	var g: int = int(res.get("gold", 0))
	var s: int = int(res.get("iron_scrap", 0))

	if g > 0 or s > 0:
		_play_dopamine_burst(g, s)
		rewards_claimed.emit(g, s)
	refresh_display()


func _on_close_pressed() -> void:
	closed.emit()
	queue_free()


func get_title_label() -> Label:
	return _title_label


func get_claim_button() -> Button:
	return _btn_claim


func get_close_button() -> Button:
	return _btn_close


func get_progress_bar_fill() -> Panel:
	return _progress_bar_fill


func get_progress_bar_bg() -> PanelContainer:
	return _progress_bar_bg


## 多巴胺金幣/鐵屑爆散反饋動效
func _play_dopamine_burst(gold: int, scrap: int) -> void:
	if _fx_container == null:
		return

	## 彈出多巴胺金屬金幣碎片粒子 (零系統字型符號、零 emoji，純視覺色塊)
	var center := size * 0.5
	for i in range(16):
		var spark := ColorRect.new()
		spark.custom_minimum_size = Vector2(8, 8)
		spark.size = Vector2(8, 8)
		spark.color = COLOR_GOLD if (i % 2 == 0) else COLOR_SKY
		spark.position = center + Vector2(randf_range(-20, 20), randf_range(-20, 20))
		_fx_container.add_child(spark)

		var target_pos := spark.position + Vector2(randf_range(-160, 160), randf_range(-140, -10))
		var tw := create_tween().set_parallel(true)
		tw.tween_property(spark, "position", target_pos, 0.6).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
		tw.tween_property(spark, "scale", Vector2(1.8, 1.8), 0.3)
		tw.tween_property(spark, "modulate:a", 0.0, 0.6)
		tw.chain().tween_callback(spark.queue_free)

	## 數字漂浮標籤
	var gain_label := Label.new()
	gain_label.text = "+%d 金幣  +%d 鐵屑" % [gold, scrap]
	gain_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	gain_label.add_theme_color_override("font_color", COLOR_GOLD)
	gain_label.add_theme_font_size_override("font_size", 24)
	if _cached_font:
		gain_label.add_theme_font_override("font", _cached_font)
	gain_label.position = center + Vector2(-150, -60)
	gain_label.size = Vector2(300, 40)
	_fx_container.add_child(gain_label)

	var gtw := create_tween()
	gtw.tween_property(gain_label, "position:y", gain_label.position.y - 45, 0.8).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	gtw.parallel().tween_property(gain_label, "modulate:a", 0.0, 0.8).set_delay(0.2)
	gtw.tween_callback(gain_label.queue_free)
